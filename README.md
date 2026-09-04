# AI Trade Finance Pre-check

A pre-deal decision-support MVP for evaluating whether one export deal's margin and liquidity remain resilient under FX, delayed collection, and funding stress.

The canonical product definition is [docs/product-spec.md](docs/product-spec.md).

## Current state

The repository contains the frozen deterministic Financial Engine v0.1 and
Deal Rescue / Negotiation Solver, Streamlit Web MVP and presentation layer,
optional AI financialization of the bundled synthetic trade-document demo,
the bounded read-only Single Deal Review Agent, public K-SURE aggregate payment
context, and the Deal Pre-check Report. The public Streamlit deployment is
operational. Financial calculations remain authoritative in the Financial
Engine and Deal Rescue Solver; AI only extracts supported facts or explains
already-computed evidence.

The Korea Eximbank reference-FX adapter passed local live validation but is
deployment-deferred; its public Streamlit runtime path is disabled because it
is unreliable in that target environment. The Bank of Korea ECOS funding
benchmark and macro context are also validated and deferred.

The current product gate is Submission Artifacts / Final Freeze.

## Scope

Arbitrary document upload, arbitrary web search, RAG, multi-agent systems,
insurance, guarantees, hedge execution, databases, authentication, and EUR/CNY
support are not part of the current scope.

## Local run

Install the pinned dependency and start the app:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Optional public K-SURE retrieval uses `KSURE_SERVICE_KEY`. AI document
financialization and the one-shot Deal Review Agent use `OPENAI_API_KEY`. The
deterministic analysis runs without either variable.

## Tests

```powershell
python -m unittest discover -s tests -v
```
