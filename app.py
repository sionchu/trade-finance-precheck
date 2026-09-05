from contextlib import contextmanager
from datetime import date, datetime
from decimal import Decimal
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from zoneinfo import ZoneInfo

import streamlit as st

from components.trade_treasury_experience import (
    build_experience_data,
    company_cash_events_from_rows,
    company_cash_rows,
    get_experience_state,
    trade_treasury_experience,
)

from src.ai.deal_review import (
    DealReviewError,
    SupportingSignal,
    TreasuryFocus,
    TreasuryReviewContext,
    is_current_deal_review,
    run_deal_review,
)
from src.ai.financialization import (
    FinancializationError,
    HedgeStatus,
    ProposalBlockedError,
    TimingAnchor,
    analyze_demo_documents,
    build_proposed_deal_patch,
    currency_exposure as extracted_currency_exposure,
    normalize_amount,
    unsupported_currencies,
)
from src.ai.financial_statement import (
    FinancialStatementError,
    analyze_demo_financial_statement,
    build_company_liquidity_profile,
)
from src.domain.deal_case import (
    Currency,
    DealCase,
    ForeignPayable,
    FxRates,
    KrwCost,
    PaymentMethod,
    Sale,
    reference_deal,
    reference_fx,
)
from src.external.ksure_payment import KsurePaymentError, fetch_payment_context
from src.finance.engine import (
    ReceivablePurchaseOption,
    Scenario,
    canonical_purchase_option,
    canonical_scenarios,
    evaluate_deal,
    solve_usd_krw_threshold,
)
from src.finance.company_liquidity import (
    CompanyCashEventCategory,
    CompanyCashEventStatus,
    CompanyLiquidityInput,
    analyze_company_liquidity,
    compare_company_gap_to_credit_line,
    parse_company_cash_events_csv,
)
from src.finance.fx_treasury import (
    ForwardAction,
    ForwardHedgeInput,
    FxExposureDirection,
    analyze_fx_treasury,
    build_currency_exposure_positions,
)
from src.finance.liquidity import (
    FundingChoice,
    FundingChoiceStatus,
    WorkingCapitalCreditLine,
    analyze_company_funding,
)
from src.finance.rescue import (
    RescueLever,
    RescueStatus,
    analyze_deal_rescue,
)
from src.finance.usance import BankersUsanceInput, analyze_bankers_usance
from src.reporting.deal_report import (
    DealReportInput,
    build_deal_report,
    current_ai_provenance,
    official_context_text,
    report_basis_text,
)


APP_CSS = (Path(__file__).parent / "assets" / "app.css").read_text(encoding="utf-8")
DEMO_PDF_PATHS = (
    Path(__file__).parent / "assets" / "demo" / "Sales_Contract.pdf",
    Path(__file__).parent / "assets" / "demo" / "Supplier_PO_US.pdf",
    Path(__file__).parent / "assets" / "demo" / "Supplier_PO_JP.pdf",
)
COMPANY_STATEMENT_PDF = (
    Path(__file__).parent / "assets" / "demo" / "Company_Financial_Statement.pdf"
)
COMPANY_CASH_PLAN_CSV = (
    Path(__file__).parent / "assets" / "demo" / "Company_Cash_Plan_ERP_Export.csv"
)

CANONICAL_COMPANY_CASH_PLAN_ROWS = (
    {
        "예정일": date(2026, 9, 24),
        "구분": "AR_COLLECTION",
        "금액 (KRW)": 40000000.0,
        "상태": "CONFIRMED",
        "출처": "MANUAL",
        "참조": "기존 매출채권 A",
    },
    {
        "예정일": date(2026, 10, 4),
        "구분": "PAYROLL_TAX",
        "금액 (KRW)": -50000000.0,
        "상태": "CONFIRMED",
        "출처": "MANUAL",
        "참조": "급여·세금",
    },
    {
        "예정일": date(2026, 10, 19),
        "구분": "AR_COLLECTION",
        "금액 (KRW)": 20000000.0,
        "상태": "CONFIRMED",
        "출처": "MANUAL",
        "참조": "기존 매출채권 B",
    },
    {
        "예정일": date(2026, 10, 29),
        "구분": "AR_COLLECTION",
        "금액 (KRW)": 30000000.0,
        "상태": "EXPECTED",
        "출처": "MANUAL",
        "참조": "예상 수금 C",
    },
    {
        "예정일": date(2026, 11, 3),
        "구분": "CAPEX",
        "금액 (KRW)": -30000000.0,
        "상태": "CONFIRMED",
        "출처": "MANUAL",
        "참조": "확정 설비대금",
    },
)

REVIEW_GOAL_QUESTIONS = {
    "overall": "이 거래의 수익성, 회사 전체 유동성, 외화노출과 자금조달 구조에서 우선 확인할 점을 설명해줘.",
    "liquidity": "회사 기존 자금계획과 이번 거래를 함께 봤을 때 유동성과 운전자금 한도에서 우선 확인할 점을 설명해줘.",
    "fx": "이 거래의 통화별 외화노출과 선물환 시뮬레이션에서 우선 확인할 점을 설명해줘.",
    "funding": "기존 운전자금 한도, 매출채권 조기현금화와 Banker's Usance에서 우선 확인할 점을 설명해줘.",
}


def decimal_from_widget(value: int | float) -> Decimal:
    return Decimal(str(value))


def percent(value: Decimal) -> str:
    return f"{value * Decimal('100'):.2f}%"


def krw_millions(value: Decimal) -> str:
    return f"KRW {value / Decimal('1000000'):,.3f}M"


def krw_consumer(value: Decimal) -> str:
    ten_thousands = int((value / Decimal("10000")).quantize(Decimal("1")))
    if ten_thousands >= 10000:
        billions, remainder = divmod(ten_thousands, 10000)
        return (
            f"{billions:,}억 {remainder:,}만원"
            if remainder
            else f"{billions:,}억원"
        )
    return f"{ten_thousands:,}만원"


def optional_krw_consumer(value: Decimal | None) -> str:
    if value is None:
        return "확인 필요"
    if value < 0:
        return f"-{krw_consumer(abs(value))}"
    return krw_consumer(value)


def signed_krw_consumer(value: Decimal) -> str:
    if value > 0:
        return f"+{krw_consumer(value)}"
    return krw_consumer(value)


def krw_ten_thousands(value: Decimal, *, signed: bool = False) -> str:
    amount = value / Decimal("10000")
    rendered = f"{amount:,.2f}".rstrip("0").rstrip(".")
    return f"{'+' if signed and value > 0 else ''}{rendered}만원"


def decimal_text(value: Decimal | None, suffix: str = "") -> str:
    return "n/a" if value is None else f"{value}{suffix}"


def apply_ai_proposal() -> None:
    proposal = st.session_state.get("ai_proposed_patch")
    if proposal is None:
        return
    st.session_state["sale_amount_input"] = float(proposal.sale_amount_usd)
    st.session_state["payment_method_input"] = proposal.payment_method.value
    if proposal.usd_payable_amount is not None:
        st.session_state["usd_payable_amount_input"] = float(
            proposal.usd_payable_amount
        )
    if proposal.usd_payable_day is not None:
        st.session_state["usd_payable_day_input"] = proposal.usd_payable_day
    if proposal.jpy_payable_amount is not None:
        st.session_state["jpy_payable_amount_input"] = float(
            proposal.jpy_payable_amount
        )
    if proposal.jpy_payable_day is not None:
        st.session_state["jpy_payable_day_input"] = proposal.jpy_payable_day
    st.session_state["ai_applied_patch"] = proposal
    st.session_state["ai_apply_notice"] = "확인한 문서 값을 거래 입력에 반영했습니다."


def amount_text(value: str | None) -> str:
    try:
        amount = normalize_amount(value)
    except ValueError:
        return "확인 필요"
    return f"{amount:,.2f}".rstrip("0").rstrip(".")


def timing_text(anchor: TimingAnchor, days: int | None) -> str:
    if days is None:
        return "지급시점 확인 필요"
    labels = {
        TimingAnchor.SHIPMENT: "선적 후",
        TimingAnchor.CONTRACT_DATE: "구매계약 후",
        TimingAnchor.INVOICE: "송장 발행 후",
        TimingAnchor.DELIVERY: "인도 후",
        TimingAnchor.OTHER: "기타 기준 후",
        TimingAnchor.UNKNOWN: "기산점 미확인 ·",
    }
    return f"{labels[anchor]} {days}일"


DEAL_REVIEW_QUESTION = (
    "이 거래의 수익성, 회사 자금여력, 외화노출과 자금조달 구조에서 "
    "우선 확인할 점을 설명해줘."
)


def rescue_option_map(analysis):
    return {option.lever: option for option in analysis.options}


def render_rescue_option(option) -> None:
    labels = {
        RescueLever.SALE_AMOUNT_USD: ("수출가격", "USD", "최소"),
        RescueLever.USD_PAYABLE_AMOUNT: ("USD 원재료비", "USD", "최대"),
        RescueLever.JPY_PAYABLE_AMOUNT: ("JPY 부품비", "JPY", "최대"),
        RescueLever.COLLECTION_DAY: ("결제기간", "D+", "최대"),
        RescueLever.FUNDING_RATE: ("조달금리", "", "최대"),
    }
    label, unit, boundary = labels[option.lever]
    st.markdown(f"**{label}**")
    if option.status is not RescueStatus.FEASIBLE:
        st.write("이 조건 단독 변경으로는 현재 Stress 가정에서 목표 회복 불가")
    elif option.lever is RescueLever.COLLECTION_DAY:
        st.write(f"{boundary} D+{option.threshold_value}")
    elif option.lever is RescueLever.FUNDING_RATE:
        st.write(f"{boundary} {percent(option.threshold_value)}")
    else:
        st.write(f"{boundary} {unit} {option.threshold_value:,.0f}")



@contextmanager
def input_group(label, stages, *, expanded=True):
    """Keep one widget identity mounted; show its controls only in its stage."""
    slot = st.empty()
    with slot.container():
        with st.expander(label, expanded=expanded):
            yield
    if active_stage not in stages:
        slot.empty()


def set_input_value(key, value):
    st.session_state[key] = value


def sync_slider(key, slider_key):
    st.session_state[key] = st.session_state[slider_key]


def exact_input(label, **kwargs):
    """One persistent exact value, including while its stage is hidden."""
    key = kwargs.setdefault("key", label + "_input")
    if "value" in kwargs:
        st.session_state.setdefault(key, kwargs.pop("value"))
    if key in st.session_state:
        st.session_state[key] = st.session_state[key]
    return st.number_input(label, **kwargs)


def scenario_input(label, *, key, value, min_value, max_value, step, **kwargs):
    """The exact input is authoritative; the slider only writes that same key."""
    st.session_state.setdefault(key, value)
    slider_key = key + "_slider"
    current = st.session_state[key]
    st.session_state[slider_key] = current
    slider_slot = st.empty()
    slider_slot.slider(
        label + " 조절",
        min_value=min(min_value, current),
        max_value=max(max_value, current),
        step=step,
        key=slider_key,
        on_change=sync_slider,
        args=(key, slider_key),
    )
    if active_stage == "deal":
        slider_slot.empty()
    return exact_input(
        label, min_value=(0.01 if "KRW" in label else 0.0 if isinstance(value, float) else min_value), max_value=100.0 if "헤지비율" in label else None, step=step, key=key, **kwargs
    )


def fx_presets(key, reference_value):
    with st.container(key="fx_presets_" + key):
        for column, (label, factor) in zip(
            st.columns(5), (("-10%", .9), ("-5%", .95), ("기준", 1.0), ("+5%", 1.05), ("+10%", 1.1))
        ):
            column.button(label, key=key + "_" + label, on_click=set_input_value,
                          args=(key, reference_value * factor), width="stretch")


def compare_values(label, before, after, delta):
    with st.container(border=True, key="comparison_" + label):
        st.markdown("**" + label + "**")
        cols = st.columns(3)
        cols[0].metric("현재", before)
        cols[1].metric("대안", after)
        cols[2].metric("변화", delta, delta_color="off")


def analyze_uploaded_documents(uploads):
    """Adapt three explicit document roles without changing extraction semantics."""
    if len(uploads) != 3 or any(not item for item in uploads):
        raise FinancializationError("세 문서 역할을 모두 선택해 주세요.")
    payloads = [item.getvalue() for item in uploads]
    if any(not data.startswith(b"%PDF-") or len(data) > 10 * 1024 * 1024 for data in payloads):
        raise FinancializationError("PDF 형식과 파일별 10MB 한도를 확인해 주세요.")
    with TemporaryDirectory(prefix="trade-documents-") as directory:
        paths = []
        for role, data in zip(DEMO_PDF_PATHS, payloads):
            path = Path(directory) / role.name
            path.write_bytes(data)
            paths.append(path)
        return analyze_demo_documents(paths)


reference = reference_deal()
reference_rates = reference_fx()
# Retain the canonical widget values when their stage is not visible.
for retained_key in list(st.session_state):
    if retained_key.endswith("_input") or retained_key == "deal_input_mode":
        st.session_state[retained_key] = st.session_state[retained_key]
input_defaults = {
    "sale_amount_input": float(reference.sale.amount),
    "payment_method_input": reference.sale.payment_method.value,
    "collection_day_input": reference.sale.collection_day,
    "usd_payable_amount_input": float(reference.foreign_payables[0].amount),
    "usd_payable_day_input": reference.foreign_payables[0].payment_day,
    "jpy_payable_amount_input": float(reference.foreign_payables[1].amount),
    "jpy_payable_day_input": reference.foreign_payables[1].payment_day,
}
for input_key, default_value in input_defaults.items():
    st.session_state.setdefault(input_key, default_value)

st.set_page_config(page_title="기업 수출거래 Treasury 사전점검", layout="wide")
st.markdown(f"<style>{APP_CSS}</style>", unsafe_allow_html=True)
st.markdown('<div class="product-label">COMPANY-AWARE TRADE TREASURY PRE-CHECK</div>', unsafe_allow_html=True)
st.title("기업 수출거래 Treasury 사전점검")
experience_state = get_experience_state()
active_stage = experience_state["active_stage"]
st.markdown(
    '<p class="product-lead">수출계약 전에 수익성·회사 자금·환율 위험을 함께 확인합니다.</p>',
    unsafe_allow_html=True,
)
st.caption("사전 의사결정 지원용 · 금융 실행, 환율 예측 또는 신용평가 서비스가 아닙니다.")



input_mode_slot = st.empty()
with input_mode_slot.container():
    input_mode = st.radio("거래를 어떻게 입력할까요?", ["직접 입력", "거래서류 불러오기"], horizontal=True, key="deal_input_mode")
if active_stage != "deal":
    input_mode_slot.empty()

experience_shell_slot = st.empty()
credit_controls_slot = st.empty()

with input_group("거래 사실 · 데모값에서 시작", {"deal"} if input_mode == "직접 입력" else set()):
    sale_amount = exact_input(
        "수출대금 (USD)",
        min_value=1.0,
        step=1000.0,
        key="sale_amount_input",
    )
    payment_method_value = st.selectbox(
        "결제방식",
        [method.value for method in PaymentMethod],
        key="payment_method_input",
    )


with input_group("비용 및 지급", {"deal"} if input_mode == "직접 입력" else set()):
    usd_payable = reference.foreign_payables[0]
    jpy_payable = reference.foreign_payables[1]
    usd_payable_amount = exact_input(
        "USD 외화비용",
        min_value=0.0,
        step=1000.0,
        key="usd_payable_amount_input",
    )
    usd_payable_day = exact_input(
        "USD 지급일 (D+)",
        min_value=0,
        step=1,
        key="usd_payable_day_input",
    )
    jpy_payable_amount = exact_input(
        "JPY 외화비용",
        min_value=0.0,
        step=100000.0,
        key="jpy_payable_amount_input",
    )
    jpy_payable_day = exact_input(
        "JPY 지급일 (D+)",
        min_value=0,
        step=1,
        key="jpy_payable_day_input",
    )
    advance, balance, logistics = reference.krw_costs
    advance_amount = exact_input(
        "국내 생산 선급금 (KRW)", min_value=0.0, value=float(advance.amount_krw), step=1000000.0
    )
    advance_day = exact_input(
        "선급금 지급일 (D+)", min_value=0, value=advance.payment_day, step=1
    )
    balance_amount = exact_input(
        "국내 생산 잔금 (KRW)", min_value=0.0, value=float(balance.amount_krw), step=1000000.0
    )
    balance_day = exact_input(
        "잔금 지급일 (D+)", min_value=0, value=balance.payment_day, step=1
    )
    logistics_amount = exact_input(
        "물류·통관비 (KRW)", min_value=0.0, value=float(logistics.amount_krw), step=1000000.0
    )
    logistics_day = exact_input(
        "물류·통관비 지급일 (D+)", min_value=0, value=logistics.payment_day, step=1
    )

with input_group("목표와 조달 가정", {"review"}):
    target_margin_percent = scenario_input("목표 마진 (%)", key="target_margin_input", value=float(reference.target_margin * Decimal("100")), min_value=5.0, max_value=25.0, step=0.1)
    target_live_result = st.empty()
    with st.expander("업종 수익성 참고"):
        st.write("한국은행 기업경영분석 · 업종별 매출액영업이익률")
        st.link_button("한국은행 공식 기업경영분석 자료", "https://www.bok.or.kr/portal/bbs/B0000501/view.do?menuNo=200690&nttId=10094231")
        st.caption("공식 수치·기준연도를 연결하기 전에는 숫자를 표시하지 않습니다. Financing-adjusted Deal Margin과 계산 정의가 다른 참고지표입니다.")
    funding_rate_percent = scenario_input("실제 연 조달금리 (%)", key="funding_rate_input", value=float(reference.annual_funding_rate * Decimal("100")), min_value=0.0, max_value=25.0, step=0.1)
    with st.expander("거래 단독 배정자금"):
        available_cash = exact_input(
            "이번 거래에 투입 가능한 회사자금 (KRW)", min_value=0.0,
            value=float(reference.available_cash_krw), step=1000000.0,
        )

with input_group("환율 시나리오", {"review"}):
    st.caption("기준환율 · 데모 USD 1,400 / JPY 900 (100 JPY) · 공식 관측값 아님")
    fx_presets("usd_krw_input", float(reference_rates.usd_krw))
    usd_krw = scenario_input("USD/KRW", key="usd_krw_input", value=float(reference_rates.usd_krw), min_value=500.0, max_value=2500.0, step=1.0)
    fx_presets("jpy_krw_input", float(reference_rates.jpy_krw_per_100))
    jpy_krw = scenario_input("JPY/KRW per 100 JPY", key="jpy_krw_input", value=float(reference_rates.jpy_krw_per_100), min_value=300.0, max_value=2000.0, step=1.0)
    st.badge("사용자 입력", color="blue")
    st.caption("시나리오만 조절합니다. 공식 환율 API의 배포 경로는 현재 사용하지 않습니다.")
    fx_live_result = st.empty()

with input_group("회수 시점 가정", {"deal", "review"}):
    collection_day = scenario_input("결제일 (D+)", key="collection_day_input", value=reference.sale.collection_day, min_value=0, max_value=365, step=1)
    collection_live_result = st.empty()

deal = DealCase(
    sale=Sale(
        currency=Currency.USD,
        amount=decimal_from_widget(sale_amount),
        payment_method=PaymentMethod(payment_method_value),
        collection_day=int(collection_day),
    ),
    foreign_payables=(
        ForeignPayable(Currency.USD, decimal_from_widget(usd_payable_amount), int(usd_payable_day)),
        ForeignPayable(Currency.JPY, decimal_from_widget(jpy_payable_amount), int(jpy_payable_day)),
    ),
    krw_costs=(
        KrwCost(decimal_from_widget(advance_amount), int(advance_day)),
        KrwCost(decimal_from_widget(balance_amount), int(balance_day)),
        KrwCost(decimal_from_widget(logistics_amount), int(logistics_day)),
    ),
    available_cash_krw=decimal_from_widget(available_cash),
    annual_funding_rate=decimal_from_widget(funding_rate_percent) / Decimal("100"),
    target_margin=decimal_from_widget(target_margin_percent) / Decimal("100"),
)
fx = FxRates(decimal_from_widget(usd_krw), decimal_from_widget(jpy_krw))
base_result = evaluate_deal(deal, fx)

scenario_results = canonical_scenarios(deal, fx)
combined_result = scenario_results[Scenario.COMBINED]
rescue_analysis = analyze_deal_rescue(deal, fx)
company_liquidity_profile = None
company_funding_analysis = None
fx_treasury_analysis = None
bankers_usance_comparison = None
usd_stress_result = scenario_results[Scenario.USD_DOWN_5]
peak_point = max(
    base_result.funding.points,
    key=lambda point: -point.cumulative_deal_cash_krw,
)
zero_profit_threshold = None
target_threshold = None
try:
    zero_profit_threshold = solve_usd_krw_threshold(deal, fx, None)
    target_threshold = solve_usd_krw_threshold(deal, fx, deal.target_margin)
except ValueError:
    pass

if active_stage == "review":
    target_live_result.info(
        f"현재 마진 {percent(base_result.financing_adjusted_deal_margin)} · "
        f"목표 대비 {(base_result.financing_adjusted_deal_margin - deal.target_margin) * 100:+.2f}%p · "
        f"복합 악화 시 {percent(combined_result.financing_adjusted_deal_margin)}"
    )
    fx_live_result.info(
        f"현재 마진 {percent(base_result.financing_adjusted_deal_margin)} · "
        f"거래 단독 외부자금 {krw_consumer(base_result.funding.maximum_external_borrowing_krw)} · "
        f"목표 유지선 {f'{target_threshold:,.2f}원' if target_threshold is not None else '계산 불가'}"
    )
    collection_live_result.caption(
        f"거래 단독 외부자금 {krw_consumer(base_result.funding.maximum_external_borrowing_krw)} · 피크 D+{peak_point.day}"
    )

deal_primary_slot = st.empty()
deal_primary_context = deal_primary_slot.container()
deal_primary_context.__enter__()
st.subheader("가정을 바꾸면 결과가 바로 달라집니다")
meets_target = base_result.financing_adjusted_deal_margin >= deal.target_margin
with st.container(border=True):
    st.badge("계산 결과", color="blue")
    st.markdown(
        "### 기본 거래 마진은 목표를 충족합니다."
        if meets_target
        else "### 현재 입력조건에서는 목표 마진에 미달합니다."
    )
    decision = st.columns([2, 1])
    decision[0].metric(
        "실제로 남는 마진",
        percent(base_result.financing_adjusted_deal_margin),
        help="금융비용 반영",
    )
    decision[1].metric("목표 마진", percent(deal.target_margin))
    if meets_target:
        st.success("✓ 목표 충족")
        st.caption("회사 전체 자금여력은 회사 자금 단계에서 확인합니다.")
    else:
        st.error("목표 미달")

st.markdown("### 거래 단독 계산")
signal_columns = st.columns(3)
with signal_columns[0].container(border=True):
    st.markdown("#### 달러가 어디까지 내려가면 위험할까요?")
    if target_threshold is None:
        st.markdown("### 현재 입력에서는 계산 불가")
    else:
        fx_buffer = fx.usd_krw - target_threshold
        st.metric("현재 분석 환율", f"{fx.usd_krw:,.0f}원")
        st.metric("목표마진 유지선", f"{target_threshold:,.2f}원")
        if fx_buffer >= 0:
            fx_buffer_ratio = fx_buffer / fx.usd_krw
            st.write(f"**현재 여유 {fx_buffer:,.2f}원 · {percent(fx_buffer_ratio)}**")
        else:
            st.write(f"**목표마진 유지선보다 {abs(fx_buffer):,.2f}원 낮음**")
    st.caption("환율 전망이 아니라 현재 계약이 목표 마진을 지킬 수 있는 기준점입니다.")
    usd_stress_meets_target = (
        usd_stress_result.financing_adjusted_deal_margin >= deal.target_margin
    )
    usd_stress_message = (
        f"달러 -5% Stress · {fx.usd_krw * Decimal('0.95'):,.0f}원 → "
        f"마진 {percent(usd_stress_result.financing_adjusted_deal_margin)} · "
        f"{'✓ 목표 충족' if usd_stress_meets_target else '목표 미달'}"
    )
    if usd_stress_meets_target:
        st.success(usd_stress_message)
    else:
        st.error(usd_stress_message)

with signal_columns[1].container(border=True):
    st.markdown("#### 최대로 빌려야 하는 돈")
    st.markdown(
        f'<div class="signal-number">'
        f'{krw_consumer(base_result.funding.maximum_external_borrowing_krw)}</div>',
        unsafe_allow_html=True,
    )
    st.write(f"돈이 가장 많이 필요한 시점  **D+{peak_point.day}**")
    st.caption(
        "거래에 가장 많이 필요한 돈 "
        f"{krw_consumer(base_result.funding.peak_deal_funding_krw)}"
    )

with signal_columns[2].container(border=True):
    combined_meets_target = (
        combined_result.financing_adjusted_deal_margin >= deal.target_margin
    )
    st.markdown("#### 조건이 동시에 나빠지면")
    st.markdown(
        f'<div class="signal-number">마진 '
        f'{percent(combined_result.financing_adjusted_deal_margin)}</div>',
        unsafe_allow_html=True,
    )
    st.error("목표 미달" if not combined_meets_target else "✓ 목표 충족")
    st.write("달러 -5% · 엔화 +10% · 금리 +1%p · 입금 +30일")
    st.caption("Stress 가정 · 미래 예측 아님")

deal_primary_context.__exit__(None, None, None)
if active_stage != "review":
    deal_primary_slot.empty()

document_slot = st.empty()
document_context = document_slot.container()
document_context.__enter__()
st.subheader("거래서류 불러오기")
st.caption("판매계약과 USD·JPY 공급자 PO를 읽습니다. 추출 후 확인한 값만 반영합니다.")
document_source = st.radio("문서 선택", ["샘플 거래 불러오기", "내 PDF 업로드"], horizontal=True, key="document_source")
uploaded_documents = []
if document_source == "내 PDF 업로드":
    st.caption("지원 역할: Sales Contract, USD Supplier PO, JPY Supplier PO · PDF별 10MB. Invoice 단독 입력은 지원하지 않습니다.")
    for role, label in zip(DEMO_PDF_PATHS, ("판매계약 PDF", "USD 공급자 PO PDF", "JPY 공급자 PO PDF")):
        uploaded_documents.append(st.file_uploader(label, type=["pdf"], key="trade_upload_" + role.stem))
        if uploaded_documents[-1] is not None:
            st.caption(f"{uploaded_documents[-1].name} → {role.name} 역할")
else:
    st.caption("샘플 문서는 모두 가상으로 생성된 데모 문서입니다.")
financialization = st.session_state.get("ai_financialization")
analysis_requested = False
if financialization is None:
    analysis_requested = st.button(
        "샘플 거래서류 3건 AI 분석" if document_source == "샘플 거래 불러오기" else "업로드한 거래서류 읽기",
        type="primary",
        key="analyze_demo_documents",
    )
else:
    st.success("AI 문서 분석 결과를 이 세션에서 재사용하고 있습니다.")
    analysis_requested = st.button("다시 AI 분석", key="reanalyze_demo_documents")

with st.expander("샘플 문서 보기"):
    document_columns = st.columns(3)
    document_labels = ("Sales Contract", "US Supplier PO", "Japan Supplier PO")
    for column, label, path in zip(document_columns, document_labels, DEMO_PDF_PATHS):
        with column:
            st.markdown(f"**{label}**")
            st.download_button(
                "PDF 보기 / 다운로드",
                data=path.read_bytes(),
                file_name=path.name,
                mime="application/pdf",
                key=f"download_{path.stem}",
            )
st.caption("AI 분석을 실행하면 해당 문서 내용이 설정된 AI API로 전송됩니다.")

if analysis_requested:
    if not os.environ.get("OPENAI_API_KEY"):
        st.session_state["ai_error"] = (
            "OPENAI_API_KEY가 없어 AI 문서 분석을 실행할 수 없습니다. "
            "기존 결정론적 거래 분석은 계속 사용할 수 있습니다."
        )
    else:
        with st.spinner("샘플 거래서류를 분석하고 있습니다..."):
            try:
                financialization = (
                    analyze_demo_documents(DEMO_PDF_PATHS)
                    if document_source == "샘플 거래 불러오기"
                    else analyze_uploaded_documents(uploaded_documents)
                )
            except FinancializationError:
                st.session_state["ai_error"] = (
                    "AI 문서 분석을 완료하지 못했습니다. 기존 거래 입력은 변경되지 않았습니다."
                )
            else:
                st.session_state["ai_financialization"] = financialization
                st.session_state["document_source_names"] = (
                    {path.name: path.name for path in DEMO_PDF_PATHS}
                    if document_source == "샘플 거래 불러오기" else
                    {path.name: item.name for path, item in zip(DEMO_PDF_PATHS, uploaded_documents)}
                )
                st.session_state.pop("ai_error", None)

if financialization is None and not os.environ.get("OPENAI_API_KEY"):
    st.info(
        "OPENAI_API_KEY가 설정되지 않아 AI 분석은 선택적으로 사용할 수 없습니다. "
        "현재 거래의 결정론적 분석에는 영향이 없습니다."
    )
if ai_error := st.session_state.get("ai_error"):
    st.warning(ai_error)

if financialization is not None:
    st.markdown("### AI가 이 거래의 돈 흐름을 정리했어요")
    st.badge("AI 문서 추출", color="violet")
    flow_columns = st.columns(2)
    with flow_columns[0].container(border=True):
        st.markdown("#### 받을 돈")
        for receivable in financialization.receivables:
            st.markdown(
                f"### {receivable.currency_code or '통화 미확인'} "
                f"{amount_text(receivable.amount)}"
            )
            st.write(timing_text(receivable.timing_anchor, receivable.timing_days))
            st.write(receivable.payment_method.value)
            st.caption(f"문서에서 추출 · {st.session_state.get('document_source_names', {}).get(receivable.source_filename, receivable.source_filename)}")
            st.caption(f"근거: {receivable.evidence}")
    with flow_columns[1].container(border=True):
        st.markdown("#### 먼저 나갈 돈")
        for payable in financialization.payables:
            st.markdown(
                f"### {payable.currency_code or '통화 미확인'} "
                f"{amount_text(payable.amount)}"
            )
            st.write(timing_text(payable.timing_anchor, payable.timing_days))
            st.caption(f"문서에서 추출 · {st.session_state.get('document_source_names', {}).get(payable.source_filename, payable.source_filename)}")
            st.caption(f"근거: {payable.evidence}")

    st.markdown("#### 환율에 노출된 돈")
    st.badge("계산 결과", color="blue")
    extraction_valid = True
    try:
        exposures = extracted_currency_exposure(financialization)
        unsupported = unsupported_currencies(financialization)
    except ValueError:
        extraction_valid = False
        exposures = {}
        unsupported = ()
        st.error("문서의 금액 또는 통화 형식을 확인해야 하므로 적용 제안을 만들 수 없습니다.")
    for currency, exposure in sorted(exposures.items()):
        receivable_total = sum(
            (
                normalize_amount(item.amount)
                for item in financialization.receivables
                if item.currency_code and item.currency_code.upper() == currency
            ),
            Decimal("0"),
        )
        payable_total = sum(
            (
                normalize_amount(item.amount)
                for item in financialization.payables
                if item.currency_code and item.currency_code.upper() == currency
            ),
            Decimal("0"),
        )
        direction = (
            "달러 가치가 떨어지면 불리합니다."
            if currency == "USD" and exposure > 0
            else "엔화 가치가 오르면 불리합니다."
            if currency == "JPY" and exposure < 0
            else "통화 방향별 영향을 별도로 확인해야 합니다."
        )
        st.write(
            f"**{currency}** · 받을 돈 {receivable_total:,.0f} · "
            f"낼 돈 {payable_total:,.0f} · 순노출 {exposure:+,.0f}"
        )
        st.caption(direction)

    if unsupported:
        extraction_valid = False
        st.error(
            "현재 MVP 계산 지원 통화는 KRW / USD / JPY입니다. "
            "지원되지 않는 금액을 제외한 불완전한 계산은 수행하지 않습니다. "
            f"확인된 미지원 통화: {', '.join(unsupported)}"
        )

    st.markdown("#### 회사에서 확인해주세요")
    st.write(
        "사내 가용자금 · 실제 차입금리 · 목표 마진 · 기존 환헤지 포지션 · "
        "국내 생산비와 물류·통관비"
    )
    st.caption("이 항목들은 문서 추출값으로 현재 거래 입력을 덮어쓰지 않습니다.")

    hedge_confirmation = False
    if financialization.hedge_status is HedgeStatus.NOT_FOUND:
        st.info("기존 환헤지 여부는 문서에서 확인되지 않았습니다.")
        hedge_confirmation = st.checkbox(
            "현재 이 거래에 별도로 반영해야 할 환헤지 포지션이 없음을 확인합니다.",
            key="ai_hedge_confirmation",
        )
        if hedge_confirmation:
            st.badge("사용자 확인", color="blue")
    else:
        extraction_valid = False
        st.error("환헤지 정보가 존재하거나 불명확하여 문서 제안을 거래에 반영할 수 없습니다.")

    st.info("문서의 회수 기산점은 D0와 자동 연결하지 않습니다. 판단 기준 단계에서 회수일을 확인하세요.")
    st.caption(
        "지급일 적용 규칙: 구매계약일을 현재 거래의 D+0으로 명시적으로 취급할 때만 "
        "CONTRACT_DATE +30을 D+30으로 제안합니다."
    )

    proposal = None
    day_zero_confirmed = document_source != "내 PDF 업로드" or st.checkbox(
        "공급자 계약일을 이 거래 검토의 D+0으로 적용함을 확인합니다.",
        key="uploaded_day_zero_confirmation",
    )
    if extraction_valid:
        try:
            proposal = build_proposed_deal_patch(
                financialization, contract_date_is_day_zero=day_zero_confirmed
            )
        except ProposalBlockedError as exc:
            st.error(f"문서 제안 적용 차단: {exc}")
    if proposal is not None:
        st.markdown("#### 거래 입력 변경 제안")
        proposed_changes = [
            f"USD 수출대금 → {proposal.sale_amount_usd:,.0f}",
            f"결제방식 → {proposal.payment_method.value}",
        ]
        if proposal.usd_payable_amount is not None:
            proposed_changes.append(f"USD 외화비용 → {proposal.usd_payable_amount:,.0f}")
        if proposal.usd_payable_day is not None:
            proposed_changes.append(f"USD 지급일 → D+{proposal.usd_payable_day}")
        if proposal.jpy_payable_amount is not None:
            proposed_changes.append(f"JPY 외화비용 → {proposal.jpy_payable_amount:,.0f}")
        if proposal.jpy_payable_day is not None:
            proposed_changes.append(f"JPY 지급일 → D+{proposal.jpy_payable_day}")
        for change in proposed_changes:
            st.write(f"- {change}")
        st.session_state["ai_proposed_patch"] = proposal
        st.button(
            "확인한 내용 거래에 반영",
            disabled=not hedge_confirmation,
            on_click=apply_ai_proposal,
            key="apply_ai_proposal",
        )
    if notice := st.session_state.pop("ai_apply_notice", None):
        st.success(notice)

document_ai_status = current_ai_provenance(
    st.session_state.get("ai_applied_patch"), deal
)
st.metric(
    "생성 기준",
    report_basis_text(document_ai_status, financialization is not None).replace("Deal", "거래"),
)
document_context.__exit__(None, None, None)
if active_stage != "deal" or input_mode != "거래서류 불러오기":
    document_slot.empty()

liquidity_profile_slot = st.empty()
liquidity_profile_context = liquidity_profile_slot.container()
liquidity_profile_context.__enter__()
st.subheader("회사 자금상태")
st.badge("재무제표 AI 인식", color="violet")
st.write(
    "재무제표에서 단기 유동성과 관련된 항목을 읽습니다. "
    "재무제표상 현금과 실제로 이 거래에 투입할 수 있는 자금은 다를 수 있습니다."
)
st.caption("가상 재무제표 · 실제 기업 자료 아님")
with st.expander("샘플 재무제표 보기"):
    st.download_button(
        "PDF 보기 / 다운로드",
        data=COMPANY_STATEMENT_PDF.read_bytes(),
        file_name=COMPANY_STATEMENT_PDF.name,
        mime="application/pdf",
        key="download_company_statement",
    )

statement_analysis = st.session_state.get("financial_statement_analysis")
if st.button("샘플 재무제표 읽기", type="primary", key="analyze_financial_statement"):
    if not os.environ.get("OPENAI_API_KEY"):
        st.session_state["financial_statement_error"] = (
            "OPENAI_API_KEY가 없어 재무제표를 읽을 수 없습니다."
        )
    else:
        with st.spinner("재무제표에서 회사 자금상태를 읽고 있습니다..."):
            try:
                statement_analysis = analyze_demo_financial_statement(
                    COMPANY_STATEMENT_PDF
                )
            except FinancialStatementError:
                st.session_state["financial_statement_error"] = (
                    "재무제표 분석을 완료하지 못했습니다."
                )
            else:
                st.session_state["financial_statement_analysis"] = statement_analysis
                st.session_state.pop("financial_statement_error", None)

if statement_error := st.session_state.get("financial_statement_error"):
    st.warning(statement_error)

if statement_analysis is not None:
    try:
        liquidity_profile = build_company_liquidity_profile(statement_analysis)
        company_liquidity_profile = liquidity_profile
    except ValueError:
        st.error("재무제표 금액 형식을 확인해야 합니다.")
    else:
        st.markdown("### 재무제표상 단기 유동성 항목")
        primary_profile = (
            ("현금 및 현금성자산", liquidity_profile.cash_and_cash_equivalents_krw),
            ("단기금융상품", liquidity_profile.short_term_financial_instruments_krw),
            ("유동자산", liquidity_profile.current_assets_krw),
            ("유동부채", liquidity_profile.current_liabilities_krw),
            ("단기차입금", liquidity_profile.short_term_borrowings_krw),
            ("영업활동현금흐름", liquidity_profile.operating_cash_flow_krw),
        )
        profile_columns = st.columns(3)
        for index, (label, value) in enumerate(primary_profile):
            profile_columns[index % 3].metric(label, optional_krw_consumer(value))

        with st.expander("기타 유동성 항목"):
            secondary_profile = st.columns(3)
            secondary_profile[0].metric(
                "매출채권", optional_krw_consumer(liquidity_profile.accounts_receivable_krw)
            )
            secondary_profile[1].metric(
                "재고자산", optional_krw_consumer(liquidity_profile.inventory_krw)
            )
            secondary_profile[2].metric(
                "금융비용", optional_krw_consumer(liquidity_profile.finance_cost_krw)
            )

        st.markdown("### 재무제표상 현금 ≠ 이 거래에 투입 가능한 자금")
        cash_boundary = st.columns(2)
        cash_boundary[0].metric(
            "재무제표상 현금 및 현금성자산",
            optional_krw_consumer(liquidity_profile.cash_and_cash_equivalents_krw),
        )
        cash_boundary[1].metric(
            "현재 거래 입력상 회사 투입가능자금",
            krw_consumer(deal.available_cash_krw),
        )
        st.info(
            "현재 거래 투입가능자금은 재무제표에서 자동 산정하지 않습니다. "
            "회사가 실제로 이 거래에 배정할 수 있는 금액을 사용자가 직접 확인합니다."
        )
