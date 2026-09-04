from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

from src.domain.deal_case import Currency, DealCase, FxRates
from src.finance.engine import DealResult, evaluate_deal


ZERO = Decimal("0")
SUPPORTED_FX_CURRENCIES = (Currency.USD, Currency.JPY)


class FxExposureDirection(Enum):
    RECEIVABLE = "RECEIVABLE"
    PAYABLE = "PAYABLE"
    FLAT = "FLAT"


class FxUnfavorableDirection(Enum):
    FX_DOWN = "FX_DOWN"
    FX_UP = "FX_UP"
    NONE = "NONE"


class ForwardAction(Enum):
    SELL = "SELL"
    BUY = "BUY"
    NONE = "NONE"


@dataclass(frozen=True)
class CurrencyExposurePosition:
    currency: Currency
    receivable_amount: Decimal
    payable_amount: Decimal
    amount_offset: Decimal
    net_exposure: Decimal
    open_exposure: Decimal
    direction: FxExposureDirection
    unfavorable_direction: FxUnfavorableDirection


@dataclass(frozen=True)
class ForwardHedgeInput:
    currency: Currency
    hedge_ratio: Decimal
    forward_rate_quote: Decimal

    def __post_init__(self) -> None:
        if self.currency not in SUPPORTED_FX_CURRENCIES:
            raise ValueError("Forward hedge currency must be USD or JPY")
        if not ZERO <= self.hedge_ratio <= Decimal("1"):
            raise ValueError("hedge_ratio must be between zero and one")
        if self.forward_rate_quote <= ZERO:
            raise ValueError("forward_rate_quote must be positive")


@dataclass(frozen=True)
class ForwardHedgeResult:
    currency: Currency
    action: ForwardAction
    open_exposure: Decimal
    hedged_notional: Decimal
    residual_exposure: Decimal
    forward_rate_quote: Decimal
    settlement_spot_quote: Decimal
    hedge_effect_on_profit_krw: Decimal


@dataclass(frozen=True)
class HedgeDealOverlay:
    unhedged_profit_krw: Decimal
    unhedged_margin: Decimal
    hedge_effect_krw: Decimal
    simulated_profit_after_hedge_krw: Decimal
    simulated_margin_after_hedge: Decimal


@dataclass(frozen=True)
class FxTreasuryAnalysis:
    positions: tuple[CurrencyExposurePosition, ...]
    current_spot_hedges: tuple[ForwardHedgeResult, ...]
    settlement_scenario_hedges: tuple[ForwardHedgeResult, ...]
    current_spot_total_effect_krw: Decimal
    settlement_scenario_total_effect_krw: Decimal
    current_spot_result: DealResult
    settlement_scenario_result: DealResult
    current_spot_overlay: HedgeDealOverlay
    settlement_scenario_overlay: HedgeDealOverlay


def build_currency_exposure_positions(
    deal: DealCase,
) -> tuple[CurrencyExposurePosition, ...]:
    positions = []
    for currency in SUPPORTED_FX_CURRENCIES:
        receivable = deal.sale.amount if deal.sale.currency is currency else ZERO
        payable = sum(
            (
                item.amount
                for item in deal.foreign_payables
                if item.currency is currency
            ),
            ZERO,
        )
        net = receivable - payable
        if net > ZERO:
            direction = FxExposureDirection.RECEIVABLE
            unfavorable = FxUnfavorableDirection.FX_DOWN
        elif net < ZERO:
            direction = FxExposureDirection.PAYABLE
            unfavorable = FxUnfavorableDirection.FX_UP
        else:
            direction = FxExposureDirection.FLAT
            unfavorable = FxUnfavorableDirection.NONE
        positions.append(
            CurrencyExposurePosition(
                currency=currency,
                receivable_amount=receivable,
                payable_amount=payable,
                amount_offset=min(receivable, payable),
                net_exposure=net,
                open_exposure=abs(net),
                direction=direction,
                unfavorable_direction=unfavorable,
            )
        )
    return tuple(positions)


def _quote_per_currency_unit(currency: Currency, quote: Decimal) -> Decimal:
    if currency is Currency.USD:
        return quote
    if currency is Currency.JPY:
        return quote / Decimal("100")
    raise ValueError("FX Treasury supports USD and JPY only")


def _spot_quote(fx: FxRates, currency: Currency) -> Decimal:
    if currency is Currency.USD:
        return fx.usd_krw
    if currency is Currency.JPY:
        return fx.jpy_krw_per_100
    raise ValueError("FX Treasury supports USD and JPY only")


def _hedge_result(
    position: CurrencyExposurePosition,
    hedge_input: ForwardHedgeInput,
    settlement_fx: FxRates,
) -> ForwardHedgeResult:
    if position.currency is not hedge_input.currency:
        raise ValueError("Hedge input currency does not match exposure position")
    if position.direction is FxExposureDirection.RECEIVABLE:
        action = ForwardAction.SELL
    elif position.direction is FxExposureDirection.PAYABLE:
        action = ForwardAction.BUY
    else:
        action = ForwardAction.NONE

    hedged_notional = position.open_exposure * hedge_input.hedge_ratio
    signed_hedged_notional = (
        hedged_notional
        if position.net_exposure >= ZERO
        else -hedged_notional
    )
    spot_quote = _spot_quote(settlement_fx, position.currency)
    forward_per_unit = _quote_per_currency_unit(
        position.currency, hedge_input.forward_rate_quote
    )
    spot_per_unit = _quote_per_currency_unit(position.currency, spot_quote)
    effect = signed_hedged_notional * (forward_per_unit - spot_per_unit)
    return ForwardHedgeResult(
        currency=position.currency,
        action=action,
        open_exposure=position.open_exposure,
        hedged_notional=hedged_notional,
        residual_exposure=position.open_exposure - hedged_notional,
        forward_rate_quote=hedge_input.forward_rate_quote,
        settlement_spot_quote=spot_quote,
        hedge_effect_on_profit_krw=effect,
    )


def _overlay(result: DealResult, hedge_effect: Decimal) -> HedgeDealOverlay:
    simulated_profit = result.financing_adjusted_deal_profit_krw + hedge_effect
    return HedgeDealOverlay(
        unhedged_profit_krw=result.financing_adjusted_deal_profit_krw,
        unhedged_margin=result.financing_adjusted_deal_margin,
        hedge_effect_krw=hedge_effect,
        simulated_profit_after_hedge_krw=simulated_profit,
        simulated_margin_after_hedge=simulated_profit / result.sales_krw,
    )


def analyze_fx_treasury(
    *,
    deal: DealCase,
    current_fx: FxRates,
    settlement_fx: FxRates,
    hedge_inputs: tuple[ForwardHedgeInput, ...],
) -> FxTreasuryAnalysis:
    inputs_by_currency = {item.currency: item for item in hedge_inputs}
    if len(inputs_by_currency) != len(hedge_inputs):
        raise ValueError("Duplicate forward hedge currency")
    if set(inputs_by_currency) != set(SUPPORTED_FX_CURRENCIES):
        raise ValueError("Provide exactly one USD and one JPY forward hedge input")

    positions = build_currency_exposure_positions(deal)
    current_hedges = tuple(
        _hedge_result(position, inputs_by_currency[position.currency], current_fx)
        for position in positions
    )
    settlement_hedges = tuple(
        _hedge_result(position, inputs_by_currency[position.currency], settlement_fx)
        for position in positions
    )
    current_effect = sum(
        (item.hedge_effect_on_profit_krw for item in current_hedges), ZERO
    )
    settlement_effect = sum(
        (item.hedge_effect_on_profit_krw for item in settlement_hedges), ZERO
    )
    current_result = evaluate_deal(deal, current_fx)
    settlement_result = evaluate_deal(deal, settlement_fx)
    return FxTreasuryAnalysis(
        positions=positions,
        current_spot_hedges=current_hedges,
        settlement_scenario_hedges=settlement_hedges,
        current_spot_total_effect_krw=current_effect,
        settlement_scenario_total_effect_krw=settlement_effect,
        current_spot_result=current_result,
        settlement_scenario_result=settlement_result,
        current_spot_overlay=_overlay(current_result, current_effect),
        settlement_scenario_overlay=_overlay(settlement_result, settlement_effect),
    )
