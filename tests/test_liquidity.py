from dataclasses import FrozenInstanceError, replace
from decimal import Decimal
from pathlib import Path
import unittest

from src.domain.deal_case import PaymentMethod, reference_deal, reference_fx
from src.finance.engine import (
    Scenario,
    canonical_purchase_option,
    evaluate_deal,
    evaluate_scenario,
)
from src.finance.liquidity import (
    FundingChoice,
    FundingChoiceStatus,
    WorkingCapitalCreditLine,
    analyze_company_funding,
)


def canonical_inputs(
    *,
    credit_line: WorkingCapitalCreditLine | None = None,
    deal=None,
):
    deal = reference_deal() if deal is None else deal
    fx = reference_fx()
    base = evaluate_deal(deal, fx)
    combined = evaluate_scenario(deal, fx, Scenario.COMBINED)
    purchase = None
    if deal.sale.payment_method is PaymentMethod.OA:
        purchase = evaluate_deal(
            deal,
            fx,
            purchase_option=canonical_purchase_option(),
        )
    line = credit_line or WorkingCapitalCreditLine(
        total_limit_krw=Decimal("100000000"),
        used_amount_krw=Decimal("30000000"),
    )
    analysis = analyze_company_funding(
        deal=deal,
        base_result=base,
        combined_result=combined,
        credit_line=line,
        purchase_result=purchase,
    )
    choices = {item.choice: item for item in analysis.choices}
    return deal, fx, base, combined, purchase, line, analysis, choices


class CompanyLiquidityTests(unittest.TestCase):
    def test_credit_line_is_immutable_and_unused_is_derived(self):
        line = WorkingCapitalCreditLine(Decimal("100000000"), Decimal("30000000"))
        self.assertEqual(line.unused_limit_krw, Decimal("70000000"))
        self.assertNotIn("unused_limit_krw", line.__dataclass_fields__)
        with self.assertRaises(FrozenInstanceError):
            line.total_limit_krw = Decimal("1")

    def test_credit_line_validation(self):
        invalid = (
            (Decimal("-1"), Decimal("0"), Decimal("0")),
            (Decimal("1"), Decimal("-1"), Decimal("0")),
            (Decimal("1"), Decimal("2"), Decimal("0")),
            (Decimal("1"), Decimal("0"), Decimal("-1")),
        )
        for total, used, fee in invalid:
            with self.subTest(total=total, used=used, fee=fee):
                with self.assertRaises(ValueError):
                    WorkingCapitalCreditLine(total, used, fee)

    def test_canonical_base_capacity(self):
        *_, analysis, _ = canonical_inputs()
        self.assertEqual(analysis.base_capacity.required_external_funding_krw, Decimal("69000000"))
        self.assertEqual(analysis.base_capacity.unused_credit_limit_krw, Decimal("70000000"))
        self.assertEqual(analysis.base_capacity.credit_headroom_krw, Decimal("1000000"))
        self.assertEqual(analysis.base_capacity.liquidity_gap_krw, Decimal("0"))
        self.assertTrue(analysis.base_capacity.feasible)

    def test_canonical_combined_capacity(self):
        *_, analysis, _ = canonical_inputs()
        self.assertEqual(analysis.combined_capacity.required_external_funding_krw, Decimal("70300000.0000"))
        self.assertEqual(analysis.combined_capacity.credit_headroom_krw, Decimal("0"))
        self.assertEqual(analysis.combined_capacity.liquidity_gap_krw, Decimal("300000.0000"))
        self.assertFalse(analysis.combined_capacity.feasible)

    def test_internal_cash_only_is_infeasible_for_canonical_deal(self):
        *_, choices = canonical_inputs()
        result = choices[FundingChoice.INTERNAL_CASH_ONLY]
        self.assertIs(result.status, FundingChoiceStatus.INFEASIBLE)
        self.assertEqual(result.liquidity_gap_krw, Decimal("69000000"))
        self.assertIsNone(result.total_financing_cost_krw)

    def test_enough_deal_cash_makes_internal_only_feasible(self):
        deal = replace(reference_deal(), available_cash_krw=Decimal("119000000"))
        *_, choices = canonical_inputs(deal=deal)
        result = choices[FundingChoice.INTERNAL_CASH_ONLY]
        self.assertIs(result.status, FundingChoiceStatus.FEASIBLE)
        self.assertEqual(result.required_external_funding_krw, Decimal("0"))
        self.assertEqual(result.total_financing_cost_krw, Decimal("0"))

    def test_wait_uses_frozen_engine_interest_and_is_feasible(self):
        _, _, base, _, _, _, _, choices = canonical_inputs()
        result = choices[FundingChoice.WAIT_WITH_CREDIT_LINE]
        self.assertIs(result.status, FundingChoiceStatus.FEASIBLE)
        self.assertEqual(result.interest_cost_krw, base.funding.external_funding_cost_krw)
        self.assertEqual(result.total_financing_cost_krw, base.funding.external_funding_cost_krw)
        self.assertEqual(result.cash_inflow_day, 90)

    def test_canonical_early_purchase_tradeoff(self):
        _, _, base, _, purchase, _, _, choices = canonical_inputs()
        wait = choices[FundingChoice.WAIT_WITH_CREDIT_LINE]
        early = choices[FundingChoice.EARLY_RECEIVABLE_PURCHASE]
        self.assertIs(early.status, FundingChoiceStatus.FEASIBLE)
        self.assertEqual(early.required_external_funding_krw, wait.required_external_funding_krw)
        self.assertEqual(early.required_external_funding_krw, Decimal("69000000"))
        self.assertEqual(
            wait.interest_cost_krw,
            Decimal("508931.5068493150684931506849"),
        )
        self.assertEqual(
            early.interest_cost_krw,
            Decimal("282082.1917808219178082191781"),
        )
        self.assertLess(early.interest_cost_krw, wait.interest_cost_krw)
        expected_other = (
            purchase.receivable_purchase.discount_cost_krw
            + purchase.receivable_purchase.purchase_fee_krw
        )
        self.assertEqual(early.other_financing_cost_krw, expected_other)
        self.assertEqual(
            early.total_financing_cost_krw,
            purchase.funding.external_funding_cost_krw + expected_other,
        )
        self.assertGreater(early.total_financing_cost_krw, wait.total_financing_cost_krw)
        self.assertEqual(
            early.total_financing_cost_krw,
            Decimal("990712.3287671232876712328767"),
        )
        self.assertEqual(early.cash_inflow_day, 65)

    def test_explicit_fee_is_included_only_when_credit_is_needed(self):
        fee = Decimal("250000")
        line = WorkingCapitalCreditLine(Decimal("100000000"), Decimal("30000000"), fee)
        _, _, _, _, purchase, _, _, choices = canonical_inputs(credit_line=line)
        wait = choices[FundingChoice.WAIT_WITH_CREDIT_LINE]
        early = choices[FundingChoice.EARLY_RECEIVABLE_PURCHASE]
        self.assertEqual(wait.other_financing_cost_krw, fee)
        self.assertEqual(
            early.other_financing_cost_krw,
            purchase.receivable_purchase.discount_cost_krw
            + purchase.receivable_purchase.purchase_fee_krw
            + fee,
        )

        rich_deal = replace(reference_deal(), available_cash_krw=Decimal("119000000"))
        *_, rich_choices = canonical_inputs(deal=rich_deal, credit_line=line)
        self.assertEqual(
            rich_choices[FundingChoice.WAIT_WITH_CREDIT_LINE].other_financing_cost_krw,
            Decimal("0"),
        )

    def test_insufficient_line_blocks_wait_and_early_purchase(self):
        line = WorkingCapitalCreditLine(Decimal("90000000"), Decimal("30000000"))
        *_, choices = canonical_inputs(credit_line=line)
        for choice in (FundingChoice.WAIT_WITH_CREDIT_LINE, FundingChoice.EARLY_RECEIVABLE_PURCHASE):
            result = choices[choice]
            self.assertIs(result.status, FundingChoiceStatus.INFEASIBLE)
            self.assertEqual(result.liquidity_gap_krw, Decimal("9000000"))
            self.assertIsNone(result.total_financing_cost_krw)

    def test_tt_makes_early_purchase_not_applicable(self):
        deal = replace(
            reference_deal(),
            sale=replace(reference_deal().sale, payment_method=PaymentMethod.TT),
        )
        *_, choices = canonical_inputs(deal=deal)
        result = choices[FundingChoice.EARLY_RECEIVABLE_PURCHASE]
        self.assertIs(result.status, FundingChoiceStatus.NOT_APPLICABLE)
        self.assertIsNone(result.cash_inflow_day)

    def test_analysis_is_deterministic_and_inputs_are_unchanged(self):
        deal, _, base, combined, purchase, line, first, _ = canonical_inputs()
        second = analyze_company_funding(
            deal=deal,
            base_result=base,
            combined_result=combined,
            credit_line=line,
            purchase_result=purchase,
        )
        self.assertEqual(first, second)
        self.assertEqual(deal, reference_deal())

    def test_module_has_no_ai_external_or_company_profile_dependency(self):
        source = (Path(__file__).resolve().parents[1] / "src/finance/liquidity.py").read_text()
        self.assertNotIn("src.ai", source)
        self.assertNotIn("src.external", source)
        self.assertNotIn("CompanyLiquidityProfile", source)


if __name__ == "__main__":
    unittest.main()