liquidity_profile_context.__exit__(None, None, None)
if active_stage != "liquidity":
    liquidity_profile_slot.empty()

deal_risk_slot = st.empty()
deal_risk_context = deal_risk_slot.container()
deal_risk_context.__enter__()
stress_details = st.expander("복합 악화 시나리오·목표마진 충족 조건 상세")
stress_details.__enter__()
st.subheader("조건이 나빠지면 어떻게 될까요?")
st.badge("Stress 가정 · 미래 예측 아님", color="orange")
scenario_rows = []
for scenario, result in scenario_results.items():
    scenario_meets_target = result.financing_adjusted_deal_margin >= deal.target_margin
    scenario_rows.append(
        {
            "Scenario": scenario.value,
            "금융비용 반영 마진": percent(result.financing_adjusted_deal_margin),
            "목표 상태": "✓ 충족" if scenario_meets_target else "목표 미달",
            "최대 외부차입": krw_millions(result.funding.maximum_external_borrowing_krw),
            "금융비용": krw_millions(result.funding.external_funding_cost_krw),
            "결제일": f"D+{result.collection_day}",
        }
    )
scenario_labels = {
    Scenario.BASE: "현재 조건",
    Scenario.USD_DOWN_5: "달러 가치 -5%",
    Scenario.JPY_UP_10: "엔화 가치 +10%",
    Scenario.RATE_UP_1PP: "조달금리 +1%p",
    Scenario.DELAY_30D: "고객 입금 +30일",
    Scenario.COMBINED: "복합 악화 시나리오",
}
summary_columns = st.columns(3)
for index, (scenario, result) in enumerate(scenario_results.items()):
    scenario_meets_target = result.financing_adjusted_deal_margin >= deal.target_margin
    with summary_columns[index % 3].container(border=True):
        st.markdown(f"**{scenario_labels[scenario]}**")
        st.markdown(f"### {percent(result.financing_adjusted_deal_margin)}")
        st.write("✓ 목표 충족" if scenario_meets_target else "목표 미달")
with st.expander("상세 수치 보기"):
    st.dataframe(scenario_rows, hide_index=True, width="stretch")

st.subheader("이 거래를 목표 수준으로 만들려면?")
st.badge("목표마진 충족 조건 · 미래 예측 아님", color="orange")
if not rescue_analysis.needs_rescue:
    st.success(
        "현재 복합 악화 시나리오에서도 목표 마진을 충족합니다. "
        "추가 목표마진 충족 조건 계산이 필요하지 않습니다."
    )
else:
    st.markdown(
        f"복합 악화 시나리오에서는 실제로 남는 마진이 "
        f"{percent(rescue_analysis.baseline_margin)}로, "
        f"목표 {percent(rescue_analysis.target_margin)}에 미달합니다."
    )
    st.caption(
        "아래 값은 한 번에 한 조건만 바꿨을 때 목표마진을 다시 충족하는 "
        "경계값입니다."
    )
    rescue_options = {option.lever: option for option in rescue_analysis.options}
    rescue_cards = st.columns(3)
    sale_rescue = rescue_options[RescueLever.SALE_AMOUNT_USD]
    usd_cost_rescue = rescue_options[RescueLever.USD_PAYABLE_AMOUNT]
    jpy_cost_rescue = rescue_options[RescueLever.JPY_PAYABLE_AMOUNT]

    with rescue_cards[0].container(border=True):
        st.markdown("#### 수출가격 기준")
        st.write(f"현재  **USD {sale_rescue.current_value:,.0f}**")
        if sale_rescue.status is RescueStatus.FEASIBLE:
            sale_change = sale_rescue.threshold_value - sale_rescue.current_value
            sale_change_ratio = sale_change / sale_rescue.current_value
            st.metric(
                "목표마진 충족 기준",
                f"최소 USD {sale_rescue.threshold_value:,.0f}",
            )
            st.write(
                f"변화  **+USD {sale_change:,.0f} · "
                f"+{percent(sale_change_ratio)}**"
            )

    with rescue_cards[1].container(border=True):
        st.markdown("#### USD 원재료비 기준")
        st.write(f"현재  **USD {usd_cost_rescue.current_value:,.0f}**")
        if usd_cost_rescue.status is RescueStatus.FEASIBLE:
            usd_change = usd_cost_rescue.threshold_value - usd_cost_rescue.current_value
            usd_change_ratio = usd_change / usd_cost_rescue.current_value
            st.metric(
                "목표마진 충족 기준",
                f"최대 USD {usd_cost_rescue.threshold_value:,.0f}",
            )
            st.write(
                f"변화  **-USD {abs(usd_change):,.0f} · "
                f"{percent(usd_change_ratio)}**"
            )

    with rescue_cards[2].container(border=True):
        st.markdown("#### JPY 부품비 기준")
        st.write(f"현재  **JPY {jpy_cost_rescue.current_value:,.0f}**")
        if jpy_cost_rescue.status is RescueStatus.FEASIBLE:
            jpy_change = jpy_cost_rescue.threshold_value - jpy_cost_rescue.current_value
            jpy_change_ratio = jpy_change / jpy_cost_rescue.current_value
            st.metric(
                "목표마진 충족 기준",
                f"최대 JPY {jpy_cost_rescue.threshold_value:,.0f}",
            )
            st.write(
                f"변화  **-JPY {abs(jpy_change):,.0f} · "
                f"{percent(jpy_change_ratio)}**"
            )

    infeasible = {
        option.lever
        for option in rescue_analysis.options
        if option.status is RescueStatus.INFEASIBLE
    }
    if infeasible:
        st.markdown("#### 단독 변경만으로 목표마진을 회복하기 어려운 조건")
        if RescueLever.COLLECTION_DAY in infeasible:
            st.write(
                f"- 결제기간 단축만으로는 복합 악화 시나리오에서 목표 "
                f"{percent(deal.target_margin)} 회복 불가"
            )
        if RescueLever.FUNDING_RATE in infeasible:
            st.write(
                f"- 조달금리 인하만으로는 복합 악화 시나리오에서 목표 "
                f"{percent(deal.target_margin)} 회복 불가"
            )
    st.caption(
        "가격·원가·결제조건의 실제 협상 가능성을 판단하거나 계약 체결을 "
        "권고하는 기능이 아닙니다."
    )
stress_details.__exit__(None, None, None)
deal_risk_context.__exit__(None, None, None)
if active_stage != "review":
    deal_risk_slot.empty()


liquidity_stage_slot = st.empty()
liquidity_stage_context = liquidity_stage_slot.container()
liquidity_stage_context.__enter__()
st.subheader("회사 자금으로 대금 회수일까지 버틸 수 있을까요?")
st.badge("자금 수용력 · 승인 예측 아님", color="blue")
liquidity_metrics = st.columns(3)
liquidity_metrics[0].metric(
    "거래 최대 자금소요",
    krw_consumer(base_result.funding.peak_deal_funding_krw),
)
liquidity_metrics[1].metric(
    "이번 거래 투입 회사자금",
    krw_consumer(deal.available_cash_krw),
)
liquidity_metrics[2].metric(
    "추가 필요자금",
    krw_consumer(base_result.funding.maximum_external_borrowing_krw),
)
st.caption(f"자금 부담이 가장 큰 시점 D+{peak_point.day} · 거래별 배정 자금 기준")
liquidity_rows = [
    {
        "시점": f"D+{point.day}",
        "누적 거래 현금흐름 (KRW)": f"{point.cumulative_deal_cash_krw:,.0f}",
        "외부차입 잔액 (KRW)": f"{point.external_loan_outstanding_krw:,.0f}",
    }
    for point in base_result.funding.points
]
with st.expander("날짜별 현금흐름 상세 보기"):
    st.caption("결정론적 계산 엔진의 날짜별 자금 일정입니다.")
    st.dataframe(liquidity_rows, hide_index=True, width="stretch")

with credit_controls_slot.container():
    with input_group("기존 운전자금 한도", {"liquidity", "treasury"}, expanded=active_stage == "liquidity"):
        st.caption("사용자 입력 기존 한도 · 승인 예측 아님")
        credit_total = exact_input(
        "운전자금 한도 총액",
        min_value=0.0,
        value=100000000.0,
        step=1000000.0,
        key="credit_total_limit_input",
    )
        credit_used = exact_input(
        "현재 사용액",
        min_value=0.0,
        value=30000000.0,
        step=1000000.0,
        key="credit_used_amount_input",
    )
        credit_fee = exact_input(
        "이 거래에 추가로 발생하는 한도 수수료",
        min_value=0.0,
        value=0.0,
        step=100000.0,
        key="credit_deal_fee_input",
    )
credit_line = None
try:
    credit_line = WorkingCapitalCreditLine(
        total_limit_krw=decimal_from_widget(credit_total),
        used_amount_krw=decimal_from_widget(credit_used),
        deal_specific_fee_krw=decimal_from_widget(credit_fee),
    )
except ValueError:
    st.error("현재 사용액은 운전자금 한도 총액을 초과할 수 없습니다.")
else:
    st.metric("미사용 한도", krw_consumer(credit_line.unused_limit_krw))
st.caption("데모 입력 · 실제 은행 승인 또는 신용평가 결과 아님")
st.write("사용자가 입력한 기존 한도 기준이며 은행 승인 가능성을 예측하지 않습니다.")

st.subheader("회사의 실제 자금 흐름을 확인합니다")
st.badge("회사 유동성 Timeline · 현재 입력 기준", color="blue")
st.write(
    "기존 회사 일정 + 이번 거래 · CONFIRMED 기준"
)
st.caption(
    "D0는 현재 거래 검토 기준일입니다. 계약일·선적일·송장일을 자동으로 뜻하지 않습니다."
)
with input_group("회사 유동성 기준", {"liquidity"}):
    company_as_of_date = st.date_input(
    "거래 검토 기준일",
    value=date(2026, 9, 4),
    key="company_liquidity_as_of_date",
)
    company_current_cash = exact_input(
    "현재 가용현금",
    min_value=0.0,
    value=120000000.0,
    step=1000000.0,
    key="company_current_available_cash",
)
    company_minimum_cash = exact_input(
    "최소 운영자금",
    min_value=0.0,
    value=70000000.0,
    step=1000000.0,
    key="company_minimum_operating_cash",
)

if "company_cash_plan_rows" not in st.session_state:
    st.session_state["company_cash_plan_rows"] = [
        dict(row) for row in CANONICAL_COMPANY_CASH_PLAN_ROWS
    ]
if "company_cash_plan_editor_version" not in st.session_state:
    st.session_state["company_cash_plan_editor_version"] = 0

manual_tab, erp_tab = st.tabs(["직접 입력", "ERP 파일 가져오기"])
with manual_tab:
    st.caption("이번 거래를 제외한 기존 지급·수금만 입력합니다.")
    edited_company_rows = st.data_editor(
        st.session_state["company_cash_plan_rows"],
        num_rows="dynamic",
        hide_index=True,
        width="stretch",
        key=f"company_cash_plan_editor_{st.session_state['company_cash_plan_editor_version']}",
        column_config={
            "예정일": st.column_config.DateColumn("예정일", format="YYYY-MM-DD"),
            "구분": st.column_config.SelectboxColumn(
                "구분", options=[item.value for item in CompanyCashEventCategory]
            ),
            "금액 (KRW)": st.column_config.NumberColumn("금액 (KRW)", format="%.0f"),
            "상태": st.column_config.SelectboxColumn(
                "상태", options=[item.value for item in CompanyCashEventStatus]
            ),
            "출처": st.column_config.TextColumn("출처", disabled=True),
            "참조": st.column_config.TextColumn("참조"),
        },
    )
    st.session_state["company_cash_plan_rows"] = [
        dict(row) for row in edited_company_rows
    ]
with erp_tab:
    st.write("ERP 파일 가져오기")
    st.caption(
        "SAP S/4HANA, 더존 등 ERP에서 추출한 자금계획을 표준 형식으로 "
        "가져오는 MVP 입력 경로입니다. 실시간 ERP 연결이 아닙니다."
    )
    st.caption("가상·데모·fictional 자금계획이며 실제 기업 자료가 아닙니다.")
    st.download_button(
        "샘플 ERP CSV 받기",
        data=COMPANY_CASH_PLAN_CSV.read_bytes(),
        file_name=COMPANY_CASH_PLAN_CSV.name,
        mime="text/csv",
        key="download_company_cash_plan_csv",
    )
    uploaded_cash_plan = st.file_uploader(
        "표준 자금계획 CSV",
        type=["csv"],
        key="company_cash_plan_upload",
    )
    if st.button(
        "가져온 자금계획 반영",
        disabled=uploaded_cash_plan is None,
        key="apply_company_cash_plan_upload",
    ):
        try:
            imported_events = parse_company_cash_events_csv(
                uploaded_cash_plan.getvalue().decode("utf-8-sig")
            )
        except (UnicodeDecodeError, ValueError):
            st.session_state["company_cash_plan_import_message"] = (
                "표준 CSV 형식과 입력값을 확인해 주세요."
            )
        else:
            st.session_state["company_cash_plan_rows"] = company_cash_rows(imported_events)
            st.session_state["company_cash_plan_editor_version"] += 1
            st.session_state["company_cash_plan_import_message"] = (
                f"{len(imported_events)}개 자금계획을 가져왔습니다."
            )
            st.rerun()
    if import_message := st.session_state.get("company_cash_plan_import_message"):
        st.info(import_message)

include_expected_company_events = st.checkbox(
    "EXPECTED 자금계획 포함 시나리오 보기",
    value=False,
    key="include_expected_company_events",
)
st.caption(
    "기본 결과는 CONFIRMED만 포함합니다. EXPECTED는 선택할 때만 별도 입력 시나리오로 포함됩니다."
)

company_liquidity_comparison = None
company_credit_capacity = None
experience_data = None
try:
    company_cash_events = company_cash_events_from_rows(edited_company_rows)
    company_liquidity_input = CompanyLiquidityInput(
        as_of_date=company_as_of_date,
        current_available_cash_krw=decimal_from_widget(company_current_cash),
        minimum_operating_cash_krw=decimal_from_widget(company_minimum_cash),
        existing_cash_events=company_cash_events,
        include_expected_events=include_expected_company_events,
    )
    company_liquidity_comparison = analyze_company_liquidity(
        liquidity_input=company_liquidity_input,
        deal=deal,
        fx=fx,
    )
    if credit_line is not None:
        company_credit_capacity = compare_company_gap_to_credit_line(
            company_liquidity_comparison.company_with_deal,
            credit_line,
        )
except (TypeError, ValueError):
    st.warning("회사 자금계획의 날짜, 구분, 금액, 상태와 참조를 확인해 주세요.")
else:
    raw_buffer = company_liquidity_input.raw_starting_liquidity_after_buffer_krw
    company_summary = st.columns(3)
    company_summary[0].metric("현재 가용현금", krw_consumer(company_liquidity_input.current_available_cash_krw))
    company_summary[1].metric("최소 운영자금", krw_consumer(company_liquidity_input.minimum_operating_cash_krw))
    company_summary[2].metric("현재 Buffer 초과 유동성", signed_krw_consumer(raw_buffer))

    comparison_metrics = st.columns(3)
    comparison_metrics[0].metric(
        "거래만 본 필요 은행자금",
        krw_consumer(base_result.funding.maximum_external_borrowing_krw),
    )
    comparison_metrics[1].metric(
        "회사 기존 자금계획까지 포함한 필요 은행자금",
        krw_consumer(company_liquidity_comparison.company_with_deal.peak_liquidity_gap_krw),
    )
    comparison_metrics[2].metric(
        "현재 미사용 운전자금 한도",
        krw_consumer(credit_line.unused_limit_krw) if credit_line is not None else "입력 확인 필요",
    )
    company_with_deal = company_liquidity_comparison.company_with_deal
    st.write(
        f"회사 자체 계획만 보면 최대 부족은 "
        f"**{krw_consumer(company_liquidity_comparison.company_without_deal.peak_liquidity_gap_krw)}**, "
        f"Deal 포함 최대 부족은 **{krw_consumer(company_with_deal.peak_liquidity_gap_krw)}**입니다."
    )
    if company_credit_capacity is not None:
        if company_credit_capacity.feasible:
            st.success(
                "현재 입력 기준 한도 내 · 한도 여유 "
                f"{krw_consumer(company_credit_capacity.credit_headroom_krw)}"
            )
        else:
            st.error(
                "현재 입력 한도 초과 · 한도 부족 "
                f"{krw_consumer(company_credit_capacity.liquidity_gap_krw)}"
            )

    margin_status = "success" if meets_target else "danger"
    remaining_gap_status = (
        "success" if company_credit_capacity and company_credit_capacity.feasible else "danger"
    )
    remaining_gap_value = (
        company_credit_capacity.liquidity_gap_krw
        if company_credit_capacity is not None
        else company_with_deal.peak_liquidity_gap_krw
    )
    remaining_gap_detail = (
        "현재 입력 한도 내"
        if company_credit_capacity and company_credit_capacity.feasible
        else f"{krw_consumer(remaining_gap_value)} 부족"
    )
    experience_data = build_experience_data(
                margin=percent(base_result.financing_adjusted_deal_margin),
                margin_detail=("목표 충족" if meets_target else "목표 미달"),
                margin_status=margin_status,
                deal_funding=krw_consumer(
                    base_result.funding.maximum_external_borrowing_krw
                ),
                company_peak_gap=krw_consumer(company_with_deal.peak_liquidity_gap_krw),
                company_peak_detail=(
                    f"Peak {company_with_deal.peak_liquidity_gap_date.isoformat()}"
                ),
                remaining_gap=krw_consumer(remaining_gap_value),
                remaining_gap_detail=remaining_gap_detail,
                remaining_gap_status=remaining_gap_status,
            )
    st.caption(
        "Deal-level 배정자금과 Company-wide 현금 포지션은 서로 다른 입력입니다. "
        "재무제표상 현금도 현재 가용현금을 자동 설정하지 않습니다."
    )
    timeline_rows = [
        {
            "날짜": point.event_date.isoformat(),
            "시점": f"D+{point.day_offset}",
            "회사 기존 흐름": f"{point.existing_company_cashflow_krw:,.0f}",
            "Deal 흐름": f"{point.prospective_deal_cashflow_krw:,.0f}",
            "예상 가용현금": f"{point.cumulative_available_liquidity_krw:,.0f}",
            "최소 운영자금": f"{point.minimum_cash_buffer_krw:,.0f}",
            "유동성 부족": f"{point.required_external_funding_krw:,.0f}",
        }
        for point in company_with_deal.points
    ]
    st.markdown(
        f"**최대 유동성 부족일**  {company_with_deal.peak_liquidity_gap_date.isoformat()} "
        f"(D+{(company_with_deal.peak_liquidity_gap_date - company_as_of_date).days})"
    )
    chart_rows = [
        {"날짜": point.event_date.isoformat(), "구분": label,
         "현금 (KRW)": float(point.cumulative_available_liquidity_krw)}
        for label, timeline in (("회사 기존 계획", company_liquidity_comparison.company_without_deal),
                                ("이번 거래 포함", company_with_deal))
        for point in timeline.points
    ]
    # Hold each already-computed ending balance through the common display horizon.
    timelines = (company_liquidity_comparison.company_without_deal, company_with_deal)
    chart_end = max(timeline.points[-1].event_date for timeline in timelines)
    for label, timeline in zip(("회사 기존 계획", "이번 거래 포함"), timelines):
        if timeline.points[-1].event_date < chart_end:
            chart_rows.append({"날짜": chart_end.isoformat(), "구분": label,
                               "현금 (KRW)": float(timeline.ending_projected_cash_krw)})
    chart_rows += [
        {"날짜": point.event_date.isoformat(), "구분": "최소 운영자금",
         "현금 (KRW)": float(point.minimum_cash_buffer_krw)}
        for point in company_with_deal.points
    ]
    st.vega_lite_chart(chart_rows, {
        "mark": {"type": "line", "interpolate": "step-after", "point": True},
        "encoding": {
            "x": {"field": "날짜", "type": "temporal", "axis": {"format": "%m/%d", "title": "날짜"}},
            "y": {"field": "현금 (KRW)", "type": "quantitative", "axis": {"format": "~s"}},
            "color": {"field": "구분", "type": "nominal", "legend": {"orient": "bottom", "columns": 1}},
            "tooltip": [{"field": "날짜", "type": "temporal"}, {"field": "구분"}, {"field": "현금 (KRW)", "format": ",.0f"}],
        }, "height": 280,
    }, use_container_width=True)
    with st.expander("날짜별 현금과 지급·수금 내역"):
        st.dataframe(timeline_rows, hide_index=True, width="stretch")
        st.dataframe(company_cash_rows(company_cash_events), hide_index=True, width="stretch")

if experience_data is None:
    experience_data = build_experience_data(
        margin=percent(base_result.financing_adjusted_deal_margin),
        margin_detail="목표 충족" if meets_target else "목표 미달",
        margin_status="success" if meets_target else "danger",
        deal_funding=krw_consumer(base_result.funding.maximum_external_borrowing_krw),
        company_peak_gap="입력 확인 필요",
        company_peak_detail="회사 자금계획을 확인해 주세요",
        remaining_gap="입력 확인 필요",
        remaining_gap_detail="현재 한도 비교 불가",
        remaining_gap_status="warning",
    )
liquidity_stage_context.__exit__(None, None, None)
if active_stage != "liquidity":
    liquidity_stage_slot.empty()

treasury_stage_slot = st.empty()
treasury_stage_context = treasury_stage_slot.container()
treasury_stage_context.__enter__()
credit_tab, receivable_tab, forward_tab, usance_tab = st.tabs(["기존 운전자금", "매출채권 조기 현금화", "선물환 시뮬레이션", "Banker's Usance"])
credit_tab.__enter__()
if credit_line is not None:
    capacity_analysis = analyze_company_funding(
        deal=deal,
        base_result=base_result,
        combined_result=combined_result,
        credit_line=credit_line,
        purchase_result=None,
    )
    capacity_columns = st.columns(2)
    for column, title, capacity, stressed in (
        (capacity_columns[0], "거래 단독 · 현재 조건", capacity_analysis.base_capacity, False),
        (capacity_columns[1], "거래 단독 · 복합 악화 시", capacity_analysis.combined_capacity, True),
    ):
        with column.container(border=True):
            st.markdown(f"#### {title}")
            if stressed:
                st.badge("Stress 가정 · 승인 예측 아님", color="orange")
            st.write(f"**필요 은행자금**  {krw_consumer(capacity.required_external_funding_krw)}")
            st.write(f"**미사용 한도**  {krw_consumer(capacity.unused_credit_limit_krw)}")
            if capacity.feasible:
                st.success(
                    f"현재 입력 기준 한도 내 · 한도 여유 {krw_consumer(capacity.credit_headroom_krw)}"
                )
            else:
                st.error(
                    f"현재 입력 한도 초과 · 한도 부족 {krw_consumer(capacity.liquidity_gap_krw)}"
                )

credit_tab.__exit__(None, None, None)
receivable_tab.__enter__()
st.subheader("매출채권 조기 현금화")
st.badge("조건 비교 · 금융 실행 아님", color="blue")
purchase_result = None
if deal.sale.payment_method is PaymentMethod.TT:
    st.info("EARLY_RECEIVABLE_PURCHASE는 v0.1에서 O/A 매출채권에만 적용됩니다.")
else:
    default_purchase = canonical_purchase_option()
    with st.expander("매출채권 현금화 조건", expanded=True):
        purchase_day = scenario_input("매입일 (D+)", key="receivable_purchase_day_input", value=default_purchase.purchase_day, min_value=0, max_value=365, step=1)
        discount_rate_percent = exact_input("연 할인율 (%)", min_value=0.0, value=float(default_purchase.annual_discount_rate * 100), step=0.1, key="receivable_discount_rate_input")
        fee_rate_percent = exact_input("수수료율 (%)", min_value=0.0, value=float(default_purchase.fee_rate * 100), step=0.05, key="receivable_fee_rate_input")
    purchase_option = ReceivablePurchaseOption(
        purchase_day=int(purchase_day),
        annual_discount_rate=decimal_from_widget(discount_rate_percent) / Decimal("100"),
        fee_rate=decimal_from_widget(fee_rate_percent) / Decimal("100"),
    )
    try:
        purchase_result = evaluate_deal(deal, fx, purchase_option=purchase_option)
    except ValueError as exc:
        st.warning(f"입력값을 확인해 주세요: {exc}")

