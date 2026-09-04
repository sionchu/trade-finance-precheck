from dataclasses import replace
from datetime import date
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch
import unittest

from src.ai.deal_review import (
    DealReviewError,
    DealReviewMemo,
    SupportingSignal,
    TOOL_NAMES,
    TreasuryFocus,
    TreasuryReviewContext,
    _current_deal_payload,
    _payment_context_payload,
    _stress_rescue_payload,
    _treasury_context_payload,
    is_current_deal_review,
    run_deal_review,
)
from src.ai.financialization import MODEL
from src.ai.financial_statement import CompanyLiquidityProfile
from src.domain.deal_case import Currency, FxRates, reference_deal, reference_fx
from src.external.ksure_payment import PaymentContext, PaymentShare
from src.finance.engine import (
    Scenario,
    canonical_purchase_option,
    canonical_scenarios,
    evaluate_deal,
)
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
from src.finance.rescue import RescueLever, analyze_deal_rescue
from src.finance.usance import BankersUsanceInput, analyze_bankers_usance


def payment_context(year=2025):
    return PaymentContext(
        country_code="450",
        industry_major_code="29",
        last_update_date=date(2026, 8, 1),
        reference_year=year,
        average_payment_period_days=Decimal("62.4"),
        late_payment_rate_percent=Decimal("8.1"),
        average_late_payment_period_days=Decimal("13.7"),
        payment_terms=(PaymentShare("OA", "Open Account", Decimal("72"), 80),),
        payment_period_distribution=(
            PaymentShare("P3", "61-90 days", Decimal("44"), 49),
        ),
    )


def canonical_treasury(deal=None, fx=None, *, include_profile=True):
    deal = deal or reference_deal()
    fx = fx or reference_fx()
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
    profile = (
        CompanyLiquidityProfile(
            Decimal("120000000"),
            Decimal("30000000"),
            Decimal("240000000"),
            Decimal("180000000"),
            Decimal("650000000"),
            Decimal("470000000"),
            Decimal("160000000"),
            Decimal("12000000"),
            Decimal("85000000"),
        )
        if include_profile
        else None
    )
    events = (
        CompanyCashEvent(date(2026, 9, 24), CompanyCashEventCategory.AR_COLLECTION, Decimal("40000000"), CompanyCashEventStatus.CONFIRMED, CompanyCashEventSource.MANUAL, "기존 매출채권 A"),
        CompanyCashEvent(date(2026, 10, 4), CompanyCashEventCategory.PAYROLL_TAX, Decimal("-50000000"), CompanyCashEventStatus.CONFIRMED, CompanyCashEventSource.MANUAL, "급여·세금"),
        CompanyCashEvent(date(2026, 10, 19), CompanyCashEventCategory.AR_COLLECTION, Decimal("20000000"), CompanyCashEventStatus.CONFIRMED, CompanyCashEventSource.MANUAL, "기존 매출채권 B"),
        CompanyCashEvent(date(2026, 11, 3), CompanyCashEventCategory.CAPEX, Decimal("-30000000"), CompanyCashEventStatus.CONFIRMED, CompanyCashEventSource.MANUAL, "확정 설비대금"),
    )
    timeline = analyze_company_liquidity(
        liquidity_input=CompanyLiquidityInput(
            date(2026, 9, 4), Decimal("120000000"), Decimal("70000000"), events
        ),
        deal=deal,
        fx=fx,
    )
    capacity = compare_company_gap_to_credit_line(timeline.company_with_deal, line)
    return TreasuryReviewContext(profile, funding, fx_treasury, usance, timeline, capacity)


def calls(names=TOOL_NAMES):
    return [
        SimpleNamespace(
            type="function_call",
            name=name,
            call_id=f"call-{index}",
            arguments="{}",
        )
        for index, name in enumerate(names)
    ]


def memo(**overrides):
    values = {
        "headline": "복합 상황에서 계약조건 점검이 필요합니다",
        "summary": "가격과 원가 경계를 함께 읽고 자금 부담의 원인을 확인해야 합니다.",
        "treasury_focus": TreasuryFocus.CREDIT_LINE_CAPACITY,
        "supporting_signals": (
            SupportingSignal.COMBINED_STRESS,
            SupportingSignal.FX_RESILIENCE,
        ),
        "negotiation_focus": (RescueLever.SALE_AMOUNT_USD,),
    }
    values.update(overrides)
    return DealReviewMemo(**values)


