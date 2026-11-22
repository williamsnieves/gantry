# Software System Orchestration Plan

## Document Control

- Product/system:
- Initiative/change:
- Orchestration version:
- Status:
- Greenfield / brownfield:
- Decision horizon:
- Owner:
- Date:
- Applicable `AGENTS.md`:

## Scope

- Business/system goal:
- Included:
- Excluded:
- Actors:
- External systems/providers:
- Team/ownership context:
- Known constraints:
- Known risks:

## System Profile

- Profile: SMALL_INTERNAL_CRUD / STANDARD_SAAS / MULTI_TENANT_SAAS / PROVIDER_HEAVY / EVENT_DRIVEN / PAYMENT_CRITICAL / BROWNFIELD_MODERNIZATION / CRITICAL_REGULATED / CUSTOM
- Risk level:
- Complexity level:
- Security/privacy significance:
- Lifecycle complexity:
- Eventing complexity:
- Deployment/recovery complexity:
- Rationale:

## Existing Artifact Inventory

| Artifact | Status | Freshness | Authority | Reuse? | Action |
|---|---|---|---|---|---|
| PRD | CURRENT / STALE / CONFLICTED / INCOMPLETE / MISSING / NOT_APPLICABLE | | | yes/no | |
| FR catalog | | | | | |
| NFR catalog | | | | | |
| Quality scenarios | | | | | |
| Architecture drivers | | | | | |
| ADRs | | | | | |
| C4 | | | | | |
| Sequence model | | | | | |
| State model | | | | | |
| DFD | | | | | |
| Domain data | | | | | |
| Event flow | | | | | |
| Deployment | | | | | |
| STRIDE | | | | | |
| Validation report | | | | | |

## Selected Skill Graph

| Node | Skill | Activation | Why | Depends on | Expected artifact | Status |
|---|---|---|---|---|---|---|
| 1 | eliciting-software-requirements | REQUIRED / CONDITIONAL / OPTIONAL / SKIP / BLOCKED / ALREADY_SATISFIED | | | | NOT_STARTED / READY / RUNNING / BLOCKED / COMPLETE / SKIPPED / SUPERSEDED |
| 2 | creating-product-requirement-documents | | | | | |
| 3 | defining-functional-requirements | | | | | |
| 4 | defining-non-functional-requirements | | | | | |
| 5 | defining-quality-attributes | | | | | |
| 6 | identifying-architecture-drivers | | | | | |
| 7 | modeling-use-cases | | | | | |
| 8 | modeling-process-flows | | | | | |
| 9 | modeling-state-machines | | | | | |
| 10 | designing-system-architecture | | | | | |
| 11 | analyzing-architecture-tradeoffs | | | | | |
| 12 | recording-architecture-decisions | | | | | |
| 13 | modeling-c4-architecture | | | | | |
| 14 | modeling-system-sequences | | | | | |
| 15 | modeling-data-flows | | | | | |
| 16 | modeling-domain-data | | | | | |
| 17 | modeling-event-flows | | | | | |
| 18 | modeling-deployment-architecture | | | | | |
| 19 | threat-modeling-with-stride | | | | | |
| 20 | validating-architecture-design | | | | | |

## DAG

```text
[Render the selected skill dependency graph only.]
```

## Parallelization Plan

| Branch | Can run in parallel? | Shared prerequisite | Join gate |
|---|---|---|---|
| | yes/no | | |

## Requirements Foundation Gate

- Goals/non-goals sufficient:
- Actors/capabilities sufficient:
- FRs sufficient:
- NFRs sufficient:
- Quality scenarios sufficient:
- Constraints/assumptions explicit:
- Architecture drivers ready:
- Result:

## Behavioral Modeling Selection

| Model | Needed? | Trigger/question | Skip rationale if not needed |
|---|---|---|---|
| Use cases | | | |
| Process flows | | | |
| State machines | | | |

## Architecture Decision Gate

- Candidate architecture design ready:
- Trade-off analysis required:
- Decision authority identified:
- ADRs required:
- Blocking decision gaps:

## Architecture Model Selection

| Model | Needed? | Material question answered | Prerequisite | Handoff |
|---|---|---|---|---|
| C4 | | | | |
| Sequence | | | | |
| DFD | | | | |
| Domain Data | | | | |
| Event Flow | | | | |
| Deployment | | | | |

## Security Gate

- STRIDE required:
- Trigger:
- DFD available:
- Critical sequences available:
- Deployment/trust context available:
- Security control handoff expected:

## Validation Gate

- Architecture package ready for validation:
- Validation profile:
- Known blockers:
- Conditional items:
- Revalidation loop:

## Backtracking Rules

| Downstream finding | Route back to | Required resolution |
|---|---|---|
| vague scale/recovery measure | NFR / Quality Attributes | |
| missing lifecycle behavior | FR / State Machine | |
| unresolved provider data policy | requirements/security/privacy decision | |
| impossible deployment | architecture trade-off / ADR | |
| conflicting model | owning model / ADR | |

## Over/Under-Modeling Audit

- Selected node with no material question (`OVER_MODELING`):
- Material risk with no model (`UNDER_MODELING`):
- Ritual architecture detected:
- Premature technology decision:
- Unnecessary L3/L4/deployment detail:

## Architecture Package Manifest

| Artifact | Required/conditional | Status | Version | Authority | Path/reference |
|---|---|---|---|---|---|
| | | | | | |

## Accepted Architecture Summary

- System purpose:
- Primary drivers:
- Accepted architecture decisions:
- Key logical boundaries:
- Critical runtime flows:
- Data/tenant invariants:
- Security/trust boundaries:
- Deployment assumptions:
- Accepted trade-offs:

## Decision / Evidence Ledger

### Blocking Decisions
-

### Non-Blocking Deferred Decisions
-

### Implementation-Level TBDs
-

### Evidence / Measurement Gaps
-

## OpenSpec / Implementation Handoff

### Accepted Behavior
-

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

### Domain / Tenant Invariants
-

### Deployment Assumptions
-

### Deferred Decisions / Conditions
-

### OpenSpec Readiness
- READY / READY_WITH_CONDITIONS / NOT_READY

## Orchestration Findings

| ID | Type | Finding | Impact | Next action | Blocking |
|---|---|---|---|---|---|
| | MISSING_INPUT / MISSING_DECISION / STALE_ARTIFACT / CONFLICTED_ARTIFACT / UNDER_MODELING / OVER_MODELING / RITUAL_ARCHITECTURE / PREMATURE_TECHNOLOGY_DECISION / SECURITY_MODEL_REQUIRED / VALIDATION_BLOCKER | | | | yes/no |

## Final Orchestration Status

- Orchestration: ORCHESTRATION_PLAN_READY / ORCHESTRATION_PLAN_READY_WITH_CONDITIONS / ORCHESTRATION_REQUIRES_REQUIREMENTS / ORCHESTRATION_REQUIRES_DECISIONS / ORCHESTRATION_REQUIRES_SECURITY_MODEL / ORCHESTRATION_REQUIRES_ARTIFACT_RECONCILIATION / BLOCKED
- Architecture Package: ARCHITECTURE_PACKAGE_ACCEPTED / ARCHITECTURE_PACKAGE_ACCEPTED_WITH_CONDITIONS / ARCHITECTURE_PACKAGE_REQUIRES_REWORK / ARCHITECTURE_PACKAGE_REQUIRES_DECISIONS / ARCHITECTURE_PACKAGE_SECURITY_BLOCKED / ARCHITECTURE_PACKAGE_CONFLICTED / BLOCKED
- Ready for OpenSpec / implementation planning:
