from app.services.market_history import load_market_history


def test_market_history_cache_covers_long_horizon() -> None:
    data = load_market_history()
    assert data.start_date.startswith("1950-")
    assert data.end_date.startswith("2026-")
    assert len(data.points) > 900
    assert data.points[0].sp500_close > 0
    assert data.points[-1].sp500_close > data.points[0].sp500_close


def test_inversion_series_have_expected_historical_coverage() -> None:
    data = load_market_history()
    ten_three = [point for point in data.points if point.spread_10y3m_bp is not None]
    ten_two = [point for point in data.points if point.spread_10y2y_bp is not None]

    assert ten_three[0].date.startswith("1953-04")
    assert ten_two[0].date.startswith("1976-06")
    assert any(point.spread_10y3m_bp < 0 for point in ten_three)
    assert any(point.spread_10y2y_bp < 0 for point in ten_two)
