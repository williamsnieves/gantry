# Tailwind UI Implementation Record

## Context

- Change/component:
- Repository/application:
- Tailwind version:
- Selected styling profile:
- Theme/token source:
- Dark/theme strategy:
- Responsive strategy:
- Project primitive library:
- Class composition utility:
- Class merge/conflict utility:
- Accessibility baseline:
- Applicable `AGENTS.md`:
- Implemented by/date:

## Readiness

- Tailwind selected:
- Version/conventions known:
- Theme tokens known:
- Primitive strategy known:
- Variant contract known:
- Responsive policy known:
- Dark-mode policy known:
- Class-merge policy known:
- Initial decision:
- Conditions/blockers:

## Styling Ownership

- Project primitive used:
- Feature-local utilities:
- Shared variant abstraction:
- Global token need:
- Hybrid styling boundary:
- Decision: PROPORTIONATE_TAILWIND_UI / UNDERMODELED_VARIANTS / OVERMODELED_TAILWIND_UI / TOKEN_GAP / STYLING_PROFILE_MISMATCH

## Component Semantics

- Component:
- Variants:
- Sizes:
- States:
- Layout:
- Responsive behavior:
- Runtime values:

## Utility Composition

```text

```

- Layout utilities:
- Spacing:
- Typography:
- Surface:
- Interaction:
- State:
- Responsive:
- Theme:
- Readable without extraction:

## Long Class List

- Long list present:
- Cohesive element:
- Formatting:
- Repeated semantic fragments:
- Extraction decision:
- Target: keep local / local constant / feature component / project primitive / existing variant utility
- `@apply` avoided/justified:

## Repeated Button Classes

- Repetition locations:
- Same semantic button:
- Existing project Button:
- Existing variant:
- Feature-local component justified:
- Coincidental duplication:
- Shared abstraction decision:

## Variants

| Variant/state | Tailwind utilities | Existing primitive/recipe |
|---|---|---|
| | | |

- Contradictory booleans avoided:
- Existing CVA/recipe utility:
- New variant tool introduced:
- Compound variants justified:

## Arbitrary Values / Tokens

| Utility/value | Existing token | Classification | Decision |
|---|---|---|---|
| | | semantic token / structural local / runtime / missing global token | |

- Repeated arbitrary colors:
- Theme palette vs semantic token:
- Missing global token:
- Escalation target:
- Global hardcoded copy avoided:

## Runtime Values

| Runtime value | Source | Technique |
|---|---|---|
| | | inline style / CSS variable + Tailwind |

- Continuous classes not generated:
- Dynamic unbounded class names avoided:
- Input constrained:

## Dark / Theme Mode

- Strategy:
- Semantic token utilities:
- Explicit `dark:` needed:
- Why:
- Repeated raw light/dark pairs removed:
- Theme-specific structural behavior:
- Alternate theme mechanism introduced:

## Responsive Variant

- Behavior: viewport / container
- Current classes:
- Approved breakpoint:
- Arbitrary breakpoint:
- Container-query capability:
- Layout primitive:
- Narrow layout:
- Wide layout:
- Translation expansion:
- Zoom/reflow:
- Essential actions:
- Fixed dimensions justified:

## Class Conflicts

| Source | Conflict | Intended winner | Resolution |
|---|---|---|---|
| base vs variant | | | |
| variant vs state | | | |
| primitive vs caller | | | |
| responsive | | | |
| theme | | | |

- Existing merge utility:
- Caller `className` policy: CALLER_MAY_OVERRIDE / CALLER_ADDS_LAYOUT_ONLY / CALLER_CLASSNAME_NOT_SUPPORTED / MERGED_WITH_PROJECT_POLICY
- Component invariants protected:
- Important modifier used:
- Important justification:

## Dynamic Classes / Content Scan

- Runtime concatenation:
- Explicit mapping:
- Safelist:
- Safelist bounded:
- Plugin required:
- Build scanning safe:

## Primitive Integration

- Shared primitive:
- Variant API used:
- Public className/slot API:
- Accessibility behavior preserved:
- Primitive classes duplicated:
- Vendor internals targeted:

## Accessibility

- Visible focus:
- Disabled semantics:
- Invalid semantics:
- Contrast:
- Color-only meaning:
- Reduced motion:
- High contrast:
- Hit target:
- Content wrapping:
- Reflow/zoom:

## Roadmap Evaluation Cases

### Long Class List
- Finding:
- Decision:

### Repeated Button Classes
- Finding:
- Decision:

### Responsive Variant
- Finding:
- Decision:

### Arbitrary Token
- Finding:
- Decision:

### Dark Mode
- Finding:
- Decision:

### Class Conflict
- Finding:
- Decision:

## Testing / Evidence

- Component semantic tests:
- Variant tests:
- Huge class-string snapshot avoided:
- Class conflict representative test:
- Runtime CSS-variable test:
- Responsive browser/visual evidence:
- Dark/theme visual evidence:
- Accessibility evidence:
- Existing component explorer:
- No new tool introduced:

## Overmodeling Audit

- CVA for tiny component:
- tailwind-merge added for one conflict:
- all class lists extracted:
- `@apply` component library:
- giant safelist:
- custom plugin:
- global utility for one feature:
- duplicated project primitive:

## Final Decision

- Decision:
- Conditions:
- Blocking issue:
- Next skill:
- Required follow-up:
