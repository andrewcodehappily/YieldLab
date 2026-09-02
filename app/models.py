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


class CurveHistory(BaseModel):
    curves: list[YieldCurve]


class SpreadQuote(BaseModel):
    as_of: str
    short_maturity_years: float
    long_maturity_years: float
    short_label: str
    long_label: str
    short_yield_pct: float
    long_yield_pct: float
    spread_bp: float


class CurveComparison(BaseModel):
    from_date: str
    to_date: str
    short_label: str
    long_label: str
    short_change_bp: float
    long_change_bp: float
    spread_change_bp: float
    level_change_bp: float
    movement: str


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


class ShockPoint(BaseModel):
    maturity_years: float = Field(gt=0)
    shock_bp: float = Field(ge=-2000, le=2000)


class CurveScenario(BaseModel):
    name: str = Field(default="custom", min_length=1, max_length=80)
    parallel_bp: float = Field(default=0.0, ge=-2000, le=2000)
    shocks: list[ShockPoint] = Field(default_factory=list, max_length=32)

    @model_validator(mode="after")
    def unique_shock_maturities(self) -> "CurveScenario":
        maturities = [round(point.maturity_years, 12) for point in self.shocks]
        if len(maturities) != len(set(maturities)):
            raise ValueError("scenario shock maturities must be unique")
        return self


class ScenarioPreset(BaseModel):
    key: str
    scenario: CurveScenario


class ShockedYieldPoint(BaseModel):
    maturity_years: float
    label: str
    base_yield_pct: float
    shock_bp: float
    shocked_yield_pct: float


class CurveShockResult(BaseModel):
    as_of: str
    scenario_name: str
    points: list[ShockedYieldPoint]
    base_two_ten_spread_bp: float | None
    shocked_two_ten_spread_bp: float | None
    two_ten_spread_change_bp: float | None
    movement: str | None


class PortfolioPosition(BondRequest):
    name: str = Field(min_length=1, max_length=80)


class PortfolioScenarioRequest(BaseModel):
    positions: list[PortfolioPosition] = Field(min_length=1, max_length=100)
    scenario: CurveScenario


class PositionScenarioResult(BaseModel):
    name: str
    maturity_years: float
    face_value: float
    base_yield_pct: float
    shock_bp: float
    shocked_yield_pct: float
    market_value_before: float
    market_value_after: float
    pnl: float
    pnl_pct: float
    dv01: float
    modified_duration: float
    convexity: float


class PortfolioScenarioResult(BaseModel):
    scenario_name: str
    market_value_before: float
    market_value_after: float
    pnl: float
    pnl_pct: float
    dv01: float
    weighted_modified_duration: float
    weighted_convexity: float
    positions: list[PositionScenarioResult]


class CurveFitPoint(BaseModel):
    maturity_years: float
    observed_yield_pct: float | None = None
    fitted_yield_pct: float


class CurveFitResult(BaseModel):
    as_of: str
    model: str
    rmse_bp: float
    parameters: dict[str, float]
    points: list[CurveFitPoint]


class FittedYieldQuote(BaseModel):
    as_of: str
    model: str
    maturity_years: float
    fitted_yield_pct: float
    rmse_bp: float


class ForwardRateQuote(BaseModel):
    as_of: str
    model: str
    start_years: float
    end_years: float
    start_yield_pct: float
    end_yield_pct: float
    forward_rate_pct: float
    methodology: str


class PcaFactorSummary(BaseModel):
    name: str
    explained_variance_pct: float
    latest_score_bp: float
    score_std_bp: float
    latest_sigma: float


class PcaLoadingPoint(BaseModel):
    maturity_years: float
    label: str
    level: float
    slope: float
    curvature: float


class PcaAnalysis(BaseModel):
    start_date: str
    end_date: str
    trading_days: int
    change_observations: int
    factors: list[PcaFactorSummary]
    loadings: list[PcaLoadingPoint]


class FactorShockRequest(BaseModel):
    level_sigma: float = Field(default=0.0, ge=-10, le=10)
    slope_sigma: float = Field(default=0.0, ge=-10, le=10)
    curvature_sigma: float = Field(default=0.0, ge=-10, le=10)


class FactorShockResult(BaseModel):
    scenario: CurveScenario
    shock_result: CurveShockResult


class MarketHistoryPoint(BaseModel):
    date: str
    sp500_close: float
    acm_fitted_yields_pct: list[float] | None = None
    acm_term_premia_pct: list[float] | None = None
    acm_expected_avg_short_rates_pct: list[float] | None = None


class MarketHistoryData(BaseModel):
    start_date: str
    end_date: str
    sp500_source: str
    rates_source: str
    acm_maturities_years: list[int]
    points: list[MarketHistoryPoint]


class MarketInversionPoint(BaseModel):
    date: str
    sp500_close: float
    expected_path_difference_bp: float | None = None
    term_premium_threshold_bp: float | None = None
    fitted_yield_spread_bp: float | None = None
    inverted: bool | None = None


class InversionEventResult(BaseModel):
    inversion_start_date: str
    six_month_date: str | None = None
    start_sp500: float
    six_month_sp500: float | None = None
    six_month_return_pct: float | None = None
    max_drawdown_pct: float | None = None
    max_drawdown_date: str | None = None
    completed: bool


class InversionEventSummary(BaseModel):
    event_count: int
    completed_event_count: int
    negative_return_count: int
    negative_return_pct: float | None = None
    average_return_pct: float | None = None
    median_return_pct: float | None = None
    worst_return_pct: float | None = None
    average_max_drawdown_pct: float | None = None
    worst_max_drawdown_pct: float | None = None


class MarketInversionData(BaseModel):
    start_date: str
    end_date: str
    t1_years: int
    t2_years: int
    sp500_source: str
    rates_source: str
    methodology: str
    points: list[MarketInversionPoint]
    events: list[InversionEventResult] = Field(default_factory=list)
    event_summary: InversionEventSummary
