from __future__ import annotations

from app.models import BondAnalytics, BondRequest


def analyze_bond(bond: BondRequest) -> BondAnalytics:
    frequency = bond.payments_per_year
    periods = int(round(bond.maturity_years * frequency))
    period_yield = bond.yield_to_maturity_pct / 100 / frequency
    coupon = bond.face_value * (bond.coupon_rate_pct / 100) / frequency

    cashflows: list[tuple[int, float]] = []
    for period in range(1, periods + 1):
        cashflow = coupon + (bond.face_value if period == periods else 0.0)
        cashflows.append((period, cashflow))

    if abs(period_yield) < 1e-15:
        discounted = [(period, cashflow, cashflow) for period, cashflow in cashflows]
    else:
        discounted = [
            (period, cashflow, cashflow / ((1 + period_yield) ** period))
            for period, cashflow in cashflows
        ]

    price = sum(pv for _, _, pv in discounted)

    macaulay_periods = sum(period * pv for period, _, pv in discounted) / price
    macaulay_duration = macaulay_periods / frequency
    modified_duration = macaulay_duration / (1 + period_yield)

    # Standard discrete-compounding convexity, expressed in years^2.
    convexity_periods = sum(
        period * (period + 1) * pv for period, _, pv in discounted
    ) / (price * ((1 + period_yield) ** 2))
    convexity = convexity_periods / (frequency**2)

    # DV01 is the price change for an approximately one-basis-point yield move.
    dv01 = modified_duration * price * 0.0001

    return BondAnalytics(
        price=round(price, 6),
        macaulay_duration=round(macaulay_duration, 6),
        modified_duration=round(modified_duration, 6),
        convexity=round(convexity, 6),
        dv01=round(dv01, 6),
    )
