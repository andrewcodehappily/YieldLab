from __future__ import annotations

from app.models import (
    BondRequest,
    CurveScenario,
    CurveShockResult,
    PortfolioPosition,
    PortfolioScenarioRequest,
    PortfolioScenarioResult,
    PositionScenarioResult,
    ScenarioPreset,
    ShockedYieldPoint,
    ShockPoint,
    YieldCurve,
    YieldPoint,
)
from app.services.bonds import analyze_bond
from app.services.curve import calculate_spread, compare_curves


PRESETS: tuple[ScenarioPreset, ...] = (
    ScenarioPreset(
        key="parallel_up_100",
        scenario=CurveScenario(name="parallel_up_100", parallel_bp=100),
    ),
    ScenarioPreset(
        key="parallel_down_100",
        scenario=CurveScenario(name="parallel_down_100", parallel_bp=-100),
    ),
    ScenarioPreset(
        key="bull_steepener",
        scenario=CurveScenario(
            name="bull_steepener",
            shocks=[
                ShockPoint(maturity_years=0.25, shock_bp=-100),
                ShockPoint(maturity_years=2, shock_bp=-100),
                ShockPoint(maturity_years=10, shock_bp=-50),
                ShockPoint(maturity_years=30, shock_bp=-25),
            ],
        ),
    ),
    ScenarioPreset(
        key="bull_flattener",
        scenario=CurveScenario(
            name="bull_flattener",
            shocks=[
                ShockPoint(maturity_years=0.25, shock_bp=-25),
                ShockPoint(maturity_years=2, shock_bp=-25),
                ShockPoint(maturity_years=10, shock_bp=-50),
                ShockPoint(maturity_years=30, shock_bp=-75),
            ],
        ),
    ),
    ScenarioPreset(
        key="bear_steepener",
        scenario=CurveScenario(
            name="bear_steepener",
            shocks=[
                ShockPoint(maturity_years=0.25, shock_bp=25),
                ShockPoint(maturity_years=2, shock_bp=25),
                ShockPoint(maturity_years=10, shock_bp=50),
                ShockPoint(maturity_years=30, shock_bp=75),
            ],
        ),
    ),
    ScenarioPreset(
        key="bear_flattener",
        scenario=CurveScenario(
            name="bear_flattener",
            shocks=[
                ShockPoint(maturity_years=0.25, shock_bp=100),
                ShockPoint(maturity_years=2, shock_bp=100),
                ShockPoint(maturity_years=10, shock_bp=50),
                ShockPoint(maturity_years=30, shock_bp=25),
            ],
        ),
    ),
)


def get_presets() -> tuple[ScenarioPreset, ...]:
    return PRESETS


def shock_at_maturity(scenario: CurveScenario, maturity_years: float) -> float:
    anchors = sorted(scenario.shocks, key=lambda point: point.maturity_years)
    shaped_shock = 0.0

    if anchors:
        if maturity_years <= anchors[0].maturity_years:
            shaped_shock = anchors[0].shock_bp
        elif maturity_years >= anchors[-1].maturity_years:
            shaped_shock = anchors[-1].shock_bp
        else:
            for left, right in zip(anchors, anchors[1:]):
                if left.maturity_years <= maturity_years <= right.maturity_years:
                    span = right.maturity_years - left.maturity_years
                    weight = (maturity_years - left.maturity_years) / span
                    shaped_shock = left.shock_bp + weight * (right.shock_bp - left.shock_bp)
                    break

    return round(scenario.parallel_bp + shaped_shock, 6)


