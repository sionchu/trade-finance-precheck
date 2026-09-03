import os
from pathlib import Path
import unittest
from unittest.mock import patch

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
    def render_without_credentials(self):
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
        self.assertEqual(app.title[0].value, "AI Trade Finance Pre-check")

    def test_default_reference_deal_renders_without_exception(self):
        app, _, _, _ = self.render_without_credentials()
        labels = {metric.label: metric.value for metric in app.metric}
        self.assertEqual(app.metric[0].label, "금융비용 반영 Deal Margin")
        self.assertEqual(app.metric[0].value, "14.64%")
        self.assertEqual(labels["금융비용 반영 전 Deal Margin"], "15.00%")
        self.assertEqual(labels["Deal 자금소요"], "KRW 119.000M")
        self.assertEqual(labels["최대 외부차입"], "KRW 69.000M")

    def test_report_download_is_available_without_credentials(self):
        app, _, _, _ = self.render_without_credentials()
        self.assertEqual(
            metric_by_label(app, "생성 기준").value,
            "현재 Deal 입력 기반 분석",
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

    def test_missing_credentials_do_not_prevent_deterministic_analysis(self):
        app, _, _, _ = self.render_without_credentials()
        self.assertTrue(any("MEETS TARGET" in message.value for message in app.success))
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
            "AI 분석 결과 존재 · 현재 Deal에는 미반영",
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
            "AI 추출값 반영 후 현재 Deal에서 일부 값 수정",
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
