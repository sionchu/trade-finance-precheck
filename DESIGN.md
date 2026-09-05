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

Use the Streamlit/system sans-serif stack. The product title is compact at 29–38px, decision headlines are 23–30px, section titles are 21–25px, primary values are 26–32px, and supporting copy is 13–15px with comfortable line height. Setup facts use compact label/value rows instead of dashboard-sized figures. A large number must always sit next to a label, context line, or visual relationship; do not leave standalone figures without meaning.

### Spacing, layout, and surfaces

Use an 8px base rhythm, a centered 1180px maximum content width, and responsive gutters. Cards use `--radius-md`, a quiet border, and `--shadow-card`; no ornamental gradients, glow, or decorative data chrome.

### Icons

Use Lucide outline icons at 18–20px. Major sections may use one 40px soft-blue icon tile; individual rows do not repeat icons. Icons supplement visible Korean labels and never carry meaning alone.

## Components

- Stage navigation uses real buttons with visible `:focus-visible` rings.
- Do not keep a persistent four-card KPI wall under every stage. Each stage surfaces only the numbers needed for the current decision.
- The Company Liquidity step uses a connected three-step relationship: transaction funding → company-wide peak gap → residual gap after the current line.
- Warning and success states include explicit text such as `부족`, `한도 내`, or `목표 충족`.
- Data-dense tables remain native Streamlit in the guided stage content.
- Supporting explanations use quiet helper surfaces instead of blog-like prose.
- Setup summaries use one restrained surface per subject and disclosure buttons for editing. Toggle controls are reserved for genuine on/off state.
- Scenario presets read as wrapping chips. Base uses one compact baseline surface; non-Base comparisons use `current → option` plus a text delta.
- Report metadata is a wrapping label/value list, not KPI metrics.

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
- If conditions change, distinguish edited inputs from the last calculated result and tell the user which calculation to run again.

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

The canonical React tokens live in `components/trade_treasury_experience/frontend/src/styles.css`. New visual values must extend those semantic roles instead of adding scattered literals. The internal precompiled Streamlit Components v2 React bundle owns three-view navigation; Streamlit/Python owns inputs, actions, evidence, and finance authority.

User-facing shell copy is authored in `ExperienceShell.tsx` and deployed from the committed build without runtime string replacement. Source changes must be followed by a frontend build so source and runtime wording stay identical.

## Guided decision loop

The three views are 입력 | 분석 | 보고서, with 분석 as the default. Setup opens with formatted Deal/company facts; edit forms and the cash-plan editor are opt-in. Analysis leads with a bounded deterministic conclusion, the connected Deal/company/residual funding relationship, and the existing cash timeline. Presets select one frozen scenario against Base; only custom comparison reveals four exact fields. Response assumptions stay behind 조건 수정, with no sliders. Report shows a compact base summary, optional Agent review and PDF. There is no five-stage compatibility mapping or duplicate navigation state.

## Final product freeze

- Native content is view-exclusive: setup facts/forms, analysis outcomes/comparisons, report summary/optional Agent/PDF.
- The shell stays visible on invalid input; Python displays correction feedback and blocks Agent execution when required evidence is unavailable.
- The report view is the single report/download entry. The deterministic PDF uses 수출거래 AI 금융진단 branding and includes only current application evidence; stale AI prose is excluded.
