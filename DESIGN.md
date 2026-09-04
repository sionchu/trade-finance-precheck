# Design System

## Design intent

Create a calm, trustworthy Treasury pre-check for Korean finance practitioners. The experience combines Toss-like clarity with a restrained corporate-finance tone; AI remains a secondary capability, while decisions and deterministic numbers lead.

## Design principles

- Put the current decision and its financial evidence before detailed inputs.
- Distinguish Deal-only funding from company-wide liquidity without recommendation language.
- Use white space, typography, and semantic status text before decorative effects.
- Keep React presentation-only; Python supplies every authoritative financial value.

## Foundations

### Color roles and semantic tokens

The React shell uses `--surface`, `--surface-subtle`, `--text-primary`, `--text-secondary`, `--border`, `--primary`, `--success`, `--warning`, and `--danger`. Streamlit theme variables are preferred fallbacks. Status color is always paired with text.

### Typography

Use the Streamlit/system sans-serif stack. Hero text is 28–36px/1.2, section labels 14–16px/1.4, primary values 24–30px/1.15, and supporting copy at least 16px on compact screens.

### Spacing, layout, and surfaces

Use an 8px base rhythm, a centered 1180px maximum content width, and responsive gutters. Cards use `--radius-md`, a quiet border, and `--shadow-card`; no gradients or ornamental surfaces.

### Icons

Use Lucide outline icons at 18–20px. Icons supplement visible Korean labels and never carry meaning alone.

## Components

- Stage navigation uses real buttons with visible `:focus-visible` rings.
- Snapshot cards contain one label, one authoritative formatted value, and one concise status or context line.
- Warning and success states include explicit text such as `부족`, `한도 내`, or `목표 충족`.
- Data-dense tables remain native Streamlit in the guided stage content.

## Interaction

### Motion

Use Motion only for 160–220ms stage selection, short card entry, restrained hover lift, and value crossfade. Respect `prefers-reduced-motion` through `MotionConfig reducedMotion="user"`; reduced motion removes translation and scale.

### Responsive behavior

At desktop widths, stages form one horizontal row and snapshots use four columns. At 720px and below, snapshot cards stack and stage navigation scrolls within its own container without body overflow. Touch targets are at least 44px high.

### Accessibility

Maintain keyboard navigation, visible focus, semantic buttons and headings, readable contrast, text-based status, and reflow without clipping at 390px.

## Do / Don't

- Do show `거래만`, `회사 전체`, and `한도 적용 후` as distinct concepts.
- Do pass dynamic content through component data and render it as React text.
- Don't calculate, round, or infer finance values in JavaScript.
- Don't use chatbot, cyberpunk, glow, particle, or recommendation styling.

## Implementation notes

The canonical React tokens live in `components/trade_treasury_experience/frontend/src/styles.css`. New visual values must extend those semantic roles instead of adding scattered literals. The internal precompiled Streamlit Components v2 React bundle owns orientation and user intent; Streamlit/Python remains the behavior and finance authority.

## Guided decision loop

The five-stage experience follows condition → choice → review → result → response. `review_goal` records user intent and `response_action` records the next comparison the user chose; neither is an AI recommendation or financial input. Tool completion is shown only from a completed Agent run, never from timers or simulated progress.
