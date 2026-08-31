import pytest

from app.models import BondRequest
from app.services.bonds import analyze_bond


def test_par_bond_prices_at_face_value() -> None:
    result = analyze_bond(
        BondRequest(
            face_value=1000,
            coupon_rate_pct=5,
            yield_to_maturity_pct=5,
            maturity_years=10,
            payments_per_year=2,
        )
    )
    assert result.price == pytest.approx(1000, abs=1e-6)
    assert result.modified_duration > 0
    assert result.convexity > 0
    assert result.dv01 > 0


def test_zero_coupon_bond_prices_below_par_for_positive_yield() -> None:
    result = analyze_bond(
        BondRequest(
            face_value=1000,
            coupon_rate_pct=0,
            yield_to_maturity_pct=5,
            maturity_years=5,
            payments_per_year=1,
        )
    )
    assert result.price == pytest.approx(1000 / (1.05**5), rel=1e-6)


def test_maturity_must_align_with_payment_frequency() -> None:
    with pytest.raises(ValueError):
        BondRequest(
            coupon_rate_pct=4,
            yield_to_maturity_pct=4,
            maturity_years=1.2,
            payments_per_year=2,
        )
