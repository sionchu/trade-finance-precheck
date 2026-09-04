from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

from src.domain.deal_case import DealCase
from src.finance.engine import DealResult


ZERO = Decimal("0")


@dataclass(frozen=True)
class WorkingCapitalCreditLine:
    total_limit_krw: Decimal
    used_amount_krw: Decimal
    deal_specific_fee_krw: Decimal = ZERO

    def __post_init__(self) -> None:
        if self.total_limit_krw < ZERO:
            raise ValueError("total_limit_krw must be nonnegative")
        if self.used_amount_krw < ZERO:
            raise ValueError("used_amount_krw must be nonnegative")
        if self.used_amount_krw > self.total_limit_krw:
            raise ValueError("used_amount_krw cannot exceed total_limit_krw")
        if self.deal_specific_fee_krw < ZERO:
            raise ValueError("deal_specific_fee_krw must be nonnegative")

    @property
    def unused_limit_krw(self) -> Decimal:
        return self.total_limit_krw - self.used_amount_krw


@dataclass(frozen=True)
class FundingCapacity:
    required_external_funding_krw: Decimal
    unused_credit_limit_krw: Decimal
    credit_headroom_krw: Decimal
    liquidity_gap_krw: Decimal
    feasible: bool


class FundingChoiceStatus(Enum):
    FEASIBLE = "FEASIBLE"
    INFEASIBLE = "INFEASIBLE"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class FundingChoice(Enum):
    INTERNAL_CASH_ONLY = "INTERNAL_CASH_ONLY"
    WAIT_WITH_CREDIT_LINE = "WAIT_WITH_CREDIT_LINE"
    EARLY_RECEIVABLE_PURCHASE = "EARLY_RECEIVABLE_PURCHASE"


@dataclass(frozen=True)
class FundingChoiceResult:
    choice: FundingChoice
    status: FundingChoiceStatus
    required_external_funding_krw: Decimal
    liquidity_gap_krw: Decimal
    credit_headroom_krw: Decimal
    interest_cost_krw: Decimal
    other_financing_cost_krw: Decimal
    total_financing_cost_krw: Decimal | None
    cash_inflow_day: int | None


@dataclass(frozen=True)
class CompanyFundingAnalysis:
    credit_line: WorkingCapitalCreditLine
    base_capacity: FundingCapacity
    combined_capacity: FundingCapacity
    choices: tuple[FundingChoiceResult, ...]


def _capacity(required: Decimal, credit_line: WorkingCapitalCreditLine) -> FundingCapacity:
    unused = credit_line.unused_limit_krw
    headroom = max(ZERO, unused - required)
    gap = max(ZERO, required - unused)
    return FundingCapacity(
        required_external_funding_krw=required,
        unused_credit_limit_krw=unused,
        credit_headroom_krw=headroom,
        liquidity_gap_krw=gap,
        feasible=gap == ZERO,
    )


def _credit_choice(
    choice: FundingChoice,
    result: DealResult,
    credit_line: WorkingCapitalCreditLine,
) -> FundingChoiceResult:
    capacity = _capacity(
        result.funding.maximum_external_borrowing_krw,
        credit_line,
    )
    uses_credit = capacity.required_external_funding_krw > ZERO
    explicit_fee = credit_line.deal_specific_fee_krw if uses_credit else ZERO
    purchase_cost = ZERO
    cash_inflow_day = result.collection_day
    if result.receivable_purchase is not None:
        purchase = result.receivable_purchase
        purchase_cost = purchase.discount_cost_krw + purchase.purchase_fee_krw
        cash_inflow_day = purchase.purchase_day
    other_cost = purchase_cost + explicit_fee
    return FundingChoiceResult(
        choice=choice,
        status=(
            FundingChoiceStatus.FEASIBLE
            if capacity.feasible
            else FundingChoiceStatus.INFEASIBLE
        ),
        required_external_funding_krw=capacity.required_external_funding_krw,
        liquidity_gap_krw=capacity.liquidity_gap_krw,
        credit_headroom_krw=capacity.credit_headroom_krw,
        interest_cost_krw=result.funding.external_funding_cost_krw,
        other_financing_cost_krw=other_cost,
        total_financing_cost_krw=(
            result.funding.external_funding_cost_krw + other_cost
            if capacity.feasible
            else None
        ),
        cash_inflow_day=cash_inflow_day,
    )


def analyze_company_funding(
    *,
    deal: DealCase,
    base_result: DealResult,
    combined_result: DealResult,
    credit_line: WorkingCapitalCreditLine,
    purchase_result: DealResult | None,
) -> CompanyFundingAnalysis:
    required = base_result.funding.maximum_external_borrowing_krw
    internal_feasible = required == ZERO
    internal = FundingChoiceResult(
        choice=FundingChoice.INTERNAL_CASH_ONLY,
        status=(
            FundingChoiceStatus.FEASIBLE
            if internal_feasible
            else FundingChoiceStatus.INFEASIBLE
        ),
        required_external_funding_krw=required,
        liquidity_gap_krw=required,
        credit_headroom_krw=ZERO,
        interest_cost_krw=ZERO,
        other_financing_cost_krw=ZERO,
        total_financing_cost_krw=ZERO if internal_feasible else None,
        cash_inflow_day=base_result.collection_day,
    )
    wait = _credit_choice(
        FundingChoice.WAIT_WITH_CREDIT_LINE,
        base_result,
        credit_line,
    )
    if purchase_result is None or purchase_result.receivable_purchase is None:
        early = FundingChoiceResult(
            choice=FundingChoice.EARLY_RECEIVABLE_PURCHASE,
            status=FundingChoiceStatus.NOT_APPLICABLE,
            required_external_funding_krw=ZERO,
            liquidity_gap_krw=ZERO,
            credit_headroom_krw=ZERO,
            interest_cost_krw=ZERO,
            other_financing_cost_krw=ZERO,
            total_financing_cost_krw=None,
            cash_inflow_day=None,
        )
    else:
        early = _credit_choice(
            FundingChoice.EARLY_RECEIVABLE_PURCHASE,
            purchase_result,
            credit_line,
        )

    return CompanyFundingAnalysis(
        credit_line=credit_line,
        base_capacity=_capacity(required, credit_line),
        combined_capacity=_capacity(
            combined_result.funding.maximum_external_borrowing_krw,
            credit_line,
        ),
        choices=(internal, wait, early),
    )
