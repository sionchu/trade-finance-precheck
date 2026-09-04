# 기업 수출거래 Treasury 사전점검

A Company-aware Trade Treasury Pre-check for evaluating one export Deal's economics, the company's Deal-specific liquidity capacity, and currency-level FX exposure before execution.

The canonical product definition is [docs/product-spec.md](docs/product-spec.md).

## Current state

The repository contains the frozen Deal Economics, Company Liquidity, and FX Treasury foundation: deterministic
Financial Engine v0.1, Deal Rescue / Negotiation Solver, Company Liquidity &
Funding Choice, Forward Hedge Simulation, Banker's Usance simulation, Streamlit Web MVP and
presentation layer, Trade Document Financialization, Financial Statement
Financialization with a normalized Company Liquidity Profile, the bounded
read-only Single Deal Review Agent with current T1–T4 Treasury evidence, public K-SURE aggregate payment context, and
the Deal Pre-check Report. The public Streamlit deployment is operational.
Financial calculations remain authoritative in the Financial Engine and Deal
Rescue Solver; AI only extracts supported facts or explains already-computed
evidence.

The Korea Eximbank reference-FX adapter passed local live validation but is
deployment-deferred; its public Streamlit runtime path is disabled because it
is unreliable in that target environment. The Bank of Korea ECOS funding
benchmark and macro context are also validated and deferred.

Financial Statement AI reads the bundled fictional KRW statement only after an
explicit click and exposes nine source-grounded liquidity facts. It does not
derive ratios, lending capacity, or the cash available to a Deal; that Deal
input remains user-confirmed.

Company funding capacity uses user-entered working-capital total and used
limits, derives the unused limit, and compares internal cash, waiting with the
existing credit line, and O/A receivable early purchase. The Deal's existing
annual funding rate remains the borrowing-rate source; financial-statement cash
never replaces Deal-specific available cash.

FX Treasury classifies USD and JPY exposure separately, distinguishes an
amount-level natural offset from timing alignment, and compares user-supplied
forward quotes at user-supplied settlement spots. It does not forecast or
execute FX. Its hedge profit/loss overlay does not recompute the Deal funding
schedule for derivative settlement cash flows.

Banker's Usance is implemented as a deterministic financing overlay on one
selected foreign payable. It compares ordinary working-capital line use with
the separate Usance principal obligation and explicit rate/fee assumptions.
It does not predict approval, execute financing, hedge FX automatically, or
implement a full L/C / UPAS workflow.

The Single Deal Review Agent reads current evidence through exactly four local
read-only tools: current Deal analysis, Stress / Rescue, already-computed
Treasury context, and already-loaded K-SURE context. It uses exactly two model
requests without retry, performs no authoritative calculation or external fetch,
and treats Treasury, Company Liquidity, and K-SURE context as part of result
freshness. Its structured memo selects one currently available Treasury review
focus while `supporting_signals` contains only always-available Deal-analysis
evidence. Optional Company Liquidity and K-SURE context are rendered
deterministically when loaded, not selected by the model. Numeric evidence
remains rendered from deterministic application state.

The current authorized gate is **T6 — Final Product Completion / Presentation IA
RE0 / Report / Submission Freeze**. T6-A, T6-B, and T6-C are implemented and frozen;
T6-D finalizes stage-exclusive presentation, the company-aware Treasury report,
and the single canonical [submission source](docs/submission.md).
The company-wide liquidity timeline combines Treasury-confirmed current cash,
existing confirmed cash-plan events, and the prospective Deal's frozen dated
cashflows. The React Experience Shell adds five-stage navigation and a compact
current-state summary while Python remains authoritative for every financial
value. The internal precompiled Streamlit Components v2 React bundle now guides
condition → choice → review → result → response while Python remains authoritative.
After T6-D acceptance the product is frozen; only evidenced P0 correctness or
deployment fixes are authorized before submission.

The Treasury gate sequence is T1 Company Liquidity Profile, T2 Company
Liquidity & Funding Choice, T3 FX Treasury / Forward Hedge Simulation, T4
Banker's Usance, T5 Treasury integration into the Single Deal Review Agent, and
T6 Final Product Completion / Presentation IA RE0 / Report / Submission Freeze.

T6-A accepts direct company cash-plan editing or a standard synthetic CSV export
path. ERP products such as SAP S/4HANA or 더존 may export the source file, but the
MVP does not claim a live ERP connection. Calendar dates resolve from a
user-selected trade review date; the frozen Deal Engine retains its D+n model.

## Scope

Full L/C and UPAS workflows, D/A / D/P engine expansion, FX forecasting,
stochastic risk models, arbitrary web search, RAG, multi-agent systems,
insurance or guarantee execution, actual hedge or loan execution, bank-credit
approval or buyer-default prediction, databases, authentication, and EUR/CNY
engine expansion remain deferred.

## Local run

Install the pinned dependency and start the app:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Optional public K-SURE retrieval uses `KSURE_SERVICE_KEY`. Both document
financialization roles and the one-shot Deal Review Agent use `OPENAI_API_KEY`.
The deterministic analysis runs without either variable.

The React component is prebuilt for deployment. To rebuild it locally:

```powershell
cd components\trade_treasury_experience\frontend
npm ci
npm run typecheck
npm run build
```

Streamlit Community Cloud serves the committed build assets and does not need
Node or npm at runtime.

## Tests

```powershell
python -m unittest discover -s tests -v
```
