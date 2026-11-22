# Responsive Layout Design Record

## Context

- Change/screen/component:
- Repository/application:
- Styling profile:
- Existing layout primitives:
- Breakpoint/token source:
- Supported viewport sizes:
- Supported container contexts:
- Localization requirements:
- RTL:
- Accessibility target:
- Browser support:
- Applicable `AGENTS.md`:
- Designed by/date:

## Readiness

- Layout semantics known:
- Content priority known:
- Breakpoint source known:
- Container query support known:
- Mobile table strategy needed:
- Initial decision:
- Conditions/blockers:

## Layout Purpose

- Primary content:
- Secondary content:
- Essential actions:
- Optional content:
- Comparison vs row-reading:
- Reusable component contexts:

## Primitive Decision

- Decision: NORMAL_FLOW / FLEXBOX / GRID / CONTAINER_QUERY / VIEWPORT_QUERY / HYBRID_LAYOUT
- Why:
- Primary axis:
- Two-dimensional tracks needed:
- Local-container dependence:
- Page-level viewport dependence:

## Container vs Viewport

- Same viewport, different parent widths possible:
- Component should adapt to parent:
- Container query:
- Viewport query:
- Hybrid:
- Reason:

## Breakpoints / Thresholds

| Transition | Failure point | Existing token | Decision |
|---|---|---|---|
| | | | |

- Device folklore avoided:
- Minimum thresholds:
- New global token required:
- Component-local threshold justified:

## Content Priority

| Region/action | Priority | Narrow behavior |
|---|---|---|
| | PRIMARY_ESSENTIAL / SECONDARY_ESSENTIAL / IMPORTANT / OPTIONAL / OVERFLOW_CANDIDATE | |

- Essential actions preserved:
- Hidden content equivalent access:

## Reflow Strategy

- Wide:
- Medium:
- Narrow:
- Stack:
- Wrap:
- Overflow menu:
- Local horizontal scroll:
- Column reduction:
- Separate representation:
- DOM order remains logical:

## Dashboard Grid

- Applicable:
- Grid/Flex decision:
- Track strategy:
- Minimum card width:
- auto-fit/explicit:
- Variable heights:
- Narrow stack:
- Card container responsiveness:
- Translation stress:

## Toolbar

- Applicable:
- Flex/other:
- Action priority:
- Wrap:
- Overflow:
- Stack:
- Primary action:
- DOM/tab order:
- Narrow labels:
- Zoom behavior:

## Card

- Applicable:
- Layout primitive:
- Container query:
- Fixed height:
- Fixed-height justification:
- Content wrapping:
- Actions:
- Media:
- Long labels:

## Mobile Table

- Applicable:
- Strategy: HORIZONTAL_SCROLL / PRIORITY_COLUMNS / TABLE_TO_CARDS / CONDENSED_TABLE / SEPARATE_MOBILE_REPRESENTATION
- Comparison priority:
- Hidden columns:
- Header labels preserved:
- Local scroll discoverability:
- Page overflow avoided:
- Shared data/view model:

## Translation

- Longest translation:
- CTA wrapping:
- Button label:
- Heading:
- Form label:
- Status:
- English-width assumptions removed:

## Zoom / Text Scaling

- 200%:
- 400%:
- Text-only scaling:
- Overlap:
- Clipping:
- Essential actions:
- Reflow:

## RTL / Logical Properties

- RTL supported:
- inline-start/end:
- padding/margin:
- sticky column:
- action order:
- directional icons:
- scroll affordance:

## Fixed Dimension Audit

| Element | Fixed dimension | Classification | Decision |
|---|---|---|---|
| | | JUSTIFIED_FIXED_SIZE / CONTENT_RISK / MEDIA_RATIO / CONTROL_SIZE / DECORATIVE / REMOVE_OR_RELAX | |

## Overflow Audit

- Type: INTENTIONAL_LOCAL_SCROLL / UNINTENDED_COMPONENT_OVERFLOW / UNINTENDED_PAGE_OVERFLOW / TEXT_OVERFLOW / MEDIA_OVERFLOW
- Root cause:
- Fixed width:
- min-content sizing:
- no-wrap:
- absolute positioning:
- transform:
- long unbroken text:
- intrinsic media:

## Structural Overflow Fix

- `min-width: 0`:
- `minmax(0, 1fr)`:
- wrapping:
- relaxed width/height:
- media max size:
- local scroll:
- truncation with full-value access:
- `overflow:hidden` avoided/justified:

## Responsive CSS vs JS

- CSS-native layout:
- Container query:
- Viewport query:
- JS measurement:
- ResizeObserver:
- JS behavior change genuinely required:
- Duplicate CSS/JS breakpoint logic:

## SSR / Hydration

- Styling-only responsiveness works before hydration:
- JS viewport branching:
- Hydration mismatch risk:
- Server-safe fallback:

## Roadmap Evaluation Cases

### Dashboard Grid
- Decision:
- Evidence:

### Toolbar
- Decision:
- Evidence:

### Card
- Decision:
- Evidence:

### Mobile Table
- Decision:
- Evidence:

### Translated CTA
- Decision:
- Evidence:

### Overflow Regression
- Root cause:
- Structural fix:
- Evidence:

## Test / Evidence Matrix

| Scenario | Width/container | Content stress | Expected |
|---|---|---|---|
| narrow | | | |
| threshold - 1 | | | |
| threshold | | | |
| threshold + 1 | | | |
| wide | | | |
| long translation | | | |
| 200% zoom | | | |
| 400% zoom | | | |
| long URL/ID | | | |
| RTL | | | |

- Real browser:
- Visual regression:
- Document page overflow assertion:
- Local scroll assertion:
- Device presets not sole evidence:

## Overmodeling Audit

- Too many breakpoints:
- Device-specific variants:
- JS measurement replacing CSS:
- Separate mobile component duplicates logic:
- Wrapper-only layout abstraction:
- Universal layout framework:
- Decision: PROPORTIONATE_RESPONSIVE_LAYOUT / UNDERMODELED_RESPONSIVENESS / OVERMODELED_RESPONSIVENESS / OVERFLOW_RISK / BREAKPOINT_TOKEN_GAP / RESPONSIVE_LAYOUT_NOT_REQUIRED

## Final Decision

- Decision:
- Conditions:
- Blocking issue:
- Next skill:
- Required follow-up:
