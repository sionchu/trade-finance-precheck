# 수출거래 AI 금융진단

계약 전 수익성·회사 자금·환위험을 한 화면에서 비교하는 B2B 금융 의사결정 지원 MVP입니다.

Canonical product specification: [`docs/product-spec.md`](docs/product-spec.md)  
Submission-facing factual source: [`docs/submission.md`](docs/submission.md)

## What it does

The product evaluates one export Deal together with company-wide liquidity and currency exposure.

Public views:

```text
입력 | 분석 | 보고서
```

Default view is `분석`.

The canonical demo shows:

```text
현재 마진                    14.64%
이번 거래 필요 외부자금        6,900만원
회사 전체 최대 자금부족        8,900만원
현재 미사용 한도               7,000만원
현재 한도 반영 후 남는 부족     1,900만원
최대 부족일                   2026-11-03 / D+60
USD -5% margin               11.20%
복합 악화 margin               8.83%
```

## Product architecture

```text
User / Demo / PDFs / ERP CSV
             ↓
           app.py
             ↓
 ┌───────────┼───────────┐
 ↓           ↓           ↓
AI          Finance     External
             ↓
        Analysis UI
             ↓
 Optional read-only Agent
             ↓
          PDF Report
```

Python deterministic finance is authoritative for every financial number.

React owns only the `입력 | 분석 | 보고서` navigation. AI extracts supported facts or explains already-computed evidence; it never becomes the authoritative financial calculator.

## Implemented scope

- deterministic Deal economics and dated cashflow
- financing-adjusted Deal Margin
- canonical FX / rate / payment-delay Stress scenarios
- deterministic USD/KRW target and break-even thresholds
- Company Liquidity Timeline
- company funding capacity against current working-capital line
- O/A receivable early-purchase comparison
- currency-level USD / JPY exposure and natural offset
- user-assumption Forward Hedge simulation
- Banker's Usance financing comparison
- Trade Document Financialization
- Financial Statement Financialization
- bounded Single Deal Review Agent
- optional K-SURE aggregate payment context
- in-memory PDF report
- responsive Dashboard-First Streamlit UI with internal React navigation

## AI roles

Exactly three product AI roles exist.

### Trade Document Financialization

The public app supports three explicit PDF roles:

- Sales Contract
- USD Supplier PO
- JPY Supplier PO

The model extracts document-supported trade facts only. It does not calculate margin, FX exposure or funding need. Extracted values are validated and user-reviewed before applying.

### Financial Statement Financialization

The current MVP reads the bundled fictional KRW statement after an explicit user action and exposes nine source-grounded liquidity facts.

It does not infer ratios, Deal-available cash, bank lending capacity, credit approval, credit score, default risk or future cash flow.

### Single Deal Review Agent

The Agent is one-shot and read-only.

- exactly four local evidence tools
- exactly two model requests on success
- no retry
- no external fetch
- no authoritative calculation
- no product recommendation or ranking

Current deterministic numbers remain rendered separately by the application.

## External data

### K-SURE

Implemented as optional country + industry aggregate payment context. It is fetched only after an explicit user action and never becomes buyer-specific default probability or a credit score.

### Korea Eximbank reference FX

The adapter passed local live validation but remains disabled in the public Streamlit path because target-environment reliability was not proven.

### Bank of Korea ECOS / OpenDART

Not implemented in the public MVP.

Core deterministic analysis does not require any public-data API.

## Security note for the public demo

Bundled demonstration contracts, POs, financial statement and ERP CSV are fictional.

The MVP has no persistent application database or authentication layer.

When a user explicitly runs Trade Document AI or Financial Statement AI, the selected PDF content is sent to the configured OpenAI API for structured extraction. Those requests use `store=False`.

The public competition deployment is not an enterprise document vault. Do not upload real trade secrets, personal information or confidential corporate documents to the public demo.

See `docs/product-spec.md` for the exact current security boundary and commercialization-only controls.

## Deferred scope

Not part of the current MVP:

- live ERP / accounting / TMS / bank integration
- database / authentication
- public Eximbank FX / ECOS / OpenDART integration
- L/C / UPAS / D/A / D/P full workflows
- insurance / guarantee execution
- actual hedge / loan / payment execution
- bank approval or buyer-default prediction
- FX / interest-rate forecasting
- stochastic CFaR / Monte Carlo risk models
- RAG / arbitrary web search
- multi-agent systems
- EUR / CNY engine expansion

## Local run

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Optional environment variables:

```text
OPENAI_API_KEY      document/statement AI and one-shot Deal Review Agent
KSURE_SERVICE_KEY   optional K-SURE aggregate payment context
```

The deterministic analysis runs without either variable.

## Frontend build

The React navigation component is prebuilt and committed for Streamlit Community Cloud.

```powershell
cd components\trade_treasury_experience\frontend
npm ci
npm run typecheck
npm run build
```

Do not hand-edit compiled frontend assets.

## Tests

```powershell
python -m unittest discover -s tests -v
python -m compileall -q src tests app.py components
git diff --check
```

Do not report a test, browser check, Agent run, API call or PDF inspection as passed unless it was actually executed.
