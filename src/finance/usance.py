from dataclasses import dataclass, replace
from decimal import Decimal

from src.domain.deal_case import Currency, DealCase, FxRates, KrwCost
from src.finance.engine import (
    DAYS_PER_YEAR,
    DealResult,
    FundingSchedule,
    dated_cashflows,
    funding_schedule,
)
from src.finance.liquidity import WorkingCapitalCreditLine


ZERO = Decimal("0")


@dataclass(frozen=True)
class BankersUsanceInput:
    payable_index: int
    repayment_day: int
    annual_usance_rate: Decimal
    fee_rate: Decimal

    def __post_init__(self) -> None:
        if self.payable_index < 0:
            raise ValueError("payable_index must be nonnegative")
        if self.annual_usance_rate < ZERO:
            raise ValueError("annual_usance_rate must be nonnegative")
        if self.fee_rate < ZERO:
            raise ValueError("fee_rate must be nonnegative")


@dataclass(frozen=True)
class BankersUsanceResult:
    currency: Currency
    principal_fcy: Decimal
    principal_krw: Decimal
    supplier_payment_day: int
    company_repayment_day: int
    tenor_days: int
    annual_usance_rate: Decimal
    fee_rate: Decimal
    usance_interest_fcy: Decimal
    usance_fee_fcy: Decimal
    usance_interest_krw: Decimal
    usance_fee_krw: Decimal
    working_capital_funding: FundingSchedule
    peak_working_capital_credit_krw: Decimal
    ordinary_line_headroom_krw: Decimal
    peak_combined_bank_principal_krw: Decimal
    total_financing_cost_krw: Decimal


@dataclass(frozen=True)
class BankersUsanceComparison:
    base_working_capital_credit_krw: Decimal
    base_ordinary_line_headroom_krw: Decimal
    base_total_financing_cost_krw: Decimal
    usance: BankersUsanceResult
    working_capital_credit_reduction_krw: Decimal
    financing_cost_difference_krw: Decimal


def analyze_bankers_usance(
    *,
    deal: DealCase,
    fx: FxRates,
    base_result: DealResult,
    credit_line: WorkingCapitalCreditLine,
    usance_input: BankersUsanceInput,
) -> BankersUsanceComparison:
    if usance_input.payable_index >= len(deal.foreign_payables):
        raise ValueError("Selected foreign payable does not exist")

    payable = deal.foreign_payables[usance_input.payable_index]
    if usance_input.repayment_day <= payable.payment_day:
        raise ValueError("repayment_day must be after supplier payment day")

    tenor_days = usance_input.repayment_day - payable.payment_day
    interest_fcy = (
        payable.amount
        * usance_input.annual_usance_rate
        * Decimal(tenor_days)
        / DAYS_PER_YEAR
    )
    fee_fcy = payable.amount * usance_input.fee_rate
    principal_krw = fx.to_krw(payable.amount, payable.currency)
    interest_krw = fx.to_krw(interest_fcy, payable.currency)
    fee_krw = fx.to_krw(fee_fcy, payable.currency)

    adjusted_payables = list(deal.foreign_payables)
    adjusted_payables[usance_input.payable_index] = replace(
        payable, payment_day=usance_input.repayment_day
    )
    adjusted_deal = replace(
        deal,
        foreign_payables=tuple(adjusted_payables),
        krw_costs=deal.krw_costs
        + (
            KrwCost(ZERO, payable.payment_day),
            KrwCost(interest_krw + fee_krw, usance_input.repayment_day),
        ),
    )
    events, _ = dated_cashflows(adjusted_deal, fx)
    working_capital = funding_schedule(
        events,
        deal.available_cash_krw,
        deal.annual_funding_rate,
    )

    combined_principal = max(
        (
            point.external_loan_outstanding_krw
            + (
                principal_krw
                if payable.payment_day <= point.day < usance_input.repayment_day
                else ZERO
            )
            for point in working_capital.points
        ),
        default=ZERO,
    )
    base_credit = base_result.funding.maximum_external_borrowing_krw
    usance_credit = working_capital.maximum_external_borrowing_krw
    base_cost = base_result.funding.external_funding_cost_krw
    usance_cost = (
        working_capital.external_funding_cost_krw
        + interest_krw
        + fee_krw
    )
    usance_result = BankersUsanceResult(
        currency=payable.currency,
        principal_fcy=payable.amount,
        principal_krw=principal_krw,
        supplier_payment_day=payable.payment_day,
        company_repayment_day=usance_input.repayment_day,
        tenor_days=tenor_days,
        annual_usance_rate=usance_input.annual_usance_rate,
        fee_rate=usance_input.fee_rate,
        usance_interest_fcy=interest_fcy,
        usance_fee_fcy=fee_fcy,
        usance_interest_krw=interest_krw,
        usance_fee_krw=fee_krw,
        working_capital_funding=working_capital,
        peak_working_capital_credit_krw=usance_credit,
        ordinary_line_headroom_krw=max(
            ZERO, credit_line.unused_limit_krw - usance_credit
        ),
        peak_combined_bank_principal_krw=combined_principal,
        total_financing_cost_krw=usance_cost,
    )
    return BankersUsanceComparison(
        base_working_capital_credit_krw=base_credit,
        base_ordinary_line_headroom_krw=max(
            ZERO, credit_line.unused_limit_krw - base_credit
        ),
        base_total_financing_cost_krw=base_cost,
        usance=usance_result,
        working_capital_credit_reduction_krw=base_credit - usance_credit,
        financing_cost_difference_krw=usance_cost - base_cost,
    )
