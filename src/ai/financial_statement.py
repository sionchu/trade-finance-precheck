from __future__ import annotations

import base64
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
import os
from pathlib import Path
import re
from typing import Literal

from openai import OpenAI
from pydantic import BaseModel, ConfigDict

from src.ai.financialization import MODEL


_NONNEGATIVE_AMOUNT = re.compile(r"^(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?$")
_SIGNED_AMOUNT = re.compile(r"^-?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?$")


class FinancialStatementError(RuntimeError):
    """Safe application-facing error for financial-statement extraction."""


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class StatementFact(StrictModel):
    amount_krw: str | None
    period_end: str | None
    source_filename: Literal["Company_Financial_Statement.pdf"]
    evidence: str
    needs_review: bool


class FinancialStatementFinancialization(StrictModel):
    cash_and_cash_equivalents: StatementFact
    short_term_financial_instruments: StatementFact
    accounts_receivable: StatementFact
    inventory: StatementFact
    current_assets: StatementFact
    current_liabilities: StatementFact
    short_term_borrowings: StatementFact
    finance_cost: StatementFact
    operating_cash_flow: StatementFact
    review_notes: tuple[str, ...]


@dataclass(frozen=True)
class CompanyLiquidityProfile:
    cash_and_cash_equivalents_krw: Decimal | None
    short_term_financial_instruments_krw: Decimal | None
    accounts_receivable_krw: Decimal | None
    inventory_krw: Decimal | None
    current_assets_krw: Decimal | None
    current_liabilities_krw: Decimal | None
    short_term_borrowings_krw: Decimal | None
    finance_cost_krw: Decimal | None
    operating_cash_flow_krw: Decimal | None


EXTRACTION_INSTRUCTIONS = """Extract only facts explicitly supported by the supplied
KRW financial statement. Use only the latest current reporting period and preserve
the exact source filename. Missing facts stay null. Never infer, sum, derive, or
convert accounting values. Do not calculate ratios, working capital, available
company cash, lending capacity, credit approval, credit score, default risk, or
future cash flow. Retained earnings is not cash and must not enter any supported
field. Inventory is not immediately available cash, and accounts receivable is not
cash on hand. Evidence must be short and source-grounded."""


def _normalize_amount(
    value: str | None, *, pattern: re.Pattern[str], nonnegative: bool
) -> Decimal | None:
    if value is None:
        return None
    normalized = value.strip()
    if not normalized or not pattern.fullmatch(normalized):
        raise ValueError("KRW amount must be a supported numeric string")
    try:
        amount = Decimal(normalized.replace(",", ""))
    except InvalidOperation as exc:
        raise ValueError("KRW amount must be a supported numeric string") from exc
    if nonnegative and amount < 0:
        raise ValueError("KRW amount cannot be negative")
    return amount


def normalize_nonnegative_krw_amount(value: str | None) -> Decimal | None:
    return _normalize_amount(value, pattern=_NONNEGATIVE_AMOUNT, nonnegative=True)


def normalize_signed_krw_amount(value: str | None) -> Decimal | None:
    return _normalize_amount(value, pattern=_SIGNED_AMOUNT, nonnegative=False)


def build_company_liquidity_profile(
    financialization: FinancialStatementFinancialization,
) -> CompanyLiquidityProfile:
    return CompanyLiquidityProfile(
        cash_and_cash_equivalents_krw=normalize_nonnegative_krw_amount(
            financialization.cash_and_cash_equivalents.amount_krw
        ),
        short_term_financial_instruments_krw=normalize_nonnegative_krw_amount(
            financialization.short_term_financial_instruments.amount_krw
        ),
        accounts_receivable_krw=normalize_nonnegative_krw_amount(
            financialization.accounts_receivable.amount_krw
        ),
        inventory_krw=normalize_nonnegative_krw_amount(
            financialization.inventory.amount_krw
        ),
        current_assets_krw=normalize_nonnegative_krw_amount(
            financialization.current_assets.amount_krw
        ),
        current_liabilities_krw=normalize_nonnegative_krw_amount(
            financialization.current_liabilities.amount_krw
        ),
        short_term_borrowings_krw=normalize_nonnegative_krw_amount(
            financialization.short_term_borrowings.amount_krw
        ),
        finance_cost_krw=normalize_nonnegative_krw_amount(
            financialization.finance_cost.amount_krw
        ),
        operating_cash_flow_krw=normalize_signed_krw_amount(
            financialization.operating_cash_flow.amount_krw
        ),
    )


def _pdf_input(path: Path) -> dict[str, str]:
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return {
        "type": "input_file",
        "filename": path.name,
        "file_data": f"data:application/pdf;base64,{encoded}",
    }


def analyze_demo_financial_statement(
    pdf_path: Path, *, client: OpenAI | None = None
) -> FinancialStatementFinancialization:
    if client is None:
        if not os.environ.get("OPENAI_API_KEY"):
            raise FinancialStatementError("Financial statement analysis unavailable")
        client = OpenAI()

    try:
        response = client.responses.parse(
            model=MODEL,
            reasoning={"effort": "low"},
            store=False,
            instructions=EXTRACTION_INSTRUCTIONS,
            input=[{"role": "user", "content": [_pdf_input(Path(pdf_path))]}],
            text_format=FinancialStatementFinancialization,
        )
    except Exception:
        raise FinancialStatementError("Financial statement analysis failed") from None

    if response.output_parsed is None:
        raise FinancialStatementError("Financial statement analysis returned no result")
    return response.output_parsed
