# Backend Brownfield Adaptation Record

## Context

- Change ID:
- Selected behavior:
- Capability/module:
- Repository/service:
- Governing standard:
- Repository-local rules:
- Architecture validation input:
- Delivery window/constraints:

## Readiness

- Current behavior understood:
- Public contract resolved:
- Data compatibility resolved:
- Transaction/side-effect order resolved:
- Security/tenant boundary resolved:
- Characterization capability:
- Initial decision:
- Conditions/blockers:

## Current-State Map

```text
entry point
→ current orchestration
→ business decisions
→ persistence
→ external effects
→ response/event
```

### Components

| Component/path | Actual classification | Responsibilities | Dependencies | Evidence |
|---|---|---|---|---|
| | DOMAIN-LIKE/APPLICATION-LIKE/INFRASTRUCTURE/DELIVERY/MIXED/UNKNOWN | | | |

### Current Runtime Behavior

- Trigger:
- Decisions:
- State changes:
- External effects:
- Error semantics:
- Transaction owner:
- Configuration/construction:
- Tests:
- Operational risks:

## Target-State Map

```text
delivery
→ Application Use Case
→ Domain
→ ports
→ adapters
→ composition
```

- Target behavior boundary:
- Required Domain:
- Required Application:
- Repository ports/adapters:
- External ports/adapters:
- Delivery:
- Composition:
- Compatibility layer:
- Explicitly out of scope:

## Change-Local Rules

| Rule | Classification | Rationale | Evidence/decision |
|---|---|---|---|
| | MANDATORY_NOW/DEFAULT_NOW/DEFERRED_WITH_REASON/ACCEPTED_TEMPORARY_DEVIATION/NOT_APPLICABLE | | |

## Scope Decisions

| Item | Classification | Decision |
|---|---|---|
| | REQUIRED_FOR_CURRENT_BEHAVIOR/REQUIRED_COMPATIBILITY/SAFE_LOCAL_IMPROVEMENT/DEFERRED_DEBT/UNRELATED/BLOCKING_RISK | |

## Characterization Plan

| Behavior/contract | Evidence source | Test/check | Status |
|---|---|---|---|
| | | | |

- Accidental behavior intentionally preserved:
- Known bug intentionally corrected:
- Missing characterization:
- Production-safe evidence:

## Migration Seams

| Seam | Current side | Target side | Type | Owner | Removal/long-term role |
|---|---|---|---|---|---|
| | | | facade/port/adapter/mapper/route/event/transaction | | |

## Incremental Adoption Plan

1.
2.
3.

- Strategy: wrap/extract/strangle/parallel-run/backfill-switch/other
- One authoritative writer:
- Routing:
- Rollback:
- Observability:
- Exit criteria:

## Compatibility

### Public Contract

- Route/API/event:
- Request:
- Response:
- Errors:
- Headers/idempotency:
- Versioning:

### Persisted Data

- Current shape:
- Target shape:
- Unknown/invalid data:
- Backfill:
- Dual-read/write:
- Verification:
- Cleanup:

### Errors

| Legacy error | Target semantic error | Compatibility translation |
|---|---|---|
| | | |

## Transaction and Side Effects

### Current

1.
2.
3.

- Failure after each step:
- Duplicate risk:
- Recovery:

### Target

1.
2.
3.

- Owner:
- Atomic boundary:
- Reconciliation:
- Decision reference:

## Temporary Deviations

| ID | Rule | Scope | Rationale/risk | Owner | Removal condition | Status |
|---|---|---|---|---|---|---|
| | | | | | | |

## Debt Ledger

| ID | Current state | Target state | Impact/risk | Trigger | Owner | Next skill/slice | Status |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

## Validation Evidence

| Check | Command/evidence | Result/classification |
|---|---|---|
| Characterization | | |
| New behavior | | |
| Adapter boundary | | |
| HTTP/public contract | | |
| Migration/backfill | | |
| Architecture before/after | | |
| Rollback/recovery | | |

## Drift Comparison

- Pre-existing:
- New:
- Worsened:
- Fixed:
- Accepted temporary:

## Security and Operations

- Tenant isolation:
- Credentials:
- PII/data copying:
- Authorization:
- Error redaction:
- Feature flag:
- Metrics/logs:
- Rollback constraints:

## Final Decision

- Decision:
- Conditions:
- Blocking risk:
- Residual uncertainty:
- Next safe slice:
- Required follow-up:
