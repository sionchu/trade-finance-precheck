# 수출거래 AI 금융진단 — Product Specification

Status: Canonical current-state product specification  
Purpose: 2026 금융 AI Challenge MVP  
Scope: One export deal in company-liquidity and currency context. Deterministic finance first.

---

## 1. Product thesis

수출거래 AI 금융진단은 수출계약 체결 전에 거래 수익성, 회사 전체 자금흐름, 외화노출을 함께 보고 대응 조건을 비교하는 B2B 금융 의사결정 지원 서비스다.

핵심 질문은 다음 두 가지다.

> 이 거래가 돈을 필요로 하는 시점에 회사가 실제로 버틸 수 있는가?

> 부족한 자금과 외화위험을 어떤 금융조건으로 검토할 수 있는가?

이 제품은 금융상품 실행 플랫폼이 아니다. 대출 승인, 송금, 환율 예측, 헤지 주문, 보험·보증 실행, 바이어 부도 예측을 수행하지 않는다.

초기 사용자는 한국의 수출입 중소·중견 제조기업 재무·자금 담당자다. Corporate RM, Trade Finance, Transaction Banking, FX 담당자는 기업과 동일한 진단 근거를 공유하는 2차 활용자다.

---

## 2. Public product contract

Public product name:

`수출거래 AI 금융진단`

Subtitle:

`계약 전 수익성·회사 자금·환위험을 한 화면에서 비교합니다.`

Public views are exactly:

```text
입력 | 분석 | 보고서
```

Default view is `분석`.

### 입력

- 거래조건 요약과 회사 자금정보를 먼저 보여준다.
- 원시 숫자 입력은 사용자가 `정보 수정`을 열 때만 노출한다.
- 직접 입력 또는 거래서류 AI 분석을 통해 현재 거래값을 반영할 수 있다.
- 거래서류 업로드가 지원하는 역할은 Sales Contract, USD Supplier PO, JPY Supplier PO다.
- 회사 자금계획은 직접 편집하거나 표준 ERP export CSV를 불러올 수 있다.
- Financial Statement AI는 bundled fictional KRW statement를 사용자가 명시적으로 실행할 때만 읽는다.

### 분석

- 결정론적 현재 판단 문장이 가장 먼저 나온다.
- `이번 거래 필요 외부자금 → 회사 전체 최대 자금부족 → 현재 한도 반영 후 남는 부족`을 하나의 관계로 보여준다.
- Company Liquidity Timeline을 주요 근거 시각화로 제공한다.
- preset scenario는 Base와 이미 계산된 deterministic Stress 결과를 선택해 비교한다.
- `기본`, `USD -5%`, `JPY +10%`, `금리 +1%p`, `회수 +30일`, `복합 악화`, `직접 설정`을 제공한다.
- preset scenario에는 별도 계산 버튼이 없다.
- 직접 설정은 정확 입력 필드만 사용하며 slider를 사용하지 않는다.
- 대응안은 기존 운전자금, 매출채권 조기 현금화, 선물환, Banker's Usance의 `현재 → 대안 → 변화`를 비교한다.

### 보고서

- 현재 결정론적 결과 요약을 먼저 보여준다.
- Single Deal Review Agent는 선택적 후순위 기능이다.
- current review만 PDF에 포함하며 stale review는 제외한다.
- 현재 조건의 `수출거래 AI 금융진단 보고서`를 인메모리 PDF로 생성한다.

---

## 3. Authoritative architecture

```text
User / Demo / Uploaded PDFs / ERP CSV
                  ↓
                app.py
        Streamlit application state
                  ↓
 ┌────────────────┼────────────────┐
 ↓                ↓                ↓
AI               Finance          External
Extraction       Deterministic    Reference
Explanation      Engine           Context
 ↓                ↓                ↓
 └──────────── current evidence ───┘
                  ↓
             Analysis UI
                  ↓
        Optional read-only Agent
                  ↓
              PDF Report
```

Authority rules:

1. Python deterministic finance is the source of truth for every authoritative financial number.
2. React owns three-view navigation only and performs no finance calculation.
3. AI may extract supported facts or explain already-computed evidence; it never becomes the authoritative calculator.
4. External APIs remain outside finance calculations. External failure must not break core deterministic analysis.
5. User-entered or user-confirmed company facts remain authoritative where no reliable official source exists.

---

## 4. Canonical reference case

Company:

- Korean mid-sized machinery-component manufacturer
- US OEM export
- USD raw-material purchase
- JPY precision-component purchase
- no dedicated Treasury organization

Export sale:

| Field | Value |
|---|---:|
| Currency | USD |
| Amount | 100,000 |
| Payment method | O/A |
| Collection | D+90 |

Foreign payables:

| Item | Currency | Amount | Payment |
|---|---|---:|---:|
| US raw material | USD | 20,000 | D+30 |
| Japan component | JPY | 3,000,000 | D+30 |

KRW costs:

| Item | Amount | Payment |
|---|---:|---:|
| Domestic production advance | KRW 30,000,000 | D+0 |
| Domestic production balance | KRW 25,000,000 | D+30 |
| Logistics / customs | KRW 9,000,000 | D+60 |

Financial assumptions:

| Field | Value |
|---|---:|
| USD/KRW | 1,400 |
| JPY/KRW | 900 KRW / 100 JPY |
| Deal-allocated company cash | KRW 50,000,000 |
| Annual funding rate | 4.8% |
| Target financing-adjusted Deal Margin | 14.0% |

Company liquidity context:

| Field | Value |
|---|---:|
| Current usable company cash | KRW 120,000,000 |
| Minimum operating cash | KRW 70,000,000 |
| Working-capital total line | KRW 100,000,000 |
| Used amount | KRW 30,000,000 |
| Unused line | KRW 70,000,000 |

Canonical company cash-plan events are defined in `app.py` and tests. Prospective Deal cashflow is overlaid from the finance engine and must not be duplicated in the company plan.

---

## 5. Canonical deterministic outputs

Base:

```text
Export sales                           140.000M KRW
Non-funding cost                       119.000M KRW
Gross Deal Profit                       21.000M KRW
Gross Deal Margin                       15.00%
Maximum external borrowing              69.000M KRW
External funding cost                    0.509M KRW
Financing-adjusted Deal Profit          20.491M KRW
Financing-adjusted Deal Margin          14.64%
USD exposure                           +80,000 USD
JPY exposure                        -3,000,000 JPY
```

Company-aware signature:

```text
이번 거래 필요 외부자금          69M KRW
→ 회사 전체 최대 자금부족        89M KRW
→ 현재 미사용 한도                70M KRW
→ 현재 한도 반영 후 남는 부족     19M KRW
Peak                         2026-11-03 / D+60
```

Canonical Stress:

| Scenario | Margin | Max external borrowing | Funding cost | Collection |
|---|---:|---:|---:|---:|
| Base | 14.64% | 69.0M | 0.509M | D+90 |
| USD -5% | 11.20% | 67.6M | 0.498M | D+90 |
| JPY +10% | 12.69% | 71.7M | 0.530M | D+90 |
| Funding +1%p | 14.56% | 69.0M | 0.615M | D+90 |
| Buyer delay +30d | 14.44% | 69.0M | 0.781M | D+120 |
| Combined | 8.83% | 70.3M | 0.962M | D+120 |

Thresholds are deterministic boundaries, never forecasts.

Reference USD/KRW thresholds are approximately:

```text
zero-profit threshold  ≈ 1,143
14% target threshold   ≈ 1,386
```

---

## 6. Finance boundaries

### Deal Economics

The frozen engine calculates:

- dated Deal cashflow
- gross Deal profit and margin
- external borrowing schedule
- funding interest
- financing-adjusted Deal profit and margin
- currency exposure
- canonical Stress scenarios
- target / break-even USD/KRW thresholds

Supported core Deal payment methods are OA and TT.

Supported currencies are KRW, USD and JPY.

### Company Liquidity

Company-wide liquidity uses:

- user-selected review date
- company-confirmed currently usable cash
- minimum operating-cash buffer
- existing confirmed company cash-plan events
- optional EXPECTED events only when explicitly included
- prospective Deal cashflow from the deterministic Deal engine

`DealCase.available_cash_krw` is Deal-allocated company cash and remains distinct from company-wide current usable cash.

Working-capital unused line is derived from total line minus used amount. It is not separately editable.

Company liquidity gap is not bank approval, credit capacity prediction, default probability or a recommendation.

### Receivable early purchase

The feature models the economics of monetizing one O/A receivable before maturity.

Canonical demo:

```text
buyer collection        D+90
purchase day            D+65
discount rate           5.2% annual
fee rate                0.15%
```

It may improve timing while increasing explicit cost and does not necessarily reduce peak funding.

### FX Treasury / Forward

The engine:

- separates USD and JPY exposure
- distinguishes amount-level natural offset from timing alignment
- uses only user-supplied forward quotes and settlement spots
- calculates hedged notional, residual exposure and deterministic settlement effect

It does not forecast FX, recommend a hedge ratio, execute a hedge or infer bank quotes.

### Banker's Usance

Banker's Usance is a narrow financing overlay on one selected foreign payable.

It compares ordinary working-capital usage with separate Usance principal, rate and fee assumptions.

A reduction in ordinary working-capital use does not mean total bank principal disappears.

It is not a payment-method enum, a complete L/C / UPAS workflow, an approval prediction or an automatic FX hedge.

---

## 7. AI contract

AI has exactly three product roles.

### 7.1 Trade Document Financialization

Supported public upload roles:

- Sales Contract PDF
- USD Supplier PO PDF
- JPY Supplier PO PDF

The model extracts document-supported facts only. Missing facts stay missing. It must not calculate margin, FX exposure, funding need or working-capital requirements.

The extracted proposal is validated deterministically and must be user-reviewed before applying.

### 7.2 Financial Statement Financialization

The current MVP reads the bundled fictional KRW financial statement only after an explicit user action.

It extracts nine source-grounded facts:

- cash and cash equivalents
- short-term financial instruments
- accounts receivable
- inventory
- current assets
- current liabilities
- short-term borrowings
- finance cost
- operating cash flow

It must not infer ratios, Deal-available cash, bank lending capacity, credit approval, credit score, default risk or future cash flow.

### 7.3 Single Deal Review Agent

The Agent is a bounded one-shot explanation layer.

Exactly four local read-only tools:

1. `read_current_deal_analysis`
2. `read_stress_and_rescue`
3. `read_treasury_context`
4. `read_payment_context`

A successful run uses exactly two model requests and no retry.

The first request must call each tool exactly once. The second request produces a strict structured memo.

The Agent:

- performs no authoritative calculation
- performs no external fetch
- does not mutate the Deal
- does not execute finance
- does not retain conversation history
- does not predict FX, rates, buyer default or bank approval
- does not recommend or rank products

Authoritative numeric evidence remains deterministic UI output. AI headline and summary contain no numeric characters.

---

## 8. External data contract

### K-SURE

Implemented optional public context.

- user explicitly requests the fetch
- context is country + industry aggregate payment information
- aggregate context is not buyer-specific default probability or a credit score
- it does not automatically change Deal collection terms
- core deterministic analysis works without it

### Korea Eximbank reference FX

Adapter exists and passed local live validation.

Public Streamlit runtime path remains disabled because reliability in that target environment was not proven.

It must not be presented as a forecast or execution quote.

### Bank of Korea ECOS

Funding benchmark / macro concept was validated during product research but remains deferred. No public ECOS adapter is implemented.

### OpenDART and other providers

Not implemented in the current MVP.

Official structured data may be considered in commercialization, but no future provider is part of the present product contract.

---

## 9. Security and privacy boundary

The current public MVP is a competition demonstration, not an enterprise document vault.

- bundled demonstration documents and ERP data are fictional
- the repository has no persistent application database or authentication layer
- when a user explicitly runs Trade Document AI or Financial Statement AI, the selected PDF content is sent to the configured OpenAI API for structured extraction
- those OpenAI requests are issued with `store=False`
- the deterministic finance engine does not require OpenAI or public-data keys
- public-demo users should not upload real trade secrets, personal information or confidential corporate documents

Commercial deployment would require an explicit enterprise security design including data-retention policy, tenant isolation, encryption, authorization, audit logging, secret management, provider governance and AI security testing.

Do not claim zero leakage risk, complete deletion guarantees or enterprise-grade confidentiality for the public MVP.

---

## 10. Report contract

The PDF report is generated in memory from current deterministic evidence.

It may include:

- current Deal inputs
- Base and canonical Stress results
- target / break-even thresholds
- company liquidity timeline and current-line capacity
- funding options
- FX Treasury evidence
- Banker's Usance comparison
- current K-SURE context if loaded
- current Agent memo and used tools only when freshness is current

It must exclude stale AI prose.

Public report title:

`수출거래 AI 금융진단 보고서`

The current target is at most three pages.

---

## 11. Deferred / commercialization scope

Not implemented in the current MVP:

- database and authentication
- live ERP / accounting / TMS integration
- real bank-account connectivity
- OpenDART integration
- BOK ECOS public integration
- public Korea Eximbank FX retrieval
- L/C, UPAS, D/A and D/P full workflows
- insurance / guarantee execution
- actual receivable purchase, hedge, loan or payment execution
- bank approval prediction
- buyer-default prediction
- FX / interest-rate forecasting
- stochastic CFaR / Monte Carlo models
- RAG or arbitrary web search
- multi-agent architecture
- EUR / CNY engine expansion

A commercialization path may progressively add governed official-data and enterprise-system integrations while preserving the same authority rule:

```text
structured / official data when available
        ↓
deterministic finance
        ↓
AI extraction / explanation as bounded assistance
        ↓
human / financial-institution final decision and execution
```

---

## 12. Verification contract

Local deterministic analysis must work without `OPENAI_API_KEY`, `KSURE_SERVICE_KEY` or Eximbank credentials.

Canonical verification commands:

```powershell
python -m unittest discover -s tests -v
python -m compileall -q src tests app.py components
```

Frontend source changes require:

```powershell
cd components\trade_treasury_experience\frontend
npm ci
npm run typecheck
npm run build
```

Canonical public acceptance values:

```text
Base margin                  14.64%
Deal external borrowing      69M KRW
Company peak gap             89M KRW
Unused line                  70M KRW
Residual gap                 19M KRW
Peak date                    2026-11-03 / D+60
USD -5% margin               11.20%
Combined margin               8.83%
```

Public Agent acceptance:

```text
4 read-only tools
2 model requests
0 retries
```

No test or deployment result may be reported as passed unless it was actually executed.
