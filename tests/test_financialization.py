from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import Mock

from pydantic import ValidationError

from src.ai.financialization import (
    DocumentFinancialization,
    ExtractedPaymentMethod,
    FinancialEvent,
    HedgeStatus,
    ProposalBlockedError,
    Receivable,
    TimingAnchor,
    analyze_demo_documents,
    build_proposed_deal_patch,
    currency_exposure,
    normalize_amount,
)


def demo_financialization(**overrides) -> DocumentFinancialization:
    values = {
        "receivables": (
            Receivable(
                currency_code="USD",
                amount="100,000",
                timing_days=90,
                timing_anchor=TimingAnchor.SHIPMENT,
                payment_method=ExtractedPaymentMethod.OA,
                description="Machinery component sale",
                source_filename="Sales_Contract.pdf",
                evidence="Payment 90 days after shipment.",
                needs_review=False,
            ),
        ),
        "payables": (
            FinancialEvent(
                currency_code="USD",
                amount="20,000",
                timing_days=30,
                timing_anchor=TimingAnchor.CONTRACT_DATE,
                description="Raw materials",
                source_filename="Supplier_PO_US.pdf",
                evidence="Net 30 after Purchase Contract Date.",
                needs_review=False,
            ),
            FinancialEvent(
                currency_code="JPY",
                amount="3,000,000",
                timing_days=30,
                timing_anchor=TimingAnchor.CONTRACT_DATE,
                description="Precision components",
                source_filename="Supplier_PO_JP.pdf",
                evidence="Net 30 after Purchase Contract Date.",
                needs_review=False,
            ),
        ),
        "incoterm": "FOB Busan, Republic of Korea - Incoterms 2020",
        "hedge_status": HedgeStatus.NOT_FOUND,
        "available_company_cash": None,
        "company_borrowing_rate": None,
        "target_margin": None,
        "review_notes": ("Company facts are not stated.",),
    }
    values.update(overrides)
    return DocumentFinancialization(**values)


