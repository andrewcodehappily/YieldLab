import pytest

from app.models import (
    CurveScenario,
    PortfolioPosition,
    PortfolioScenarioRequest,
    ShockPoint,
)
from app.services.curve import DEMO_CURVE
from app.services.scenarios import get_presets, shock_at_maturity, shock_curve, stress_portfolio


def test_shock_interpolates_between_anchors_and_adds_parallel_shift() -> None:
    scenario = CurveScenario(
        parallel_bp=10,
        shocks=[
            ShockPoint(maturity_years=2, shock_bp=100),
            ShockPoint(maturity_years=10, shock_bp=0),
        ],
    )
    assert shock_at_maturity(scenario, 2) == 110
    assert shock_at_maturity(scenario, 6) == 60
    assert shock_at_maturity(scenario, 10) == 10


def test_parallel_curve_shock_preserves_two_ten_spread() -> None:
    result = shock_curve(DEMO_CURVE, CurveScenario(name="up", parallel_bp=100))
    assert all(point.shock_bp == 100 for point in result.points)
    assert result.base_two_ten_spread_bp == result.shocked_two_ten_spread_bp
    assert result.two_ten_spread_change_bp == 0
    assert result.movement == "bear_parallel"


def test_portfolio_reprices_exactly_under_rate_shock() -> None:
    request = PortfolioScenarioRequest(
        scenario=CurveScenario(name="up100", parallel_bp=100),
        positions=[
            PortfolioPosition(
                name="10Y par bond",
                face_value=100_000,
                coupon_rate_pct=5,
                yield_to_maturity_pct=5,
                maturity_years=10,
                payments_per_year=2,
            )
        ],
    )
    result = stress_portfolio(request)
    assert result.market_value_before == pytest.approx(100_000, abs=1e-4)
    assert result.market_value_after < result.market_value_before
    assert result.pnl < 0
    assert result.positions[0].shock_bp == 100
    assert result.positions[0].shocked_yield_pct == 6
    assert result.dv01 > 0
    assert result.weighted_modified_duration > 0
    assert result.weighted_convexity > 0


def test_zero_shock_has_zero_portfolio_pnl() -> None:
    result = stress_portfolio(
        PortfolioScenarioRequest(
            scenario=CurveScenario(name="unchanged"),
            positions=[
                PortfolioPosition(
                    name="5Y",
                    face_value=50_000,
                    coupon_rate_pct=4,
                    yield_to_maturity_pct=4,
                    maturity_years=5,
                    payments_per_year=2,
                )
            ],
        )
    )
    assert result.pnl == pytest.approx(0, abs=1e-6)
    assert result.pnl_pct == pytest.approx(0, abs=1e-9)


def test_standard_scenario_presets_are_available() -> None:
    keys = {preset.key for preset in get_presets()}
    assert {
        "parallel_up_100",
        "parallel_down_100",
        "bull_steepener",
        "bull_flattener",
        "bear_steepener",
        "bear_flattener",
    }.issubset(keys)
