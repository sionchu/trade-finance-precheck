# AI Trade Finance Pre-check

A pre-deal decision-support MVP for evaluating whether one export deal's margin and liquidity remain resilient under FX, delayed collection, and funding stress.

The canonical product definition is [docs/product-spec.md](docs/product-spec.md).

## Current state

The deterministic Financial Engine v0.1 implements the canonical one-deal
economics, dated cashflows, external financing, stress scenarios, USD/KRW
thresholds, and receivable purchase simulation.

## Scope

The implemented scope is limited to the deterministic Financial Engine v0.1
defined in the product specification.

## Tests

```powershell
python -m unittest discover -s tests -v
```
