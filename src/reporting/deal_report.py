from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from src.ai.financialization import ProposedDealPatch
from src.ai.deal_review import DealReviewMemo, SupportingSignal, TreasuryFocus
from src.domain.deal_case import Currency, DealCase, PaymentMethod
from src.external.eximbank_fx import FxReferenceSnapshot
from src.external.ksure_payment import PaymentContext
from src.finance.engine import DealResult, Scenario
from src.finance.company_liquidity import (
    CompanyDealLiquidityComparison,
    CompanyLiquidityCreditCapacity,
)
from src.finance.fx_treasury import FxTreasuryAnalysis
from src.finance.liquidity import CompanyFundingAnalysis, FundingChoice
from src.finance.usance import BankersUsanceComparison


FONT_NAME = "HYGothic-Medium"
NAVY = colors.HexColor("#163A5F")
INK = colors.HexColor("#17212B")
MUTED = colors.HexColor("#5E6B78")
LINE = colors.HexColor("#D9E1E8")
PALE_BLUE = colors.HexColor("#EEF4F8")
PALE_GREEN = colors.HexColor("#EAF6EF")
PALE_RED = colors.HexColor("#FBEDEE")
PALE_AMBER = colors.HexColor("#FFF5DF")


class AiProvenanceStatus(Enum):
    NOT_APPLIED = "NOT_APPLIED"
    CURRENT = "CURRENT"
    MODIFIED_AFTER_APPLY = "MODIFIED_AFTER_APPLY"


def current_ai_provenance(
    applied_patch: ProposedDealPatch | None,
    deal: DealCase,
) -> AiProvenanceStatus:
    if applied_patch is None:
        return AiProvenanceStatus.NOT_APPLIED

    payables = {payable.currency: payable for payable in deal.foreign_payables}
    comparisons = [
        deal.sale.amount == applied_patch.sale_amount_usd,
        deal.sale.payment_method.value == applied_patch.payment_method.value,
    ]
    for currency, amount, day in (
        (Currency.USD, applied_patch.usd_payable_amount, applied_patch.usd_payable_day),
        (Currency.JPY, applied_patch.jpy_payable_amount, applied_patch.jpy_payable_day),
    ):
        payable = payables.get(currency)
        if amount is not None:
            comparisons.append(payable is not None and payable.amount == amount)
        if day is not None:
            comparisons.append(payable is not None and payable.payment_day == day)
    return (
        AiProvenanceStatus.CURRENT
        if all(comparisons)
        else AiProvenanceStatus.MODIFIED_AFTER_APPLY
    )


def report_basis_text(
    status: AiProvenanceStatus,
    ai_analysis_exists: bool,
) -> str:
    if status is AiProvenanceStatus.CURRENT:
        return "거래서류 AI 추출값 일부 반영"
    if status is AiProvenanceStatus.MODIFIED_AFTER_APPLY:
        return "AI 추출값 반영 후 현재 Deal에서 일부 값 수정"
    if ai_analysis_exists:
        return "AI 분석 결과 존재 · 현재 Deal에는 미반영"
    return "현재 Deal 입력 기반 분석"


def official_context_text(
    fx_reference: FxReferenceSnapshot | None,
    payment_context: PaymentContext | None,
) -> str:
    if fx_reference is not None and payment_context is not None:
        return "한국수출입은행 환율 / K-SURE 결제 참고정보"
    if fx_reference is not None:
        return "한국수출입은행 환율 참고정보"
    if payment_context is not None:
        return "K-SURE 결제 참고정보"
    return "이 세션에 불러온 공식 데이터 없음"


@dataclass(frozen=True)
class DealReportInput:
    generated_at: datetime
    deal: DealCase
    base_result: DealResult
    scenario_results: tuple[tuple[Scenario, DealResult], ...]
    zero_profit_threshold: Decimal | None
    target_margin_threshold: Decimal | None
    purchase_result: DealResult | None = None
    fx_reference: FxReferenceSnapshot | None = None
    payment_context: PaymentContext | None = None
    ai_analysis_exists: bool = False
    ai_provenance_status: AiProvenanceStatus = AiProvenanceStatus.NOT_APPLIED
    hedge_confirmed: bool = False
    company_liquidity_timeline: CompanyDealLiquidityComparison | None = None
    company_liquidity_capacity: CompanyLiquidityCreditCapacity | None = None
    treasury_confirmed_current_cash_krw: Decimal | None = None
    minimum_operating_cash_krw: Decimal | None = None
    company_funding: CompanyFundingAnalysis | None = None
    fx_treasury: FxTreasuryAnalysis | None = None
    bankers_usance: BankersUsanceComparison | None = None
    company_liquidity_includes_expected: bool = False
    review_memo: DealReviewMemo | None = None
    review_used_tools: tuple[str, ...] = ()
    review_is_current: bool = False


def _krw_millions(value: Decimal) -> str:
    return f"KRW {value / Decimal('1000000'):,.3f}M"


def _percent(value: Decimal) -> str:
    return f"{value * Decimal('100'):.2f}%"


def _amount(value: Decimal) -> str:
    return f"{value:,.0f}"


def _styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "KoreanTitle", parent=base["Title"], fontName=FONT_NAME,
            fontSize=19, leading=24, textColor=NAVY, spaceAfter=3 * mm,
        ),
        "subtitle": ParagraphStyle(
            "KoreanSubtitle", parent=base["Heading2"], fontName=FONT_NAME,
            fontSize=11, leading=15, textColor=MUTED, spaceAfter=4 * mm,
        ),
        "section": ParagraphStyle(
            "KoreanSection", parent=base["Heading2"], fontName=FONT_NAME,
            fontSize=12, leading=16, textColor=NAVY, spaceBefore=3 * mm,
            spaceAfter=2 * mm,
        ),
        "body": ParagraphStyle(
            "KoreanBody", parent=base["BodyText"], fontName=FONT_NAME,
            fontSize=8.3, leading=12, textColor=INK,
        ),
        "small": ParagraphStyle(
            "KoreanSmall", parent=base["BodyText"], fontName=FONT_NAME,
            fontSize=7.2, leading=10, textColor=MUTED,
        ),
        "metric": ParagraphStyle(
            "KoreanMetric", parent=base["BodyText"], fontName=FONT_NAME,
            fontSize=15, leading=19, textColor=NAVY, alignment=TA_CENTER,
        ),
        "metric_label": ParagraphStyle(
            "KoreanMetricLabel", parent=base["BodyText"], fontName=FONT_NAME,
            fontSize=7.4, leading=10, textColor=MUTED, alignment=TA_CENTER,
        ),
    }


def _p(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text, style)


