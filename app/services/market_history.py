from __future__ import annotations

import json
from pathlib import Path

from app.models import MarketHistoryData, MarketInversionData, MarketInversionPoint

PROJECT_DIR = Path(__file__).resolve().parents[2]
MARKET_HISTORY_FILE = PROJECT_DIR / "data" / "sp500_inversion_history.json"


def load_market_history(path: Path = MARKET_HISTORY_FILE) -> MarketHistoryData:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return MarketHistoryData.model_validate(payload)


def build_inversion_view(
    data: MarketHistoryData,
    t1_years: int,
    t2_years: int,
    start_year: int = 1950,
    end_year: int = 2026,
) -> MarketInversionData:
    if t1_years not in data.acm_maturities_years or t2_years not in data.acm_maturities_years:
        raise ValueError("T1 and T2 must be available ACM maturities")
    if t1_years >= t2_years:
        raise ValueError("T1 must be shorter than T2")
    if start_year > end_year:
        raise ValueError("start_year must not exceed end_year")

    t1_index = data.acm_maturities_years.index(t1_years)
    t2_index = data.acm_maturities_years.index(t2_years)
    selected: list[MarketInversionPoint] = []

    for point in data.points:
        year = int(point.date[:4])
        if year < start_year or year > end_year:
            continue

        fitted = point.acm_fitted_yields_pct
        premia = point.acm_term_premia_pct
        expected = point.acm_expected_avg_short_rates_pct
        if fitted is None or premia is None or expected is None:
            selected.append(
                MarketInversionPoint(
                    date=point.date,
                    sp500_close=point.sp500_close,
                )
            )
            continue

        expected_diff_bp = (expected[t2_index] - expected[t1_index]) * 100
        premium_threshold_bp = (premia[t1_index] - premia[t2_index]) * 100
        fitted_spread_bp = (fitted[t2_index] - fitted[t1_index]) * 100

        # The user's inequality is algebraically equivalent to a negative ACM fitted-yield spread:
        # RNY(T2)-RNY(T1) < TP(T1)-TP(T2)  <=>  Y(T2)-Y(T1) < 0.
        inverted = expected_diff_bp < premium_threshold_bp

        # Guard against malformed source data by enforcing the ACM decomposition identity numerically.
        if abs(fitted_spread_bp - (expected_diff_bp - premium_threshold_bp)) > 1e-3:
            raise ValueError("ACM decomposition identity failed for market-history observation")

        selected.append(
            MarketInversionPoint(
                date=point.date,
                sp500_close=point.sp500_close,
                expected_path_difference_bp=round(expected_diff_bp, 6),
                term_premium_threshold_bp=round(premium_threshold_bp, 6),
                fitted_yield_spread_bp=round(fitted_spread_bp, 6),
                inverted=inverted,
            )
        )

    if not selected:
        raise ValueError("No market-history observations exist in the requested date range")

    return MarketInversionData(
        start_date=selected[0].date,
        end_date=selected[-1].date,
        t1_years=t1_years,
        t2_years=t2_years,
        sp500_source=data.sp500_source,
        rates_source=data.rates_source,
        methodology=(
            "ACM decomposition inversion: Eavg(T2)-Eavg(T1) < L(T1)-L(T2), "
            "where Eavg is ACMRNY and L(T) is the ACM term premium"
        ),
        points=selected,
    )
