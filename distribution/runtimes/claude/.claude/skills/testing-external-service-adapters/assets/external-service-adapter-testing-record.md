# External Service Adapter Testing Record

## Context

- Change ID:
- Application port:
- Concrete adapter:
- Provider:
- API version:
- SDK version:
- Consuming capability:
- Test framework:
- Focused command:

## Readiness

- Provider contract confirmed:
- Failure taxonomy confirmed:
- Retry/timeout/idempotency policy confirmed:
- Async/reconciliation policy confirmed:
- Safe test capability:
- Conditions/blockers:

## Evidence Strategy

| Level | Capability | Selected | Limitations |
|---|---|---|---|
| Pure mapping | | | |
| Protocol/contract | | | |
| Official emulator/test mode | | | |
| Real sandbox | | | |

## Credentials and Environment

- Secret source:
- Sandbox/test scope:
- Least privilege:
- Tenant/account:
- Region/endpoint:
- Untrusted PR policy:
- Rotation:
- Production guard:
- Cost/rate-limit guard:

## Request Mapping

| Application field | Provider field/header | Transformation | Evidence |
|---|---|---|---|
| | | | |

## Response Mapping

| Provider state | Application result | External reference | Evidence |
|---|---|---|---|
| | | | |

## Failure Translation

| Provider/technical condition | Semantic failure | Retryable | Evidence |
|---|---|---|---|
| | | | |

## Retry, Timeout, and Rate Limits

- Timeout:
- Ambiguous completion:
- Retryable cases:
- Permanent cases:
- Attempts/backoff:
- Retry-after:
- Same idempotency key:
- Exhaustion:
- No real sleeps:

## Idempotency and Reconciliation

- Key source:
- Provider mapping:
- Duplicate result:
- Key reuse:
- Status/reconciliation query:
- External reference:
- Repeated request behavior:

## Async Behavior

- Initial pending/queued result:
- Correlation:
- Polling:
- Webhook/event utility:
- Signature/replay:
- Final state:
- Duplicate event:
- Eventual-consistency deadline:

## Security and Observability

- Outbound PII:
- Sensitive fixtures:
- Log redaction:
- Error redaction:
- Metrics/traces:
- Safe provider request ID:
- Secret-leak test:

## Client Lifecycle

- Construction:
- Sharing:
- Tenant-scoped cache:
- Cleanup:
- Partial construction failure:
- Composition-owned concerns:

## Sandbox/Test Data

- Resource prefix/run ID:
- Synthetic data:
- Cleanup/expiry:
- Destructive restrictions:
- Cost:
- Rate limits:
- Residual resources:

## Commands and Evidence

| Command | Evidence level | Result | Classification |
|---|---|---|---|
| | | | |

## Failure Classification

- Product failures:
- Provider contract failures:
- Sandbox/provider outages:
- Credentials/network/rate-limit blocks:
- Cleanup failures:
- Flakiness:

## Residual Uncertainty

- Provider behavior not covered:
- Sandbox versus production differences:
- Unsupported emulator behavior:
- Missing credentials/capability:
- Required future command/evidence:

## Boundary Audit

- SDK types exposed inward:
- HTTP status exposed inward:
- Provider enum/error exposed inward:
- Credentials exposed:
- Vendor headers exposed:
- Mock-only proof mislabeled:

## Final Status

- Decision:
- Conditions:
- Known failures:
- Residual risks:
- Required follow-up:
