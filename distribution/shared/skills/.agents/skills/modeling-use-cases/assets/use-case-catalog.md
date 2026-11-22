# Use Case Catalog

## Document Control

- Product/system:
- Initiative:
- Catalog version:
- Status:
- Source PRD:
- Source FR catalog:
- Owner:
- Date:
- Applicable `AGENTS.md`:

## System Boundary

- System being modeled:
- Inside boundary:
- Outside boundary:
- Explicit exclusions:
- Brownfield boundary notes:

## Actor Catalog

### ACT-001 — [Actor]

- Type: human / external system / external trigger
- Goal/interests:
- Capabilities:
- Scope:
- Source:
- Notes:

## Actor Generalization

| Parent actor | Specialized actor | Shared capability rationale |
|---|---|---|
| | | |

## Use Cases

### UC-001 — [Title]

- Status: PROPOSED / REVIEW_REQUIRED / ACCEPTED / DEFERRED / REJECTED / SUPERSEDED
- Primary actor:
- Supporting actors:
- Goal:
- Scope:
- Stakeholders/interests:
- Preconditions:
- Trigger:

### Main Success Flow

1.
2.
3.

### Alternative Flows

#### A1 — [Alternative]

- Condition:
1.
2.
- Return/Outcome:

### Failure Flows

#### F1 — [Failure]

- Condition:
1.
2.
- Failure outcome:
- Postcondition:

### Postconditions

- Success:
- Minimal guarantee:
- Failure:

### Business Rules

- BR-:

### Relevant NFR References

- NFR:
- QA:

### Traceability

- FRs:
- PRD goal(s):
- Journey(s):
- PRD AC(s):
- Source(s):

### Open Questions

- 

## Business Rules

### BR-001 — [Rule]

- Rule:
- Source:
- Applies to use cases:
- Status:

## Actor → Use Case Capability Matrix

| Actor | Use Case | Allowed | Scope / Rule |
|---|---|---|---|
| | | yes/no/conditional | |

## Privilege Boundary Matrix

| Capability | Actor/role | Resource scope | Rule source | Notes |
|---|---|---|---|---|
| | | | | |

## External Actor Participation

| External actor | Use Case | Trigger/participation | Contract detail deferred to |
|---|---|---|---|
| | | | modeling-system-sequences / integration design |

## Include Relationships

| Base use case | Included use case | Why mandatory/reusable |
|---|---|---|
| | | |

## Extend Relationships

| Base use case | Extending use case | Extension condition | Why separate use case |
|---|---|---|---|
| | | | |

## Use Case Diagram Decision

- Diagram useful: yes/no
- Reason:
- Diagram split/domain:
- Preferred syntax:
- Diagram file/source:

## Functional Requirement Coverage

| FR | Use Case(s) | Status |
|---|---|---|
| | | COVERED / PARTIALLY_COVERED / NO_USE_CASE_NEEDED / MISSING_USE_CASE / BLOCKED_BY_REQUIREMENT_DECISION |

## Goal / Journey Coverage

| Goal / Journey | Use Cases | Status |
|---|---|---|
| | | |

## Alternative / Failure Coverage Audit

| Use Case | Permission | Invalid state | Dependency failure | Conflict | Cancel/retry | Gaps |
|---|---|---|---|---|---|---|
| | | | | | | |

## Modeling Handoffs

### Process Flow Candidates

| Use Case | Why process-flow modeling helps |
|---|---|
| | |

### State Machine Candidates

| Use Case | Entity/process lifecycle implied |
|---|---|
| | |

### Sequence Diagram Candidates

| Use Case | Participants/integration complexity |
|---|---|
| | |

## Leakage Audit

- UI implementation detail removed:
- API detail removed:
- Architecture detail removed:
- Sequence/component detail removed:
- Internal-system actors removed/corrected:

## Open Questions / Decisions

| ID | Use Case | Issue | Type | Owner |
|---|---|---|---|---|
| | | | PRODUCT_DECISION_REQUIRED / REQUIREMENT_CLARIFICATION_REQUIRED / ACTOR_SCOPE_REQUIRED / BUSINESS_RULE_REQUIRED / FAILURE_BEHAVIOR_REQUIRED | |

## Final Decision

- Decision: USE_CASE_MODEL_READY / USE_CASE_MODEL_READY_WITH_OPEN_QUESTIONS / USE_CASE_MODEL_REQUIRES_REQUIREMENT_CLARIFICATION / USE_CASE_MODEL_REQUIRES_PRODUCT_DECISION / USE_CASE_MODEL_REQUIRES_ACTOR_SCOPE / USE_CASE_MODEL_CONFLICTED / BLOCKED
- Blocking questions:
- Missing use cases:
- Privilege gaps:
- Ready for `modeling-process-flows`:
- Ready for `modeling-state-machines`:
