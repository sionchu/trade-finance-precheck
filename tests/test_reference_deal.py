import unittest
from dataclasses import FrozenInstanceError, replace
from decimal import Decimal

from src.domain.deal_case import (
    Currency,
    FxRates,
    PaymentMethod,
    reference_deal,
    reference_fx,
)
from src.finance.engine import (
    Scenario,
    canonical_purchase_option,
    canonical_scenarios,
    evaluate_deal,
    evaluate_scenario,
    solve_usd_krw_threshold,
)


MILLION = Decimal("1000000")
ZERO = Decimal("0")


class DecimalAssertions(unittest.TestCase):
    def assertDecimalClose(self, actual, expected, tolerance):
        self.assertLessEqual(abs(actual - Decimal(expected)), Decimal(tolerance))


class RequiredDeterministicTests(DecimalAssertions):
    def setUp(self):
        self.deal = reference_deal()
        self.fx = reference_fx()

    def test_01_base_deal_economics(self):
        result = evaluate_deal(self.deal, self.fx)
        self.assertEqual(result.sales_krw, Decimal("140000000"))
        self.assertEqual(result.total_non_funding_cost_krw, Decimal("119000000"))
        self.assertEqual(result.gross_deal_profit_krw, Decimal("21000000"))
        self.assertEqual(result.gross_deal_margin, Decimal("0.15"))
        self.assertEqual(result.currency_exposure[Currency.USD], Decimal("80000"))
        self.assertEqual(result.currency_exposure[Currency.JPY], Decimal("-3000000"))

    def test_02_base_external_financing_schedule(self):
        result = evaluate_deal(self.deal, self.fx)
        points = {
            point.day: point.external_loan_outstanding_krw
            for point in result.funding.points
        }
        self.assertEqual(points, {
            0: Decimal("0"),
            30: Decimal("60000000"),
            60: Decimal("69000000"),
            90: Decimal("0"),
        })
        self.assertEqual(result.funding.peak_deal_funding_krw, Decimal("119000000"))
        self.assertEqual(
            result.funding.maximum_external_borrowing_krw, Decimal("69000000")
        )
        self.assertDecimalClose(
            result.funding.external_funding_cost_krw / MILLION, "0.509", "0.001"
        )

    def test_03_usd_down_5_percent(self):
        result = evaluate_scenario(self.deal, self.fx, Scenario.USD_DOWN_5)
        self.assertEqual(result.sales_krw, Decimal("133000000.00"))
        self.assertEqual(result.total_non_funding_cost_krw, Decimal("117600000.00"))
        self.assertEqual(result.gross_deal_profit_krw, Decimal("15400000.00"))
        self.assertEqual(
            result.funding.maximum_external_borrowing_krw, Decimal("67600000.00")
        )
        self.assertDecimalClose(
            result.funding.external_funding_cost_krw / MILLION, "0.498", "0.001"
        )
        self.assertDecimalClose(result.financing_adjusted_deal_margin, "0.1120", "0.0001")

    def test_04_jpy_up_10_percent(self):
        result = evaluate_scenario(self.deal, self.fx, Scenario.JPY_UP_10)
        self.assertEqual(result.total_non_funding_cost_krw, Decimal("121700000.000"))
        self.assertEqual(result.gross_deal_profit_krw, Decimal("18300000.000"))
        self.assertEqual(
            result.funding.maximum_external_borrowing_krw, Decimal("71700000.000")
        )
        self.assertDecimalClose(
            result.funding.external_funding_cost_krw / MILLION, "0.530", "0.001"
        )
        self.assertDecimalClose(result.financing_adjusted_deal_margin, "0.1269", "0.0001")

    def test_05_funding_rate_up_1_percentage_point(self):
        result = evaluate_scenario(self.deal, self.fx, Scenario.RATE_UP_1PP)
        self.assertDecimalClose(
            result.funding.external_funding_cost_krw / MILLION, "0.615", "0.001"
        )
        self.assertDecimalClose(result.financing_adjusted_deal_margin, "0.1456", "0.0001")

    def test_06_payment_delay_30_days(self):
        result = evaluate_scenario(self.deal, self.fx, Scenario.DELAY_30D)
        self.assertEqual(result.collection_day, 120)
        self.assertEqual(
            result.funding.maximum_external_borrowing_krw, Decimal("69000000")
        )
        self.assertDecimalClose(
            result.funding.external_funding_cost_krw / MILLION, "0.781", "0.001"
        )
        self.assertDecimalClose(result.financing_adjusted_deal_margin, "0.1444", "0.0001")

    def test_07_combined_stress(self):
        result = evaluate_scenario(self.deal, self.fx, Scenario.COMBINED)
        self.assertEqual(result.sales_krw, Decimal("133000000.00"))
        self.assertEqual(result.total_non_funding_cost_krw, Decimal("120300000.000"))
        self.assertEqual(result.gross_deal_profit_krw, Decimal("12700000.000"))
        self.assertEqual(
            result.funding.maximum_external_borrowing_krw, Decimal("70300000.000")
        )
        self.assertDecimalClose(
            result.funding.external_funding_cost_krw / MILLION, "0.962", "0.001"
        )
        self.assertDecimalClose(
            result.financing_adjusted_deal_profit_krw / MILLION, "11.738", "0.001"
        )
        self.assertDecimalClose(result.financing_adjusted_deal_margin, "0.0883", "0.0001")

    def test_08_zero_profit_usd_threshold(self):
        threshold = solve_usd_krw_threshold(self.deal, self.fx, None)
        self.assertDecimalClose(threshold, "1143", "1")
        result = evaluate_deal(self.deal, replace(self.fx, usd_krw=threshold))
        self.assertDecimalClose(result.financing_adjusted_deal_profit_krw, "0", "0.10")

    def test_09_target_margin_usd_threshold(self):
        threshold = solve_usd_krw_threshold(
            self.deal, self.fx, self.deal.target_margin
        )
        self.assertDecimalClose(threshold, "1386", "1")
        result = evaluate_deal(self.deal, replace(self.fx, usd_krw=threshold))
        self.assertDecimalClose(
            result.financing_adjusted_deal_margin, self.deal.target_margin, "0.000000001"
        )

    def test_10_receivable_held_to_maturity(self):
        result = evaluate_deal(self.deal, self.fx)
        self.assertIsNone(result.receivable_purchase)
        self.assertEqual(result.collection_day, 90)
        self.assertEqual(result.funding.points[-1].day, 90)
        self.assertEqual(result.funding.points[-1].external_loan_outstanding_krw, ZERO)

    def test_11_early_receivable_purchase(self):
        option = canonical_purchase_option()
        result = evaluate_deal(self.deal, self.fx, purchase_option=option)
        purchase = result.receivable_purchase
        self.assertIsNotNone(purchase)
        self.assertEqual(result.collection_day, 90)
        self.assertEqual(purchase.purchase_day, 65)
        self.assertEqual(purchase.remaining_tenor_days, 25)
        self.assertDecimalClose(purchase.discount_cost_krw / MILLION, "0.499", "0.001")
        self.assertEqual(purchase.purchase_fee_krw, Decimal("210000.0000"))
        self.assertDecimalClose(
            result.funding.external_funding_cost_krw / MILLION, "0.282", "0.001"
        )
        total_cost = (
            result.funding.external_funding_cost_krw
            + purchase.discount_cost_krw
            + purchase.purchase_fee_krw
        )
        self.assertDecimalClose(total_cost / MILLION, "0.991", "0.001")

    def test_12_early_purchase_repays_external_borrowing(self):
        result = evaluate_deal(
            self.deal,
            self.fx,
            purchase_option=canonical_purchase_option(),
        )
        purchase_point = result.funding.points[-1]
        self.assertEqual(purchase_point.day, 65)
        self.assertEqual(purchase_point.external_loan_outstanding_krw, ZERO)
        self.assertTrue(all(interval.end_day <= 65 for interval in result.funding.intervals))

    def test_13_buyer_delay_changes_receivable_discount_tenor(self):
        base = evaluate_deal(
            self.deal,
            self.fx,
            purchase_option=canonical_purchase_option(),
        )
        delayed = evaluate_deal(
            self.deal,
            self.fx,
            collection_day=120,
            purchase_option=canonical_purchase_option(),
        )
        self.assertEqual(base.collection_day, 90)
        self.assertEqual(delayed.collection_day, 120)
        self.assertEqual(base.receivable_purchase.purchase_day, 65)
        self.assertEqual(delayed.receivable_purchase.purchase_day, 65)
        self.assertEqual(base.receivable_purchase.remaining_tenor_days, 25)
        self.assertEqual(delayed.receivable_purchase.remaining_tenor_days, 55)
        self.assertFalse(hasattr(canonical_purchase_option(), "buyer_due_day"))
        self.assertGreater(
            delayed.receivable_purchase.discount_cost_krw,
            base.receivable_purchase.discount_cost_krw,
        )
        self.assertLess(
            delayed.financing_adjusted_deal_margin,
            base.financing_adjusted_deal_margin,
        )

