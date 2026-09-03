from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
import json
import os
import re
from typing import Any, Callable, Mapping
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ENDPOINT = "https://oapi.koreaexim.go.kr/site/program/financial/exchangeJSON"
AUTH_KEY_ENV = "EXIMBANK_AUTH_KEY"
_RATE_PATTERN = re.compile(r"^[+-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?$")


class EximbankFxError(RuntimeError):
    """Base error for Korea Eximbank reference-FX retrieval and parsing."""


class EximbankFxResponseError(EximbankFxError):
    """Raised when the response does not match the live-validated contract."""


@dataclass(frozen=True)
class FxReferenceSnapshot:
    """Official reference/base rates, not achieved customer settlement rates."""

    reference_date: date
    usd_krw: Decimal
    jpy_krw_per_100: Decimal


def _required_rate(value: Any, field: str) -> Decimal:
    if not isinstance(value, str):
        raise EximbankFxResponseError(f"{field} must be a string")
    normalized = value.strip()
    if not normalized or not _RATE_PATTERN.fullmatch(normalized):
        raise EximbankFxResponseError(f"{field} is not a valid exchange rate")
    try:
        return Decimal(normalized.replace(",", ""))
    except InvalidOperation as exc:
        raise EximbankFxResponseError(
            f"{field} is not a valid exchange rate"
        ) from exc


def _required_currency_row(
    rows: list[Any], currency_unit: str
) -> Mapping[str, Any]:
    matches = [
        row
        for row in rows
        if isinstance(row, Mapping) and row.get("cur_unit") == currency_unit
    ]
    if len(matches) != 1:
        raise EximbankFxResponseError(
            f"Expected exactly one {currency_unit} currency row"
        )
    row = matches[0]
    if type(row.get("result")) is not int or row["result"] != 1:
        raise EximbankFxResponseError(
            f"{currency_unit} currency row is not successful"
        )
    return row


def parse_fx_reference(
    payload: Any, reference_date: date
) -> FxReferenceSnapshot | None:
    if not isinstance(payload, list):
        raise EximbankFxResponseError("Korea Eximbank response must be an array")
    if not payload:
        return None

    usd = _required_currency_row(payload, "USD")
    jpy = _required_currency_row(payload, "JPY(100)")
    return FxReferenceSnapshot(
        reference_date=reference_date,
        usd_krw=_required_rate(usd.get("deal_bas_r"), "USD deal_bas_r"),
        jpy_krw_per_100=_required_rate(
            jpy.get("deal_bas_r"), "JPY(100) deal_bas_r"
        ),
    )


def fetch_fx_reference(
    reference_date: date,
    *,
    timeout_seconds: float = 10.0,
    open_url: Callable[..., Any] = urlopen,
) -> FxReferenceSnapshot | None:
    auth_key = os.environ.get(AUTH_KEY_ENV)
    if not auth_key:
        raise EximbankFxError(f"{AUTH_KEY_ENV} is not set")

    query = urlencode(
        {
            "authkey": auth_key,
            "searchdate": reference_date.strftime("%Y%m%d"),
            "data": "AP01",
        }
    )
    request = Request(f"{ENDPOINT}?{query}", headers={"Accept": "application/json"})

    try:
        with open_url(request, timeout=timeout_seconds) as response:
            payload = json.load(response)
    except HTTPError as exc:
        raise EximbankFxError(f"Korea Eximbank HTTP error {exc.code}") from None
    except URLError:
        raise EximbankFxError("Korea Eximbank request failed") from None
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise EximbankFxResponseError(
            "Korea Eximbank response is not valid JSON"
        ) from exc

    return parse_fx_reference(payload, reference_date)
