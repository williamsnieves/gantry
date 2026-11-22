# External Service Port Design Report

## Context

- Change ID:
- Vertical slice:
- Consuming Use Cases:
- Application capability:
- External capability:
- Existing provider/integration:
- Applicable policies:
- Error/result convention:

## Suitability and Ownership

- Why external collaboration is required:
- Why this is not persistence:
- Port owner:
- Consuming Use Cases:
- Port decision:
- Explicit exclusions:

## Capability Responsibility

- Port name:
- Responsibility statement:
- Provider-neutral vocabulary:
- Split/merge rationale:

## Operations

| Operation | Consumer | Intention | Side effect |
|---|---|---|---|
| | | | |

## Inputs

| Operation | Input type | Fields | Domain/Application ownership |
|---|---|---|---|
| | | | |

## Outputs

| Operation | Output type | Success meaning | Pending/partial semantics |
|---|---|---|---|
| | | | |

## Failure Taxonomy

| Application meaning | Retryable | Use Case reaction | Provider mapping obligation |
|---|---|---|---|
| | | | |

## Resilience

### Timeouts

- Timeout expectation:
- Enforcement layer:
- Ambiguous completion:
- Reconciliation:

### Retries

- Retry owner:
- Retryable categories:
- Attempts/backoff:
- Observability:

### Idempotency

- Key/source:
- Provider support:
- Duplicate semantics:
- Persistence/reconciliation:

### Cancellation/Fallback/Circuit Breaking

- Cancellation:
- Fallback:
- Circuit breaker:
- Semantic impact:

## Asynchronous Behavior

- Synchronous/pending:
- Correlation reference:
- Polling/webhook ownership:
- Completion reconciliation:
- Duplicate event handling:

## Security, Privacy, and Tenancy

- Outbound fields:
- PII/sensitive data:
- Credentials:
- Tenant context:
- Redaction:
- Residency/retention:
- Audit requirements:

## Test Doubles

- Stub scenarios:
- Spy records:
- Fake behavior:
- Deterministic time/IDs:
- Prohibited provider details:

## Use Case Test Plan

| Test | Port setup | Expected Application behavior |
|---|---|---|
| | | |

## Adapter Handoff

- Provider request mapping:
- Provider response mapping:
- Error translation:
- Authentication:
- Timeout/retry:
- Idempotency:
- Rate limiting:
- Logging/metrics/tracing:
- SDK lifecycle:
- Required environment:

## Boundary Audit

- SDK leakage:
- HTTP/framework leakage:
- Provider naming:
- Credential leakage:
- ORM/database leakage:
- Generic API client:
- Unused operations:

## Follow-up Skills

1.
2.

## Readiness

- Decision:
- Conditions:
- Open decisions:
- Risks:
- Recommended next action:
