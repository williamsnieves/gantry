# Application Use Case Design Report

## Context

- Change ID:
- Vertical slice:
- Application capability:
- Existing service/Use Case:
- Applicable standards/policies:
- Error/result convention:
- Transaction policy:
- Authorization policy:

## Suitability and Intention

- User/system intention:
- Why Application orchestration is required:
- Why behavior does not belong entirely to Domain:
- Use Case decision:
- Explicitly excluded intentions:

## Use Case Boundary

- Use Case name:
- `execute` signature:
- Request DTO:
- Response DTO or `void`:
- Sync/async:
- Stability considerations:

## Input Conversion

| Request field | Primitive/plain type | Domain type | Validation/failure |
|---|---|---|---|
| | | | |

## Dependencies

| Dependency | Port owner | Intention | Why required |
|---|---|---|---|
| | | | |

## Orchestration

1.
2.
3.

### Domain Delegation

- Entity operations:
- Value Object construction/operations:
- Domain Services:
- Rules explicitly not implemented in Application:

## Authorization

- Authenticated actor input:
- Operation-level decision:
- Ownership/tenant checks:
- Failure meaning:

## Transaction and Consistency

- Atomic boundary:
- Participating repositories:
- External side effects:
- Commit/event strategy:
- Rollback/recovery:
- Concurrency/versioning:

## Idempotency and Retry

- Repetition risk:
- Idempotency key/source:
- Authoritative protection:
- Duplicate result:
- Provider support:
- Retry owner:

## Error Semantics

| Condition | Domain/Application meaning | Transport mapping owner |
|---|---|---|
| | | |

## Output Mapping

| Domain source | Response field | Transformation |
|---|---|---|
| | | |

## Test Plan

| Test | Collaborators/setup | Expected behavior |
|---|---|---|
| | | |

## Boundary Review

- Concrete adapters:
- HTTP/framework types:
- ORM/database types:
- Provider SDK types:
- Use Case chaining:
- Environment/time/randomness:
- Entity leakage:

## Follow-up Skills

1.
2.

## Readiness

- Decision:
- Conditions:
- Open decisions:
- Risks:
- Recommended next action:
