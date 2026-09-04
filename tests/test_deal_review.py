from dataclasses import replace
from datetime import date
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch
import unittest

from src.ai.deal_review import (
    DealReviewError,
    DealReviewMemo,
    ReviewSignal,
    TOOL_NAMES,
    _current_deal_payload,
    _payment_context_payload,
    _stress_rescue_payload,
    is_current_deal_review,
    run_deal_review,
)
from src.ai.financialization import MODEL
from src.domain.deal_case import reference_deal, reference_fx
from src.external.ksure_payment import PaymentContext, PaymentShare
from src.finance.engine import Scenario, canonical_scenarios, evaluate_deal
from src.finance.rescue import RescueLever, analyze_deal_rescue


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
        "key_signals": (
            ReviewSignal.COMBINED_STRESS,
            ReviewSignal.SALE_PRICE_BOUNDARY,
        ),
        "negotiation_focus": (RescueLever.SALE_AMOUNT_USD,),
        "payment_context_note": None,
    }
    values.update(overrides)
    return DealReviewMemo(**values)


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

    def invoke(self, client=None, context=None, question="거래를 검토해줘"):
        return run_deal_review(
            question,
            deal=self.deal,
            fx=self.fx,
            base_result=self.base,
            scenario_results=self.scenarios,
            zero_profit_threshold=Decimal("1143.35"),
            target_margin_threshold=Decimal("1386.47"),
            rescue_analysis=self.rescue,
            payment_context=context,
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

    def test_payment_tool_returns_loaded_false_when_absent(self):
        self.assertEqual(_payment_context_payload(None), {"loaded": False})

    def test_payment_tool_returns_aggregate_semantics_when_present(self):
        payload = _payment_context_payload(payment_context())
        self.assertTrue(payload["loaded"])
        self.assertEqual(payload["average_late_payment_period_days"], "13.7")
        self.assertIn("개별 바이어", payload["semantic_warning"])
        self.assertEqual(payload["payment_terms"][0]["observation_count"], 80)

    def test_first_request_receives_exactly_three_local_tools(self):
        client = FakeClient()
        self.invoke(client)
        request = client.responses.create_calls[0]
        self.assertEqual(tuple(tool["name"] for tool in request["tools"]), TOOL_NAMES)
        self.assertEqual(request["tool_choice"], "required")
        self.assertTrue(all(tool["strict"] for tool in request["tools"]))

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
        self.assertEqual(result.memo.key_signals[0], ReviewSignal.COMBINED_STRESS)

    def test_numeric_ai_prose_is_rejected(self):
        client = FakeClient(final_memo=memo(summary="마진은 8퍼센트 수준입니다."))
        with self.assertRaises(DealReviewError):
            self.invoke(client)

    def test_ksure_note_without_loaded_context_is_rejected(self):
        client = FakeClient(final_memo=memo(payment_context_note="집계 맥락을 참고합니다."))
        with self.assertRaises(DealReviewError):
            self.invoke(client)

    def test_ksure_signal_without_loaded_context_is_rejected(self):
        client = FakeClient(
            final_memo=memo(
                key_signals=(
                    ReviewSignal.COMBINED_STRESS,
                    ReviewSignal.KSURE_PAYMENT_CONTEXT,
                )
            )
        )
        with self.assertRaises(DealReviewError):
            self.invoke(client)

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
                    existing, existing.question, self.deal, self.fx, None
                )
            )
        self.assertEqual(len(client.responses.create_calls), 1)
        self.assertEqual(len(client.responses.parse_calls), 1)

    def test_freshness_is_current_for_equal_state(self):
        result = self.invoke(FakeClient())
        self.assertTrue(
            is_current_deal_review(result, result.question, self.deal, self.fx, None)
        )

    def test_changing_deal_makes_run_stale(self):
        result = self.invoke(FakeClient())
        changed = replace(self.deal, target_margin=Decimal("0.12"))
        self.assertFalse(
            is_current_deal_review(result, result.question, changed, self.fx, None)
        )

    def test_changing_fx_makes_run_stale(self):
        result = self.invoke(FakeClient())
        changed = replace(self.fx, usd_krw=Decimal("1399"))
        self.assertFalse(
            is_current_deal_review(result, result.question, self.deal, changed, None)
        )

    def test_changing_payment_context_makes_run_stale(self):
        context = payment_context()
        result = self.invoke(FakeClient(), context=context)
        changed = payment_context(year=2024)
        self.assertFalse(
            is_current_deal_review(
                result, result.question, self.deal, self.fx, changed
            )
        )

    def test_changing_question_makes_run_stale(self):
        result = self.invoke(FakeClient())
        self.assertFalse(
            is_current_deal_review(result, "다른 질문", self.deal, self.fx, None)
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
            3,
        )


if __name__ == "__main__":
    unittest.main()
