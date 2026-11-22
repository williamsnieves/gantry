# Backend Architecture Review Report

## Context

- Change/PR/design:
- Accepted behavior:
- Repository/service:
- Review scope:
- Current architecture:
- Proposed architecture:
- Governing standard:
- Local rules/decisions:
- Architecture validation report:
- Code review report:
- Reviewer/date:

## Architecture Decision Inventory

| Decision | Introduced/modified | Reason | Evidence |
|---|---|---|---|
| | | | |

## Current and Target Maps

### Current

```text

```

### Target

```text

```

### Migration Path

```text
current
→ seam
→ target
→ cleanup
```

## Ownership

- Owning capability:
- Cross-module contracts:
- Shared code justification:
- Ambiguous ownership:
- Findings:

## Domain Model

- Invariants:
- Entity/Value Object boundaries:
- Domain Services:
- Aggregate scope:
- Over-design:
- Under-design:
- Findings:

## Application Flow

- Use Case intention:
- DTOs:
- Authorization/tenancy:
- Side-effect ordering:
- Use Case chaining:
- Workflow ownership:
- Findings:

## Ports and Adapters

| Port/adapter | Owner | Boundary justified | Neutral contract | Lifecycle | Findings |
|---|---|---|---|---|---|
| | | | | | |

## Composition

- Concrete selection:
- Shared/transient lifecycle:
- Configuration:
- Startup/shutdown:
- Test reset:
- Service Locator/runtime DI:
- Findings:

## Transactions and Idempotency

- Transaction owner:
- Atomic boundary:
- Remote calls:
- Partial failure:
- Compensation/reconciliation:
- Idempotency key flow:
- Authoritative duplicate protection:
- Findings:

## Events and Async

- Event/async need:
- Ownership:
- Delivery semantics:
- Consumer idempotency:
- Ordering:
- Versioning:
- Outbox/inbox:
- Findings:

## Migration and Compatibility

- Public contract:
- Persisted data:
- Mixed-version deployment:
- Backfill:
- Dual-read/write:
- Feature flag/routing:
- Rollback:
- Exit criteria:
- Temporary deviations:
- Findings:

## Proportionality and Complexity

- Abstractions justified:
- Generic abstractions:
- Indirection:
- Duplicate paths:
- Long-lived seams:
- Testability:
- Evolution cost:
- Findings:

## Operability

- Configuration/readiness:
- Timeout/retry:
- Observability:
- Reconciliation:
- Cleanup:
- Resource lifecycle:
- Incident diagnosis:
- Findings:

## Testing Architecture

- Domain:
- Application:
- Repository:
- External provider:
- HTTP E2E:
- Architecture checks:
- Excessive mocks/E2E dependence:
- Findings:

## Drift Assessment

| Item | Classification | Scope | Accepted/owner/exit |
|---|---|---|---|
| | NEW_DRIFT/WORSENED_DRIFT/PRE_EXISTING/FIXED/ACCEPTED_TEMPORARY | | |

## Findings

### BE-ARCH-REV-001 — <title>

- Severity:
- Category:
- Confidence:
- Status:
- Basis:
- Evidence:
- Architectural consequence:
- Failure/evolution scenario:
- Recommendation:
- Alternatives considered:
- Validation/decision required:

## Decisions Required

| Question | Options/tradeoffs | Owner | Blocking |
|---|---|---|---|
| | | | |

## Positive Architectural Evidence

- 

## Summary

- Critical:
- High:
- Medium:
- Low:
- New/worsened drift:
- Accepted temporary deviations:
- Missing evidence:

## Final Decision

- Decision:
- Blocking findings:
- Conditions:
- Required decisions:
- Residual risk:
- Recommended next skill:
