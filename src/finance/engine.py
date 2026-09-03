from dataclasses import dataclass, replace
from decimal import Decimal
from enum import Enum
from types import MappingProxyType
from typing import Mapping

from src.domain.deal_case import Currency, DealCase, FxRates, PaymentMethod


ZERO = Decimal("0")
DAYS_PER_YEAR = Decimal("365")


class Scenario(Enum):
    BASE = "Base"
    USD_DOWN_5 = "USD -5%"
    JPY_UP_10 = "JPY +10%"
    RATE_UP_1PP = "Rate +1%p"
    DELAY_30D = "Delay +30d"
    COMBINED = "Combined"


@dataclass(frozen=True)
class CashEvent:
    day: int
    amount_krw: Decimal


@dataclass(frozen=True)
class FundingPoint:
    day: int
    cumulative_deal_cash_krw: Decimal
    external_loan_outstanding_krw: Decimal


@dataclass(frozen=True)
class FundingInterval:
    start_day: int
    end_day: int
    external_loan_outstanding_krw: Decimal
    interest_cost_krw: Decimal


@dataclass(frozen=True)
class FundingSchedule:
    points: tuple[FundingPoint, ...]
    intervals: tuple[FundingInterval, ...]
    peak_deal_funding_krw: Decimal
    maximum_external_borrowing_krw: Decimal
    external_funding_cost_krw: Decimal


@dataclass(frozen=True)
class ReceivablePurchaseOption:
    purchase_day: int
    annual_discount_rate: Decimal
    fee_rate: Decimal


@dataclass(frozen=True)
class ReceivablePurchaseResult:
    purchase_day: int
    remaining_tenor_days: int
    face_value_krw: Decimal
    discount_cost_krw: Decimal
    purchase_fee_krw: Decimal
    net_proceeds_krw: Decimal


@dataclass(frozen=True)
class DealResult:
    sales_krw: Decimal
    total_non_funding_cost_krw: Decimal
    gross_deal_profit_krw: Decimal
    gross_deal_margin: Decimal
    currency_exposure: Mapping[Currency, Decimal]
    funding: FundingSchedule
    financing_adjusted_deal_profit_krw: Decimal
    financing_adjusted_deal_margin: Decimal
    collection_day: int
    receivable_purchase: ReceivablePurchaseResult | None


def currency_exposure(deal: DealCase) -> dict[Currency, Decimal]:
    exposure = {currency: ZERO for currency in Currency}
    exposure[deal.sale.currency] += deal.sale.amount
    for payable in deal.foreign_payables:
        exposure[payable.currency] -= payable.amount
    return exposure


def _combine_events(events: list[CashEvent]) -> tuple[CashEvent, ...]:
    amounts_by_day: dict[int, Decimal] = {}
    for event in events:
        amounts_by_day[event.day] = amounts_by_day.get(event.day, ZERO) + event.amount_krw
    return tuple(CashEvent(day, amounts_by_day[day]) for day in sorted(amounts_by_day))


def _purchase_result(
    deal: DealCase,
    fx: FxRates,
    option: ReceivablePurchaseOption,
    effective_collection_day: int,
) -> ReceivablePurchaseResult:
    remaining_tenor = effective_collection_day - option.purchase_day
    if remaining_tenor < 0:
        raise ValueError("purchase_day cannot be after the effective collection day")
    if deal.sale.currency is not Currency.USD:
        raise ValueError("EARLY_RECEIVABLE_PURCHASE requires a USD receivable in v0.1")
    if deal.sale.payment_method is not PaymentMethod.OA:
        raise ValueError("EARLY_RECEIVABLE_PURCHASE requires an O/A receivable")
    face_value = fx.to_krw(deal.sale.amount, deal.sale.currency)
    discount = (
        face_value
        * option.annual_discount_rate
        * Decimal(remaining_tenor)
        / DAYS_PER_YEAR
    )
    fee = face_value * option.fee_rate
    return ReceivablePurchaseResult(
        purchase_day=option.purchase_day,
        remaining_tenor_days=remaining_tenor,
        face_value_krw=face_value,
        discount_cost_krw=discount,
        purchase_fee_krw=fee,
        net_proceeds_krw=face_value - discount - fee,
    )


def dated_cashflows(
    deal: DealCase,
    fx: FxRates,
    collection_day: int | None = None,
    purchase_option: ReceivablePurchaseOption | None = None,
) -> tuple[tuple[CashEvent, ...], ReceivablePurchaseResult | None]:
    effective_collection_day = (
        deal.sale.collection_day if collection_day is None else collection_day
    )
    events = [
        CashEvent(cost.payment_day, -cost.amount_krw) for cost in deal.krw_costs
    ]
    events.extend(
        CashEvent(payable.payment_day, -fx.to_krw(payable.amount, payable.currency))
        for payable in deal.foreign_payables
    )

    purchase = None
    if purchase_option is None:
        events.append(
            CashEvent(
                effective_collection_day,
                fx.to_krw(deal.sale.amount, deal.sale.currency),
            )
        )
    else:
        purchase = _purchase_result(
            deal, fx, purchase_option, effective_collection_day
        )
        events.append(CashEvent(purchase.purchase_day, purchase.net_proceeds_krw))
    return _combine_events(events), purchase


