import os
from dataclasses import replace
from datetime import date
from decimal import Decimal
from pathlib import Path
import unittest
from unittest.mock import patch
from zoneinfo import ZoneInfo

from streamlit.testing.v1 import AppTest

from src.ai.deal_review import (
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


def trigger_component_review(app):
    app.session_state["trade_treasury_experience"] = {
        "active_stage": "result",
        "review_goal": "overall",
        "response_action": "none",
        "primary_action": "run_review",
    }
    return app.run()


def switch_stage(app, stage):
    try:
        state = dict(app.session_state["trade_treasury_experience"])
    except KeyError:
        state = {}
    state.update({"active_stage": stage, "review_goal": state.get("review_goal", "overall"), "response_action": state.get("response_action", "none")})
    state.pop("primary_action", None)
    app.session_state["trade_treasury_experience"] = state
    return app.run()


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
    def render_without_credentials(self, input_values=None):
        with (
            patch.dict(
                os.environ,
                {
                    "EXIMBANK_AUTH_KEY": "",
                    "KSURE_SERVICE_KEY": "",
                    "OPENAI_API_KEY": "",
                },
                clear=False,
            ),
            patch("src.external.eximbank_fx.fetch_fx_reference") as eximbank_fetch,
            patch("src.external.ksure_payment.fetch_payment_context") as ksure_fetch,
            patch("src.ai.financialization.analyze_demo_documents") as openai_extract,
            patch(
                "src.ai.financial_statement.analyze_demo_financial_statement"
            ) as statement_extract,
            patch("src.ai.deal_review.run_deal_review") as deal_review,
        ):
            app_path = Path(__file__).resolve().parents[1] / "app.py"
            app = AppTest.from_file(app_path, default_timeout=10).run()
            for label, value in (input_values or {}).items():
                next(
                    item for item in app.number_input if item.label == label
                ).set_value(value)
            if input_values:
                app.run()
        self.last_deal_review = deal_review
        self.last_statement_extract = statement_extract
        self.assertEqual(app.exception, [])
        return app, eximbank_fetch, ksure_fetch, openai_extract

    def render_with_extraction(self, result=None):
        with (
            patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}, clear=False),
            patch(
                "src.ai.financialization.analyze_demo_documents",
                return_value=extracted_demo() if result is None else result,
            ) as openai_extract,
        ):
            app_path = Path(__file__).resolve().parents[1] / "app.py"
            app = AppTest.from_file(app_path, default_timeout=10).run()
            element_by_key(app.button, "analyze_demo_documents").click()
            app.run()
            self.assertEqual(app.exception, [])
            return app, openai_extract

    def test_app_starts_without_api_credentials(self):
        app, _, _, _ = self.render_without_credentials()
        self.assertEqual(app.title[0].value, "기업 수출거래 Treasury 사전점검")

    def test_react_experience_shell_mounts_without_external_or_ai_calls(self):
        app, _, ksure_fetch, openai_extract = self.render_without_credentials()
        shell = app.get("bidi_component")
        self.assertEqual(len(shell), 1)
        self.assertEqual(shell[0].key, "trade_treasury_experience")
        ksure_fetch.assert_not_called()
        openai_extract.assert_not_called()
        self.last_statement_extract.assert_not_called()
        self.last_deal_review.assert_not_called()

    def test_report_entry_is_result_stage_only(self):
        app, _, _, _ = self.render_without_credentials()
        self.assertFalse(any(item.key == "deal_report_download" for item in app.get("download_button")))

    def test_shell_remains_visible_when_company_cash_plan_is_invalid(self):
        app, _, _, _ = self.render_without_credentials()
        rows = list(app.session_state["company_cash_plan_rows"])
        rows[0] = {**rows[0], "참조": ""}
        app.session_state["company_cash_plan_rows"] = rows
        app.run()
        self.assertEqual(len(app.get("bidi_component")), 1)

    def test_default_reference_deal_renders_without_exception(self):
        app, _, _, _ = self.render_without_credentials()
        labels = {metric.label: metric.value for metric in app.metric}
        self.assertEqual(app.metric[0].label, "실제로 남는 마진")
        self.assertEqual(app.metric[0].value, "14.64%")
        self.assertEqual(labels["현재 분석 환율"], "1,400원")
        self.assertEqual(labels["목표마진 유지선"], "1,386.47원")
        self.assertNotIn("거래 최대 자금소요", labels)

    def test_canonical_usd_stress_is_below_fourteen_percent_target(self):
        app, _, _, _ = self.render_without_credentials()
        message = next(
            item.value for item in app.error if "달러 -5% Stress" in item.value
        )
        self.assertIn("마진 11.20% · 목표 미달", message)

    def test_usd_stress_meets_ten_percent_target(self):
        app, _, _, _ = self.render_without_credentials({"목표 마진 (%)": 10.0})
        message = next(
            item.value for item in app.success if "달러 -5% Stress" in item.value
        )
        self.assertIn("마진 11.20% · ✓ 목표 충족", message)

    def test_below_threshold_fx_is_not_described_as_available_buffer(self):
        app, _, _, _ = self.render_without_credentials({"USD/KRW": 1300.0})
        visible = "\n".join(item.value for item in app.markdown)
        self.assertIn("목표마진 유지선보다", visible)
        self.assertNotIn("현재 여유 -", visible)

    def test_decision_first_information_hierarchy(self):
        app, _, _, _ = self.render_without_credentials()
        headings = [item.value for item in app.subheader]
        expected_order = [
            "이 거래, 현재 조건에서 버틸까요?",
            "거래서류로 자동 입력하기",
            "조건이 나빠지면 어떻게 될까요?",
            "이 거래를 목표 수준으로 만들려면?",
        ]
        positions = [headings.index(label) for label in expected_order]
        self.assertEqual(positions, sorted(positions))

    def test_company_cash_plan_timeline_is_visible_and_confirmed_only(self):
        app, _, _, _ = self.render_without_credentials()
        switch_stage(app, "liquidity")
        headings = [item.value for item in app.subheader]
        self.assertIn("회사의 실제 자금 흐름을 확인합니다", headings)
        self.assertEqual([item.label for item in app.tabs], ["직접 입력", "ERP 파일 가져오기"])
        self.assertFalse(
            next(
                item
                for item in app.checkbox
                if item.label == "EXPECTED 자금계획 포함 시나리오 보기"
            ).value
        )
        metrics = {item.label: item.value for item in app.metric}
        self.assertEqual(metrics["현재 가용현금"], "1억 2,000만원")
        self.assertEqual(metrics["최소 운영자금"], "7,000만원")
        self.assertEqual(metrics["현재 Buffer 초과 유동성"], "+5,000만원")
        self.assertEqual(metrics["거래만 본 필요 은행자금"], "6,900만원")
        self.assertEqual(
            metrics["회사 기존 자금계획까지 포함한 필요 은행자금"],
            "8,900만원",
        )
        self.assertEqual(metrics["현재 미사용 운전자금 한도"], "7,000만원")
        visible = "\n".join(
            item.value
            for item in (*app.markdown, *app.caption, *app.info, *app.error)
        )
        for text in (
            "가상·데모·fictional 자금계획",
            "실시간 ERP 연결이 아닙니다",
            "기본 결과는 CONFIRMED만 포함합니다",
            "현재 입력 한도 초과 · 한도 부족 1,900만원",
            "2026-11-03 (D+60)",
            "Deal-level 배정자금과 Company-wide 현금 포지션",
        ):
            self.assertIn(text, visible)

    def test_canonical_rescue_boundaries_are_visible(self):
        app, _, _, _ = self.render_without_credentials()
        visible = "\n".join(
            item.value
            for item in (*app.markdown, *app.metric, *app.caption, *app.error)
        )
        self.assertIn(
            "이 거래를 목표 수준으로 만들려면?",
            [item.value for item in app.subheader],
        )
        self.assertIn("8.83%", visible)
        self.assertIn("최소 USD 106,017", visible)
        self.assertIn("최대 USD 14,898", visible)
        self.assertIn("최대 JPY 2,314,602", visible)
        self.assertIn("결제기간 단축만으로는", visible)
        self.assertIn("조달금리 인하만으로는", visible)

    def test_lower_target_hides_rescue_cards(self):
        app, _, _, _ = self.render_without_credentials({"목표 마진 (%)": 8.0})
        visible = "\n".join(
            item.value for item in (*app.markdown, *app.metric, *app.success)
        )
        self.assertIn("추가 목표마진 충족 조건 계산이 필요하지 않습니다", visible)
        self.assertNotIn("최소 USD 106,017", visible)

    def test_report_download_is_available_without_credentials(self):
        app, _, _, _ = self.render_without_credentials()
        app.session_state["trade_treasury_experience"] = {
            "active_stage": "result",
            "review_goal": "overall",
            "response_action": "none",
        }
        app.run()
        self.assertEqual(
            metric_by_label(app, "생성 기준").value,
            "현재 거래 입력 기반 분석",
        )
        report_button = element_by_key(
            app.get("download_button"), "deal_report_download"
        )
        self.assertEqual(report_button.label, "Treasury 사전점검 보고서 다운로드")
        self.assertTrue(report_button.proto.url.endswith(".pdf"))

    def test_external_apis_are_not_invoked_on_initial_render(self):
        _, eximbank_fetch, ksure_fetch, openai_extract = self.render_without_credentials()
        eximbank_fetch.assert_not_called()
        ksure_fetch.assert_not_called()
        openai_extract.assert_not_called()
        self.last_statement_extract.assert_not_called()
        self.last_deal_review.assert_not_called()

    def test_financial_statement_section_is_bounded_and_explicit(self):
        app, _, _, _ = self.render_without_credentials()
        switch_stage(app, "liquidity")
        self.assertIn("회사 자금상태", [item.value for item in app.subheader])
        self.assertIn("샘플 재무제표 읽기", [item.label for item in app.button])
        visible = "\n".join(item.value for item in (*app.markdown, *app.caption))
        self.assertIn("가상 재무제표 · 실제 기업 자료 아님", visible)
        self.last_statement_extract.assert_not_called()

    def test_company_funding_capacity_and_choices_are_visible(self):
        app, _, _, _ = self.render_without_credentials()
        switch_stage(app, "liquidity")
        labels = {item.label: item.value for item in app.metric}
        self.assertEqual(labels["미사용 한도"], "7,000만원")
        switch_stage(app, "treasury")
        headings = [item.value for item in app.subheader]
        self.assertNotIn("회사 자금으로 대금 회수일까지 버틸 수 있을까요?", headings)
        self.assertIn("부족한 돈은 어떻게 메울까요?", headings)
        number_labels = [item.label for item in app.number_input]
        self.assertIn("운전자금 한도 총액", number_labels)
        self.assertIn("현재 사용액", number_labels)
        self.assertEqual(number_labels.count("실제 연 조달금리 (%)"), 1)
        visible = "\n".join(
            item.value
            for item in (*app.markdown, *app.success, *app.error, *app.info, *app.caption)
        )
        self.assertIn("현재 입력 기준 한도 내 · 한도 여유 100만원", visible)
        self.assertIn("현재 입력 한도 초과 · 한도 부족 30만원", visible)
        self.assertIn("회사자금만으로 기다리기", visible)
        self.assertIn("D+90에 입금받기 · 기존 운전자금 한도", visible)
        self.assertIn("매출채권 먼저 현금화하기", visible)
        self.assertIn("**최대 은행 필요액**  6,900만원", visible)
        self.assertIn("최대 자금부족이 D+60", visible)
        self.assertIn("매출채권 현금화는 D+65", visible)
        self.assertIn("기존 Deal Margin 엔진에는 자동 반영하지 않습니다", visible)

    def test_sixty_million_unused_line_blocks_wait_and_purchase(self):
        app, _, _, _ = self.render_without_credentials(
            {"운전자금 한도 총액": 90000000.0, "현재 사용액": 30000000.0}
        )
        switch_stage(app, "treasury")
        visible = "\n".join(item.value for item in (*app.markdown, *app.error))
        self.assertGreaterEqual(visible.count("**부족**  900만원"), 2)

    def test_bankers_usance_comparison_is_visible_and_bounded(self):
        app, _, _, _ = self.render_without_credentials()
        switch_stage(app, "treasury")
        headings = [item.value for item in app.subheader]
        self.assertIn("수입대금 지급을 은행 신용으로 늦춰보면?", headings)
        payable_input = next(
            item for item in app.selectbox if item.label == "대상 외화 지급"
        )
        self.assertIn("JPY 3,000,000 · 공급자 지급 D+30", payable_input.options)
        values = {item.label: item.value for item in app.number_input}
        self.assertEqual(values["회사 상환일 (D+)"], 90)
        self.assertEqual(values["Usance 연 금리 (%)"], 4.8)
        self.assertEqual(values["Usance 수수료율 (%)"], 0.15)
        visible = "\n".join(
            item.value
            for item in (
                *app.markdown,
                *app.caption,
                *app.info,
                *app.metric,
            )
        )
        for text in (
            "Banker's Usance 시뮬레이션 · 승인/실행 아님",
            "**일반 운전자금 피크**  6,900만원",
            "**일반 운전자금 피크**  4,200만원",
            "**일반 운전자금 한도 여유**  100만원",
            "**일반 운전자금 한도 여유**  2,800만원",
            "**Usance 원금**  2,700만원",
            "**Usance 이자**  약 21.3만원",
            "**Usance 수수료**  4.05만원",
            "**총 금융비용**  약 54.94만원",
            "일반 운전자금 한도 사용은 줄지만",
            "Usance 자체 승인·한도는 본 시뮬레이션에서 판단하지 않습니다",
            "환위험이 자동으로 없어지는 것은 아닙니다",
        ):
            self.assertIn(text, visible)
        self.assertGreaterEqual(visible.count("6,900만원"), 3)
        self.assertIn("2,700만원", [item.value for item in app.metric])
        self.assertIn("4.05만원", visible)
        self.last_statement_extract.assert_not_called()
        self.last_deal_review.assert_not_called()

    def test_fx_treasury_positions_and_hedge_overlay_are_visible(self):
        app, _, _, _ = self.render_without_credentials()
        switch_stage(app, "treasury")
        headings = [item.value for item in app.subheader]
        self.assertIn("외화는 어느 방향으로 위험할까요?", headings)
        self.assertIn("환율을 열어둘까, 일부 고정할까?", headings)
        input_labels = [item.label for item in app.number_input]
        for label in (
            "USD 선물환 매도환율",
            "USD 헤지비율 (%)",
            "JPY 선물환 매수환율 (100 JPY)",
            "JPY 헤지비율 (%)",
            "정산 시 가정 USD/KRW",
            "정산 시 가정 JPY/KRW (100 JPY)",
        ):
            self.assertIn(label, input_labels)
        visible = "\n".join(
            item.value
            for item in (
                *app.markdown,
                *app.caption,
                *app.warning,
                *app.success,
                *app.error,
            )
        )
        self.assertIn("**통화 기준 상계 가능액**  USD 20,000", visible)
        self.assertIn("**순수취 노출**  USD 80,000", visible)
        self.assertIn("**순지급 노출**  JPY 3,000,000", visible)
        self.assertIn("USD 지급 D+30 · 수취 D+90", visible)
        self.assertIn("**고정한 금액**  USD 64,000", visible)
        self.assertIn("**남은 노출**  USD 16,000", visible)
        self.assertIn("**고정한 금액**  JPY 2,400,000", visible)
        self.assertIn("**남은 노출**  JPY 600,000", visible)
        self.assertIn("**선물환 정산효과**  -44만원", visible)
        self.assertIn("**선물환 정산효과**  +620만원", visible)
        self.assertIn("**헤지 전 마진**  9.16%", visible)
        self.assertIn("**선물환 overlay 마진**  13.82%", visible)
        self.assertIn("현재 입력 기준 · 목표 미달", visible)
        self.assertIn("파생상품 정산에 따른 차입일정 재계산은 포함하지 않습니다", visible)
        self.last_statement_extract.assert_not_called()
        self.last_deal_review.assert_not_called()

    def test_explicit_statement_cta_renders_normalized_profile_without_changing_deal_cash(self):
        with (
            patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}, clear=False),
            patch(
                "src.ai.financial_statement.analyze_demo_financial_statement",
                return_value=extracted_statement(),
            ) as statement_extract,
            patch("src.ai.financialization.analyze_demo_documents"),
            patch("src.ai.deal_review.run_deal_review"),
            patch("src.external.ksure_payment.fetch_payment_context"),
        ):
            app_path = Path(__file__).resolve().parents[1] / "app.py"
            app = AppTest.from_file(app_path, default_timeout=10).run()
            switch_stage(app, "liquidity")
            element_by_key(app.button, "analyze_financial_statement").click()
            app.run()
            switch_stage(app, "liquidity")
        self.assertEqual(app.exception, [])
        statement_extract.assert_called_once()
        labels = {metric.label: metric.value for metric in app.metric}
        self.assertEqual(labels["현금 및 현금성자산"], "1억 2,000만원")
        self.assertEqual(labels["단기금융상품"], "3,000만원")
        self.assertEqual(labels["유동자산"], "6억 5,000만원")
        self.assertEqual(labels["유동부채"], "4억 7,000만원")
        self.assertEqual(labels["단기차입금"], "1억 6,000만원")
        self.assertEqual(labels["영업활동현금흐름"], "8,500만원")
        self.assertEqual(labels["현재 거래 입력상 회사 투입가능자금"], "5,000만원")
        visible = "\n".join(
            item.value for item in (*app.markdown, *app.info, *app.caption)
        )
        self.assertIn("재무제표상 현금 ≠ 이 거래에 투입 가능한 자금", visible)
        self.assertNotIn("이익잉여금", visible)
        self.assertEqual(
            next(
                item
                for item in app.number_input
                if item.label == "이번 거래에 투입 가능한 회사자금 (KRW)"
            ).value,
            50000000.0,
        )

    def test_agent_is_visible_and_normal_rerun_does_not_call_it(self):
        app, _, _, _ = self.render_without_credentials()
        self.assertIn("trade_treasury_experience", app.session_state)
        self.assertFalse(any(button.key == "run_deal_review" for button in app.button))
        with patch("src.ai.deal_review.run_deal_review") as review:
            app.run()
        review.assert_not_called()

    def test_invalid_required_treasury_input_blocks_agent_before_openai(self):
        app, _, _, _ = self.render_without_credentials(
            {
                "운전자금 한도 총액": 20000000.0,
                "현재 사용액": 30000000.0,
            }
        )
        self.last_deal_review.assert_not_called()
        self.assertFalse(any(button.key == "run_deal_review" for button in app.button))

    def test_explicit_agent_cta_renders_current_deterministic_evidence_and_trace(self):
        with (
            patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}, clear=False),
            patch("src.ai.deal_review.run_deal_review", return_value=review_result()) as review,
            patch("src.external.ksure_payment.fetch_payment_context"),
            patch("src.ai.financialization.analyze_demo_documents"),
        ):
            app_path = Path(__file__).resolve().parents[1] / "app.py"
            app = AppTest.from_file(app_path, default_timeout=10).run()
            trigger_component_review(app)
        self.assertEqual(app.exception, [])
        review.assert_called_once()
        visible = "\n".join(
            item.value
            for item in (*app.markdown, *app.info, *app.warning)
        )
        self.assertIn("복합 상황에서 계약조건 점검이 필요합니다", visible)
        self.assertIn("먼저 확인할 Treasury 이슈", visible)
        self.assertIn("함께 본 근거", visible)
        self.assertIn("마진 8.83% · 목표 미달", visible)
        self.assertIn("회사 전체 유동성과 운전자금 한도", visible)
        self.assertEqual(visible.count("회사 전체 유동성과 운전자금 한도"), 1)
        self.assertIn("현재 1,400.00원", visible)
        self.assertIn("현재 거래 분석", visible)
        self.assertIn("Stress / 목표마진 충족 조건", visible)
        self.assertIn("회사 자금 / 자금조달 / 외화위험", visible)
        self.assertIn("K-SURE 결제 참고정보 · 불러온 공식 데이터 없음", visible)

    def test_changed_deal_marks_agent_result_stale_without_another_call(self):
        with (
            patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}, clear=False),
            patch("src.ai.deal_review.run_deal_review", return_value=review_result()) as review,
            patch("src.external.ksure_payment.fetch_payment_context"),
            patch("src.ai.financialization.analyze_demo_documents"),
        ):
            app_path = Path(__file__).resolve().parents[1] / "app.py"
            app = AppTest.from_file(app_path, default_timeout=10).run()
            trigger_component_review(app)
            next(item for item in app.number_input if item.label == "목표 마진 (%)").set_value(13.0)
            app.run()
        review.assert_called_once()
        visible = "\n".join(item.value for item in (*app.markdown, *app.warning))
        self.assertIn("기존 AI 검토는 현재 상태와 일치하지 않습니다", visible)
        self.assertNotIn("복합 상황에서 계약조건 점검이 필요합니다", visible)

    def test_restoring_inputs_does_not_repeat_agent_call(self):
        with (
            patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}, clear=False),
            patch("src.ai.deal_review.run_deal_review", return_value=review_result()) as review,
            patch("src.external.ksure_payment.fetch_payment_context"),
            patch("src.ai.financialization.analyze_demo_documents"),
        ):
            app_path = Path(__file__).resolve().parents[1] / "app.py"
            app = AppTest.from_file(app_path, default_timeout=10).run()
            trigger_component_review(app)
            target = next(
                item for item in app.number_input if item.label == "목표 마진 (%)"
            )
            target.set_value(13.0)
            app.run()
            target = next(
                item for item in app.number_input if item.label == "목표 마진 (%)"
            )
            target.set_value(14.0)
            app.run()
        review.assert_called_once()
        visible = "\n".join(item.value for item in (*app.markdown, *app.warning))
        self.assertNotIn("기존 AI 검토는 현재 상태와 일치하지 않습니다", visible)

    def test_each_treasury_input_stales_and_exact_restore_recovers_without_ai_call(self):
        with (
            patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}, clear=False),
            patch("src.ai.deal_review.run_deal_review", return_value=review_result()) as review,
            patch("src.external.ksure_payment.fetch_payment_context"),
            patch("src.ai.financialization.analyze_demo_documents"),
        ):
            app_path = Path(__file__).resolve().parents[1] / "app.py"
            app = AppTest.from_file(app_path, default_timeout=10).run()
            trigger_component_review(app)
            changes = (
                ("credit_total_limit_input", 101000000.0, 100000000.0),
                ("receivable_purchase_day_input", 66, 65),
                ("usd_hedge_ratio_input", 75.0, 80.0),
                ("settlement_usd_krw_input", 1329.0, 1330.0),
                ("usance_repayment_day_input", 91, 90),
            )
            for key, changed, original in changes:
                widget = element_by_key(app.number_input, key)
                widget.set_value(changed)
                app.run()
                stale = "\n".join(
                    item.value for item in (*app.markdown, *app.warning)
                )
                self.assertIn(
                    "기존 AI 검토는 현재 상태와 일치하지 않습니다", stale
                )

                widget = element_by_key(app.number_input, key)
                widget.set_value(original)
                app.run()
                current = "\n".join(
                    item.value for item in (*app.markdown, *app.warning)
                )
                self.assertNotIn(
                    "기존 AI 검토는 현재 상태와 일치하지 않습니다", current
                )

        review.assert_called_once()

    def test_company_liquidity_signal_renders_only_from_loaded_statement_profile(self):
        profile = build_company_liquidity_profile(extracted_statement())
        loaded_run = review_result(
            treasury_context=current_treasury_context(profile)
        )
        loaded_run = replace(
            loaded_run,
            memo=DealReviewMemo(
                headline="회사 자금 맥락을 함께 확인합니다",
                summary="재무제표상 현금과 거래 배정자금의 차이를 구분해 봐야 합니다.",
                treasury_focus=TreasuryFocus.CREDIT_LINE_CAPACITY,
                supporting_signals=(SupportingSignal.COMBINED_STRESS,),
                negotiation_focus=(),
            ),
        )
        with (
            patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}, clear=False),
            patch(
                "src.ai.financial_statement.analyze_demo_financial_statement",
                return_value=extracted_statement(),
            ) as statement_ai,
            patch("src.ai.deal_review.run_deal_review", return_value=loaded_run) as review,
            patch("src.external.ksure_payment.fetch_payment_context"),
            patch("src.ai.financialization.analyze_demo_documents"),
        ):
            app_path = Path(__file__).resolve().parents[1] / "app.py"
            app = AppTest.from_file(app_path, default_timeout=10).run()
            switch_stage(app, "liquidity")
            element_by_key(app.button, "analyze_financial_statement").click()
            app.run()
            trigger_component_review(app)

        statement_ai.assert_called_once()
        review.assert_called_once()
        visible = "\n".join(
            item.value for item in (*app.markdown, *app.info, *app.caption)
        )
        self.assertIn("재무제표상 현금 및 현금성자산", visible)
        self.assertIn("재무제표상 현금은 Deal 투입가능자금과 동일하지 않습니다", visible)

    def test_loaded_ksure_context_renders_automatically_after_agent_result(self):
        context = PaymentContext(
            country_code="450",
            industry_major_code="29",
            last_update_date=date(2026, 8, 1),
            reference_year=2025,
            average_payment_period_days=Decimal("62.4"),
            late_payment_rate_percent=Decimal("8.1"),
            average_late_payment_period_days=Decimal("13.7"),
            payment_terms=(),
            payment_period_distribution=(),
        )
        loaded_run = review_result(payment_context=context)
        with (
            patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}, clear=False),
            patch("src.ai.deal_review.run_deal_review", return_value=loaded_run) as review,
            patch("src.external.ksure_payment.fetch_payment_context") as fetch,
            patch("src.ai.financialization.analyze_demo_documents"),
        ):
            app_path = Path(__file__).resolve().parents[1] / "app.py"
            app = AppTest.from_file(app_path, default_timeout=10).run()
            app.session_state["ksure_payment_context"] = context
            switch_stage(app, "review")
            trigger_component_review(app)

        review.assert_called_once()
        fetch.assert_not_called()
        visible = "\n".join(
            item.value for item in (*app.markdown, *app.info, *app.warning)
        )
        self.assertIn("공식 결제 참고정보", visible)
        self.assertIn("평균 결제기간 62.4일", visible)
        self.assertIn("개별 바이어 예측 아님", visible)

    def test_loaded_ksure_context_is_available_without_agent_or_ksure_fetch(self):
        context = PaymentContext(
            country_code="450",
            industry_major_code="29",
            last_update_date=date(2026, 8, 1),
            reference_year=2025,
            average_payment_period_days=Decimal("62.4"),
            late_payment_rate_percent=Decimal("8.1"),
            average_late_payment_period_days=Decimal("13.7"),
            payment_terms=(),
            payment_period_distribution=(),
        )
        with (
            patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}, clear=False),
            patch("src.ai.deal_review.run_deal_review") as review,
            patch("src.external.ksure_payment.fetch_payment_context") as fetch,
            patch("src.ai.financialization.analyze_demo_documents"),
        ):
            app_path = Path(__file__).resolve().parents[1] / "app.py"
            app = AppTest.from_file(app_path, default_timeout=10).run()
            app.session_state["ksure_payment_context"] = context
            app.run()
        review.assert_not_called()
        fetch.assert_not_called()
        self.assertEqual(app.session_state["ksure_payment_context"], context)

    def test_public_market_surface_is_ksure_only(self):
        app, _, _, _ = self.render_without_credentials()
        switch_stage(app, "review")
        button_labels = [item.label for item in app.button]
        self.assertIn("K-SURE 결제정보 불러오기", button_labels)
        self.assertNotIn("공식 기준환율 불러오기", button_labels)
        self.assertNotIn("현재 거래에 적용", button_labels)
        self.assertEqual(
            [item.label for item in app.date_input],
            ["거래 검토 기준일"],
        )

    def test_collection_day_updates_receivable_comparison_label(self):
        app, _, _, _ = self.render_without_credentials({"결제일 (D+)": 120})
        switch_stage(app, "treasury")
        visible = "\n".join(item.value for item in app.markdown)
        self.assertIn("D+120에 입금받기", visible)
        self.assertNotIn("90일 뒤 입금받기", visible)

    def test_report_generated_at_uses_seoul_timezone(self):
        with (
            patch.dict(
                os.environ,
                {"KSURE_SERVICE_KEY": "", "OPENAI_API_KEY": ""},
                clear=False,
            ),
            patch(
                "src.reporting.deal_report.build_deal_report",
                return_value=b"%PDF-1.4",
            ) as build_report,
            patch("src.external.ksure_payment.fetch_payment_context"),
            patch("src.ai.financialization.analyze_demo_documents"),
        ):
            app_path = Path(__file__).resolve().parents[1] / "app.py"
            app = AppTest.from_file(app_path, default_timeout=10).run()
        self.assertEqual(app.exception, [])
        generated_at = build_report.call_args.args[0].generated_at
        self.assertEqual(generated_at.tzinfo, ZoneInfo("Asia/Seoul"))

    def test_missing_credentials_do_not_prevent_deterministic_analysis(self):
        app, _, _, _ = self.render_without_credentials()
        self.assertTrue(any("목표 충족" in message.value for message in app.success))
        self.assertEqual(len(app.dataframe), 1)

    def test_ai_section_safely_reports_missing_key(self):
        app, _, _, _ = self.render_without_credentials()
        self.assertTrue(
            any("OPENAI_API_KEY" in message.value for message in app.info)
        )

    def test_mocked_extraction_displays_money_flow_and_exposure(self):
        app, openai_extract = self.render_with_extraction()
        visible = "\n".join(item.value for item in (*app.markdown, *app.caption))
        self.assertIn("USD 100,000", visible)
        self.assertIn("USD 20,000", visible)
        self.assertIn("JPY 3,000,000", visible)
        self.assertIn("순노출 +80,000", visible)
        self.assertIn("순노출 -3,000,000", visible)
        self.assertEqual(
            metric_by_label(app, "생성 기준").value,
            "AI 분석 결과 존재 · 현재 거래에는 미반영",
        )
        openai_extract.assert_called_once()

    def test_proposal_does_not_change_deal_before_apply(self):
        with (
            patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}, clear=False),
            patch(
                "src.ai.financialization.analyze_demo_documents",
                return_value=extracted_demo(),
            ),
        ):
            app_path = Path(__file__).resolve().parents[1] / "app.py"
            app = AppTest.from_file(app_path, default_timeout=10).run()
            sale_input = element_by_key(app.number_input, "sale_amount_input")
            sale_input.set_value(90000.0)
            app.run()
            element_by_key(app.button, "analyze_demo_documents").click()
            app.run()
            self.assertEqual(
                element_by_key(app.number_input, "sale_amount_input").value,
                90000.0,
            )

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

    def test_confirmed_proposal_updates_only_safe_inputs(self):
        with (
            patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}, clear=False),
            patch(
                "src.ai.financialization.analyze_demo_documents",
                return_value=extracted_demo(),
            ) as openai_extract,
        ):
            app_path = Path(__file__).resolve().parents[1] / "app.py"
            app = AppTest.from_file(app_path, default_timeout=10).run()
            element_by_key(app.number_input, "sale_amount_input").set_value(90000.0)
            app.run()
            element_by_key(app.button, "analyze_demo_documents").click()
            app.run()
            element_by_key(app.checkbox, "ai_hedge_confirmation").check()
            app.run()
            element_by_key(app.button, "apply_ai_proposal").click()
            app.run()

        self.assertEqual(
            element_by_key(app.number_input, "sale_amount_input").value,
            100000.0,
        )
        self.assertEqual(
            element_by_key(app.number_input, "collection_day_input").value,
            90,
        )
        self.assertEqual(
            element_by_key(app.number_input, "usd_payable_day_input").value,
            30,
        )
        self.assertEqual(
            app.session_state["ai_applied_patch"],
            app.session_state["ai_proposed_patch"],
        )
        self.assertEqual(
            metric_by_label(app, "생성 기준").value,
            "거래서류 AI 추출값 일부 반영",
        )
        openai_extract.assert_called_once()

    def test_edit_after_ai_apply_updates_current_provenance_without_openai(self):
        with (
            patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}, clear=False),
            patch(
                "src.ai.financialization.analyze_demo_documents",
                return_value=extracted_demo(),
            ) as openai_extract,
        ):
            app_path = Path(__file__).resolve().parents[1] / "app.py"
            app = AppTest.from_file(app_path, default_timeout=10).run()
            element_by_key(app.button, "analyze_demo_documents").click()
            app.run()
            element_by_key(app.checkbox, "ai_hedge_confirmation").check()
            app.run()
            element_by_key(app.button, "apply_ai_proposal").click()
            app.run()
            applied_snapshot = app.session_state["ai_applied_patch"]
            element_by_key(app.number_input, "sale_amount_input").set_value(150000.0)
            app.run()

        self.assertEqual(app.session_state["ai_applied_patch"], applied_snapshot)
        self.assertEqual(
            metric_by_label(app, "생성 기준").value,
            "AI 추출값 반영 후 현재 거래에서 일부 값 수정",
        )
        openai_extract.assert_called_once()

    def test_ordinary_rerun_reuses_extraction_without_openai_call(self):
        app, _ = self.render_with_extraction()
        with (
            patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}, clear=False),
            patch("src.ai.financialization.analyze_demo_documents") as rerun_extract,
        ):
            app.run()
        rerun_extract.assert_not_called()


if __name__ == "__main__":
    unittest.main()
