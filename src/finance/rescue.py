from dataclasses import dataclass, replace
from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR
from enum import Enum

from src.domain.deal_case import Currency, DealCase, FxRates
from src.finance.engine import Scenario, evaluate_scenario


ZERO = Decimal("0")
TWO = Decimal("2")
CENT = Decimal("0.01")
MARGIN_TOLERANCE = Decimal("0.000000000001")
BISECTION_TOLERANCE = Decimal("0.000000001")
MAX_BRACKET_STEPS = 64


class RescueLever(Enum):
    SALE_AMOUNT_USD = "SALE_AMOUNT_USD"
    USD_PAYABLE_AMOUNT = "USD_PAYABLE_AMOUNT"
    JPY_PAYABLE_AMOUNT = "JPY_PAYABLE_AMOUNT"
    COLLECTION_DAY = "COLLECTION_DAY"
    FUNDING_RATE = "FUNDING_RATE"


class RescueStatus(Enum):
    FEASIBLE = "FEASIBLE"
    INFEASIBLE = "INFEASIBLE"
    NOT_APPLICABLE = "NOT_APPLICABLE"


@dataclass(frozen=True)
class RescueOption:
    lever: RescueLever
    status: RescueStatus
    current_value: Decimal | int
    threshold_value: Decimal | int | None
    threshold_margin: Decimal | None


@dataclass(frozen=True)
class DealRescueAnalysis:
    scenario: Scenario
    baseline_margin: Decimal
    target_margin: Decimal
    needs_rescue: bool
    options: tuple[RescueOption, ...]


def _margin(deal: DealCase, fx: FxRates, scenario: Scenario) -> Decimal:
    return evaluate_scenario(deal, fx, scenario).financing_adjusted_deal_margin


def _meets_target(margin: Decimal, target: Decimal) -> bool:
    return margin + MARGIN_TOLERANCE >= target


def _sale_option(deal: DealCase, fx: FxRates, scenario: Scenario) -> RescueOption:
    current = deal.sale.amount
    if deal.sale.currency is not Currency.USD:
        return RescueOption(
            RescueLever.SALE_AMOUNT_USD,
            RescueStatus.NOT_APPLICABLE,
            current,
            None,
            None,
        )

    low = current
    high = current
    for _ in range(MAX_BRACKET_STEPS):
        high *= TWO
        candidate = replace(deal, sale=replace(deal.sale, amount=high))
        if _meets_target(_margin(candidate, fx, scenario), deal.target_margin):
            break
    else:
        return RescueOption(
            RescueLever.SALE_AMOUNT_USD,
            RescueStatus.INFEASIBLE,
            current,
            None,
            None,
        )

    while high - low > BISECTION_TOLERANCE:
        midpoint = (low + high) / TWO
        candidate = replace(deal, sale=replace(deal.sale, amount=midpoint))
        if _meets_target(_margin(candidate, fx, scenario), deal.target_margin):
            high = midpoint
        else:
            low = midpoint

    threshold = high.quantize(CENT, rounding=ROUND_CEILING)
    threshold_deal = replace(deal, sale=replace(deal.sale, amount=threshold))
    threshold_margin = _margin(threshold_deal, fx, scenario)
    return RescueOption(
        RescueLever.SALE_AMOUNT_USD,
        RescueStatus.FEASIBLE,
        current,
        threshold,
        threshold_margin,
    )


def _payable_option(
    deal: DealCase,
    fx: FxRates,
    scenario: Scenario,
    currency: Currency,
    lever: RescueLever,
) -> RescueOption:
    matches = [
        (index, payable)
        for index, payable in enumerate(deal.foreign_payables)
        if payable.currency is currency
    ]
    if len(matches) != 1:
        current = matches[0][1].amount if len(matches) == 1 else ZERO
        return RescueOption(lever, RescueStatus.NOT_APPLICABLE, current, None, None)

    index, payable = matches[0]
    current = payable.amount

    def deal_with_amount(amount: Decimal) -> DealCase:
        payables = list(deal.foreign_payables)
        payables[index] = replace(payable, amount=amount)
        return replace(deal, foreign_payables=tuple(payables))

    zero_margin = _margin(deal_with_amount(ZERO), fx, scenario)
    if not _meets_target(zero_margin, deal.target_margin):
        return RescueOption(lever, RescueStatus.INFEASIBLE, current, None, None)

    low = ZERO
    high = current
    while high - low > BISECTION_TOLERANCE:
        midpoint = (low + high) / TWO
        if _meets_target(
            _margin(deal_with_amount(midpoint), fx, scenario), deal.target_margin
        ):
            low = midpoint
        else:
            high = midpoint

    threshold = low.quantize(CENT, rounding=ROUND_FLOOR)
    threshold_margin = _margin(deal_with_amount(threshold), fx, scenario)
    return RescueOption(
        lever,
        RescueStatus.FEASIBLE,
        current,
        threshold,
        threshold_margin,
    )


def _collection_day_option(
    deal: DealCase, fx: FxRates, scenario: Scenario
) -> RescueOption:
    current = deal.sale.collection_day
    earliest_deal = replace(deal, sale=replace(deal.sale, collection_day=0))
    if not _meets_target(
        _margin(earliest_deal, fx, scenario), deal.target_margin
    ):
        return RescueOption(
            RescueLever.COLLECTION_DAY,
            RescueStatus.INFEASIBLE,
            current,
            None,
            None,
        )

    low = 0
    high = current
    while low < high:
        midpoint = (low + high + 1) // 2
        candidate = replace(
            deal, sale=replace(deal.sale, collection_day=midpoint)
        )
        if _meets_target(_margin(candidate, fx, scenario), deal.target_margin):
            low = midpoint
        else:
            high = midpoint - 1

    threshold_deal = replace(deal, sale=replace(deal.sale, collection_day=low))
    return RescueOption(
        RescueLever.COLLECTION_DAY,
        RescueStatus.FEASIBLE,
        current,
        low,
        _margin(threshold_deal, fx, scenario),
    )


def _funding_rate_option(
    deal: DealCase, fx: FxRates, scenario: Scenario
) -> RescueOption:
    current = deal.annual_funding_rate
    zero_deal = replace(deal, annual_funding_rate=ZERO)
    if not _meets_target(_margin(zero_deal, fx, scenario), deal.target_margin):
        return RescueOption(
            RescueLever.FUNDING_RATE,
            RescueStatus.INFEASIBLE,
            current,
            None,
            None,
        )

    low = ZERO
    high = current
    while high - low > BISECTION_TOLERANCE:
        midpoint = (low + high) / TWO
        candidate = replace(deal, annual_funding_rate=midpoint)
        if _meets_target(_margin(candidate, fx, scenario), deal.target_margin):
            low = midpoint
        else:
            high = midpoint

    threshold = low
    threshold_deal = replace(deal, annual_funding_rate=threshold)
    return RescueOption(
        RescueLever.FUNDING_RATE,
        RescueStatus.FEASIBLE,
        current,
        threshold,
        _margin(threshold_deal, fx, scenario),
    )


def analyze_deal_rescue(
    deal: DealCase,
    fx: FxRates,
    scenario: Scenario = Scenario.COMBINED,
) -> DealRescueAnalysis:
    baseline = evaluate_scenario(deal, fx, scenario)
    if baseline.financing_adjusted_deal_margin >= deal.target_margin:
        return DealRescueAnalysis(
            scenario=scenario,
            baseline_margin=baseline.financing_adjusted_deal_margin,
            target_margin=deal.target_margin,
            needs_rescue=False,
            options=(),
        )

    return DealRescueAnalysis(
        scenario=scenario,
        baseline_margin=baseline.financing_adjusted_deal_margin,
        target_margin=deal.target_margin,
        needs_rescue=True,
        options=(
            _sale_option(deal, fx, scenario),
            _payable_option(
                deal,
                fx,
                scenario,
                Currency.USD,
                RescueLever.USD_PAYABLE_AMOUNT,
            ),
            _payable_option(
                deal,
                fx,
                scenario,
                Currency.JPY,
                RescueLever.JPY_PAYABLE_AMOUNT,
            ),
            _collection_day_option(deal, fx, scenario),
            _funding_rate_option(deal, fx, scenario),
        ),
    )
