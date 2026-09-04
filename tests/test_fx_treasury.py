from dataclasses import FrozenInstanceError, replace
from decimal import Decimal
from pathlib import Path
import unittest

from src.domain.deal_case import (
    Currency,
    ForeignPayable,
    FxRates,
    reference_deal,
    reference_fx,
)
from src.finance.engine import evaluate_deal
from src.finance.fx_treasury import (
    ForwardAction,
    ForwardHedgeInput,
    FxExposureDirection,
    FxUnfavorableDirection,
    analyze_fx_treasury,
    build_currency_exposure_positions,
)


def canonical_analysis(deal=None):
    deal = reference_deal() if deal is None else deal
    current_fx = reference_fx()
    settlement_fx = FxRates(Decimal("1330"), Decimal("990"))
    inputs = (
        ForwardHedgeInput(Currency.USD, Decimal("0.8"), Decimal("1395")),
        ForwardHedgeInput(Currency.JPY, Decimal("0.8"), Decimal("905")),
    )
    return deal, current_fx, settlement_fx, inputs, analyze_fx_treasury(
        deal=deal,
        current_fx=current_fx,
        settlement_fx=settlement_fx,
        hedge_inputs=inputs,
    )


class FxTreasuryTests(unittest.TestCase):
    def test_positions_are_frozen_and_canonical_usd_position(self):
        positions = build_currency_exposure_positions(reference_deal())
        usd = positions[0]
        self.assertIs(usd.currency, Currency.USD)
        self.assertEqual(usd.receivable_amount, Decimal("100000"))
        self.assertEqual(usd.payable_amount, Decimal("20000"))
        self.assertEqual(usd.amount_offset, Decimal("20000"))
        self.assertEqual(usd.net_exposure, Decimal("80000"))
        self.assertEqual(usd.open_exposure, Decimal("80000"))
        self.assertIs(usd.direction, FxExposureDirection.RECEIVABLE)
        self.assertIs(usd.unfavorable_direction, FxUnfavorableDirection.FX_DOWN)
        with self.assertRaises(FrozenInstanceError):
            usd.open_exposure = Decimal("0")

    def test_canonical_jpy_position(self):
        jpy = build_currency_exposure_positions(reference_deal())[1]
        self.assertIs(jpy.currency, Currency.JPY)
        self.assertEqual(jpy.receivable_amount, Decimal("0"))
        self.assertEqual(jpy.payable_amount, Decimal("3000000"))
        self.assertEqual(jpy.amount_offset, Decimal("0"))
        self.assertEqual(jpy.net_exposure, Decimal("-3000000"))
        self.assertEqual(jpy.open_exposure, Decimal("3000000"))
        self.assertIs(jpy.direction, FxExposureDirection.PAYABLE)
        self.assertIs(jpy.unfavorable_direction, FxUnfavorableDirection.FX_UP)

    def test_forward_input_validation(self):
        invalid = (
            (Currency.USD, Decimal("-0.01"), Decimal("1")),
            (Currency.USD, Decimal("1.01"), Decimal("1")),
            (Currency.USD, Decimal("0.5"), Decimal("0")),
            (Currency.USD, Decimal("0.5"), Decimal("-1")),
            (Currency.KRW, Decimal("0.5"), Decimal("1")),
        )
        for currency, ratio, quote in invalid:
            with self.subTest(currency=currency, ratio=ratio, quote=quote):
                with self.assertRaises(ValueError):
                    ForwardHedgeInput(currency, ratio, quote)

    def test_actions_and_canonical_hedge_notionals(self):
        *_, analysis = canonical_analysis()
        usd, jpy = analysis.settlement_scenario_hedges
        self.assertIs(usd.action, ForwardAction.SELL)
        self.assertEqual(usd.hedged_notional, Decimal("64000.0"))
        self.assertEqual(usd.residual_exposure, Decimal("16000.0"))
        self.assertIs(jpy.action, ForwardAction.BUY)
        self.assertEqual(jpy.hedged_notional, Decimal("2400000.0"))
        self.assertEqual(jpy.residual_exposure, Decimal("600000.0"))

    def test_flat_position_derives_none_action(self):
        deal = replace(
            reference_deal(),
            foreign_payables=(
                ForeignPayable(Currency.USD, Decimal("100000"), 30),
                reference_deal().foreign_payables[1],
            ),
        )
        *_, analysis = canonical_analysis(deal)
        usd = analysis.settlement_scenario_hedges[0]
        self.assertIs(usd.action, ForwardAction.NONE)
        self.assertEqual(usd.hedged_notional, Decimal("0.0"))
        self.assertEqual(usd.hedge_effect_on_profit_krw, Decimal("0.0"))

    def test_jpy_quote_is_normalized_per_100(self):
        *_, analysis = canonical_analysis()
        jpy = analysis.settlement_scenario_hedges[1]
        self.assertEqual(jpy.forward_rate_quote, Decimal("905"))
        self.assertEqual(jpy.settlement_spot_quote, Decimal("990"))
        self.assertEqual(jpy.hedge_effect_on_profit_krw, Decimal("2040000.000"))

    def test_adverse_settlement_effects(self):
        *_, analysis = canonical_analysis()
        usd, jpy = analysis.settlement_scenario_hedges
        self.assertEqual(usd.hedge_effect_on_profit_krw, Decimal("4160000.0"))
        self.assertEqual(jpy.hedge_effect_on_profit_krw, Decimal("2040000.000"))
        self.assertEqual(analysis.settlement_scenario_total_effect_krw, Decimal("6200000.000"))

    def test_current_spot_tradeoff_effects(self):
        *_, analysis = canonical_analysis()
        usd, jpy = analysis.current_spot_hedges
        self.assertEqual(usd.hedge_effect_on_profit_krw, Decimal("-320000.0"))
        self.assertEqual(jpy.hedge_effect_on_profit_krw, Decimal("-120000.000"))
        self.assertEqual(analysis.current_spot_total_effect_krw, Decimal("-440000.000"))

    def test_overlays_use_frozen_engine_results_and_exact_margins(self):
        deal, current_fx, settlement_fx, _, analysis = canonical_analysis()
        current = evaluate_deal(deal, current_fx)
        adverse = evaluate_deal(deal, settlement_fx)
        self.assertEqual(analysis.current_spot_result, current)
        self.assertEqual(analysis.settlement_scenario_result, adverse)
        self.assertEqual(
            analysis.current_spot_overlay.unhedged_margin,
            Decimal("0.1463647749510763209393346380"),
        )
        self.assertEqual(
            analysis.current_spot_overlay.simulated_margin_after_hedge,
            Decimal("0.1432219178082191780821917809"),
        )
        self.assertEqual(
            analysis.settlement_scenario_overlay.unhedged_margin,
            Decimal("0.09158504480379029766196312699"),
        )
        self.assertEqual(
            analysis.settlement_scenario_overlay.simulated_margin_after_hedge,
            Decimal("0.1382015861571737563085796683"),
        )

    def test_analysis_is_deterministic_and_inputs_are_unchanged(self):
        deal, current_fx, settlement_fx, inputs, first = canonical_analysis()
        second = analyze_fx_treasury(
            deal=deal,
            current_fx=current_fx,
            settlement_fx=settlement_fx,
            hedge_inputs=inputs,
        )
        self.assertEqual(first, second)
        self.assertEqual(deal, reference_deal())
        self.assertEqual(current_fx, reference_fx())
        self.assertEqual(settlement_fx, FxRates(Decimal("1330"), Decimal("990")))

    def test_requires_exactly_one_supported_input_per_currency(self):
        deal = reference_deal()
        with self.assertRaises(ValueError):
            analyze_fx_treasury(
                deal=deal,
                current_fx=reference_fx(),
                settlement_fx=reference_fx(),
                hedge_inputs=(
                    ForwardHedgeInput(Currency.USD, Decimal("0.8"), Decimal("1395")),
                ),
            )

    def test_module_has_no_ai_external_liquidity_or_extra_currency_dependency(self):
        source = (
            Path(__file__).resolve().parents[1] / "src/finance/fx_treasury.py"
        ).read_text()
        self.assertNotIn("src.ai", source)
        self.assertNotIn("src.external", source)
        self.assertNotIn("src.finance.liquidity", source)
        self.assertNotIn("EUR", source)
        self.assertNotIn("CNY", source)


if __name__ == "__main__":
    unittest.main()
