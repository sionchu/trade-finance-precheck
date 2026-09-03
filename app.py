from datetime import date
from decimal import Decimal
import os

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
    canonical_purchase_option,
    canonical_scenarios,
    evaluate_deal,
    solve_usd_krw_threshold,
)


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
st.title("AI Trade Finance Pre-check")
st.write(
    "Evaluate whether one export deal's margin and liquidity remain resilient "
    "under FX, delayed collection, and funding stress."
)
st.info(
    "Pre-deal decision support. Not a bank approval, FX forecast, credit score, "
    "or financing execution tool."
)

st.sidebar.header("Deal input")
st.sidebar.badge("Demo assumption", color="gray")
st.sidebar.caption("Canonical reference values are preloaded and remain editable.")

with st.sidebar.expander("Export sale", expanded=True):
    sale_amount = st.number_input(
        "USD sale amount",
        min_value=1.0,
        value=float(reference.sale.amount),
        step=1000.0,
        key="sale_amount_input",
    )
    payment_method_value = st.selectbox(
        "Payment method", [method.value for method in PaymentMethod], index=0
    )
    collection_day = st.number_input(
        "Collection day", min_value=0, value=reference.sale.collection_day, step=1
    )

with st.sidebar.expander("Foreign inputs", expanded=True):
    usd_payable = reference.foreign_payables[0]
    jpy_payable = reference.foreign_payables[1]
    usd_payable_amount = st.number_input(
        "USD payable amount", min_value=0.0, value=float(usd_payable.amount), step=1000.0
    )
    usd_payable_day = st.number_input(
        "USD payable day", min_value=0, value=usd_payable.payment_day, step=1
    )
    jpy_payable_amount = st.number_input(
        "JPY payable amount", min_value=0.0, value=float(jpy_payable.amount), step=100000.0
    )
    jpy_payable_day = st.number_input(
        "JPY payable day", min_value=0, value=jpy_payable.payment_day, step=1
    )

with st.sidebar.expander("KRW costs", expanded=False):
    advance, balance, logistics = reference.krw_costs
    advance_amount = st.number_input(
        "Domestic advance amount", min_value=0.0, value=float(advance.amount_krw), step=1000000.0
    )
    advance_day = st.number_input(
        "Domestic advance day", min_value=0, value=advance.payment_day, step=1
    )
    balance_amount = st.number_input(
        "Domestic balance amount", min_value=0.0, value=float(balance.amount_krw), step=1000000.0
    )
    balance_day = st.number_input(
        "Domestic balance day", min_value=0, value=balance.payment_day, step=1
    )
    logistics_amount = st.number_input(
        "Logistics / customs amount", min_value=0.0, value=float(logistics.amount_krw), step=1000000.0
    )
    logistics_day = st.number_input(
        "Logistics / customs day", min_value=0, value=logistics.payment_day, step=1
    )

with st.sidebar.expander("Liquidity / finance", expanded=True):
    available_cash = st.number_input(
        "Available company cash (KRW)",
        min_value=0.0,
        value=float(reference.available_cash_krw),
        step=1000000.0,
    )
    funding_rate_percent = st.number_input(
        "Actual annual funding rate (%)",
        min_value=0.0,
        value=float(reference.annual_funding_rate * Decimal("100")),
        step=0.1,
    )
    target_margin_percent = st.number_input(
        "Target deal margin (%)",
        min_value=0.0,
        value=float(reference.target_margin * Decimal("100")),
        step=0.1,
    )

with st.sidebar.expander("FX", expanded=True):
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
    st.caption("Preloaded from the demo assumptions; official rates apply only on request.")

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

st.subheader("Base decision snapshot")
st.badge("Calculated result", color="blue")
decision = st.columns([2, 1])
decision[0].metric(
    "Financing-adjusted Deal Margin",
    percent(base_result.financing_adjusted_deal_margin),
    border=True,
)
if base_result.financing_adjusted_deal_margin >= deal.target_margin:
    decision[1].success("MEETS TARGET")
else:
    decision[1].error("BELOW TARGET")

