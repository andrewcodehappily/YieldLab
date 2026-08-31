from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.models import BondAnalytics, BondRequest, CurveMetrics, YieldCurve
from app.services.bonds import analyze_bond
from app.services.curve import analyze_curve
from app.services.treasury import get_current_curve

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="YieldLab",
    version="0.1.0",
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


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "yieldlab", "version": "0.1.0"}


@app.get("/api/curve", response_model=YieldCurve)
def get_curve() -> YieldCurve:
    return get_current_curve()


@app.get("/api/curve/metrics", response_model=CurveMetrics)
def get_curve_metrics() -> CurveMetrics:
    return analyze_curve(get_current_curve())


@app.post("/api/bonds/analyze", response_model=BondAnalytics)
def bond_analytics(bond: BondRequest) -> BondAnalytics:
    return analyze_bond(bond)
