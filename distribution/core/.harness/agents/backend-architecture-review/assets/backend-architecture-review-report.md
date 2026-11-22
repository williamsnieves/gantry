# Backend Architecture Review Report

## Gate Decision

- Decision: ARCHITECTURE_APPROVED / ARCHITECTURE_APPROVED_WITH_CONDITIONS / ARCHITECTURE_CHANGES_REQUIRED / BLOCKED_PENDING_ARCHITECTURE_DECISION / BLOCKED_PENDING_PRODUCT_DECISION / BLOCKED_PENDING_EVIDENCE
- Review version:
- Reviewer:
- Date:
- Target change / PR:
- Backend scope:
- Re-review required: yes/no

## Authoritative Basis

- Applicable `AGENTS.md`:
- Accepted requirement / OpenSpec:
- Backend engineering standard:
- Backend decision register / accepted exceptions:
- ADR(s) / architecture validation:
- Known unresolved architecture/product decisions:

## Review Scope

### Introduced by Change
-

### Modified by Change
-

### Directly Depended On
-

### Pre-Existing Adjacent
-

### Explicitly Excluded
-

## Current → Proposed Architecture Map

### Current
```text
...
```

### Proposed
```text
...
```

### Material Changes
-

## Architecture Decision Inventory

| ID | Decision | Owner/boundary | Behavior/driver | Alternatives/evidence | Reversibility | Status |
|---|---|---|---|---|---|---|
| ADI-001 | | | | | | |

## Ownership Matrix

| Responsibility | Current owner | Proposed owner | Layer/module | Authority clear? | Finding |
|---|---|---|---|---|---|
| | | | | | |

## Boundary / Abstraction Review

| Boundary / abstraction | Concrete need | Protected inward policy | Consumers | Proportional? | Result |
|---|---|---|---|---|---|
| | | | | | |

## Transaction / Idempotency / Side Effects

- Transaction owner:
- Remote side effects:
- Partial-failure semantics:
- Retry owner:
- Compensation/reconciliation:
- Idempotency owner:
- Durable replay behavior:
- Blocking gaps:

## Event / Async Architecture

- Applicable: yes/no
- Event owner:
- Delivery/order semantics:
- Consumer idempotency:
- Versioning:
- Replay:
- Observability:
- Unresolved decisions:

## Migration / Compatibility / Reversibility

### Current → Seam → Target
```text
...
```

- One authoritative path:
- Dual-write/dual-read:
- Backfill:
- Mixed-version compatibility:
- Rollback:
- Data irreversibility:
- External side effects:
- Reconciliation:
- Exit/removal condition:
- Debt owner:
- Result:

## Drift / Temporary Deviations

| Area | Classification | Accepted? | Scope | Exit/removal condition | Finding |
|---|---|---|---|---|---|
| | NEW_DRIFT / WORSENED_DRIFT / PRE_EXISTING / FIXED / ACCEPTED_TEMPORARY | | | | |

## Testability / Operability

### Testability
- Domain/Application isolation:
- Excessive mocking required:
- Adapter contract evidence:
- Architecture validation support:

### Operability
- Configuration/lifecycle:
- Readiness/shutdown:
- Timeouts/retries:
- Correlation/tracing:
- Reconciliation/cleanup:
- Incident diagnosis:

## Architecture Findings

### BAR-001 — [Title]

- Severity: CRITICAL / HIGH / MEDIUM / LOW
- Category: OWNERSHIP / BOUNDARY / ABSTRACTION / DOMAIN_MODEL / APPLICATION_FLOW / PORT_ADAPTER / COMPOSITION / TRANSACTION / IDEMPOTENCY / EVENTING / MIGRATION / COMPATIBILITY / OPERABILITY / TESTABILITY / ARCHITECTURAL_DRIFT
- Confidence: HIGH / MEDIUM / LOW
- Status:
- Decision / standard basis:
- Evidence:
- Architectural consequence:
- Failure / evolution scenario:
- Recommendation:
- Alternatives considered:
- Validation / decision required:
- Related Backend Code Review finding:
- Blocking: yes/no
- Handoff / owner:

## Decision Questions

### DQ-001 — [Question]

- Why a decision is required:
- Option A:
- Option B:
- Other viable options:
- Trade-offs:
- Work blocked:
- Recommended decision owner:
- Blocking: yes/no

## Validation / Review Evidence

| Evidence | Status | Source | Architectural implication |
|---|---|---|---|
| Validator | PASSED / FAILED / BLOCKED / UNAVAILABLE / INCONCLUSIVE | | |
| Backend Code Review | | | |
| Architecture tests | | | |
| Migration/schema evidence | | | |
| Runtime/operability evidence | | | |

## Residual Architecture Risk

- Accepted trade-offs:
- Pre-existing debt not worsened:
- Conditional architecture risks:
- Evidence gaps:
- Future decision triggers:

## Handoffs

| Finding/question | Recipient | Expected output | Blocking | Re-entry condition |
|---|---|---|---|---|
| | Implementation / Backend Code Review / Validator / QA / Security / Performance / Detail Analyst / Product / Architecture Owner / Reviewer | | yes/no | |

## Architecture Review Summary

- Critical findings:
- High findings:
- Medium findings:
- Low findings:
- Blocking architecture decisions:
- Blocking product decisions:
- Blocking evidence gaps:
- Conditions:
- Why final decision is justified:

## Exact Next Action

-
