from dataclasses import replace
from datetime import date, datetime
from decimal import Decimal
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from zoneinfo import ZoneInfo

import streamlit as st

from components.trade_treasury_experience import (
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
    ForwardHedgeInput,
    analyze_fx_treasury,
)
from src.finance.liquidity import (
    FundingChoice,
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

DEFAULT_REVIEW_QUESTION = "이 거래의 수익성, 회사 전체 유동성, 외화노출과 자금조달 구조에서 우선 확인할 점을 설명해줘."


def decimal_from_widget(value: int | float) -> Decimal:
    return Decimal(str(value))


def percent(value: Decimal) -> str:
    return f"{value * Decimal('100'):.2f}%"


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
    st.session_state["input_origin"] = "문서 반영"
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
fx = reference_fx()
# Widget keys are the applied input values. Forms submit atomically; retain them
# when a different view is mounted. There is no second draft-value store.
defaults = {
    "sale_amount_input": float(reference.sale.amount), "payment_method_input": reference.sale.payment_method.value,
    "collection_day_input": reference.sale.collection_day,
    "usd_payable_amount_input": float(reference.foreign_payables[0].amount), "usd_payable_day_input": reference.foreign_payables[0].payment_day,
    "jpy_payable_amount_input": float(reference.foreign_payables[1].amount), "jpy_payable_day_input": reference.foreign_payables[1].payment_day,
    "advance_amount_input": float(reference.krw_costs[0].amount_krw), "advance_day_input": reference.krw_costs[0].payment_day,
    "balance_amount_input": float(reference.krw_costs[1].amount_krw), "balance_day_input": reference.krw_costs[1].payment_day,
    "logistics_amount_input": float(reference.krw_costs[2].amount_krw), "logistics_day_input": reference.krw_costs[2].payment_day,
    "available_cash_input": float(reference.available_cash_krw), "funding_rate_input": float(reference.annual_funding_rate * 100),
    "target_margin_input": float(reference.target_margin * 100),
    "credit_total_limit_input": 100000000.0, "credit_used_amount_input": 30000000.0,
    "credit_deal_fee_input": 0.0,
    "company_current_available_cash": 120000000.0,
    "company_minimum_operating_cash": 70000000.0,
    "company_liquidity_as_of_date": date(2026, 9, 4),
    "include_expected_company_events": False,
    "receivable_purchase_day_input": 65, "receivable_discount_rate_input": 5.2,
    "receivable_fee_rate_input": 0.15,
    "usance_payable_input": 1, "usance_repayment_day_input": 90,
    "usance_rate_input": 4.8, "usance_fee_input": 0.15,
    "usd_forward_quote_input": 1395.0, "usd_hedge_ratio_input": 80.0,
    "jpy_forward_quote_input": 905.0, "jpy_hedge_ratio_input": 80.0,
    "settlement_usd_krw_input": 1330.0, "settlement_jpy_krw_input": 990.0,
    "custom_usd_input": 1400.0, "custom_jpy_input": 900.0,
    "custom_rate_input": 0.0, "custom_delay_input": 0,
    "selected_scenario": "기본",
}
for key, value in defaults.items():
    st.session_state[key] = st.session_state.get(key, value)
st.session_state.setdefault("company_cash_plan_rows", [dict(row) for row in CANONICAL_COMPANY_CASH_PLAN_ROWS])
st.session_state.setdefault("company_cash_plan_editor_version", 0)


def number(label, key, *, minimum=0.0, maximum=None, step=1.0):
    return st.number_input(label, key=key, min_value=minimum, max_value=maximum, step=step)


def applied_notice():
    st.session_state["input_origin"] = "직접 입력"


def compare_values(label, before, after, delta):
    with st.container(key="comparison_" + label):
        st.markdown("**" + label + "**")
        cols = st.columns(3)
        cols[0].metric("현재", before)
        cols[1].metric("대안", after)
        cols[2].metric("변화", delta, delta_color="off")


st.set_page_config(page_title="수출거래 AI 금융진단", layout="wide")
st.markdown(f"<style>{APP_CSS}</style>", unsafe_allow_html=True)
st.title("수출거래 AI 금융진단")
st.caption("계약 전 수익성·회사 자금·환위험을 한 화면에서 비교합니다.")
origin = st.session_state.get("input_origin", "샘플 거래 · 기준값 적용 중")
st.caption(origin)
trade_treasury_experience()
active_view = get_experience_state()["active_view"]

if active_view == "setup":
    st.subheader("거래 정보")
    st.write(
        f"수출대금 **USD {st.session_state['sale_amount_input']:,.0f}** · "
        f"결제방식 **{'O/A' if st.session_state['payment_method_input'] == 'OA' else 'T/T'}** · "
        f"대금 회수 **D+{st.session_state['collection_day_input']}**"
    )
    st.write(
        f"주요 외화비용 **USD {st.session_state['usd_payable_amount_input']:,.0f} · "
        f"JPY {st.session_state['jpy_payable_amount_input']:,.0f}**"
    )
    st.caption("출처 · " + origin)
    edit_deal = st.toggle("거래 정보 수정", key="edit_deal")
    show_documents = st.toggle("거래서류 불러오기", key="show_documents")
    if edit_deal:
        with st.form("deal_form"):
            st.markdown("#### 매출")
            number("수출대금 (USD)", "sale_amount_input", minimum=1.0, step=1000.0)
            st.selectbox("결제방식", ["OA", "TT"], key="payment_method_input")
            number("계약 회수일 (D+)", "collection_day_input", minimum=0, step=1)
            st.markdown("#### 외화 원가")
            number("USD 외화비용", "usd_payable_amount_input", step=1000.0)
            number("JPY 외화비용", "jpy_payable_amount_input", step=100000.0)
            st.markdown("#### 국내 원가")
            number("국내 생산 선급금 (KRW)", "advance_amount_input", step=1000000.0)
            number("국내 생산 잔금 (KRW)", "balance_amount_input", step=1000000.0)
            number("물류·통관비 (KRW)", "logistics_amount_input", step=1000000.0)
            st.markdown("#### 지급 일정")
            for label, key in (
                ("USD 지급일 (D+)", "usd_payable_day_input"),
                ("JPY 지급일 (D+)", "jpy_payable_day_input"),
                ("선급금 지급일 (D+)", "advance_day_input"),
                ("잔금 지급일 (D+)", "balance_day_input"),
                ("물류·통관비 지급일 (D+)", "logistics_day_input"),
            ):
                number(label, key, minimum=0, step=1)
            st.form_submit_button("변경사항 적용", on_click=applied_notice)
    document_slot = st.container()
    company_setup_slot = st.container()

    with company_setup_slot:
        st.subheader("회사 정보")
        st.write(
            f"현재 가용현금 **{krw_consumer(decimal_from_widget(st.session_state['company_current_available_cash']))}** · "
            f"최소 운영자금 **{krw_consumer(decimal_from_widget(st.session_state['company_minimum_operating_cash']))}**"
        )
        st.write(
            f"이번 거래 배정자금 **{krw_consumer(decimal_from_widget(st.session_state['available_cash_input']))}** · "
            f"현재 미사용 한도 **{krw_consumer(decimal_from_widget(st.session_state['credit_total_limit_input'] - st.session_state['credit_used_amount_input']))}** · "
            f"현재 조달금리 **{st.session_state['funding_rate_input']:.2f}%**"
        )
        st.caption("거래 배정자금과 회사 전체 현재 현금은 서로 다른 입력입니다.")
        if st.toggle("회사 정보 수정", key="edit_company"):
            with st.form("company_form"):
                number("현재 가용현금", "company_current_available_cash", step=1000000.0)
                number("최소 운영자금", "company_minimum_operating_cash", step=1000000.0)
                number("이번 거래 배정자금 (KRW)", "available_cash_input", step=1000000.0)
                number("운전자금 한도 총액", "credit_total_limit_input", step=1000000.0)
                number("현재 사용액", "credit_used_amount_input", step=1000000.0)
                number("현재 실제 연 조달금리 (%)", "funding_rate_input", step=0.1)
                number("이 거래에 추가로 발생하는 한도 수수료", "credit_deal_fee_input", step=100000.0)
                st.date_input("거래 검토 기준일", key="company_liquidity_as_of_date")
                st.form_submit_button("변경사항 적용", on_click=applied_notice)
        if st.toggle("자금계획 확인", key="edit_cash_plan"):
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


deal = DealCase(
    sale=Sale(Currency.USD, decimal_from_widget(st.session_state["sale_amount_input"]),
              PaymentMethod(st.session_state["payment_method_input"]),
              int(st.session_state["collection_day_input"])),
    foreign_payables=(
        ForeignPayable(Currency.USD, decimal_from_widget(st.session_state["usd_payable_amount_input"]), int(st.session_state["usd_payable_day_input"])),
        ForeignPayable(Currency.JPY, decimal_from_widget(st.session_state["jpy_payable_amount_input"]), int(st.session_state["jpy_payable_day_input"])),
    ),
    krw_costs=tuple(
        KrwCost(decimal_from_widget(st.session_state[amount]), int(st.session_state[day]))
        for amount, day in (("advance_amount_input", "advance_day_input"),
                            ("balance_amount_input", "balance_day_input"),
                            ("logistics_amount_input", "logistics_day_input"))
    ),
    available_cash_krw=decimal_from_widget(st.session_state["available_cash_input"]),
    annual_funding_rate=decimal_from_widget(st.session_state["funding_rate_input"]) / 100,
    target_margin=decimal_from_widget(st.session_state["target_margin_input"]) / 100,
)

financialization = st.session_state.get("ai_financialization")


if active_view == "setup" and show_documents:
    with document_slot:
        st.markdown("#### 거래서류 불러오기")
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

            st.info("문서의 회수 기산점은 D0와 자동 연결하지 않습니다. 입력 화면에서 계약 회수일을 확인하세요.")
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


if active_view == "setup":
    with st.expander("재무제표 참고정보 · 선택"):
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


base_result = evaluate_deal(deal, fx)
scenario_results = canonical_scenarios(deal, fx)
combined_result = scenario_results[Scenario.COMBINED]
rescue_analysis = analyze_deal_rescue(deal, fx)
meets_target = base_result.financing_adjusted_deal_margin >= deal.target_margin
zero_profit_threshold = target_threshold = None
try:
    zero_profit_threshold = solve_usd_krw_threshold(deal, fx, None)
    target_threshold = solve_usd_krw_threshold(deal, fx, deal.target_margin)
except ValueError:
    pass

company_liquidity_profile = None
statement_analysis = st.session_state.get("financial_statement_analysis")
if statement_analysis is not None:
    try:
        company_liquidity_profile = build_company_liquidity_profile(statement_analysis)
    except ValueError:
        pass

credit_line = company_liquidity_comparison = company_credit_capacity = None
company_liquidity_input = None
company_as_of_date = st.session_state["company_liquidity_as_of_date"]
include_expected_company_events = st.session_state["include_expected_company_events"]
try:
    credit_line = WorkingCapitalCreditLine(
        decimal_from_widget(st.session_state["credit_total_limit_input"]),
        decimal_from_widget(st.session_state["credit_used_amount_input"]),
        decimal_from_widget(st.session_state["credit_deal_fee_input"]),
    )
except ValueError:
    st.warning("현재 사용액은 운전자금 한도 총액을 초과할 수 없습니다. 입력 화면에서 수정하세요.")
try:
    company_cash_events = company_cash_events_from_rows(st.session_state["company_cash_plan_rows"])
    company_liquidity_input = CompanyLiquidityInput(
        as_of_date=company_as_of_date,
        current_available_cash_krw=decimal_from_widget(st.session_state["company_current_available_cash"]),
        minimum_operating_cash_krw=decimal_from_widget(st.session_state["company_minimum_operating_cash"]),
        existing_cash_events=company_cash_events,
        include_expected_events=include_expected_company_events,
    )
    company_liquidity_comparison = analyze_company_liquidity(
        liquidity_input=company_liquidity_input, deal=deal, fx=fx,
    )
    if credit_line is not None:
        company_credit_capacity = compare_company_gap_to_credit_line(
            company_liquidity_comparison.company_with_deal, credit_line,
        )
except (TypeError, ValueError):
    st.warning("회사 자금계획의 날짜·금액·상태를 입력 화면에서 수정하세요.")

scenario_labels = {
    "기본": Scenario.BASE, "USD -5%": Scenario.USD_DOWN_5,
    "JPY +10%": Scenario.JPY_UP_10, "금리 +1%p": Scenario.RATE_UP_1PP,
    "회수 +30일": Scenario.DELAY_30D, "복합 악화": Scenario.COMBINED,
}
selected_label = st.session_state["selected_scenario"]
if active_view == "analysis":
    gap = company_credit_capacity.liquidity_gap_krw if company_credit_capacity else None
    margin_copy = "현재 거래는 목표마진을 충족하지만" if meets_target else "현재 거래는 목표마진에 미달하며"
    if gap is None:
        conclusion = "현재 거래 마진을 확인했습니다. 회사 정보의 입력을 수정하면 전체 자금부족을 비교할 수 있습니다."
    elif gap > 0:
        conclusion = f"{margin_copy}, 회사 전체 자금계획 기준 {krw_consumer(gap)}이 부족합니다."
    else:
        conclusion = ("현재 거래는 목표마진을 충족하고" if meets_target else "현재 거래는 목표마진에 미달하지만") + ", 회사 전체 자금계획은 현재 한도 내입니다."
    st.markdown("### " + conclusion)
    st.caption(f"현재 마진 {percent(base_result.financing_adjusted_deal_margin)} · 목표마진 {percent(deal.target_margin)}")
    if st.toggle("목표마진 수정", key="edit_target"):
        with st.form("target_form"):
            number("목표 마진 (%)", "target_margin_input", maximum=100.0, step=0.1)
            if st.form_submit_button("적용"):
                st.rerun()
        with st.expander("업종 수익성 참고"):
            st.link_button("한국은행 기업경영분석", "https://www.bok.or.kr/portal/main/contents.do?menuNo=200455")
            st.caption("매출액영업이익률은 본 서비스의 금융비용 반영 거래 마진과 정의가 다릅니다. 업종 수치는 연결하지 않았습니다.")
    if company_liquidity_comparison is not None:
        company_with_deal = company_liquidity_comparison.company_with_deal
        remaining = krw_consumer(gap) if gap is not None else "한도 입력 필요"
        unused = krw_consumer(credit_line.unused_limit_krw) if credit_line else "한도 입력 필요"
        st.markdown(
            '<div class="funding-relationship">'
            '<div><span>이번 거래 필요 외부자금</span><strong>' +
            krw_consumer(base_result.funding.maximum_external_borrowing_krw) +
            '</strong></div><div class="flow-connector">→<small>회사 기존 일정 포함</small></div>'
            '<div><span>회사 전체 최대 자금부족</span><strong>' +
            krw_consumer(company_with_deal.peak_liquidity_gap_krw) +
            '</strong></div><div class="flow-connector">→<small>현재 미사용 한도 ' + unused +
            '</small></div><div><span>남는 부족</span><strong>' + remaining + '</strong></div></div>',
            unsafe_allow_html=True,
        )
        st.caption(
            f"가장 부족한 날 · {company_with_deal.peak_liquidity_gap_date.isoformat()} · "
            f"D+{(company_with_deal.peak_liquidity_gap_date - company_as_of_date).days}"
        )
        st.subheader("회사 현금흐름")
        st.caption("EXPECTED 포함 사용자 선택 시나리오" if include_expected_company_events else "CONFIRMED 기준 · 기존 회사 일정과 이번 거래")

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
            st.dataframe([
                {"날짜": p.event_date.isoformat(), "시점": f"D+{p.day_offset}",
                 "회사 기존 흐름": str(p.existing_company_cashflow_krw),
                 "이번 거래 흐름": str(p.prospective_deal_cashflow_krw),
                 "가용현금": str(p.cumulative_available_liquidity_krw),
                 "최소 운영자금": str(p.minimum_cash_buffer_krw),
                 "자금부족": str(p.required_external_funding_krw)}
                for p in company_with_deal.points
            ], hide_index=True, width="stretch")
    st.subheader("조건을 바꿔보면")
    selected_label = st.radio(
        "비교할 조건", [*scenario_labels, "+ 직접 설정"],
        horizontal=True, key="selected_scenario",
    )
    if selected_label == "+ 직접 설정":
        st.caption("기준환율 · 데모 USD 1,400 / JPY 900 (100 JPY) · 공식 관측값 아님")
        with st.form("custom_scenario_form"):
            number("USD/KRW", "custom_usd_input", minimum=0.01)
            number("JPY/KRW (100 JPY)", "custom_jpy_input", minimum=0.01)
            number("금리 상승 (+%p)", "custom_rate_input", step=0.1)
            number("회수 지연 (+일)", "custom_delay_input", minimum=0, step=1)
            st.form_submit_button("적용")
        st.caption("현재 실제 조달금리와 계약 회수일에 입력한 변화량을 더합니다.")

if selected_label == "+ 직접 설정":
    custom_deal = replace(
        deal, sale=replace(deal.sale, collection_day=deal.sale.collection_day + st.session_state["custom_delay_input"]),
        annual_funding_rate=deal.annual_funding_rate + decimal_from_widget(st.session_state["custom_rate_input"]) / 100,
    )
    selected_scenario_result = evaluate_deal(
        custom_deal, FxRates(decimal_from_widget(st.session_state["custom_usd_input"]), decimal_from_widget(st.session_state["custom_jpy_input"])),
    )
else:
    selected_scenario_result = scenario_results[scenario_labels[selected_label]]

if active_view == "analysis":
    compare_values("마진 · 기본 → " + selected_label,
                   percent(base_result.financing_adjusted_deal_margin),
                   percent(selected_scenario_result.financing_adjusted_deal_margin),
                   f"{(selected_scenario_result.financing_adjusted_deal_margin - base_result.financing_adjusted_deal_margin) * 100:+.2f}%p")
    compare_values("거래 필요 외부자금",
                   krw_consumer(base_result.funding.maximum_external_borrowing_krw),
                   krw_consumer(selected_scenario_result.funding.maximum_external_borrowing_krw),
                   signed_krw_consumer(selected_scenario_result.funding.maximum_external_borrowing_krw - base_result.funding.maximum_external_borrowing_krw))
    delay = selected_scenario_result.collection_day - base_result.collection_day
    compare_values("회수",
                   f"D+{base_result.collection_day}", f"D+{selected_scenario_result.collection_day}",
                   f"{delay:+}일" if delay else "변화 없음")
    with st.expander("전체 시나리오·목표마진 충족 조건"):
        st.dataframe([
            {"조건": label, "마진": percent(scenario_results[name].financing_adjusted_deal_margin),
             "필요 외부자금": krw_consumer(scenario_results[name].funding.maximum_external_borrowing_krw),
             "회수": f"D+{scenario_results[name].collection_day}"}
            for label, name in scenario_labels.items()
        ], hide_index=True, width="stretch")
        if target_threshold is not None:
            st.write(f"목표마진 유지 USD/KRW 경계 · {target_threshold:,.2f}원")
        for option in rescue_analysis.options:
            render_rescue_option(option)
    st.subheader("대응안 비교")
    credit_tab, receivable_tab, forward_tab, usance_tab = st.tabs(
        ["기존 운전자금", "매출채권 조기 현금화", "선물환", "Banker's Usance"]
    )
    with credit_tab:
        if company_credit_capacity is not None:
            st.write(f"회사 전체 부족 **{krw_consumer(company_liquidity_comparison.company_with_deal.peak_liquidity_gap_krw)}**")
            st.write(f"현재 미사용 한도 **{krw_consumer(credit_line.unused_limit_krw)}** → 남는 부족 **{krw_consumer(company_credit_capacity.liquidity_gap_krw)}**")
            st.caption("한도 수정은 입력 화면의 회사 정보에서 적용합니다.")


if active_view == "analysis":
    with receivable_tab:
        receivable_result_slot = st.container()
        if st.toggle("조건 수정", key="edit_receivable"):
            with st.form("receivable_form"):
                number("매입일 (D+)", "receivable_purchase_day_input", minimum=0, step=1)
                number("연 할인율 (%)", "receivable_discount_rate_input", step=0.1)
                number("수수료율 (%)", "receivable_fee_rate_input", step=0.05)
                st.form_submit_button("적용")
    with forward_tab:
        forward_result_slot = st.container()
        if st.toggle("조건 수정", key="edit_forward"):
            with st.form("forward_form"):
                number("USD 헤지비율 (%)", "usd_hedge_ratio_input", maximum=100.0)
                number("USD 선물환 매도환율", "usd_forward_quote_input", minimum=0.01)
                number("JPY 헤지비율 (%)", "jpy_hedge_ratio_input", maximum=100.0)
                number("JPY 선물환 매수환율 (100 JPY)", "jpy_forward_quote_input", minimum=0.01)
                number("정산 시 가정 USD/KRW", "settlement_usd_krw_input", minimum=0.01)
                number("정산 시 가정 JPY/KRW (100 JPY)", "settlement_jpy_krw_input", minimum=0.01)
                st.form_submit_button("적용")
    with usance_tab:
        usance_result_slot = st.container()
        if st.toggle("조건 수정", key="edit_usance"):
            with st.form("usance_form"):
                st.selectbox(
                    "대상 외화 지급", range(len(deal.foreign_payables)),
                    format_func=lambda i: f"{deal.foreign_payables[i].currency.value} {deal.foreign_payables[i].amount:,.0f} · 공급자 D+{deal.foreign_payables[i].payment_day}",
                    key="usance_payable_input",
                )
                number("회사 상환일 (D+)", "usance_repayment_day_input", minimum=0, step=1)
                number("Usance 연 금리 (%)", "usance_rate_input", step=0.1)
                number("Usance 수수료율 (%)", "usance_fee_input", step=0.05)
                st.form_submit_button("적용")

purchase_result = company_funding_analysis = bankers_usance_comparison = fx_treasury_analysis = None
purchase_error = usance_error = forward_error = None
if deal.sale.payment_method is PaymentMethod.OA:
    try:
        purchase_result = evaluate_deal(
            deal, fx, purchase_option=ReceivablePurchaseOption(
                int(st.session_state["receivable_purchase_day_input"]),
                decimal_from_widget(st.session_state["receivable_discount_rate_input"]) / 100,
                decimal_from_widget(st.session_state["receivable_fee_rate_input"]) / 100,
            ),
        )
    except ValueError:
        purchase_error = "매입일은 계약 회수일 이전이어야 합니다. 현금화 조건을 수정하세요."
if credit_line is not None:
    company_funding_analysis = analyze_company_funding(
        deal=deal, base_result=base_result, combined_result=combined_result,
        credit_line=credit_line, purchase_result=purchase_result,
    )
    try:
        bankers_usance_comparison = analyze_bankers_usance(
            deal=deal, fx=fx, base_result=base_result, credit_line=credit_line,
            usance_input=BankersUsanceInput(
                st.session_state["usance_payable_input"], st.session_state["usance_repayment_day_input"],
                decimal_from_widget(st.session_state["usance_rate_input"]) / 100,
                decimal_from_widget(st.session_state["usance_fee_input"]) / 100,
            ),
        )
    except (ValueError, IndexError):
        usance_error = "회사 상환일은 공급자 지급일 이후여야 합니다. Usance 조건을 수정하세요."
try:
    fx_treasury_analysis = analyze_fx_treasury(
        deal=deal, current_fx=fx,
        settlement_fx=FxRates(
            decimal_from_widget(st.session_state["settlement_usd_krw_input"]),
            decimal_from_widget(st.session_state["settlement_jpy_krw_input"]),
        ),
        hedge_inputs=(
            ForwardHedgeInput(Currency.USD, decimal_from_widget(st.session_state["usd_hedge_ratio_input"]) / 100,
                              decimal_from_widget(st.session_state["usd_forward_quote_input"])),
            ForwardHedgeInput(Currency.JPY, decimal_from_widget(st.session_state["jpy_hedge_ratio_input"]) / 100,
                              decimal_from_widget(st.session_state["jpy_forward_quote_input"])),
        ),
    )
except ValueError:
    forward_error = "선물환 비율과 환율을 수정하세요."

if active_view == "analysis":
    with receivable_result_slot:
        if purchase_error:
            st.warning(purchase_error)
        elif purchase_result is None:
            st.info("현재 결제방식에는 매출채권 조기 현금화를 적용하지 않습니다.")
        elif company_funding_analysis is not None:
            choices = {item.choice: item for item in company_funding_analysis.choices}
            early = choices[FundingChoice.EARLY_RECEIVABLE_PURCHASE]
            wait = choices[FundingChoice.WAIT_WITH_CREDIT_LINE]
            compare_values("현금 유입일",
                           f"D+{base_result.collection_day}", f"D+{purchase_result.receivable_purchase.purchase_day}",
                           f"{base_result.collection_day - purchase_result.receivable_purchase.purchase_day}일 빠름")
            compare_values("최대 외부자금",
                           krw_consumer(wait.required_external_funding_krw),
                           krw_consumer(early.required_external_funding_krw),
                           signed_krw_consumer(early.required_external_funding_krw - wait.required_external_funding_krw))
            compare_values("금융·거래 비용",
                           krw_ten_thousands(wait.total_financing_cost_krw),
                           krw_ten_thousands(early.total_financing_cost_krw),
                           krw_ten_thousands(early.total_financing_cost_krw - wait.total_financing_cost_krw, signed=True))
            if early.required_external_funding_krw == wait.required_external_funding_krw:
                st.caption("현금 유입은 앞당겨지지만 현재 조건에서는 최대 필요 한도는 줄지 않습니다.")
            st.caption("거래 단독 기준 · 실제 은행 매입조건이 아닌 입력 비교입니다.")
    with usance_result_slot:
        if usance_error:
            st.warning(usance_error)
        elif bankers_usance_comparison is not None:
            comparison = bankers_usance_comparison
            usance = comparison.usance
            compare_values("일반 운전자금 부담",
                           krw_consumer(comparison.base_working_capital_credit_krw),
                           krw_consumer(usance.peak_working_capital_credit_krw),
                           signed_krw_consumer(-comparison.working_capital_credit_reduction_krw))
            compare_values("총 은행원금",
                           krw_consumer(comparison.base_working_capital_credit_krw),
                           krw_consumer(usance.peak_combined_bank_principal_krw),
                           "변화 없음" if usance.peak_combined_bank_principal_krw == comparison.base_working_capital_credit_krw else signed_krw_consumer(usance.peak_combined_bank_principal_krw - comparison.base_working_capital_credit_krw))
            compare_values("금융비용",
                           krw_ten_thousands(comparison.base_total_financing_cost_krw),
                           krw_ten_thousands(usance.total_financing_cost_krw),
                           krw_ten_thousands(comparison.financing_cost_difference_krw, signed=True))
            st.caption("일반 운전자금 사용이 줄어도 총 은행원금이 줄어드는 것은 아닙니다.")
            st.caption("데모 조건 · 승인/실행 아님 · 지급시점 변경이 환위험을 자동으로 없애지 않습니다.")
            with st.expander("원금·이자·수수료 상세"):
                st.write(f"공급자 D+{usance.supplier_payment_day} → 회사 D+{usance.company_repayment_day}")
                st.write(f"원금 {krw_consumer(usance.principal_krw)} · 이자 {krw_ten_thousands(usance.usance_interest_krw)} · 수수료 {krw_ten_thousands(usance.usance_fee_krw)}")
    with forward_result_slot:
        if forward_error:
            st.warning(forward_error)
        elif fx_treasury_analysis is not None:
            for position, hedge in zip(fx_treasury_analysis.positions, fx_treasury_analysis.settlement_scenario_hedges):
                currency = position.currency.value
                st.write(f"**{currency} 열린 노출 {position.open_exposure:,.0f}** · 고정 {hedge.hedged_notional:,.0f} · 남은 노출 {hedge.residual_exposure:,.0f}")
            overlay = fx_treasury_analysis.settlement_scenario_overlay
            compare_values("입력 정산환율의 마진",
                           percent(overlay.unhedged_margin), percent(overlay.simulated_margin_after_hedge),
                           f"{(overlay.simulated_margin_after_hedge - overlay.unhedged_margin) * 100:+.2f}%p")
            st.write(f"정산효과 **{signed_krw_consumer(overlay.hedge_effect_krw)}** · 현재 환율 유지 시 **{signed_krw_consumer(fx_treasury_analysis.current_spot_total_effect_krw)}**")
            st.caption("데모 가정 · 실제 은행 quote 아님 · 환율 예측이나 헤지 추천이 아닙니다.")
            with st.expander("통화별 노출·정산 기준"):
                for position in fx_treasury_analysis.positions:
                    currency = position.currency.value
                    st.write(f"{currency} 받을 외화 {position.receivable_amount:,.0f} · 지급 외화 {position.payable_amount:,.0f} · 금액 기준 상계 {position.amount_offset:,.0f}")
                    st.write(f"순노출 {position.net_exposure:+,.0f} · 불리한 방향 {'하락' if position.net_exposure > 0 else '상승' if position.net_exposure < 0 else '없음'}")
                st.caption(f"USD 지급 D+{deal.foreign_payables[0].payment_day} · 수취 D+{deal.sale.collection_day} — 금액 상계와 시점 일치는 다릅니다.")
                st.caption("JPY 환율은 100 JPY 기준입니다. 선물환 정산효과는 손익 비교이며 파생상품 정산 차입일정은 재계산하지 않습니다.")


if active_view == "analysis":
    with st.expander("결제 지연 참고정보"):
        st.caption("불러온 공식 집계는 계약조건을 자동으로 바꾸지 않습니다.")
        st.write(
            "공식 데이터는 명시적으로 불러옵니다. K-SURE 정보는 결제 참고정보로만 "
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


current_payment_context = st.session_state.get("ksure_payment_context")
treasury_review_context = TreasuryReviewContext(
    company_liquidity=company_liquidity_profile, company_funding=company_funding_analysis,
    fx_treasury=fx_treasury_analysis, bankers_usance=bankers_usance_comparison,
    company_cash_timeline=company_liquidity_comparison, company_cash_capacity=company_credit_capacity,
)
tool_labels = {
    "read_current_deal_analysis": "현재 거래 분석",
    "read_stress_and_rescue": "악화 조건 / 목표마진 충족 조건",
    "read_treasury_context": "회사 자금 / 자금조달 / 외화위험",
    "read_payment_context": "K-SURE 결제 참고정보",
}
custom_review_question = st.session_state.get("custom_deal_review_question", "")
if active_view == "report":
    st.subheader("현재 결과")
    st.write(f"현재 마진 **{percent(base_result.financing_adjusted_deal_margin)}** · 목표 **{percent(deal.target_margin)}** · {'목표 충족' if meets_target else '목표 미달'}")
    if company_credit_capacity is not None:
        st.write(f"회사 전체 최대 자금부족 **{krw_consumer(company_liquidity_comparison.company_with_deal.peak_liquidity_gap_krw)}** · 현재 한도 반영 후 부족 **{krw_consumer(company_credit_capacity.liquidity_gap_krw)}**")
    st.caption(f"선택한 비교 · {selected_label} · 마진 {percent(selected_scenario_result.financing_adjusted_deal_margin)}. 보고서는 기본 조건과 기본 악화 가정를 포함합니다.")
    st.subheader("AI 거래 검토")
    st.caption("선택 사항 · 기본 조건과 현재 근거를 읽고 검토 의미를 정리합니다.")
    with st.expander("질문 직접 수정"):
        custom_review_question = st.text_area("검토 질문", value=custom_review_question,
                                             max_chars=400, key="custom_deal_review_question",
                                             placeholder=DEFAULT_REVIEW_QUESTION)
review_question = custom_review_question.strip() or DEFAULT_REVIEW_QUESTION
treasury_review_ready = all(value is not None for value in (
    company_funding_analysis, fx_treasury_analysis, bankers_usance_comparison,
    company_liquidity_comparison, company_credit_capacity,
))
if active_view == "report":
    if not treasury_review_ready:
        st.warning("회사 자금계획·한도·선물환·Usance 조건을 수정하면 거래 검토를 실행할 수 있습니다.")
    if st.button("이 조건으로 거래 검토", type="primary", disabled=not treasury_review_ready, key="run_review"):
        with st.spinner("현재 거래 근거를 확인하고 있습니다."):
            try:
                review_run = run_deal_review(
                    review_question, deal=deal, fx=fx, base_result=base_result,
                    scenario_results=tuple(scenario_results.items()),
                    zero_profit_threshold=zero_profit_threshold, target_margin_threshold=target_threshold,
                    rescue_analysis=rescue_analysis, treasury_context=treasury_review_context,
                    payment_context=current_payment_context,
                )
            except DealReviewError:
                st.session_state["deal_review_error"] = "AI 거래 검토를 완료하지 못했습니다."
                st.session_state.pop("deal_review_run", None)
            else:
                st.session_state["deal_review_run"] = review_run
                st.session_state.pop("deal_review_error", None)
            st.rerun()
    if review_error := st.session_state.get("deal_review_error"):
        st.warning(review_error)

review_run = st.session_state.get("deal_review_run")
review_is_current = bool(review_run is not None and is_current_deal_review(
    review_run, review_question, deal, fx, treasury_review_context, current_payment_context,
))


if active_view == "report" and review_run is not None:
    if not review_is_current:
        st.warning("조건이 바뀌었습니다. 현재 조건으로 다시 거래 검토하세요.")
    else:
        memo = review_run.memo
        st.markdown(f"### {memo.headline}")
        st.write(memo.summary)
        review_details = st.expander("상세 설명 보기")
        review_details.__enter__()
        display_signals = (
            memo.treasury_focus,
            *memo.supporting_signals,
        )
        options = rescue_option_map(rescue_analysis)
        for index, signal in enumerate(display_signals):
            if index == 0:
                st.markdown("#### 우선 검토 주제")
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
                            f"회사 전체 최대 자금부족 {krw_consumer(peak.peak_liquidity_gap_krw)} · "
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



if active_view == "report":
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
    st.subheader("PDF 보고서")
    st.write("현재 입력 기준 계산과 현재 거래 검토를 최대 3페이지 보고서로 저장합니다.")
    report_preview = st.columns(3)
    report_preview[0].metric("현재 상태", "목표 충족" if meets_target else "목표 미달")
    report_preview[1].metric("생성 기준", report_basis.replace("Deal", "거래"))
    report_preview[2].metric("공식 데이터", official_context)
    st.download_button(
        "보고서 다운로드",
        data=report_bytes,
        file_name="export-deal-diagnosis-report.pdf",
        mime="application/pdf",
        type="primary",
        key="deal_report_download",
    )
    st.caption("현재 화면의 결정론적 분석 결과로 즉시 생성되며 서버에 저장되지 않습니다.")
