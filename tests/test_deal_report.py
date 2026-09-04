from dataclasses import replace
from datetime import date, datetime, timezone
from decimal import Decimal
import unittest
from unittest.mock import patch
import re

from src.ai.financialization import ExtractedPaymentMethod, ProposedDealPatch
from src.ai.deal_review import DealReviewMemo, SupportingSignal, TreasuryFocus
from src.domain.deal_case import PaymentMethod, reference_deal, reference_fx
from src.external.eximbank_fx import FxReferenceSnapshot
from src.external.ksure_payment import PaymentContext
from src.finance.engine import (
    Scenario,
    canonical_purchase_option,
    canonical_scenarios,
    evaluate_deal,
    evaluate_scenario,
    solve_usd_krw_threshold,
)
from src.finance.company_liquidity import (
    CompanyCashEvent,
    CompanyCashEventCategory,
    CompanyCashEventSource,
    CompanyCashEventStatus,
    CompanyLiquidityInput,
    analyze_company_liquidity,
    compare_company_gap_to_credit_line,
)
from src.finance.fx_treasury import ForwardHedgeInput, analyze_fx_treasury
from src.finance.liquidity import WorkingCapitalCreditLine, analyze_company_funding
from src.finance.usance import BankersUsanceInput, analyze_bankers_usance
from src.domain.deal_case import Currency, FxRates
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


