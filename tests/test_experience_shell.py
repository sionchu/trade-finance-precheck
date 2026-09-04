from decimal import Decimal
from pathlib import Path
import unittest

from components.trade_treasury_experience import (
    STAGES,
    build_experience_data,
    company_cash_events_from_rows,
    company_cash_rows,
    trade_treasury_experience,
)
from src.finance.company_liquidity import (
    CompanyCashEventSource,
    parse_company_cash_events_csv,
)


ROOT = Path(__file__).parents[1]
FRONTEND = ROOT / "components" / "trade_treasury_experience" / "frontend"


class ExperienceShellTests(unittest.TestCase):
    def test_wrapper_imports_and_has_five_exact_stages(self):
        self.assertTrue(callable(trade_treasury_experience))
        self.assertEqual(
            [stage["id"] for stage in STAGES],
            ["deal", "liquidity", "treasury", "review", "result"],
        )
        self.assertEqual(STAGES[0]["status"], "active")

    def test_python_supplies_canonical_formatted_snapshot(self):
        data = build_experience_data(
            margin="14.64%",
            margin_detail="목표 충족",
            margin_status="success",
            deal_funding="6,900만원",
            company_peak_gap="8,900만원",
            company_peak_detail="Peak 2026-11-03",
            remaining_gap="1,900만원",
            remaining_gap_detail="1,900만원 부족",
            remaining_gap_status="danger",
        )
        self.assertEqual([item["value"] for item in data["snapshot"]], ["14.64%", "6,900만원", "8,900만원", "1,900만원"])
        self.assertEqual(data["insight"]["company"], "8,900만원 필요")

    def test_frontend_has_no_finance_or_ai_dependency(self):
        source = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (FRONTEND / "src").glob("*.*")
        ).lower()
        for forbidden in ("src.finance", "evaluate_deal", "openai", "ksure"):
            self.assertNotIn(forbidden, source)
        self.assertIn('active_stage: stageid', source)
        self.assertIn('"deal"', source)

    def test_imported_rows_survive_bridge_as_erp_import(self):
        source = (ROOT / "assets" / "demo" / "Company_Cash_Plan_ERP_Export.csv").read_text(encoding="utf-8")
        imported = parse_company_cash_events_csv(source)
        bridged = company_cash_events_from_rows(company_cash_rows(imported))
        self.assertTrue(all(item.source is CompanyCashEventSource.ERP_IMPORT for item in bridged))
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
