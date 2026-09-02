from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.models import (
    BondAnalytics,
    BondRequest,
    CurveComparison,
    CurveFitResult,
    CurveHistory,
    CurveMetrics,
    CurveScenario,
    CurveShockResult,
    FactorShockRequest,
    FactorShockResult,
    FittedYieldQuote,
    ForwardRateQuote,
    MarketInversionData,
    PcaAnalysis,
    PortfolioScenarioRequest,
    PortfolioScenarioResult,
    ScenarioPreset,
    SpreadQuote,
    YieldCurve,
)
from app.services.bonds import analyze_bond
from app.services.curve import analyze_curve, calculate_spread, compare_curves
from app.services.factors import analyze_pca, factor_shock
from app.services.fitting import fit_curve, fitted_yield_quote, forward_rate_quote
from app.services.history import get_curve_by_date, load_history, merge_history
from app.services.market_history import build_inversion_view, load_market_history
from app.services.scenarios import get_presets, shock_curve, stress_portfolio
from app.services.treasury import get_current_curve

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
VERSION = "0.4.2"
CurveModel = Literal["nelson_siegel", "svensson"]

app = FastAPI(
    title="YieldLab",
    version=VERSION,
    description="Fixed-income analytics, yield-curve modelling, factor analysis, and interest-rate stress testing lab",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


def _available_history() -> list[YieldCurve]:
    try:
        history = load_history()
    except (OSError, json.JSONDecodeError, ValueError):
        history = []
    return merge_history(history, [get_current_curve()])


def _curve_for_date(as_of: str | None) -> YieldCurve:
    if as_of is None:
        return get_current_curve()
    curve = get_curve_by_date(_available_history(), as_of)
    if curve is None:
        raise HTTPException(status_code=404, detail=f"No curve available for {as_of}")
    return curve


def _history_window(limit: int) -> list[YieldCurve]:
    history = _available_history()
    if len(history) < 4:
        raise HTTPException(status_code=422, detail="At least four trading days are required for PCA")
    return history[-limit:]


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "yieldlab", "version": VERSION}


@app.get("/api/curve", response_model=YieldCurve)
def get_curve(as_of: str | None = None) -> YieldCurve:
    return _curve_for_date(as_of)


@app.get("/api/curve/metrics", response_model=CurveMetrics)
def get_curve_metrics(as_of: str | None = None) -> CurveMetrics:
    return analyze_curve(_curve_for_date(as_of))


@app.get("/api/curves/history", response_model=CurveHistory)
def get_curve_history(
    limit: int = Query(default=90, ge=1, le=1000),
) -> CurveHistory:
    curves = _available_history()
    return CurveHistory(curves=curves[-limit:])


@app.get("/api/market/sp500-inversions", response_model=MarketInversionData)
def get_sp500_inversion_history(
    t1: int = Query(default=2, ge=1, le=9),
    t2: int = Query(default=10, ge=2, le=10),
    start_year: int = Query(default=1950, ge=1950, le=2026),
    end_year: int = Query(default=2026, ge=1950, le=2026),
) -> MarketInversionData:
    try:
        return build_inversion_view(
            load_market_history(),
            t1_years=t1,
            t2_years=t2,
            start_year=start_year,
            end_year=end_year,
        )
    except (OSError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=503, detail="Market history cache is unavailable") from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/api/spread", response_model=SpreadQuote)
def get_spread(
    short: float = Query(gt=0),
    long: float = Query(gt=0),
    as_of: str | None = None,
) -> SpreadQuote:
    try:
        return calculate_spread(_curve_for_date(as_of), short, long)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/api/curve/compare", response_model=CurveComparison)
def get_curve_comparison(
    from_date: str,
    to_date: str,
    short: float = Query(default=2, gt=0),
    long: float = Query(default=10, gt=0),
) -> CurveComparison:
    history = _available_history()
    from_curve = get_curve_by_date(history, from_date)
    to_curve = get_curve_by_date(history, to_date)
    if from_curve is None:
        raise HTTPException(status_code=404, detail=f"No curve available for {from_date}")
    if to_curve is None:
        raise HTTPException(status_code=404, detail=f"No curve available for {to_date}")

    try:
        return compare_curves(from_curve, to_curve, short, long)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/api/curve/fit", response_model=CurveFitResult)
def get_curve_fit(
    model: CurveModel = "svensson",
    as_of: str | None = None,
    grid_points: int = Query(default=121, ge=20, le=400),
) -> CurveFitResult:
    try:
        return fit_curve(_curve_for_date(as_of), model=model, grid_points=grid_points)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/api/curve/fitted-yield", response_model=FittedYieldQuote)
def get_fitted_yield(
    maturity: float = Query(gt=0, le=30),
    model: CurveModel = "svensson",
    as_of: str | None = None,
) -> FittedYieldQuote:
    try:
        return fitted_yield_quote(_curve_for_date(as_of), maturity_years=maturity, model=model)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/api/curve/forward", response_model=ForwardRateQuote)
def get_forward_rate(
    start: float = Query(gt=0, le=30),
    end: float = Query(gt=0, le=30),
    model: CurveModel = "svensson",
    as_of: str | None = None,
) -> ForwardRateQuote:
    try:
        return forward_rate_quote(
            _curve_for_date(as_of),
            start_years=start,
            end_years=end,
            model=model,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/api/factors/pca", response_model=PcaAnalysis)
def get_pca_analysis(
    limit: int = Query(default=180, ge=4, le=1000),
) -> PcaAnalysis:
    try:
        return analyze_pca(_history_window(limit))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/api/factors/shock", response_model=FactorShockResult)
def apply_factor_shock(
    request: FactorShockRequest,
    as_of: str | None = None,
    limit: int = Query(default=180, ge=4, le=1000),
) -> FactorShockResult:
    try:
        return factor_shock(_history_window(limit), _curve_for_date(as_of), request)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/api/scenarios/presets", response_model=list[ScenarioPreset])
def get_scenario_presets() -> list[ScenarioPreset]:
    return list(get_presets())


@app.post("/api/scenarios/curve", response_model=CurveShockResult)
def apply_curve_scenario(
    scenario: CurveScenario,
    as_of: str | None = None,
) -> CurveShockResult:
    return shock_curve(_curve_for_date(as_of), scenario)


@app.post("/api/portfolio/stress", response_model=PortfolioScenarioResult)
def portfolio_stress_test(request: PortfolioScenarioRequest) -> PortfolioScenarioResult:
    try:
        return stress_portfolio(request)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/api/bonds/analyze", response_model=BondAnalytics)
def bond_analytics(bond: BondRequest) -> BondAnalytics:
    return analyze_bond(bond)
