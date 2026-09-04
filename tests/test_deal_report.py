from dataclasses import replace
from datetime import date, datetime, timezone
from decimal import Decimal
import unittest
from unittest.mock import patch

from src.ai.financialization import ExtractedPaymentMethod, ProposedDealPatch
from src.domain.deal_case import PaymentMethod, reference_deal, reference_fx
from src.external.eximbank_fx import FxReferenceSnapshot
from src.external.ksure_payment import PaymentContext
from src.finance.engine import (
    canonical_purchase_option,
    canonical_scenarios,
    evaluate_deal,
    solve_usd_krw_threshold,
)
from src.reporting.deal_report import (
    AiProvenanceStatus,
    DealReportInput,
    build_deal_report,
    current_ai_provenance,
    official_context_text,
    report_basis_text,
)


def reference_report_input(**overrides) -> DealReportInput:
    deal = overrides.pop("deal", reference_deal())
    fx = overrides.pop("fx", reference_fx())
    base = evaluate_deal(deal, fx)
    purchase = (
        evaluate_deal(deal, fx, purchase_option=canonical_purchase_option())
        if deal.sale.payment_method is PaymentMethod.OA
        else None
    )
    values = {
        "generated_at": datetime(2026, 9, 4, 12, 0, tzinfo=timezone.utc),
        "deal": deal,
        "base_result": base,
        "scenario_results": tuple(canonical_scenarios(deal, fx).items()),
        "zero_profit_threshold": solve_usd_krw_threshold(deal, fx, None),
        "target_margin_threshold": solve_usd_krw_threshold(
            deal, fx, deal.target_margin
        ),
        "purchase_result": purchase,
    }
    values.update(overrides)
    return DealReportInput(**values)


class DealReportTests(unittest.TestCase):
    def assert_pdf(self, report_input: DealReportInput) -> bytes:
        output = build_deal_report(report_input)
        self.assertTrue(output.startswith(b"%PDF"))
        self.assertGreater(len(output), 5_000)
        return output

    def test_canonical_reference_report_generates_pdf_bytes(self):
        self.assert_pdf(reference_report_input())

    def test_report_works_without_ai_or_official_data(self):
        self.assert_pdf(reference_report_input())

    def test_report_works_with_mocked_eximbank_context(self):
        self.assert_pdf(
            reference_report_input(
                fx_reference=FxReferenceSnapshot(
                    reference_date=date(2026, 9, 3),
                    usd_krw=Decimal("1400.00"),
                    jpy_krw_per_100=Decimal("900.00"),
                )
            )
        )

    def test_report_works_with_mocked_ksure_context(self):
        self.assert_pdf(
            reference_report_input(
                payment_context=PaymentContext(
                    country_code="450",
                    industry_major_code="29",
                    last_update_date=date(2026, 1, 31),
                    reference_year=2025,
                    average_payment_period_days=Decimal("47.2"),
                    late_payment_rate_percent=Decimal("18.4"),
                    average_late_payment_period_days=Decimal("13.7"),
                    payment_terms=(),
                    payment_period_distribution=(),
                )
            )
        )

    def test_official_context_provenance_is_source_aware(self):
        fx_reference = FxReferenceSnapshot(
            reference_date=date(2026, 9, 3),
            usd_krw=Decimal("1400.00"),
            jpy_krw_per_100=Decimal("900.00"),
        )
        payment_context = PaymentContext(
            country_code="450",
            industry_major_code="29",
            last_update_date=date(2026, 1, 31),
            reference_year=2025,
            average_payment_period_days=Decimal("47.2"),
            late_payment_rate_percent=Decimal("18.4"),
            average_late_payment_period_days=Decimal("13.7"),
            payment_terms=(),
            payment_period_distribution=(),
        )
        cases = (
            (None, payment_context, "K-SURE 결제 Context"),
            (fx_reference, None, "한국수출입은행 환율 Context"),
            (
                fx_reference,
                payment_context,
                "한국수출입은행 환율 / K-SURE 결제 Context",
            ),
            (None, None, "이 세션에 불러온 공식 데이터 없음"),
        )
        for fx_value, payment_value, expected in cases:
            with self.subTest(expected=expected):
                self.assertEqual(
                    official_context_text(fx_value, payment_value),
                    expected,
                )

    def test_report_does_not_invoke_openai_or_external_apis(self):
        with (
            patch("src.ai.financialization.analyze_demo_documents") as openai_call,
            patch("src.external.eximbank_fx.fetch_fx_reference") as eximbank_call,
            patch("src.external.ksure_payment.fetch_payment_context") as ksure_call,
        ):
            self.assert_pdf(reference_report_input())
        openai_call.assert_not_called()
        eximbank_call.assert_not_called()
        ksure_call.assert_not_called()

    def test_inputs_and_reference_financial_values_are_not_mutated(self):
        report_input = reference_report_input()
        deal_before = report_input.deal
        result_before = report_input.base_result
        expected = (
            Decimal("0.146364774951076320939334638"),
            Decimal("119000000"),
            Decimal("69000000"),
        )
        self.assertEqual(
            (
                result_before.financing_adjusted_deal_margin,
                result_before.funding.peak_deal_funding_krw,
                result_before.funding.maximum_external_borrowing_krw,
            ),
            expected,
        )
        self.assert_pdf(report_input)
        self.assertEqual(report_input.deal, deal_before)
        self.assertEqual(report_input.base_result, result_before)

    def test_current_ai_provenance_compares_only_applied_fields(self):
        deal = reference_deal()
        patch = ProposedDealPatch(
            sale_amount_usd=Decimal("100000"),
            payment_method=ExtractedPaymentMethod.OA,
            usd_payable_amount=Decimal("20000"),
            usd_payable_day=30,
            jpy_payable_amount=Decimal("3000000"),
            jpy_payable_day=30,
        )
        self.assertIs(
            current_ai_provenance(patch, deal),
            AiProvenanceStatus.CURRENT,
        )
        edited = replace(deal, sale=replace(deal.sale, amount=Decimal("150000")))
        self.assertIs(
            current_ai_provenance(patch, edited),
            AiProvenanceStatus.MODIFIED_AFTER_APPLY,
        )
        unrelated_edit = replace(deal, target_margin=Decimal("0.18"))
        self.assertIs(
            current_ai_provenance(patch, unrelated_edit),
            AiProvenanceStatus.CURRENT,
        )

    def test_report_basis_copy_matches_current_provenance(self):
        self.assertEqual(
            report_basis_text(AiProvenanceStatus.NOT_APPLIED, False),
            "현재 Deal 입력 기반 분석",
        )
        self.assertEqual(
            report_basis_text(AiProvenanceStatus.NOT_APPLIED, True),
            "AI 분석 결과 존재 · 현재 Deal에는 미반영",
        )
        self.assertEqual(
            report_basis_text(AiProvenanceStatus.CURRENT, True),
            "거래서류 AI 추출값 일부 반영",
        )
        self.assertEqual(
            report_basis_text(AiProvenanceStatus.MODIFIED_AFTER_APPLY, True),
            "AI 추출값 반영 후 현재 Deal에서 일부 값 수정",
        )

    def test_tt_path_generates_without_receivable_purchase(self):
        deal = reference_deal()
        tt_deal = replace(deal, sale=replace(deal.sale, payment_method=PaymentMethod.TT))
        report_input = reference_report_input(deal=tt_deal)
        self.assertIsNone(report_input.purchase_result)
        self.assert_pdf(report_input)


if __name__ == "__main__":
    unittest.main()
