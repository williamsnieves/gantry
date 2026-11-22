# Component Variant Design Record

## Context

- Change/component:
- Repository/application:
- Component owner:
- Shared or feature-local:
- Existing project primitive:
- Styling profile:
- Design-token source:
- Existing variant conventions:
- Accessibility baseline:
- Applicable `AGENTS.md`:
- Designed by/date:

## Readiness

- Component responsibility known:
- Shared/feature ownership known:
- Visual semantics known:
- State behavior known:
- Token source known:
- Initial decision:
- Conditions/blockers:

## Variant Justification

- Variant model required:
- Why:
- Decision: PROPORTIONATE_VARIANT_MODEL / UNDERMODELED_VARIANTS / OVERMODELED_VARIANTS / FEATURE_STYLING_LEAK / TOKEN_GAP / NO_VARIANT_MODEL_REQUIRED

## Component Responsibility

- Component semantic purpose:
- Stable interaction contract:
- Shared-system meaning:
- Feature-specific meaning:
- Business logic excluded:

## Variant Axes

| Axis | Type | Values | Semantic meaning |
|---|---|---|---|
| variant | VISUAL_VARIANT | | |
| size | SIZE | | |
| density | DENSITY | | |
| orientation | ORIENTATION | | |
| state | STATE | | |
| placement | PLACEMENT | | |

- Unneeded axes removed:

## Public Contract

```text

```

- Defaults:
- Required props:
- Optional props:
- Raw style knobs avoided:

## Boolean Prop Audit

| Current boolean | Same-axis conflict | Decision |
|---|---|---|
| primary | secondary/danger | replace with variant |
| small | medium/large | replace with size |
| loading | no same-axis conflict | keep boolean/state |
| disabled | no same-axis conflict | keep boolean/state |

- Contradictory combinations eliminated:

## Button Variants

- Applicable:
- Shared variants:
- Primary:
- Secondary:
- Danger/destructive:
- Ghost/subtle:
- Link:
- Feature-specific names rejected:
- Semantic rationale:

## Size Variants

| Size | Control height | Padding | Typography | Icon | Hit target |
|---|---|---|---|---|---|
| sm | | | | | |
| md | | | | | |
| lg | | | | | |

- Size meaning consistent:
- Density separated:
- Accessibility impact:

## Loading State

- Applicable:
- Meaning:
- Loading implies disabled: yes/no/conditional
- Cancellation allowed:
- Duplicate activation blocked:
- Spinner behavior:
- Label preservation:
- `aria-busy`/status:
- Width/layout stability:
- Focus behavior:

## Disabled State

- Semantic/native behavior:
- Visual treatment:
- Pointer behavior:
- Keyboard behavior:
- Disabled vs unavailable reason:
- Color-only communication avoided:

## State Priority

| State | Overrides |
|---|---|
| disabled | hover/active |
| loading | activation/interactive feedback |
| focus-visible | remains visible |
| invalid | neutral border/tone if applicable |

## Compound Variants

| Combination | Special behavior | Independent axes insufficient |
|---|---|---|
| | | |

- Decision: COMPOUND_VARIANT_JUSTIFIED / INDEPENDENT_AXES_SUFFICIENT / VARIANT_MODEL_TOO_COMPLEX / FEATURE_SPLIT_REQUIRED
- Compound count:
- Cartesian explosion risk:

## Invalid Combinations

| Combination | Why invalid | Prevention |
|---|---|---|
| | | TypeScript / runtime / API split |

- Type-level complexity proportionate:

## Shared vs Feature Ownership

| Proposed variant | Ownership | Reason |
|---|---|---|
| | SHARED_PRIMITIVE_VARIANT / FEATURE_WRAPPER_VARIANT / LOCAL_COMPONENT_VARIANT / NO_VARIANT_REQUIRED | |

- Feature-specific styling leaking into shared primitive:
- Feature wrapper needed:
- Shared primitive extension justified:

## Token Mapping Requirements

| Variant/state | Surface | Foreground | Border | Focus | Hover/active |
|---|---|---|---|---|---|
| | semantic token | | | | |

- Existing tokens:
- Token gaps:
- Feature-local values:
- Raw hex/palette not part of contract:

## Accessibility

- Accessible name:
- Focus-visible across all variants:
- Contrast:
- Disabled semantics:
- Loading semantics:
- Icon-only labeling:
- Color-only meaning avoided:
- Touch target:
- Reduced motion:

## Implementation Independence

- CSS Modules mapping possible:
- Tailwind mapping possible:
- Design-system recipe mapping possible:
- CSS-in-JS mapping possible:
- Class names absent from public contract:
- No variant library selected here:

## Representative Test Matrix

| Case | Expected |
|---|---|
| default variant | |
| each shared variant | |
| smallest/largest size | |
| loading | |
| disabled | |
| loading + disabled interaction | |
| representative compound | |
| invalid combination | |
| feature-only style | remains outside shared primitive |

- Full Cartesian matrix avoided:
- Visual regression:
- Component explorer:
- Class-string snapshots avoided:

## Overmodeling Audit

- Too many variant axes:
- Raw CSS property props:
- Shared variant for one feature:
- Duplicate aliases:
- Visual-only arbitrary color variants:
- Complex generic type system:
- Separate component preferable:

## Roadmap Evaluation Cases

### Button Variants
- Decision:
- Evidence:

### Size Variants
- Decision:
- Evidence:

### Compound Variants
- Decision:
- Evidence:

### Loading / Disabled State
- Decision:
- Evidence:

### Feature-Specific Styling in Shared Primitive
- Decision:
- Evidence:

## Final Decision

- Decision:
- Conditions:
- Blocking issue:
- Next skill:
- Required follow-up:
