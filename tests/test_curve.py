from app.services.curve import DEMO_CURVE, analyze_curve


def test_demo_curve_metrics() -> None:
    metrics = analyze_curve(DEMO_CURVE)
    assert metrics.two_ten_spread_bp == 10.0
    assert metrics.five_thirty_spread_bp == 63.0
    assert metrics.front_back_spread_bp == -31.0
    assert metrics.shape == "inverted"
