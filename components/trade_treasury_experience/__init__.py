from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, Mapping

import streamlit as st
from streamlit.errors import StreamlitAPIException

from src.finance.company_liquidity import (
    CompanyCashEvent,
    CompanyCashEventCategory,
    CompanyCashEventSource,
    CompanyCashEventStatus,
)


_BUILD_DIR = Path(__file__).parent / "frontend" / "build"
_JS = "/* bundled component */\n" + (_BUILD_DIR / "index.js").read_text(encoding="utf-8")
_CSS = "/* bundled component */\n" + (_BUILD_DIR / "index.css").read_text(encoding="utf-8")

def _register_component():
    return st.components.v2.component(
        "trade-finance-precheck.trade-treasury-experience",
        html='<div class="react-root"></div>',
        css=_CSS,
        js=_JS,
    )


_experience_shell = _register_component()

STAGES = (
    {"id": "deal", "label": "거래 조건", "status": "active"},
    {"id": "liquidity", "label": "회사 유동성", "status": "upcoming"},
    {"id": "treasury", "label": "Treasury 검토", "status": "upcoming"},
    {"id": "review", "label": "AI 거래 검토", "status": "upcoming"},
    {"id": "result", "label": "결과 / 공유", "status": "upcoming"},
)


def company_cash_events_from_rows(rows) -> tuple[CompanyCashEvent, ...]:
    """Rebuild company events without losing their UI-row origin."""
    events = []
    for row in rows:
        event_date = row.get("예정일")
        if isinstance(event_date, datetime):
            event_date = event_date.date()
        elif isinstance(event_date, str):
            event_date = date.fromisoformat(event_date)
        events.append(
            CompanyCashEvent(
                event_date=event_date,
                category=CompanyCashEventCategory(row.get("구분")),
                amount_krw=Decimal(str(row.get("금액 (KRW)"))),
                status=CompanyCashEventStatus(row.get("상태")),
                source=CompanyCashEventSource(row.get("출처") or "MANUAL"),
                reference=str(row.get("참조", "")),
            )
        )
    return tuple(events)


def company_cash_rows(events) -> list[dict[str, Any]]:
    """Convert events to editable rows while retaining read-only provenance."""
    return [
        {
            "예정일": item.event_date,
            "구분": item.category.value,
            "금액 (KRW)": float(item.amount_krw),
            "상태": item.status.value,
            "출처": item.source.value,
            "참조": item.reference,
        }
        for item in events
    ]


def build_experience_data(
    *,
    margin: str,
    margin_detail: str,
    margin_status: str,
    deal_funding: str,
    company_peak_gap: str,
    company_peak_detail: str,
    remaining_gap: str,
    remaining_gap_detail: str,
    remaining_gap_status: str,
) -> dict[str, Any]:
    """Build the presentation contract from already-formatted Python values."""
    return {
        "product": {
            "title": "기업 수출거래 Treasury 사전점검",
            "subtitle": (
                "거래조건과 회사 자금계획을 함께 보고 "
                "유동성·외화·자금조달 조건을 검토합니다."
            ),
        },
        "stages": [dict(stage) for stage in STAGES],
        "snapshot": [
            {
                "label": "현재 Deal 마진",
                "value": margin,
                "detail": margin_detail,
                "status": margin_status,
            },
            {
                "label": "거래만 본 은행 필요액",
                "value": deal_funding,
                "detail": "Deal-level 배정자금 기준",
                "status": "neutral",
            },
            {
                "label": "회사 전체 Peak 부족",
                "value": company_peak_gap,
                "detail": company_peak_detail,
                "status": "warning",
            },
            {
                "label": "기존 한도 적용 후 부족",
                "value": remaining_gap,
                "detail": remaining_gap_detail,
                "status": remaining_gap_status,
            },
        ],
        "insight": {
            "deal": f"{deal_funding} 필요",
            "company": f"{company_peak_gap} 필요",
            "afterCredit": remaining_gap_detail,
        },
    }


def trade_treasury_experience(
    data: dict[str, Any],
    *,
    key: str = "trade_treasury_experience",
):
    """Mount the presentation-only Treasury shell."""
    global _experience_shell
    persisted = st.session_state.get(key, {})
    if isinstance(persisted, Mapping):
        active_stage = persisted.get("active_stage", "deal")
    else:
        active_stage = getattr(persisted, "active_stage", "deal")
    if active_stage not in {stage["id"] for stage in STAGES}:
        active_stage = "deal"
    component_data = {**data, "activeStage": active_stage}
    mount_args = {
        "key": key,
        "data": component_data,
        "default": {"active_stage": "deal"},
        "on_active_stage_change": lambda: None,
        "on_primary_action_change": lambda: None,
    }
    try:
        return _experience_shell(**mount_args)
    except StreamlitAPIException as exc:
        if "is not registered" not in str(exc):
            raise
        _experience_shell = _register_component()
        return _experience_shell(**mount_args)