def _table(data, widths, *, header=True, highlight_last=False) -> Table:
    table = Table(data, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("FONTNAME", (0, 0), (-1, -1), FONT_NAME),
        ("FONTSIZE", (0, 0), (-1, -1), 7.2),
        ("LEADING", (0, 0), (-1, -1), 9.5),
        ("TEXTCOLOR", (0, 0), (-1, -1), INK),
        ("GRID", (0, 0), (-1, -1), 0.35, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if header:
        commands.extend([
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ])
    if highlight_last:
        commands.append(("BACKGROUND", (0, -1), (-1, -1), PALE_AMBER))
    table.setStyle(TableStyle(commands))
    return table


def _metric_cards(rows, styles) -> Table:
    cells = []
    for label, value in rows:
        cells.append([
            _p(label, styles["metric_label"]),
            _p(value, styles["metric"]),
        ])
    table = Table([cells], colWidths=[55 * mm] * len(cells), hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE_BLUE),
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return table


def _scenario_label(scenario: Scenario) -> str:
    return {
        Scenario.BASE: "현재 조건",
        Scenario.USD_DOWN_5: "달러 가치 -5%",
        Scenario.JPY_UP_10: "엔화 가치 +10%",
        Scenario.RATE_UP_1PP: "조달금리 +1%p",
        Scenario.DELAY_30D: "고객 입금 +30일 지연",
        Scenario.COMBINED: "복합 악화 시나리오",
    }[scenario]


def _footer(canvas, document) -> None:
    canvas.saveState()
    canvas.setFont(FONT_NAME, 7)
    canvas.setFillColor(MUTED)
    canvas.drawString(18 * mm, 10 * mm, "기업 수출거래 Treasury 사전점검")
    canvas.drawRightString(192 * mm, 10 * mm, f"{document.page}")
    canvas.restoreState()


def build_deal_report(report: DealReportInput) -> bytes:
    """Render supplied, already-computed current evidence as an in-memory PDF."""
    pdfmetrics.registerFont(UnicodeCIDFont(FONT_NAME))
    styles = _styles()
    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer, pagesize=A4, leftMargin=16 * mm, rightMargin=16 * mm,
        topMargin=14 * mm, bottomMargin=16 * mm,
        title="기업 수출거래 Treasury 사전점검 보고서",
        author="Company-aware Trade Treasury Pre-check",
    )
    story: list = []
    basis = report_basis_text(
        report.ai_provenance_status,
        report.ai_analysis_exists,
    )
    story.extend([
        _p("Company-aware Trade Treasury Pre-check", styles["subtitle"]),
        _p("기업 수출거래 Treasury 사전점검 보고서", styles["title"]),
        _p(
            f"생성시각 {report.generated_at.strftime('%Y-%m-%d %H:%M %Z')} / "
            "분석용 사전점검 / 은행 승인 / 금융 실행 / 신용평가 아님",
            styles["small"],
        ),
        _p(basis, styles["small"]),
    ])

    meets = report.base_result.financing_adjusted_deal_margin >= report.deal.target_margin
    status_text = "목표 충족" if meets else "목표 미달"
    status_bg = PALE_GREEN if meets else PALE_RED
    decision = Table([[
        _p(
            "현재 조건에서는 목표 마진을 충족합니다." if meets
            else "현재 조건에서는 목표 마진에 미달합니다.",
            styles["section"],
        ),
        _p(f"{status_text}<br/>{_percent(report.base_result.financing_adjusted_deal_margin)}", styles["metric"]),
    ]], colWidths=[118 * mm, 60 * mm])
    decision.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), status_bg),
        ("BOX", (0, 0), (-1, -1), 0.6, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.extend([
        Spacer(1, 4 * mm), decision,
        _p("1. 거래 사전점검 요약", styles["section"]),
    ])
    peak_point = max(
        report.base_result.funding.points,
        key=lambda point: -point.cumulative_deal_cash_krw,
    )
    story.append(_metric_cards([
        ("Deal 자금소요", _krw_millions(report.base_result.funding.peak_deal_funding_krw)),
        ("최대 외부차입", _krw_millions(report.base_result.funding.maximum_external_borrowing_krw)),
        ("외부 금융비용", _krw_millions(report.base_result.funding.external_funding_cost_krw)),
    ], styles))
    story.append(_p(f"거래 자금 부담이 가장 큰 시점: D+{peak_point.day} / 목표 마진 {_percent(report.deal.target_margin)}", styles["small"]))

    receivable = f"{report.deal.sale.currency.value} {_amount(report.deal.sale.amount)}"
    payable_lines = "<br/>".join(
        f"{item.currency.value} {_amount(item.amount)}" for item in report.deal.foreign_payables
    )
    exposure_lines = []
    for currency in (Currency.USD, Currency.JPY):
        exposure = report.base_result.currency_exposure.get(currency, Decimal("0"))
        note = "달러 가치가 떨어지면 불리" if currency is Currency.USD and exposure > 0 else "엔화 가치가 오르면 불리" if currency is Currency.JPY and exposure < 0 else "방향별 영향 확인"
        exposure_lines.append(f"{currency.value} {exposure:+,.0f} / {note}")
    story.extend([
        _p("2. Deal economics", styles["section"]),
        _table([
            ["받을 돈", "낼 돈", "환율에 노출된 금액"],
            [_p(receivable, styles["body"]), _p(payable_lines, styles["body"]), _p("<br/>".join(exposure_lines), styles["body"])],
        ], [48 * mm, 55 * mm, 75 * mm]),
        _p("아래 거래 현금은 회사 전체 현금잔액이 아니라 기존 Deal 엔진의 거래별 배정자금입니다.", styles["small"]),
        _p("3. Company-wide liquidity", styles["section"]),
    ])
    if report.company_liquidity_timeline is None or report.company_liquidity_capacity is None:
        story.append(_p("현재 조건 기준 회사 전체 유동성 요약 없음", styles["body"]))
    else:
        comparison = report.company_liquidity_timeline
        timeline = comparison.company_with_deal
        without = comparison.company_without_deal
        capacity = report.company_liquidity_capacity
        peak_point_company = next(
            point for point in timeline.points
            if point.event_date == timeline.peak_liquidity_gap_date
        )
        mode = (
            "EXPECTED 포함 사용자 선택 시나리오"
            if report.company_liquidity_includes_expected
            else "CONFIRMED 기준"
        )
        story.extend([
            _p(mode, styles["small"]),
            _table([
                ["현재 가용현금", "최소 운영자금", "거래만 본 필요 은행자금"],
                [
                    _krw_millions(report.treasury_confirmed_current_cash_krw)
                    if report.treasury_confirmed_current_cash_krw is not None else "입력 없음",
                    _krw_millions(report.minimum_operating_cash_krw)
                    if report.minimum_operating_cash_krw is not None else "입력 없음",
                    _krw_millions(report.base_result.funding.maximum_external_borrowing_krw),
                ],
                ["회사 자체 Peak 부족", "Deal 포함 Peak 부족", "기존 한도 적용 후 부족"],
                [
                    _krw_millions(without.peak_liquidity_gap_krw),
                    _krw_millions(timeline.peak_liquidity_gap_krw),
                    _krw_millions(capacity.liquidity_gap_krw),
                ],
            ], [59 * mm, 59 * mm, 60 * mm]),
            _p(
                f"Peak {timeline.peak_liquidity_gap_date.isoformat()} / D+{peak_point_company.day_offset} · "
                f"미사용 운전자금 한도 {_krw_millions(capacity.unused_credit_limit_krw)} · "
                f"종료 예상현금 {_krw_millions(timeline.ending_projected_cash_krw)}",
                styles["small"],
            ),
            _p("Deal-level allocated cash != Company-wide current cash position", styles["small"]),
        ])

    story.extend([
        _p("4. 복합 악화 시나리오 / 목표마진 충족 조건", styles["section"]),
        _p("아래 값은 사용자·제품 Stress 가정이며 환율·입금 시점에 대한 예측이 아닙니다.", styles["small"]),
    ])
    scenario_rows = [["상황", "금융비용 반영 마진", "목표 상태", "최대 외부차입"]]
    for scenario, result in report.scenario_results:
        scenario_rows.append([
            _scenario_label(scenario),
            _percent(result.financing_adjusted_deal_margin),
            "충족" if result.financing_adjusted_deal_margin >= report.deal.target_margin else "미달",
            _krw_millions(result.funding.maximum_external_borrowing_krw),
        ])
    story.extend([
        _table(scenario_rows, [53 * mm, 45 * mm, 30 * mm, 50 * mm], highlight_last=True),
        _p("USD/KRW 계산 기준점", styles["section"]),
    ])
    missing_threshold = "현재 입력조건에서는 계산 가능한 범위에서 기준점을 찾지 못했습니다."
    story.append(_table([
        ["목표 마진이 깨지는 USD/KRW 기준점", "Zero-profit USD/KRW 기준점"],
        [
            f"{report.target_margin_threshold:,.2f}" if report.target_margin_threshold is not None else missing_threshold,
            f"{report.zero_profit_threshold:,.2f}" if report.zero_profit_threshold is not None else missing_threshold,
        ],
    ], [89 * mm, 89 * mm]))
    story.append(_p("계산 기준점이며 환율 전망이 아닙니다.", styles["small"]))

    story.extend([PageBreak(), _p("5. Funding / receivable purchase / Banker's Usance", styles["section"])])
    if report.company_funding is not None:
        funding = report.company_funding
        choice_labels = {
            FundingChoice.INTERNAL_CASH_ONLY: "회사자금만",
            FundingChoice.WAIT_WITH_CREDIT_LINE: "기존 운전자금 한도",
            FundingChoice.EARLY_RECEIVABLE_PURCHASE: "매출채권 조기현금화",
        }
        rows = [["자금조달 비교", "상태", "최대 은행 필요액", "총 금융비용"]]
        for choice in funding.choices:
            rows.append([
                choice_labels[choice.choice], choice.status.value,
                _krw_millions(choice.required_external_funding_krw),
                "산정 없음" if choice.total_financing_cost_krw is None else _krw_millions(choice.total_financing_cost_krw),
            ])
        story.append(_table(rows, [43 * mm, 32 * mm, 50 * mm, 53 * mm]))
    if report.deal.sale.payment_method is PaymentMethod.TT:
        story.append(_p("TT 거래의 조기 매출채권 현금화 비교는 v0.1 범위 밖입니다.", styles["body"]))
    elif report.purchase_result is None or report.purchase_result.receivable_purchase is None:
        story.append(_p("현재 입력조건에서는 조기 매출채권 현금화 비교 결과를 생성하지 못했습니다.", styles["body"]))
    else:
        purchase = report.purchase_result.receivable_purchase
        story.append(_table([
            ["구분", "고객 입금일까지 기다리기", "매출채권 먼저 현금화하기"],
            ["현금 확보일", f"D+{report.base_result.collection_day}", f"D+{purchase.purchase_day}"],
            ["금융비용 반영 마진", _percent(report.base_result.financing_adjusted_deal_margin), _percent(report.purchase_result.financing_adjusted_deal_margin)],
            ["최대 외부차입", _krw_millions(report.base_result.funding.maximum_external_borrowing_krw), _krw_millions(report.purchase_result.funding.maximum_external_borrowing_krw)],
            ["외부 금융비용", _krw_millions(report.base_result.funding.external_funding_cost_krw), _krw_millions(report.purchase_result.funding.external_funding_cost_krw)],
            ["할인비용", "해당 없음", _krw_millions(purchase.discount_cost_krw)],
            ["수수료", "해당 없음", _krw_millions(purchase.purchase_fee_krw)],
        ], [40 * mm, 69 * mm, 69 * mm]))
        story.append(_p("먼저 현금화하면 자금을 더 일찍 확보할 수 있지만 할인비용과 수수료가 추가됩니다.", styles["small"]))

    if report.bankers_usance is not None:
        comparison = report.bankers_usance
        usance = comparison.usance
        story.extend([
            _p("Banker's Usance", styles["section"]),
            _table([
                ["공급자 지급 / 회사 상환", "일반 운전자금 Peak", "은행 신용 원금 Peak", "금융비용 차이"],
                [
                    f"D+{usance.supplier_payment_day} / D+{usance.company_repayment_day}",
                    f"{_krw_millions(comparison.base_working_capital_credit_krw)} -> {_krw_millions(usance.peak_working_capital_credit_krw)}",
                    _krw_millions(usance.peak_combined_bank_principal_krw),
                    _krw_millions(comparison.financing_cost_difference_krw),
                ],
            ], [43 * mm, 52 * mm, 45 * mm, 38 * mm]),
            _p("일반 운전자금 사용 감소는 총 은행 원금채무가 사라진다는 뜻이 아니며, 승인·실행을 판단하지 않습니다.", styles["small"]),
        ])

    story.append(_p("6. FX Treasury", styles["section"]))
    if report.fx_treasury is None:
        story.append(_p("현재 조건 기준 FX Treasury 요약 없음", styles["body"]))
    else:
        position_rows = [["통화", "수취", "지급", "금액 기준 상계", "순노출 / 불리한 방향"]]
        for position in report.fx_treasury.positions:
            position_rows.append([
                position.currency.value,
                _amount(position.receivable_amount),
                _amount(position.payable_amount),
                _amount(position.amount_offset),
                f"{position.net_exposure:+,.0f} / {position.unfavorable_direction.value}",
            ])
        overlay = report.fx_treasury.settlement_scenario_overlay
        story.extend([
            _table(position_rows, [22 * mm, 34 * mm, 34 * mm, 40 * mm, 48 * mm]),
            _p(
                f"사용자 입력 정산환율 시나리오: 헤지효과 {_krw_millions(overlay.hedge_effect_krw)} / "
                f"미헤지 마진 {_percent(overlay.unhedged_margin)} / overlay 마진 {_percent(overlay.simulated_margin_after_hedge)}",
                styles["body"],
            ),
            _p("선물환 quote와 정산환율은 사용자 선택 가정입니다. 환율예측·헤지 권고가 아니며, 금액 기준 상계는 시점 일치 헤지를 뜻하지 않습니다.", styles["small"]),
        ])

    story.append(_p("7. 거래 검토 요약", styles["section"]))
    if report.review_is_current and report.review_memo is not None:
        focus_labels = {
            TreasuryFocus.CREDIT_LINE_CAPACITY: "운전자금 한도 수용력",
            TreasuryFocus.FUNDING_OPTIONS: "자금조달 비교",
            TreasuryFocus.FX_EXPOSURE: "통화별 외화노출",
            TreasuryFocus.FORWARD_HEDGE: "선물환 시뮬레이션",
            TreasuryFocus.BANKERS_USANCE: "Banker's Usance",
        }
        signal_labels = {
            SupportingSignal.CURRENT_MARGIN: "현재 마진",
            SupportingSignal.FX_RESILIENCE: "환율 회복력",
            SupportingSignal.FUNDING_BURDEN: "자금 부담",
            SupportingSignal.COMBINED_STRESS: "복합 악화 시나리오",
            SupportingSignal.SALE_PRICE_BOUNDARY: "수출가격 경계",
            SupportingSignal.USD_COST_BOUNDARY: "USD 원가 경계",
            SupportingSignal.JPY_COST_BOUNDARY: "JPY 원가 경계",
            SupportingSignal.COLLECTION_DAY_BOUNDARY: "회수일 경계",
            SupportingSignal.FUNDING_RATE_BOUNDARY: "조달금리 경계",
        }
        tool_labels = {
            "read_current_deal_analysis": "현재 거래 분석",
            "read_stress_and_rescue": "Stress / 목표마진 충족 조건",
            "read_treasury_context": "회사 자금 / 자금조달 / 외화위험",
            "read_payment_context": "K-SURE 결제 참고정보 확인",
        }
        memo = report.review_memo
        story.extend([
            _p(escape(memo.headline), styles["body"]),
            _p(escape(memo.summary), styles["body"]),
            _p(f"우선 검토 주제: {focus_labels[memo.treasury_focus]}", styles["small"]),
            _p("함께 본 근거: " + ", ".join(signal_labels[item] for item in memo.supporting_signals), styles["small"]),
            _p("사용한 분석 도구: " + ", ".join(tool_labels.get(item, item) for item in report.review_used_tools), styles["small"]),
        ])
    else:
        story.append(_p("현재 조건 기준 거래 검토 요약 없음", styles["body"]))

    story.append(_p("8. 공식 데이터 / 출처 / 제한", styles["section"]))
    context_rows = []
    if report.fx_reference is not None:
        context_rows.append([
            "한국수출입은행",
            f"기준일 {report.fx_reference.reference_date.isoformat()} / USD/KRW {report.fx_reference.usd_krw} / JPY/KRW(100 JPY) {report.fx_reference.jpy_krw_per_100}",
            "Observed official data",
        ])
    if report.payment_context is not None:
        context = report.payment_context
        avg = "n/a" if context.average_payment_period_days is None else f"{context.average_payment_period_days}일"
        late = "n/a" if context.late_payment_rate_percent is None else f"{context.late_payment_rate_percent}%"
        delay = "n/a" if context.average_late_payment_period_days is None else f"{context.average_late_payment_period_days}일"
        context_rows.append([
            "K-SURE 결제 참고정보",
            f"기준년도 {context.reference_year} / 평균 결제기간 {avg} / 지연결제율 {late} / 평균 지연기간 {delay}<br/>국가/산업 집계 Context",
            "Observed official aggregate data",
        ])
    if context_rows:
        story.append(_table([["출처", "관측값", "구분"]] + context_rows, [33 * mm, 105 * mm, 40 * mm]))
    else:
        story.append(_p("이 보고서 생성 시점에 불러온 공식 데이터 없음", styles["body"]))

    ai_provenance = (
        report_basis_text(report.ai_provenance_status, report.ai_analysis_exists)
    )
    official_context = official_context_text(
        report.fx_reference,
        report.payment_context,
    )
    provenance = [
        ["구분", "이 보고서의 근거"],
        ["User-entered / Treasury-confirmed fact", "현재 거래조건, 현재 가용현금, 최소 운영자금, 한도와 사용자 시나리오"],
        ["ERP-imported company cash-plan event", "표준 CSV에서 가져온 이벤트는 ERP_IMPORT 출처를 유지"],
        ["AI-extracted document fact", ai_provenance],
        ["Observed official aggregate data", official_context],
        ["Stress / user scenario assumption", "복합 악화, 조기현금화, 선물환, Usance의 명시적 가정"],
        ["Deterministic calculated result", "Deal economics, Company Liquidity, Funding, FX, Usance, Rescue"],
        ["Current AI review summary", "현재 검토만 포함" if report.review_is_current and report.review_memo is not None else "포함 없음"],
    ]
    story.extend([
        _p("데이터 출처와 성격", styles["section"]),
        _table(provenance, [51 * mm, 127 * mm]),
        Spacer(1, 2 * mm),
        _p(
            "본 보고서는 거래 전 금융 의사결정을 돕기 위한 사전점검 자료입니다. "
            "은행의 여신승인, 무역보험 인수, 환율예측, 회계·세무 보고서 또는 법률의견을 의미하지 않습니다. "
            "실제 금융조건 및 계약조건은 해당 금융기관과 회사 내부 담당자가 확인해야 합니다.",
            styles["small"],
        ),
    ])
    document.build(story, onFirstPage=_footer, onLaterPages=_footer)
    return buffer.getvalue()
