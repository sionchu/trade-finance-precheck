from dataclasses import FrozenInstanceError
from decimal import Decimal
from pathlib import Path
import unittest

from src.domain.deal_case import Currency, reference_deal, reference_fx
from src.finance.engine import evaluate_deal
from src.finance.liquidity import WorkingCapitalCreditLine
from src.finance.usance import BankersUsanceInput, analyze_bankers_usance


def canonical_analysis(payable_index: int = 1):
    deal = reference_deal()
    fx = reference_fx()
    base = evaluate_deal(deal, fx)
    line = WorkingCapitalCreditLine(Decimal("100000000"), Decimal("30000000"))
    usance_input = BankersUsanceInput(
        payable_index=payable_index,
        repayment_day=90,
        annual_usance_rate=Decimal("0.048"),
        fee_rate=Decimal("0.0015"),
    )
    comparison = analyze_bankers_usance(
        deal=deal,
        fx=fx,
        base_result=base,
        credit_line=line,
        usance_input=usance_input,
    )
    return deal, fx, base, line, usance_input, comparison


class BankersUsanceTests(unittest.TestCase):
    def test_input_and_result_are_frozen(self):
        *_, usance_input, comparison = canonical_analysis()
        with self.assertRaises(FrozenInstanceError):
            usance_input.repayment_day = 120
        with self.assertRaises(FrozenInstanceError):
            comparison.usance.tenor_days = 30

    def test_input_and_selection_validation(self):
        invalid_input_args = (
            (-1, 90, Decimal("0.048"), Decimal("0")),
            (0, 90, Decimal("-0.01"), Decimal("0")),
            (0, 90, Decimal("0.048"), Decimal("-0.01")),
        )
        deal = reference_deal()
        base = evaluate_deal(deal, reference_fx())
        line = WorkingCapitalCreditLine(Decimal("100000000"), Decimal("30000000"))
        for args in invalid_input_args:
            with self.subTest(args=args):
                with self.assertRaises(ValueError):
                    BankersUsanceInput(*args)
        for item in (
            BankersUsanceInput(2, 90, Decimal("0.048"), Decimal("0")),
            BankersUsanceInput(1, 30, Decimal("0.048"), Decimal("0")),
            BankersUsanceInput(1, 20, Decimal("0.048"), Decimal("0")),
        ):
            with self.subTest(item=item):
                with self.assertRaises(ValueError):
                    analyze_bankers_usance(
                        deal=deal,
                        fx=reference_fx(),
                        base_result=base,
                        credit_line=line,
                        usance_input=item,
                    )

    def test_canonical_payable_principal_and_tenor(self):
        *_, comparison = canonical_analysis()
        result = comparison.usance
        self.assertIs(result.currency, Currency.JPY)
        self.assertEqual(result.principal_fcy, Decimal("3000000"))
        self.assertEqual(result.principal_krw, Decimal("27000000"))
        self.assertEqual(result.supplier_payment_day, 30)
        self.assertEqual(result.company_repayment_day, 90)
        self.assertEqual(result.tenor_days, 60)

    def test_canonical_interest_and_fee(self):
        *_, comparison = canonical_analysis()
        result = comparison.usance
        self.assertEqual(
            result.usance_interest_fcy,
            Decimal("23671.23287671232876712328767"),
        )
        self.assertEqual(
            result.usance_interest_krw,
            Decimal("213041.0958904109589041095890"),
        )
        self.assertEqual(result.usance_fee_fcy, Decimal("4500.0000"))
        self.assertEqual(result.usance_fee_krw, Decimal("40500.0000"))

    def test_original_deal_is_unchanged_and_cashflow_moves_to_repayment(self):
        deal, *_, comparison = canonical_analysis()
        self.assertEqual(deal, reference_deal())
        self.assertEqual(deal.foreign_payables[1].payment_day, 30)
        points = {point.day: point for point in comparison.usance.working_capital_funding.points}
        self.assertEqual(points[30].cumulative_deal_cash_krw, Decimal("-83000000"))
        self.assertEqual(points[60].cumulative_deal_cash_krw, Decimal("-92000000"))
        self.assertGreater(points[90].cumulative_deal_cash_krw, Decimal("0"))

    def test_working_capital_peaks_and_reduction(self):
        *_, comparison = canonical_analysis()
        self.assertEqual(comparison.base_working_capital_credit_krw, Decimal("69000000"))
        self.assertEqual(comparison.usance.peak_working_capital_credit_krw, Decimal("42000000"))
        self.assertEqual(comparison.working_capital_credit_reduction_krw, Decimal("27000000"))

    def test_frozen_schedule_supplies_exact_working_capital_interest(self):
        *_, comparison = canonical_analysis()
        self.assertEqual(
            comparison.usance.working_capital_funding.external_funding_cost_krw,
            Decimal("295890.4109589041095890410959"),
        )

    def test_total_costs_and_difference(self):
        *_, comparison = canonical_analysis()
        self.assertEqual(
            comparison.base_total_financing_cost_krw,
            Decimal("508931.5068493150684931506849"),
        )
        self.assertEqual(
            comparison.usance.total_financing_cost_krw,
            Decimal("549431.5068493150684931506849"),
        )
        self.assertEqual(comparison.financing_cost_difference_krw, Decimal("40500.0000000000000000000000"))

    def test_line_headroom_and_combined_bank_principal(self):
        *_, comparison = canonical_analysis()
        self.assertEqual(comparison.base_ordinary_line_headroom_krw, Decimal("1000000"))
        self.assertEqual(comparison.usance.ordinary_line_headroom_krw, Decimal("28000000"))
        self.assertEqual(
            comparison.usance.peak_combined_bank_principal_krw,
            Decimal("69000000"),
        )
        self.assertEqual(
            comparison.usance.peak_combined_bank_principal_krw,
            comparison.base_working_capital_credit_krw,
        )

    def test_usd_payable_can_be_selected(self):
        *_, comparison = canonical_analysis(payable_index=0)
        self.assertIs(comparison.usance.currency, Currency.USD)
        self.assertEqual(comparison.usance.principal_fcy, Decimal("20000"))
        self.assertEqual(comparison.usance.principal_krw, Decimal("28000000"))

    def test_analysis_is_deterministic(self):
        deal, fx, base, line, usance_input, first = canonical_analysis()
        second = analyze_bankers_usance(
            deal=deal,
            fx=fx,
            base_result=base,
            credit_line=line,
            usance_input=usance_input,
        )
        self.assertEqual(first, second)

    def test_scope_dependencies_and_boundaries(self):
        source = (Path(__file__).resolve().parents[1] / "src/finance/usance.py").read_text()
        self.assertNotIn("src.ai", source)
        self.assertNotIn("src.external", source)
        self.assertNotIn("fx_treasury", source)
        self.assertNotIn("PaymentMethod", source)
        self.assertNotIn("LetterOfCredit", source)
        self.assertNotIn("UPAS", source)


if __name__ == "__main__":
    unittest.main()
