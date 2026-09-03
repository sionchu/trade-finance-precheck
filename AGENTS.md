# AGENTS.md

## Authority

- `docs/product-spec.md` is the authoritative product and implementation specification.
- Start from the canonical Clean-v0 state. Do not reconstruct brainstorming history, discarded concepts, or superseded drafts.
- If another document conflicts with `docs/product-spec.md`, follow `docs/product-spec.md`.

## Current gate

- This repository is pre-implementation.
- Do not implement the application until explicitly requested.
- When implementation is authorized, implement only the deterministic Financial Engine v0.1 gate defined in `docs/product-spec.md`.
- Do not advance to insurance, guarantees, external APIs, UI, or later product gates until the v0.1 financial-engine gate passes.

## Anti-bloat rules

- Add only files and abstractions required by the current authorized gate.
- Do not create duplicate spec variants or filenames containing `v0`, `v2`, `final`, `new`, or `refactored`.
- Do not add frontend/backend scaffolding, dependencies, CI, issue templates, databases, authentication, RAG, multi-agent systems, provider/factory abstractions, microservices, or deployment configuration unless a later explicit task and spec revision require them.
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
- Do not implement the Financial Engine in repository-setup tasks.

