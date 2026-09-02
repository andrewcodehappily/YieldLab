import math

from app.models import FactorShockRequest, YieldCurve, YieldPoint
from app.services.factors import analyze_pca, build_factor_scenario


MATURITIES = [1.0, 2.0, 5.0, 10.0, 30.0]


def _synthetic_history(days: int = 24) -> list[YieldCurve]:
    base = [4.0, 4.1, 4.2, 4.3, 4.4]
    level = [1, 1, 1, 1, 1]
    slope = [-2, -1, 0, 1, 2]
    curvature = [-1, 0.5, 1, 0.5, -1]

    current = base[:]
    curves = []
    for day in range(days):
        if day:
            a = 0.018 * math.sin(day * 0.73)
            b = 0.010 * math.cos(day * 0.41)
            c = 0.007 * math.sin(day * 1.13)
            current = [
                value + a * level[i] + b * slope[i] + c * curvature[i]
                for i, value in enumerate(current)
            ]
        curves.append(
            YieldCurve(
                as_of=f"2026-01-{day + 1:02d}",
                source="synthetic",
                points=[
                    YieldPoint(maturity_years=maturity, yield_pct=current[i], label=f"{maturity:g}Y")
                    for i, maturity in enumerate(MATURITIES)
                ],
            )
        )
    return curves


def test_pca_labels_level_slope_and_curvature() -> None:
    result = analyze_pca(_synthetic_history())
    factors = {factor.name: factor for factor in result.factors}
    assert set(factors) == {"level", "slope", "curvature"}
    assert result.change_observations == 23
    assert sum(f.explained_variance_pct for f in result.factors) > 99

    level_loadings = [point.level for point in result.loadings]
    slope_loadings = [point.slope for point in result.loadings]
    curvature_loadings = [point.curvature for point in result.loadings]

    assert min(level_loadings) > 0
    assert slope_loadings[0] < slope_loadings[-1]
    assert curvature_loadings[2] > curvature_loadings[0]
    assert curvature_loadings[2] > curvature_loadings[-1]


def test_one_sigma_level_shock_is_upward_on_average() -> None:
    scenario = build_factor_scenario(
        _synthetic_history(),
        FactorShockRequest(level_sigma=1, slope_sigma=0, curvature_sigma=0),
    )
    assert len(scenario.shocks) == len(MATURITIES)
    assert sum(point.shock_bp for point in scenario.shocks) / len(scenario.shocks) > 0
