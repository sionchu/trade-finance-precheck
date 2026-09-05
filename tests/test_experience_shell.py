from decimal import Decimal
from pathlib import Path
import unittest

from components.trade_treasury_experience import (
    HELP_TOPICS,
    RESPONSE_ACTIONS,
    REVIEW_GOALS,
    STAGE_GUIDE,
    STAGES,
    _JS,
    _component_html,
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
            ["deal", "review", "liquidity", "treasury", "result"],
        )
        self.assertEqual(
            [stage["label"] for stage in STAGES],
            ["거래 입력", "판단 기준", "회사 자금", "대응 시뮬레이션", "결과·보고서"],
        )
        self.assertEqual(
            [goal["id"] for goal in REVIEW_GOALS],
            ["overall", "liquidity", "fx", "funding"],
        )
        self.assertEqual(
            ["none", *(action["id"] for action in RESPONSE_ACTIONS)],
            ["none", "price", "receivable", "credit", "forward", "usance"],
        )

    def test_python_supplies_canonical_formatted_snapshot_with_plain_language(self):
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
        self.assertEqual(
            [item["value"] for item in data["snapshot"]],
            ["14.64%", "6,900만원", "8,900만원", "1,900만원"],
        )
        self.assertEqual(
            [item["label"] for item in data["snapshot"]],
            [
                "현재 마진",
                "이번 거래에 필요한 외부자금",
                "회사 전체 최대 자금부족",
                "현재 한도 반영 후 부족",
            ],
        )
        self.assertEqual(
            data["snapshot"][2]["detail"], "가장 부족한 날 · 2026-11-03"
        )
        self.assertEqual(data["insight"]["company"], "8,900만원 필요")
        self.assertEqual(data["reviewGoals"], list(REVIEW_GOALS))
        self.assertNotIn("Deal-level", "\n".join(item["detail"] for item in data["snapshot"]))

    def test_help_center_is_collapsed_clickable_and_single_source(self):
        markup = _component_html()
        self.assertIn('<details class="help-center">', markup)
        self.assertIn("용어·사용법", markup)
        self.assertEqual(len(STAGE_GUIDE), 5)
        self.assertGreaterEqual(len(HELP_TOPICS), 12)
        for text in (
            "회사 전체 최대 자금부족",
            "현재 한도 반영 후 부족",
            "Banker&#x27;s Usance",
            "CONFIRMED / EXPECTED",
            "거래 검토",
        ):
            self.assertIn(text, markup)

    def test_runtime_copy_removes_prominent_internal_wording(self):
        for forbidden in (
            "거래만 본 은행 필요액",
            "회사 자금계획 포함 Peak 부족",
            "미사용 한도 적용 후",
            "Stress / 조건 경계",
            "공식 결제 Context",
        ):
            self.assertNotIn(forbidden, _JS)
        for expected in (
            "이번 거래에 필요한 외부자금",
            "회사 전체 최대 자금부족",
            "현재 한도 반영 후 부족",
            "판단 기준 조절",
            "이 조건으로 거래 검토",
        ):
            self.assertIn(expected, _JS)

    def test_visual_css_removes_persistent_kpi_wall_and_adds_help(self):
        source = (FRONTEND / "src" / "styles.css").read_text(encoding="utf-8")
        built = (FRONTEND / "build" / "index.css").read_text(encoding="utf-8")
        for css in (source, built):
            self.assertRegex(css, r"\.snapshot-grid\s*\{\s*display:\s*none;?\s*\}")
            self.assertIn(".help-center", css)
            self.assertIn(".help-topic", css)
            self.assertRegex(css, r"\.insight div:{1,2}before")
            self.assertIn("회사 전체 최대 자금부족", css)

    def test_frontend_has_no_finance_or_ai_dependency(self):
        source = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (FRONTEND / "src").glob("*.*")
        ).lower()
        for forbidden in ("src.finance", "evaluate_deal", "openai", "ksure"):
            self.assertNotIn(forbidden, source)
        self.assertIn('active_stage: stageid', source)
        self.assertIn('review_goal: reviewgoal', source)
        self.assertIn('response_action: responseaction', source)
        self.assertNotIn('"continue"', source)
        self.assertNotIn("settimeout", source)
        self.assertNotIn("추천", source)
        self.assertIn('"deal"', source)

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
