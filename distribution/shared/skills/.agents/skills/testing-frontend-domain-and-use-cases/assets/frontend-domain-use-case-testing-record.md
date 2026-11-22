# Frontend Domain and Use Case Testing Record

## Context

- Change/capability:
- Repository/package:
- Architecture profile:
- Domain models:
- Use Cases:
- Repository ports:
- InMemory repositories:
- External-service ports:
- Test runner:
- Applicable `AGENTS.md`:
- Tested by/date:

## Boundary Classification

| Behavior | Boundary | Why |
|---|---|---|
| | DOMAIN_TEST / USE_CASE_TEST / ADAPTER_TEST / HOOK_TEST / COMPONENT_TEST / E2E_TEST | |

## Domain Test Inventory

| Model | Behavior/invariant | Case | Expected |
|---|---|---|---|
| | | | |

- React imports:
- Browser globals:
- HTTP/provider imports:
- Mocks:
- Private-field assertions:
- Deterministic time/randomness:

## Use Case Inventory

| Use Case | Case | Observable result/state |
|---|---|---|
| | | |

## Collaborators

| Collaborator | Strategy | Why |
|---|---|---|
| Domain object | real | |
| Domain Service | real | |
| Repository | InMemory | |
| external port | stub/spy/fake | |
| clock | fixed double | |
| ID generator | deterministic double | |

## InMemory Repository

- Implementation:
- Fresh per test:
- Seed semantics:
- Save/replace semantics:
- Absence:
- Query semantics:
- Duplicate/conflict semantics:
- Failure simulation:
- Contract gaps:

## External Port Doubles

| Port | Double | Configurable result | Recorded semantic calls |
|---|---|---|---|
| | | | |

- Concrete vendor SDK mocks:
- Interaction assertions limited to semantic effects:

## Determinism

- Clock:
- IDs:
- Randomness:
- Locale:
- Timezone:
- Async sequencing:
- Arbitrary sleeps:
- Network:

## Result / State Assertions

- Response DTO:
- semantic result/error:
- persisted aggregate:
- repository-visible state:
- negative side effect:
- interaction-only assertions:
- transport details excluded:

## Duplicate Coverage Audit

| Behavior | Lowest useful boundary | Higher coverage needed |
|---|---|---|
| | | |

- Domain rule duplicated in component:
- Use Case orchestration duplicated in E2E:
- Hook-specific behavior separated:
- Adapter behavior separated:

## Regression Placement

- Bug:
- Root boundary:
- Regression test:
- Why not higher/lower:

## Execution Evidence

- Focused command:
- Result:
- Neighboring suite:
- Result:
- Duration:
- Flaky behavior:
- Browser required:
- Network required:

## Boundary Audit

- React:
- DOM/jsdom behavior:
- HTTP/fetch/Axios:
- localStorage/IndexedDB:
- concrete repository adapter:
- provider SDK:
- router:
- SWR/React Query:
- composition root:

## Final Decision

- Decision:
- Conditions:
- Blocking issue:
- Next skill:
- Required follow-up:
