from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import json
import os
from typing import Any, Callable, Mapping
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlencode
from urllib.request import Request, urlopen


ENDPOINT = "https://apis.data.go.kr/B552696/exportPayment/getPaymentInfo"
SERVICE_KEY_ENV = "KSURE_SERVICE_KEY"


class KsurePaymentError(RuntimeError):
    """Base error for K-SURE payment-context retrieval and parsing."""


class KsureApiError(KsurePaymentError):
    def __init__(self, result_code: str, result_message: str):
        self.result_code = result_code
        self.result_message = result_message
        super().__init__(f"K-SURE API error {result_code}: {result_message}")


class KsureResponseError(KsurePaymentError):
    """Raised when a successful response does not match the validated schema."""


@dataclass(frozen=True)
class PaymentShare:
    code: str
    name: str
    percent: Decimal | None
    observation_count: int | None


@dataclass(frozen=True)
class PaymentContext:
    country_code: str
    industry_major_code: str
    last_update_date: date
    reference_year: int
    average_payment_period_days: Decimal | None
    late_payment_rate_percent: Decimal | None
    average_late_payment_period_days: Decimal | None
    payment_terms: tuple[PaymentShare, ...]
    payment_period_distribution: tuple[PaymentShare, ...]

    def contextual_delay_days(self) -> int | None:
        """Round aggregate late-payment days only at the scenario boundary."""
        if self.average_late_payment_period_days is None:
            return None
        return int(
            self.average_late_payment_period_days.quantize(
                Decimal("1"), rounding=ROUND_HALF_UP
            )
        )


def _mapping(value: Any, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise KsureResponseError(f"{field} must be an object")
    return value


def _list(value: Any, field: str) -> list[Any]:
    if not isinstance(value, list):
        raise KsureResponseError(f"{field} must be an array")
    return value


def _decimal_or_none(value: Any) -> Decimal | None:
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        if not value or value.lower() == "n/a":
            return None
    if isinstance(value, bool):
        raise KsureResponseError("Boolean is not a numeric K-SURE value")
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise KsureResponseError(f"Invalid numeric K-SURE value: {value!r}") from exc


def _count_or_none(value: Any) -> int | None:
    number = _decimal_or_none(value)
    if number is None:
        return None
    if number != number.to_integral_value():
        raise KsureResponseError("Observation count must be a whole number")
    return int(number)


def _year_value(rows: Any, reference_year: int, field: str) -> Decimal | None:
    for raw_row in _list(rows, field):
        row = _mapping(raw_row, f"{field} entry")
        if str(row.get("YEAR")) == str(reference_year):
            return _decimal_or_none(row.get("VALUE"))
    return None


def _shares(
    groups: Any, reference_year: int, values_field: str, field: str
) -> tuple[PaymentShare, ...]:
    result = []
    for raw_group in _list(groups, field):
        group = _mapping(raw_group, f"{field} entry")
        selected = None
        for raw_row in _list(group.get(values_field), f"{field}.{values_field}"):
            row = _mapping(raw_row, f"{field}.{values_field} entry")
            if str(row.get("YEAR")) == str(reference_year):
                selected = row
                break
        result.append(
            PaymentShare(
                code=str(group.get("CODE", "")),
                name=str(group.get("CODE_NM", "")),
                percent=(
                    None if selected is None else _decimal_or_none(selected.get("VALUE"))
                ),
                observation_count=(
                    None if selected is None else _count_or_none(selected.get("CNT"))
                ),
            )
        )
    return tuple(result)


def parse_payment_context(
    payload: Mapping[str, Any], country_code: str, industry_major_code: str
) -> PaymentContext | None:
    response = _mapping(payload.get("response"), "response")
    header = _mapping(response.get("header"), "response.header")
    result_code = str(header.get("resultCode", ""))
    result_message = str(header.get("resultMsg", ""))

    if result_code == "3":
        return None
    if result_code != "0":
        raise KsureApiError(result_code, result_message)

    body = _mapping(response.get("body"), "response.body")
    items = _mapping(body.get("items"), "response.body.items")
    item_list = _list(items.get("item"), "response.body.items.item")
    if not item_list:
        raise KsureResponseError("Successful K-SURE response contains no item")
    item = _mapping(item_list[0], "response.body.items.item[0]")

    try:
        reference_year = max(int(year) for year in _list(item.get("yearList"), "yearList"))
    except (TypeError, ValueError) as exc:
        raise KsureResponseError("yearList must contain valid years") from exc

    raw_date = str(item.get("lastUpdateDate", ""))
    parsed_date = None
    for date_format in ("%Y.%m.%d", "%Y-%m-%d"):
        try:
            parsed_date = datetime.strptime(raw_date, date_format).date()
            break
        except ValueError:
            pass
    if parsed_date is None:
        raise KsureResponseError("lastUpdateDate has an unsupported format")

    return PaymentContext(
        country_code=country_code,
        industry_major_code=industry_major_code,
        last_update_date=parsed_date,
        reference_year=reference_year,
        average_payment_period_days=_year_value(
            item.get("averagePaymentPeriod"), reference_year, "averagePaymentPeriod"
        ),
        late_payment_rate_percent=_year_value(
            item.get("latePaymentRate"), reference_year, "latePaymentRate"
        ),
        average_late_payment_period_days=_year_value(
            item.get("averagelatePaymentPeriod"),
            reference_year,
            "averagelatePaymentPeriod",
        ),
        payment_terms=_shares(
            item.get("paymentTerms"), reference_year, "PAYMENT_TERMS", "paymentTerms"
        ),
        payment_period_distribution=_shares(
            item.get("paymentPeriod"),
            reference_year,
            "PAYMENT_PERIOD",
            "paymentPeriod",
        ),
    )


def fetch_payment_context(
    country_code: str,
    industry_major_code: str,
    industry_middle_code: str | None = None,
    *,
    timeout_seconds: float = 10.0,
    open_url: Callable[..., Any] = urlopen,
) -> PaymentContext | None:
    service_key = os.environ.get(SERVICE_KEY_ENV)
    if not service_key:
        raise KsurePaymentError(f"{SERVICE_KEY_ENV} is not set")

    params = {
        "serviceKey": unquote(service_key),
        "ctryCd": country_code,
        "industryLagCd": industry_major_code,
    }
    if industry_middle_code is not None:
        params["industryMidCd"] = industry_middle_code
    request = Request(
        f"{ENDPOINT}?{urlencode(params)}", headers={"Accept": "application/json"}
    )

    try:
        with open_url(request, timeout=timeout_seconds) as response:
            payload = json.load(response)
    except HTTPError as exc:
        raise KsurePaymentError(f"K-SURE HTTP error {exc.code}") from None
    except URLError:
        raise KsurePaymentError("K-SURE request failed") from None
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise KsureResponseError("K-SURE response is not valid JSON") from exc

    return parse_payment_context(payload, country_code, industry_major_code)
