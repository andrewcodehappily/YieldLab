from __future__ import annotations

from app.models import CurveMetrics, YieldCurve, YieldPoint


DEMO_CURVE = YieldCurve(
    as_of="demo",
    source="YieldLab built-in demo data",
    points=[
        YieldPoint(maturity_years=0.25, yield_pct=4.72, label="3M"),
        YieldPoint(maturity_years=0.5, yield_pct=4.50, label="6M"),
        YieldPoint(maturity_years=1, yield_pct=4.18, label="1Y"),
        YieldPoint(maturity_years=2, yield_pct=3.92, label="2Y"),
        YieldPoint(maturity_years=5, yield_pct=3.78, label="5Y"),
        YieldPoint(maturity_years=10, yield_pct=4.02, label="10Y"),
        YieldPoint(maturity_years=30, yield_pct=4.41, label="30Y"),
    ],
)


def _yield_at(curve: YieldCurve, maturity_years: float) -> float | None:
    for point in curve.points:
        if abs(point.maturity_years - maturity_years) < 1e-9:
            return point.yield_pct
    return None


def _spread_bp(long_yield: float | None, short_yield: float | None) -> float | None:
    if long_yield is None or short_yield is None:
        return None
    return round((long_yield - short_yield) * 100, 2)


def analyze_curve(curve: YieldCurve) -> CurveMetrics:
    ordered = sorted(curve.points, key=lambda point: point.maturity_years)
    if len(ordered) < 2:
        raise ValueError("A curve needs at least two maturity points")

    front_back = (ordered[-1].yield_pct - ordered[0].yield_pct) * 100

    if front_back < -15:
        shape = "inverted"
    elif abs(front_back) <= 15:
        shape = "flat"
    else:
        shape = "normal"

    return CurveMetrics(
        two_ten_spread_bp=_spread_bp(_yield_at(curve, 10), _yield_at(curve, 2)),
        five_thirty_spread_bp=_spread_bp(_yield_at(curve, 30), _yield_at(curve, 5)),
        front_back_spread_bp=round(front_back, 2),
        shape=shape,
    )
