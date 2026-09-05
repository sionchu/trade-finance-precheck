# AGENTS.md

## Authority

- `docs/product-spec.md` is the authoritative current product and implementation specification.
- `DESIGN.md` is authoritative for current UI/UX rules and semantic visual tokens.
- `docs/submission.md` is the canonical submission-facing factual source.
- `README.md` is for repository overview and developer run/test instructions.
- If these documents conflict, follow `docs/product-spec.md` for product behavior and scope.
- Do not reconstruct superseded brainstorming, T1–T6 patch history, five-stage navigation, or discarded product names.

## Current product

Public product name:

`수출거래 AI 금융진단`

Public views are exactly:

```text
입력 | 분석 | 보고서
```

Default view is `분석`.

The product is a final competition submission candidate. Treat implemented finance, AI boundaries, public data behavior, report generation and accepted presentation as frozen unless a new evidenced P0 correctness, security or deployment issue is established.

## Frozen authority boundaries

### Finance

Python deterministic finance is authoritative for all financial numbers.

Frozen areas include:

- Deal economics and dated cashflow
- external borrowing and funding cost
- canonical Stress scenarios
- Deal Rescue / deterministic thresholds
- Company Liquidity Timeline
- working-capital capacity and funding-choice comparison
- O/A receivable early-purchase simulation
- currency-level FX exposure and natural offset
- forward-hedge simulation from user-supplied assumptions
- Banker's Usance financing overlay

React and AI must not calculate, round, infer or replace authoritative finance values.

### Company liquidity

- company-wide current usable cash is a user-confirmed company fact
- minimum operating cash is a user-entered policy threshold
- Deal-allocated cash remains distinct from company-wide current cash
- working-capital total line and used amount are user-entered; unused line is derived
- prospective Deal cashflow comes from the deterministic engine and must not be duplicated in company cash-plan rows
- company liquidity gap is not bank approval, default prediction or a lending-capacity estimate

### AI

AI has exactly three product roles:

1. Trade Document Financialization
2. Financial Statement Financialization
3. Single Deal Review Agent

Trade Document AI extracts only document-supported facts and never calculates margin, FX exposure or funding need.

Financial Statement AI extracts only explicit statement facts. It must not infer ratios, company available cash, Deal-available cash, lending capacity, credit approval, credit score, default risk or future cash flow.

Single Deal Review Agent:

- exactly four local read-only evidence tools
- successful run = exactly two model requests
- no retry
- no external fetch
- no authoritative calculation
- no Deal mutation
- no finance execution
- no conversation-history retention
- no FX/rate/default/bank-approval prediction
- no product recommendation or ranking
- headline and summary contain no numeric characters

Authoritative numbers remain deterministic UI output.

### External data

External providers stay outside finance calculations.

Current public state:

- K-SURE aggregate payment context: implemented, explicit user action only
- Korea Eximbank reference FX adapter: locally validated, public runtime disabled/deferred
- Bank of Korea ECOS: researched/validated concept, no public adapter
- OpenDART: not implemented

Do not make application startup or core calculations depend on an external provider.

### Report

The PDF is generated from current deterministic evidence. Stale Agent prose must be excluded. Do not add model/API calls inside report generation.

## Public security boundary

The public MVP is a competition demonstration, not an enterprise document vault.

- bundled demo documents and ERP data are fictional
- no persistent application database or authentication layer exists
- when a user explicitly runs Trade Document AI or Financial Statement AI, the selected PDF content is sent to the configured OpenAI API for structured extraction
- those OpenAI requests use `store=False`
- public-demo users should not be encouraged to upload real trade secrets, personal information or confidential corporate documents

Do not claim zero leakage risk, guaranteed deletion, enterprise-grade tenant isolation or other unimplemented security controls.

Future enterprise security controls belong in commercialization documentation only unless explicitly authorized for implementation.

## Deferred scope

Do not implement without an explicit new product-spec gate:

- database / authentication
- RAG / arbitrary web search
- multi-agent architecture
- microservices
- speculative provider abstractions
- full L/C / UPAS / D/A / D/P workflows
- insurance / guarantee execution
- real hedge / loan / payment execution
- bank approval or buyer-default prediction
- FX / rate forecasting
- stochastic CFaR / Monte Carlo risk models
- EUR / CNY engine expansion
- live ERP / accounting / TMS / bank connectivity
- OpenDART integration
- public ECOS integration
- public Korea Eximbank reference-FX activation

## Anti-bloat rules

- Start from current canonical behavior, not historical patches.
- Prefer modifying an existing canonical artifact over creating `new`, `v2`, `final`, `refactored` variants.
- Do not add duplicate configuration, duplicate product copy or parallel UI paths.
- Do not add dependencies unless the authorized change genuinely requires them.
- Avoid wrappers, managers, factories and interfaces that do not reduce real complexity.
- Remove obsolete compatibility code when a replacement is proven and accepted.
- Do not add CI, issue templates or deployment infrastructure unless explicitly authorized.

## Evidence-first work

- Read actual code, tests and current docs before proposing architecture changes.
- Check imports, call sites, runtime behavior and tests before classifying code as dead.
- Never report expected, inferred or simulated results as executed results.
- Distinguish implemented, validated, deferred, blocked and proposed states.
- Never fabricate commands, logs, screenshots, sources, files or links.
- If a required assumption is missing, state the ambiguity rather than inventing it.

## Verification

Canonical Python verification:

```powershell
python -m unittest discover -s tests -v
python -m compileall -q src tests app.py components
git diff --check
```

If frontend source changes:

```powershell
cd components\trade_treasury_experience\frontend
npm ci
npm run typecheck
npm run build
```

Then rerun relevant Python tests because committed frontend build assets are runtime inputs.

Public acceptance values are defined in `docs/product-spec.md`.

Do not claim PASS for a command, browser viewport, Agent run, API call or PDF inspection unless it was actually executed.

## Change discipline

When explicitly asked to modify the project:

1. preserve unrelated user changes;
2. choose the smallest coherent scope;
3. keep frozen finance/AI contracts unless the issue directly requires a change;
4. modify canonical artifacts rather than adding parallel versions;
5. remove an old path when it is truly replaced;
6. run applicable verification;
7. reread the final diff;
8. remove newly introduced bloat before finalizing.

Before submission, no feature work is authorized unless a new evidenced P0 issue is found. Documentation corrections, submission synchronization and factual security disclosures are allowed when they align existing behavior.
