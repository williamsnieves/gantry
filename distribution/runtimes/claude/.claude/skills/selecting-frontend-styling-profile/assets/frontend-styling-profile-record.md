# Frontend Styling Profile Record

## Context

- Change/capability:
- Scope: WORKSPACE / APPLICATION / PACKAGE / CAPABILITY / FEATURE / COMPONENT_FAMILY
- Repository/application:
- Architecture profile:
- Component/slice:
- Applicable `AGENTS.md`:
- Existing design decisions:
- Prepared by/date:

## Readiness

- Accepted visual behavior:
- Existing style evidence:
- Primitive ownership:
- Token source:
- Theme policy:
- Responsive policy:
- Accessibility baseline:
- Migration status:
- Initial decision:
- Conditions/blockers:

## Existing Styling Systems

| System | Scope | Current owner | Policy/evidence |
|---|---|---|---|
| CSS Modules | | | |
| Tailwind | | | |
| CSS-in-JS | | | |
| Vanilla/global CSS | | | |
| Company design system | | | |
| shadcn/ui | | | |
| Headless primitives | | | |
| Native HTML | | | |

## Competition and Boundaries

- Classification: COHERENT_SUPPORTING_TOOLS / EXPLICIT_HYBRID / ACCIDENTAL_MIXTURE / MIGRATION_IN_PROGRESS / CONFLICT_REQUIRES_DECISION
- Competing roles:
- Conflict precedence:
- Forbidden combinations:
- Migration boundary:

## Selected Profile

- Primary classification:
- Supporting systems:
- Decision:
- Rationale:
- Why alternatives were rejected:
- Why this is the smallest coherent strategy:

## Hybrid Boundary

| Layer/scope | Allowed system | Forbidden system | Owner |
|---|---|---|---|
| Shared primitives | | | |
| Feature layout | | | |
| Component variants | | | |
| Third-party integration | | | |
| Themes/tokens | | | |
| Package public UI | | | |

## Primitive Ownership

| Primitive/component type | Ownership | Allowed import path | Accessibility owner | Styling owner |
|---|---|---|---|---|
| Native controls | | | | |
| Shared UI | | | | |
| Headless vendor | | | | |
| Feature-local UI | | | | |
| Package public UI | | | | |

- Raw vendor imports:
- Wrapper policy:
- Upgrade owner:
- Shared promotion criteria:
- Business logic excluded:

## Token Source

- Authoritative source:
- Supporting/generated representations:
- Token categories:
- Semantic naming:
- Raw-value policy:
- Hardcoded-value exception:
- Conflicting token sources:

## Variant Strategy

- Selected strategy:
- Typed/discriminated variants:
- State attributes:
- Contradictory booleans prevented:
- Extension policy:
- Class conflict policy:
- Repeated-style extraction trigger:

## Theming

- Theme classification:
- Owner/provider:
- Mechanism:
- Persistence:
- SSR/hydration:
- Multi-brand/tenant behavior:
- Contrast validation:
- Theme-switch validation:
- Second-provider risk:

## Responsive Strategy

- Classification:
- Breakpoint source:
- Flexbox use:
- Grid use:
- Container queries:
- Viewport queries:
- Fluid sizing:
- Overflow/wrapping:
- Translation expansion:
- Zoom/text scaling:
- Logical properties:
- Fixed-dimension exceptions:

## Global CSS and Specificity

- Global allowed:
- Feature-scoped required:
- Third-party global boundary:
- Selector-depth policy:
- Cascade layers:
- `!important` policy:
- Deep-selector policy:
- State/data-attribute policy:
- Specificity escalation risk:

## Runtime Values and Inline Styles

| Runtime value | Allowed mechanism | Safety/SSR notes |
|---|---|---|
| | inline style / CSS custom property / generated class / not allowed | |

- Inline-style boundary:
- Sanitization:
- Hydration consistency:
- Second-system risk:

## Accessibility Baseline

- Target:
- Semantic HTML:
- Keyboard:
- Focus-visible:
- Disabled/invalid:
- Contrast:
- Non-color meaning:
- Zoom/reflow:
- Reduced motion:
- Forced colors/high contrast:
- Touch targets:
- Library claims independently verified:

## Motion, Typography, and Layering

- Motion tokens:
- Reduced-motion behavior:
- Typography source:
- Localization/script support:
- Font loading:
- Z-index scale:
- Overlay ownership:

## Component Ownership

| Component | Classification | Consumers | Owner | Promotion status |
|---|---|---|---|---|
| | FEATURE_LOCAL/CAPABILITY_SHARED/APPLICATION_SHARED/DESIGN_SYSTEM/PACKAGE_PUBLIC/THIRD_PARTY_BOUNDARY | | | |

- Feature-local default:
- Shared evidence:
- Public package contract:
- Escape hatches:

## Exception Policy

| Exception | Classification | Scope | Reason/risk | Owner | Removal trigger |
|---|---|---|---|---|---|
| | APPROVED_PERMANENT_EXCEPTION/APPROVED_TEMPORARY_EXCEPTION/MIGRATION_EXCEPTION/THIRD_PARTY_EXCEPTION/ACCESSIBILITY_EXCEPTION_REQUIRES_REVIEW/UNAPPROVED_EXCEPTION | | | | |

## Migration

- Current profile:
- Target profile:
- New-code policy:
- Migration unit:
- Compatibility period:
- Token alignment:
- Wrapper/adapter boundary:
- Removal trigger:
- Repository-wide rewrite excluded:

## Validation Matrix

| Evidence | Required | Scope/tooling |
|---|---|---|
| Style lint/build | | |
| Typecheck/variant API | | |
| Component tests | | |
| Accessibility | | |
| Visual regression | | |
| Responsive | | |
| Theme | | |
| Reduced motion | | |
| Package/consumer build | | |
| Forbidden import check | | |
| Bundle/runtime impact | | |

## Decisions and Risks

| Question/risk | Owner | Blocking |
|---|---|---|
| | | |

## Final Decision

- Decision:
- Conditions:
- Blocking issue:
- Next skill:
- Required follow-up:
