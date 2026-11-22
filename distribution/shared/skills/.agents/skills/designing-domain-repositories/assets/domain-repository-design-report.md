# Domain Repository Design Report

## Context

- Change ID:
- Vertical slice:
- Consuming Use Cases:
- Capability/module:
- Entity or aggregate root:
- Applicable policies:
- Existing repository:
- Identifier policy:

## Suitability and Ownership

- Persistence need:
- Repository decision:
- Port owner:
- Aggregate boundary:
- Explicitly excluded responsibilities:
- Cross-module considerations:

## Use Case Traceability

| Use Case behavior | Persistence need | Repository operation |
|---|---|---|
| | | |

## Repository Contract

### Repository Name

-

### Operations

| Operation | Inputs | Output | Absence/failure semantics | Consumer |
|---|---|---|---|---|
| | | | | |

## Aggregate and Consistency

- Root:
- Owned children:
- Save unit:
- Atomicity:
- Transaction owner:
- Concurrency/versioning:
- Idempotency/uniqueness:

## Query Semantics

- Criteria types:
- Ordering:
- Tie-breakers:
- Pagination:
- Empty result:
- Duplicate behavior:
- Read-model separation:

## Error Semantics

| Meaning | Inner error/result | Adapter translation obligation |
|---|---|---|
| | | |

## InMemory Design

- Seed format:
- Internal storage:
- Identity key:
- Save/replace behavior:
- Query behavior:
- Ordering:
- Isolation/defensive copies:
- Controlled failure support:

## Test Plan

| Test | InMemory | Real adapter contract |
|---|---|---|
| | | |

## Boundary Review

- Domain/Application imports:
- ORM/database leakage:
- DTO/provider leakage:
- Generic CRUD/query leakage:
- Module ownership:

## Adapter Handoff

- Mapping requirements:
- Real constraints:
- Transaction/concurrency:
- Error translation:
- Migration/schema:
- Required environment:

## Follow-up Skills

1.
2.

## Readiness

- Decision:
- Conditions:
- Open decisions:
- Risks:
- Recommended next action:
