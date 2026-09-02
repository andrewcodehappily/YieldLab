from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.models import (
    BondAnalytics,
    BondRequest,
    CurveComparison,
    CurveHistory,
    CurveMetrics,
    SpreadQuote,
    YieldCurve,
)
from app.services.bonds import analyze_bond
from app.services.curve import analyze_curve, calculate_spread, compare_curves
from app.services.history import get_curve_by_date, load_history, merge_history
from app.services.treasury import get_current_curve

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="YieldLab",
    version="0.2.0",
    description="Fixed-income analytics and yield-curve research lab",
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


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "yieldlab", "version": "0.2.0"}


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


@app.post("/api/bonds/analyze", response_model=BondAnalytics)
def bond_analytics(bond: BondRequest) -> BondAnalytics:
    return analyze_bond(bond)
