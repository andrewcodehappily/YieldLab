import numpy as np
import pytest

from app.models import YieldCurve, YieldPoint
from app.services.fitting import (
    fit_curve,
    forward_rate_quote,
    nelson_siegel_yield,
)


def _synthetic_ns_curve() -> YieldCurve:
    maturities = np.asarray([0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30], dtype=float)
    parameters = np.asarray([4.7, -1.0, 1.8, 2.2], dtype=float)
    yields = nelson_siegel_yield(maturities, parameters)
    return YieldCurve(
        as_of="2026-01-01",
        source="synthetic",
        points=[
            YieldPoint(maturity_years=float(maturity), yield_pct=float(rate), label=f"{maturity:g}Y")
            for maturity, rate in zip(maturities, yields)
        ],
    )


def test_nelson_siegel_fits_synthetic_curve() -> None:
    result = fit_curve(_synthetic_ns_curve(), model="nelson_siegel", grid_points=60)
    assert result.model == "nelson_siegel"
    assert result.rmse_bp < 0.01
    assert len(result.points) >= 60
    assert {"beta0", "beta1", "beta2", "tau1"} == set(result.parameters)


def test_forward_rate_is_flat_for_flat_curve() -> None:
    curve = YieldCurve(
        as_of="2026-01-01",
        source="flat",
        points=[
            YieldPoint(maturity_years=maturity, yield_pct=5.0, label=f"{maturity:g}Y")
            for maturity in [0.5, 1, 2, 5, 10, 20, 30]
        ],
    )
    quote = forward_rate_quote(curve, 5, 10, model="nelson_siegel")
    assert quote.forward_rate_pct == pytest.approx(5.0, abs=1e-4)
    assert "approximation" in quote.methodology


def test_forward_rate_rejects_reversed_window() -> None:
    with pytest.raises(ValueError):
        forward_rate_quote(_synthetic_ns_curve(), 10, 5, model="nelson_siegel")
