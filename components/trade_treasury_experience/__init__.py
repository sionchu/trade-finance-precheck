from datetime import date, datetime
from decimal import Decimal
from html import escape as html_escape
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
_JS = "/* bundled component */\n" + (_BUILD_DIR / "index.js").read_text(
    encoding="utf-8"
)
_CSS = "/* bundled component */\n" + (_BUILD_DIR / "index.css").read_text(encoding="utf-8")


STAGES = (
    {"id": "deal", "label": "거래 입력"},
    {"id": "review", "label": "판단 기준"},
    {"id": "liquidity", "label": "회사 자금"},
    {"id": "treasury", "label": "대응 시뮬레이션"},
    {"id": "result", "label": "결과·보고서"},
)
VALID_STAGES = {stage["id"] for stage in STAGES}

STAGE_GUIDE = (
    {"title": "거래 입력", "description": "PDF 또는 직접 입력으로 거래 사실을 확인합니다.", "next": "다음: 판단 기준을 조절합니다."},
    {"title": "판단 기준", "description": "목표·환율·금리·회수일을 바꾸면 결과가 즉시 달라집니다.", "next": "다음: 회사 자금계획을 합칩니다."},
    {"title": "회사 자금", "description": "회사 기존 일정과 거래를 같은 Timeline에서 비교합니다.", "next": "다음: 부족분을 메울 조건을 비교합니다."},
    {"title": "대응 시뮬레이션", "description": "운전자금·매출채권·선물환·Usance의 현재→대안→변화를 봅니다.", "next": "다음: 결과와 보고서를 확인합니다."},
    {"title": "결과·보고서", "description": "계산 결과를 먼저 보고 선택적으로 짧은 거래 검토를 실행합니다.", "next": "보고서를 저장하거나 조건을 다시 조절합니다."},
)

HELP_TOPICS = (
    {
        "title": "현재 마진",
        "description": "이번 거래의 금융비용까지 반영한 현재 마진입니다.",
        "caution": "목표마진과 비교하는 현재 입력 기준 계산값입니다.",
    },
    {
        "title": "이번 거래에 필요한 외부자금",
        "description": "이번 거래에 배정한 회사자금을 제외하고 추가로 필요한 최대 자금입니다.",
        "caution": "회사 전체의 다른 지급일정은 포함하지 않은 거래 단독 기준입니다.",
    },
    {
        "title": "회사 전체 최대 자금부족",
        "description": "기존 회사 자금계획과 이번 거래를 함께 봤을 때 최소 운영자금보다 가장 크게 부족한 금액입니다.",
        "caution": "은행이 이 금액을 대출해 준다는 뜻은 아닙니다.",
    },
    {
        "title": "현재 한도 반영 후 부족",
        "description": "회사 전체 최대 부족액에 현재 미사용 운전자금 한도를 반영하고도 남는 부족액입니다.",
        "caution": "현재 입력한 기존 한도 기준이며 신규 승인 가능성을 예측하지 않습니다.",
    },
    {
        "title": "현재 가용현금",
        "description": "Treasury가 지금 실제로 사용할 수 있다고 확인한 현금입니다.",
        "caution": "재무제표상 현금과 자동으로 같은 값으로 보지 않습니다.",
    },
    {
        "title": "최소 운영자금",
        "description": "급여, 세금, 운영비 등을 위해 회사가 남겨두려는 최소 현금 기준입니다.",
        "caution": "사용자가 정한 내부 기준이며 금융기관의 기준이 아닙니다.",
    },
    {
        "title": "D+n",
        "description": "현재 거래 검토 기준일에서 n일 뒤라는 뜻입니다.",
        "caution": "계약일, 선적일, 송장일과 자동으로 같은 기산점은 아닙니다.",
    },
    {
        "title": "O/A",
        "description": "상품을 먼저 공급하고 약정된 날짜에 대금을 받는 외상거래 방식입니다.",
        "caution": "현재 MVP의 핵심 결제방식 중 하나입니다.",
    },
    {
        "title": "매출채권 현금화",
        "description": "고객에게 받을 돈을 만기 전에 먼저 현금화했을 때의 자금·비용 변화를 비교합니다.",
        "caution": "실제 금융상품 실행이나 승인을 의미하지 않습니다.",
    },
    {
        "title": "Banker's Usance",
        "description": "공급자는 먼저 지급받고 회사는 은행에 나중에 상환하는 자금조달 구조를 비교합니다.",
        "caution": "일반 운전자금 사용이 줄어도 총 은행 원금이 사라지는 것은 아닙니다.",
    },
    {
        "title": "순노출",
        "description": "해당 통화로 받을 돈에서 낼 돈을 차감한 금액입니다.",
        "caution": "양수와 음수에 따라 불리한 환율 방향이 달라집니다.",
    },
    {
        "title": "금액 기준 상계",
        "description": "같은 통화의 수취와 지급 금액이 서로 상쇄되는 부분입니다.",
        "caution": "금액이 상계돼도 지급일과 수취일이 다르면 시점 위험은 남습니다.",
    },
    {
        "title": "선물환 시뮬레이션",
        "description": "사용자가 입력한 선물환 가격으로 일부 외화금액을 고정했을 때를 비교합니다.",
        "caution": "환율 전망이나 헤지비율 추천이 아닙니다.",
    },
    {
        "title": "목표마진 유지선",
        "description": "현재 거래가 설정한 목표마진을 유지할 수 있는 환율의 계산 경계입니다.",
        "caution": "미래 환율 예측값이 아닙니다.",
    },
    {
        "title": "복합 악화 시나리오",
        "description": "환율, 금리, 입금 지연 등 여러 불리한 가정을 동시에 적용한 계산입니다.",
        "caution": "발생 확률을 예측하는 모델이 아닙니다.",
    },
    {
        "title": "CONFIRMED / EXPECTED",
        "description": "CONFIRMED는 기본 유동성 계산에 포함하고, EXPECTED는 사용자가 선택할 때만 별도 시나리오에 포함합니다.",
        "caution": "EXPECTED를 AI 예측이나 확정 수금으로 취급하지 않습니다.",
    },
)


def _component_html() -> str:
    steps = "".join(
        (
            '<div class="help-step">'
            f'<strong>{index}. {html_escape(step["title"])}</strong>'
            f'<p>{html_escape(step["description"])}</p>'
            f'<small>{html_escape(step["next"])}</small>'
            "</div>"
        )
        for index, step in enumerate(STAGE_GUIDE, start=1)
    )
    topics = "".join(
        (
            '<details class="help-topic">'
            f'<summary>{html_escape(topic["title"])}</summary>'
            f'<p>{html_escape(topic["description"])}</p>'
            f'<small>{html_escape(topic["caution"])}</small>'
            "</details>"
        )
        for topic in HELP_TOPICS
    )
    return (
        '<div class="react-root"></div>'
        '<details class="help-center">'
        '<summary><span class="help-mark">?</span><span>용어·사용법</span></summary>'
        '<div class="help-panel" role="region" aria-label="서비스 도움말">'
        '<div class="help-heading"><span>처음이라면</span>'
        '<strong>다섯 단계만 따라가면 됩니다</strong>'
        '<p>숫자를 외우기보다 각 단계에서 무엇을 확인하는지 먼저 보세요.</p></div>'
        f'<div class="help-steps">{steps}</div>'
        '<h2>용어·계산 기준</h2>'
        f'<div class="help-topic-list">{topics}</div>'
        '<p class="help-footnote">조건을 바꾼 뒤 이전 결과가 남아 있다면 상단의 '
        '<strong>결과·보고서</strong> 단계에서 현재 조건으로 다시 검토하세요.</p>'
        "</div></details>"
    )


def _register_component():
    return st.components.v2.component(
        "trade-finance-precheck.trade-treasury-experience",
        html=_component_html(),
        css=_CSS,
        js=_JS,
    )


_experience_shell = _register_component()


def get_experience_state(key: str = "trade_treasury_experience") -> dict[str, str]:
    persisted = st.session_state.get(key, {})

    def read(name: str, default: str) -> str:
        if isinstance(persisted, Mapping):
            value = persisted.get(name, default)
        else:
            value = getattr(persisted, name, default)
        return str(value)

    active_stage = read("active_stage", "deal")
    return {
        "active_stage": active_stage if active_stage in VALID_STAGES else "deal",
    }


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
    stage_states: Mapping[str, str] | None = None,
    review_status: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the presentation contract from already-formatted Python values."""
    peak_detail = company_peak_detail
    if company_peak_detail.startswith("Peak "):
        peak_detail = "가장 부족한 날 · " + company_peak_detail.removeprefix("Peak ")
    return {
        "product": {
            "title": "기업 수출거래 Treasury 사전점검",
            "subtitle": (
                "거래조건과 회사 자금계획을 함께 보고, "
                "이 거래를 실제로 감당할 수 있는지 확인합니다."
            ),
        },
        "stages": [
            {**stage, "state": (stage_states or {}).get(stage["id"], "ready")}
            for stage in STAGES
        ],
        "reviewState": dict(review_status or {}),
        "snapshot": [
            {
                "label": "현재 마진",
                "value": margin,
                "detail": margin_detail,
                "status": margin_status,
            },
            {
                "label": "이번 거래에 필요한 외부자금",
                "value": deal_funding,
                "detail": "이번 거래에 배정한 현금 기준",
                "status": "neutral",
            },
            {
                "label": "회사 전체 최대 자금부족",
                "value": company_peak_gap,
                "detail": peak_detail,
                "status": "warning",
            },
            {
                "label": "현재 한도 반영 후 부족",
                "value": remaining_gap,
                "detail": remaining_gap_detail,
                "status": remaining_gap_status,
            },
        ],
    }


def trade_treasury_experience(
    data: dict[str, Any],
    *,
    key: str = "trade_treasury_experience",
):
    """Mount the presentation-only Treasury shell."""
    global _experience_shell
    state = get_experience_state(key)
    component_data = {
        **data,
        "activeStage": state["active_stage"],
    }
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
