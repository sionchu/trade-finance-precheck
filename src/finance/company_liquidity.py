import csv
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation
from enum import Enum
from io import StringIO

from src.domain.deal_case import DealCase, FxRates
from src.finance.engine import dated_cashflows
from src.finance.liquidity import WorkingCapitalCreditLine


ZERO = Decimal("0")
CSV_COLUMNS = ("event_date", "category", "amount_krw", "status", "reference")


class CompanyCashEventCategory(Enum):
    AR_COLLECTION = "AR_COLLECTION"
    AP_PAYMENT = "AP_PAYMENT"
    PAYROLL_TAX = "PAYROLL_TAX"
    DEBT_SERVICE = "DEBT_SERVICE"
    CAPEX = "CAPEX"
    OTHER = "OTHER"


class CompanyCashEventStatus(Enum):
    CONFIRMED = "CONFIRMED"
    EXPECTED = "EXPECTED"


class CompanyCashEventSource(Enum):
    MANUAL = "MANUAL"
    ERP_IMPORT = "ERP_IMPORT"


@dataclass(frozen=True)
class CompanyCashEvent:
    event_date: date
    category: CompanyCashEventCategory
    amount_krw: Decimal
    status: CompanyCashEventStatus
    source: CompanyCashEventSource
    reference: str

    def __post_init__(self) -> None:
        if not isinstance(self.event_date, date):
            raise ValueError("event_date must be a date")
        if not isinstance(self.amount_krw, Decimal) or not self.amount_krw.is_finite():
            raise ValueError("amount_krw must be a finite Decimal")
        if not self.reference.strip():
            raise ValueError("reference must not be blank")


@dataclass(frozen=True)
class CompanyLiquidityInput:
    as_of_date: date
    current_available_cash_krw: Decimal
    minimum_operating_cash_krw: Decimal
    existing_cash_events: tuple[CompanyCashEvent, ...]
    include_expected_events: bool = False

    def __post_init__(self) -> None:
        for name, value in (
            ("current_available_cash_krw", self.current_available_cash_krw),
            ("minimum_operating_cash_krw", self.minimum_operating_cash_krw),
        ):
            if not value.is_finite() or value < ZERO:
                raise ValueError(f"{name} must be a finite nonnegative Decimal")
        if any(event.event_date < self.as_of_date for event in self.existing_cash_events):
            raise ValueError("company cash events cannot precede as_of_date")

    @property
    def raw_starting_liquidity_after_buffer_krw(self) -> Decimal:
        return self.current_available_cash_krw - self.minimum_operating_cash_krw

    @property
    def starting_surplus_liquidity_krw(self) -> Decimal:
        return max(ZERO, self.raw_starting_liquidity_after_buffer_krw)


@dataclass(frozen=True)
class CompanyLiquidityPoint:
    event_date: date
    day_offset: int
    existing_company_cashflow_krw: Decimal
    prospective_deal_cashflow_krw: Decimal
    net_cashflow_krw: Decimal
    cumulative_available_liquidity_krw: Decimal
    minimum_cash_buffer_krw: Decimal
    liquidity_surplus_after_buffer_krw: Decimal
    required_external_funding_krw: Decimal


@dataclass(frozen=True)
class CompanyLiquidityTimeline:
    as_of_date: date
    points: tuple[CompanyLiquidityPoint, ...]
    minimum_projected_cash_krw: Decimal
    minimum_projected_cash_date: date
    peak_liquidity_gap_krw: Decimal
    peak_liquidity_gap_date: date
    ending_projected_cash_krw: Decimal


@dataclass(frozen=True)
class CompanyDealLiquidityComparison:
    company_without_deal: CompanyLiquidityTimeline
    company_with_deal: CompanyLiquidityTimeline
    incremental_peak_gap_from_deal_krw: Decimal


@dataclass(frozen=True)
class CompanyLiquidityCreditCapacity:
    company_peak_liquidity_gap_krw: Decimal
    unused_credit_limit_krw: Decimal
    credit_headroom_krw: Decimal
    liquidity_gap_krw: Decimal
    feasible: bool


def _included_company_events(
    liquidity_input: CompanyLiquidityInput,
) -> tuple[CompanyCashEvent, ...]:
    return tuple(
        event
        for event in liquidity_input.existing_cash_events
        if liquidity_input.include_expected_events
        or event.status is CompanyCashEventStatus.CONFIRMED
    )


def _build_timeline(
    liquidity_input: CompanyLiquidityInput,
    deal_events_by_date: dict[date, Decimal],
) -> CompanyLiquidityTimeline:
    company_by_date: dict[date, Decimal] = {}
    for event in _included_company_events(liquidity_input):
        company_by_date[event.event_date] = (
            company_by_date.get(event.event_date, ZERO) + event.amount_krw
        )

    event_dates = sorted(
        {liquidity_input.as_of_date, *company_by_date, *deal_events_by_date}
    )
    projected_cash = liquidity_input.current_available_cash_krw
    points = []
    for event_date in event_dates:
        company_flow = company_by_date.get(event_date, ZERO)
        deal_flow = deal_events_by_date.get(event_date, ZERO)
        net_flow = company_flow + deal_flow
        projected_cash += net_flow
        surplus = projected_cash - liquidity_input.minimum_operating_cash_krw
        points.append(
            CompanyLiquidityPoint(
                event_date=event_date,
                day_offset=(event_date - liquidity_input.as_of_date).days,
                existing_company_cashflow_krw=company_flow,
                prospective_deal_cashflow_krw=deal_flow,
                net_cashflow_krw=net_flow,
                cumulative_available_liquidity_krw=projected_cash,
                minimum_cash_buffer_krw=liquidity_input.minimum_operating_cash_krw,
                liquidity_surplus_after_buffer_krw=surplus,
                required_external_funding_krw=max(ZERO, -surplus),
            )
        )

    minimum_point = min(points, key=lambda point: point.cumulative_available_liquidity_krw)
    peak_gap_point = max(points, key=lambda point: point.required_external_funding_krw)
    return CompanyLiquidityTimeline(
        as_of_date=liquidity_input.as_of_date,
        points=tuple(points),
        minimum_projected_cash_krw=minimum_point.cumulative_available_liquidity_krw,
        minimum_projected_cash_date=minimum_point.event_date,
        peak_liquidity_gap_krw=peak_gap_point.required_external_funding_krw,
        peak_liquidity_gap_date=peak_gap_point.event_date,
        ending_projected_cash_krw=points[-1].cumulative_available_liquidity_krw,
    )


def analyze_company_liquidity(
    *,
    liquidity_input: CompanyLiquidityInput,
    deal: DealCase,
    fx: FxRates,
) -> CompanyDealLiquidityComparison:
    frozen_events, _ = dated_cashflows(deal, fx)
    deal_events_by_date = {
        liquidity_input.as_of_date + timedelta(days=event.day): event.amount_krw
        for event in frozen_events
    }
    without_deal = _build_timeline(liquidity_input, {})
    with_deal = _build_timeline(liquidity_input, deal_events_by_date)
    return CompanyDealLiquidityComparison(
        company_without_deal=without_deal,
        company_with_deal=with_deal,
        incremental_peak_gap_from_deal_krw=(
            with_deal.peak_liquidity_gap_krw
            - without_deal.peak_liquidity_gap_krw
        ),
    )


def compare_company_gap_to_credit_line(
    timeline: CompanyLiquidityTimeline,
    credit_line: WorkingCapitalCreditLine,
) -> CompanyLiquidityCreditCapacity:
    required = timeline.peak_liquidity_gap_krw
    unused = credit_line.unused_limit_krw
    headroom = max(ZERO, unused - required)
    gap = max(ZERO, required - unused)
    return CompanyLiquidityCreditCapacity(
        company_peak_liquidity_gap_krw=required,
        unused_credit_limit_krw=unused,
        credit_headroom_krw=headroom,
        liquidity_gap_krw=gap,
        feasible=gap == ZERO,
    )


def parse_company_cash_events_csv(
    csv_text: str,
) -> tuple[CompanyCashEvent, ...]:
    reader = csv.DictReader(StringIO(csv_text.lstrip("\ufeff")))
    if reader.fieldnames is None or tuple(reader.fieldnames) != CSV_COLUMNS:
        raise ValueError("CSV columns must match the canonical import schema")
    events = []
    for row in reader:
        try:
            event_date = date.fromisoformat(row["event_date"].strip())
            category = CompanyCashEventCategory(row["category"].strip())
            amount = Decimal(row["amount_krw"].strip())
            status = CompanyCashEventStatus(row["status"].strip())
            reference = row["reference"].strip()
        except (AttributeError, InvalidOperation, ValueError) as exc:
            raise ValueError("Invalid company cash-plan row") from exc
        events.append(
            CompanyCashEvent(
                event_date=event_date,
                category=category,
                amount_krw=amount,
                status=status,
                source=CompanyCashEventSource.ERP_IMPORT,
                reference=reference,
            )
        )
    return tuple(sorted(events, key=lambda event: event.event_date))
