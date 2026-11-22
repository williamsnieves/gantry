# Frontend Vertical Slice Plan

## Context

- Change/specification:
- Repository/application:
- Owning capability:
- Architecture profile:
- Frontend standard record:
- Profile classification record:
- Applicable `AGENTS.md`:
- Planned by/date:

## Readiness

- Accepted behavior:
- Acceptance criteria:
- Data/API contract:
- Design status:
- Accessibility status:
- Migration/rollout status:
- Initial decision:
- Conditions/blockers:

## Behavior Inventory

| ID | Actor/context | Trigger | Visible/semantic outcome | State/data effect | Failure outcomes | Classification |
|---|---|---|---|---|---|---|
| | | | | | | PRIMARY_SUCCESS/ALTERNATIVE_SUCCESS/VALIDATION_FAILURE/SEMANTIC_FAILURE/AUTHORIZATION_FAILURE/SYSTEM_FAILURE/EMPTY_STATE/LOADING_STATE/RETRY_OR_RECOVERY/NAVIGATION_OR_COMPOSITION/MIGRATION_OR_COMPATIBILITY |

## Capability and Ownership

- Owning capability:
- Route/screen/package entry:
- Feature-local boundary:
- Existing shared dependencies:
- Cross-capability dependencies:
- Public-contract owner:
- Explicitly excluded shared extraction:

## Slice Summary

| Slice | User-visible outcome | Owner | Dependencies | Readiness |
|---|---|---|---|---|
| | | | HARD/SOFT/PARALLEL/BLOCKED | SLICE_READY/SLICE_READY_WITH_CONDITIONS/SLICE_BLOCKED/SLICE_NEEDS_REFINEMENT |

## Slice 1 — <Name>

### User Outcome

- Actor/context:
- Trigger:
- Visible result:
- Included acceptance cases:
- Explicitly excluded cases:

### Boundaries

| Boundary | Status | Responsibility |
|---|---|---|
| Frontend Domain | REQUIRED/REUSED/NOT_APPLICABLE/DEFERRED_WITH_TRIGGER/DECISION_REQUIRED | |
| Application | | |
| Port | | |
| Adapter | | |
| Server state | | |
| Local/form/router/browser state | | |
| Composition | | |
| Component | | |
| Custom hook | | |
| Effect | | |
| Styling/design system | | |
| Accessibility | | |
| Package/public contract | | |

### Data and Mapping

- Request/input mapping:
- Runtime decoding:
- Response mapping:
- Error translation:
- Date/enum/null conversion:
- Cache/update/invalidation:
- Cancellation:
- Optimistic/rollback/reconciliation:
- Raw external types excluded:

### UI State Matrix

| State | Included | Visible behavior | Owner |
|---|---|---|---|
| INITIAL | | | |
| LOADING | | | |
| EMPTY | | | |
| READY | | | |
| SUBMITTING | | | |
| SUCCESS | | | |
| DUPLICATE_OR_IDEMPOTENT_SUCCESS | | | |
| VALIDATION_ERROR | | | |
| SEMANTIC_ERROR | | | |
| FORBIDDEN | | | |
| UNAVAILABLE | | | |
| RETRYING | | | |
| STALE/PARTIAL | | | |
| OFFLINE | | | |
| DISABLED | | | |

### Accessibility Checkpoints

- Semantic element:
- Accessible name/description:
- Keyboard behavior:
- Focus behavior:
- Error/status announcement:
- Busy/disabled semantics:
- Zoom/reflow:
- Reduced motion:
- Contrast/theme:
- Automated/manual evidence:

### Styling and Responsive Behavior

- Styling profile:
- Existing primitives:
- Tokens/variants:
- Small viewport:
- Large viewport:
- Long text/localization:
- Focus/error/pending states:
- Visual regression:

### Test Matrix

| Behavior | Cheapest reliable level | Test/evidence | Required |
|---|---|---|---|
| | DOMAIN/USE_CASE/ADAPTER/HOOK/COMPONENT/ACCESSIBILITY/E2E/PACKAGE/ARCHITECTURE | | |

### Implementation Sequence

1.
2.
3.

### Completion Evidence

- Focused tests:
- Accessibility:
- Typecheck/lint:
- Build:
- Integration/E2E:
- Architecture/package:
- Manual verification:
- Status:

## Cross-Slice Dependency Map

```text

```

## Overall Implementation Sequence

1.
2.
3.

## Parallelizable Work

| Work | Can run with | Coordination boundary |
|---|---|---|
| | | |

## Brownfield or Migration Plan

- Current path:
- Target path:
- Characterization:
- Seam:
- Feature flag/routing:
- Compatibility:
- Rollback:
- Removal condition:
- Unrelated files excluded:

## Deferred Complexity and Triggers

| Deferred item | Why excluded now | Trigger |
|---|---|---|
| | | |

## Risks and Decisions

| Risk/question | Impact | Owner | Blocking |
|---|---|---|---|
| | | | |

## Final Decision

- Decision:
- Conditions:
- Blocking issue:
- First implementation skill:
- Required follow-up:
