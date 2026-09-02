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
        start_year=2000,
        end_year=2010,
    )
    assert view.t1_years == 5
    assert view.t2_years == 9
    assert view.start_date.startswith("2000-")
    assert view.end_date.startswith("2010-")


def test_invalid_maturity_order_is_rejected() -> None:
    with pytest.raises(ValueError):
        build_inversion_view(load_market_history(), t1_years=10, t2_years=2)
