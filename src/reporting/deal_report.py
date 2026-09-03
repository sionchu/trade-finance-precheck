from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from io import BytesIO

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

from src.domain.deal_case import Currency, DealCase, FxRates, PaymentMethod
from src.external.eximbank_fx import FxReferenceSnapshot
from src.external.ksure_payment import PaymentContext
from src.finance.engine import DealResult, Scenario


FONT_NAME = "HYGothic-Medium"
NAVY = colors.HexColor("#163A5F")
INK = colors.HexColor("#17212B")
MUTED = colors.HexColor("#5E6B78")
LINE = colors.HexColor("#D9E1E8")
PALE_BLUE = colors.HexColor("#EEF4F8")
PALE_GREEN = colors.HexColor("#EAF6EF")
PALE_RED = colors.HexColor("#FBEDEE")
PALE_AMBER = colors.HexColor("#FFF5DF")


@dataclass(frozen=True)
class DealReportInput:
    generated_at: datetime
    deal: DealCase
    fx: FxRates
    base_result: DealResult
    scenario_results: tuple[tuple[Scenario, DealResult], ...]
    zero_profit_threshold: Decimal | None
    target_margin_threshold: Decimal | None
    purchase_result: DealResult | None = None
    fx_reference: FxReferenceSnapshot | None = None
    payment_context: PaymentContext | None = None
    ai_analysis_exists: bool = False
    ai_patch_applied: bool = False
    hedge_confirmed: bool = False


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
        Scenario.COMBINED: "복합 Stress",
    }[scenario]


def _footer(canvas, document) -> None:
    canvas.saveState()
    canvas.setFont(FONT_NAME, 7)
    canvas.setFillColor(MUTED)
    canvas.drawString(18 * mm, 10 * mm, "AI Trade Finance Pre-check / 분석용 사전점검")
    canvas.drawRightString(192 * mm, 10 * mm, f"{document.page}")
    canvas.restoreState()


def build_deal_report(report: DealReportInput) -> bytes:
    """Render already-computed deterministic analysis as an in-memory PDF."""
    pdfmetrics.registerFont(UnicodeCIDFont(FONT_NAME))
    styles = _styles()
    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer, pagesize=A4, leftMargin=16 * mm, rightMargin=16 * mm,
        topMargin=14 * mm, bottomMargin=16 * mm,
        title="거래 금융 사전점검 보고서", author="AI Trade Finance Pre-check",
    )
    story = []
    basis = "거래서류 AI 추출값 일부 반영" if report.ai_patch_applied else "사용자 입력 기반 분석"
    story.extend([
        _p("AI Trade Finance Pre-check", styles["subtitle"]),
        _p("거래 금융 사전점검 보고서", styles["title"]),
        _p(
            f"생성시각 {report.generated_at.astimezone().strftime('%Y-%m-%d %H:%M %Z')} / "
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
        _p("1. 핵심 자금 지표", styles["section"]),
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
    story.append(_p(f"자금 부담이 가장 큰 시점: D+{peak_point.day} / 목표 마진 {_percent(report.deal.target_margin)}", styles["small"]))

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
        _p("2. 돈의 흐름과 환노출", styles["section"]),
        _table([
            ["받을 돈", "낼 돈", "환율에 노출된 금액"],
            [_p(receivable, styles["body"]), _p(payable_lines, styles["body"]), _p("<br/>".join(exposure_lines), styles["body"])],
        ], [48 * mm, 55 * mm, 75 * mm]),
        _p("3. Stress 요약", styles["section"]),
        _p("아래 값은 Stress 가정이며 환율·입금 시점에 대한 예측이 아닙니다.", styles["small"]),
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
        PageBreak(),
        _p("4. USD/KRW 계산 기준점", styles["section"]),
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

    story.append(_p("5. 매출채권 현금화 비교", styles["section"]))
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

    story.append(_p("6. 공식 시장 Context", styles["section"]))
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
            "K-SURE",
            f"기준년도 {context.reference_year} / 평균 결제기간 {avg} / 지연결제율 {late} / 평균 지연기간 {delay}<br/>국가/산업 집계 Context",
            "Observed official aggregate data",
        ])
    if context_rows:
        story.append(_table([["출처", "관측값", "구분"]] + context_rows, [33 * mm, 105 * mm, 40 * mm]))
    else:
        story.append(_p("공식 시장 Context가 이 보고서 생성 시점에 불러와지지 않았습니다.", styles["body"]))

    confirmations = []
    if report.ai_patch_applied:
        confirmations.append("AI 제안 적용")
    if report.hedge_confirmed:
        confirmations.append("환헤지 확인")
    ai_provenance = (
        "Deal 입력에 반영"
        if report.ai_patch_applied
        else "분석 결과 존재(Deal 미반영)"
        if report.ai_analysis_exists
        else "사용하지 않음"
    )
    provenance = [
        ["구분", "이 보고서의 근거"],
        ["Observed official data", "불러온 Eximbank / K-SURE Context" if context_rows else "이 세션에 불러온 값 없음"],
        ["AI extracted from document", ai_provenance],
        ["User confirmed", " / ".join(confirmations) if confirmations else "해당 없음"],
        ["User-entered fact", "사내 가용자금, 실제 조달금리, 목표 마진, 편집한 거래조건"],
        ["Demo assumption", "사용자가 변경하지 않은 기준 Deal 입력"],
        ["Stress assumption", "USD -5%, JPY +10%, 금리 +1%p, 입금 +30일"],
        ["Calculated result", "마진, 자금소요, 외부차입, 환노출, 기준점"],
    ]
    story.extend([
        _p("7. 데이터 출처와 성격", styles["section"]),
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