def legacy_only_memo():
    return memo(
        supporting_signals=(
            SupportingSignal.COMBINED_STRESS,
            SupportingSignal.SALE_PRICE_BOUNDARY,
        )
    )


class FakeResponses:
    def __init__(self, *, tool_calls=None, final_memo=None, create_error=None):
        self.tool_calls = calls() if tool_calls is None else tool_calls
        self.final_memo = memo() if final_memo is None else final_memo
        self.create_error = create_error
        self.create_calls = []
        self.parse_calls = []

    def create(self, **kwargs):
        self.create_calls.append(kwargs)
        if self.create_error is not None:
            raise self.create_error
        return SimpleNamespace(
            output=self.tool_calls,
            usage=SimpleNamespace(input_tokens=30, output_tokens=12, total_tokens=42),
        )

    def parse(self, **kwargs):
        self.parse_calls.append(kwargs)
        return SimpleNamespace(
            output_parsed=self.final_memo,
            usage=SimpleNamespace(input_tokens=80, output_tokens=25, total_tokens=105),
        )


class FakeClient:
    def __init__(self, **kwargs):
        self.responses = FakeResponses(**kwargs)


class DealReviewTests(unittest.TestCase):
    def setUp(self):
        self.deal = reference_deal()
        self.fx = reference_fx()
        self.base = evaluate_deal(self.deal, self.fx)
        self.scenarios = tuple(canonical_scenarios(self.deal, self.fx).items())
        self.rescue = analyze_deal_rescue(self.deal, self.fx)
        self.treasury = canonical_treasury(self.deal, self.fx)

    def invoke(
        self,
        client=None,
        payment=None,
        question="거래를 검토해줘",
        treasury=None,
    ):
        return run_deal_review(
            question,
            deal=self.deal,
            fx=self.fx,
            base_result=self.base,
            scenario_results=self.scenarios,
            zero_profit_threshold=Decimal("1143.35"),
            target_margin_threshold=Decimal("1386.47"),
            rescue_analysis=self.rescue,
            treasury_context=self.treasury if treasury is None else treasury,
            payment_context=payment,
            client=client or FakeClient(),
        )

    def test_current_deal_tool_payload_is_deterministic(self):
        payload = _current_deal_payload(
            self.deal, self.fx, self.base, Decimal("1143.35"), Decimal("1386.47")
        )
        self.assertEqual(payload["sale"]["amount"], "100000")
        self.assertEqual(payload["currency_exposure"]["USD"], "80000")
        self.assertEqual(payload["currency_exposure"]["JPY"], "-3000000")
        self.assertEqual(payload["target_margin_usd_krw_threshold"], "1386.47")

    def test_stress_and_rescue_tool_payload_is_deterministic(self):
        payload = _stress_rescue_payload(
            self.scenarios, self.deal.target_margin, self.rescue
        )
        self.assertEqual(len(payload["scenarios"]), 6)
        self.assertTrue(payload["rescue"]["needs_rescue"])
        self.assertEqual(len(payload["rescue"]["options"]), 5)

    def test_treasury_context_is_frozen_and_payload_is_deterministic(self):
        with self.assertRaises(Exception):
            self.treasury.company_funding = None
        first = _treasury_context_payload(self.treasury, self.deal)
        second = _treasury_context_payload(self.treasury, self.deal)
        self.assertEqual(first, second)

    def test_treasury_payload_exposes_canonical_evidence_and_boundaries(self):
        payload = _treasury_context_payload(self.treasury, self.deal)
        company = payload["company_liquidity"]
        self.assertEqual(company["cash_and_cash_equivalents_krw"], "120000000")
        self.assertEqual(company["deal_available_cash_krw"], "50000000")
        funding = payload["company_funding"]
        self.assertEqual(
            funding["base_capacity"]["required_external_funding_krw"], "69000000"
        )
        self.assertEqual(funding["base_capacity"]["credit_headroom_krw"], "1000000")
        self.assertEqual(funding["combined_capacity"]["liquidity_gap_krw"], "300000.00")
        self.assertEqual(len(funding["choices"]), 3)
        fx_payload = payload["fx_treasury"]
        positions = {item["currency"]: item for item in fx_payload["positions"]}
        self.assertEqual(positions["USD"]["net_exposure"], "80000")
        self.assertEqual(positions["USD"]["amount_level_offset"], "20000")
        self.assertEqual(positions["JPY"]["net_exposure"], "-3000000")
        self.assertEqual(
            fx_payload["settlement_scenario_total_hedge_effect_krw"], "6200000.000"
        )
        self.assertEqual(
            fx_payload["settlement_hedge_overlay_margin"],
            str(self.treasury.fx_treasury.settlement_scenario_overlay.simulated_margin_after_hedge),
        )
        usance = payload["bankers_usance"]
        self.assertEqual(usance["base_ordinary_working_capital_peak_krw"], "69000000")
        self.assertEqual(usance["usance_ordinary_working_capital_peak_krw"], "42000000")
        self.assertEqual(usance["peak_combined_bank_principal_krw"], "69000000")
        self.assertEqual(usance["financing_cost_difference_krw"], "40500.0000000000000000000000")
        timeline = payload["company_cash_timeline"]
        self.assertEqual(timeline["company_without_deal_peak_gap_krw"], "0")
        self.assertEqual(timeline["company_with_deal_peak_gap_krw"], "89000000")
        self.assertEqual(timeline["incremental_peak_gap_from_deal_krw"], "89000000")
        self.assertEqual(timeline["peak_gap_date"], "2026-11-03")
        self.assertEqual(timeline["peak_gap_day_offset"], 60)
        self.assertEqual(timeline["unused_credit_limit_krw"], "70000000")
        self.assertEqual(timeline["residual_gap_after_credit_krw"], "19000000")

    def test_absent_treasury_subsections_are_loaded_false(self):
        empty = TreasuryReviewContext(None, None, None, None)
        payload = _treasury_context_payload(empty, self.deal)
        self.assertTrue(all(value == {"loaded": False} for value in payload.values()))

    def test_payment_tool_returns_loaded_false_when_absent(self):
        self.assertEqual(_payment_context_payload(None), {"loaded": False})

    def test_payment_tool_returns_aggregate_semantics_when_present(self):
        payload = _payment_context_payload(payment_context())
        self.assertTrue(payload["loaded"])
        self.assertEqual(payload["average_late_payment_period_days"], "13.7")
        self.assertIn("개별 바이어", payload["semantic_warning"])
        self.assertEqual(payload["payment_terms"][0]["observation_count"], 80)

    def test_first_request_receives_exactly_four_strict_local_tools(self):
        client = FakeClient()
        self.invoke(client)
        request = client.responses.create_calls[0]
        self.assertEqual(tuple(tool["name"] for tool in request["tools"]), TOOL_NAMES)
        self.assertEqual(request["tool_choice"], "required")
        self.assertTrue(all(tool["strict"] for tool in request["tools"]))
        self.assertTrue(
            all(tool["parameters"]["additionalProperties"] is False for tool in request["tools"])
        )

    def test_reasoning_item_is_preserved_but_never_executed_as_a_tool(self):
        tool_calls = [SimpleNamespace(type="reasoning"), *calls()]
        client = FakeClient(tool_calls=tool_calls)
        result = self.invoke(client)
        self.assertEqual(result.used_tools, TOOL_NAMES)

    def test_unknown_tool_call_is_rejected(self):
        client = FakeClient(tool_calls=calls((TOOL_NAMES[0], TOOL_NAMES[1], "other")))
        with self.assertRaises(DealReviewError):
            self.invoke(client)

    def test_missing_api_key_is_a_safe_application_error(self):
        with patch.dict("os.environ", {"OPENAI_API_KEY": ""}, clear=False):
            with self.assertRaisesRegex(DealReviewError, "AI 거래 검토"):
                run_deal_review(
                    "거래를 검토해줘",
                    deal=self.deal,
                    fx=self.fx,
                    base_result=self.base,
                    scenario_results=self.scenarios,
                    zero_profit_threshold=None,
                    target_margin_threshold=None,
                    rescue_analysis=self.rescue,
                    treasury_context=self.treasury,
                    payment_context=None,
                )

    def test_provider_failure_is_a_safe_application_error(self):
        client = FakeClient(create_error=RuntimeError("provider detail"))
        with self.assertRaisesRegex(DealReviewError, "AI 거래 검토") as caught:
            self.invoke(client)
        self.assertNotIn("provider detail", str(caught.exception))

    def test_missing_required_tool_is_rejected(self):
        client = FakeClient(tool_calls=calls(TOOL_NAMES[:2]))
        with self.assertRaises(DealReviewError):
            self.invoke(client)

    def test_duplicate_tool_call_is_rejected(self):
        client = FakeClient(tool_calls=calls((TOOL_NAMES[0], TOOL_NAMES[0], TOOL_NAMES[2])))
        with self.assertRaises(DealReviewError):
            self.invoke(client)

    def test_successful_flow_performs_exactly_two_requests(self):
        client = FakeClient()
        result = self.invoke(client)
        self.assertEqual(len(client.responses.create_calls), 1)
        self.assertEqual(len(client.responses.parse_calls), 1)
        self.assertEqual(result.request_count, 2)

    def test_both_requests_disable_storage(self):
        client = FakeClient()
        self.invoke(client)
        self.assertFalse(client.responses.create_calls[0]["store"])
        self.assertFalse(client.responses.parse_calls[0]["store"])

    def test_correct_model_and_low_reasoning_are_used(self):
        client = FakeClient()
        result = self.invoke(client)
        self.assertEqual(result.model, MODEL)
        for request in (
            client.responses.create_calls[0], client.responses.parse_calls[0]
        ):
            self.assertEqual(request["model"], MODEL)
            self.assertEqual(request["reasoning"], {"effort": "low"})

    def test_final_structured_memo_is_returned(self):
        result = self.invoke(FakeClient())
        self.assertIsInstance(result.memo, DealReviewMemo)
        self.assertEqual(
            result.memo.treasury_focus, TreasuryFocus.CREDIT_LINE_CAPACITY
        )
        self.assertEqual(
            result.memo.supporting_signals[0], SupportingSignal.COMBINED_STRESS
        )

    def test_treasury_focus_contains_exactly_five_supported_values(self):
        self.assertEqual(
            {focus.value for focus in TreasuryFocus},
            {
                "CREDIT_LINE_CAPACITY",
                "FUNDING_OPTIONS",
                "FX_EXPOSURE",
                "FORWARD_HEDGE",
                "BANKERS_USANCE",
            },
        )
        self.assertNotIn("COMPANY_LIQUIDITY", {focus.value for focus in TreasuryFocus})

    def test_supporting_signal_contains_exactly_always_available_deal_values(self):
        self.assertEqual(
            {signal.value for signal in SupportingSignal},
            {
                "CURRENT_MARGIN",
                "FX_RESILIENCE",
                "FUNDING_BURDEN",
                "COMBINED_STRESS",
                "SALE_PRICE_BOUNDARY",
                "USD_COST_BOUNDARY",
                "JPY_COST_BOUNDARY",
                "COLLECTION_DAY_BOUNDARY",
                "FUNDING_RATE_BOUNDARY",
            },
        )
        self.assertNotIn("COMPANY_LIQUIDITY", SupportingSignal.__members__)
        self.assertNotIn("KSURE_PAYMENT_CONTEXT", SupportingSignal.__members__)
        self.assertTrue(
            {focus.value for focus in TreasuryFocus}.isdisjoint(
                {signal.value for signal in SupportingSignal}
            )
        )

    def test_memo_requires_treasury_focus(self):
        values = memo().model_dump()
        values.pop("treasury_focus")
        with self.assertRaises(Exception):
            DealReviewMemo(**values)

    def test_numeric_ai_prose_is_rejected(self):
        client = FakeClient(final_memo=memo(summary="마진은 8퍼센트 수준입니다."))
        with self.assertRaises(DealReviewError):
            self.invoke(client)

    def test_valid_focus_accepts_legacy_only_supporting_signals(self):
        result = self.invoke(FakeClient(final_memo=legacy_only_memo()))
        self.assertEqual(
            result.memo.supporting_signals,
            legacy_only_memo().supporting_signals,
        )

    def test_each_available_treasury_focus_passes(self):
        for focus in TreasuryFocus:
            with self.subTest(focus=focus):
                result = self.invoke(
                    FakeClient(final_memo=legacy_only_memo().model_copy(
                        update={"treasury_focus": focus}
                    ))
                )
                self.assertEqual(result.memo.treasury_focus, focus)

    def test_each_unavailable_treasury_focus_is_rejected(self):
        cases = (
            (TreasuryReviewContext(None, None, self.treasury.fx_treasury, self.treasury.bankers_usance), TreasuryFocus.CREDIT_LINE_CAPACITY),
            (TreasuryReviewContext(None, None, self.treasury.fx_treasury, self.treasury.bankers_usance), TreasuryFocus.FUNDING_OPTIONS),
            (TreasuryReviewContext(None, self.treasury.company_funding, None, self.treasury.bankers_usance), TreasuryFocus.FX_EXPOSURE),
            (TreasuryReviewContext(None, self.treasury.company_funding, None, self.treasury.bankers_usance), TreasuryFocus.FORWARD_HEDGE),
            (TreasuryReviewContext(None, self.treasury.company_funding, self.treasury.fx_treasury, None), TreasuryFocus.BANKERS_USANCE),
        )
        for treasury, focus in cases:
            with self.subTest(focus=focus):
                client = FakeClient(
                    final_memo=legacy_only_memo().model_copy(
                        update={"treasury_focus": focus}
                    )
                )
                with self.assertRaises(DealReviewError):
                    self.invoke(client, treasury=treasury)

    def test_optional_context_absence_cannot_break_structured_output(self):
        without_optional = canonical_treasury(
            self.deal, self.fx, include_profile=False
        )
        result = self.invoke(
            FakeClient(final_memo=legacy_only_memo()),
            treasury=without_optional,
            payment=None,
        )
        self.assertEqual(
            result.memo.supporting_signals,
            legacy_only_memo().supporting_signals,
        )

    def test_loaded_optional_context_does_not_change_memo_contract(self):
        result = self.invoke(
            FakeClient(final_memo=legacy_only_memo()),
            payment=payment_context(),
        )
        self.assertEqual(
            set(DealReviewMemo.model_fields),
            {
                "headline",
                "summary",
                "treasury_focus",
                "supporting_signals",
                "negotiation_focus",
            },
        )

    def test_input_state_is_not_mutated(self):
        original = (self.deal, self.fx, self.rescue)
        self.invoke(FakeClient())
        self.assertEqual((self.deal, self.fx, self.rescue), original)

    def test_repeated_render_without_explicit_run_does_not_call_client(self):
        client = FakeClient()
        existing = self.invoke(client)
        for _ in range(2):
            self.assertTrue(
                is_current_deal_review(
                    existing,
                    existing.question,
                    self.deal,
                    self.fx,
                    self.treasury,
                    None,
                )
            )
        self.assertEqual(len(client.responses.create_calls), 1)
        self.assertEqual(len(client.responses.parse_calls), 1)

    def test_freshness_is_current_for_equal_state(self):
        result = self.invoke(FakeClient())
        self.assertTrue(
            is_current_deal_review(
                result, result.question, self.deal, self.fx, self.treasury, None
            )
        )

    def test_changing_deal_makes_run_stale(self):
        result = self.invoke(FakeClient())
        changed = replace(self.deal, target_margin=Decimal("0.12"))
        self.assertFalse(
            is_current_deal_review(
                result, result.question, changed, self.fx, self.treasury, None
            )
        )

    def test_changing_fx_makes_run_stale(self):
        result = self.invoke(FakeClient())
        changed = replace(self.fx, usd_krw=Decimal("1399"))
        self.assertFalse(
            is_current_deal_review(
                result, result.question, self.deal, changed, self.treasury, None
            )
        )

    def test_changing_payment_context_makes_run_stale(self):
        context = payment_context()
        result = self.invoke(FakeClient(), payment=context)
        changed = payment_context(year=2024)
        self.assertFalse(
            is_current_deal_review(
                result, result.question, self.deal, self.fx, self.treasury, changed
            )
        )

    def test_changing_question_makes_run_stale(self):
        result = self.invoke(FakeClient())
        self.assertFalse(
            is_current_deal_review(
                result, "다른 질문", self.deal, self.fx, self.treasury, None
            )
        )

    def test_changing_or_restoring_treasury_context_controls_freshness(self):
        result = self.invoke(FakeClient())
        changed = TreasuryReviewContext(
            None,
            self.treasury.company_funding,
            self.treasury.fx_treasury,
            self.treasury.bankers_usance,
        )
        self.assertFalse(
            is_current_deal_review(
                result, result.question, self.deal, self.fx, changed, None
            )
        )
        self.assertTrue(
            is_current_deal_review(
                result,
                result.question,
                self.deal,
                self.fx,
                canonical_treasury(self.deal, self.fx),
                None,
            )
        )

    def test_each_treasury_dimension_participates_in_freshness(self):
        result = self.invoke(FakeClient())
        funding = self.treasury.company_funding
        fx_treasury = self.treasury.fx_treasury
        usance = self.treasury.bankers_usance
        self.assertIsNotNone(funding)
        self.assertIsNotNone(fx_treasury)
        self.assertIsNotNone(usance)

        changed_line = replace(
            funding,
            credit_line=WorkingCapitalCreditLine(
                Decimal("100000001"), Decimal("30000000")
            ),
        )
        changed_purchase = replace(
            funding,
            choices=tuple(
                replace(choice, cash_inflow_day=66)
                if choice.choice.value == "EARLY_RECEIVABLE_PURCHASE"
                else choice
                for choice in funding.choices
            ),
        )
        changed_forward = replace(
            fx_treasury,
            settlement_scenario_hedges=(
                replace(
                    fx_treasury.settlement_scenario_hedges[0],
                    forward_rate_quote=Decimal("1396"),
                ),
                fx_treasury.settlement_scenario_hedges[1],
            ),
        )
        changed_settlement = replace(
            fx_treasury,
            settlement_scenario_overlay=replace(
                fx_treasury.settlement_scenario_overlay,
                unhedged_margin=Decimal("0.1"),
            ),
        )
        changed_usance = replace(
            usance,
            usance=replace(usance.usance, company_repayment_day=91),
        )
        variants = (
            replace(self.treasury, company_funding=changed_line),
            replace(self.treasury, company_funding=changed_purchase),
            replace(self.treasury, fx_treasury=changed_forward),
            replace(self.treasury, fx_treasury=changed_settlement),
            replace(self.treasury, bankers_usance=changed_usance),
            replace(self.treasury, company_liquidity=None),
        )
        for changed in variants:
            with self.subTest(changed=changed):
                self.assertFalse(
                    is_current_deal_review(
                        result,
                        result.question,
                        self.deal,
                        self.fx,
                        changed,
                        None,
                    )
                )

        self.assertTrue(
            is_current_deal_review(
                result,
                result.question,
                self.deal,
                self.fx,
                self.treasury,
                None,
            )
        )

    def test_usage_is_aggregated_only_from_both_requests(self):
        result = self.invoke(FakeClient())
        self.assertEqual(result.usage.input_tokens, 110)
        self.assertEqual(result.usage.output_tokens, 37)
        self.assertEqual(result.usage.total_tokens, 147)

    def test_second_request_has_no_callable_tools(self):
        client = FakeClient()
        self.invoke(client)
        self.assertNotIn("tools", client.responses.parse_calls[0])
        outputs = client.responses.parse_calls[0]["input"]
        self.assertEqual(outputs[0]["content"], "거래를 검토해줘")
        self.assertEqual(
            sum(isinstance(item, dict) and item.get("type") == "function_call_output" for item in outputs),
            4,
        )


if __name__ == "__main__":
    unittest.main()
