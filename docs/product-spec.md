AI Trade Finance Pre-check — Product Spec v0.1

Status: Canonical implementation and product specification
Purpose: 2026 금융 AI Challenge MVP
Scope rule: One export deal. Deterministic finance first.
Last updated: 2026-09-03

────────

Implementation State

FROZEN / IMPLEMENTED:

• Financial Engine v0.1
• K-SURE aggregate payment context
• Korea Eximbank official reference FX

VALIDATED / DEFERRED:

• Bank of Korea ECOS funding benchmark / macro context

NEXT GATE:

• End-to-End Web MVP

────────

0. Canonical Scope and Model

Canonical model principle:

> A trade deal is not financially complete if the engine only calculates FX and an abstract funding-rate cost.

The canonical model separates:

1. Deal economics — sales, foreign inputs, KRW costs
2. Liquidity requirement — how much cash the deal requires and when
3. External financing — how much must actually be borrowed after available company cash
4. Receivable monetization — wait for the buyer or sell/purchase the receivable early
5. Risk-transfer context — insurance / guarantee / FX-cover as later option simulations

The project is not a trade-finance platform.

Financial Engine v0.1 includes:

• Base Deal
• External working-capital financing
• O/A receivable held to maturity
• O/A receivable early-purchase simulation
• FX / rate / payment-delay stress

Insurance, guarantees and FX cover remain deferred product options.

────────

1. Product Thesis

Problem

A Korean export-oriented SME or mid-sized manufacturer can sign a profitable-looking contract and still experience a poor financial outcome because the sales price is only one part of the deal.

The company must finance production before collection and may simultaneously carry:

• export FX exposure,
• imported-material FX exposure,
• delayed buyer payment,
• working-capital borrowing,
• receivable-discount / negotiation cost,
• buyer credit risk,
• hedge / insurance / guarantee decisions.

These facts are often split across contracts, invoices, spreadsheets, ERP, banks and K-SURE.

Canonical Question

> **“If we accept this deal on these payment terms, will its margin and liquidity still hold under FX, delayed collection and funding stress?”**

Target User

Initial target:

• Korean export/import SME or mid-sized manufacturer
• CEO / CFO / finance team / overseas sales / trade operations
• companies without a dedicated treasury-risk platform

Position

This is a pre-deal decision layer, not an execution layer.

The MVP does not:

• transfer money,
• open an L/C,
• purchase a bill in a real bank,
• issue insurance,
• approve a loan,
• approve a guarantee,
• predict FX,
• predict rates,
• predict buyer default.

────────

2. Canonical User Journey

```text
PO / Contract / Invoice
        ↓
DealCase review
        ↓
Base deal economics
        ↓
Liquidity / external financing need
        ↓
Stress scenarios
        ↓
Wait for receivable
        vs
Early receivable purchase
        ↓
Financial explanation
```

Deferred product options:

```text
Export credit insurance
Export credit guarantee
FX insurance / hedge
```

may be added as option simulations, not execution workflows.

────────

3. Reference DealCase

Every first implementation and test uses this one case.

3.1 Company Context

• Korean mid-sized machinery-component manufacturer
• exports to a US OEM
• imports some USD raw material
• imports a Japanese precision component
• no dedicated treasury organization
• KRW 50,000,000 of internal liquidity can be allocated to this deal

3.2 Export Sale

|Field         |Value      |
|--------------|----------:|
|Buyer country |US         |
|Currency      |USD        |
|Amount        |USD 100,000|
|Payment method|O/A        |
|Collection    |D+90       |

3.3 Foreign Inputs

|Item                     |Currency|Amount   |Payment|
|-------------------------|--------|--------:|------:|
|US raw material          |USD     |20,000   |D+30   |
|Japan precision component|JPY     |3,000,000|D+30   |

3.4 KRW Costs

|Item                          |Amount        |Payment|
|------------------------------|-------------:|------:|
|Domestic production advance   |KRW 30,000,000|D+0    |
|Domestic production balance   |KRW 25,000,000|D+30   |
|Logistics / customs / handling|KRW 9,000,000 |D+60   |

3.5 Financial Assumptions

|Field                                |Value            |
|-------------------------------------|----------------:|
|USD/KRW                              |1,400            |
|JPY/KRW                              |900 KRW / 100 JPY|
|Available company cash for deal      |KRW 50,000,000   |
|External funding rate                |4.8% annual      |
|Target financing-adjusted deal margin|14.0%            |

Reference FX values are demo baselines, not forecasts.

────────

4. Reference Lifecycle

```text
D+0
Sales Contract / PO
Domestic production advance
-30M KRW

D+30
Domestic production balance
USD raw material
JPY component

D+60
Logistics / customs / handling

D+90
Buyer pays O/A receivable
+USD 100,000
```

At the reference FX rates:

```text
D+0      -30.0M KRW

D+30
-25.0M KRW domestic
-28.0M KRW USD input
-27.0M KRW JPY input
= -80.0M

D+60      -9.0M

D+90    +140.0M
```

Cumulative deal cash before financing:

```text
D+0      -30.0M
D+30    -110.0M
D+60    -119.0M   ← peak deal funding requirement
D+90     +21.0M
```

────────

5. Core Domain Model

5.1 DealCase

```text
DealCase
├── sales
│   ├── currency
│   ├── amount
│   ├── payment_method
│   └── collection_day
│
├── foreign_payables[]
│   ├── currency
│   ├── amount
│   └── payment_day
│
├── krw_costs[]
│   ├── amount_krw
│   └── payment_day
│
├── liquidity
│   └── available_cash_krw
│
├── funding
│   └── annual_rate
│
└── target_margin
```

5.2 Required Payment Methods

First engine:

• OA
• TT

Do not implement:

• L/C
• D/A
• D/P

until a later product-spec revision.

5.3 Required Currencies

• KRW
• USD
• JPY

No EUR/CNY in v0.1.

────────

6. Deal Economics

6.1 Currency Conversion

```text
KRW value = foreign amount × settlement FX
```

JPY:

```text
KRW value
= JPY amount × (KRW per 100 JPY / 100)
```

6.2 Gross Deal Profit

```text
Gross Deal Profit
= Export Sales KRW
- Foreign Input Costs KRW
- Domestic KRW Costs
```

Reference:

```text
Sales
100,000 USD × 1,400
= 140.0M KRW

USD input
20,000 × 1,400
= 28.0M

JPY input
3,000,000 × 900 / 100
= 27.0M

Domestic production
= 55.0M

Logistics
= 9.0M

Total cost
= 119.0M

Gross Deal Profit
= 21.0M

Gross Deal Margin
= 15.00%
```

6.3 Currency Exposure

```text
Net Exposure(currency)
= receivables - payables
```

Reference:

```text
USD
+100,000 - 20,000
= +80,000 USD

JPY
0 - 3,000,000
= -3,000,000 JPY
```

Interpretation:

• positive USD exposure: falling USD/KRW hurts the deal
• negative JPY exposure: rising JPY/KRW hurts the deal

────────

7. Liquidity and Working-Capital Financing

7.1 Peak Deal Funding Requirement

Construct dated deal cashflows before financing.

```text
Peak Deal Funding Requirement
= maximum absolute negative cumulative deal cash
```

Reference:

```text
119.0M KRW
```

This is a deal-level liquidity requirement, not company-wide working capital.

7.2 Available Company Cash

The company may allocate internal cash to the deal.

Reference:

```text
Available cash
= 50.0M KRW
```

This internal cash does not generate an explicit interest expense in v0.1.

Do not invent an opportunity-cost rate yet.

7.3 External Borrowing Need

Borrow only when cumulative deal cash demand exceeds allocated internal cash.

At any point:

