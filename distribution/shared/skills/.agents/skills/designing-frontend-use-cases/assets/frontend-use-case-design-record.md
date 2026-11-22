# Frontend Use Case Design Record

## Context

- Change/capability:
- Repository/application:
- Architecture profile:
- Accepted behavior:
- Frontend Domain model:
- Available ports:
- Backend authority:
- Offline/local behavior:
- Package/public boundary:
- Test strategy:
- Applicable `AGENTS.md`:
- Designed by/date:

## Readiness

- User/system intention known:
- Application layer justified:
- Domain decision:
- Port contracts:
- Failure semantics:
- Cancellation policy:
- Initial decision:
- Conditions/blockers:

## Intention

- Use Case name:
- Actor:
- Intention:
- Trigger:
- Completion meaning:
- Command/query classification: QUERY / COMMAND / COMMAND_WITH_RESULT / SYNC_ORCHESTRATION / LOCAL_WORKFLOW
- Justification: USE_CASE_JUSTIFIED / USE_CASE_BOUNDARY_VALUE_ONLY / USE_CASE_OVERMODELED / NO_USE_CASE_REQUIRED

## Primary Operation

```text

```

- Operation name:
- Async:
- Why one primary operation is sufficient:
- Internal helper operations:

## Input Decision

- Input style: PRIMITIVES / REQUEST_DTO / DOMAIN_TYPE / NO_INPUT
- Why:
- Optional values:
- Evolution risk:
- Package boundary:

### Request DTO

```text

```

| Field | Type | Semantic meaning | Optional |
|---|---|---|---|
| | | | |

- Transport casing excluded:
- React/browser/provider types excluded:
- Catch-all flags excluded:

## Input Validation

| Concern | Owner |
|---|---|
| Shape | Application/boundary |
| Domain invariant | Domain |
| Server authority | Backend |

- Value Object creation:
- Domain validation:
- Server-only validation explicitly not duplicated:

## Dependencies / Ports

| Dependency | Type | Why Application needs it | Concrete implementation excluded |
|---|---|---|---|
| | repository/external service/clock/id/analytics/feature flag/local persistence/sync | | |

- HttpClient excluded:
- Fetch/Axios excluded:
- Browser globals excluded:
- Global Factory excluded:

## Domain Interaction

| Step | Domain concept/behavior | Purpose |
|---|---|---|
| | | |

- Domain rules duplicated in Use Case:
- Pure business logic still misplaced in Application:

## Orchestration

```text

```

- Load/read:
- Domain decision:
- Write/save:
- External service:
- Analytics:
- Sync/local persistence:
- Partial success:
- Transaction assumptions explicitly excluded:

## Use Case Chaining Audit

- Calls another Use Case:
- Shared behavior owner:
- Domain helper candidate:
- Application helper candidate:
- Port candidate:
- Chained Use Case avoided:

## Output Decision

- Output style: APPLICATION_DTO / EXPLICIT_RESULT / PRIMITIVE / VOID
- Why:

### Application DTO

```text

```

### Explicit Result

```text

```

- Serializable:
- Provider types excluded:
- JSX/ReactNode excluded:
- View-library types excluded:
- Locale formatting excluded:

## Failure Semantics

| Failure | Stable Application meaning | Caller needs different behavior |
|---|---|---|
| validation | | |
| not found | | |
| forbidden | | |
| unauthenticated | | |
| conflict | | |
| unavailable | | |
| timeout | | |
| cancelled | | |
| contract mismatch | | |
| unknown | | |

- Raw HTTP/provider errors excluded:
- Domain-error translation:

## Cancellation and Races

- Request can become obsolete:
- Cancellation input/mechanism:
- Cancellation result:
- Port cancellation:
- Latest-wins owner:
- Stale-response prevention owner:
- AbortSignal kept outside Domain:

## Duplicate Commands / Idempotency

- Relevant:
- Policy: ALLOW_CONCURRENT / REJECT_WHILE_PENDING / IDEMPOTENT_BY_KEY / QUEUE / OUTER_LAYER_OWNS
- Application-owned:
- UI-owned:
- Backend support:
- Idempotency key:
- False client-only guarantee avoided:

## Offline / Partial Success

- Offline applicable:
- Local persistence behavior:
- Sync behavior:
- Partial success state:
- Recovery:
- Provider protocol excluded:

## Browser / Routing / Analytics

- Browser capability needed:
- Semantic port:
- Router usage excluded:
- Navigation returned only as semantic data:
- Analytics port:
- Analytics failure policy:

## Composition

- Construction boundary:
- Dependencies provided by:
- Lifecycle:
- Use Case does not access Factory:
- Public package surface:

## Test Matrix

| Scenario | Dependencies | Expected semantic outcome |
|---|---|---|
| success | | |
| semantic failure | | |
| infrastructure failure | | |
| cancellation | | |
| duplicate/idempotent | | |
| partial success | | |

- InMemory repositories:
- External-service stubs/spies:
- React/browser excluded:
- Interaction-only assertions avoided:

## Overmodeling Audit

- Trivial forwarding-only Use Case:
- Endpoint-shaped name:
- Request DTO with no value:
- Result wrapper with no semantic value:
- Chained Use Cases:
- Presentation logic:
- Framework/browser leakage:

## Final Decision

- Decision:
- Conditions:
- Blocking issue:
- Next skill:
- Required follow-up:
