# AI Trade Finance Pre-check

A Company-aware Trade Treasury Pre-check for evaluating one export Deal's economics, the company's Deal-specific liquidity capacity, and currency-level FX exposure before execution.

The canonical product definition is [docs/product-spec.md](docs/product-spec.md).

## Current state

The repository contains the frozen Deal Economics foundation: deterministic
Financial Engine v0.1, Deal Rescue / Negotiation Solver, Streamlit Web MVP and
presentation layer, Trade Document Financialization, Financial Statement
Financialization with a normalized Company Liquidity Profile, the bounded
read-only Single Deal Review Agent, public K-SURE aggregate payment context, and
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

The current authorized gate is **T2 — Company Liquidity & Funding Choice**.

The Treasury gate sequence is T1 Company Liquidity Profile, T2 Company
Liquidity & Funding Choice, T3 FX Treasury / Forward Hedge Simulation, T4
Banker's Usance, T5 Treasury integration into the Single Deal Review Agent, and
T6 Presentation IA RE0 / Report / Submission Final Freeze.

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

## Tests

```powershell
python -m unittest discover -s tests -v
```
