from decimal import Decimal
from pathlib import Path
import unittest
from unittest.mock import patch
from components.trade_treasury_experience import (
    HELP_TOPICS, VIEW_GUIDE, VIEWS, _JS, _component_html,
    get_experience_state, company_cash_events_from_rows, company_cash_rows,
    trade_treasury_experience,
)
from src.finance.company_liquidity import CompanyCashEventSource, parse_company_cash_events_csv

ROOT = Path(__file__).parents[1]
FRONTEND = ROOT / "components" / "trade_treasury_experience" / "frontend"

class ExperienceShellTests(unittest.TestCase):
    def test_three_exact_views_and_default_analysis(self):
        self.assertEqual([view["id"] for view in VIEWS], ["setup", "analysis", "report"])
        self.assertEqual([view["label"] for view in VIEWS], ["입력", "분석", "보고서"])
        with patch("components.trade_treasury_experience.st.session_state", {}):
            self.assertEqual(get_experience_state(), {"active_view": "analysis"})
        for view in ("setup", "analysis", "report"):
            with patch("components.trade_treasury_experience.st.session_state", {"trade_treasury_experience": {"active_view": view}}):
                self.assertEqual(get_experience_state()["active_view"], view)
        with patch("components.trade_treasury_experience.st.session_state", {"trade_treasury_experience": {"active_view": "invalid"}}):
            self.assertEqual(get_experience_state()["active_view"], "analysis")

    def test_help_is_collapsed_single_source(self):
        markup = _component_html()
        self.assertIn('<details class="help-center">', markup)
        self.assertEqual(len(VIEW_GUIDE), 3)
        self.assertGreaterEqual(len(HELP_TOPICS), 12)
        self.assertNotIn("Treasury", markup)
        self.assertIn("용어·사용법", markup)

    def test_runtime_uses_build_without_copy_patch(self):
        built = (FRONTEND / "build/index.js").read_text(encoding="utf-8")
        wrapper = (ROOT / "components/trade_treasury_experience/__init__.py").read_text(encoding="utf-8")
        self.assertEqual(_JS, "/* bundled component */\n" + built)
        self.assertNotIn("_JS_COPY_REPLACEMENTS", wrapper)
        self.assertNotIn("active_stage", wrapper)

    def test_frontend_owns_only_accessible_navigation(self):
        source = (FRONTEND / "src/ExperienceShell.tsx").read_text(encoding="utf-8")
        self.assertIn('active_view: ViewId', source)
        self.assertIn('aria-current', source)
        self.assertIn('<button', source)
        for forbidden in ("setTriggerValue", "primary_action", "run_review", "setTimeout", "active_stage", "evaluate_deal", "openai", "src.finance", "추천"):
            self.assertNotIn(forbidden, source)
        self.assertIn('reducedMotion="user"', source)

    def test_mobile_navigation_fits_and_focus_is_visible(self):
        css = (FRONTEND / "src/styles.css").read_text(encoding="utf-8")
        self.assertIn("min-width: 0", css)
        self.assertIn("focus-visible", css)
        self.assertNotIn(".snapshot-grid", css)

    def test_imported_rows_survive_bridge_as_erp_import(self):
        source = (
            ROOT / "assets" / "demo" / "Company_Cash_Plan_ERP_Export.csv"
        ).read_text(encoding="utf-8")
        imported = parse_company_cash_events_csv(source)
        bridged = company_cash_events_from_rows(company_cash_rows(imported))
        self.assertTrue(
            all(item.source is CompanyCashEventSource.ERP_IMPORT for item in bridged)
        )
        self.assertEqual(bridged, imported)

    def test_manual_rows_default_to_manual_source(self):
        row = {
            "예정일": "2026-09-24",
            "구분": "AR_COLLECTION",
            "금액 (KRW)": Decimal("40000000"),
            "상태": "CONFIRMED",
            "참조": "기존 매출채권 A",
        }
        event = company_cash_events_from_rows([row])[0]
        self.assertIs(event.source, CompanyCashEventSource.MANUAL)

    def test_compiled_assets_are_committed_inputs_for_runtime(self):
        self.assertTrue((FRONTEND / "build" / "index.js").is_file())
        self.assertTrue((FRONTEND / "build" / "index.css").is_file())


if __name__ == "__main__":
    unittest.main()