```text
External Loan Outstanding
= max(
    0,
    absolute negative cumulative deal cash
    - available company cash
  )
```

Reference:

```text
D+0
cash need = 30M
available cash = 50M
loan = 0

D+30
cumulative need = 110M
loan = 60M

D+60
cumulative need = 119M
loan = 69M

D+90
buyer collection received
loan repaid
```

Therefore:

```text
Maximum External Borrowing
= 69.0M KRW
```

7.4 External Funding Cost

For each time interval:

```text
Funding Cost
+= outstanding external loan
 × annual funding rate
 × interval days / 365
```

Reference:

```text
D+30 → D+60
60M × 4.8% × 30/365

D+60 → D+90
69M × 4.8% × 30/365

Total
≈ 0.509M KRW
```

7.5 Financing-adjusted Deal Profit

```text
Financing-adjusted Deal Profit
= Gross Deal Profit
- External Funding Cost
```

Reference:

```text
21.0M - 0.509M
≈ 20.491M KRW
```

7.6 Financing-adjusted Deal Margin

```text
Financing-adjusted Deal Margin
= Financing-adjusted Deal Profit
/ Export Sales KRW
```

Reference:

```text
≈ 14.64%
```

UI terminology:

• Deal Margin
• Financing-adjusted Deal Margin

Do not label it statutory accounting Operating Margin.

────────

8. Stress Engine v0.1

Exactly five stress cases.

8.1 Base

Expected:

```text
Gross Deal Margin                 15.00%
Peak Deal Funding                119.0M
Maximum External Borrowing        69.0M
External Funding Cost             0.509M
Financing-adjusted Deal Margin    14.64%
```

8.2 Scenario A — USD/KRW -5%

```text
1,400 → 1,330
```

Apply to unsettled USD sale and USD payable.

Expected:

```text
Sales                             133.0M
Total non-funding cost            117.6M
Gross Deal Profit                  15.4M
Maximum External Borrowing         67.6M
Funding Cost                        0.498M
Financing-adjusted Deal Margin     11.20%
```

8.3 Scenario B — JPY/KRW +10%

```text
900 → 990 KRW / 100 JPY
```

Expected:

```text
Total non-funding cost            121.7M
Gross Deal Profit                  18.3M
Maximum External Borrowing         71.7M
Funding Cost                        0.530M
Financing-adjusted Deal Margin     12.69%
```

8.4 Scenario C — Funding Rate +1.0%p

```text
4.8% → 5.8%
```

Expected:

```text
Funding Cost                        0.615M
Financing-adjusted Deal Margin     14.56%
```

8.5 Scenario D — Buyer Payment Delay +30 days

```text
D+90 → D+120
```

Expected:

```text
Maximum External Borrowing         69.0M
Funding Cost                        0.781M
Financing-adjusted Deal Margin     14.44%
```

8.6 Scenario E — Combined Stress

```text
USD/KRW        -5%
JPY/KRW       +10%
Funding rate   +1.0%p
Buyer delay   +30 days
```

Expected:

```text
Sales                             133.0M
Total non-funding cost            120.3M
Gross Deal Profit                  12.7M
Maximum External Borrowing         70.3M
Funding Cost                        0.962M
Financing-adjusted Deal Profit     11.738M
Financing-adjusted Deal Margin      8.83%
```

This is the canonical demo stress case.

────────

9. Receivable / Bill Purchase Simulation

This is the first explicit Trade Finance option.

9.1 Scope

The first engine does not implement the legal/documentary lifecycle of:

• a bill of exchange,
• D/A,
• D/P,
• L/C negotiation.

It models one economic decision:

> Hold an O/A export receivable to buyer maturity  
> **vs**  
> monetize the receivable early through a bank-style purchase/discount assumption.

Name the product feature:

```text
EARLY_RECEIVABLE_PURCHASE
```

Do not claim the user is actually eligible for bank purchase.

9.2 Parameters

