import os
from pathlib import Path
import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest


class WebMvpTests(unittest.TestCase):
    def render_without_credentials(self):
        with (
            patch.dict(
                os.environ,
                {"EXIMBANK_AUTH_KEY": "", "KSURE_SERVICE_KEY": ""},
                clear=False,
            ),
            patch("src.external.eximbank_fx.fetch_fx_reference") as eximbank_fetch,
            patch("src.external.ksure_payment.fetch_payment_context") as ksure_fetch,
        ):
            app_path = Path(__file__).resolve().parents[1] / "app.py"
            app = AppTest.from_file(app_path, default_timeout=10).run()
        self.assertEqual(app.exception, [])
        return app, eximbank_fetch, ksure_fetch

    def test_app_starts_without_api_credentials(self):
        app, _, _ = self.render_without_credentials()
        self.assertEqual(app.title[0].value, "AI Trade Finance Pre-check")

    def test_default_reference_deal_renders_without_exception(self):
        app, _, _ = self.render_without_credentials()
        labels = {metric.label: metric.value for metric in app.metric}
        self.assertEqual(labels["Gross Deal Margin"], "15.00%")
        self.assertEqual(labels["Financing-adjusted Deal Margin"], "14.64%")
        self.assertEqual(labels["Peak Deal Funding Requirement"], "KRW 119.000M")
        self.assertEqual(labels["Maximum External Borrowing"], "KRW 69.000M")

    def test_external_apis_are_not_invoked_on_initial_render(self):
        _, eximbank_fetch, ksure_fetch = self.render_without_credentials()
        eximbank_fetch.assert_not_called()
        ksure_fetch.assert_not_called()

    def test_missing_credentials_do_not_prevent_deterministic_analysis(self):
        app, _, _ = self.render_without_credentials()
        self.assertTrue(any(message.value == "MEETS TARGET" for message in app.success))
        self.assertEqual(len(app.dataframe), 3)


if __name__ == "__main__":
    unittest.main()
