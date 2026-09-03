from datetime import date
from decimal import Decimal
import os
from pathlib import Path

import streamlit as st

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
from src.external.eximbank_fx import EximbankFxError, fetch_fx_reference
from src.external.ksure_payment import KsurePaymentError, fetch_payment_context
from src.finance.engine import (
    ReceivablePurchaseOption,
    Scenario,
    canonical_purchase_option,
    canonical_scenarios,
    evaluate_deal,
    solve_usd_krw_threshold,
)


APP_CSS = (Path(__file__).parent / "assets" / "app.css").read_text(encoding="utf-8")


def decimal_from_widget(value: int | float) -> Decimal:
    return Decimal(str(value))


def percent(value: Decimal) -> str:
    return f"{value * Decimal('100'):.2f}%"


def krw_millions(value: Decimal) -> str:
    return f"KRW {value / Decimal('1000000'):,.3f}M"


def decimal_text(value: Decimal | None, suffix: str = "") -> str:
    return "n/a" if value is None else f"{value}{suffix}"


def apply_loaded_fx() -> None:
    snapshot = st.session_state.get("fx_reference_snapshot")
    if snapshot is not None:
        st.session_state["usd_krw_input"] = float(snapshot.usd_krw)
        st.session_state["jpy_krw_input"] = float(snapshot.jpy_krw_per_100)
        st.session_state["fx_apply_notice"] = "Official reference FX applied to Deal inputs."


reference = reference_deal()
reference_rates = reference_fx()

st.set_page_config(page_title="AI Trade Finance Pre-check", layout="wide")
st.markdown(f"<style>{APP_CSS}</style>", unsafe_allow_html=True)
st.title("AI Trade Finance Pre-check")
st.write(
    "수출 Deal의 마진과 자금 부담을 계약 전에 점검하는 금융 의사결정 지원 서비스"
)
st.info(
    "사전 의사결정 지원용입니다. 은행 승인, 환율 예측, 신용점수 또는 금융 실행 서비스가 아닙니다."
)

st.sidebar.header("Deal 입력")
st.sidebar.badge("Demo assumption", color="gray")
st.sidebar.caption("기준 Deal 값이 미리 입력되어 있으며 언제든 수정할 수 있습니다.")

with st.sidebar.expander("거래 조건", expanded=True):
    sale_amount = st.number_input(
        "수출대금 (USD)",
        min_value=1.0,
        value=float(reference.sale.amount),
        step=1000.0,
        key="sale_amount_input",
    )
    payment_method_value = st.selectbox(
        "결제방식", [method.value for method in PaymentMethod], index=0
    )
    collection_day = st.number_input(
        "결제일 (D+)", min_value=0, value=reference.sale.collection_day, step=1
    )

