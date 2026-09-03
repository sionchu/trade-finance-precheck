# AI Trade Finance Pre-check

A pre-deal decision-support MVP for evaluating whether one export deal's margin and liquidity remain resilient under FX, delayed collection, and funding stress.

The canonical product definition is [docs/product-spec.md](docs/product-spec.md).

## Current state

The repository contains the frozen deterministic Financial Engine v0.1,
the K-SURE aggregate payment-context integration, and the Korea Eximbank
official reference-FX integration, exposed through a deterministic Streamlit
Web MVP. The MVP also includes optional AI financialization of the bundled
synthetic trade-document demo.

The current deterministic analysis can also be downloaded as a Deal Pre-check
Report. Report generation does not require AI or official-data credentials.

The Bank of Korea ECOS funding benchmark and macro context are validated but
deferred; no ECOS adapter is implemented.

## Scope

AI explanation, arbitrary document upload, insurance, guarantees, hedge
execution, databases, and authentication are not part of the current scope.

## Local run

Install the pinned dependency and start the app:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Optional official-data retrieval uses `EXIMBANK_AUTH_KEY` and
`KSURE_SERVICE_KEY`. Optional AI document financialization uses
`OPENAI_API_KEY`. The deterministic analysis runs without any of these
variables.

## Tests

```powershell
python -m unittest discover -s tests -v
```
