# Application Use Case Testing Record

## Context

- Change ID:
- Vertical slice:
- Application capability:
- Use Case:
- Request DTO:
- Response DTO or `void`:
- Test framework:
- Focused command:
- Applicable policies:

## Behavior Inventory

| Behavior | Type | Status |
|---|---|---|
| | success/input/missing/authorization/rejection/conflict/external/persistence/output/regression | |

## Collaborators

### Real Domain

- Entities:
- Value Objects:
- Domain Services:
- Domain errors/results:

### InMemory Repositories

| Port | InMemory implementation | Seed | Observable queries |
|---|---|---|---|
| | | | |

### External-Port Doubles

| Port | Double type | Configured outcome | Recorded calls |
|---|---|---|---|
| | stub/spy/fake | | |

### Deterministic Utilities

- Clock:
- ID generator:
- Idempotency key:
- Other:

## Input and Domain Conversion

| Request field | Domain type | Valid case | Invalid case |
|---|---|---|---|
| | | | |

## Success Behavior

- Response:
- Persisted state:
- External call:
- Ordering semantics:
- DTO mapping:
- Internal fields excluded:

## Failure Behavior

| Case | Semantic outcome | State after | Calls prevented |
|---|---|---|---|
| | | | |

## Idempotency and Concurrency

- Repeated request:
- Same key propagation:
- Duplicate semantic:
- State duplication:
- Authoritative real-boundary limitation:

## Transactions and Partial Failure

- Transaction port:
- Commit/rollback:
- Provider success + persistence failure:
- Recovery semantics:
- Real atomicity tested elsewhere:

## Assertion Strategy

- State assertions:
- Result assertions:
- Meaningful interaction assertions:
- Incidental interactions avoided:
- Private/technical assertions:

## Boundary Audit

- Repository mocks:
- Domain mocks:
- Concrete adapters:
- ORM/database:
- Provider SDK:
- HTTP/framework:
- Composition:
- Environment reads:

## Commands and Evidence

| Command | Scope | Result/classification |
|---|---|---|
| | | |

## Gaps and Follow-up

- Missing accepted cases:
- Harness issues:
- Port/Use Case design issues:
- Real-boundary follow-up:
- Regression risks:

## Final Status

- Decision:
- Conditions:
- Known failures:
- Residual risks:
- Required follow-up:
