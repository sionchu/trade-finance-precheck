from __future__ import annotations

import base64
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from enum import Enum
import os
from pathlib import Path
import re
from typing import Iterable, Literal

from openai import OpenAI
from pydantic import BaseModel, ConfigDict, Field


MODEL = "gpt-5.6-luna"
SUPPORTED_CURRENCIES = frozenset({"KRW", "USD", "JPY"})
_AMOUNT_PATTERN = re.compile(r"^(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?$")


class FinancializationError(RuntimeError):
    """Safe application-facing error for document financialization."""


class ProposalBlockedError(ValueError):
    """Raised when extracted facts cannot safely update the frozen Deal inputs."""


class TimingAnchor(str, Enum):
    SHIPMENT = "SHIPMENT"
    CONTRACT_DATE = "CONTRACT_DATE"
    INVOICE = "INVOICE"
    DELIVERY = "DELIVERY"
    OTHER = "OTHER"
    UNKNOWN = "UNKNOWN"


class ExtractedPaymentMethod(str, Enum):
    OA = "OA"
    TT = "TT"
    LC = "LC"
    DA = "DA"
    DP = "DP"
    OTHER = "OTHER"
    UNKNOWN = "UNKNOWN"


class HedgeStatus(str, Enum):
    PRESENT = "PRESENT"
    NOT_FOUND = "NOT_FOUND"
    AMBIGUOUS = "AMBIGUOUS"


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class FinancialEvent(StrictModel):
    currency_code: str | None
    amount: str | None
    timing_days: int | None = Field(ge=0)
    timing_anchor: TimingAnchor
    description: str
    source_filename: Literal[
        "Sales_Contract.pdf", "Supplier_PO_US.pdf", "Supplier_PO_JP.pdf"
    ]
    evidence: str
    needs_review: bool


class Receivable(FinancialEvent):
    payment_method: ExtractedPaymentMethod


class DocumentFinancialization(StrictModel):
    receivables: tuple[Receivable, ...]
    payables: tuple[FinancialEvent, ...]
    incoterm: str | None
    hedge_status: HedgeStatus
    available_company_cash: str | None
    company_borrowing_rate: str | None
    target_margin: str | None
    review_notes: tuple[str, ...]


@dataclass(frozen=True)
class ProposedDealPatch:
    sale_amount_usd: Decimal
    payment_method: ExtractedPaymentMethod
    usd_payable_amount: Decimal | None
    usd_payable_day: int | None
    jpy_payable_amount: Decimal | None
    jpy_payable_day: int | None


EXTRACTION_INSTRUCTIONS = """Extract only document-supported trade finance facts.
Missing information stays null, and missing hedge information is NOT_FOUND.
Never invent common commercial values. Do not calculate FX, net exposure, margin,
funding need, or working-capital requirements. Do not predict buyer behavior, give
legal conclusions, or recommend accepting or rejecting the deal. Incoterms never
determine payment timing. Preserve each timing anchor exactly: shipment remains
SHIPMENT and purchase contract date remains CONTRACT_DATE. Map Open Account or O/A
to OA. Evidence must be short. Currency codes must remain their actual ISO-style
codes, including currently unsupported currencies. source_filename must be the
exact filename of the input PDF that supports the event."""


def normalize_amount(value: str | None) -> Decimal:
    if value is None:
        raise ValueError("Amount is required")
    normalized = value.strip()
    if not normalized or not _AMOUNT_PATTERN.fullmatch(normalized):
        raise ValueError("Amount must be a numeric string")
    try:
        amount = Decimal(normalized.replace(",", ""))
    except InvalidOperation as exc:
        raise ValueError("Amount must be a numeric string") from exc
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    return amount


def currency_exposure(
    financialization: DocumentFinancialization,
) -> dict[str, Decimal]:
    exposure: dict[str, Decimal] = {}
    for direction, events in (
        (Decimal("1"), financialization.receivables),
        (Decimal("-1"), financialization.payables),
    ):
        for event in events:
            amount = normalize_amount(event.amount)
            if event.currency_code is None:
                raise ValueError("Currency code is required for a financial event")
            currency = event.currency_code.upper()
            exposure[currency] = exposure.get(currency, Decimal("0")) + direction * amount
    return exposure


