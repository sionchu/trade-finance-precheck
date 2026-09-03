import copy
from datetime import date
from decimal import Decimal
import io
import json
import os
import unittest
from dataclasses import FrozenInstanceError
from unittest.mock import patch
from urllib.error import URLError
from urllib.parse import parse_qs, urlparse

from src.external.eximbank_fx import (
    EximbankFxError,
    EximbankFxResponseError,
    fetch_fx_reference,
    parse_fx_reference,
)


REFERENCE_DATE = date(2026, 9, 2)
LIVE_SANITIZED_ROWS = [
    {
        "result": 1,
        "cur_unit": "JPY(100)",
        "deal_bas_r": "855.21",
        "ttb": "846.65",
        "tts": "863.76",
        "kftc_deal_bas_r": "855.21",
    },
    {
        "result": 1,
        "cur_unit": "USD",
        "deal_bas_r": "1,370.3",
        "ttb": "1,356.59",
        "tts": "1,384",
        "kftc_deal_bas_r": "1,370.3",
    },
    {"result": 1, "cur_unit": "EUR", "deal_bas_r": "1,599.6"},
]


class EximbankFxTests(unittest.TestCase):
    def test_successful_usd_jpy_parsing(self):
        snapshot = parse_fx_reference(LIVE_SANITIZED_ROWS, REFERENCE_DATE)
        self.assertEqual(snapshot.reference_date, REFERENCE_DATE)
        self.assertEqual(snapshot.usd_krw, Decimal("1370.3"))
        self.assertEqual(snapshot.jpy_krw_per_100, Decimal("855.21"))

    def test_comma_separated_decimal_conversion(self):
        snapshot = parse_fx_reference(LIVE_SANITIZED_ROWS, REFERENCE_DATE)
        self.assertEqual(snapshot.usd_krw, Decimal("1370.3"))

    def test_usd_deal_bas_r_is_the_reference_value(self):
        payload = copy.deepcopy(LIVE_SANITIZED_ROWS)
        usd = next(row for row in payload if row["cur_unit"] == "USD")
        usd["ttb"] = "1"
        usd["tts"] = "2"
        self.assertEqual(
            parse_fx_reference(payload, REFERENCE_DATE).usd_krw,
            Decimal("1370.3"),
        )

    def test_jpy_100_deal_bas_r_is_the_reference_value(self):
        snapshot = parse_fx_reference(LIVE_SANITIZED_ROWS, REFERENCE_DATE)
        self.assertEqual(snapshot.jpy_krw_per_100, Decimal("855.21"))

    def test_plain_jpy_does_not_replace_jpy_100_semantics(self):
        payload = copy.deepcopy(LIVE_SANITIZED_ROWS)
        payload[0]["cur_unit"] = "JPY"
        with self.assertRaisesRegex(EximbankFxResponseError, r"JPY\(100\)"):
            parse_fx_reference(payload, REFERENCE_DATE)

    def test_empty_array_is_no_data(self):
        self.assertIsNone(parse_fx_reference([], REFERENCE_DATE))

    def test_missing_usd_fails(self):
        payload = [row for row in LIVE_SANITIZED_ROWS if row["cur_unit"] != "USD"]
        with self.assertRaisesRegex(EximbankFxResponseError, "one USD"):
            parse_fx_reference(payload, REFERENCE_DATE)

    def test_duplicate_usd_fails(self):
        payload = copy.deepcopy(LIVE_SANITIZED_ROWS)
        payload.append(copy.deepcopy(payload[1]))
        with self.assertRaisesRegex(EximbankFxResponseError, "one USD"):
            parse_fx_reference(payload, REFERENCE_DATE)

    def test_missing_jpy_100_fails(self):
        payload = [
            row for row in LIVE_SANITIZED_ROWS if row["cur_unit"] != "JPY(100)"
        ]
        with self.assertRaisesRegex(EximbankFxResponseError, r"JPY\(100\)"):
            parse_fx_reference(payload, REFERENCE_DATE)

    def test_duplicate_jpy_100_fails(self):
        payload = copy.deepcopy(LIVE_SANITIZED_ROWS)
        payload.append(copy.deepcopy(payload[0]))
        with self.assertRaisesRegex(EximbankFxResponseError, r"JPY\(100\)"):
            parse_fx_reference(payload, REFERENCE_DATE)

    def test_malformed_required_rate_fails(self):
        for malformed in (None, "", "n/a", "1,2,3", 1370.3):
            with self.subTest(malformed=malformed):
                payload = copy.deepcopy(LIVE_SANITIZED_ROWS)
                payload[1]["deal_bas_r"] = malformed
                with self.assertRaises(EximbankFxResponseError):
                    parse_fx_reference(payload, REFERENCE_DATE)

    def test_unsuccessful_required_row_fails(self):
        for unsuccessful in (None, "1", 2):
            with self.subTest(unsuccessful=unsuccessful):
                payload = copy.deepcopy(LIVE_SANITIZED_ROWS)
                payload[1]["result"] = unsuccessful
                with self.assertRaisesRegex(EximbankFxResponseError, "not successful"):
                    parse_fx_reference(payload, REFERENCE_DATE)

    def test_normalized_snapshot_is_immutable(self):
        snapshot = parse_fx_reference(LIVE_SANITIZED_ROWS, REFERENCE_DATE)
        with self.assertRaises(FrozenInstanceError):
            snapshot.usd_krw = Decimal("0")

    def test_missing_auth_key_is_explicit(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(EximbankFxError, "EXIMBANK_AUTH_KEY is not set"):
                fetch_fx_reference(REFERENCE_DATE)

    def test_request_contract_uses_runtime_auth_key(self):
        captured = {}

        def fake_open(request, timeout):
            captured["query"] = parse_qs(urlparse(request.full_url).query)
            captured["timeout"] = timeout
            return io.BytesIO(json.dumps(LIVE_SANITIZED_ROWS).encode("utf-8"))

        with patch.dict(os.environ, {"EXIMBANK_AUTH_KEY": "test-key"}, clear=True):
            snapshot = fetch_fx_reference(
                REFERENCE_DATE, timeout_seconds=4.0, open_url=fake_open
            )

        self.assertEqual(
            set(captured["query"]), {"authkey", "searchdate", "data"}
        )
        self.assertEqual(captured["query"]["searchdate"], ["20260902"])
        self.assertEqual(captured["query"]["data"], ["AP01"])
        self.assertEqual(captured["timeout"], 4.0)
        self.assertEqual(snapshot.usd_krw, Decimal("1370.3"))

    def test_transport_error_does_not_expose_credential(self):
        secret = "transport-secret"

        def failing_open(request, timeout):
            raise URLError(f"failed request containing {secret}")

        with patch.dict(os.environ, {"EXIMBANK_AUTH_KEY": secret}, clear=True):
            with self.assertRaises(EximbankFxError) as raised:
                fetch_fx_reference(REFERENCE_DATE, open_url=failing_open)

        self.assertNotIn(secret, str(raised.exception))
        self.assertIsNone(raised.exception.__cause__)


if __name__ == "__main__":
    unittest.main()