metrics = st.columns(3)
metrics[0].metric("Target Margin", percent(deal.target_margin))
metrics[1].metric("Gross Deal Margin", percent(base_result.gross_deal_margin))
metrics[2].metric(
    "Peak Deal Funding Requirement", krw_millions(base_result.funding.peak_deal_funding_krw)
)
metrics = st.columns(2)
metrics[0].metric(
    "Maximum External Borrowing",
    krw_millions(base_result.funding.maximum_external_borrowing_krw),
)
metrics[1].metric(
    "External Funding Cost", krw_millions(base_result.funding.external_funding_cost_krw)
)

st.subheader("Deterministic stress test")
st.badge("STRESS ASSUMPTION", color="orange")
st.caption("Deterministic stress assumptions, not forecasts.")
scenario_rows = []
for scenario, result in canonical_scenarios(deal, fx).items():
    scenario_rows.append(
        {
            "Scenario": scenario.value,
            "Financing-adjusted margin": percent(result.financing_adjusted_deal_margin),
            "Maximum external borrowing": krw_millions(result.funding.maximum_external_borrowing_krw),
            "Funding cost": krw_millions(result.funding.external_funding_cost_krw),
            "Collection day": f"D+{result.collection_day}",
        }
    )
st.dataframe(scenario_rows, hide_index=True, width="stretch")

st.subheader("Liquidity view")
st.badge("Calculated result", color="blue")
st.caption("Financial Engine FundingSchedule detail.")
liquidity_rows = [
    {
        "Day": f"D+{point.day}",
        "Cumulative deal cash (KRW)": f"{point.cumulative_deal_cash_krw:,.0f}",
        "External loan outstanding (KRW)": f"{point.external_loan_outstanding_krw:,.0f}",
    }
    for point in base_result.funding.points
]
st.dataframe(liquidity_rows, hide_index=True, width="stretch")

st.subheader("USD/KRW thresholds")
st.badge("Calculated result", color="blue")
st.caption("Not an FX prediction.")
try:
    zero_profit_threshold = solve_usd_krw_threshold(deal, fx, None)
    target_threshold = solve_usd_krw_threshold(deal, fx, deal.target_margin)
except ValueError:
    st.warning("A USD/KRW threshold is not bracketed for the current Deal inputs.")
else:
    threshold_columns = st.columns(2)
    threshold_columns[0].metric("Zero-profit USD/KRW threshold", f"{zero_profit_threshold:,.2f}")
    threshold_columns[1].metric("Target-margin USD/KRW threshold", f"{target_threshold:,.2f}")

st.subheader("Receivable decision")
st.badge("Calculated result", color="blue")
if deal.sale.payment_method is PaymentMethod.TT:
    st.info("EARLY_RECEIVABLE_PURCHASE is available only for O/A receivables in v0.1.")