def treasury_report_input(*, include_expected=False, review_is_current=True):
    deal = reference_deal()
    fx = reference_fx()
    base = evaluate_deal(deal, fx)
    purchase = evaluate_deal(deal, fx, purchase_option=canonical_purchase_option())
    line = WorkingCapitalCreditLine(Decimal("100000000"), Decimal("30000000"))
    funding = analyze_company_funding(
        deal=deal, base_result=base,
        combined_result=evaluate_scenario(deal, fx, Scenario.COMBINED),
        credit_line=line, purchase_result=purchase,
    )
    events = (
        CompanyCashEvent(date(2026, 9, 24), CompanyCashEventCategory.AR_COLLECTION, Decimal("40000000"), CompanyCashEventStatus.CONFIRMED, CompanyCashEventSource.MANUAL, "기존 매출채권 A"),
        CompanyCashEvent(date(2026, 10, 4), CompanyCashEventCategory.PAYROLL_TAX, Decimal("-50000000"), CompanyCashEventStatus.CONFIRMED, CompanyCashEventSource.MANUAL, "급여·세금"),
        CompanyCashEvent(date(2026, 10, 19), CompanyCashEventCategory.AR_COLLECTION, Decimal("20000000"), CompanyCashEventStatus.CONFIRMED, CompanyCashEventSource.MANUAL, "기존 매출채권 B"),
        CompanyCashEvent(date(2026, 10, 29), CompanyCashEventCategory.AR_COLLECTION, Decimal("30000000"), CompanyCashEventStatus.EXPECTED, CompanyCashEventSource.MANUAL, "예상 수금 C"),
        CompanyCashEvent(date(2026, 11, 3), CompanyCashEventCategory.CAPEX, Decimal("-30000000"), CompanyCashEventStatus.CONFIRMED, CompanyCashEventSource.MANUAL, "확정 설비대금"),
    )
    timeline = analyze_company_liquidity(
        liquidity_input=CompanyLiquidityInput(date(2026, 9, 4), Decimal("120000000"), Decimal("70000000"), events, include_expected),
        deal=deal, fx=fx,
    )
    capacity = compare_company_gap_to_credit_line(timeline.company_with_deal, line)
    fx_treasury = analyze_fx_treasury(
        deal=deal, current_fx=fx, settlement_fx=FxRates(Decimal("1330"), Decimal("990")),
        hedge_inputs=(
            ForwardHedgeInput(Currency.USD, Decimal("0.8"), Decimal("1395")),
            ForwardHedgeInput(Currency.JPY, Decimal("0.8"), Decimal("905")),
        ),
    )
    usance = analyze_bankers_usance(
        deal=deal, fx=fx, base_result=base, credit_line=line,
        usance_input=BankersUsanceInput(1, 90, Decimal("0.048"), Decimal("0.0015")),
    )
    memo = DealReviewMemo(
        headline="회사 전체 유동성을 먼저 확인합니다",
        summary="거래 단독 자금과 기존 회사 계획을 함께 살펴야 합니다.",
        treasury_focus=TreasuryFocus.CREDIT_LINE_CAPACITY,
        supporting_signals=(SupportingSignal.COMBINED_STRESS,),
        negotiation_focus=(),
    )
    return reference_report_input(
        company_liquidity_timeline=timeline,
        company_liquidity_capacity=capacity,
        treasury_confirmed_current_cash_krw=Decimal("120000000"),
        minimum_operating_cash_krw=Decimal("70000000"),
        company_funding=funding, fx_treasury=fx_treasury,
        bankers_usance=usance,
        company_liquidity_includes_expected=include_expected,
        review_memo=memo,
        review_used_tools=("read_current_deal_analysis", "read_stress_and_rescue", "read_treasury_context", "read_payment_context"),
        review_is_current=review_is_current,
    )


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
            (None, payment_context, "K-SURE 결제 참고정보"),
            (fx_reference, None, "한국수출입은행 환율 참고정보"),
            (
                fx_reference,
                payment_context,
                "한국수출입은행 환율 / K-SURE 결제 참고정보",
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

    def report_text(self, report_input):
        from src.reporting import deal_report
        captured = []
        original = deal_report._p

        def recording_paragraph(text, style):
            captured.append(text)
            return original(text, style)

        with patch("src.reporting.deal_report._p", side_effect=recording_paragraph):
            output = self.assert_pdf(report_input)
        return "\n".join(captured), output

    def test_final_branding_and_company_treasury_sections(self):
        text, output = self.report_text(treasury_report_input())
        self.assertIn("기업 수출거래 Treasury 사전점검 보고서", text)
        self.assertNotIn("AI Trade Finance Pre-check", text)
        self.assertIn("Company-wide liquidity", text)
        report_input = treasury_report_input()
        self.assertEqual(report_input.company_liquidity_timeline.company_with_deal.peak_liquidity_gap_krw, Decimal("89000000"))
        self.assertEqual(report_input.company_liquidity_capacity.liquidity_gap_krw, Decimal("19000000"))
        self.assertEqual(report_input.base_result.funding.maximum_external_borrowing_krw, Decimal("69000000"))
        self.assertIn("2026-11-03 / D+60", text)
        self.assertIn("Banker's Usance", text)
        self.assertIn("FX Treasury", text)
        self.assertIn("회사 전체 유동성을 먼저 확인합니다", text)
        self.assertLessEqual(len(re.findall(rb"/Type\s*/Page\b", output)), 3)

    def test_expected_mode_is_labeled_as_user_scenario(self):
        text, _ = self.report_text(treasury_report_input(include_expected=True))
        self.assertIn("EXPECTED 포함 사용자 선택 시나리오", text)
        self.assertNotIn("예측", next(line for line in text.splitlines() if "EXPECTED" in line))

    def test_stale_review_is_not_included(self):
        text, _ = self.report_text(treasury_report_input(review_is_current=False))
        self.assertIn("현재 조건 기준 거래 검토 요약 없음", text)
        self.assertNotIn("회사 전체 유동성을 먼저 확인합니다", text)

    def test_treasury_report_is_repeatable_and_does_not_mutate_inputs(self):
        report_input = treasury_report_input()
        timeline_before = report_input.company_liquidity_timeline
        first_text, first = self.report_text(report_input)
        second_text, second = self.report_text(report_input)
        self.assertEqual(first_text, second_text)
        self.assertEqual(len(first), len(second))
        self.assertEqual(report_input.company_liquidity_timeline, timeline_before)


if __name__ == "__main__":
    unittest.main()
