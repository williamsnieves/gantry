# External Service Adapter Implementation Record

## Context

- Change ID:
- Application port:
- Adapter:
- Provider:
- SDK/API version:
- Consuming Use Cases:
- Test environment:
- Resilience policy:
- Credential source:

## Readiness

- Port complete:
- Provider contract confirmed:
- Credentials available:
- Sandbox/emulator available:
- Timeout/retry/idempotency decisions:
- Async/reconciliation decisions:
- Conditions/blockers:

## Contract Mapping

| Port operation | Provider operation | Success meaning | Test |
|---|---|---|---|
| | | | |

## Request Mapping

| Application field | Provider field/header | Transformation | Sensitive |
|---|---|---|---|
| | | | |

## Response Mapping

| Provider condition | Application result | External reference |
|---|---|---|
| | | |

## Failure Translation

| Provider/technical failure | Semantic failure | Retryable | Safe diagnostics |
|---|---|---|---|
| | | | |

## Timeout, Retry, and Rate Limit

- Timeout configuration:
- Ambiguous timeout:
- Retry owner:
- Retryable categories:
- Attempts/backoff:
- Retry-after handling:
- Circuit breaker:
- Metrics:

## Idempotency

- Neutral key:
- Provider mapping:
- Key reuse:
- Duplicate response:
- Reconciliation:
- Persistence/correlation:

## Async and Webhooks

- Provider states:
- Pending result:
- Correlation ID:
- Polling owner:
- Webhook owner:
- Signature verification:
- Duplicate handling:
- Final-state reconciliation:

## Security and Configuration

- Credentials:
- Tenant/account selection:
- Region/endpoint:
- Outbound PII:
- Redaction:
- Secret rotation:
- Startup validation:

## Client Lifecycle

- Shared/transient:
- Construction owner:
- Pool/session:
- Cleanup:
- Tenant-scoped cache:
- Concurrency safety:

## Observability

- Operation metric:
- Provider dimension:
- Latency:
- Retry count:
- Semantic outcome:
- Correlation:
- Safe provider request ID:
- Prohibited logging:

## Test Evidence

| Test | Environment | Result/classification |
|---|---|---|
| | | |

## Residual Uncertainty

- Unavailable provider behavior:
- Sandbox differences:
- Untested failure modes:
- Follow-up evidence:

## Boundary Audit

- SDK types exposed:
- HTTP status exposed:
- Provider enum/error exposed:
- Credentials exposed:
- Generic client abstraction:
- Unapproved fallback:

## Final Status

- Decision:
- Remaining blockers:
- Residual risks:
- Required follow-up:
