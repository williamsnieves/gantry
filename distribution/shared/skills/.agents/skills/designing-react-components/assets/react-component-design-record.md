# React Component Design Record

## Context

- Change/slice:
- Repository/application:
- Owning capability:
- Architecture profile:
- Route/screen:
- Existing component(s):
- Design system/styling profile:
- Applicable `AGENTS.md`:
- Designed by/date:

## Readiness

- Accepted visible behavior:
- Interaction states:
- Data/state owner:
- Accessibility pattern:
- Design-system primitive:
- Initial decision:
- Conditions/blockers:

## Responsibility Inventory

| Responsibility | Classification | Proposed owner |
|---|---|---|
| | PRESENTATION/INTERACTION_WIRING/DATA_ORCHESTRATION/BUSINESS_DECISION/EXTERNAL_SYNCHRONIZATION/ROUTING/DEPENDENCY_COMPOSITION/STYLING/ACCESSIBILITY | |

## Current Component Problems

- Repository/fetch/adapter access:
- Business rules:
- Effects in render:
- Contradictory state booleans:
- Prop drilling:
- Mixed interaction regions:
- Accessibility issues:
- Reuse ambiguity:
- Server/client boundary issues:

## Proposed Component Tree

```text

```

| Component | Role | Responsibility | Ownership |
|---|---|---|---|
| | ROUTE_OR_SCREEN_CONTAINER/FEATURE_CONTAINER/FEATURE_COMPONENT/PRESENTATIONAL_COMPONENT/DESIGN_SYSTEM_COMPONENT/LAYOUT_COMPONENT/ERROR_OR_LOADING_BOUNDARY | | |

## Container and Presentation Decision

- Decision:
- Container responsibilities:
- Presentation responsibilities:
- Colocation decision:
- Existing composition root:
- Dependencies selected:
- Why a wrapper is or is not justified:

## Props Contract

### `<ComponentName>`

| Prop | Type/shape | Category | Required/default | Meaning |
|---|---|---|---|---|
| | | VIEW_DATA/RENDER_STATE/USER_EVENT/ACCESSIBILITY/COMPOSITION_SLOT/VISUAL_VARIANT/DEPENDENCY/ROUTING | | |

- Catch-all objects rejected:
- Concrete dependencies excluded:
- Forbidden combinations:
- Defaults:
- Serialization/server-client constraints:

## Event Contract

| Event | Parameters | Intent | Busy/duplicate behavior | Error ownership |
|---|---|---|---|---|
| | | | | |

## State Ownership

- Controlled/uncontrolled:
- Source of truth:
- Local ephemeral state:
- Form state:
- Server state:
- Derived state:
- State setters exposed:
- Context required:

## Rendering-State Model

```text

```

| State | Visible regions | Enabled actions | Retained data | Focus/announcement |
|---|---|---|---|---|
| INITIAL | | | | |
| LOADING | | | | |
| EMPTY | | | | |
| READY | | | | |
| SUBMITTING | | | | |
| SUCCESS | | | | |
| PARTIAL/STALE | | | | |
| VALIDATION_ERROR | | | | |
| SEMANTIC_ERROR | | | | |
| FORBIDDEN/NOT_FOUND | | | | |
| UNAVAILABLE/RETRYING | | | | |
| DISABLED | | | | |

- Invalid combinations prevented:
- Background refresh combination:
- Transition owner:

## Component Splitting

| Region/responsibility | Separate component | Reason |
|---|---|---|
| | | |

- Splits rejected as meaningless:
- Reusable substructures:
- Independent test boundaries:

## Prop Drilling and Context

- Drilling path:
- Legitimate composition:
- Proposed change:
- Context status:
- Provider scope/owner:
- Value stability:
- Missing-provider behavior:
- Global state explicitly rejected:

## Reuse and Placement

- Classification:
- Real consumers:
- Feature-local path:
- Shared/design-system/public contract:
- Owner:
- Promotion trigger:
- Speculative reuse excluded:

## Composition API

- Selected pattern: plain props / children / named slots / compound / render prop / context-backed compound
- Why:
- Alternatives rejected:
- Render-prop decision:
- Escape hatches:

## Semantic HTML Structure

```text

```

| Interaction/region | Native element/primitive | Accessible name/description |
|---|---|---|
| | | |

## Accessibility Contract

- Keyboard:
- Focus order:
- Focus placement/return:
- Visible focus:
- Busy semantics:
- Disabled semantics:
- Invalid/error association:
- Live-region/status:
- Zoom/reflow:
- Reduced motion:
- Contrast/theme:
- Touch target:
- Approved accessible primitive:

## Error and Empty-State Design

- Validation:
- Semantic rejection:
- Permission:
- Not found:
- Unavailable/network:
- Unknown:
- Cancellation:
- Empty state:
- Technical details excluded:

## Server/Client Boundary

- Classification:
- Server-owned rendering:
- Client interaction boundary:
- Browser APIs/hooks/effects:
- Serializable props:
- Suspense/error boundary:
- Client-only scope minimized:

## Styling Contract

- Styling profile:
- Tokens:
- Variants:
- Responsive:
- Theme:
- Focus/pending/error/disabled:
- Class extension:
- Visual regression:

## Test Boundary

| Behavior | Component test | Lower/higher test level |
|---|---|---|
| | | |

- Semantic queries:
- User-event coverage:
- Accessibility checks:
- Focus/status assertions:
- Implementation details excluded:

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
