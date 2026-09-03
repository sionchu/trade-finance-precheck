# AI Trade Finance Pre-check

A pre-deal decision-support MVP for evaluating whether one export deal's margin and liquidity remain resilient under FX, delayed collection, and funding stress.

The canonical product definition is [docs/product-spec.md](docs/product-spec.md).

## Current state

The repository contains the frozen deterministic Financial Engine v0.1 and
the K-SURE aggregate payment-context integration.

## Scope

The implemented scope is limited to those two components.

## Tests

```powershell
python -m unittest discover -s tests -v
```
