from datetime import datetime
from decimal import Decimal
import os
from pathlib import Path
from zoneinfo import ZoneInfo

import streamlit as st

from src.ai.deal_review import (
    DealReviewError,
    ReviewSignal,
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
from src.finance.rescue import (
    RescueLever,
    RescueStatus,
    analyze_deal_rescue,
)
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
    "이 거래의 주요 취약점과 목표마진을 지키기 위해 검토할 조건을 설명해줘."
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


reference = reference_deal()
reference_rates = reference_fx()
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

st.set_page_config(page_title="수출거래 사전점검", layout="wide")
st.markdown(f"<style>{APP_CSS}</style>", unsafe_allow_html=True)
st.markdown('<div class="product-label">AI TRADE FINANCE PRE-CHECK</div>', unsafe_allow_html=True)
st.title("수출거래 사전점검")
st.markdown(
    '<p class="product-lead">계약 전에 환율·입금 지연·금융비용이 바뀌어도<br>'
    '이 거래의 마진과 현금흐름이 버티는지 확인합니다.</p>',
    unsafe_allow_html=True,
)
st.caption("사전 의사결정 지원용 · 금융 실행, 환율 예측 또는 신용평가 서비스가 아닙니다.")

st.sidebar.header("거래 입력")
st.sidebar.badge("데모 가정", color="gray")
st.sidebar.caption("기준 거래값이 미리 입력되어 있으며 언제든 수정할 수 있습니다.")

with st.sidebar.expander("거래 조건", expanded=True):
    sale_amount = st.number_input(
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
    collection_day = st.number_input(
        "결제일 (D+)",
        min_value=0,
        step=1,
        key="collection_day_input",
    )

with st.sidebar.expander("비용 및 지급", expanded=False):
    usd_payable = reference.foreign_payables[0]
    jpy_payable = reference.foreign_payables[1]
    usd_payable_amount = st.number_input(
        "USD 외화비용",
        min_value=0.0,
        step=1000.0,
        key="usd_payable_amount_input",
    )
    usd_payable_day = st.number_input(
        "USD 지급일 (D+)",
        min_value=0,
        step=1,
        key="usd_payable_day_input",
    )
    jpy_payable_amount = st.number_input(
        "JPY 외화비용",
        min_value=0.0,
        step=100000.0,
        key="jpy_payable_amount_input",
    )
    jpy_payable_day = st.number_input(
        "JPY 지급일 (D+)",
        min_value=0,
        step=1,
        key="jpy_payable_day_input",
    )
    advance, balance, logistics = reference.krw_costs
    advance_amount = st.number_input(
        "국내 생산 선급금 (KRW)", min_value=0.0, value=float(advance.amount_krw), step=1000000.0
    )
    advance_day = st.number_input(
        "선급금 지급일 (D+)", min_value=0, value=advance.payment_day, step=1
    )
    balance_amount = st.number_input(
        "국내 생산 잔금 (KRW)", min_value=0.0, value=float(balance.amount_krw), step=1000000.0
    )
    balance_day = st.number_input(
        "잔금 지급일 (D+)", min_value=0, value=balance.payment_day, step=1
    )
    logistics_amount = st.number_input(
        "물류·통관비 (KRW)", min_value=0.0, value=float(logistics.amount_krw), step=1000000.0
    )
    logistics_day = st.number_input(
        "물류·통관비 지급일 (D+)", min_value=0, value=logistics.payment_day, step=1
    )

with st.sidebar.expander("자금 / 목표", expanded=True):
    available_cash = st.number_input(
        "사내 가용자금 (KRW)",
        min_value=0.0,
        value=float(reference.available_cash_krw),
        step=1000000.0,
    )
    funding_rate_percent = st.number_input(
        "실제 연 조달금리 (%)",
        min_value=0.0,
        value=float(reference.annual_funding_rate * Decimal("100")),
        step=0.1,
    )
    target_margin_percent = st.number_input(
        "목표 마진 (%)",
        min_value=0.0,
        value=float(reference.target_margin * Decimal("100")),
        step=0.1,
    )

with st.sidebar.expander("환율", expanded=True):
    usd_krw = st.number_input(
        "USD/KRW",
        min_value=0.01,
        value=float(reference_rates.usd_krw),
        step=1.0,
        key="usd_krw_input",
    )
    jpy_krw = st.number_input(
        "JPY/KRW per 100 JPY",
        min_value=0.01,
        value=float(reference_rates.jpy_krw_per_100),
        step=1.0,
        key="jpy_krw_input",
    )
    st.badge("사용자 입력", color="blue")
    st.caption("초기값은 데모 가정입니다. 공식 환율은 사용자가 적용할 때만 반영됩니다.")

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

st.subheader("이 거래, 현재 조건에서 버틸까요?")
meets_target = base_result.financing_adjusted_deal_margin >= deal.target_margin
with st.container(border=True):
    st.badge("계산 결과", color="blue")
    st.markdown(
        "### 현재 입력조건에서는 목표 마진을 지킵니다."
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
    else:
        st.error("목표 미달")

st.markdown("### 지금 확인할 세 가지")
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

st.subheader("거래서류로 자동 입력하기")
st.write(
    "샘플 계약서와 구매주문서를 AI가 읽어 받을 돈·낼 돈·통화·지급시점을 정리합니다."
)
st.caption("샘플 문서는 모두 가상으로 생성된 데모 문서입니다.")
financialization = st.session_state.get("ai_financialization")
analysis_requested = False
if financialization is None:
    analysis_requested = st.button(
        "샘플 거래서류 3건 AI 분석",
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
                financialization = analyze_demo_documents(DEMO_PDF_PATHS)
            except FinancializationError:
                st.session_state["ai_error"] = (
                    "AI 문서 분석을 완료하지 못했습니다. 기존 거래 입력은 변경되지 않았습니다."
                )
            else:
                st.session_state["ai_financialization"] = financialization
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
            st.caption(f"{receivable.source_filename}에서 확인")
            st.caption(f"근거: {receivable.evidence}")
    with flow_columns[1].container(border=True):
        st.markdown("#### 먼저 나갈 돈")
        for payable in financialization.payables:
            st.markdown(
                f"### {payable.currency_code or '통화 미확인'} "
                f"{amount_text(payable.amount)}"
            )
            st.write(timing_text(payable.timing_anchor, payable.timing_days))
            st.caption(f"{payable.source_filename}에서 확인")
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

    st.info("대금회수 조건: 선적 후 90일. 현재 거래의 D+N 기산점과 자동 연결하지 않았습니다.")
    st.caption(
        "지급일 적용 규칙: 구매계약일을 현재 거래의 D+0으로 명시적으로 취급할 때만 "
        "CONTRACT_DATE +30을 D+30으로 제안합니다."
    )

    proposal = None
    if extraction_valid:
        try:
            proposal = build_proposed_deal_patch(
                financialization, contract_date_is_day_zero=True
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
    Scenario.COMBINED: "복합 Stress",
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
st.badge("조건 역산 · 미래 예측 아님", color="orange")
if not rescue_analysis.needs_rescue:
    st.success(
        "현재 복합 Stress에서도 목표 마진을 충족합니다. "
        "추가 조건 역산이 필요하지 않습니다."
    )
else:
    st.markdown(
        f"복합 Stress에서는 실제로 남는 마진이 "
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
                f"- 결제기간 단축만으로는 복합 Stress에서 목표 "
                f"{percent(deal.target_margin)} 회복 불가"
            )
        if RescueLever.FUNDING_RATE in infeasible:
            st.write(
                f"- 조달금리 인하만으로는 복합 Stress에서 목표 "
                f"{percent(deal.target_margin)} 회복 불가"
            )
    st.caption(
        "가격·원가·결제조건의 실제 협상 가능성을 판단하거나 계약 체결을 "
        "권고하는 기능이 아닙니다."
    )

st.subheader("AI 거래 검토 에이전트")
st.badge("읽기 전용 · 금융계산은 결정론적 엔진", color="violet")
st.write(
    "AI가 현재 거래, Stress, 조건 역산과 이미 불러온 공식 Context를 "
    "도구로 읽고 검토 포인트를 정리합니다."
)
st.info("AI는 계산하지 않습니다. 검증된 계산 결과를 읽고 연결해 설명합니다.")
current_payment_context = st.session_state.get("ksure_payment_context")
st.markdown("#### 현재 Agent 근거")
st.write("- 현재 거래 분석")
st.write("- Stress / 조건 역산")
st.write(
    "- K-SURE Context: "
    + ("포함 가능" if current_payment_context is not None else "불러온 값 없음")
)
review_question = st.text_area(
    "검토 질문",
    value=DEAL_REVIEW_QUESTION,
    max_chars=400,
    key="deal_review_question",
)
if st.button("AI 거래 검토 실행", type="primary", key="run_deal_review"):
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
                payment_context=current_payment_context,
            )
        except DealReviewError:
            st.session_state["deal_review_error"] = (
                "AI 거래 검토를 완료하지 못했습니다."
            )
        else:
            st.session_state["deal_review_run"] = review_run
            st.session_state.pop("deal_review_error", None)

if review_error := st.session_state.get("deal_review_error"):
    st.warning(review_error)

review_run = st.session_state.get("deal_review_run")
if review_run is not None:
    review_is_current = is_current_deal_review(
        review_run,
        review_question,
        deal,
        fx,
        current_payment_context,
    )
    if not review_is_current:
        st.warning(
            "현재 거래 입력 또는 공식 Context가 변경되어 기존 AI 검토는 현재 "
            "상태와 일치하지 않습니다. 다시 생성해 주세요."
        )
    else:
        memo = review_run.memo
        st.markdown(f"### {memo.headline}")
        st.write(memo.summary)
        st.markdown("#### AI가 선택한 핵심 근거")
        options = rescue_option_map(rescue_analysis)
        for signal in memo.key_signals:
            with st.container(border=True):
                if signal is ReviewSignal.CURRENT_MARGIN:
                    st.markdown("**현재 마진**")
                    st.write(
                        f"{percent(base_result.financing_adjusted_deal_margin)} · "
                        f"{'✓ 목표 충족' if meets_target else '목표 미달'}"
                    )
                elif signal is ReviewSignal.FX_RESILIENCE:
                    st.markdown("**USD/KRW 목표마진 유지선**")
                    if target_threshold is None:
                        st.write("현재 입력에서는 계산 불가")
                    else:
                        buffer = fx.usd_krw - target_threshold
                        st.write(
                            f"현재 {fx.usd_krw:,.2f}원 · 유지선 "
                            f"{target_threshold:,.2f}원 · 차이 {buffer:+,.2f}원"
                        )
                elif signal is ReviewSignal.FUNDING_BURDEN:
                    st.markdown("**자금 부담**")
                    st.write(
                        f"최대 자금소요 {krw_consumer(base_result.funding.peak_deal_funding_krw)}"
                        f" · 최대 외부차입 {krw_consumer(base_result.funding.maximum_external_borrowing_krw)}"
                    )
                elif signal is ReviewSignal.COMBINED_STRESS:
                    combined_meets = (
                        combined_result.financing_adjusted_deal_margin
                        >= deal.target_margin
                    )
                    st.markdown("**복합 Stress**")
                    st.write(
                        f"마진 {percent(combined_result.financing_adjusted_deal_margin)} · "
                        f"{'✓ 목표 충족' if combined_meets else '목표 미달'}"
                    )
                elif signal is ReviewSignal.KSURE_PAYMENT_CONTEXT:
                    if current_payment_context is not None:
                        st.markdown("**K-SURE 결제 Context**")
                        st.write(
                            "평균 결제기간 "
                            f"{decimal_text(current_payment_context.average_payment_period_days, '일')} · "
                            "지연결제율 "
                            f"{decimal_text(current_payment_context.late_payment_rate_percent, '%')} · "
                            "평균 지연기간 "
                            f"{decimal_text(current_payment_context.average_late_payment_period_days, '일')}"
                        )
                else:
                    signal_levers = {
                        ReviewSignal.SALE_PRICE_BOUNDARY: RescueLever.SALE_AMOUNT_USD,
                        ReviewSignal.USD_COST_BOUNDARY: RescueLever.USD_PAYABLE_AMOUNT,
                        ReviewSignal.JPY_COST_BOUNDARY: RescueLever.JPY_PAYABLE_AMOUNT,
                        ReviewSignal.COLLECTION_DAY_BOUNDARY: RescueLever.COLLECTION_DAY,
                        ReviewSignal.FUNDING_RATE_BOUNDARY: RescueLever.FUNDING_RATE,
                    }
                    lever = signal_levers[signal]
                    if lever in options:
                        render_rescue_option(options[lever])
                    else:
                        st.write("현재 Stress에서는 추가 조건 역산이 필요하지 않습니다.")

        if memo.negotiation_focus:
            st.markdown("#### AI가 설명 대상으로 선택한 계약조건")
            for lever in memo.negotiation_focus:
                if lever in options:
                    render_rescue_option(options[lever])
                else:
                    st.write("현재 Stress에서는 추가 조건 역산이 필요하지 않습니다.")

        if current_payment_context is not None and memo.payment_context_note:
            st.markdown("#### K-SURE Context 해석")
            st.warning("국가·업종 집계 · 개별 바이어 예측 아님")
            st.write(memo.payment_context_note)

        st.markdown("#### 사용한 분석 도구")
        tool_labels = {
            "read_current_deal_analysis": "현재 거래 분석",
            "read_stress_and_rescue": "Stress / 조건 역산",
            "read_payment_context": "K-SURE Context 확인",
        }
        for tool_name in review_run.used_tools:
            label = tool_labels[tool_name]
            if tool_name == "read_payment_context" and current_payment_context is None:
                label += " · 불러온 공식 데이터 없음"
            st.write(f"✓ {label}")

        with st.expander("AI 실행 정보"):
            st.write(f"모델: {review_run.model}")
            st.write(f"요청 횟수: {review_run.request_count}")
            st.write("도구: " + ", ".join(review_run.used_tools))
            if review_run.usage is not None:
                st.write(
                    f"토큰: 입력 {review_run.usage.input_tokens:,} · "
                    f"출력 {review_run.usage.output_tokens:,} · "
                    f"합계 {review_run.usage.total_tokens:,}"
                )

st.subheader("돈은 언제 가장 많이 필요할까요?")
st.badge("계산 결과", color="blue")
st.markdown(f"**돈이 가장 많이 필요한 시점은 D+{peak_point.day}입니다.**")
liquidity_metrics = st.columns(2)
liquidity_metrics[0].metric(
    "거래에 가장 많이 필요한 돈",
    krw_consumer(base_result.funding.peak_deal_funding_krw),
)
liquidity_metrics[1].metric(
    "최대로 빌려야 하는 돈",
    krw_consumer(base_result.funding.maximum_external_borrowing_krw),
)
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

st.subheader("고객 입금일까지 기다릴까, 먼저 현금화할까?")
st.badge("계산 결과", color="blue")
purchase_result = None
if deal.sale.payment_method is PaymentMethod.TT:
    st.info("EARLY_RECEIVABLE_PURCHASE는 v0.1에서 O/A 매출채권에만 적용됩니다.")
else:
    default_purchase = canonical_purchase_option()
    purchase_columns = st.columns(3)
    purchase_day = purchase_columns[0].number_input(
        "매입일 (D+)", min_value=0, value=default_purchase.purchase_day, step=1
    )
    discount_rate_percent = purchase_columns[1].number_input(
        "연 할인율 (%)",
        min_value=0.0,
        value=float(default_purchase.annual_discount_rate * Decimal("100")),
        step=0.1,
    )
    fee_rate_percent = purchase_columns[2].number_input(
        "수수료율 (%)",
        min_value=0.0,
        value=float(default_purchase.fee_rate * Decimal("100")),
        step=0.05,
    )
    purchase_option = ReceivablePurchaseOption(
        purchase_day=int(purchase_day),
        annual_discount_rate=decimal_from_widget(discount_rate_percent) / Decimal("100"),
        fee_rate=decimal_from_widget(fee_rate_percent) / Decimal("100"),
    )
    try:
        purchase_result = evaluate_deal(deal, fx, purchase_option=purchase_option)
    except ValueError as exc:
        st.warning(f"입력값을 확인해 주세요: {exc}")
    else:
        purchase = purchase_result.receivable_purchase
        comparison_columns = st.columns(2)
        with comparison_columns[0].container(border=True):
            st.markdown(f"#### D+{base_result.collection_day}에 입금받기")
            st.metric(
                "실제로 남는 마진",
                percent(base_result.financing_adjusted_deal_margin),
            )
            st.write(
                f"**최대로 빌려야 하는 돈**  "
                f"{krw_consumer(base_result.funding.maximum_external_borrowing_krw)}"
            )
            st.write(
                f"**돈을 받기 전까지 드는 이자**  "
                f"{krw_consumer(base_result.funding.external_funding_cost_krw)}"
            )
            st.write("**조기 현금화 비용**  해당 없음")
            st.write(f"**현금 유입일**  D+{base_result.collection_day}")

        with comparison_columns[1].container(border=True):
            st.markdown("#### D+65에 먼저 현금화하기")
            st.metric(
                "실제로 남는 마진",
                percent(purchase_result.financing_adjusted_deal_margin),
            )
            st.write(
                f"**최대로 빌려야 하는 돈**  "
                f"{krw_consumer(purchase_result.funding.maximum_external_borrowing_krw)}"
            )
            st.write(
                f"**돈을 받기 전까지 드는 이자**  "
                f"{krw_consumer(purchase_result.funding.external_funding_cost_krw)}"
            )
            st.write(f"**할인비용**  {krw_consumer(purchase.discount_cost_krw)}")
            st.write(f"**수수료**  {krw_consumer(purchase.purchase_fee_krw)}")
            st.write(f"**현금화일**  D+{purchase.purchase_day}")

        st.info("판단 포인트: 빠른 유동성 확보와 명시적 매입·할인비용 간의 교환관계입니다.")

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

st.subheader("분석 근거")
evidence_columns = st.columns(3)
with evidence_columns[0].container(border=True):
    st.markdown("**계산 엔진**")
    st.write("마진·현금흐름·Stress를 결정론적으로 계산")
with evidence_columns[1].container(border=True):
    st.markdown("**AI 문서 추출**")
    st.write("계약서에서 금액·통화·지급시점만 추출")
with evidence_columns[2].container(border=True):
    st.markdown("**사용자 확인**")
    st.write("AI 값은 명시적 확인 후에만 거래에 반영")
evidence_columns = st.columns(2)
with evidence_columns[0].container(border=True):
    st.markdown("**공식 데이터**")
    st.write("K-SURE 결제 참고정보, 실제 불러온 경우만 표시")
with evidence_columns[1].container(border=True):
    st.markdown("**Stress 가정**")
    st.write("미래 예측이 아닌 조건 변화 시뮬레이션")

st.subheader("결과를 공유해야 하나요?")
st.write("현재 분석 결과를 2페이지 사전점검 보고서로 저장할 수 있습니다.")
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
report_preview = st.columns(3)
report_preview[0].metric("현재 상태", "목표 충족" if meets_target else "목표 미달")
report_preview[1].metric(
    "생성 기준",
    report_basis.replace("Deal", "거래"),
)
report_preview[2].metric(
    "공식 데이터",
    official_context,
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
    )
)
st.download_button(
    "거래 사전점검 보고서 다운로드",
    data=report_bytes,
    file_name="trade-finance-precheck-report.pdf",
    mime="application/pdf",
    type="primary",
    key="deal_report_download",
)
st.caption("현재 화면의 결정론적 분석 결과로 즉시 생성되며 서버에 저장되지 않습니다.")
