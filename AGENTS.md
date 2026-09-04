# AGENTS.md

## Authority

- `docs/product-spec.md` is the authoritative product and implementation specification.
- Start from the canonical Clean-v0 state. Do not reconstruct brainstorming history, discarded concepts, or superseded drafts.
- If another document conflicts with `docs/product-spec.md`, follow `docs/product-spec.md`.

## Current gate

- The deterministic Financial Engine v0.1, Deal Rescue / Negotiation Solver, Company Liquidity & Funding Choice, FX Treasury / Forward Hedge Simulation, Banker's Usance simulation, End-to-End Web MVP, accepted presentation layer, Trade Document Financialization, Financial Statement Financialization / Company Liquidity Profile, Treasury-integrated bounded Single Deal Review Agent, K-SURE public payment-context integration, Deal Pre-check Report, and public Streamlit deployment are implemented and frozen.
- The Korea Eximbank reference-FX adapter is locally validated and deployment-deferred. Its public Streamlit runtime path is disabled because it is unreliable in that target environment.
- Bank of Korea ECOS is validated and deferred; no ECOS adapter is implemented.
- Do not modify frozen behavior unless a new, evidenced P0 correctness issue is established.
- New application layers must consume frozen components through explicit boundaries. External API access must never move inside Financial Engine calculations.
- The product is a Company-aware Trade Treasury Pre-check with three connected decision layers: frozen Deal Economics, authorized Company Liquidity, and authorized FX Treasury.
- AI has exactly three product roles: Trade Document Financialization, Financial Statement Financialization, and the Single Deal Review Agent.
- The current authorized gate is T6 — Presentation IA RE0 / Report / Submission Final Freeze.
- The canonical gate sequence is T1 Company Liquidity Profile, T2 Company Liquidity & Funding Choice, T3 FX Treasury / Forward Hedge Simulation, T4 Banker's Usance, T5 Treasury integration into the Single Deal Review Agent, and T6 Presentation IA RE0 / Report / Submission Final Freeze.
- Financial Statement AI extracts only explicitly supported liquidity facts and is frozen. It must not infer credit approval, bank lending capacity, company available cash, a credit score, default, or future cash flow. Deal-specific available company cash always requires explicit user confirmation.
- Working-capital total limit and used amount are user-entered facts; unused limit is derived. `DealCase.annual_funding_rate` remains the borrowing-rate SSOT, and financial-statement cash never sets Deal-specific available cash.
- FX Treasury classifies exposure per currency, treats same-currency receivables and payables as an amount-level offset rather than proof of a timing-matched hedge, and uses only user-supplied forward quotes and settlement spots. It forecasts and executes nothing. Its hedge profit/loss overlay does not recompute derivative-settlement funding schedules.
- Payment method and financing structure are separate concepts. Core Deal payment methods remain OA / TT; do not create a generic `PAYMENT_USANCE` enum. The frozen Banker's Usance simulation is a narrow funding overlay for one selected foreign payable; it predicts no approval, executes nothing, and is not an FX hedge or full L/C / UPAS workflow.
- The Single Deal Review Agent is a one-shot, bounded read-only explanation layer with exactly four local evidence tools. Its structured memo selects exactly one available `treasury_focus`; `supporting_signals` contains only always-available Deal-analysis evidence. Optional Company Liquidity and K-SURE context are rendered deterministically when loaded and are not model-selectable fields. Its Treasury tool only serializes already-computed T1–T4 evidence. A successful run uses exactly two API requests with no retry, never fetches external data, and includes Treasury, Company Liquidity, and K-SURE context in current-state freshness. Authoritative numbers remain deterministic UI output; the Agent must not calculate them, mutate the Deal, execute finance, or retain conversation history.
- Do not advance outside the canonical gate sequence or add full L/C / UPAS / D/A / D/P workflows, FX forecasting, stochastic risk models, insurance or guarantee execution, actual hedge or loan execution, bank approval or buyer-default prediction, databases, authentication, multi-agent systems, RAG, arbitrary web search, EUR/CNY support, microservices, or speculative provider abstractions.

## Anti-bloat rules

- Add only files and abstractions required by the current authorized gate.
- Do not create duplicate spec variants or filenames containing `v0`, `v2`, `final`, `new`, or `refactored`.
- Do not add dependencies, CI, issue templates, databases, authentication, RAG, multi-agent systems, provider/factory abstractions, microservices, or deployment configuration unless an explicit authorized gate requires them.
- Do not create speculative packages for deferred financial options.
- Preserve a single deterministic model; financial options modify cashflow or risk assumptions rather than introducing agent architectures.

## Evidence-first work

- Never report expected, inferred, or simulated results as executed results.
- Keep completed, not executed, blocked, and proposed work distinct.
- Do not fabricate command output, tests, logs, screenshots, sources, files, or links.
- Verify financial outputs against the canonical reference case and required invariants.
- Run the complete applicable test suite and report the exact commands and results.
- If an assumption is missing, report the ambiguity; do not silently invent it.
- AI extraction or explanation must never mutate deterministic financial-engine values.

## Change discipline

- Preserve unrelated user changes.
- Keep secrets and environment files out of Git.
- Do not broaden scope without an explicit product-spec revision.
- Preserve frozen component boundaries in later application work.
