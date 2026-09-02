from __future__ import annotations

from math import sqrt

import numpy as np
from scipy.optimize import least_squares

from app.models import CurveFitPoint, CurveFitResult, FittedYieldQuote, ForwardRateQuote, YieldCurve


_MODEL_PARAMETER_NAMES = {
    "nelson_siegel": ("beta0", "beta1", "beta2", "tau1"),
    "svensson": ("beta0", "beta1", "beta2", "beta3", "tau1", "tau2"),
}


def _loading_1(maturity: np.ndarray, tau: float) -> np.ndarray:
    x = maturity / tau
    return np.where(np.abs(x) < 1e-10, 1.0, -np.expm1(-x) / x)


def _loading_2(maturity: np.ndarray, tau: float) -> np.ndarray:
    x = maturity / tau
    return _loading_1(maturity, tau) - np.exp(-x)


def nelson_siegel_yield(maturity: np.ndarray, parameters: np.ndarray) -> np.ndarray:
    beta0, beta1, beta2, tau1 = parameters
    return beta0 + beta1 * _loading_1(maturity, tau1) + beta2 * _loading_2(maturity, tau1)


def svensson_yield(maturity: np.ndarray, parameters: np.ndarray) -> np.ndarray:
    beta0, beta1, beta2, beta3, tau1, tau2 = parameters
    return (
        beta0
        + beta1 * _loading_1(maturity, tau1)
        + beta2 * _loading_2(maturity, tau1)
        + beta3 * _loading_2(maturity, tau2)
    )


def _model_function(model: str):
    if model == "nelson_siegel":
        return nelson_siegel_yield
    if model == "svensson":
        return svensson_yield
    raise ValueError("model must be 'nelson_siegel' or 'svensson'")


def _fit_parameters(curve: YieldCurve, model: str) -> tuple[np.ndarray, float]:
    if len(curve.points) < 4:
        raise ValueError("curve fitting requires at least four maturity points")

    maturities = np.asarray([point.maturity_years for point in curve.points], dtype=float)
    yields = np.asarray([point.yield_pct for point in curve.points], dtype=float)
    order = np.argsort(maturities)
    maturities = maturities[order]
    yields = yields[order]

    model_fn = _model_function(model)
    long_rate = float(yields[-1])
    short_rate = float(yields[0])

    if model == "nelson_siegel":
        lower = np.asarray([-10.0, -30.0, -30.0, 0.03])
        upper = np.asarray([20.0, 30.0, 30.0, 40.0])
        seeds = [
            [long_rate, short_rate - long_rate, 0.0, 1.5],
            [long_rate, short_rate - long_rate, 2.0, 3.0],
            [long_rate, short_rate - long_rate, -2.0, 0.75],
            [float(np.mean(yields)), short_rate - long_rate, 1.0, 7.0],
        ]
    else:
        lower = np.asarray([-10.0, -30.0, -30.0, -30.0, 0.03, 0.03])
        upper = np.asarray([20.0, 30.0, 30.0, 30.0, 40.0, 40.0])
        seeds = [
            [long_rate, short_rate - long_rate, 0.0, 0.0, 1.5, 5.0],
            [long_rate, short_rate - long_rate, 2.0, -1.0, 0.75, 7.0],
            [long_rate, short_rate - long_rate, -2.0, 2.0, 3.0, 12.0],
            [float(np.mean(yields)), short_rate - long_rate, 1.0, -1.0, 5.0, 1.0],
        ]

    def residuals(parameters: np.ndarray) -> np.ndarray:
        return model_fn(maturities, parameters) - yields

    best = None
    for seed in seeds:
        result = least_squares(
            residuals,
            np.asarray(seed, dtype=float),
            bounds=(lower, upper),
            max_nfev=6000,
            xtol=1e-12,
            ftol=1e-12,
            gtol=1e-12,
        )
        if best is None or result.cost < best.cost:
            best = result

    if best is None or not np.all(np.isfinite(best.x)):
        raise ValueError("curve fitting failed")

    fitted = model_fn(maturities, best.x)
    rmse_bp = sqrt(float(np.mean((fitted - yields) ** 2))) * 100
    return best.x, rmse_bp


def fitted_yield_pct(model: str, parameters: np.ndarray, maturity_years: float) -> float:
    if maturity_years <= 0:
        raise ValueError("maturity must be positive")
    value = _model_function(model)(np.asarray([maturity_years], dtype=float), parameters)[0]
    return float(value)


def fit_curve(curve: YieldCurve, model: str = "svensson", grid_points: int = 121) -> CurveFitResult:
    if grid_points < 20 or grid_points > 400:
        raise ValueError("grid_points must be between 20 and 400")

    parameters, rmse_bp = _fit_parameters(curve, model)
    observed = {round(point.maturity_years, 12): point.yield_pct for point in curve.points}

    min_maturity = min(point.maturity_years for point in curve.points)
    max_maturity = max(point.maturity_years for point in curve.points)
    dense = np.geomspace(min_maturity, max_maturity, grid_points)
    all_maturities = sorted(
        {round(float(value), 12) for value in dense}
        | {round(point.maturity_years, 12) for point in curve.points}
    )

    points = [
        CurveFitPoint(
            maturity_years=maturity,
            observed_yield_pct=observed.get(round(maturity, 12)),
            fitted_yield_pct=round(fitted_yield_pct(model, parameters, maturity), 6),
        )
        for maturity in all_maturities
    ]

    names = _MODEL_PARAMETER_NAMES[model]
    return CurveFitResult(
        as_of=curve.as_of,
        model=model,
        rmse_bp=round(rmse_bp, 6),
        parameters={name: round(float(value), 8) for name, value in zip(names, parameters)},
        points=points,
    )


def fitted_yield_quote(
    curve: YieldCurve,
    maturity_years: float,
    model: str = "svensson",
) -> FittedYieldQuote:
    max_maturity = max(point.maturity_years for point in curve.points)
    if maturity_years > max_maturity:
        raise ValueError("fitted-yield queries must stay within the observed curve range")
    parameters, rmse_bp = _fit_parameters(curve, model)
    return FittedYieldQuote(
        as_of=curve.as_of,
        model=model,
        maturity_years=maturity_years,
        fitted_yield_pct=round(fitted_yield_pct(model, parameters, maturity_years), 6),
        rmse_bp=round(rmse_bp, 6),
    )


def forward_rate_quote(
    curve: YieldCurve,
    start_years: float,
    end_years: float,
    model: str = "svensson",
) -> ForwardRateQuote:
    if start_years <= 0 or end_years <= 0 or start_years >= end_years:
        raise ValueError("forward-rate maturities must satisfy 0 < start < end")
    max_maturity = max(point.maturity_years for point in curve.points)
    if end_years > max_maturity:
        raise ValueError("forward-rate queries must stay within the observed curve range")

    parameters, _ = _fit_parameters(curve, model)
    start_yield = fitted_yield_pct(model, parameters, start_years)
    end_yield = fitted_yield_pct(model, parameters, end_years)

    # The Treasury input is a par-yield curve. For an educational forward-rate view,
    # YieldLab treats the fitted yield curve as a continuously compounded zero curve.
    # This is an approximation, not a full coupon-bond bootstrap.
    forward = (end_yield * end_years - start_yield * start_years) / (end_years - start_years)

    return ForwardRateQuote(
        as_of=curve.as_of,
        model=model,
        start_years=start_years,
        end_years=end_years,
        start_yield_pct=round(start_yield, 6),
        end_yield_pct=round(end_yield, 6),
        forward_rate_pct=round(forward, 6),
        methodology="continuous-compounding zero-curve approximation from fitted Treasury par yields",
    )
