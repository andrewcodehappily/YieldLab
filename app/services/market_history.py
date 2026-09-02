from __future__ import annotations

import json
from pathlib import Path
from statistics import mean, median

from app.models import (
    InversionEventResult,
    InversionEventSummary,
    MarketHistoryData,
    MarketInversionData,
    MarketInversionPoint,
)

PROJECT_DIR = Path(__file__).resolve().parents[2]
MARKET_HISTORY_FILE = PROJECT_DIR / "data" / "sp500_inversion_history.json"


def load_market_history(path: Path = MARKET_HISTORY_FILE) -> MarketHistoryData:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return MarketHistoryData.model_validate(payload)


def _month_key(date: str) -> str:
    return date[:7]


def _validate_month(value: str) -> str:
    if len(value) != 7 or value[4] != "-":
        raise ValueError("month must use YYYY-MM format")
    year = int(value[:4])
    month = int(value[5:7])
    if year < 1950 or not 1 <= month <= 12:
        raise ValueError("month is outside the supported history range")
    return value


def _add_months(month: str, months: int) -> str:
    year = int(month[:4])
    month_number = int(month[5:7]) - 1 + months
    target_year = year + month_number // 12
    target_month = month_number % 12 + 1
    return f"{target_year:04d}-{target_month:02d}"


def _point_for_maturities(
    point,
    t1_index: int,
    t2_index: int,
) -> MarketInversionPoint:
    fitted = point.acm_fitted_yields_pct
    premia = point.acm_term_premia_pct
    expected = point.acm_expected_avg_short_rates_pct
    if fitted is None or premia is None or expected is None:
        return MarketInversionPoint(date=point.date, sp500_close=point.sp500_close)

    expected_diff_bp = (expected[t2_index] - expected[t1_index]) * 100
    premium_threshold_bp = (premia[t1_index] - premia[t2_index]) * 100
    fitted_spread_bp = (fitted[t2_index] - fitted[t1_index]) * 100

    # User definition:
    # Eavg(T2)-Eavg(T1) < L(T1)-L(T2)
    # With the ACM decomposition Y(T)=Eavg(T)+L(T), this is equivalent to Y(T2)-Y(T1)<0.
    inverted = expected_diff_bp < premium_threshold_bp

    if abs(fitted_spread_bp - (expected_diff_bp - premium_threshold_bp)) > 1e-3:
        raise ValueError("ACM decomposition identity failed for market-history observation")

    return MarketInversionPoint(
        date=point.date,
        sp500_close=point.sp500_close,
        expected_path_difference_bp=round(expected_diff_bp, 6),
        term_premium_threshold_bp=round(premium_threshold_bp, 6),
        fitted_yield_spread_bp=round(fitted_spread_bp, 6),
        inverted=inverted,
    )


def _event_results(
    all_points: list[MarketInversionPoint],
    selected_start_month: str,
    selected_end_month: str,
) -> list[InversionEventResult]:
    by_month = {_month_key(point.date): point for point in all_points}
    events: list[InversionEventResult] = []

    previous_valid_state: bool | None = None
    for point in all_points:
        current_state = point.inverted
        if current_state is None:
            previous_valid_state = None
            continue

        month = _month_key(point.date)
        started = current_state is True and previous_valid_state is False
        previous_valid_state = current_state
        if not started or month < selected_start_month or month > selected_end_month:
            continue

        target_month = _add_months(month, 6)
        target = by_month.get(target_month)
        if target is None:
            events.append(
                InversionEventResult(
                    inversion_start_date=point.date,
                    start_sp500=point.sp500_close,
                    completed=False,
                )
            )
            continue

        start_index = all_points.index(point)
        target_index = all_points.index(target)
        window = all_points[start_index : target_index + 1]
        running_peak = window[0].sp500_close
        max_drawdown = 0.0
        max_drawdown_date = window[0].date
        for observation in window:
            running_peak = max(running_peak, observation.sp500_close)
            drawdown = (observation.sp500_close / running_peak - 1) * 100
            if drawdown < max_drawdown:
                max_drawdown = drawdown
                max_drawdown_date = observation.date

        six_month_return = (target.sp500_close / point.sp500_close - 1) * 100
        events.append(
            InversionEventResult(
                inversion_start_date=point.date,
                six_month_date=target.date,
                start_sp500=round(point.sp500_close, 6),
                six_month_sp500=round(target.sp500_close, 6),
                six_month_return_pct=round(six_month_return, 6),
                max_drawdown_pct=round(max_drawdown, 6),
                max_drawdown_date=max_drawdown_date,
                completed=True,
            )
        )

    return events


def _event_summary(events: list[InversionEventResult]) -> InversionEventSummary:
    completed = [event for event in events if event.completed and event.six_month_return_pct is not None]
    returns = [event.six_month_return_pct for event in completed if event.six_month_return_pct is not None]
    drawdowns = [event.max_drawdown_pct for event in completed if event.max_drawdown_pct is not None]
    negative_count = sum(value < 0 for value in returns)

    return InversionEventSummary(
        event_count=len(events),
        completed_event_count=len(completed),
        negative_return_count=negative_count,
        negative_return_pct=round(negative_count / len(completed) * 100, 6) if completed else None,
        average_return_pct=round(mean(returns), 6) if returns else None,
        median_return_pct=round(median(returns), 6) if returns else None,
        worst_return_pct=round(min(returns), 6) if returns else None,
        average_max_drawdown_pct=round(mean(drawdowns), 6) if drawdowns else None,
        worst_max_drawdown_pct=round(min(drawdowns), 6) if drawdowns else None,
    )


def build_inversion_view(
    data: MarketHistoryData,
    t1_years: int,
    t2_years: int,
    start_year: int = 1950,
    end_year: int = 2026,
    start_month: str | None = None,
    end_month: str | None = None,
) -> MarketInversionData:
    if t1_years not in data.acm_maturities_years or t2_years not in data.acm_maturities_years:
        raise ValueError("T1 and T2 must be available ACM maturities")
    if t1_years >= t2_years:
        raise ValueError("T1 must be shorter than T2")
    if start_year > end_year:
        raise ValueError("start_year must not exceed end_year")

    selected_start_month = _validate_month(start_month) if start_month else f"{start_year:04d}-01"
    selected_end_month = _validate_month(end_month) if end_month else f"{end_year:04d}-12"
    if selected_start_month > selected_end_month:
        raise ValueError("start month must not exceed end month")

    t1_index = data.acm_maturities_years.index(t1_years)
    t2_index = data.acm_maturities_years.index(t2_years)
    all_points = [_point_for_maturities(point, t1_index, t2_index) for point in data.points]
    selected = [
        point
        for point in all_points
        if selected_start_month <= _month_key(point.date) <= selected_end_month
    ]
    if not selected:
        raise ValueError("No market-history observations exist in the requested date range")

    events = _event_results(all_points, selected_start_month, selected_end_month)
    summary = _event_summary(events)

    return MarketInversionData(
        start_date=selected[0].date,
        end_date=selected[-1].date,
        t1_years=t1_years,
        t2_years=t2_years,
        sp500_source=data.sp500_source,
        rates_source=data.rates_source,
        methodology=(
            "ACM decomposition inversion: Eavg(T2)-Eavg(T1) < L(T1)-L(T2), "
            "where Eavg is ACMRNY and L(T) is the ACM term premium. "
            "Six-month event study starts when the state changes from non-inverted to inverted; "
            "drawdowns use monthly S&P 500 observations."
        ),
        points=selected,
        events=events,
        event_summary=summary,
    )