class CanonicalInvariantTests(DecimalAssertions):
    def setUp(self):
        self.deal = reference_deal()
        self.fx = reference_fx()
        self.base = evaluate_deal(self.deal, self.fx)

    def test_lower_usd_cannot_improve_positive_usd_exposure_deal(self):
        stressed = evaluate_deal(self.deal, replace(self.fx, usd_krw=Decimal("1300")))
        self.assertLess(stressed.financing_adjusted_deal_profit_krw, self.base.financing_adjusted_deal_profit_krw)

    def test_higher_jpy_cannot_improve_negative_jpy_exposure_deal(self):
        stressed = evaluate_deal(self.deal, replace(self.fx, jpy_krw_per_100=Decimal("1000")))
        self.assertLess(stressed.financing_adjusted_deal_profit_krw, self.base.financing_adjusted_deal_profit_krw)

    def test_higher_rate_cannot_reduce_borrowing_cost(self):
        stressed = evaluate_deal(replace(self.deal, annual_funding_rate=Decimal("0.06")), self.fx)
        self.assertGreaterEqual(stressed.funding.external_funding_cost_krw, self.base.funding.external_funding_cost_krw)

    def test_later_collection_cannot_reduce_hold_borrowing_cost(self):
        delayed = evaluate_deal(self.deal, self.fx, collection_day=120)
        self.assertGreaterEqual(delayed.funding.external_funding_cost_krw, self.base.funding.external_funding_cost_krw)

    def test_larger_available_cash_cannot_increase_maximum_borrowing(self):
        richer = evaluate_deal(replace(self.deal, available_cash_krw=Decimal("60000000")), self.fx)
        self.assertLessEqual(richer.funding.maximum_external_borrowing_krw, self.base.funding.maximum_external_borrowing_krw)

    def test_early_purchase_leaves_no_repaid_borrowing_outstanding(self):
        early = evaluate_deal(self.deal, self.fx, purchase_option=canonical_purchase_option())
        self.assertEqual(early.funding.points[-1].external_loan_outstanding_krw, ZERO)

    def test_higher_discount_rate_cannot_reduce_purchase_cost(self):
        option = canonical_purchase_option()
        base = evaluate_deal(self.deal, self.fx, purchase_option=option)
        higher = evaluate_deal(
            self.deal,
            self.fx,
            purchase_option=replace(option, annual_discount_rate=Decimal("0.06")),
        )
        self.assertGreaterEqual(
            higher.receivable_purchase.discount_cost_krw,
            base.receivable_purchase.discount_cost_krw,
        )

    def test_financial_results_are_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            self.base.sales_krw = Decimal("0")
        with self.assertRaises(TypeError):
            self.base.currency_exposure[Currency.USD] = Decimal("0")

    def test_early_purchase_uses_active_usd_fx_as_single_valuation_source(self):
        option = canonical_purchase_option()
        active_fx = replace(self.fx, usd_krw=Decimal("1300"))
        result = evaluate_deal(self.deal, active_fx, purchase_option=option)

        self.assertFalse(hasattr(option, "settlement_fx"))
        self.assertEqual(result.sales_krw, Decimal("130000000"))
        self.assertEqual(
            result.receivable_purchase.face_value_krw, result.sales_krw
        )

    def test_early_purchase_rejects_usd_tt_receivable(self):
        tt_deal = replace(
            self.deal,
            sale=replace(self.deal.sale, payment_method=PaymentMethod.TT),
        )

        with self.assertRaisesRegex(ValueError, "requires an O/A receivable"):
            evaluate_deal(tt_deal, self.fx, purchase_option=canonical_purchase_option())


class GenericCashflowTests(unittest.TestCase):
    def test_same_day_events_are_combined_and_sorted(self):
        result = evaluate_deal(reference_deal(), reference_fx())
        self.assertEqual([point.day for point in result.funding.points], [0, 30, 60, 90])

    def test_jpy_quote_is_per_100_jpy(self):
        fx = FxRates(Decimal("1400"), Decimal("900"))
        self.assertEqual(
            fx.to_krw(Decimal("3000000"), Currency.JPY), Decimal("27000000")
        )


if __name__ == "__main__":
    unittest.main()