def unsupported_currencies(
    financialization: DocumentFinancialization,
) -> tuple[str, ...]:
    unsupported = set()
    for event in (*financialization.receivables, *financialization.payables):
        amount = normalize_amount(event.amount)
        if amount and (
            event.currency_code is None
            or event.currency_code.upper() not in SUPPORTED_CURRENCIES
        ):
            unsupported.add(
                "UNKNOWN" if event.currency_code is None else event.currency_code.upper()
            )
    return tuple(sorted(unsupported))


def _contract_day(event: FinancialEvent, contract_date_is_day_zero: bool) -> int | None:
    if not contract_date_is_day_zero:
        return None
    if event.timing_anchor is TimingAnchor.CONTRACT_DATE:
        return event.timing_days
    return None


def build_proposed_deal_patch(
    financialization: DocumentFinancialization,
    *,
    contract_date_is_day_zero: bool,
) -> ProposedDealPatch:
    if any(
        event.needs_review
        for event in (*financialization.receivables, *financialization.payables)
    ):
        raise ProposalBlockedError("Extracted financial events require review")
    unsupported = unsupported_currencies(financialization)
    if unsupported:
        raise ProposalBlockedError(
            f"Unsupported currencies: {', '.join(unsupported)}"
        )
    if financialization.hedge_status is not HedgeStatus.NOT_FOUND:
        raise ProposalBlockedError("Hedge information must be reviewed before applying")
    if len(financialization.receivables) != 1:
        raise ProposalBlockedError("Exactly one sale receivable is required")

    receivable = financialization.receivables[0]
    if receivable.currency_code is None or receivable.currency_code.upper() != "USD":
        raise ProposalBlockedError("The current Deal input supports a USD sale only")
    if receivable.payment_method not in (
        ExtractedPaymentMethod.OA,
        ExtractedPaymentMethod.TT,
    ):
        raise ProposalBlockedError("The extracted sale payment method is unsupported")

    payables: dict[str, FinancialEvent] = {}
    for payable in financialization.payables:
        if payable.currency_code is None:
            raise ProposalBlockedError("A payable currency is missing")
        currency = payable.currency_code.upper()
        if currency in payables:
            raise ProposalBlockedError(f"Multiple {currency} payables require review")
        payables[currency] = payable

    usd = payables.get("USD")
    jpy = payables.get("JPY")
    return ProposedDealPatch(
        sale_amount_usd=normalize_amount(receivable.amount),
        payment_method=receivable.payment_method,
        usd_payable_amount=None if usd is None else normalize_amount(usd.amount),
        usd_payable_day=None if usd is None else _contract_day(usd, contract_date_is_day_zero),
        jpy_payable_amount=None if jpy is None else normalize_amount(jpy.amount),
        jpy_payable_day=None if jpy is None else _contract_day(jpy, contract_date_is_day_zero),
    )


def _pdf_input(path: Path) -> dict[str, str]:
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return {
        "type": "input_file",
        "filename": path.name,
        "file_data": f"data:application/pdf;base64,{encoded}",
    }


def analyze_demo_documents(
    pdf_paths: Iterable[Path], *, client: OpenAI | None = None
) -> DocumentFinancialization:
    if client is None:
        if not os.environ.get("OPENAI_API_KEY"):
            raise FinancializationError("OPENAI_API_KEY is not set")
        client = OpenAI()

    paths = tuple(Path(path) for path in pdf_paths)
    try:
        content = [_pdf_input(path) for path in paths]
        response = client.responses.parse(
            model=MODEL,
            reasoning={"effort": "low"},
            store=False,
            instructions=EXTRACTION_INSTRUCTIONS,
            input=[{"role": "user", "content": content}],
            text_format=DocumentFinancialization,
        )
    except Exception:
        raise FinancializationError("AI document analysis failed") from None

    if response.output_parsed is None:
        raise FinancializationError("AI document analysis returned no structured result")
    return response.output_parsed
