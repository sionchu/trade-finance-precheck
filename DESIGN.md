# Design System

## Design intent

Create a calm, trustworthy B2B financial-diagnosis experience for Korean export practitioners. The interface borrows the clarity and progressive disclosure of modern fintech products while keeping a restrained corporate-finance tone.

AI is secondary. Deterministic financial evidence and the user's decision context lead.

---

## Product experience

Public views are exactly:

```text
입력 | 분석 | 보고서
```

`분석` is the default view.

The experience should feel like:

```text
setup when needed
      ↓
result-first financial diagnosis
      ↓
scenario / response comparison
      ↓
optional AI explanation
      ↓
report output
```

It should not feel like a multi-page calculator or an admin form.

---

## Design principles

- Show the decision before exposing raw inputs.
- Use progressive disclosure for edit forms and advanced assumptions.
- Distinguish transaction-only funding from company-wide liquidity.
- Show financial relationships visually instead of placing unrelated KPI cards side by side.
- Use `current → option → delta` for scenario and response comparisons.
- Use semantic status text together with color; never color alone.
- Keep one functional icon anchor per major section rather than decorating every row.
- Keep AI behind deterministic evidence.
- Keep React presentation-only; Python supplies all authoritative financial values and actions.
- Translate internal engineering vocabulary into practitioner-facing Korean unless the technical term itself is useful.

---

## Foundations

### Color roles

Use semantic tokens rather than scattered values:

- `primary`: selection, navigation, primary action
- `success`: target met / clear improvement
- `warning`: Stress, increased cost, deterioration requiring attention
- `danger`: target miss / actual residual shortage
- neutral surface / muted text / border roles

Status color must always be paired with explicit text such as `목표 충족`, `목표 미달`, `부족`, `변화 없음`.

Avoid gradient-heavy, neon, cyber-fintech, glow or decorative data-chrome styling.

### Typography

Use the existing Streamlit/system Korean sans-serif stack.

Guideline:

- product title: compact, visually below 40px
- decision headline: stronger than section titles, but not a marketing hero banner
- section title: clear 21–25px role
- primary financial values: 26–32px only when the number is a decision anchor
- setup values: compact label/value rows, not dashboard-sized metrics
- supporting copy: 13–15px with comfortable line height

A large number must always sit next to a label, context line or visible relationship.

### Spacing and surfaces

- use an 8px base rhythm
- centered content around the current 1180px maximum width
- use quiet borders and soft tinted surfaces
- avoid nested card-inside-card structures
- use whitespace to separate major decisions, not to create empty visual height

### Icons

Use the existing Lucide icon set.

- major sections may use one 36–40px soft icon tile
- icons supplement visible Korean labels and never carry meaning alone
- do not repeat icons on every metric or table row
- scenario chips do not need individual icons except where an icon carries real meaning, such as warning or add/custom

---

## Navigation

The React shell owns only the top navigation:

```text
입력 | 분석 | 보고서
```

Requirements:

- semantic buttons
- visible keyboard focus
- active state with restrained primary treatment
- icon + label
- reduced motion respected through `MotionConfig reducedMotion="user"`
- no financial calculations in React

The navigation must remain usable at 390px without page-level overflow.

---

## 입력 view

The default view of each subject is a summary surface, not raw widgets.

### 거래 정보

Show a concise summary of:

- export amount
- payment method
- collection timing
- major USD / JPY costs
- source/provenance

Actions are disclosures, not toggles:

- `정보 수정`
- `서류 불러오기`

Only the edit state exposes exact inputs.

### 회사 정보

Show compact label/value rows for:

- current usable cash
- minimum operating cash
- Deal-allocated cash
- unused working-capital line
- actual funding rate

Actions:

- `정보 수정`
- `자금계획 보기`

Company-wide cash and Deal-allocated cash must remain visibly distinct.

### Financial Statement AI

Financial-statement context is optional and secondary.

It should remain collapsed until explicitly requested and must not visually compete with the core company summary.

---

## 분석 view

This is the product's primary decision workspace.

Order:

1. deterministic conclusion
2. funding relationship
3. Company Liquidity Timeline
4. scenario comparison
5. response comparison
6. optional payment context

### Deterministic conclusion

Keep one bounded factual sentence as the main message.

Canonical style:

> 현재 거래는 목표마진을 충족하지만, 회사 전체 자금계획 기준 1,900만원이 부족합니다.

Small status badges may support the sentence, for example:

- `목표마진 충족`
- `자금부족 1,900만원`

Badges do not replace the sentence.

### Funding relationship

The signature relationship is:

```text
이번 거래 필요 외부자금
        + 회사 기존 일정
회사 전체 최대 자금부족
        - 현재 미사용 한도
남는 부족
```

Desktop may show three connected horizontal nodes. Mobile stacks them vertically.

Do not use `Peak` or internal implementation terms in public copy.

### Company cash-flow chart

The existing Company Liquidity Timeline is the primary evidence visualization.

It should make these relationships understandable:

- company existing plan
- company with prospective Deal
- minimum operating cash

Keep the chart visually prominent and the legend close to the plot.

Do not add unsupported scenario overlays or another chart library.

### Scenario presets

Preset scenarios should read as wrapping chips / segmented choices, not a raw calculator form.

Current presets:

- 기본
- USD -5%
- JPY +10%
- 금리 +1%p
- 회수 +30일
- 복합 악화
- 직접 설정

Base state should show one compact baseline summary instead of zero-delta comparisons.

Non-Base comparisons use:

```text
current → scenario
        delta
```

No slider + exact-input duplication.

Direct custom scenario exposes only the minimum exact fields needed.

### Response options

Current options:

- 기존 운전자금
- 매출채권 조기 현금화
- 선물환
- Banker's Usance

Selected option content should use one consistent comparison grammar:

```text
metric
current → option
delta
```

Assumptions stay behind `조건 수정` or an equivalent disclosure.

No recommendation or approval styling.

---

## 보고서 view

Order:

1. current deterministic result
2. optional AI 거래 검토
3. PDF 보고서

Do not duplicate the full Analysis dashboard.

### Current result

Use a compact summary surface with at most the most important current metrics, such as:

- current margin / target status
- company maximum gap
- residual gap after the current line
- selected scenario context

### AI 거래 검토

AI is an optional interpretation layer.

Copy should make the boundary clear:

- current calculation evidence is read
- financial numbers are not recalculated by AI
- user may edit the review question
- stale review requires rerun

Do not use chatbot styling.

### PDF metadata

Report metadata is a wrapping label/value list, not KPI metrics.

Long provenance or basis text must wrap naturally and never clip or ellipsize at 390px.

---

## Help and guidance

A single collapsed `용어·사용법` control sits below the navigation experience.

Its first level explains the current three-view workflow:

- 입력: 거래·회사 정보를 확인하고 필요할 때만 수정
- 분석: 현재 결과, 회사 현금흐름, 시나리오와 대응안을 비교
- 보고서: 현재 결과를 저장하고 선택적으로 AI 검토 실행

Financial terms remain individual native disclosures with:

- one plain-language definition
- one caution / calculation boundary

Help content remains one canonical Python presentation source in `components/trade_treasury_experience/__init__.py`.

Do not create separate tooltip, popover and manual copies that can drift.

---

## Product language

Prefer:

- `현재 마진` instead of `현재 Deal 마진`
- `이번 거래에 필요한 외부자금` instead of `거래만 본 은행 필요액`
- `회사 전체 최대 자금부족` instead of `Company-wide Peak 부족`
- `현재 한도 반영 후 부족` instead of `기존 한도 적용 후 부족`
- `회사 자금` instead of internal `liquidity` labels
- `자금·환위험` instead of exposing `Treasury` as a generic menu identity
- `거래 검토` instead of making AI the product identity

Keep actual practitioner terms such as O/A, Forward, Banker's Usance and Treasury only where their domain meaning is useful.

---

## Interaction and motion

Use motion only for short navigation/selection transitions and restrained hover/value transitions.

Respect `prefers-reduced-motion`.

Do not use:

- fake thinking states
- infinite pulse
- typewriter output
- decorative progress
- fake tool execution progress

Touch targets should be about 44px or larger where practical.

---

## Responsive behavior

At desktop widths:

- three-view navigation is horizontal
- funding relationship is horizontal
- setup label/value layouts may use two columns

At 390px:

- no page-level horizontal overflow
- navigation remains usable
- funding relationship stacks vertically
- scenario chips wrap
- comparison flows reflow without clipping
- report metadata becomes stacked label/value rows when needed

---

## Accessibility

Maintain:

- keyboard navigation
- visible focus
- semantic buttons/headings/disclosures
- readable contrast
- text-based status alongside color
- no hover-only explanation
- reflow without clipping at 390px

---

## Implementation notes

- canonical React tokens live in `components/trade_treasury_experience/frontend/src/styles.css`
- native Streamlit presentation styling lives in `assets/app.css`
- user-facing React shell copy is authored in `ExperienceShell.tsx`
- committed frontend build assets are runtime inputs; source changes require typecheck/build
- React owns navigation only
- Streamlit/Python owns inputs, finance, actions, external context, Agent and report
- dynamic content rendered through custom HTML must be escaped

---

## Do / Don't

Do:

- show decisions before forms
- explain what a number means
- keep one visible relationship between Deal need, company gap and residual gap
- use icons, badges and tints only when they improve comprehension
- preserve deterministic authority

Don't:

- calculate finance in JavaScript
- expose internal implementation vocabulary merely because it exists
- recreate a persistent KPI wall
- show sliders for scenario parameters already supported as exact inputs
- create another UI path for a visual redesign
- use chatbot, cyberpunk, glow, particle or recommendation styling

---

## Freeze

The current three-view Dashboard-First visual system is accepted for submission.

Before submission, visual or interaction changes require an evidenced P0 usability/accessibility problem. Cosmetic preference alone is not sufficient reason to reopen the UI.
