import os
import json
from dataclasses import replace
from datetime import date
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from zoneinfo import ZoneInfo

from streamlit.testing.v1 import AppTest
from streamlit.testing.v1 import element_tree
from streamlit.proto.WidgetStates_pb2 import WidgetState

from src.ai.deal_review import (
    DealReviewError,
    DealReviewMemo,
    DealReviewRun,
    SupportingSignal,
    TOOL_NAMES,
    TreasuryFocus,
    TreasuryReviewContext,
)
from src.ai.financialization import (
    DocumentFinancialization,
    ExtractedPaymentMethod,
    FinancialEvent,
    HedgeStatus,
    Receivable,
    TimingAnchor,
)
from src.ai.financial_statement import (
    FinancialStatementFinancialization,
    StatementFact,
    build_company_liquidity_profile,
)
from src.domain.deal_case import Currency, FxRates, reference_deal, reference_fx
from src.external.ksure_payment import PaymentContext
from src.finance.engine import Scenario, canonical_purchase_option, canonical_scenarios, evaluate_deal
from src.finance.fx_treasury import ForwardHedgeInput, analyze_fx_treasury
from src.finance.company_liquidity import (
    CompanyCashEvent,
    CompanyCashEventCategory,
    CompanyCashEventSource,
    CompanyCashEventStatus,
    CompanyLiquidityInput,
    analyze_company_liquidity,
    compare_company_gap_to_credit_line,
)
from src.finance.liquidity import WorkingCapitalCreditLine, analyze_company_funding
from src.finance.rescue import RescueLever
from src.finance.usance import BankersUsanceInput, analyze_bankers_usance


def extracted_demo(**overrides):
    values = {
        "receivables": (
            Receivable(
                currency_code="USD",
                amount="100,000",
                timing_days=90,
                timing_anchor=TimingAnchor.SHIPMENT,
                payment_method=ExtractedPaymentMethod.OA,
                description="Sale",
                source_filename="Sales_Contract.pdf",
                evidence="90 days after shipment",
                needs_review=False,
            ),
        ),
        "payables": (
            FinancialEvent(
                currency_code="USD",
                amount="20,000",
                timing_days=30,
                timing_anchor=TimingAnchor.CONTRACT_DATE,
                description="US materials",
                source_filename="Supplier_PO_US.pdf",
                evidence="Net 30 after Purchase Contract Date",
                needs_review=False,
            ),
            FinancialEvent(
                currency_code="JPY",
                amount="3,000,000",
                timing_days=30,
                timing_anchor=TimingAnchor.CONTRACT_DATE,
                description="JP parts",
                source_filename="Supplier_PO_JP.pdf",
                evidence="Net 30 after Purchase Contract Date",
                needs_review=False,
            ),
        ),
        "incoterm": "FOB Busan, Republic of Korea - Incoterms 2020",
        "hedge_status": HedgeStatus.NOT_FOUND,
        "available_company_cash": None,
        "company_borrowing_rate": None,
        "target_margin": None,
        "review_notes": (),
    }
    values.update(overrides)
    return DocumentFinancialization(**values)


def statement_fact(amount):
    return StatementFact(
        amount_krw=amount,
        period_end="2025-12-31",
        source_filename="Company_Financial_Statement.pdf",
        evidence="2025-12-31 current period",
        needs_review=False,
    )


def extracted_statement():
    return FinancialStatementFinancialization(
        cash_and_cash_equivalents=statement_fact("120,000,000"),
        short_term_financial_instruments=statement_fact("30,000,000"),
        accounts_receivable=statement_fact("240,000,000"),
        inventory=statement_fact("180,000,000"),
        current_assets=statement_fact("650,000,000"),
        current_liabilities=statement_fact("470,000,000"),
        short_term_borrowings=statement_fact("160,000,000"),
        finance_cost=statement_fact("12,000,000"),
        operating_cash_flow=statement_fact("85,000,000"),
        review_notes=(),
    )


def element_by_key(elements, key):
    return next(element for element in elements if element.key == key)


def metric_by_label(app, label):
    return next(metric for metric in app.metric if metric.label == label)


def switch_view(app, view):
    app.session_state["trade_treasury_experience"] = {"active_view": view}
    return app.run()

def visible(app):
    return "\n".join(str(x.value) for x in (*app.markdown, *app.caption, *app.info, *app.warning, *app.error, *app.title, *app.subheader))

def current_treasury_context(company_liquidity=None):
    deal = reference_deal()
    fx = reference_fx()
    base = evaluate_deal(deal, fx)
    scenarios = canonical_scenarios(deal, fx)
    line = WorkingCapitalCreditLine(Decimal("100000000"), Decimal("30000000"))
    purchase = evaluate_deal(deal, fx, purchase_option=canonical_purchase_option())
    funding = analyze_company_funding(
        deal=deal,
        base_result=base,
        combined_result=scenarios[Scenario.COMBINED],
        credit_line=line,
        purchase_result=purchase,
    )
    fx_treasury = analyze_fx_treasury(
        deal=deal,
        current_fx=fx,
        settlement_fx=FxRates(Decimal("1330"), Decimal("990")),
        hedge_inputs=(
            ForwardHedgeInput(Currency.USD, Decimal("0.8"), Decimal("1395")),
            ForwardHedgeInput(Currency.JPY, Decimal("0.8"), Decimal("905")),
        ),
    )
    usance = analyze_bankers_usance(
        deal=deal,
        fx=fx,
        base_result=base,
        credit_line=line,
        usance_input=BankersUsanceInput(1, 90, Decimal("0.048"), Decimal("0.0015")),
    )
    events = (
        CompanyCashEvent(date(2026, 9, 24), CompanyCashEventCategory.AR_COLLECTION, Decimal("40000000"), CompanyCashEventStatus.CONFIRMED, CompanyCashEventSource.MANUAL, "기존 매출채권 A"),
        CompanyCashEvent(date(2026, 10, 4), CompanyCashEventCategory.PAYROLL_TAX, Decimal("-50000000"), CompanyCashEventStatus.CONFIRMED, CompanyCashEventSource.MANUAL, "급여·세금"),
        CompanyCashEvent(date(2026, 10, 19), CompanyCashEventCategory.AR_COLLECTION, Decimal("20000000"), CompanyCashEventStatus.CONFIRMED, CompanyCashEventSource.MANUAL, "기존 매출채권 B"),
        CompanyCashEvent(date(2026, 11, 3), CompanyCashEventCategory.CAPEX, Decimal("-30000000"), CompanyCashEventStatus.CONFIRMED, CompanyCashEventSource.MANUAL, "확정 설비대금"),
    )
    timeline = analyze_company_liquidity(
        liquidity_input=CompanyLiquidityInput(date(2026, 9, 4), Decimal("120000000"), Decimal("70000000"), events),
        deal=deal,
        fx=fx,
    )
    capacity = compare_company_gap_to_credit_line(timeline.company_with_deal, line)
    return TreasuryReviewContext(company_liquidity, funding, fx_treasury, usance, timeline, capacity)


def review_result(payment_context=None, treasury_context=None):
    return DealReviewRun(
        question=(
            "이 거래의 수익성, 회사 전체 유동성, 외화노출과 자금조달 구조에서 "
            "우선 확인할 점을 설명해줘."
        ),
        memo=DealReviewMemo(
            headline="복합 상황에서 계약조건 점검이 필요합니다",
            summary="가격과 원가 경계를 함께 읽고 자금 부담의 원인을 확인해야 합니다.",
            treasury_focus=TreasuryFocus.CREDIT_LINE_CAPACITY,
            supporting_signals=(
                SupportingSignal.COMBINED_STRESS,
                SupportingSignal.FX_RESILIENCE,
            ),
            negotiation_focus=(
                RescueLever.SALE_AMOUNT_USD,
                RescueLever.COLLECTION_DAY,
            ),
        ),
        deal=reference_deal(),
        fx=reference_fx(),
        treasury_context=treasury_context or current_treasury_context(),
        payment_context=payment_context,
        used_tools=TOOL_NAMES,
        model="gpt-5.6-luna",
        request_count=2,
        usage=None,
    )


