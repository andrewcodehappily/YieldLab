from __future__ import annotations

from app.models import CurveComparison, CurveMetrics, SpreadQuote, YieldCurve, YieldPoint


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


def yield_point_at(curve: YieldCurve, maturity_years: float) -> YieldPoint | None:
    return next(
        (
            point
            for point in curve.points
            if abs(point.maturity_years - maturity_years) < 1e-9
        ),
        None,
    )


def _spread_bp(long_yield: float | None, short_yield: float | None) -> float | None:
    if long_yield is None or short_yield is None:
        return None
    return round((long_yield - short_yield) * 100, 2)


def calculate_spread(
    curve: YieldCurve,
    short_maturity_years: float,
    long_maturity_years: float,
) -> SpreadQuote:
    if short_maturity_years >= long_maturity_years:
        raise ValueError("short maturity must be less than long maturity")

    short = yield_point_at(curve, short_maturity_years)
    long = yield_point_at(curve, long_maturity_years)
    if short is None or long is None:
        raise ValueError("requested maturity is not available in this curve")

    return SpreadQuote(
        as_of=curve.as_of,
        short_maturity_years=short.maturity_years,
        long_maturity_years=long.maturity_years,
        short_label=short.label,
        long_label=long.label,
        short_yield_pct=short.yield_pct,
        long_yield_pct=long.yield_pct,
        spread_bp=round((long.yield_pct - short.yield_pct) * 100, 2),
    )


def analyze_curve(curve: YieldCurve) -> CurveMetrics:
    ordered = sorted(curve.points, key=lambda point: point.maturity_years)
    if len(ordered) < 2:
        raise ValueError("A curve needs at least two maturity points")

    front_back = (ordered[-1].yield_pct - ordered[0].yield_pct) * 100
    two = yield_point_at(curve, 2)
    ten = yield_point_at(curve, 10)
    five = yield_point_at(curve, 5)
    thirty = yield_point_at(curve, 30)

    if front_back < -15:
        shape = "inverted"
    elif abs(front_back) <= 15:
        shape = "flat"
    else:
        shape = "normal"

    return CurveMetrics(
        two_ten_spread_bp=_spread_bp(
            ten.yield_pct if ten else None,
            two.yield_pct if two else None,
        ),
        five_thirty_spread_bp=_spread_bp(
            thirty.yield_pct if thirty else None,
            five.yield_pct if five else None,
        ),
        front_back_spread_bp=round(front_back, 2),
        shape=shape,
    )


def compare_curves(
    from_curve: YieldCurve,
    to_curve: YieldCurve,
    short_maturity_years: float = 2,
    long_maturity_years: float = 10,
    tolerance_bp: float = 1.0,
) -> CurveComparison:
    from_spread = calculate_spread(
        from_curve,
        short_maturity_years,
        long_maturity_years,
    )
    to_spread = calculate_spread(
        to_curve,
        short_maturity_years,
        long_maturity_years,
    )

    short_change = (to_spread.short_yield_pct - from_spread.short_yield_pct) * 100
    long_change = (to_spread.long_yield_pct - from_spread.long_yield_pct) * 100
    spread_change = to_spread.spread_bp - from_spread.spread_bp
    level_change = (short_change + long_change) / 2

    if level_change < -tolerance_bp:
        direction = "bull"
    elif level_change > tolerance_bp:
        direction = "bear"
    else:
        direction = "neutral"

    if spread_change > tolerance_bp:
        slope = "steepener"
    elif spread_change < -tolerance_bp:
        slope = "flattener"
    else:
        slope = "parallel"

    movement = f"{direction}_{slope}"

    return CurveComparison(
        from_date=from_curve.as_of,
        to_date=to_curve.as_of,
        short_label=from_spread.short_label,
        long_label=from_spread.long_label,
        short_change_bp=round(short_change, 2),
        long_change_bp=round(long_change, 2),
        spread_change_bp=round(spread_change, 2),
        level_change_bp=round(level_change, 2),
        movement=movement,
    )