class FinancializationTests(unittest.TestCase):
    def test_strict_structured_model_rejects_extra_fields(self):
        with self.assertRaises(ValidationError):
            DocumentFinancialization(
                **demo_financialization().model_dump(), unexpected="value"
            )

    def test_source_filename_must_be_one_of_the_bundled_documents(self):
        with self.assertRaises(ValidationError):
            FinancialEvent.model_validate(
                {
                    **demo_financialization().payables[0].model_dump(),
                    "source_filename": "",
                }
            )

    def test_comma_decimal_parsing(self):
        self.assertEqual(normalize_amount("3,000,000"), Decimal("3000000"))
        self.assertEqual(normalize_amount("100000.00"), Decimal("100000.00"))

    def test_malformed_amount_rejection(self):
        for value in (None, "", "n/a", "USD 100", "1,2,3", "10.00.00"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                normalize_amount(value)

    def test_deterministic_usd_exposure(self):
        self.assertEqual(
            currency_exposure(demo_financialization())["USD"], Decimal("80000")
        )

    def test_deterministic_jpy_exposure(self):
        self.assertEqual(
            currency_exposure(demo_financialization())["JPY"], Decimal("-3000000")
        )

    def test_unsupported_eur_blocks_proposed_patch(self):
        eur = FinancialEvent(
            currency_code="EUR",
            amount="1",
            timing_days=30,
            timing_anchor=TimingAnchor.CONTRACT_DATE,
            description="EUR cost",
            source_filename="Supplier_PO_US.pdf",
            evidence="EUR 1",
            needs_review=False,
        )
        with self.assertRaisesRegex(ProposalBlockedError, "EUR"):
            build_proposed_deal_patch(
                demo_financialization(
                    payables=demo_financialization().payables + (eur,)
                ),
                contract_date_is_day_zero=True,
            )

    def test_unsupported_cny_blocks_proposed_patch(self):
        cny = FinancialEvent(
            currency_code="CNY",
            amount="1",
            timing_days=30,
            timing_anchor=TimingAnchor.CONTRACT_DATE,
            description="CNY cost",
            source_filename="Supplier_PO_US.pdf",
            evidence="CNY 1",
            needs_review=False,
        )
        with self.assertRaisesRegex(ProposalBlockedError, "CNY"):
            build_proposed_deal_patch(
                demo_financialization(
                    payables=demo_financialization().payables + (cny,)
                ),
                contract_date_is_day_zero=True,
            )

    def test_lc_does_not_become_oa(self):
        receivable = demo_financialization().receivables[0].model_copy(
            update={"payment_method": ExtractedPaymentMethod.LC}
        )
        with self.assertRaisesRegex(ProposalBlockedError, "payment method"):
            build_proposed_deal_patch(
                demo_financialization(receivables=(receivable,)),
                contract_date_is_day_zero=True,
            )

    def test_shipment_timing_does_not_enter_patch(self):
        patch = build_proposed_deal_patch(
            demo_financialization(), contract_date_is_day_zero=True
        )
        self.assertFalse(hasattr(patch, "collection_day"))

    def test_contract_date_maps_only_through_explicit_rule(self):
        unmapped = build_proposed_deal_patch(
            demo_financialization(), contract_date_is_day_zero=False
        )
        mapped = build_proposed_deal_patch(
            demo_financialization(), contract_date_is_day_zero=True
        )
        self.assertIsNone(unmapped.usd_payable_day)
        self.assertIsNone(unmapped.jpy_payable_day)
        self.assertEqual(mapped.usd_payable_day, 30)
        self.assertEqual(mapped.jpy_payable_day, 30)

    def test_not_found_is_unknown_not_no_hedge(self):
        result = demo_financialization()
        self.assertEqual(result.hedge_status, HedgeStatus.NOT_FOUND)
        self.assertNotEqual(result.hedge_status.value, "NONE")

    def test_present_hedge_blocks_patch(self):
        with self.assertRaisesRegex(ProposalBlockedError, "Hedge"):
            build_proposed_deal_patch(
                demo_financialization(hedge_status=HedgeStatus.PRESENT),
                contract_date_is_day_zero=True,
            )

    def test_flagged_event_blocks_patch(self):
        receivable = demo_financialization().receivables[0].model_copy(
            update={"needs_review": True}
        )
        with self.assertRaisesRegex(ProposalBlockedError, "require review"):
            build_proposed_deal_patch(
                demo_financialization(receivables=(receivable,)),
                contract_date_is_day_zero=True,
            )

    def test_ambiguous_hedge_blocks_patch(self):
        with self.assertRaisesRegex(ProposalBlockedError, "Hedge"):
            build_proposed_deal_patch(
                demo_financialization(hedge_status=HedgeStatus.AMBIGUOUS),
                contract_date_is_day_zero=True,
            )

    def test_company_cash_never_enters_patch(self):
        patch = build_proposed_deal_patch(
            demo_financialization(available_company_cash="50000000"),
            contract_date_is_day_zero=True,
        )
        self.assertFalse(hasattr(patch, "available_company_cash"))

    def test_borrowing_rate_never_enters_patch(self):
        patch = build_proposed_deal_patch(
            demo_financialization(company_borrowing_rate="4.8%"),
            contract_date_is_day_zero=True,
        )
        self.assertFalse(hasattr(patch, "company_borrowing_rate"))

    def test_target_margin_never_enters_patch(self):
        patch = build_proposed_deal_patch(
            demo_financialization(target_margin="14%"),
            contract_date_is_day_zero=True,
        )
        self.assertFalse(hasattr(patch, "target_margin"))

    def test_fx_rates_never_enter_patch(self):
        patch = build_proposed_deal_patch(
            demo_financialization(), contract_date_is_day_zero=True
        )
        self.assertFalse(hasattr(patch, "usd_krw"))
        self.assertFalse(hasattr(patch, "jpy_krw_per_100"))

    def test_openai_boundary_sends_all_pdfs_once_without_storage(self):
        client = Mock()
        expected = demo_financialization()
        client.responses.parse.return_value = SimpleNamespace(output_parsed=expected)
        demo_dir = Path(__file__).resolve().parents[1] / "assets" / "demo"

        result = analyze_demo_documents(
            (
                demo_dir / "Sales_Contract.pdf",
                demo_dir / "Supplier_PO_US.pdf",
                demo_dir / "Supplier_PO_JP.pdf",
            ),
            client=client,
        )

        self.assertIs(result, expected)
        client.responses.parse.assert_called_once()
        request = client.responses.parse.call_args.kwargs
        self.assertEqual(request["model"], "gpt-5.6-luna")
        self.assertEqual(request["reasoning"], {"effort": "low"})
        self.assertIs(request["store"], False)
        content = request["input"][0]["content"]
        self.assertEqual(
            [item["filename"] for item in content],
            ["Sales_Contract.pdf", "Supplier_PO_US.pdf", "Supplier_PO_JP.pdf"],
        )
        self.assertTrue(
            all(item["file_data"].startswith("data:application/pdf;base64,") for item in content)
        )


if __name__ == "__main__":
    unittest.main()