```text
ReceivablePurchaseOption
├── purchase_day
├── annual_discount_rate
└── fee_rate
```

Canonical demo parameters:

|Field                    |Value           |
|-------------------------|---------------:|
|Purchase day             |D+65            |
|Annual discount rate     |5.2%            |
|Fee rate                 |0.15%           |

These are demo assumptions unless later replaced by official/bank data.

The receivable KRW face value uses the active scenario USD/KRW from the Deal
evaluation. No separate option-level settlement FX exists.

The evaluation resolves one effective collection day from the DealCase or the
active payment-delay scenario. That same day controls buyer cash collection on
the hold path and remaining tenor on the early-purchase path.

9.3 Discount Cost

```text
Remaining Tenor
= effective collection day - purchase day
```

```text
Discount Cost
= receivable KRW face value
× annual discount rate
× remaining tenor / 365
```

9.4 Purchase Fee

```text
Purchase Fee
= receivable KRW face value × fee rate
```

9.5 Net Purchase Proceeds

```text
Net Purchase Proceeds
= receivable KRW face value
- discount cost
- purchase fee
```

9.6 Loan Interaction

When early-purchase proceeds arrive:

1. repay outstanding external deal borrowing first;
2. remaining proceeds increase deal cash;
3. external financing interest stops on the repaid amount.

This interaction is essential.

Do not calculate:

```text
normal full-period loan cost
+
full receivable-purchase cost
```

independently.

The cashflow engine must recompute financing after the early collection event.

────────

10. Reference Financing Comparison

10.1 Wait for Buyer

Reference Base Deal:

```text
Collection
D+90

Maximum External Borrowing
69.0M KRW

External Funding Cost
≈0.509M KRW

Financing-adjusted Deal Margin
≈14.64%
```

10.2 Early Receivable Purchase

Reference assumptions:

```text
Purchase at D+65
Discount rate 5.2%
Fee 0.15%
```

Approximate reference:

```text
Loan interest before D+65
≈0.282M

Receivable discount
≈0.499M

Purchase fee
≈0.210M

Total explicit financing / monetization cost
≈0.991M
```

Interpretation:

• early purchase improves liquidity,
• external borrowing is repaid sooner,
• but explicit transaction cost can be higher than simply waiting.

This trade-off is the product value.

Do not force the product to label one option universally “better.”

────────

11. Delay + Early Purchase

If the buyer contractual/expected collection moves to D+120 while purchase remains available at D+65:

```text
remaining tenor
= 55 days
```

The engine must recalculate:

• higher discount cost,
• shorter external-loan duration,
• liquidity benefit,
• financing-adjusted margin.

This lets the product answer:

> “When buyer payment is delayed, is the liquidity benefit of early receivable monetization worth its extra cost?”

────────

12. Threshold Metrics

12.1 Zero-profit USD/KRW Threshold

Solve numerically where:

```text
Financing-adjusted Deal Profit = 0
```

Reference approximate result:

```text
USD/KRW ≈ 1,143
```

12.2 14% Target-margin USD/KRW Threshold

Solve numerically where:

```text
Financing-adjusted Deal Margin = 14%
```

Reference approximate result:

```text
USD/KRW ≈ 1,386
```

Use bounded bisection / numerical solving over the full deterministic engine.

Do not hard-code a simplified analytic result.

UI wording:

> “With the current deal and financing structure, maintaining a 14% financing-adjusted Deal Margin requires approximately USD/KRW 1,386 or above.”

Never present this as an FX forecast.

────────

13. Insurance and Guarantee Model — Deferred Scope

These concepts belong to the product model, but are not authorized in the current gate.

13.1 Export Credit Insurance

Economic role:

```text
Buyer non-payment risk
        ↓
risk transfer
        ↓
premium / insured coverage
```

Later simulation parameters may include:

```text
coverage_ratio
premium
insured_loss_assumption
```

Rules:

• no invented buyer default probability,
• no claim that insurance eligibility has been approved,
• no fabricated official premium.

13.2 Export Credit Guarantee

Economic role:

```text
Export receivable / trade activity
        +
K-SURE-style credit enhancement
        ↓
financial institution
        ↓
financing availability
```

The guarantee is not the same as insurance.

Potential later effects:

• borrowing availability,
• borrowing limit,
• financing cost assumption.

Do not simulate until the input assumptions can be sourced or user-entered.

13.3 FX Insurance / Hedge

Economic role:

```text
FX downside
        ↓
reduced FX variability
        +
coverage cost
```

Later parameters:

```text
covered_amount
hedged_fx_rate
coverage_cost
```

Rules:

• no FX forecast,
• no automatic hedge recommendation,
• before/after simulation only.

────────

14. Financial Options

Canonical future enum:

```text
FinancialOption
├── HOLD_RECEIVABLE
├── WORKING_CAPITAL_FINANCING
├── EARLY_RECEIVABLE_PURCHASE
├── EXPORT_CREDIT_INSURANCE        # deferred
├── EXPORT_CREDIT_GUARANTEE        # deferred
└── FX_COVER                       # deferred
```

Do not create:

```text
LoanAgent
BillAgent
InsuranceAgent
GuaranteeAgent
HedgeAgent
```

Each option should modify deterministic cashflow/risk assumptions, not create a new agent architecture.

────────

15. External Data

P0

Korea Eximbank FX

Implemented use:

• `deal_bas_r` as the official neutral USD/KRW reference FX
• `deal_bas_r` as the official neutral JPY/KRW-per-100 reference FX

The Financial Engine retains one rate per currency. TTB/TTS are not implemented
application behavior, and reference FX is not an achieved customer settlement rate.

K-SURE Export Payment Information

Use for country/industry context such as:

• payment terms,
• average payment period,
• late-payment rate,
• average late-payment period,
• payment-period distribution.

Do not manufacture an AI risk score.
K-SURE aggregate context is not individual buyer risk prediction.

K-SURE Country Risk

Use as official country-level context.

Do not claim it is individual buyer default probability.

Bank of Korea ECOS

Validated / deferred series:

• `121Y006` / `BECBLA02` — 예금은행 대출금리(신규취급액 기준), 기업대출, monthly, annualized percent → `FUNDING_BENCHMARK`
• `722Y001` / `0101000` — 한국은행 기준금리, monthly → `MACRO_CONTEXT`

Neither series overwrites `DealCase.annual_funding_rate`. The company/user-entered
actual borrowing rate remains authoritative. No BOK ECOS adapter is implemented.

P1 Deferred

• bank-specific receivable purchase rates
• actual trade-finance fee schedules
• product-specific insurance premium calculations
• Customs export/import trend
• corporate financials
• logistics tracking
• buyer-specific credit
• cargo insurance
• sanctions screening
• maps
• news

────────

16. AI Responsibility

AI has only two jobs.

16.1 Document Extraction

Input:

• PO
• Sales Contract
• Commercial Invoice

Output:

• proposed DealCase

The user reviews extracted values before calculation.

16.2 Explanation

Explain:

• Base vs Stress
• which FX exposure mattered
• why external borrowing increased
• why payment delay increased funding cost
• liquidity/cost tradeoff of receivable purchase

AI must distinguish:

```text
Observed official data
User-entered fact
Demo assumption
Stress assumption
Calculated result
```

AI must not alter deterministic numbers.

────────

17. MVP Screen

Base Result

```text
Financing-adjusted Deal Margin
14.64%

Peak Deal Funding
119.0M KRW

Max External Borrowing
69.0M KRW
```

Exposure:

```text
USD   +80,000
JPY   -3,000,000
```

Stress