class WebMvpTests(unittest.TestCase):
    def setUp(self):
        # AppTest has no Components v2 Widget implementation. Send its actual
        # persisted state on reruns, as the browser does, instead of dropping it.
        original = element_tree.get_widget_state

        def widget_state(node):
            if getattr(node, "type", None) == "bidi_component":
                return WidgetState(id=node.proto.id, json_value=json.dumps(dict(node.value)))
            return original(node)

        patcher = patch.object(element_tree, "get_widget_state", side_effect=widget_state)
        patcher.start()
        self.addCleanup(patcher.stop)


    def render(self):
        app = AppTest.from_file(Path(__file__).parents[1] / "app.py", default_timeout=30).run()
        self.assertEqual(list(app.exception), [])
        return app

    def render_with_extraction(self, result=None):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}), patch(
            "src.ai.financialization.analyze_demo_documents",
            return_value=result or extracted_demo(),
        ) as extraction:
            app = self.render()
            switch_view(app, "setup")
            element_by_key(app.button, "show_documents_action").click().run()
            element_by_key(app.button, "analyze_demo_documents").click().run()
            self.assertEqual(list(app.exception), [])
        return app, extraction

    def test_default_analysis_has_no_inputs_or_automatic_provider_calls(self):
        with patch("src.ai.deal_review.run_deal_review") as review, patch("src.ai.financialization.analyze_demo_documents") as document, patch("src.ai.financial_statement.analyze_demo_financial_statement") as statement, patch("src.external.ksure_payment.fetch_payment_context") as ksure, patch("src.external.eximbank_fx.fetch_fx_reference") as fx:
            app = self.render()
            self.assertEqual(app.title[0].value, "수출거래 AI 금융진단")
            self.assertEqual(len(app.number_input), 0)
            self.assertEqual(len(app.slider), 0)
            self.assertEqual(len(app.get("bidi_component")), 1)
            self.assertIn("현재 거래는 목표마진", visible(app))
            for provider in (review, document, statement, ksure, fx):
                provider.assert_not_called()

    def test_all_default_views_have_zero_numeric_inputs(self):
        app = self.render()
        for view in ("setup", "report", "analysis"):
            switch_view(app, view)
            self.assertEqual(list(app.exception), [])
            self.assertEqual(len(app.number_input), 0, view)
            self.assertEqual(len(app.slider), 0, view)

    def test_setup_disclosures_are_actions_and_base_is_compact(self):
        app = self.render()
        self.assertIn("기본 조건", visible(app))
        self.assertNotIn("마진 · 기본 → 기본", visible(app))
        switch_view(app, "setup")
        action_keys = {item.key for item in app.button}
        self.assertTrue({
            "edit_deal_action", "show_documents_action",
            "edit_company_action", "edit_cash_plan_action",
        }.issubset(action_keys))
        self.assertEqual(len(app.toggle), 0)

    def test_report_metadata_is_wrapping_content_not_kpis(self):
        app = self.render()
        switch_view(app, "report")
        text = visible(app)
        for label in ("현재 상태", "생성 기준", "공식 데이터"):
            self.assertIn(label, text)
        self.assertEqual(len(app.metric), 0)

    def test_canonical_connected_relationship_and_chart(self):
        app = self.render()
        text = visible(app)
        for value in ("6,900만원", "8,900만원", "7,000만원", "1,900만원", "2026-11-03", "D+60"):
            self.assertIn(value, text)
        self.assertIn("funding-relationship", text)
        self.assertTrue(app.get("vega_lite_chart"))
        self.assertNotIn("Treasury", text)

    def test_presets_select_frozen_results_without_calculate_button(self):
        app = self.render()
        selector = element_by_key(app.radio, "selected_scenario")
        for label, margin in (("USD -5%", "11.20%"), ("복합 악화", "8.83%"), ("기본", "14.64%")):
            selector.set_value(label).run()
            self.assertIn(margin, visible(app))
            self.assertEqual(len(app.number_input), 0)
            self.assertFalse(any("계산" in x.label for x in app.button))

    def test_custom_scenario_has_four_exact_fields_and_no_slider(self):
        app = self.render()
        element_by_key(app.radio, "selected_scenario").set_value("+ 직접 설정").run()
        self.assertEqual(len(app.number_input), 4)
        self.assertEqual(len(app.slider), 0)
        element_by_key(app.number_input, "custom_usd_input").set_value(1330.0)
        element_by_key(app.button, "FormSubmitter:custom_scenario_form-적용").click().run()
        self.assertIn("11.20%", visible(app))

    def test_target_is_opt_in_exact_preference(self):
        app = self.render()
        element_by_key(app.button, "edit_target_action").click().run()
        self.assertEqual(len(app.number_input), 1)
        element_by_key(app.number_input, "target_margin_input").set_value(20.0)
        element_by_key(app.button, "FormSubmitter:target_form-적용").click().run()
        self.assertIn("목표마진", visible(app))
        self.assertEqual(app.session_state["target_margin_input"], 20.0)
        self.assertIn("14.64%", visible(app))

    def test_manual_fact_form_and_persistence(self):
        app = self.render()
        switch_view(app, "setup")
        self.assertIn("거래 정보", visible(app))
        element_by_key(app.button, "edit_deal_action").click().run()
        element_by_key(app.number_input, "sale_amount_input").set_value(110000.0)
        element_by_key(app.button, "FormSubmitter:deal_form-변경사항 적용").click().run()
        switch_view(app, "analysis")
        self.assertEqual(app.session_state["sale_amount_input"], 110000.0)
        self.assertEqual(list(app.exception), [])
        self.assertIn("110,000", visible(app))

    def test_company_form_reuses_credit_line_and_changes_residual(self):
        app = self.render()
        switch_view(app, "setup")
        element_by_key(app.button, "edit_company_action").click().run()
        element_by_key(app.number_input, "credit_total_limit_input").set_value(110000000.0)
        element_by_key(app.button, "FormSubmitter:company_form-변경사항 적용").click().run()
        switch_view(app, "analysis")
        self.assertIn("900만원", visible(app))
        self.assertEqual(app.session_state["credit_used_amount_input"], 30000000.0)

    def test_cash_plan_persists_when_editor_unmounted(self):
        app = self.render()
        switch_view(app, "setup")
        element_by_key(app.button, "edit_cash_plan_action").click().run()
        rows = list(app.session_state["company_cash_plan_rows"])
        self.assertIn("ERP 파일 가져오기", [x.label for x in app.tabs])
        switch_view(app, "analysis")
        self.assertEqual(app.session_state["company_cash_plan_rows"], rows)
        self.assertIn("8,900만원", visible(app))

    def test_invalid_cash_plan_keeps_shell_and_blocks_review(self):
        app = self.render()
        rows = list(app.session_state["company_cash_plan_rows"])
        rows[0] = {**rows[0], "참조": ""}
        app.session_state["company_cash_plan_rows"] = rows
        app.run()
        self.assertEqual(len(app.get("bidi_component")), 1)
        switch_view(app, "report")
        self.assertTrue(element_by_key(app.button, "run_review").disabled)

    def test_response_before_after_delta_and_principal_boundary(self):
        app = self.render()
        text = visible(app)
        self.assertIn("현재", text)
        self.assertIn("대안", text)
        self.assertIn("변화", text)
        self.assertIn("D+65", text)
        self.assertIn("4,200만원", text)
        self.assertIn("총 은행원금", visible(app))
        self.assertIn("줄어드는 것은 아닙니다", visible(app))

    def test_receivable_edit_only_required_fields(self):
        app = self.render()
        element_by_key(app.button, "edit_receivable_action").click().run()
        self.assertEqual(len(app.number_input), 3)
        element_by_key(app.number_input, "receivable_purchase_day_input").set_value(60)
        element_by_key(app.button, "FormSubmitter:receivable_form-적용").click().run()
        self.assertIn("D+60", visible(app))
        self.assertEqual(list(app.exception), [])

    def test_usance_edit_recalculates_existing_comparison(self):
        app = self.render()
        element_by_key(app.button, "edit_usance_action").click().run()
        element_by_key(app.number_input, "usance_repayment_day_input").set_value(100)
        element_by_key(app.button, "FormSubmitter:usance_form-적용").click().run()
        self.assertEqual(list(app.exception), [])
        self.assertNotIn("54.94만원", visible(app))

    def test_report_output_only_and_no_ai_prerequisite(self):
        app = self.render()
        switch_view(app, "report")
        self.assertTrue(app.get("download_button"))
        self.assertIn("14.64%", visible(app))
        self.assertIn("이 조건으로 거래 검토", [x.label for x in app.button])
        self.assertEqual(len(app.number_input), 0)

    def test_agent_success_settles_once_and_preserves_current_run(self):
        app = self.render()
        switch_view(app, "report")
        with patch("src.ai.deal_review.run_deal_review", return_value=review_result()) as review:
            element_by_key(app.button, "run_review").click().run()
            self.assertEqual(list(app.exception), [])
            self.assertEqual(app.session_state["deal_review_run"], review_result())
            self.assertIn(review_result().memo.headline, visible(app))
            self.assertFalse(any("조건이 바뀌었습니다" in x.value for x in app.warning))
            app.run()
        review.assert_called_once()
        context = review.call_args.kwargs["treasury_context"]
        self.assertEqual(context.company_cash_timeline.company_with_deal.peak_liquidity_gap_krw, Decimal("89000000"))
        self.assertIn("요청 횟수: 2", visible(app))

    def test_agent_error_settles_without_retry(self):
        app = self.render()
        switch_view(app, "report")
        with patch("src.ai.deal_review.run_deal_review", side_effect=DealReviewError("안전한 오류")) as review:
            element_by_key(app.button, "run_review").click().run()
            app.run()
        review.assert_called_once()
        self.assertIn("AI 거래 검토를 완료하지 못했습니다.", visible(app))

    def test_changed_base_stales_agent_without_another_call(self):
        app = self.render()
        switch_view(app, "report")
        with patch("src.ai.deal_review.run_deal_review", return_value=review_result()) as review:
            element_by_key(app.button, "run_review").click().run()
            app.session_state["sale_amount_input"] = 110000.0
            app.run()
        review.assert_called_once()
        self.assertTrue(any("조건" in x.value for x in app.warning))
        self.assertNotIn(review_result().memo.headline, visible(app))

    def test_document_extraction_remains_explicit_and_confirmed(self):
        app, extract = self.render_with_extraction()
        extract.assert_called_once()
        self.assertIn("USD 100,000", visible(app))
        self.assertEqual(app.session_state["sale_amount_input"], 100000.0)
        self.assertTrue(element_by_key(app.button, "apply_ai_proposal").disabled)

    def test_unsupported_currency_blocks_apply(self):
        eur = FinancialEvent(
            currency_code="EUR",
            amount="10",
            timing_days=30,
            timing_anchor=TimingAnchor.CONTRACT_DATE,
            description="EUR cost",
            source_filename="Supplier_PO_US.pdf",
            evidence="EUR 10",
            needs_review=False,
        )
        result = extracted_demo(payables=extracted_demo().payables + (eur,))
        app, _ = self.render_with_extraction(result)
        self.assertTrue(any("미지원 통화: EUR" in item.value for item in app.error))
        self.assertFalse(any(item.key == "apply_ai_proposal" for item in app.button))

    def test_hedge_confirmation_is_required(self):
        app, _ = self.render_with_extraction()
        apply_button = element_by_key(app.button, "apply_ai_proposal")
        self.assertTrue(apply_button.disabled)

    def test_ordinary_rerun_reuses_extraction_without_openai_call(self):
        app, _ = self.render_with_extraction()
        with (
            patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}, clear=False),
            patch("src.ai.financialization.analyze_demo_documents") as rerun_extract,
        ):
            app.run()
        rerun_extract.assert_not_called()

    def test_uploaded_role_pdfs_delegate_once_and_are_removed_after_analysis(self):
        captured = []

        def extract(paths):
            captured.extend(paths)
            self.assertEqual([p.name for p in paths], ["Sales_Contract.pdf", "Supplier_PO_US.pdf", "Supplier_PO_JP.pdf"])
            self.assertTrue(all(p.read_bytes() == b"%PDF-1.4 test" for p in paths))
            return extracted_demo()

        with (
            patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}),
            patch("streamlit.file_uploader", return_value=SimpleNamespace(name="my-contract.pdf", getvalue=lambda: b"%PDF-1.4 test")),
            patch("src.ai.financialization.analyze_demo_documents", side_effect=extract) as extraction,
        ):
            app = AppTest.from_file(Path(__file__).parents[1] / "app.py", default_timeout=30).run()
            switch_view(app, "setup")
            element_by_key(app.button, "show_documents_action").click().run()
            element_by_key(app.radio, "document_source").set_value("내 PDF 업로드").run()
            extraction.assert_not_called()
            element_by_key(app.button, "analyze_demo_documents").click().run()
            self.assertEqual(app.exception, [])
            self.assertIn("my-contract.pdf", "\n".join(x.value for x in app.caption))
        extraction.assert_called_once()
        self.assertTrue(captured)
        self.assertTrue(all(not p.exists() for p in captured))

    def test_upload_rejects_non_pdf_without_model_request(self):
        with (
            patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}),
            patch("streamlit.file_uploader", return_value=SimpleNamespace(name="bad.pdf", getvalue=lambda: b"not-pdf")),
            patch("src.ai.financialization.analyze_demo_documents") as extraction,
        ):
            app = AppTest.from_file(Path(__file__).parents[1] / "app.py", default_timeout=30).run()
            switch_view(app, "setup")
            element_by_key(app.button, "show_documents_action").click().run()
            element_by_key(app.radio, "document_source").set_value("내 PDF 업로드").run()
            element_by_key(app.button, "analyze_demo_documents").click().run()
            self.assertTrue(app.warning)
        extraction.assert_not_called()


    def test_confirmed_document_apply_preserves_finance_assumptions(self):
        app, _ = self.render_with_extraction()
        element_by_key(app.checkbox, "ai_hedge_confirmation").check().run()
        element_by_key(app.button, "apply_ai_proposal").click().run()
        self.assertEqual(list(app.exception), [])
        self.assertEqual(app.session_state["input_origin"], "문서 반영")
        self.assertEqual(app.session_state["funding_rate_input"], 4.8)
        self.assertEqual(app.session_state["available_cash_input"], 50000000.0)
        self.assertEqual(app.session_state["ai_applied_patch"], app.session_state["ai_proposed_patch"])

    def test_expected_scenario_is_explicit_and_stales_previous_review(self):
        app = self.render()
        switch_view(app, "report")
        app.session_state["deal_review_run"] = review_result()
        app.session_state["include_expected_company_events"] = True
        app.run()
        self.assertTrue(any("조건이 바뀌었습니다" in x.value for x in app.warning))
        switch_view(app, "analysis")
        self.assertIn("EXPECTED 포함 사용자 선택 시나리오", visible(app))

    def test_statement_context_is_optional_and_does_not_overwrite_allocated_cash(self):
        app = self.render()
        app.session_state["financial_statement_analysis"] = extracted_statement()
        switch_view(app, "report")
        def review_current(*args, **kwargs):
            return review_result(treasury_context=kwargs["treasury_context"])
        with patch("src.ai.deal_review.run_deal_review", side_effect=review_current) as review:
            element_by_key(app.button, "run_review").click().run()
        self.assertEqual(list(app.exception), [])
        self.assertIsNotNone(review.call_args.kwargs["treasury_context"].company_liquidity)
        self.assertEqual(app.session_state["available_cash_input"], 50000000.0)
        self.assertIn("회사 자금 맥락", visible(app))

    def test_viewing_preset_does_not_mutate_base_or_stale_base_review(self):
        app = self.render()
        app.session_state["deal_review_run"] = review_result()
        element_by_key(app.radio, "selected_scenario").set_value("복합 악화").run()
        switch_view(app, "report")
        self.assertIn(review_result().memo.headline, visible(app))
        self.assertFalse(any("조건이 바뀌었습니다" in x.value for x in app.warning))
        self.assertEqual(app.session_state["funding_rate_input"], 4.8)
        self.assertEqual(app.session_state["collection_day_input"], 90)


if __name__ == "__main__":
    unittest.main()
