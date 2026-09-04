from dataclasses import FrozenInstanceError, replace
from datetime import date
from decimal import Decimal
from pathlib import Path
import unittest

from src.domain.deal_case import reference_deal, reference_fx
from src.finance.company_liquidity import (
    CompanyCashEvent,
    CompanyCashEventCategory,
    CompanyCashEventSource,
    CompanyCashEventStatus,
    CompanyLiquidityInput,
    analyze_company_liquidity,
    compare_company_gap_to_credit_line,
    parse_company_cash_events_csv,
)
from src.finance.engine import dated_cashflows
from src.finance.liquidity import WorkingCapitalCreditLine


AS_OF = date(2026, 9, 4)


def event(day, category, amount, status, reference):
    return CompanyCashEvent(
        day, category, Decimal(amount), status, CompanyCashEventSource.MANUAL, reference
    )


def canonical_input(include_expected=False):
    return CompanyLiquidityInput(
        AS_OF,
        Decimal("120000000"),
        Decimal("70000000"),
        (
            event(date(2026, 9, 24), CompanyCashEventCategory.AR_COLLECTION, "40000000", CompanyCashEventStatus.CONFIRMED, "기존 매출채권 A"),
            event(date(2026, 10, 4), CompanyCashEventCategory.PAYROLL_TAX, "-50000000", CompanyCashEventStatus.CONFIRMED, "급여·세금"),
            event(date(2026, 10, 19), CompanyCashEventCategory.AR_COLLECTION, "20000000", CompanyCashEventStatus.CONFIRMED, "기존 매출채권 B"),
            event(date(2026, 10, 29), CompanyCashEventCategory.AR_COLLECTION, "30000000", CompanyCashEventStatus.EXPECTED, "예상 수금 C"),
            event(date(2026, 11, 3), CompanyCashEventCategory.CAPEX, "-30000000", CompanyCashEventStatus.CONFIRMED, "확정 설비대금"),
        ),
        include_expected,
    )


class CompanyLiquidityTests(unittest.TestCase):
    def test_types_are_frozen_and_enums_are_explicit(self):
        item = canonical_input().existing_cash_events[0]
        with self.assertRaises(FrozenInstanceError):
            item.amount_krw = Decimal("1")
        self.assertEqual(len(CompanyCashEventCategory), 6)
        self.assertEqual({item.value for item in CompanyCashEventStatus}, {"CONFIRMED", "EXPECTED"})
        self.assertEqual({item.value for item in CompanyCashEventSource}, {"MANUAL", "ERP_IMPORT"})

    def test_signed_amounts_and_input_validation(self):
        values = [item.amount_krw for item in canonical_input().existing_cash_events]
        self.assertIn(Decimal("40000000"), values)
        self.assertIn(Decimal("-50000000"), values)
        with self.assertRaises(ValueError):
            replace(canonical_input(), current_available_cash_krw=Decimal("-1"))
        with self.assertRaises(ValueError):
            replace(canonical_input(), minimum_operating_cash_krw=Decimal("NaN"))
        with self.assertRaises(ValueError):
            replace(canonical_input(), existing_cash_events=(replace(canonical_input().existing_cash_events[0], event_date=date(2026, 9, 3)),))
        with self.assertRaises(ValueError):
            replace(canonical_input().existing_cash_events[0], reference=" ")

    def test_starting_surplus_keeps_raw_negative_difference(self):
        normal = canonical_input()
        self.assertEqual(normal.raw_starting_liquidity_after_buffer_krw, Decimal("50000000"))
        below = replace(normal, current_available_cash_krw=Decimal("60000000"))
        self.assertEqual(below.raw_starting_liquidity_after_buffer_krw, Decimal("-10000000"))
        self.assertEqual(below.starting_surplus_liquidity_krw, Decimal("0"))

    def test_confirmed_only_company_without_deal(self):
        result = analyze_company_liquidity(liquidity_input=canonical_input(), deal=reference_deal(), fx=reference_fx())
        timeline = result.company_without_deal
        self.assertEqual(timeline.minimum_projected_cash_krw, Decimal("100000000"))
        self.assertEqual(timeline.minimum_projected_cash_date, date(2026, 11, 3))
        self.assertEqual(timeline.peak_liquidity_gap_krw, Decimal("0"))
        self.assertEqual(timeline.ending_projected_cash_krw, Decimal("100000000"))
        self.assertNotIn(date(2026, 10, 29), [point.event_date for point in timeline.points])

    def test_expected_event_is_a_separate_explicit_scenario(self):
        result = analyze_company_liquidity(liquidity_input=canonical_input(True), deal=reference_deal(), fx=reference_fx())
        self.assertIn(date(2026, 10, 29), [point.event_date for point in result.company_without_deal.points])
        self.assertEqual(result.company_without_deal.ending_projected_cash_krw, Decimal("130000000"))
        self.assertEqual(result.company_with_deal.peak_liquidity_gap_krw, Decimal("70000000"))

    def test_deal_overlay_uses_frozen_cashflows_and_calendar_dates(self):
        deal = reference_deal()
        fx = reference_fx()
        result = analyze_company_liquidity(liquidity_input=canonical_input(), deal=deal, fx=fx)
        expected = {event.day: event.amount_krw for event in dated_cashflows(deal, fx)[0]}
        actual = {point.day_offset: point.prospective_deal_cashflow_krw for point in result.company_with_deal.points if point.prospective_deal_cashflow_krw}
        self.assertEqual(actual, expected)
        self.assertEqual(next(point.event_date for point in result.company_with_deal.points if point.day_offset == 60), date(2026, 11, 3))

    def test_canonical_company_with_deal_gap_and_increment(self):
        result = analyze_company_liquidity(liquidity_input=canonical_input(), deal=reference_deal(), fx=reference_fx())
        timeline = result.company_with_deal
        self.assertEqual(timeline.minimum_projected_cash_krw, Decimal("-19000000"))
        self.assertEqual(timeline.minimum_projected_cash_date, date(2026, 11, 3))
        self.assertEqual(timeline.peak_liquidity_gap_krw, Decimal("89000000"))
        self.assertEqual(timeline.peak_liquidity_gap_date, date(2026, 11, 3))
        self.assertEqual(timeline.ending_projected_cash_krw, Decimal("121000000"))
        self.assertEqual(result.incremental_peak_gap_from_deal_krw, Decimal("89000000"))

    def test_credit_line_comparison(self):
        timeline = analyze_company_liquidity(liquidity_input=canonical_input(), deal=reference_deal(), fx=reference_fx()).company_with_deal
        capacity = compare_company_gap_to_credit_line(timeline, WorkingCapitalCreditLine(Decimal("100000000"), Decimal("30000000")))
        self.assertEqual(capacity.unused_credit_limit_krw, Decimal("70000000"))
        self.assertEqual(capacity.liquidity_gap_krw, Decimal("19000000"))
        self.assertEqual(capacity.credit_headroom_krw, Decimal("0"))
        self.assertFalse(capacity.feasible)

    def test_deterministic_and_inputs_unchanged(self):
        deal = reference_deal()
        fx = reference_fx()
        source = canonical_input()
        before = (deal, fx, source)
        first = analyze_company_liquidity(liquidity_input=source, deal=deal, fx=fx)
        self.assertEqual(first, analyze_company_liquidity(liquidity_input=source, deal=deal, fx=fx))
        self.assertEqual((deal, fx, source), before)

    def test_module_has_no_ai_external_or_sap_dependency(self):
        text = (Path(__file__).parents[1] / "src" / "finance" / "company_liquidity.py").read_text(encoding="utf-8").lower()
        for forbidden in ("src.ai", "src.external", "sap", "pandas", "openpyxl"):
            self.assertNotIn(forbidden, text)


class CompanyCashImportTests(unittest.TestCase):
    def parse(self, body):
        return parse_company_cash_events_csv("event_date,category,amount_krw,status,reference\n" + body)

    def test_valid_csv_is_sorted_and_source_is_normalized(self):
        events = self.parse("2026-10-04,PAYROLL_TAX,-50000000,CONFIRMED,급여·세금\n2026-09-24,AR_COLLECTION,40000000,CONFIRMED,기존 매출채권 A\n")
        self.assertEqual([item.event_date for item in events], sorted(item.event_date for item in events))
        self.assertTrue(all(item.source is CompanyCashEventSource.ERP_IMPORT for item in events))

    def test_invalid_rows_and_missing_column_are_rejected(self):
        invalid_bodies = (
            "not-a-date,AR_COLLECTION,1,CONFIRMED,x\n",
            "2026-09-24,NOPE,1,CONFIRMED,x\n",
            "2026-09-24,AR_COLLECTION,1,NOPE,x\n",
            "2026-09-24,AR_COLLECTION,nope,CONFIRMED,x\n",
            "2026-09-24,AR_COLLECTION,1,CONFIRMED, \n",
        )
        for body in invalid_bodies:
            with self.subTest(body=body), self.assertRaises(ValueError):
                self.parse(body)
        with self.assertRaises(ValueError):
            parse_company_cash_events_csv("event_date,category,amount_krw,status\n2026-09-24,AR_COLLECTION,1,CONFIRMED\n")

    def test_bundled_synthetic_csv_matches_canonical_rows(self):
        path = Path(__file__).parents[1] / "assets" / "demo" / "Company_Cash_Plan_ERP_Export.csv"
        events = parse_company_cash_events_csv(path.read_text(encoding="utf-8"))
        self.assertEqual(len(events), 5)
        self.assertEqual(events[-1].reference, "확정 설비대금")


if __name__ == "__main__":
    unittest.main()