|Scenario  |Margin   |Max Loan |Funding Cost|Collection|
|----------|--------:|--------:|-----------:|---------:|
|Base      |14.64%   |69.0M    |0.509M      |D+90      |
|USD -5%   |11.20%   |67.6M    |0.498M      |D+90      |
|JPY +10%  |12.69%   |71.7M    |0.530M      |D+90      |
|Rate +1%p |14.56%   |69.0M    |0.615M      |D+90      |
|Delay +30d|14.44%   |69.0M    |0.781M      |D+120     |
|Combined  |**8.83%**|**70.3M**|**0.962M**  |**D+120** |

Finance Decision

```text
Wait until D+90
        vs
Early receivable purchase at D+65
```

Show:

• cash-availability date,
• max external borrowing,
• borrowing-interest cost,
• receivable-purchase cost,
• financing-adjusted margin.

No universal “best” badge in v0.1.

────────

18. Non-goals

Unless this spec is explicitly revised, do not implement:

• L/C workflow
• D/A workflow
• D/P workflow
• actual bill-of-exchange document generation
• real bank receivable purchase
• real bank loan
• real insurance signup
• real guarantee application
• factoring platform
• forfaiting workflow
• company-wide treasury
• ERP integration
• user authentication
• portfolio database
• multiple companies
• multi-agent
• LangGraph
• vector DB
• RAG framework
• custom financial LLM
• FX prediction
• rate prediction
• buyer-default ML
• generic API Provider Factory
• microservices
• Kubernetes
• map
• news sentiment

────────

19. Validation

Required Deterministic Tests

1. Base deal economics
2. Base external-financing schedule
3. USD -5%
4. JPY +10%
5. funding rate +1%p
6. payment delay +30d
7. combined stress
8. zero-profit USD threshold
9. 14% target-margin USD threshold
10. receivable held to maturity
11. early receivable purchase
12. early purchase repays external borrowing at purchase date
13. buyer delay changes receivable discount tenor

Invariants

• lower USD/KRW cannot improve a positive USD-net-exposure deal
• higher JPY/KRW cannot improve a negative JPY-exposure deal
• higher borrowing rate cannot reduce borrowing cost
• later buyer collection cannot reduce hold-to-maturity borrowing cost
• larger available cash cannot increase maximum external borrowing
• early purchase cannot leave the same borrowing outstanding after purchase proceeds have repaid it
• higher discount rate cannot reduce receivable-purchase cost
• AI output cannot mutate financial-engine values

────────

20. Frozen Gate — Financial Engine v0.1

The completed Financial Engine v0.1 gate satisfies:

• DealCase is cleanly represented
• internal cash and external borrowing are separate concepts
• base borrowing schedule matches the reference case
• all five stress scenarios match expected values
• threshold solver is deterministic
• receivable held-to-maturity path works
• early-purchase path correctly changes cash timing and borrowing
• all deterministic tests pass
• no unnecessary financial-agent or provider abstraction exists

────────

21. Next Implementation Gate — End-to-End Web MVP

The web MVP may consume the frozen Financial Engine, K-SURE payment-context
adapter and Korea Eximbank reference-FX adapter through explicit boundaries.

The next gate does not authorize insurance, guarantees, hedge execution,
databases, authentication, multi-agent systems, RAG, microservices or
speculative provider abstractions.

Generative AI remains a later sub-gate of the MVP. When authorized, its scope is
limited to:

1. document extraction into proposed DealCase values;
2. explanation of deterministic outputs.

AI must never become the authoritative financial calculator.

────────

22. Implemented Component Boundaries

```text
Web MVP caller
    ├──→ Financial Engine v0.1
    ├──→ K-SURE payment context
    └──→ Korea Eximbank reference FX
```

External APIs never run inside Financial Engine calculations. A caller converts
the Eximbank reference snapshot into the engine's existing one-rate-per-currency
input explicitly.

────────

23. Deferred Product Gates

Insurance, guarantee and FX-cover simulation remain deferred. They are not part
of the End-to-End Web MVP gate and require a later explicit specification change.