def funding_schedule(
    events: tuple[CashEvent, ...], available_cash_krw: Decimal, annual_rate: Decimal
) -> FundingSchedule:
    if not events:
        raise ValueError("At least one cash event is required")

    cumulative = ZERO
    peak = ZERO
    max_loan = ZERO
    points: list[FundingPoint] = []
    intervals: list[FundingInterval] = []

    for index, event in enumerate(events):
        cumulative += event.amount_krw
        deal_funding_need = max(ZERO, -cumulative)
        outstanding = max(ZERO, deal_funding_need - available_cash_krw)
        peak = max(peak, deal_funding_need)
        max_loan = max(max_loan, outstanding)
        points.append(FundingPoint(event.day, cumulative, outstanding))

        if index + 1 < len(events):
            next_day = events[index + 1].day
            interval_days = next_day - event.day
            interest = (
                outstanding * annual_rate * Decimal(interval_days) / DAYS_PER_YEAR
            )
            intervals.append(
                FundingInterval(event.day, next_day, outstanding, interest)
            )

    return FundingSchedule(
        points=tuple(points),
        intervals=tuple(intervals),
        peak_deal_funding_krw=peak,
        maximum_external_borrowing_krw=max_loan,
        external_funding_cost_krw=sum(
            (interval.interest_cost_krw for interval in intervals), ZERO
        ),
    )


def evaluate_deal(
    deal: DealCase,
    fx: FxRates,
    collection_day: int | None = None,
    purchase_option: ReceivablePurchaseOption | None = None,
) -> DealResult:
    sales_krw = fx.to_krw(deal.sale.amount, deal.sale.currency)
    foreign_costs = sum(
        (fx.to_krw(item.amount, item.currency) for item in deal.foreign_payables), ZERO
    )
    krw_costs = sum((item.amount_krw for item in deal.krw_costs), ZERO)
    total_cost = foreign_costs + krw_costs
    gross_profit = sales_krw - total_cost

    events, purchase = dated_cashflows(deal, fx, collection_day, purchase_option)
    funding = funding_schedule(
        events, deal.available_cash_krw, deal.annual_funding_rate
    )
    purchase_cost = ZERO
    effective_collection_day = (
        deal.sale.collection_day if collection_day is None else collection_day
    )
    if purchase is not None:
        purchase_cost = purchase.discount_cost_krw + purchase.purchase_fee_krw

    adjusted_profit = gross_profit - funding.external_funding_cost_krw - purchase_cost
    return DealResult(
        sales_krw=sales_krw,
        total_non_funding_cost_krw=total_cost,
        gross_deal_profit_krw=gross_profit,
        gross_deal_margin=gross_profit / sales_krw,
        currency_exposure=MappingProxyType(currency_exposure(deal)),
        funding=funding,
        financing_adjusted_deal_profit_krw=adjusted_profit,
        financing_adjusted_deal_margin=adjusted_profit / sales_krw,
        collection_day=effective_collection_day,
        receivable_purchase=purchase,
    )


def evaluate_scenario(deal: DealCase, fx: FxRates, scenario: Scenario) -> DealResult:
    scenario_fx = fx
    scenario_deal = deal
    collection_day = deal.sale.collection_day

    if scenario in (Scenario.USD_DOWN_5, Scenario.COMBINED):
        scenario_fx = replace(scenario_fx, usd_krw=fx.usd_krw * Decimal("0.95"))
    if scenario in (Scenario.JPY_UP_10, Scenario.COMBINED):
        scenario_fx = replace(
            scenario_fx, jpy_krw_per_100=fx.jpy_krw_per_100 * Decimal("1.10")
        )
    if scenario in (Scenario.RATE_UP_1PP, Scenario.COMBINED):
        scenario_deal = replace(
            scenario_deal,
            annual_funding_rate=deal.annual_funding_rate + Decimal("0.01"),
        )
    if scenario in (Scenario.DELAY_30D, Scenario.COMBINED):
        collection_day += 30

    return evaluate_deal(scenario_deal, scenario_fx, collection_day=collection_day)


def canonical_scenarios(deal: DealCase, fx: FxRates) -> dict[Scenario, DealResult]:
    return {scenario: evaluate_scenario(deal, fx, scenario) for scenario in Scenario}


def solve_usd_krw_threshold(
    deal: DealCase,
    fx: FxRates,
    target_margin: Decimal | None,
    lower: Decimal = Decimal("500"),
    upper: Decimal = Decimal("2500"),
    tolerance: Decimal = Decimal("0.000001"),
) -> Decimal:
    def objective(rate: Decimal) -> Decimal:
        result = evaluate_deal(deal, replace(fx, usd_krw=rate))
        if target_margin is None:
            return result.financing_adjusted_deal_profit_krw
        return result.financing_adjusted_deal_margin - target_margin

    low_value = objective(lower)
    high_value = objective(upper)
    if low_value == ZERO:
        return lower
    if high_value == ZERO:
        return upper
    if low_value * high_value > ZERO:
        raise ValueError("Threshold is not bracketed by the supplied bounds")

    low = lower
    high = upper
    while high - low > tolerance:
        midpoint = (low + high) / Decimal("2")
        value = objective(midpoint)
        if value == ZERO:
            return midpoint
        if low_value * value < ZERO:
            high = midpoint
        else:
            low = midpoint
            low_value = value
    return (low + high) / Decimal("2")


def canonical_purchase_option() -> ReceivablePurchaseOption:
    return ReceivablePurchaseOption(
        purchase_day=65,
        annual_discount_rate=Decimal("0.052"),
        fee_rate=Decimal("0.0015"),
    )
