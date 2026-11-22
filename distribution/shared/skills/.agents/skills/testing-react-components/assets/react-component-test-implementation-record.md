# React Component Test Implementation Record

## Context

- Change/component:
- Repository/application:
- Test strategy record:
- Component design record:
- Accessibility record:
- Test stack:
- Render helper/providers:
- Applicable `AGENTS.md`:
- Implemented by/date:

## Readiness

- Accepted behavior:
- Selected component cases:
- Dependency boundary:
- HTTP/mock-server requirement:
- Accessibility requirements:
- Real-browser requirements:
- Initial decision:
- Conditions/blockers:

## Behavior Matrix

| Behavior | User trigger | Observable outcome | Test boundary |
|---|---|---|---|
| | | | component / browser escalation |

## Semantic Query Map

| Element/status | Preferred selector | Accessible name/text |
|---|---|---|
| | role / label / text / status / test-id escape hatch | |

- Test IDs required:
- Brittle selectors rejected:

## Provider and Dependency Setup

| Dependency/provider | Test implementation | Scope |
|---|---|---|
| | semantic spy / fake / provider / isolated cache / router / i18n / theme / MSW | per test / suite |

- Concrete Infrastructure injected directly:
- Global production patching:
- Cache isolation:
- Handler reset:

## State Coverage

| State | Required | Observable assertion |
|---|---|---|
| INITIAL | | |
| LOADING | | |
| EMPTY | | |
| READY | | |
| SUBMITTING | | |
| SUCCESS | | |
| VALIDATION_ERROR | | |
| SEMANTIC_ERROR | | |
| FORBIDDEN | | |
| UNAVAILABLE | | |
| RETRY | | |
| DISABLED | | |

## Interaction Coverage

| Interaction | User action | Semantic command/outcome |
|---|---|---|
| | | |

## Form Coverage

- Label/name:
- Input:
- Submit:
- Busy/duplicate behavior:
- Validation:
- Semantic rejection:
- Data preservation:
- Success:
- Focus:
- Status:

## Keyboard and Focus

| Scenario | Keys/action | Expected focus/behavior |
|---|---|---|
| | | |

- Positive tabindex reliance:
- Focus restoration:
- Focus after error:
- Component environment fidelity:

## Accessibility Evidence

- Roles/names:
- Labels/descriptions:
- Error association:
- Busy/disabled/invalid:
- Status messages:
- Automated check:
- Automated limitations:
- Manual/browser/AT escalation:

## HTTP / Server-State Integration

- Integrated boundary:
- MSW/equivalent:
- Representative cases:
- Adapter branches intentionally excluded:
- Library internals intentionally excluded:
- Visible cache/mutation outcome:

## Async Behavior

- Observable wait:
- Arbitrary sleeps:
- Fake timers:
- Race/cancellation case:
- Pending cleanup:
- Background requests:

## Regression Coverage

| Defect/risk | Smallest semantic regression test |
|---|---|
| | |

## Anti-Brittleness Review

- Internal state assertions:
- Setter/dispatch assertions:
- Hook/Effect call assertions:
- Wrapper hierarchy:
- CSS classes:
- Snapshots:
- Incidental copy:
- DOM path selectors:

## Escalation

| Behavior | Component environment sufficient | Escalation |
|---|---|---|
| | yes/no | visual / real browser / route / E2E / manual AT |

## Test Evidence

| Test/check | Result |
|---|---|
| Focused component suite | |
| Automated accessibility | |
| Typecheck/lint if applicable | |
| Real-browser follow-up | |

## Residual Risks

| Risk/gap | Status | Owner |
|---|---|---|
| | | |

## Final Decision

- Decision:
- Conditions:
- Blocking issue:
- Next skill:
- Required follow-up:
