from dataclasses import asdict
from decimal import Decimal
import os
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from pydantic import ValidationError

from src.ai.financial_statement import (
    CompanyLiquidityProfile,
    FinancialStatementError,
    FinancialStatementFinancialization,
    StatementFact,
    analyze_demo_financial_statement,
    build_company_liquidity_profile,
    normalize_nonnegative_krw_amount,
    normalize_signed_krw_amount,
)


def fact(amount: str | None, *, review: bool = False) -> StatementFact:
    return StatementFact(
        amount_krw=amount,
        period_end="2025-12-31",
        source_filename="Company_Financial_Statement.pdf",
        evidence="2025-12-31 current period",
        needs_review=review,
    )


def demo_analysis(**overrides) -> FinancialStatementFinancialization:
    values = {
        "cash_and_cash_equivalents": fact("120,000,000"),
        "short_term_financial_instruments": fact("30,000,000"),
        "accounts_receivable": fact("240,000,000"),
        "inventory": fact("180,000,000"),
        "current_assets": fact("650,000,000"),
        "current_liabilities": fact("470,000,000"),
        "short_term_borrowings": fact("160,000,000"),
        "finance_cost": fact("12,000,000"),
        "operating_cash_flow": fact("85,000,000"),
        "review_notes": (),
    }
    values.update(overrides)
    return FinancialStatementFinancialization(**values)


class FinancialStatementTests(unittest.TestCase):
    def test_exact_supported_schema_fields(self):
        self.assertEqual(
            set(FinancialStatementFinancialization.model_fields),
            {
                "cash_and_cash_equivalents",
                "short_term_financial_instruments",
                "accounts_receivable",
                "inventory",
                "current_assets",
                "current_liabilities",
                "short_term_borrowings",
                "finance_cost",
                "operating_cash_flow",
                "review_notes",
            },
        )
        with self.assertRaises(ValidationError):
            FinancialStatementFinancialization(
                **demo_analysis().model_dump(), retained_earnings=fact("520000000")
            )

    def test_source_filename_is_exact(self):
        with self.assertRaises(ValidationError):
            StatementFact(
                amount_krw="1",
                period_end="2025-12-31",
                source_filename="statement.pdf",
                evidence="current period",
                needs_review=False,
            )

    def test_nonnegative_amount_normalization(self):
        self.assertEqual(
            normalize_nonnegative_krw_amount("120,000,000"), Decimal("120000000")
        )
        self.assertIsNone(normalize_nonnegative_krw_amount(None))
        with self.assertRaises(ValueError):
            normalize_nonnegative_krw_amount("-1")

    def test_signed_operating_cash_flow_normalization(self):
        self.assertEqual(normalize_signed_krw_amount("-1,000"), Decimal("-1000"))
        self.assertEqual(normalize_signed_krw_amount("85,000,000"), Decimal("85000000"))

    def test_malformed_amounts_are_rejected(self):
        for value in ("", "KRW 100", "1,2,3", "n/a", "+100", "100원"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                normalize_nonnegative_krw_amount(value)

    def test_missing_fact_stays_none_and_review_does_not_block_profile(self):
        analysis = demo_analysis(finance_cost=fact(None, review=True))
        profile = build_company_liquidity_profile(analysis)
        self.assertIsNone(profile.finance_cost_krw)
        self.assertEqual(profile.cash_and_cash_equivalents_krw, Decimal("120000000"))

    def test_current_period_values_build_expected_profile(self):
        profile = build_company_liquidity_profile(demo_analysis())
        self.assertEqual(profile.cash_and_cash_equivalents_krw, Decimal("120000000"))
        self.assertEqual(profile.short_term_financial_instruments_krw, Decimal("30000000"))
        self.assertEqual(profile.accounts_receivable_krw, Decimal("240000000"))
        self.assertEqual(profile.inventory_krw, Decimal("180000000"))
        self.assertEqual(profile.current_assets_krw, Decimal("650000000"))
        self.assertEqual(profile.current_liabilities_krw, Decimal("470000000"))
        self.assertEqual(profile.short_term_borrowings_krw, Decimal("160000000"))
        self.assertEqual(profile.finance_cost_krw, Decimal("12000000"))
        self.assertEqual(profile.operating_cash_flow_krw, Decimal("85000000"))

    def test_profile_has_no_retained_earnings_or_available_cash(self):
        fields = set(CompanyLiquidityProfile.__dataclass_fields__)
        self.assertNotIn("retained_earnings_krw", fields)
        self.assertNotIn("available_cash_krw", fields)

    def test_builder_is_deterministic_and_source_is_immutable(self):
        analysis = demo_analysis()
        before = analysis.model_dump()
        first = build_company_liquidity_profile(analysis)
        second = build_company_liquidity_profile(analysis)
        self.assertEqual(first, second)
        self.assertEqual(analysis.model_dump(), before)
        self.assertEqual(asdict(first)["cash_and_cash_equivalents_krw"], Decimal("120000000"))

    def test_one_pdf_one_request_and_canonical_sdk_settings(self):
        client = Mock()
        expected = demo_analysis()
        client.responses.parse.return_value = SimpleNamespace(output_parsed=expected)
        pdf = Path(__file__).resolve().parents[1] / "assets/demo/Company_Financial_Statement.pdf"
        result = analyze_demo_financial_statement(pdf, client=client)
        self.assertIs(result, expected)
        client.responses.parse.assert_called_once()
        request = client.responses.parse.call_args.kwargs
        self.assertEqual(request["model"], "gpt-5.6-luna")
        self.assertEqual(request["reasoning"], {"effort": "low"})
        self.assertIs(request["store"], False)
        self.assertNotIn("tools", request)
        self.assertEqual(len(request["input"][0]["content"]), 1)
        self.assertEqual(
            request["input"][0]["content"][0]["filename"],
            "Company_Financial_Statement.pdf",
        )

    def test_missing_api_key_is_safe(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": ""}, clear=False):
            with self.assertRaises(FinancialStatementError):
                analyze_demo_financial_statement(Path("unused.pdf"))

    def test_provider_failure_is_safe(self):
        client = Mock()
        client.responses.parse.side_effect = RuntimeError("provider details")
        pdf = (
            Path(__file__).resolve().parents[1]
            / "assets/demo/Company_Financial_Statement.pdf"
        )
        with self.assertRaisesRegex(FinancialStatementError, "analysis failed") as caught:
            analyze_demo_financial_statement(pdf, client=client)
        self.assertNotIn("provider details", str(caught.exception))

    def test_analysis_function_requires_no_deal(self):
        self.assertNotIn(
            "deal", analyze_demo_financial_statement.__annotations__
        )


if __name__ == "__main__":
    unittest.main()
