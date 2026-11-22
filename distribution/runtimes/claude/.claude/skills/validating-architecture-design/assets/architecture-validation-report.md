# Architecture Validation Report

## Document Control

- Product/system:
- Architecture version:
- Validation version:
- Validation profile: LIGHTWEIGHT / STANDARD / CRITICAL_COMPLEX
- Target environment:
- Validation owner:
- Date:
- Applicable `AGENTS.md`:

## Validation Scope

- Included architecture:
- Excluded:
- Decision horizon:
- Current / target / transition:
- Acceptance authority:
- Known limitations:

## Architecture Package Inventory

| Artifact | Requirement | Version/status | Authority | Result | Notes |
|---|---|---|---|---|---|
| Architecture drivers | REQUIRED | | | PASS / MISSING / NOT_APPLICABLE | |
| NFR / Quality scenarios | | | | | |
| Trade-off analysis | | | | | |
| ADRs | | | | | |
| C4 | | | | | |
| Sequence model | | | | | |
| State model | | | | | |
| DFD | | | | | |
| Domain data model | | | | | |
| Event flow | | | | | |
| Deployment model | | | | | |
| STRIDE threat model | | | | | |

## Driver → Decision → Evidence Matrix

| Driver | Decision / ADR | Model evidence | Validation evidence | Result |
|---|---|---|---|---|
| | | | | DRIVER_ADDRESSED / DRIVER_PARTIALLY_ADDRESSED / DRIVER_UNADDRESSED / DRIVER_EVIDENCE_INSUFFICIENT |

## Quality Attribute Validation

| QA / NFR | Required measure | Architectural support | Evidence | Result |
|---|---|---|---|---|
| | | | | PASS / PASS_WITH_CONDITIONS / FAIL / INSUFFICIENT_EVIDENCE |

## Constraint Compliance

| Constraint | Source/authority | Architecture evidence | Result | Blocking? |
|---|---|---|---|---|
| | | | CONSTRAINT_SATISFIED / CONSTRAINT_VIOLATED / CONSTRAINT_COMPLIANCE_UNKNOWN | |

## Assumption Validation

| Assumption | Still valid? | Evidence | Impact if false | Revisit trigger | Result |
|---|---|---|---|---|---|
| | | | | | |

## Trade-Off / ADR Audit

### Trade-offs
- Benefit-only decisions:
- Missing negative consequences:
- Missing reversal triggers:

### ADR Consistency
- Conflicting accepted ADRs:
- Supersession gaps:
- Scope overlaps:
- Authority/status issues:

## C4 Alignment

- ADR/C4 conflicts:
- Missing accepted containers/components:
- Invented/phantom structure:
- Abstraction mixing:
- Relationship gaps:
- Current/target mismatch:

## Sequence Feasibility

| Sequence | Participants feasible? | Auth feasible? | Data/store path feasible? | State/order valid? | Failure coverage | Result |
|---|---|---|---|---|---|---|
| | | | | | | PASS / PASS_WITH_CONDITIONS / FAIL |

## State Model Consistency

- Use-case/state conflicts:
- Sequence/state conflicts:
- Data/state conflicts:
- Illegal transitions used:
- Reachability issues:
- Terminal-state contradictions:

## Domain Data Consistency

- Ownership ambiguity:
- Multiple authoritative writers:
- Cardinality conflicts:
- Identifier conflicts:
- Tenant-scope conflicts:
- Lifecycle conflicts:
- DFD/C4 ownership mismatch:

## DFD / Privacy / Trust Alignment

- Missing sensitive flows:
- Missing trust boundaries:
- Third-party mismatch:
- Residency conflict:
- Retention/privacy unresolved:
- Logging/observability data conflict:
- Secret-flow mismatch:

## Event Flow Consistency

- Unmodeled producer/consumer:
- State/domain mismatch:
- Delivery/order/retry gaps:
- Versioning/ownership gaps:
- Deployment transport mismatch:
- Duplicate/idempotency gaps:

## Deployment Feasibility

- Unplaced C4 containers:
- Phantom infrastructure:
- Connectivity gaps:
- Trust/network mismatch:
- Data placement conflict:
- Messaging placement gap:
- Observability gap:
- Secret distribution gap:
- SPOFs/blast radius:
- RTO/RPO/failover gaps:
- Unsupported HA/recovery claims:

## Security Threat Treatment

| Threat ID | STRIDE | Attack path / affected asset | Required mitigation/control | Architecture response | Residual risk | Status |
|---|---|---|---|---|---|---|
| | | | | | | ADDRESSED_BY_DESIGN / CONTROL_REQUIRED_DOWNSTREAM / RISK_ACCEPTED / OPEN / BLOCKING / NOT_APPLICABLE |

## Architecture Claim Inventory

| Claim | Evidence expected | Evidence found | Status |
|---|---|---|---|
| | | | SUPPORTED / PARTIALLY_SUPPORTED / UNSUPPORTED / UNMEASURABLE |

## Cross-Model Identity / Relationship Matrix

| Concept/relationship | ADR | C4 | Sequence | DFD | Domain | Event | Deployment | Result |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

## Findings

### AV-001 — [Finding]

- Severity: CRITICAL / HIGH / MEDIUM / LOW / INFO
- Type: DESIGN_DEFECT / MODEL_CONFLICT / MISSING_DECISION / MISSING_EVIDENCE / UNSUPPORTED_CLAIM / CONSTRAINT_VIOLATION / SECURITY_RISK / TRACEABILITY_GAP / DOCUMENTATION_GAP
- Result: FAIL / PASS_WITH_CONDITIONS / INSUFFICIENT_EVIDENCE
- Evidence:
- Affected driver(s):
- Affected requirement(s):
- Affected artifact(s):
- Architecture impact:
- Recommended next action:
- Blocking: yes/no
- Owner:

## Blocking Ledger

| Finding | Why blocking | Required resolution |
|---|---|---|
| | | |

## Conditional Acceptance Ledger

| Condition | Why non-blocking now | Required before | Owner |
|---|---|---|---|
| | | | |

## Architecture Spikes / Evidence Work

| Claim/gap | Suggested evidence | Why it could change validation |
|---|---|---|
| | | |

## OpenSpec / Implementation Handoff

### Architecture Constraints
-

### ADRs to Respect
-

### Required Security Controls
-

### Quality Scenarios to Verify
-

### Critical Runtime Flows
-

### Data / Tenant Invariants
-

### Deployment Assumptions
-

### Deferred Architecture Decisions
-

## Acceptance Recommendation

- Recommendation: ACCEPT / ACCEPT_WITH_CONDITIONS / REJECT_PENDING_REWORK / BLOCKED_PENDING_DECISION / BLOCKED_PENDING_EVIDENCE
- Rationale:
- Blocking findings:
- Conditions:
- Residual risks:
- Required authority:

## Final Status

- Status: ARCHITECTURE_VALIDATED / ARCHITECTURE_VALIDATED_WITH_CONDITIONS / ARCHITECTURE_REQUIRES_REWORK / ARCHITECTURE_REQUIRES_DECISIONS / ARCHITECTURE_REQUIRES_EVIDENCE / ARCHITECTURE_SECURITY_BLOCKED / ARCHITECTURE_CONFLICTED / BLOCKED
- Ready for OpenSpec / implementation planning:
