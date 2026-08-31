from __future__ import annotations

from pydantic import BaseModel, Field, model_validator


class YieldPoint(BaseModel):
    maturity_years: float = Field(gt=0)
    yield_pct: float
    label: str


class YieldCurve(BaseModel):
    as_of: str
    source: str
    points: list[YieldPoint]


class BondRequest(BaseModel):
    face_value: float = Field(default=1000.0, gt=0)
    coupon_rate_pct: float = Field(ge=0)
    yield_to_maturity_pct: float
    maturity_years: float = Field(gt=0)
    payments_per_year: int = Field(default=2, ge=1, le=12)

    @model_validator(mode="after")
    def validate_bond_terms(self) -> "BondRequest":
        periods = self.maturity_years * self.payments_per_year
        if abs(periods - round(periods)) > 1e-9:
            raise ValueError("maturity_years must align with payments_per_year")

        period_yield = self.yield_to_maturity_pct / 100 / self.payments_per_year
        if period_yield <= -1:
            raise ValueError("yield_to_maturity_pct produces an invalid discount factor")
        return self


class BondAnalytics(BaseModel):
    price: float
    macaulay_duration: float
    modified_duration: float
    convexity: float
    dv01: float


class CurveMetrics(BaseModel):
    two_ten_spread_bp: float | None
    five_thirty_spread_bp: float | None
    front_back_spread_bp: float
    shape: str
