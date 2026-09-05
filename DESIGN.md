# Design System

## Design intent

Create a calm, trustworthy Treasury pre-check for Korean finance practitioners. The experience combines Toss-like clarity with a restrained corporate-finance tone; AI remains a secondary capability, while decisions and deterministic numbers lead.

## Design principles

- Follow facts → assumptions → immediate deterministic change → option trade-off → short review → report.
- Distinguish transaction-only funding from company-wide liquidity without recommendation language.
- Show relationships visually instead of placing unrelated KPI cards side by side.
- Use white space, typography, semantic status text, and one clear next action before decorative effects.
- Keep React presentation-only; Python supplies every authoritative financial value.
- Translate internal engineering terms into practitioner-facing Korean wherever the technical term is not itself useful.

## Foundations

### Color roles and semantic tokens

The React shell uses `--surface`, `--surface-subtle`, `--surface-raised`, `--text-primary`, `--text-secondary`, `--border`, `--primary`, `--success`, `--warning`, and `--danger`, plus restrained soft semantic surfaces. Streamlit theme variables are preferred fallbacks. Status color is always paired with text.

### Typography

Use the Streamlit/system sans-serif stack. Hero text is 28–36px/1.2, section labels 14–16px/1.4, primary values 24–30px/1.15, and supporting copy at least 16px on compact screens. A large number must always sit next to a label, context line, or visual relationship; do not leave standalone figures without meaning.

### Spacing, layout, and surfaces

Use an 8px base rhythm, a centered 1180px maximum content width, and responsive gutters. Cards use `--radius-md`, a quiet border, and `--shadow-card`; no ornamental gradients, glow, or decorative data chrome.

### Icons

Use Lucide outline icons at 18–20px. Icons supplement visible Korean labels and never carry meaning alone.

## Components

- Stage navigation uses real buttons with visible `:focus-visible` rings.
- Do not keep a persistent four-card KPI wall under every stage. Each stage surfaces only the numbers needed for the current decision.
- The Company Liquidity step uses a connected three-step relationship: transaction funding → company-wide peak gap → residual gap after the current line.
- Warning and success states include explicit text such as `부족`, `한도 내`, or `목표 충족`.
- Data-dense tables remain native Streamlit in the guided stage content.
- Supporting explanations use quiet helper surfaces instead of blog-like prose.

## Product language

Prefer user-facing terms such as:

- `현재 마진` instead of `현재 Deal 마진`
- `이번 거래에 필요한 외부자금` instead of `거래만 본 은행 필요액`
- `회사 전체 최대 자금부족` instead of `Company-wide Peak 부족`
- `현재 한도 반영 후 부족` instead of `기존 한도 적용 후 부족`
- `회사 자금` instead of a generic internal `liquidity` label where the user needs an action-oriented phrase
- `자금·환위험` instead of exposing `Treasury` as a menu label
- `거래 검토` instead of making AI the menu identity

Keep actual practitioner terms such as O/A, Forward, Banker's Usance, and Treasury only where their domain meaning is useful.

## Help and guidance

The experience uses progressive disclosure rather than forcing a manual into the main screen.

- A collapsed `용어·사용법` control sits directly below the active experience.
- The first level explains the five-step workflow and the next action in each stage.
- Financial terms are individual clickable disclosure items with one plain-language definition and one caution/boundary sentence.
- The help content is one canonical Python presentation SSOT in `components/trade_treasury_experience/__init__.py`; do not create separate tooltip, popover, and manual copies that can drift.
- Core information needed to make the next decision stays visible. Definitions and caveats may be progressively disclosed.
- If conditions change, tell the user exactly what to do next: return to `결과·보고서` and run the current conditions again.

## Interaction

### Motion

Use Motion only for 160–220ms stage selection, short result entry, restrained hover lift, and value crossfade. Respect `prefers-reduced-motion` through `MotionConfig reducedMotion="user"`; reduced motion removes translation and scale. Do not use fake thinking, infinite pulse, typewriter output, or decorative progress.

### Responsive behavior

At desktop widths, stages form one horizontal row. The Company Liquidity relationship is a connected three-step horizontal flow. At 720px and below, stages remain horizontally scrollable while the relationship changes to a vertical connected flow. Touch targets are at least 44px high.

### Accessibility

Maintain keyboard navigation, visible focus, semantic buttons/headings/disclosures, readable contrast, text-based status, and reflow without clipping at 390px. Help uses native `details/summary`, so definitions are reachable without hover.

## Do / Don't

- Do show `이번 거래`, `회사 전체`, and `한도 반영 후` as one visible relationship.
- Do explain what a number means and what the user can do next.
- Do pass dynamic content through component data and render it as text.
- Don't calculate, round, or infer finance values in JavaScript.
- Don't use chatbot, cyberpunk, glow, particle, or recommendation styling.
- Don't use internal implementation vocabulary merely because it exists in code.

## Implementation notes

The canonical React tokens live in `components/trade_treasury_experience/frontend/src/styles.css`. New visual values must extend those semantic roles instead of adding scattered literals. The internal precompiled Streamlit Components v2 React bundle owns orientation and user intent; Streamlit/Python remains the behavior and finance authority.

The wrapper performs a bounded Korean copy-normalization pass over the committed bundle so the deployed static bundle and the presentation SSOT use the same user-facing terminology without touching finance or Agent behavior. This map is copy-only and must never change logic, state, or calculations.

## Guided decision loop

The five stages are 거래 입력 → 판단 기준 → 회사 자금 → 대응 시뮬레이션 → 결과·보고서. Internal stage IDs remain compatible; `review` now means judgment assumptions. The prominent review-goal selector is removed and Agent review defaults to overall. Facts use exact inputs; assumptions use synchronized sliders and exact inputs sharing one authoritative key. Stage-local controls persist across navigation. Company cash uses the existing timeline as a native step chart. Alternatives show current → option → delta, including unchanged bank principal. Deterministic results lead; the single optional Agent action and report live together in the final stage. Tool completion is shown only after actual success.

## Final product freeze

- Native evidence remains stage-exclusive: each stage shows only its detailed inputs, evidence, or result actions while the experience shell remains visible.
- The shell uses neutral unavailable values and Python-supplied `complete`, `ready`, or `blocked` states when an input is invalid; it never disappears or infers readiness.
- The result stage is the single report/download entry. The deterministic PDF uses the final Treasury brand and includes only current application evidence; stale AI prose is excluded.
