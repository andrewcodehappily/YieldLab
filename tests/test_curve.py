from app.models import YieldCurve, YieldPoint
from app.services.curve import DEMO_CURVE, analyze_curve, calculate_spread, compare_curves


def test_demo_curve_metrics() -> None:
    metrics = analyze_curve(DEMO_CURVE)
    assert metrics.two_ten_spread_bp == 10.0
    assert metrics.five_thirty_spread_bp == 63.0
    assert metrics.front_back_spread_bp == -31.0
    assert metrics.shape == "inverted"


def test_custom_spread_uses_long_minus_short() -> None:
    quote = calculate_spread(DEMO_CURVE, 2, 30)
    assert quote.short_label == "2Y"
    assert quote.long_label == "30Y"
    assert quote.spread_bp == 49.0


def test_curve_comparison_classifies_bull_steepener() -> None:
    old = YieldCurve(
        as_of="2026-01-01",
        source="test",
        points=[
            YieldPoint(maturity_years=2, yield_pct=5.0, label="2Y"),
            YieldPoint(maturity_years=10, yield_pct=5.0, label="10Y"),
        ],
    )
    new = YieldCurve(
        as_of="2026-01-02",
        source="test",
        points=[
            YieldPoint(maturity_years=2, yield_pct=4.0, label="2Y"),
            YieldPoint(maturity_years=10, yield_pct=4.5, label="10Y"),
        ],
    )

    comparison = compare_curves(old, new)
    assert comparison.short_change_bp == -100.0
    assert comparison.long_change_bp == -50.0
    assert comparison.spread_change_bp == 50.0
    assert comparison.level_change_bp == -75.0
    assert comparison.movement == "bull_steepener"