def shock_curve(curve: YieldCurve, scenario: CurveScenario) -> CurveShockResult:
    shocked_points: list[ShockedYieldPoint] = []
    shocked_curve_points: list[YieldPoint] = []

    for point in curve.points:
        shock_bp = shock_at_maturity(scenario, point.maturity_years)
        shocked_yield = point.yield_pct + shock_bp / 100
        shocked_points.append(
            ShockedYieldPoint(
                maturity_years=point.maturity_years,
                label=point.label,
                base_yield_pct=point.yield_pct,
                shock_bp=shock_bp,
                shocked_yield_pct=round(shocked_yield, 6),
            )
        )
        shocked_curve_points.append(
            YieldPoint(
                maturity_years=point.maturity_years,
                label=point.label,
                yield_pct=round(shocked_yield, 6),
            )
        )

    shocked_curve = YieldCurve(
        as_of=curve.as_of,
        source=f"YieldLab scenario: {scenario.name}",
        points=shocked_curve_points,
    )

    base_two_ten = None
    shocked_two_ten = None
    spread_change = None
    movement = None
    try:
        base_quote = calculate_spread(curve, 2, 10)
        shocked_quote = calculate_spread(shocked_curve, 2, 10)
        base_two_ten = base_quote.spread_bp
        shocked_two_ten = shocked_quote.spread_bp
        spread_change = round(shocked_two_ten - base_two_ten, 6)
        movement = compare_curves(curve, shocked_curve, 2, 10).movement
    except ValueError:
        pass

    return CurveShockResult(
        as_of=curve.as_of,
        scenario_name=scenario.name,
        points=shocked_points,
        base_two_ten_spread_bp=base_two_ten,
        shocked_two_ten_spread_bp=shocked_two_ten,
        two_ten_spread_change_bp=spread_change,
        movement=movement,
    )


def _bond_from_position(position: PortfolioPosition, ytm_pct: float) -> BondRequest:
    return BondRequest(
        face_value=position.face_value,
        coupon_rate_pct=position.coupon_rate_pct,
        yield_to_maturity_pct=ytm_pct,
        maturity_years=position.maturity_years,
        payments_per_year=position.payments_per_year,
    )


def stress_portfolio(request: PortfolioScenarioRequest) -> PortfolioScenarioResult:
    results: list[PositionScenarioResult] = []

    total_before = 0.0
    total_after = 0.0
    total_dv01 = 0.0
    duration_numerator = 0.0
    convexity_numerator = 0.0

    for position in request.positions:
        shock_bp = shock_at_maturity(request.scenario, position.maturity_years)
        shocked_yield = position.yield_to_maturity_pct + shock_bp / 100

        before = analyze_bond(_bond_from_position(position, position.yield_to_maturity_pct))
        after = analyze_bond(_bond_from_position(position, shocked_yield))

        pnl = after.price - before.price
        pnl_pct = (pnl / before.price * 100) if before.price else 0.0

        total_before += before.price
        total_after += after.price
        total_dv01 += before.dv01
        duration_numerator += before.modified_duration * before.price
        convexity_numerator += before.convexity * before.price

        results.append(
            PositionScenarioResult(
                name=position.name,
                maturity_years=position.maturity_years,
                face_value=position.face_value,
                base_yield_pct=position.yield_to_maturity_pct,
                shock_bp=shock_bp,
                shocked_yield_pct=round(shocked_yield, 6),
                market_value_before=round(before.price, 6),
                market_value_after=round(after.price, 6),
                pnl=round(pnl, 6),
                pnl_pct=round(pnl_pct, 6),
                dv01=round(before.dv01, 6),
                modified_duration=round(before.modified_duration, 6),
                convexity=round(before.convexity, 6),
            )
        )

    pnl = total_after - total_before
    pnl_pct = (pnl / total_before * 100) if total_before else 0.0

    return PortfolioScenarioResult(
        scenario_name=request.scenario.name,
        market_value_before=round(total_before, 6),
        market_value_after=round(total_after, 6),
        pnl=round(pnl, 6),
        pnl_pct=round(pnl_pct, 6),
        dv01=round(total_dv01, 6),
        weighted_modified_duration=round(duration_numerator / total_before, 6),
        weighted_convexity=round(convexity_numerator / total_before, 6),
        positions=results,
    )
