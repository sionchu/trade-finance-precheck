import copy
import io
import json
import os
import unittest
from dataclasses import FrozenInstanceError
from datetime import date
from decimal import Decimal
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

from src.external.ksure_payment import (
    KsureApiError,
    KsurePaymentError,
    fetch_payment_context,
    parse_payment_context,
)


SUCCESS_RESPONSE = {
    "response": {
        "header": {"resultCode": 0, "resultMsg": "NORMAL SERVICE."},
        "body": {
            "totalCount": 1,
            "items": {
                "item": [
                    {
                        "lastUpdateDate": "2026.01.01",
                        "yearList": [2024, 2025],
                        "paymentTerms": [
                            {
                                "CODE": "PDR_OATT",
                                "CODE_NM": "O/A(T/T 포함)",
                                "PAYMENT_TERMS": [
                                    {"YEAR": "2024", "CNT": 2381.0, "VALUE": 95.5},
                                    {"YEAR": "2025", "CNT": 1903.0, "VALUE": 98.2},
                                ],
                            }
                        ],
                        "averagePaymentPeriod": [
                            {"YEAR": "2024", "VALUE": 78.0},
                            {"YEAR": "2025", "VALUE": 80.8},
                        ],
                        "latePaymentRate": [
                            {"YEAR": "2024", "VALUE": 7.5},
                            {"YEAR": "2025", "VALUE": 15.2},
                        ],
                        "averagelatePaymentPeriod": [
                            {"YEAR": "2024", "VALUE": 11.6},
                            {"YEAR": "2025", "VALUE": 13.7},
                        ],
                        "paymentPeriod": [
                            {
                                "CODE": "90_UNDER",
                                "CODE_NM": "61일 ~ 90일",
                                "PAYMENT_PERIOD": [
                                    {"YEAR": "2024", "CNT": 1265, "VALUE": 50.7},
                                    {"YEAR": "2025", "CNT": 1189, "VALUE": 61.4},
                                ],
                            }
                        ],
                    }
                ]
            },
        },
    }
}


class KsurePaymentParsingTests(unittest.TestCase):
    def parse(self, payload=None):
        return parse_payment_context(
            SUCCESS_RESPONSE if payload is None else payload, "450", "29"
        )

    def test_validated_success_response_parsing(self):
        context = self.parse()
        self.assertEqual(context.country_code, "450")
        self.assertEqual(context.industry_major_code, "29")
        self.assertEqual(context.last_update_date, date(2026, 1, 1))
        self.assertEqual(context.average_payment_period_days, Decimal("80.8"))
        self.assertEqual(context.late_payment_rate_percent, Decimal("15.2"))

    def test_top_level_response_wrapper_is_required(self):
        with self.assertRaisesRegex(KsurePaymentError, "response must be an object"):
            parse_payment_context(SUCCESS_RESPONSE["response"], "450", "29")

    def test_item_array_is_parsed(self):
        self.assertEqual(self.parse().reference_year, 2025)

    def test_result_code_3_with_null_body_is_no_data(self):
        payload = {
            "response": {
                "header": {"resultCode": 3, "resultMsg": "데이터 없음"},
                "body": None,
            }
        }
        self.assertIsNone(self.parse(payload))

    def test_other_nonzero_result_code_is_api_error(self):
        payload = {
            "response": {
                "header": {"resultCode": 10, "resultMsg": "잘못된 요청 파라메터 에러"},
                "body": None,
            }
        }
        with self.assertRaises(KsureApiError) as raised:
            self.parse(payload)
        self.assertEqual(raised.exception.result_code, "10")

    def test_na_and_null_do_not_become_zero(self):
        payload = copy.deepcopy(SUCCESS_RESPONSE)
        item = payload["response"]["body"]["items"]["item"][0]
        item["averagePaymentPeriod"][-1]["VALUE"] = "n/a"
        item["latePaymentRate"][-1]["VALUE"] = None
        del item["averagelatePaymentPeriod"][-1]["VALUE"]
        item["paymentTerms"][0]["PAYMENT_TERMS"][-1]["CNT"] = "n/a"
        context = self.parse(payload)
        self.assertIsNone(context.average_payment_period_days)
        self.assertIsNone(context.late_payment_rate_percent)
        self.assertIsNone(context.average_late_payment_period_days)
        self.assertIsNone(context.payment_terms[0].observation_count)

    def test_latest_reference_year_is_extracted(self):
        context = self.parse()
        self.assertEqual(context.reference_year, 2025)
        self.assertEqual(context.average_payment_period_days, Decimal("80.8"))

    def test_contextual_delay_parses_and_rounds_at_boundary(self):
        context = self.parse()
        self.assertEqual(context.average_late_payment_period_days, Decimal("13.7"))
        self.assertEqual(context.contextual_delay_days(), 14)

    def test_payment_term_percentage_and_count_are_preserved(self):
        term = self.parse().payment_terms[0]
        self.assertEqual(term.code, "PDR_OATT")
        self.assertEqual(term.percent, Decimal("98.2"))
        self.assertEqual(term.observation_count, 1903)

    def test_payment_period_percentage_and_count_are_preserved(self):
        period = self.parse().payment_period_distribution[0]
        self.assertEqual(period.code, "90_UNDER")
        self.assertEqual(period.percent, Decimal("61.4"))
        self.assertEqual(period.observation_count, 1189)

    def test_normalized_model_is_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            self.parse().reference_year = 2024

    def test_missing_service_key_is_explicit(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(KsurePaymentError, "KSURE_SERVICE_KEY is not set"):
                fetch_payment_context("450", "29")

    def test_fetch_uses_ksure_query_and_normalizes_without_live_network(self):
        captured = {}

        def fake_open(request, timeout):
            captured["query"] = parse_qs(urlparse(request.full_url).query)
            captured["timeout"] = timeout
            return io.BytesIO(json.dumps(SUCCESS_RESPONSE).encode("utf-8"))

        with patch.dict(os.environ, {"KSURE_SERVICE_KEY": "test-key"}, clear=True):
            context = fetch_payment_context(
                "450", "29", timeout_seconds=4.0, open_url=fake_open
            )

        self.assertEqual(captured["query"]["ctryCd"], ["450"])
        self.assertEqual(captured["query"]["industryLagCd"], ["29"])
        self.assertEqual(captured["timeout"], 4.0)
        self.assertEqual(context.reference_year, 2025)


if __name__ == "__main__":
    unittest.main()
