# AI Trade Finance Pre-check

A pre-deal decision-support MVP for evaluating whether one export deal's margin and liquidity remain resilient under FX, delayed collection, and funding stress.

The canonical product definition is [docs/product-spec.md](docs/product-spec.md).

## Current state

The repository contains the frozen deterministic Financial Engine v0.1,
Streamlit Web MVP and presentation layer, optional AI financialization of the
bundled synthetic trade-document demo, public K-SURE aggregate payment context,
and the Deal Pre-check Report. The public Streamlit deployment is operational.

The Korea Eximbank reference-FX adapter passed local live validation but is
deployment-deferred; its public Streamlit runtime path is disabled because it
is unreliable in that target environment. The Bank of Korea ECOS funding
benchmark and macro context are also validated and deferred.

The current product gate is Deal Rescue / Negotiation Solver.

## Scope

AI explanation, arbitrary document upload, insurance, guarantees, hedge
execution, databases, and authentication are not part of the current scope.

## Local run

Install the pinned dependency and start the app:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Optional public K-SURE retrieval uses `KSURE_SERVICE_KEY`. Optional AI document
financialization uses `OPENAI_API_KEY`. The deterministic analysis runs without
either variable.

## Tests

```powershell
python -m unittest discover -s tests -v
```
