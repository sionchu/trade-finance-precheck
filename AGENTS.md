# AGENTS.md

## Authority

- `docs/product-spec.md` is the authoritative product and implementation specification.
- Start from the canonical Clean-v0 state. Do not reconstruct brainstorming history, discarded concepts, or superseded drafts.
- If another document conflicts with `docs/product-spec.md`, follow `docs/product-spec.md`.

## Current gate

- The deterministic Financial Engine v0.1, Deal Rescue / Negotiation Solver, End-to-End Web MVP, accepted presentation layer, AI Financialization, K-SURE public payment-context integration, Deal Pre-check Report, and public Streamlit deployment are implemented and frozen.
- The Korea Eximbank reference-FX adapter is locally validated and deployment-deferred. Its public Streamlit runtime path is disabled because it is unreliable in that target environment.
- Bank of Korea ECOS is validated and deferred; no ECOS adapter is implemented.
- Do not modify frozen behavior unless a new, evidenced P0 correctness issue is established.
- New application layers must consume frozen components through explicit boundaries. External API access must never move inside Financial Engine calculations.
- The current authorized gate is Single Deal Review Agent: one bounded read-only agent that consumes current Deal state and already-computed finance, stress, rescue, and loaded K-SURE context to produce a grounded Deal Review memo. It must not perform authoritative financial calculations, mutate the Deal, or execute finance.
- AI plain-Korean explanation is deferred. AI must never become the authoritative financial calculator.
- Do not advance to insurance, guarantees, hedge execution, databases, authentication, multi-agent systems, RAG, arbitrary web search, EUR/CNY support, microservices, or speculative provider abstractions.

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