with st.sidebar.expander("비용 및 지급", expanded=False):
    usd_payable = reference.foreign_payables[0]
    jpy_payable = reference.foreign_payables[1]
    usd_payable_amount = st.number_input(
        "USD 외화비용", min_value=0.0, value=float(usd_payable.amount), step=1000.0
    )
    usd_payable_day = st.number_input(
        "USD 지급일 (D+)", min_value=0, value=usd_payable.payment_day, step=1
    )
    jpy_payable_amount = st.number_input(
        "JPY 외화비용", min_value=0.0, value=float(jpy_payable.amount), step=100000.0
    )
    jpy_payable_day = st.number_input(
        "JPY 지급일 (D+)", min_value=0, value=jpy_payable.payment_day, step=1
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
        "목표 Deal Margin (%)",
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
    st.badge("User-entered fact", color="blue")
    st.caption("초기값은 Demo assumption입니다. 공식 환율은 사용자가 적용할 때만 반영됩니다.")

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

st.subheader("현재 Deal 판단")
st.badge("Calculated result", color="blue")
meets_target = base_result.financing_adjusted_deal_margin >= deal.target_margin
st.markdown(
    "### 현재 조건에서 목표 마진을 충족합니다."
    if meets_target
    else "### 현재 조건에서는 목표 마진에 미달합니다."
)
decision = st.columns([2, 1])
decision[0].metric(
    "금융비용 반영 Deal Margin",
    percent(base_result.financing_adjusted_deal_margin),
    border=True,
)
if meets_target:
    decision[1].success("✓ 목표 충족 · MEETS TARGET")
else:
    decision[1].error("목표 미달 · BELOW TARGET")

metrics = st.columns(3)
metrics[0].metric("목표 마진", percent(deal.target_margin))
metrics[1].metric("금융비용 반영 전 Deal Margin", percent(base_result.gross_deal_margin))
metrics[2].metric(
    "Deal 자금소요", krw_millions(base_result.funding.peak_deal_funding_krw)
)
metrics = st.columns(2)
metrics[0].metric(
    "최대 외부차입",
    krw_millions(base_result.funding.maximum_external_borrowing_krw),
)
metrics[1].metric(
    "외부 금융비용", krw_millions(base_result.funding.external_funding_cost_krw)
)

st.subheader("Stress Test")
st.badge("STRESS ASSUMPTION", color="orange")
st.caption("결과는 예측이 아닌 결정론적 Stress assumption입니다.")
scenario_rows = []
scenario_results = canonical_scenarios(deal, fx)
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
st.dataframe(scenario_rows, hide_index=True, width="stretch")
combined_result = scenario_results[Scenario.COMBINED]
combined_status = "목표 충족" if combined_result.financing_adjusted_deal_margin >= deal.target_margin else "목표 미달"
st.warning(
    f"복합 Stress: 금융비용 반영 Deal Margin "
    f"{percent(combined_result.financing_adjusted_deal_margin)} · {combined_status}"
)

st.subheader("Official Market Context")
st.caption("공식 데이터는 명시적으로 불러오고, Deal에는 사용자가 선택할 때만 반영됩니다.")
market_columns = st.columns(2)

with market_columns[0].container(border=True):
    st.markdown("#### 한국수출입은행 · 공식 기준환율")
    st.badge("Observed official data", color="green")
    reference_date = st.date_input("기준일", value=date.today())
    if st.button("공식 기준환율 불러오기"):
        if not os.environ.get("EXIMBANK_AUTH_KEY"):
            st.session_state["fx_load_message"] = (
                "EXIMBANK_AUTH_KEY가 없어 공식 환율을 불러올 수 없습니다."
            )
        else:
            try:
                snapshot = fetch_fx_reference(reference_date)
            except EximbankFxError:
                st.session_state["fx_reference_snapshot"] = None
                st.session_state["fx_load_message"] = (
                    "공식 환율을 불러오지 못했습니다. 현재 Deal 환율은 유지됩니다."
                )
            else:
                st.session_state["fx_reference_snapshot"] = snapshot
                st.session_state["fx_load_message"] = (
                    "선택한 날짜의 공식 환율이 없습니다. 현재 Deal 환율은 유지됩니다."
                    if snapshot is None
                    else "공식 기준환율을 불러왔습니다."
                )
    if message := st.session_state.get("fx_load_message"):
        st.info(message)
    if snapshot := st.session_state.get("fx_reference_snapshot"):
        st.metric("USD/KRW", str(snapshot.usd_krw))
        st.metric("JPY/KRW · 100 JPY", str(snapshot.jpy_krw_per_100))
        st.caption(
            f"기준일 {snapshot.reference_date.isoformat()} · deal_bas_r · 출처: 한국수출입은행"
        )
        st.button("현재 Deal에 적용", on_click=apply_loaded_fx)
    if notice := st.session_state.pop("fx_apply_notice", None):
        st.success(notice)

with market_columns[1].container(border=True):
    st.markdown("#### K-SURE · 결제정보")
    st.badge("Observed official aggregate data", color="green")
    st.caption("미국 · 기타 기계 및 장비 제조업 기준")
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
        st.caption(
            "집계 맥락으로, 개별 바이어의 지연 확률·신용점수·지급보장이 아닙니다."
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
        st.info("K-SURE 집계정보는 Deal 결제일을 자동으로 변경하지 않습니다.")

st.subheader("유동성 자금소요")
st.badge("Calculated result", color="blue")
peak_point = max(
    base_result.funding.points,
    key=lambda point: -point.cumulative_deal_cash_krw,
)
st.markdown(f"**현금 제약이 가장 큰 시점은 D+{peak_point.day}입니다.**")
liquidity_metrics = st.columns(2)
liquidity_metrics[0].metric(
    "Deal 자금소요", krw_millions(base_result.funding.peak_deal_funding_krw)
)
liquidity_metrics[1].metric(
    "최대 외부차입",
    krw_millions(base_result.funding.maximum_external_borrowing_krw),
)
st.caption("동결 Financial Engine의 FundingSchedule 상세입니다.")
liquidity_rows = [
    {
        "시점": f"D+{point.day}",
        "누적 Deal 현금흐름 (KRW)": f"{point.cumulative_deal_cash_krw:,.0f}",
        "외부차입 잔액 (KRW)": f"{point.external_loan_outstanding_krw:,.0f}",
    }
    for point in base_result.funding.points
]
st.dataframe(liquidity_rows, hide_index=True, width="stretch")

st.subheader("USD/KRW 임계환율")
st.badge("Calculated result", color="blue")
st.caption("결정론적 계산 결과이며 환율 예측이 아닙니다.")
try:
    zero_profit_threshold = solve_usd_krw_threshold(deal, fx, None)
    target_threshold = solve_usd_krw_threshold(deal, fx, deal.target_margin)
except ValueError:
    st.warning("현재 Deal 입력으로는 USD/KRW 임계값을 지정 범위에서 찾을 수 없습니다.")
else:
    threshold_columns = st.columns(2)
    threshold_columns[0].metric("손익 0 USD/KRW 임계환율", f"{zero_profit_threshold:,.2f}")
    threshold_columns[1].metric("목표 마진 USD/KRW 임계환율", f"{target_threshold:,.2f}")

st.subheader("매출채권 현금화 선택")
st.badge("Calculated result", color="blue")
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
            st.markdown("#### 바이어 결제일까지 보유")
            st.metric(
                "금융비용 반영 Deal Margin",
                percent(base_result.financing_adjusted_deal_margin),
            )
            st.write(
                f"**최대 외부차입**  {krw_millions(base_result.funding.maximum_external_borrowing_krw)}"
            )
            st.write(
                f"**외부 금융비용**  {krw_millions(base_result.funding.external_funding_cost_krw)}"
            )
            st.write("**매출채권 매입비용**  해당 없음")
            st.write(f"**현금 유입일**  D+{base_result.collection_day}")

        with comparison_columns[1].container(border=True):
            st.markdown("#### 매출채권 조기 매입")
            st.metric(
                "금융비용 반영 Deal Margin",
                percent(purchase_result.financing_adjusted_deal_margin),
            )
            st.write(
                f"**최대 외부차입**  {krw_millions(purchase_result.funding.maximum_external_borrowing_krw)}"
            )
            st.write(
                f"**외부 금융비용**  {krw_millions(purchase_result.funding.external_funding_cost_krw)}"
            )
            st.write(f"**할인비용**  {krw_millions(purchase.discount_cost_krw)}")
            st.write(f"**수수료**  {krw_millions(purchase.purchase_fee_krw)}")
            st.write(f"**현금화일**  D+{purchase.purchase_day}")

        st.info("판단 포인트: 빠른 유동성 확보와 명시적 매입·할인비용 간의 교환관계입니다.")
