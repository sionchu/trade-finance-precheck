from dataclasses import FrozenInstanceError, replace
from decimal import Decimal
import unittest

from src.domain.deal_case import Currency, Sale, reference_deal, reference_fx
from src.finance.engine import Scenario, evaluate_scenario
from src.finance.rescue import (
    RescueLever,
    RescueStatus,
    analyze_deal_rescue,
)


class DealRescueTests(unittest.TestCase):
    def setUp(self):
        self.deal = reference_deal()
        self.fx = reference_fx()
        self.analysis = analyze_deal_rescue(self.deal, self.fx)

    def option(self, lever):
        return next(option for option in self.analysis.options if option.lever is lever)

    def margin_for_sale(self, amount):
        deal = replace(self.deal, sale=replace(self.deal.sale, amount=amount))
        return evaluate_scenario(deal, self.fx, Scenario.COMBINED).financing_adjusted_deal_margin

    def margin_for_payable(self, currency, amount):
        payables = tuple(
            replace(payable, amount=amount)
            if payable.currency is currency
            else payable
            for payable in self.deal.foreign_payables
        )
        deal = replace(self.deal, foreign_payables=payables)
        return evaluate_scenario(deal, self.fx, Scenario.COMBINED).financing_adjusted_deal_margin

    def test_canonical_combined_requires_rescue(self):
        self.assertTrue(self.analysis.needs_rescue)
        self.assertAlmostEqual(
            self.analysis.baseline_margin,
            Decimal("0.088252"),
            delta=Decimal("0.000001"),
        )

    def test_canonical_combined_minimum_sale_threshold(self):
        option = self.option(RescueLever.SALE_AMOUNT_USD)
        self.assertEqual(option.status, RescueStatus.FEASIBLE)
        self.assertAlmostEqual(
            option.threshold_value, Decimal("106017.21"), delta=Decimal("0.01")
        )

    def test_canonical_combined_maximum_usd_payable_threshold(self):
        option = self.option(RescueLever.USD_PAYABLE_AMOUNT)
        self.assertEqual(option.status, RescueStatus.FEASIBLE)
        self.assertAlmostEqual(
            option.threshold_value, Decimal("14898.16"), delta=Decimal("0.01")
        )

    def test_canonical_combined_maximum_jpy_payable_threshold(self):
        option = self.option(RescueLever.JPY_PAYABLE_AMOUNT)
        self.assertEqual(option.status, RescueStatus.FEASIBLE)
        self.assertAlmostEqual(
            option.threshold_value, Decimal("2314601.91"), delta=Decimal("0.01")
        )

    def test_canonical_combined_collection_day_is_infeasible(self):
        option = self.option(RescueLever.COLLECTION_DAY)
        self.assertEqual(option.status, RescueStatus.INFEASIBLE)
        earliest = replace(self.deal, sale=replace(self.deal.sale, collection_day=0))
        result = evaluate_scenario(earliest, self.fx, Scenario.COMBINED)
        self.assertLess(result.financing_adjusted_deal_margin, self.deal.target_margin)

    def test_canonical_combined_funding_rate_is_infeasible(self):
        option = self.option(RescueLever.FUNDING_RATE)
        self.assertEqual(option.status, RescueStatus.INFEASIBLE)
        zero_rate = replace(self.deal, annual_funding_rate=Decimal("0"))
        result = evaluate_scenario(zero_rate, self.fx, Scenario.COMBINED)
        self.assertLess(result.financing_adjusted_deal_margin, self.deal.target_margin)

    def test_sale_threshold_boundary(self):
        threshold = self.option(RescueLever.SALE_AMOUNT_USD).threshold_value
        self.assertGreaterEqual(self.margin_for_sale(threshold), self.deal.target_margin)
        self.assertLess(self.margin_for_sale(threshold - Decimal("0.01")), self.deal.target_margin)

    def test_payable_threshold_boundaries(self):
        for lever, currency in (
            (RescueLever.USD_PAYABLE_AMOUNT, Currency.USD),
            (RescueLever.JPY_PAYABLE_AMOUNT, Currency.JPY),
        ):
            with self.subTest(lever=lever):
                threshold = self.option(lever).threshold_value
                self.assertGreaterEqual(
                    self.margin_for_payable(currency, threshold), self.deal.target_margin
                )
                self.assertLess(
                    self.margin_for_payable(currency, threshold + Decimal("0.01")),
                    self.deal.target_margin,
                )

    def test_base_scenario_needs_no_rescue(self):
        analysis = analyze_deal_rescue(self.deal, self.fx, Scenario.BASE)
        self.assertFalse(analysis.needs_rescue)
        self.assertEqual(analysis.options, ())

    def test_non_usd_sale_is_not_applicable(self):
        deal = replace(
            self.deal,
            sale=Sale(
                Currency.JPY,
                self.deal.sale.amount,
                self.deal.sale.payment_method,
                self.deal.sale.collection_day,
            ),
        )
        analysis = analyze_deal_rescue(deal, self.fx)
        option = next(
            item
            for item in analysis.options
            if item.lever is RescueLever.SALE_AMOUNT_USD
        )
        self.assertEqual(option.status, RescueStatus.NOT_APPLICABLE)

    def test_missing_usd_payable_is_not_applicable(self):
        deal = replace(
            self.deal,
            foreign_payables=tuple(
                item
                for item in self.deal.foreign_payables
                if item.currency is not Currency.USD
            ),
            target_margin=Decimal("0.50"),
        )
        analysis = analyze_deal_rescue(deal, self.fx)
        option = next(
            item
            for item in analysis.options
            if item.lever is RescueLever.USD_PAYABLE_AMOUNT
        )
        self.assertEqual(option.status, RescueStatus.NOT_APPLICABLE)

    def test_inputs_are_immutable_and_unchanged(self):
        original_deal = self.deal
        original_fx = self.fx
        analyze_deal_rescue(self.deal, self.fx)
        self.assertEqual(self.deal, original_deal)
        self.assertEqual(self.fx, original_fx)
        with self.assertRaises(FrozenInstanceError):
            self.analysis.needs_rescue = False

    def test_repeated_analysis_is_deterministic(self):
        self.assertEqual(self.analysis, analyze_deal_rescue(self.deal, self.fx))


if __name__ == "__main__":
    unittest.main()