if credit_line is not None:
    funding_analysis = analyze_company_funding(
        deal=deal,
        base_result=base_result,
        combined_result=combined_result,
        credit_line=credit_line,
        purchase_result=purchase_result,
    )
    company_funding_analysis = funding_analysis
    choices = {item.choice: item for item in funding_analysis.choices}
    funding_details = st.expander("자금조달별 상세 조건")
    funding_details.__enter__()
    choice_columns = st.columns(3)
    choice_specs = (
        (FundingChoice.INTERNAL_CASH_ONLY, "회사자금만으로 기다리기"),
        (
            FundingChoice.WAIT_WITH_CREDIT_LINE,
            f"D+{base_result.collection_day}에 입금받기 · 기존 운전자금 한도",
        ),
        (FundingChoice.EARLY_RECEIVABLE_PURCHASE, "매출채권 먼저 현금화하기"),
    )
    for column, (choice_name, title) in zip(choice_columns, choice_specs):
        choice = choices[choice_name]
        with column.container(border=True):
            st.markdown(f"#### {title}")
            if choice.status is FundingChoiceStatus.FEASIBLE:
                st.success("거래 단독 기준 현재 입력 한도 내")
            elif choice.status is FundingChoiceStatus.INFEASIBLE:
                st.error("거래 단독 기준 자금 부족")
            else:
                st.info("현재 결제방식에는 적용 안 됨")
            if choice.status is not FundingChoiceStatus.NOT_APPLICABLE:
                st.write(f"**최대 은행 필요액**  {krw_consumer(choice.required_external_funding_krw)}")
                if choice.liquidity_gap_krw > 0:
                    st.write(f"**부족**  {krw_consumer(choice.liquidity_gap_krw)}")
                elif choice_name is not FundingChoice.INTERNAL_CASH_ONLY:
                    st.write(f"**한도 여유**  {krw_consumer(choice.credit_headroom_krw)}")
                cost = (
                    "산정하지 않음"
                    if choice.total_financing_cost_krw is None
                    else krw_consumer(choice.total_financing_cost_krw)
                )
                st.write(f"**금융비용**  {cost}")
                st.write(f"**현금 유입일**  D+{choice.cash_inflow_day}")
                if choice_name is FundingChoice.EARLY_RECEIVABLE_PURCHASE and purchase_result is not None:
                    purchase = purchase_result.receivable_purchase
                    st.write(f"**할인비용**  {krw_consumer(purchase.discount_cost_krw)}")
                    st.write(f"**매입수수료**  {krw_consumer(purchase.purchase_fee_krw)}")

    funding_details.__exit__(None, None, None)
    early = choices[FundingChoice.EARLY_RECEIVABLE_PURCHASE]
    wait = choices[FundingChoice.WAIT_WITH_CREDIT_LINE]
    if purchase_result is not None and purchase_result.receivable_purchase is not None:
        compare_values("현금 유입일 · 현재 → 조기 현금화 → 변화",
                       f"D+{base_result.collection_day}", f"D+{purchase_result.receivable_purchase.purchase_day}",
                       f"{purchase_result.receivable_purchase.purchase_day - base_result.collection_day:+}일")
        compare_values("거래 단독 최대 외부자금",
                       krw_consumer(wait.required_external_funding_krw),
                       krw_consumer(early.required_external_funding_krw),
                       signed_krw_consumer(early.required_external_funding_krw - wait.required_external_funding_krw))
        if early.total_financing_cost_krw is not None and wait.total_financing_cost_krw is not None:
            compare_values("금융·거래 비용",
                           krw_ten_thousands(wait.total_financing_cost_krw),
                           krw_ten_thousands(early.total_financing_cost_krw),
                           krw_ten_thousands(early.total_financing_cost_krw - wait.total_financing_cost_krw, signed=True))
        compare_values("거래 마진",
                       percent(base_result.financing_adjusted_deal_margin),
                       percent(purchase_result.financing_adjusted_deal_margin),
                       f"{(purchase_result.financing_adjusted_deal_margin - base_result.financing_adjusted_deal_margin) * 100:+.2f}%p")
    if (
        purchase_result is not None
        and purchase_result.receivable_purchase is not None
        and purchase_result.receivable_purchase.purchase_day > peak_point.day
        and early.required_external_funding_krw == wait.required_external_funding_krw
    ):
        st.info(
            f"이 거래에서는 최대 자금부족이 D+{peak_point.day}에 발생하고 "
            f"매출채권 현금화는 D+{purchase_result.receivable_purchase.purchase_day}이므로, "
            "조기현금화가 최대 필요 한도를 줄이지는 않습니다. "
            "대신 현금 유입을 앞당겨 차입기간을 줄입니다."
        )
    else:
        st.info("현금 유입 시점, 최대 은행 필요액과 금융비용을 함께 비교합니다.")
    st.caption(
        "T2의 추가 한도 수수료는 자금조달 비교 비용에 포함되며 "
        "기존 Deal Margin 엔진에는 자동 반영하지 않습니다."
    )

receivable_tab.__exit__(None, None, None)
usance_tab.__enter__()
st.subheader("수입대금 지급을 은행 신용으로 늦춰보면?")
st.badge("Banker's Usance 시뮬레이션 · 승인/실행 아님", color="blue")
st.write(
    "은행이 공급자에게 먼저 지급하고 회사가 만기에 은행에 상환하는 "
    "자금조달 가정입니다."
)
payable_labels = tuple(
    f"{payable.currency.value} {payable.amount:,.0f} · 공급자 지급 D+{payable.payment_day}"
    for payable in deal.foreign_payables
)
default_usance_index = next(
    (
        index
        for index, payable in enumerate(deal.foreign_payables)
        if payable.currency is Currency.JPY
    ),
    0,
)
with st.expander("Banker's Usance 조건", expanded=True):
    selected_payable_label = st.selectbox(
        "대상 외화 지급",
        payable_labels,
        index=default_usance_index,
        key="usance_payable_input",
    )
    selected_payable_index = payable_labels.index(selected_payable_label)
    selected_payable = deal.foreign_payables[selected_payable_index]
    usance_repayment_day = scenario_input("회사 상환일 (D+)", key="usance_repayment_day_input", value=max(90, selected_payable.payment_day + 1), min_value=selected_payable.payment_day + 1, max_value=max(365, selected_payable.payment_day + 2), step=1)
    usance_rate_percent = exact_input(
        "Usance 연 금리 (%)",
        min_value=0.0,
        value=4.8,
        step=0.1,
        key="usance_rate_input",
    )
    usance_fee_percent = exact_input(
        "Usance 수수료율 (%)",
        min_value=0.0,
        value=0.15,
        step=0.05,
        key="usance_fee_input",
    )
st.caption("데모 입력 · 실제 은행 Usance 승인·한도·quote 아님")

if credit_line is not None:
    usance_comparison = analyze_bankers_usance(
        deal=deal,
        fx=fx,
        base_result=base_result,
        credit_line=credit_line,
        usance_input=BankersUsanceInput(
            payable_index=selected_payable_index,
            repayment_day=int(usance_repayment_day),
            annual_usance_rate=decimal_from_widget(usance_rate_percent)
            / Decimal("100"),
            fee_rate=decimal_from_widget(usance_fee_percent) / Decimal("100"),
        ),
    )
    bankers_usance_comparison = usance_comparison
    usance = usance_comparison.usance
    compare_values("일반 운전자금 · 현재 → Usance → 변화",
                   krw_consumer(usance_comparison.base_working_capital_credit_krw),
                   krw_consumer(usance.peak_working_capital_credit_krw),
                   signed_krw_consumer(-usance_comparison.working_capital_credit_reduction_krw))
    compare_values("은행 신용 원금 기준 피크",
                   krw_consumer(usance_comparison.base_working_capital_credit_krw),
                   krw_consumer(usance.peak_combined_bank_principal_krw),
                   signed_krw_consumer(usance.peak_combined_bank_principal_krw - usance_comparison.base_working_capital_credit_krw))
    compare_values("총 금융비용",
                   krw_ten_thousands(usance_comparison.base_total_financing_cost_krw),
                   krw_ten_thousands(usance.total_financing_cost_krw),
                   krw_ten_thousands(usance_comparison.financing_cost_difference_krw, signed=True))
    usance_details = st.expander("Usance 원금·이자·수수료 상세")
    usance_details.__enter__()
    usance_columns = st.columns(2)
    with usance_columns[0].container(border=True):
        st.markdown("#### 현재 지급구조")
        st.write(f"**공급자 지급**  D+{usance.supplier_payment_day}")
        st.write(
            f"**일반 운전자금 피크**  "
            f"{krw_consumer(usance_comparison.base_working_capital_credit_krw)}"
        )
        st.write(
            f"**일반 운전자금 한도 여유**  "
            f"{krw_consumer(usance_comparison.base_ordinary_line_headroom_krw)}"
        )
        st.write(
            f"**일반 운전자금 이자**  "
            f"약 {krw_ten_thousands(base_result.funding.external_funding_cost_krw)}"
        )
        st.write(
            f"**총 금융비용**  약 "
            f"{krw_ten_thousands(usance_comparison.base_total_financing_cost_krw)}"
        )
    with usance_columns[1].container(border=True):
        st.markdown("#### Banker's Usance 가정")
        st.write(f"**은행 → 공급자**  D+{usance.supplier_payment_day}")
        st.write(f"**회사 → 은행**  D+{usance.company_repayment_day}")
        st.write(f"**Usance 원금**  {krw_consumer(usance.principal_krw)}")
        st.write(
            f"**일반 운전자금 피크**  "
            f"{krw_consumer(usance.peak_working_capital_credit_krw)}"
        )
        st.write(
            f"**일반 운전자금 한도 여유**  "
            f"{krw_consumer(usance.ordinary_line_headroom_krw)}"
        )
        st.write(f"**Usance 이자**  약 {krw_ten_thousands(usance.usance_interest_krw)}")
        st.write(f"**Usance 수수료**  {krw_ten_thousands(usance.usance_fee_krw)}")
        st.write(f"**총 금융비용**  약 {krw_ten_thousands(usance.total_financing_cost_krw)}")

    st.markdown("#### 일반 운전자금 한도 부담")
    burden_columns = st.columns(3)
    burden_columns[0].metric(
        "현재", krw_consumer(usance_comparison.base_working_capital_credit_krw)
    )
    burden_columns[1].metric(
        "Usance", krw_consumer(usance.peak_working_capital_credit_krw)
    )
    burden_columns[2].metric(
        "감소", krw_consumer(usance_comparison.working_capital_credit_reduction_krw)
    )
    st.markdown("#### 은행 신용 원금 기준 피크")
    exposure_columns = st.columns(2)
    exposure_columns[0].metric(
        "현재 구조", krw_consumer(usance_comparison.base_working_capital_credit_krw)
    )
    exposure_columns[1].metric(
        "Usance 구조", krw_consumer(usance.peak_combined_bank_principal_krw)
    )
    st.write("일반 운전자금 한도 사용은 줄지만, 동일 금액의 Usance 은행채무가 별도로 생깁니다.")
    st.write(
        f"**총 금융비용 차이**  "
        f"{signed_krw_consumer(usance_comparison.financing_cost_difference_krw)}"
    )
    if (
        usance_comparison.working_capital_credit_reduction_krw > 0
        and usance_comparison.financing_cost_difference_krw == usance.usance_fee_krw
    ):
        st.info(
            "현재 입력에서는 일반 운전자금 한도 부담은 줄고, "
            "금융비용은 수수료만큼 증가합니다."
        )
    else:
        st.info("현재 입력에 따른 일반 운전자금 부담과 총 금융비용을 함께 비교합니다.")

    usance_details.__exit__(None, None, None)
st.caption("일반 한도 부담은 줄어도 Usance 은행채무가 별도로 남습니다. 승인·실행은 포함하지 않습니다.")
st.caption(
    "지급시점이 늦어져도 환위험이 자동으로 없어지는 것은 아닙니다. "
    "실제 만기 상환통화와 환율고정 조건은 은행 계약조건 확인이 필요합니다."
)
st.caption(
    "Usance는 자금조달 시점을 바꾸는 기능이며, "
    "환율위험은 선물환 시뮬레이션 탭에서 별도로 확인합니다."
)

usance_tab.__exit__(None, None, None)
forward_tab.__enter__()
st.subheader("외화는 어느 방향으로 위험할까요?")
st.badge("통화별 결정론적 노출", color="blue")
st.write(
    "같은 통화의 받을 돈과 낼 돈을 금액 기준으로 상계합니다. "
    "지급일과 수취일이 다르면 시점 위험은 별도로 남습니다."
)
fx_positions = build_currency_exposure_positions(deal)
position_columns = st.columns(2)
for column, position in zip(position_columns, fx_positions):
    currency = position.currency.value
    with column.container(border=True):
        st.markdown(f"#### {currency} 노출")
        st.write(f"**받을 외화**  {currency} {position.receivable_amount:,.0f}")
        st.write(f"**지급할 외화**  {currency} {position.payable_amount:,.0f}")
        st.write(f"**통화 기준 상계 가능액**  {currency} {position.amount_offset:,.0f}")
        if position.direction is FxExposureDirection.RECEIVABLE:
            st.write(f"**순수취 노출**  {currency} {position.open_exposure:,.0f}")
            st.warning(f"불리한 방향: {currency}/KRW 하락")
        elif position.direction is FxExposureDirection.PAYABLE:
            st.write(f"**순지급 노출**  {currency} {position.open_exposure:,.0f}")
            st.warning(f"불리한 방향: {currency}/KRW 상승")
        else:
            st.write("**순노출**  없음")
            st.info("불리한 방향: 없음")

usd_position = fx_positions[0]
usd_payment_days = tuple(
    payable.payment_day
    for payable in deal.foreign_payables
    if payable.currency is Currency.USD and payable.amount > 0
)
if (
    usd_position.amount_offset > 0
    and deal.sale.currency is Currency.USD
    and usd_payment_days
    and any(day != deal.sale.collection_day for day in usd_payment_days)
):
    st.caption(
        f"USD 지급 D+{min(usd_payment_days)} · 수취 D+{deal.sale.collection_day} — "
        "금액은 상계되지만 시점은 다릅니다."
    )

st.subheader("환율을 열어둘까, 일부 고정할까?")
st.badge("선물환 시뮬레이션 · 실행 아님", color="orange")
st.caption(
    "기존 복합 악화 시나리오는 계약 전체 가정이고, 아래 선물환 비교는 사용자가 입력한 "
    "정산환율 기준입니다."
)
with st.expander("외환 / 선물환 조건", expanded=True):
    usd_forward = exact_input(
        "USD 선물환 매도환율",
        min_value=0.01,
        value=1395.0,
        step=1.0,
        key="usd_forward_quote_input",
    )
    usd_hedge_percent = scenario_input("USD 헤지비율 (%)", key="usd_hedge_ratio_input", value=80.0, min_value=0.0, max_value=100.0, step=1.0)
    jpy_forward = exact_input(
        "JPY 선물환 매수환율 (100 JPY)",
        min_value=0.01,
        value=905.0,
        step=1.0,
        key="jpy_forward_quote_input",
    )
    jpy_hedge_percent = scenario_input("JPY 헤지비율 (%)", key="jpy_hedge_ratio_input", value=80.0, min_value=0.0, max_value=100.0, step=1.0)
    settlement_usd = scenario_input("정산 시 가정 USD/KRW", key="settlement_usd_krw_input", value=1330.0, min_value=500.0, max_value=2500.0, step=1.0)
    settlement_jpy = scenario_input("정산 시 가정 JPY/KRW (100 JPY)", key="settlement_jpy_krw_input", value=990.0, min_value=300.0, max_value=2000.0, step=1.0)
st.caption("데모 가정 · 실제 은행 선물환 quote 아님 · 정산환율은 미래 예측 아님")

fx_treasury = analyze_fx_treasury(
    deal=deal,
    current_fx=fx,
    settlement_fx=FxRates(
        usd_krw=decimal_from_widget(settlement_usd),
        jpy_krw_per_100=decimal_from_widget(settlement_jpy),
    ),
    hedge_inputs=(
        ForwardHedgeInput(
            Currency.USD,
            decimal_from_widget(usd_hedge_percent) / Decimal("100"),
            decimal_from_widget(usd_forward),
        ),
        ForwardHedgeInput(
            Currency.JPY,
            decimal_from_widget(jpy_hedge_percent) / Decimal("100"),
            decimal_from_widget(jpy_forward),
        ),
    ),
)
fx_treasury_analysis = fx_treasury
hedge_columns = st.columns(2)
for column, hedge in zip(hedge_columns, fx_treasury.settlement_scenario_hedges):
    currency = hedge.currency.value
    action = {
        ForwardAction.SELL: "선물환 매도 시뮬레이션",
        ForwardAction.BUY: "선물환 매수 시뮬레이션",
        ForwardAction.NONE: "선물환 방향 없음",
    }[hedge.action]
    with column.container(border=True):
        st.markdown(f"#### {currency} 일부 고정")
        st.write(f"**열린 노출**  {currency} {hedge.open_exposure:,.0f}")
        st.write(f"**고정한 금액**  {currency} {hedge.hedged_notional:,.0f}")
        st.write(f"**남은 노출**  {currency} {hedge.residual_exposure:,.0f}")
        st.write(f"**방향**  {action}")

comparison_columns = st.columns(2)
for column, title, overlay in (
    (
        comparison_columns[0],
        "현재 환율이 유지되는 경우",
        fx_treasury.current_spot_overlay,
    ),
    (
        comparison_columns[1],
        "사용자가 입력한 가정환율",
        fx_treasury.settlement_scenario_overlay,
    ),
):
    meets_overlay_target = overlay.simulated_margin_after_hedge >= deal.target_margin
    with column.container(border=True):
        st.markdown(f"#### {title}")
        st.write(f"**헤지 전 마진**  {percent(overlay.unhedged_margin)}")
        st.write(f"**선물환 overlay 마진**  {percent(overlay.simulated_margin_after_hedge)}")
        st.write(f"**선물환 정산효과**  {signed_krw_consumer(overlay.hedge_effect_krw)}")
        st.write(f"**목표마진**  {percent(deal.target_margin)}")
        if meets_overlay_target:
            st.success("현재 입력 기준 · ✓ 목표 충족")
        else:
            st.error("현재 입력 기준 · 목표 미달")
st.caption(
    "선물환 정산효과는 거래손익 비교에 반영하며, "
    "파생상품 정산에 따른 차입일정 재계산은 포함하지 않습니다."
)
forward_tab.__exit__(None, None, None)
treasury_stage_context.__exit__(None, None, None)
if active_stage != "treasury":
    treasury_stage_slot.empty()

review_context_slot = st.empty()
review_context_container = review_context_slot.container()
review_context_container.__enter__()
st.subheader("공식 시장 참고정보")
st.write(
    "공식 데이터는 명시적으로 불러옵니다. K-SURE 정보는 참고 Context로만 "
    "사용되며 거래조건이나 결제일을 자동으로 변경하지 않습니다."
)
with st.container(border=True):
    st.markdown("#### 미국 기계업종의 실제 결제 참고정보")
    st.badge("공식 데이터", color="green")
    st.warning("국가·업종 집계 · 개별 바이어 예측 아님")
    st.write(
        "**결제완료 건 기준 집계 · 개별 바이어의 연체확률이나 "
        "신용점수가 아닙니다.**"
    )
    st.caption("미국 · 기타 기계 및 장비 제조업 · 출처: K-SURE")
    if st.button("K-SURE 결제정보 불러오기"):
        if not os.environ.get("KSURE_SERVICE_KEY"):
            st.session_state["ksure_load_message"] = (
                "KSURE_SERVICE_KEY가 없어 공식 결제정보를 불러올 수 없습니다."
            )
        else:
            try:
                context = fetch_payment_context("450", "29")
            except KsurePaymentError:
                st.session_state["ksure_payment_context"] = None
                st.session_state["ksure_load_message"] = (
                    "K-SURE 결제정보를 불러오지 못했습니다."
                )
            else:
                st.session_state["ksure_payment_context"] = context
                st.session_state["ksure_load_message"] = (
                    "해당 조회 조건의 K-SURE 결제정보가 없습니다."
                    if context is None
                    else "K-SURE 결제정보를 불러왔습니다."
                )
    if message := st.session_state.get("ksure_load_message"):
        st.info(message)
    if context := st.session_state.get("ksure_payment_context"):
        context_metrics = st.columns(3)
        context_metrics[0].metric(
            "평균 결제기간",
            decimal_text(context.average_payment_period_days, "일"),
        )
        context_metrics[1].metric(
            "지연결제율", decimal_text(context.late_payment_rate_percent, "%")
        )
        context_metrics[2].metric(
            "평균 지연기간",
            decimal_text(context.average_late_payment_period_days, "일"),
        )
        st.caption(
            f"기준년도 {context.reference_year} · 최종갱신 "
            f"{context.last_update_date.isoformat()} · 출처: K-SURE"
        )
        if context.payment_terms or context.payment_period_distribution:
            with st.expander("결제조건·기간 분포 상세"):
                if context.payment_terms:
                    st.dataframe(
                        [
                            {
                                "결제조건": share.name,
                                "비중": decimal_text(share.percent, "%"),
                                "관측수": share.observation_count,
                            }
                            for share in context.payment_terms
                        ],
                        hide_index=True,
                        width="stretch",
                    )
                if context.payment_period_distribution:
                    st.dataframe(
                        [
                            {
                                "결제기간": share.name,
                                "비중": decimal_text(share.percent, "%"),
                                "관측수": share.observation_count,
                            }
                            for share in context.payment_period_distribution
                        ],
                        hide_index=True,
                        width="stretch",
                    )
        st.info("K-SURE 집계정보는 현재 거래의 결제일을 자동으로 변경하지 않습니다.")
review_context_container.__exit__(None, None, None)
if active_stage != "result":
    review_context_slot.empty()

current_payment_context = st.session_state.get("ksure_payment_context")
treasury_review_context = TreasuryReviewContext(
    company_liquidity=company_liquidity_profile,
    company_funding=company_funding_analysis,
    fx_treasury=fx_treasury_analysis,
    bankers_usance=bankers_usance_comparison,
    company_cash_timeline=company_liquidity_comparison,
    company_cash_capacity=company_credit_capacity,
)

default_review_question = REVIEW_GOAL_QUESTIONS["overall"]
custom_review_question = st.session_state.get("custom_deal_review_question", "")
if active_stage == "result":
    st.subheader("거래 검토 요약")
    st.write("현재 거래와 결정론적 근거를 읽고 검토 포인트를 정리합니다.")
    with st.expander("질문 직접 수정"):
        custom_review_question = st.text_area(
            "검토 질문",
            value=custom_review_question,
            max_chars=400,
            key="custom_deal_review_question",
            placeholder=default_review_question,
        )
review_question = custom_review_question.strip() or default_review_question
treasury_review_ready = all(
    analysis is not None
    for analysis in (
        company_funding_analysis,
        fx_treasury_analysis,
        bankers_usance_comparison,
        company_liquidity_comparison,
        company_credit_capacity,
    )
)
if active_stage == "result" and not treasury_review_ready:
    st.warning(
        "현재 Treasury 입력으로 결정론적 분석을 완성할 수 없습니다. "
        "회사 자금계획·자금조달·외화위험·Usance 입력을 먼저 확인해 주세요."
    )

stored_review_run = st.session_state.get("deal_review_run")
stored_review_current = bool(
    stored_review_run is not None
    and is_current_deal_review(
        stored_review_run,
        review_question,
        deal,
        fx,
        treasury_review_context,
        current_payment_context,
    )
)
tool_labels = {
    "read_current_deal_analysis": "현재 거래 분석",
    "read_stress_and_rescue": "Stress / 목표마진 충족 조건",
    "read_treasury_context": "회사 자금 / 자금조달 / 외화위험",
    "read_payment_context": "K-SURE 결제 참고정보",
}
if experience_data is not None:
    stage_states = {
        "deal": "complete",
        "liquidity": "complete" if company_liquidity_comparison is not None else "ready",
        "treasury": "complete" if treasury_review_ready else "ready",
        "review": "ready",
        "result": "ready",
    }
    experience_data["stages"] = [
        {**stage, "state": stage_states[stage["id"]]}
        for stage in experience_data["stages"]
    ]
    experience_data["reviewState"] = {
        "ready": treasury_review_ready,
        "hasResult": stored_review_run is not None,
        "current": stored_review_current,
        "headline": stored_review_run.memo.headline if stored_review_current else None,
        "summary": stored_review_run.memo.summary if stored_review_current else None,
        "usedTools": [tool_labels[name] for name in stored_review_run.used_tools] if stored_review_current else [],
        "error": st.session_state.get("deal_review_error"),
    }
    experience_data["snapshot"].extend([
        {"label": "목표 마진", "value": percent(deal.target_margin), "detail": "사용자 기준", "status": "neutral"},
        {"label": "현재 미사용 한도", "value": krw_consumer(credit_line.unused_limit_krw) if credit_line else "입력 확인 필요", "detail": "기존 운전자금", "status": "neutral"},
        {"label": "복합 악화 시 마진", "value": percent(combined_result.financing_adjusted_deal_margin), "detail": "현재 가정 기준", "status": "neutral"},
    ])
    experience_data["snapshot"] = [experience_data["snapshot"][i] for i in (0, 4, 1, 2, 5, 3, 6)]
    with experience_shell_slot.container():
        component_result = trade_treasury_experience(experience_data)
else:
    component_result = None

if isinstance(component_result, dict):
    primary_action = component_result.get("primary_action")
else:
    primary_action = getattr(component_result, "primary_action", None)
if primary_action is None:
    persisted_experience = st.session_state.get("trade_treasury_experience", {})
    if isinstance(persisted_experience, dict):
        primary_action = persisted_experience.get("primary_action")
    else:
        primary_action = getattr(persisted_experience, "primary_action", None)
if primary_action == "run_review" and treasury_review_ready:
    persisted_experience = st.session_state.get("trade_treasury_experience")
    if hasattr(persisted_experience, "pop"):
        persisted_experience.pop("primary_action", None)
    with st.spinner("현재 거래 근거를 읽고 검토하고 있습니다..."):
        try:
            review_run = run_deal_review(
                review_question,
                deal=deal,
                fx=fx,
                base_result=base_result,
                scenario_results=tuple(scenario_results.items()),
                zero_profit_threshold=zero_profit_threshold,
                target_margin_threshold=target_threshold,
                rescue_analysis=rescue_analysis,
                treasury_context=treasury_review_context,
                payment_context=current_payment_context,
            )
        except DealReviewError:
            st.session_state["deal_review_error"] = (
                "AI 거래 검토를 완료하지 못했습니다."
            )
            st.rerun()
        else:
            st.session_state["deal_review_run"] = review_run
            st.session_state.pop("deal_review_error", None)
            st.rerun()

if active_stage == "result" and (
    review_error := st.session_state.get("deal_review_error")
):
    st.warning(review_error)

review_run = st.session_state.get("deal_review_run")
review_is_current = False
if review_run is not None:
    review_is_current = is_current_deal_review(
        review_run,
        review_question,
        deal,
        fx,
        treasury_review_context,
        current_payment_context,
    )
    if not review_is_current:
        st.warning(
            "현재 거래 입력 또는 공식 Context가 변경되어 기존 AI 검토는 현재 "
            "상태와 일치하지 않습니다. 다시 생성해 주세요."
        )
    elif active_stage == "result":
        memo = review_run.memo
        review_details = st.expander("검토 근거·계약조건 상세")
        review_details.__enter__()
        st.markdown(f"### {memo.headline}")
        st.write(memo.summary)
        display_signals = (
            memo.treasury_focus,
            *memo.supporting_signals,
        )
        options = rescue_option_map(rescue_analysis)
        for index, signal in enumerate(display_signals):
            if index == 0:
                st.markdown("#### 먼저 확인할 Treasury 이슈")
            elif index == 1:
                st.markdown("#### 함께 본 근거")
            with st.container(border=True):
                if signal is SupportingSignal.CURRENT_MARGIN:
                    st.markdown("**현재 마진**")
                    st.write(
                        f"{percent(base_result.financing_adjusted_deal_margin)} · "
                        f"{'✓ 목표 충족' if meets_target else '목표 미달'}"
                    )
                elif signal is SupportingSignal.FX_RESILIENCE:
                    st.markdown("**USD/KRW 목표마진 유지선**")
                    if target_threshold is None:
                        st.write("현재 입력에서는 계산 불가")
                    else:
                        buffer = fx.usd_krw - target_threshold
                        st.write(
                            f"현재 {fx.usd_krw:,.2f}원 · 유지선 "
                            f"{target_threshold:,.2f}원 · 차이 {buffer:+,.2f}원"
                        )
                elif signal is SupportingSignal.FUNDING_BURDEN:
                    st.markdown("**자금 부담**")
                    st.write(
                        f"최대 자금소요 {krw_consumer(base_result.funding.peak_deal_funding_krw)}"
                        f" · 최대 외부차입 {krw_consumer(base_result.funding.maximum_external_borrowing_krw)}"
                    )
                elif signal is SupportingSignal.COMBINED_STRESS:
                    combined_meets = (
                        combined_result.financing_adjusted_deal_margin
                        >= deal.target_margin
                    )
                    st.markdown("**복합 악화 시나리오**")
                    st.write(
                        f"마진 {percent(combined_result.financing_adjusted_deal_margin)} · "
                        f"{'✓ 목표 충족' if combined_meets else '목표 미달'}"
                    )
                elif signal is TreasuryFocus.CREDIT_LINE_CAPACITY:
                    funding = treasury_review_context.company_funding
                    st.markdown("**회사 전체 유동성과 운전자금 한도**")
                    timeline = treasury_review_context.company_cash_timeline
                    capacity = treasury_review_context.company_cash_capacity
                    if timeline is not None and capacity is not None:
                        peak = timeline.company_with_deal
                        st.write(
                            f"회사 전체 Peak 부족 {krw_consumer(peak.peak_liquidity_gap_krw)} · "
                            f"{peak.peak_liquidity_gap_date.isoformat()} / "
                            f"D+{next(point.day_offset for point in peak.points if point.event_date == peak.peak_liquidity_gap_date)}"
                        )
                        st.write(
                            f"미사용 한도 {krw_consumer(capacity.unused_credit_limit_krw)} · "
                            f"적용 후 잔여 부족 {krw_consumer(capacity.liquidity_gap_krw)}"
                        )
                    for label, capacity in (
                        ("현재", funding.base_capacity),
                        ("복합 악화 시나리오", funding.combined_capacity),
                    ):
                        status = "한도 내" if capacity.feasible else "한도 초과"
                        balance_label = "여유" if capacity.feasible else "부족"
                        balance = (
                            capacity.credit_headroom_krw
                            if capacity.feasible
                            else capacity.liquidity_gap_krw
                        )
                        st.write(
                            f"{label}: 필요 {krw_consumer(capacity.required_external_funding_krw)} · "
                            f"미사용 {krw_consumer(capacity.unused_credit_limit_krw)} · "
                            f"{balance_label} {krw_consumer(balance)} · {status}"
                        )
                elif signal is TreasuryFocus.FUNDING_OPTIONS:
                    st.markdown("**자금조달 비교**")
                    funding = treasury_review_context.company_funding
                    funding_labels = {
                        FundingChoice.INTERNAL_CASH_ONLY: "회사자금만",
                        FundingChoice.WAIT_WITH_CREDIT_LINE: "기존 운전자금 한도",
                        FundingChoice.EARLY_RECEIVABLE_PURCHASE: "매출채권 조기현금화",
                    }
                    for choice in funding.choices:
                        cost = (
                            "산정하지 않음"
                            if choice.total_financing_cost_krw is None
                            else krw_consumer(choice.total_financing_cost_krw)
                        )
                        inflow = (
                            "해당 없음"
                            if choice.cash_inflow_day is None
                            else f"D+{choice.cash_inflow_day}"
                        )
                        st.write(
                            f"{funding_labels[choice.choice]} · {choice.status.value} · "
                            f"필요 {krw_consumer(choice.required_external_funding_krw)} · "
                            f"비용 {cost} · 현금유입 {inflow}"
                        )
                elif signal is TreasuryFocus.FX_EXPOSURE:
                    st.markdown("**통화별 외화노출**")
                    for position in treasury_review_context.fx_treasury.positions:
                        st.write(
                            f"{position.currency.value}: 순노출 {position.net_exposure:+,.0f} · "
                            f"금액 기준 상계 {position.amount_offset:,.0f} · "
                            f"불리한 방향 {position.unfavorable_direction.value}"
                        )
                    st.caption("금액 기준 상계와 지급·수취 시점 일치는 다릅니다.")
                elif signal is TreasuryFocus.FORWARD_HEDGE:
                    analysis = treasury_review_context.fx_treasury
                    st.markdown("**선물환 시뮬레이션**")
                    for hedge in analysis.settlement_scenario_hedges:
                        st.write(
                            f"{hedge.currency.value}: 고정 {hedge.hedged_notional:,.0f} · "
                            f"잔여 {hedge.residual_exposure:,.0f}"
                        )
                    overlay = analysis.settlement_scenario_overlay
                    st.write(
                        f"사용자 정산환율 가정 · 헤지 전 {percent(overlay.unhedged_margin)} · "
                        f"overlay {percent(overlay.simulated_margin_after_hedge)} · "
                        f"효과 {signed_krw_consumer(overlay.hedge_effect_krw)} · "
                        f"{'✓ 목표 충족' if overlay.simulated_margin_after_hedge >= deal.target_margin else '목표 미달'}"
                    )
                elif signal is TreasuryFocus.BANKERS_USANCE:
                    comparison = treasury_review_context.bankers_usance
                    usance = comparison.usance
                    st.markdown("**Banker's Usance**")
                    st.write(
                        f"{usance.currency.value} {usance.principal_fcy:,.0f} · "
                        f"공급자 D+{usance.supplier_payment_day} · 회사 D+{usance.company_repayment_day}"
                    )
                    st.write(
                        f"일반 운전자금 {krw_consumer(comparison.base_working_capital_credit_krw)}"
                        f" → {krw_consumer(usance.peak_working_capital_credit_krw)} · "
                        f"감소 {krw_consumer(comparison.working_capital_credit_reduction_krw)}"
                    )
                    st.write(
                        f"은행 신용 원금 피크 {krw_consumer(usance.peak_combined_bank_principal_krw)} · "
                        f"금융비용 차이 {signed_krw_consumer(comparison.financing_cost_difference_krw)}"
                    )
                    st.caption("일반 운전자금 사용 감소와 총 은행 원금 감소는 같은 의미가 아닙니다.")
                else:
                    signal_levers = {
                        SupportingSignal.SALE_PRICE_BOUNDARY: RescueLever.SALE_AMOUNT_USD,
                        SupportingSignal.USD_COST_BOUNDARY: RescueLever.USD_PAYABLE_AMOUNT,
                        SupportingSignal.JPY_COST_BOUNDARY: RescueLever.JPY_PAYABLE_AMOUNT,
                        SupportingSignal.COLLECTION_DAY_BOUNDARY: RescueLever.COLLECTION_DAY,
                        SupportingSignal.FUNDING_RATE_BOUNDARY: RescueLever.FUNDING_RATE,
                    }
                    lever = signal_levers[signal]
                    if lever in options:
                        render_rescue_option(options[lever])
                    else:
                        st.write("현재 시나리오에서는 추가 목표마진 충족 조건 계산이 필요하지 않습니다.")

        if memo.negotiation_focus:
            st.markdown("#### AI가 설명 대상으로 선택한 계약조건")
            for lever in memo.negotiation_focus:
                if lever in options:
                    render_rescue_option(options[lever])
                else:
                    st.write("현재 시나리오에서는 추가 목표마진 충족 조건 계산이 필요하지 않습니다.")

        if treasury_review_context.company_liquidity is not None:
            profile = treasury_review_context.company_liquidity
            st.markdown("#### 회사 자금 맥락")
            with st.container(border=True):
                st.write(
                    "재무제표상 현금 및 현금성자산 "
                    f"{optional_krw_consumer(profile.cash_and_cash_equivalents_krw)} · "
                    f"이번 거래 투입가능 회사자금 {krw_consumer(deal.available_cash_krw)}"
                )
                st.write(
                    f"단기차입금 {optional_krw_consumer(profile.short_term_borrowings_krw)} · "
                    "영업활동현금흐름 "
                    f"{optional_krw_consumer(profile.operating_cash_flow_krw)}"
                )
                st.caption("재무제표상 현금은 Deal 투입가능자금과 동일하지 않습니다.")

        if current_payment_context is not None:
            st.markdown("#### 공식 결제 참고정보")
            st.warning("국가·업종 집계 · 개별 바이어 예측 아님")
            st.write(
                "평균 결제기간 "
                f"{decimal_text(current_payment_context.average_payment_period_days, '일')} · "
                "지연결제율 "
                f"{decimal_text(current_payment_context.late_payment_rate_percent, '%')} · "
                "평균 지연기간 "
                f"{decimal_text(current_payment_context.average_late_payment_period_days, '일')}"
            )

        st.markdown("#### 사용한 분석 도구")
        for tool_name in review_run.used_tools:
            label = tool_labels[tool_name]
            if tool_name == "read_payment_context" and current_payment_context is None:
                label += " · 불러온 공식 데이터 없음"
            st.write(f"✓ {label}")

        review_details.__exit__(None, None, None)
        with st.expander("분석 정보"):
            st.write(f"모델: {review_run.model}")
            st.write(f"요청 횟수: {review_run.request_count}")
            st.write("도구: " + ", ".join(review_run.used_tools))
            if review_run.usage is not None:
                st.write(
                    f"토큰: 입력 {review_run.usage.input_tokens:,} · "
                    f"출력 {review_run.usage.output_tokens:,} · "
                    f"합계 {review_run.usage.total_tokens:,}"
                )


ai_provenance_status = current_ai_provenance(
    st.session_state.get("ai_applied_patch"),
    deal,
)
report_basis = report_basis_text(
    ai_provenance_status,
    financialization is not None,
)
payment_context = st.session_state.get("ksure_payment_context")
official_context = official_context_text(
    fx_reference=None,
    payment_context=payment_context,
)
report_bytes = build_deal_report(
    DealReportInput(
        generated_at=datetime.now(ZoneInfo("Asia/Seoul")),
        deal=deal,
        base_result=base_result,
        scenario_results=tuple(scenario_results.items()),
        zero_profit_threshold=zero_profit_threshold,
        target_margin_threshold=target_threshold,
        purchase_result=purchase_result,
        payment_context=payment_context,
        ai_analysis_exists=financialization is not None,
        ai_provenance_status=ai_provenance_status,
        hedge_confirmed=bool(st.session_state.get("ai_hedge_confirmation")),
        company_liquidity_timeline=company_liquidity_comparison,
        company_liquidity_capacity=company_credit_capacity,
        treasury_confirmed_current_cash_krw=(
            company_liquidity_input.current_available_cash_krw
            if company_liquidity_comparison is not None else None
        ),
        minimum_operating_cash_krw=(
            company_liquidity_input.minimum_operating_cash_krw
            if company_liquidity_comparison is not None else None
        ),
        company_funding=company_funding_analysis,
        fx_treasury=fx_treasury_analysis,
        bankers_usance=bankers_usance_comparison,
        company_liquidity_includes_expected=bool(include_expected_company_events),
        review_memo=review_run.memo if review_is_current else None,
        review_used_tools=review_run.used_tools if review_is_current else (),
        review_is_current=review_is_current,
    )
)
if active_stage == "result":
    st.subheader("결과를 공유해야 하나요?")
    st.write("현재 입력 기준 계산과 현재 거래 검토를 최대 3페이지 보고서로 저장합니다.")
    report_preview = st.columns(3)
    report_preview[0].metric("현재 상태", "목표 충족" if meets_target else "목표 미달")
    report_preview[1].metric("생성 기준", report_basis.replace("Deal", "거래"))
    report_preview[2].metric("공식 데이터", official_context)
    st.download_button(
        "Treasury 사전점검 보고서 다운로드",
        data=report_bytes,
        file_name="trade-treasury-precheck-report.pdf",
        mime="application/pdf",
        type="primary",
        key="deal_report_download",
    )
    st.caption("현재 화면의 결정론적 분석 결과로 즉시 생성되며 서버에 저장되지 않습니다.")