else:
    default_purchase = canonical_purchase_option()
    purchase_columns = st.columns(3)
    purchase_day = purchase_columns[0].number_input(
        "Purchase day", min_value=0, value=default_purchase.purchase_day, step=1
    )
    discount_rate_percent = purchase_columns[1].number_input(
        "Annual discount rate (%)",
        min_value=0.0,
        value=float(default_purchase.annual_discount_rate * Decimal("100")),
        step=0.1,
    )
    fee_rate_percent = purchase_columns[2].number_input(
        "Fee rate (%)",
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
        st.warning(str(exc))
    else:
        purchase = purchase_result.receivable_purchase
        comparison = [
            {
                "Path": "Wait for buyer",
                "Financing-adjusted margin": percent(base_result.financing_adjusted_deal_margin),
                "Maximum external borrowing": krw_millions(base_result.funding.maximum_external_borrowing_krw),
                "External funding cost": krw_millions(base_result.funding.external_funding_cost_krw),
                "Purchase discount cost": "—",
                "Purchase fee": "—",
                "Collection / monetization day": f"D+{base_result.collection_day}",
            },
            {
                "Path": "Early receivable purchase",
                "Financing-adjusted margin": percent(purchase_result.financing_adjusted_deal_margin),
                "Maximum external borrowing": krw_millions(purchase_result.funding.maximum_external_borrowing_krw),
                "External funding cost": krw_millions(purchase_result.funding.external_funding_cost_krw),
                "Purchase discount cost": krw_millions(purchase.discount_cost_krw),
                "Purchase fee": krw_millions(purchase.purchase_fee_krw),
                "Collection / monetization day": f"D+{purchase.purchase_day}",
            },
        ]
        st.dataframe(comparison, hide_index=True, width="stretch")
        st.caption("Deterministic trade-off: earlier liquidity versus explicit purchase and discount cost.")

st.subheader("Official reference FX")
reference_date = st.date_input("Reference date", value=date.today())
if st.button("Load official reference FX"):
    if not os.environ.get("EXIMBANK_AUTH_KEY"):
        st.session_state["fx_load_message"] = "Official FX retrieval is unavailable: EXIMBANK_AUTH_KEY is not set."
    else:
        try:
            snapshot = fetch_fx_reference(reference_date)
        except EximbankFxError:
            st.session_state["fx_reference_snapshot"] = None
            st.session_state["fx_load_message"] = "Official FX retrieval failed. Current Deal FX values were preserved."
        else:
            st.session_state["fx_reference_snapshot"] = snapshot
            st.session_state["fx_load_message"] = (
                "No official FX data exists for that date. Current Deal FX values were preserved."
                if snapshot is None
                else "Official reference FX loaded."
            )
if message := st.session_state.get("fx_load_message"):
    st.info(message)
if snapshot := st.session_state.get("fx_reference_snapshot"):
    st.badge("Observed official data", color="green")
    st.write(f"Reference date: {snapshot.reference_date.isoformat()}")
    st.write(f"USD/KRW `deal_bas_r`: {snapshot.usd_krw}")
    st.write(f"JPY/KRW per 100 JPY `deal_bas_r`: {snapshot.jpy_krw_per_100}")
    st.write("Source: Korea Eximbank")
    st.button("Apply official FX to Deal inputs", on_click=apply_loaded_fx)
if notice := st.session_state.pop("fx_apply_notice", None):
    st.success(notice)

st.subheader("K-SURE payment context")
st.caption("Canonical demo query: United States / other machinery and equipment manufacturing.")
if st.button("Load K-SURE payment context"):
    if not os.environ.get("KSURE_SERVICE_KEY"):
        st.session_state["ksure_load_message"] = "Official payment context is unavailable: KSURE_SERVICE_KEY is not set."
    else:
        try:
            context = fetch_payment_context("450", "29")
        except KsurePaymentError:
            st.session_state["ksure_payment_context"] = None
            st.session_state["ksure_load_message"] = "K-SURE payment-context retrieval failed."
        else:
            st.session_state["ksure_payment_context"] = context
            st.session_state["ksure_load_message"] = (
                "No K-SURE payment context is available for the canonical query."
                if context is None
                else "K-SURE payment context loaded."
            )
if message := st.session_state.get("ksure_load_message"):
    st.info(message)
if context := st.session_state.get("ksure_payment_context"):
    st.badge("Observed official aggregate data", color="green")
    st.write(f"Reference year: {context.reference_year}")
    st.write(f"Average payment period: {decimal_text(context.average_payment_period_days, ' days')}")
    st.write(f"Late-payment rate: {decimal_text(context.late_payment_rate_percent, '%')}")
    st.write(
        "Average late-payment period: "
        f"{decimal_text(context.average_late_payment_period_days, ' days')}"
    )
    st.write(f"Source: K-SURE · Last update: {context.last_update_date.isoformat()}")
    st.caption("Aggregate context, not buyer delinquency probability, a buyer credit score, or a guaranteed payment date.")
    if context.payment_terms:
        st.write("Payment-term distribution")
        st.dataframe(
            [
                {
                    "Term": share.name,
                    "Percent": decimal_text(share.percent, "%"),
                    "Observations": share.observation_count,
                }
                for share in context.payment_terms
            ],
            hide_index=True,
            width="stretch",
        )
    if context.payment_period_distribution:
        st.write("Payment-period distribution")
        st.dataframe(
            [
                {
                    "Period": share.name,
                    "Percent": decimal_text(share.percent, "%"),
                    "Observations": share.observation_count,
                }
                for share in context.payment_period_distribution
            ],
            hide_index=True,
            width="stretch",
        )
    st.info("K-SURE context does not automatically change the Deal collection day.")
