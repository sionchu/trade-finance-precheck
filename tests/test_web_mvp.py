import os
from pathlib import Path
import unittest
from unittest.mock import patch
from zoneinfo import ZoneInfo

from streamlit.testing.v1 import AppTest

from src.ai.financialization import (
    DocumentFinancialization,
    ExtractedPaymentMethod,
    FinancialEvent,
    HedgeStatus,
    Receivable,
    TimingAnchor,
)


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


def element_by_key(elements, key):
    return next(element for element in elements if element.key == key)


def metric_by_label(app, label):
    return next(metric for metric in app.metric if metric.label == label)


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
        ):
            app_path = Path(__file__).resolve().parents[1] / "app.py"
            app = AppTest.from_file(app_path, default_timeout=10).run()
            for label, value in (input_values or {}).items():
                next(
                    item for item in app.number_input if item.label == label
                ).set_value(value)
            if input_values:
                app.run()
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
        self.assertEqual(app.title[0].value, "수출거래 사전점검")

    def test_default_reference_deal_renders_without_exception(self):
        app, _, _, _ = self.render_without_credentials()
        labels = {metric.label: metric.value for metric in app.metric}
        self.assertEqual(app.metric[0].label, "실제로 남는 마진")
        self.assertEqual(app.metric[0].value, "14.64%")
        self.assertEqual(labels["현재 분석 환율"], "1,400원")
        self.assertEqual(labels["목표마진 유지선"], "1,386.47원")
        self.assertEqual(labels["거래에 가장 많이 필요한 돈"], "1억 1,900만원")
        self.assertEqual(labels["최대로 빌려야 하는 돈"], "6,900만원")

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
            "돈은 언제 가장 많이 필요할까요?",
            "고객 입금일까지 기다릴까, 먼저 현금화할까?",
            "공식 시장 참고정보",
            "분석 근거",
            "결과를 공유해야 하나요?",
        ]
        positions = [headings.index(label) for label in expected_order]
        self.assertEqual(positions, sorted(positions))

    def test_report_download_is_available_without_credentials(self):
        app, _, _, _ = self.render_without_credentials()
        self.assertEqual(
            metric_by_label(app, "생성 기준").value,
            "현재 거래 입력 기반 분석",
        )
        report_button = element_by_key(
            app.get("download_button"), "deal_report_download"
        )
        self.assertEqual(report_button.label, "거래 사전점검 보고서 다운로드")
        self.assertTrue(report_button.proto.url.endswith(".pdf"))

    def test_external_apis_are_not_invoked_on_initial_render(self):
        _, eximbank_fetch, ksure_fetch, openai_extract = self.render_without_credentials()
        eximbank_fetch.assert_not_called()
        ksure_fetch.assert_not_called()
        openai_extract.assert_not_called()

    def test_public_market_surface_is_ksure_only(self):
        app, _, _, _ = self.render_without_credentials()
        button_labels = [item.label for item in app.button]
        self.assertIn("K-SURE 결제정보 불러오기", button_labels)
        self.assertNotIn("공식 기준환율 불러오기", button_labels)
        self.assertNotIn("현재 거래에 적용", button_labels)
        self.assertEqual(len(app.date_input), 0)

    def test_collection_day_updates_receivable_comparison_label(self):
        app, _, _, _ = self.render_without_credentials({"결제일 (D+)": 120})
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
        self.assertEqual(len(app.dataframe), 2)

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
