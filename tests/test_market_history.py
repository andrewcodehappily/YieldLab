import pytest

from app.services.market_history import build_inversion_view, load_market_history


def test_market_history_cache_covers_long_horizon() -> None:
    data = load_market_history()
    assert data.start_date.startswith("1950-")
    assert data.end_date.startswith("2026-")
    assert len(data.points) > 900
    assert data.points[0].sp500_close > 0
    assert data.points[-1].sp500_close > data.points[0].sp500_close
    assert data.acm_maturities_years == list(range(1, 11))


def test_acm_components_start_in_1961_and_satisfy_identity() -> None:
    data = load_market_history()
    available = [point for point in data.points if point.acm_fitted_yields_pct is not None]
    assert available[0].date.startswith("1961-06")
    assert len(available) > 700

    sample = available[len(available) // 2]
    assert sample.acm_term_premia_pct is not None
    assert sample.acm_expected_avg_short_rates_pct is not None
    for fitted, premium, expected in zip(
        sample.acm_fitted_yields_pct or [],
        sample.acm_term_premia_pct,
        sample.acm_expected_avg_short_rates_pct,
    ):
        assert fitted == pytest.approx(expected + premium, abs=1e-6)


def test_user_inversion_inequality_matches_acm_fitted_spread_sign() -> None:
    view = build_inversion_view(load_market_history(), t1_years=2, t2_years=10)
    available = [point for point in view.points if point.inverted is not None]
    assert available
    assert any(point.inverted for point in available)
    assert any(not point.inverted for point in available)

    for point in available:
        assert point.expected_path_difference_bp is not None
        assert point.term_premium_threshold_bp is not None
        assert point.fitted_yield_spread_bp is not None
        assert point.inverted == (
            point.expected_path_difference_bp < point.term_premium_threshold_bp
        )
        assert point.inverted == (point.fitted_yield_spread_bp < 0)


def test_market_history_supports_maturity_and_date_ranges() -> None:
    view = build_inversion_view(
        load_market_history(),
        t1_years=5,
        t2_years=9,
        start_month="2000-03",
        end_month="2010-08",
    )
    assert view.t1_years == 5
    assert view.t2_years == 9
    assert view.start_date.startswith("2000-03")
    assert view.end_date.startswith("2010-08")


def test_six_month_event_study_uses_inversion_ends() -> None:
    view = build_inversion_view(
        load_market_history(),
        t1_years=2,
        t2_years=10,
        start_month="1961-06",
        end_month="2026-09",
    )
    assert view.events
    assert view.event_summary.event_count == len(view.events)
    assert view.event_summary.completed_event_count <= view.event_summary.event_count

    points_by_month = {point.date[:7]: point for point in view.points}
    for event in view.events:
        end_month = event.inversion_end_date[:7]
        end_point = points_by_month[end_month]
        year, month = map(int, end_month.split("-"))
        previous_year = year if month > 1 else year - 1
        previous_month = month - 1 if month > 1 else 12
        previous_key = f"{previous_year:04d}-{previous_month:02d}"
        assert end_point.inverted is False
        assert points_by_month[previous_key].inverted is True

    completed = [event for event in view.events if event.completed]
    assert completed
    assert all(event.six_month_return_pct is not None for event in completed)
    assert all(event.max_drawdown_pct is not None and event.max_drawdown_pct <= 0 for event in completed)
    assert 0 <= (view.event_summary.negative_return_pct or 0) <= 100


def test_invalid_maturity_order_is_rejected() -> None:
    with pytest.raises(ValueError):
        build_inversion_view(load_market_history(), t1_years=10, t2_years=2)
