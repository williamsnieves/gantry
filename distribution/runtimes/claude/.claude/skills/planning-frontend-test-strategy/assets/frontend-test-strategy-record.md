# Frontend Test Strategy Record

## Context

- Change/capability:
- Scope:
- Repository/application:
- Architecture profile:
- Vertical slices:
- Existing tooling:
- CI environments:
- Browser/AT support policy:
- Applicable `AGENTS.md`:
- Planned by/date:

## Readiness

- Acceptance criteria complete:
- Architecture boundaries known:
- Adapter/environment contracts:
- Accessibility evidence requirements:
- Visual requirements:
- E2E environment:
- Initial decision:
- Conditions/blockers:

## Behavior and Risk Inventory

| ID | Behavior | Classification | Risk | Historical regression | External boundary |
|---|---|---|---|---|---|
| | | PURE_RULE/USER_INTENTION/DATA_MAPPING/ASYNC_STATE_TRANSITION/UI_INTERACTION/ACCESSIBILITY_BEHAVIOR/VISUAL_BEHAVIOR/ROUTE_INTEGRATION/PACKAGE_CONTRACT/CRITICAL_JOURNEY/MANUAL_ONLY_EVIDENCE | LOW/MODERATE/HIGH/CRITICAL | | |

## Test Boundary Matrix

| Behavior | Lowest reliable boundary | Additional confidence boundary | Unique purpose | Status |
|---|---|---|---|---|
| | DOMAIN/USE_CASE/ADAPTER/HOOK/COMPONENT/ACCESSIBILITY/VISUAL/ROUTE/PACKAGE/E2E/MANUAL_AT | | | PLANNED/BLOCKED/DEFERRED |

## Domain Coverage

- Entities/Value Objects/Services:
- Boundaries/equivalence classes:
- State transitions:
- Property-based cases:
- Dependencies excluded:
- Environment:

## Application Use Case Coverage

| Use Case | InMemory ports | True external doubles | Outcomes |
|---|---|---|---|
| | | | |

- Repository mocks excluded:
- Orchestration evidence:
- Cancellation/idempotency:
- Environment:

## Adapter Coverage

| Adapter | Boundary | Cases | Environment |
|---|---|---|---|
| | real sandbox/test server/MSW/contract fixture/emulator/storage runtime | mapping/failure/cancel/pagination/migration | |

- Adapter self-mocking excluded:
- Technical leakage assertions:
- Provider sandbox requirements:

## Hook Coverage

| Hook | Observable state/commands | Race/cancel/retry | Independent test justified |
|---|---|---|---|
| | | | |

- Internal details excluded:
- Pure helpers/reducers:
- Library internals excluded:

## Component Coverage

| Component/interaction | Semantic query | States/interactions | Dependency setup |
|---|---|---|---|
| | | | |

- Keyboard/focus:
- Error/status:
- State preservation:
- DOM/class implementation assertions excluded:

## Accessibility Evidence

| Journey/criterion | Automated | Component/browser | Manual/AT |
|---|---|---|---|
| | | | |

- Automated limitations:
- Keyboard matrix:
- Focus matrix:
- Zoom/reflow:
- Contrast/themes:
- Representative AT:

## Visual Regression

| Surface | Viewport/theme/data | Risk | Baseline owner |
|---|---|---|---|
| | | | |

- Animation/font stabilization:
- Threshold/review policy:
- Trivial snapshots excluded:

## Route and Package Integration

- Routing/URL state:
- Providers/composition:
- Hydration:
- Package exports/contracts:
- Consumer applications:
- Deep-import checks:

## E2E Journey Selection

| Journey | Business/integration risk | Decision | Paths covered |
|---|---|---|---|
| | | E2E_REQUIRED/ROUTE_INTEGRATION_SUFFICIENT/LOWER_BOUNDARY_SUFFICIENT/MANUAL_PRODUCTION_CHECK_ONLY/NOT_IN_SCOPE | |

- Essential success:
- Critical failure/recovery:
- Browser/deployment risk:
- Local branches intentionally excluded:
- All-E2E strategy rejected:

## Duplication Review

| Scenario at multiple levels | Unique purpose per level | Keep/remove |
|---|---|---|
| | | |

## Test-Double Policy

| Dependency | Double | Reason | Scope |
|---|---|---|---|
| | REAL_IMPLEMENTATION/IN_MEMORY_IMPLEMENTATION/FAKE/STUB/SPY/MOCK_SERVER/EMULATOR/SANDBOX/FIXTURE/VIRTUAL_CLOCK/NO_DOUBLE | | |

- Never mocked:
- Repository InMemory policy:
- External ports:
- Fetch-internal mocks excluded:

## Environment Matrix

| Suite | Environment | Missing fidelity/risk |
|---|---|---|
| | NODE/JSDOM/HAPPY_DOM/REAL_BROWSER/TEST_SERVER/MSW/EMULATOR/SANDBOX/STORYBOOK_OR_COMPONENT_HARNESS/PRODUCTION_SMOKE/ASSISTIVE_TECHNOLOGY | |

## Test Data and Determinism

- Builders/factories:
- Minimal fixtures:
- Clock:
- Random IDs:
- Locale/timezone:
- Permissions:
- Long text:
- Themes:
- Network:
- Storage/cache:
- Concurrency:
- Sensitive-data policy:

## Flakiness Controls

- Arbitrary sleeps excluded:
- Observable waits:
- Shared account/data isolation:
- Retry policy:
- Selector policy:
- Animation:
- Background requests:
- Cross-test global state:
- Quarantine/removal policy:

## CI Plan

| Suite | Stage | Blocking | Parallelization |
|---|---|---|---|
| | PRE_COMMIT/PULL_REQUEST_FAST/PULL_REQUEST_BROWSER/MAIN_BRANCH/NIGHTLY/RELEASE_GATE/POST_DEPLOYMENT_SMOKE/MANUAL_REVIEW | | |

- Sharding:
- Data isolation:
- Sandbox rate limits:
- Expected duration:

## Regression Plan

| Risk/incident | Missing evidence | New smallest reliable regression test | Owner |
|---|---|---|---|
| | | | |

- Characterization coverage:
- Coverage metric role:
- Mutation testing:

## Ownership and Maintenance

- Capability owner:
- Test environment owner:
- Fixture/data owner:
- Visual baseline reviewer:
- E2E triage owner:
- Accessibility evidence owner:
- Flake-removal SLA/policy:
- Test removal/deprecation trigger:

## Gaps and Residual Risks

| Gap | User/business impact | Status | Owner/trigger |
|---|---|---|---|
| | | BLOCKED_BY_ENVIRONMENT/MANUAL_EVIDENCE_REQUIRED/DEFERRED_WITH_TRIGGER | |

## Final Decision

- Decision:
- Conditions:
- Blocking issue:
- First implementation skill:
- Required follow-up:
