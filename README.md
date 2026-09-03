# AI Trade Finance Pre-check

A pre-deal decision-support MVP for evaluating whether one export deal's margin and liquidity remain resilient under FX, delayed collection, and funding stress.

The canonical product definition is [docs/product-spec.md](docs/product-spec.md).

## Current state

The repository contains the frozen deterministic Financial Engine v0.1,
the K-SURE aggregate payment-context integration, and the Korea Eximbank
official reference-FX integration.

The Bank of Korea ECOS funding benchmark and macro context are validated but
deferred; no ECOS adapter is implemented.

## Scope

The next implementation gate is the End-to-End Web MVP. Insurance, guarantees,
hedge execution, databases, authentication, and generative AI are not part of
the current implemented scope.

## Tests

```powershell
python -m unittest discover -s tests -v
```
