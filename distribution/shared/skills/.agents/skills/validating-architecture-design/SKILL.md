---
name: validating-architecture-design
description: Portable engineering capability `validating-architecture-design`. Use
  when the harness or a specialist agent explicitly requires this named capability.
---
# Validating Architecture Design

## Purpose

Verify that the proposed architecture actually addresses the accepted drivers, constraints, risks, and required models.

Roadmap validation chain:

```text
drivers → decisions
quality attributes → measurable support
constraints → respected
trade-offs → explicit
ADRs → aligned
C4 → aligned
sequence flows → feasible
state models → consistent
data model → consistent
deployment → feasible
security threats → addressed
```

Output:

```text
architecture-validation-report.md
```

## Core Principle

Architecture validation asks:

```text
Does the architecture actually support what we claim it supports?
```

not:

```text
Are all expected documents present?
```

Artifact presence is necessary evidence only when the artifact is required.

It is not proof of correctness.

# Use When

- Architecture drivers are accepted enough to evaluate.
- Candidate selection/trade-off analysis has occurred.
- ADRs exist for significant decisions.
- Relevant C4, sequence, state, data, event, and deployment models exist.
- STRIDE has been performed for security-relevant architecture where required.
- The Architecture Package needs a final quality gate.
- A brownfield target architecture needs consistency validation before implementation planning.
- Architecture review needs evidence-backed pass/conditional/fail outcomes.

# Do Not Use When

- Requirements are still being elicited.
- Architecture candidates have not been selected.
- The task is to design architecture rather than validate it.
- The task is implementation/code review.
- The task is to verify implemented controls; use `verifying-security-controls`.
- The task is only STRIDE threat discovery; use `threat-modeling-with-stride`.

# Inputs

Preferred:

- architecture drivers record;
- NFR catalog;
- quality-attribute scenarios;
- constraints and assumptions;
- candidate architecture record;
- trade-off analysis;
- ADR set/index;
- use-case catalog;
- process-flow model where relevant;
- state-machine model where relevant;
- C4 architecture model;
- sequence model;
- DFD;
- domain-data model;
- event-flow model where relevant;
- deployment architecture model;
- STRIDE threat model where required;
- risk register;
- applicable `AGENTS.md`.

Optional:

- architecture spikes/benchmarks;
- provider documentation;
- production baseline metrics;
- cost evidence;
- compliance/security policies;
- brownfield current-state model;
- migration plan.

# Outputs

- Architecture Validation Report.
- Architecture-package inventory.
- Driver-to-decision validation matrix.
- Quality-attribute support matrix.
- Constraint-compliance matrix.
- ADR consistency audit.
- Cross-model consistency audit.
- Sequence-feasibility audit.
- State/data consistency audit.
- Deployment-feasibility audit.
- Security-threat treatment audit.
- Unsupported-claim inventory.
- Blocking/open-condition ledger.
- Final architecture acceptance recommendation.

# Validation Outcome Vocabulary

Use item-level outcomes:

```text
PASS
PASS_WITH_CONDITIONS
FAIL
NOT_APPLICABLE
INSUFFICIENT_EVIDENCE
BLOCKED
```

Never convert `INSUFFICIENT_EVIDENCE` into `PASS`.

# Severity

Use:

```text
CRITICAL
HIGH
MEDIUM
LOW
INFO
```

Severity reflects architecture impact, not writing quality.

# Evidence Strength

Use:

```text
HIGH
MEDIUM
LOW
UNKNOWN
```

Evidence may be:

```text
accepted requirement
accepted ADR
quality scenario
benchmark/spike
provider contract
existing production evidence
model cross-check
STRIDE record
deployment proof
```

# Step 1 — Establish Validation Scope

Record:

```text
system / architecture version
target environment
decision horizon
included architecture package
excluded areas
validation profile
```

Do not imply whole-system validation if scope is partial.

# Step 2 — Select Validation Profile

Useful profiles:

```text
LIGHTWEIGHT
STANDARD
CRITICAL_COMPLEX
```

Profile selection should follow architecture risk/complexity.

Do not require every diagram for every system.

# Step 3 — Architecture Package Inventory

Classify every potentially relevant artifact:

```text
REQUIRED
REQUIRED_IF_APPLICABLE
OPTIONAL
NOT_APPLICABLE
MISSING
```

Architecture validity is risk-triggered, not ritual.

# Step 4 — Artifact Freshness / Version Alignment

Check:

```text
Do the artifacts describe the same architecture version?
```

Flag:

```text
ARCHITECTURE_PACKAGE_VERSION_MISMATCH
```

when ADR/C4/deployment/etc. describe incompatible states.

# Step 5 — Source Authority

For each important input identify:

```text
accepted
proposed
draft
unknown authority
```

Do not validate proposed evidence as authoritative without labeling it.

# Step 6 — Drivers → Decisions

Roadmap-required.

For every primary architecture driver:

```text
which decision(s) address it?
where is rationale?
what architectural mechanism exists?
what evidence supports the claim?
```

Use:

```text
DRIVER_ADDRESSED
DRIVER_PARTIALLY_ADDRESSED
DRIVER_UNADDRESSED
DRIVER_EVIDENCE_INSUFFICIENT
```

# Step 7 — Architecture by Preference Detection

Roadmap detection.

Flag a decision if rationale is primarily:

```text
technology popularity
team familiarity alone
industry trend
personal preference
"best practice" without driver link
```

Use:

```text
ARCHITECTURE_BY_PREFERENCE
```

A technology may still be appropriate, but rationale must connect to evidence/constraints/trade-offs.

# Step 8 — Driver Traceability Integrity

Trace:

```text
requirement / quality scenario
→ architecture driver
→ decision / ADR
→ structural/runtime model
→ validation evidence
```

Missing links are validation gaps.

# Step 9 — Quality Attributes → Measurable Support

Roadmap-required.

For every accepted quality scenario:

```text
source
stimulus
environment
artifact
response
response measure
```

validate whether architecture has plausible support.

# Step 10 — Quality Measure Discipline

If measure is TBD:

```text
do not claim validated satisfaction
```

Use:

```text
QUALITY_ATTRIBUTE_MEASURE_REQUIRED
```

Architecture can be:

```text
plausibly supportive
```

without being proven to meet an unknown target.

# Step 11 — Unsupported Scalability Claims

Roadmap detection.

Flag:

```text
scales horizontally
internet scale
high throughput
100x growth ready
```

when no accepted measure, bottleneck model, deployment support, or evidence exists.

Use:

```text
UNSUPPORTED_SCALABILITY_CLAIM
```

# Step 12 — Unsupported Availability Claims

Likewise flag:

```text
highly available
fault tolerant
zero downtime
resilient
```

without topology/recovery evidence.

Use:

```text
UNSUPPORTED_AVAILABILITY_CLAIM
```

# Step 13 — Performance Validation

Need:

```text
accepted target
workload/environment
architectural path
measurement/proof if required
```

If no target:

```text
PERFORMANCE_TARGET_REQUIRED
```

# Step 14 — Availability / Recoverability Validation

Check:

```text
failure domains
failover/recovery path
RTO/RPO
state/data consequences
manual vs automatic behavior
```

Unknown RTO/RPO prevents strong recovery claims.

# Step 15 — Security / Privacy Quality Validation

Check architectural support for accepted:

```text
tenant isolation
authorization
confidentiality
integrity
auditability
privacy boundaries
residency
secret handling
```

Do not substitute “STRIDE performed” for “threat addressed.”

# Step 16 — Modifiability Validation

Use actual change scenarios.

Example:

```text
add new messaging provider
```

Check whether accepted boundaries/dependencies actually localize the change.

# Step 17 — Observability / Diagnosability Validation

Check whether architecture provides plausible path to detect/localize failures required by quality scenarios.

If target diagnostic window is TBD:

```text
DIAGNOSTIC_MEASURE_REQUIRED
```

# Step 18 — Cost Validation

Only validate numeric cost envelope if accepted evidence exists.

Otherwise validate architecture's cost drivers/risks, not fabricated totals.

# Step 19 — Constraints → Respected

Roadmap-required.

For each hard constraint:

```text
where is compliance demonstrated?
which decision/model could violate it?
```

Use:

```text
CONSTRAINT_SATISFIED
CONSTRAINT_VIOLATED
CONSTRAINT_COMPLIANCE_UNKNOWN
```

# Step 20 — Constraint Violation

Roadmap detection.

Any unapproved hard-constraint violation is a blocking architecture finding unless explicitly waived by authoritative decision.

Use:

```text
ARCHITECTURE_CONSTRAINT_VIOLATION
```

# Step 21 — Preferences vs Constraints

Check that preferences are not treated as hard constraints.

# Step 22 — Assumption Validation

For material architecture assumptions:

```text
still true?
evidence strength?
what breaks if false?
revisit trigger exists?
```

# Step 23 — Trade-Offs → Explicit

Roadmap-required.

Every significant decision should expose:

```text
benefits
liabilities
accepted downside
risk
reversal trigger
```

Flag benefit-only ADRs:

```text
TRADEOFF_NOT_EXPLICIT
```

# Step 24 — Trade-Off Consistency

Check trade-off analysis matches final ADR consequences.

If ADR claims only upsides but analysis records downsides:

```text
ADR_TRADEOFF_MISMATCH
```

# Step 25 — ADRs → Aligned

Roadmap-required.

Audit:

```text
status
authority
scope overlap
supersession
contradiction
references
```

# Step 26 — Conflicting ADRs

Roadmap detection.

Use:

```text
CONFLICTING_ACCEPTED_ADRS
```

when accepted ADRs prescribe incompatible outcomes for the same decision scope.

Do not choose one silently.

# Step 27 — ADR → C4 Alignment

Every structural decision should be reflected accurately.

Flag:

```text
ADR_C4_CONFLICT
```

# Step 28 — ADR → Deployment Alignment

Deployment must not silently contradict logical/deployment decisions.

# Step 29 — ADR → Event/Data Alignment

Accepted decisions affecting ownership, consistency, eventing, or boundaries must appear in relevant models.

# Step 30 — C4 → Aligned

Roadmap-required.

Check:

```text
system boundary
containers
components if used
relationships
technology labels
current/target status
```

against ADRs and deployment.

# Step 31 — C4 Abstraction Consistency

Flag:

```text
component modeled as system
deployment node modeled as logical container
undecided service invented
```

# Step 32 — C4 Orphans / Missing Relationships

Check architecturally meaningful elements/relationships.

# Step 33 — Sequence Flows → Feasible

Roadmap-required.

For every critical sequence:

```text
participants exist?
network/path feasible?
authorization exists?
data/store reachable?
ordering compatible?
provider interaction plausible?
state transitions legal?
```

# Step 34 — Impossible Sequence

Roadmap detection.

Use:

```text
IMPOSSIBLE_SEQUENCE
```

Examples:

```text
sequence calls non-existent container
private store is reached by external actor directly
sequence requires queue not in deployment
state transition is forbidden
```

# Step 35 — Missing Failure Paths

Roadmap detection.

For critical scenarios ask:

```text
authorization denied?
provider unavailable?
write failure?
timeout?
duplicate/retry?
concurrent conflict?
```

only when relevant.

Use:

```text
CRITICAL_FAILURE_PATH_MISSING
```

when architecture depends on unspecified behavior.

# Step 36 — Failure Path Sufficiency

Do not require every conceivable failure.

Focus on:

```text
primary drivers
critical journeys
trust boundaries
external dependencies
state-changing operations
```

# Step 37 — Authorization Feasibility

Check protected operations have an authoritative architecture-level decision point.

Frontend-only gating fails validation.

# Step 38 — Concurrency / Idempotency Feasibility

If state/sequence/event models flag:

```text
CONCURRENCY_POLICY_REQUIRED
IDEMPOTENCY_POLICY_REQUIRED
```

determine whether they are blocking for current architecture scope.

Do not invent the policy.

# Step 39 — State Models → Consistent

Roadmap-required.

Check:

```text
states align with use cases/domain data
transitions align with sequences/process flows
terminal states are coherent
illegal transitions are not used
```

# Step 40 — State-Machine Inconsistency

Roadmap detection.

Use:

```text
STATE_MACHINE_INCONSISTENCY
```

Examples:

```text
sequence performs REOPEN but state model excludes it
data model has ARCHIVED but no accepted state
deployment/event flow assumes a transition not accepted
```

# Step 41 — State Reachability

Check accepted states are reachable and critical terminal outcomes feasible.

# Step 42 — Data Model → Consistent

Roadmap-required.

Check:

```text
concept relationships
cardinality
identifiers
ownership
tenant scope
lifecycle
```

against use cases, DFD, state, C4.

# Step 43 — Data Ownership Ambiguity

Roadmap detection.

Use:

```text
DATA_OWNERSHIP_AMBIGUITY
```

when:

```text
multiple authoritative writers
no owner
ownership differs across C4/domain/event models
```

unless intentionally shared and governed.

# Step 44 — Tenant Data Consistency

Validate same-tenant/cross-tenant invariants across:

```text
domain data
sequence auth
DFD
C4 responsibilities
security threats
```

# Step 45 — Identifier Consistency

Check internal/external identifier semantics are not conflated.

# Step 46 — DFD / Privacy Consistency

Check:

```text
all sensitive transfers represented?
third parties align with C4/sequence?
trust boundaries align with deployment?
residency/retention/privacy gaps acknowledged?
```

# Step 47 — DFD Security Completeness

DFD should provide enough:

```text
external entities
processes
stores
flows
trust boundaries
assets
```

for STRIDE where required.

# Step 48 — Event Flow Consistency

Where event-driven architecture exists, check:

```text
producer/consumer exists
event aligns with domain/state
delivery/order/retry/version gaps explicit
deployment transport alignment
```

# Step 49 — Event Infrastructure Mismatch

If event flow says async messaging exists but deployment has no selected/possible transport and architecture depends on it:

```text
EVENT_DEPLOYMENT_MISMATCH
```

An intentionally TBD transport can be conditional rather than failing if architecture decision is not yet needed for the current acceptance threshold.

# Step 50 — Deployment → Feasible

Roadmap-required.

Check:

```text
all logical containers placed
runtime connectivity plausible
data placement coherent
trust boundaries mapped
external providers reachable
observability path plausible
secrets can reach only needed runtime
availability/recovery claims supported
```

# Step 51 — Deployment Mismatch

Roadmap detection.

Use:

```text
DEPLOYMENT_ARCHITECTURE_MISMATCH
```

Examples:

```text
C4 has container with no deployment placement
deployment adds phantom service
sequence requires ingress path absent in topology
residency policy conflicts with placement
```

# Step 52 — Deployment Feasibility with TBD Technology

Technology can remain TBD if the deployment model is architecture-level and no driver requires a specific decision yet.

Do not fail merely because vendor/runtime is undecided.

# Step 53 — Recovery Feasibility

If architecture claims resilience but:

```text
region/zone/failover/RTO/RPO
```

are all unknown:

```text
recovery validation cannot pass strongly
```

# Step 54 — Observability Feasibility

Check critical failure paths have enough architecture support for required diagnosis.

# Step 55 — Secret-Handling Feasibility

If runtime needs provider credentials but no secret-distribution decision exists, determine whether:

```text
condition
or blocker
```

based on architecture phase/profile.

Do not invent secret manager.

# Step 56 — Security Threats → Addressed

Roadmap-required.

Input:

```text
threat-modeling-with-stride
```

For every material threat:

```text
threat
attack path
required mitigation/control
decision/requirement
verification plan
residual risk
owner/acceptance
```

# Step 57 — Threat Status

Use:

```text
ADDRESSED_BY_DESIGN
CONTROL_REQUIRED_DOWNSTREAM
RISK_ACCEPTED
OPEN
BLOCKING
NOT_APPLICABLE
```

# Step 58 — Threat Model Presence

STRIDE is required when architecture includes meaningful security/trust risk such as:

```text
multi-tenancy
public entry points
identity/auth
third-party providers
sensitive data
privileged actions
secrets
deployment/network boundaries
```

If required but missing:

```text
REQUIRED_THREAT_MODEL_MISSING
```

# Step 59 — Threat ≠ Addressed Because Document Exists

A STRIDE threat is only addressed if:

```text
mitigation/control requirement exists
architecture placement is plausible
or
risk is explicitly accepted by authority
```

# Step 60 — Security Control Verification Boundary

Architecture validation validates design/control intent.

Implementation proof remains downstream:

```text
reviewing-application-security
verifying-security-controls
```

# Step 61 — Residual Risk

Record residual architecture risk explicitly.

Do not mark risk eliminated unless evidence supports it.

# Step 62 — Security Conflict

If architecture contradicts security requirement:

```text
ARCHITECTURE_SECURITY_CONFLICT
```

# Step 63 — Cross-Model Identity Matrix

Maintain stable mappings:

```text
ADR decision
C4 element
sequence participant
DFD process/store
domain owner
event producer/consumer
deployment node
```

Detect same concept with incompatible identities.

# Step 64 — Cross-Model Relationship Matrix

Validate major relationships consistently across:

```text
C4
sequence
DFD
deployment
```

# Step 65 — Current vs Target Alignment

For brownfield architecture:

```text
CURRENT
TARGET
TRANSITION
```

must not be mixed as if simultaneously true.

# Step 66 — Architecture Claim Inventory

Extract material claims such as:

```text
tenant isolated
provider resilient
scalable
highly available
modifiable
diagnosable
secure
low operational complexity
```

For each record evidence.

# Step 67 — Unsupported Claim Detection

Use:

```text
SUPPORTED
PARTIALLY_SUPPORTED
UNSUPPORTED
UNMEASURABLE
```

# Step 68 — Evidence Gap vs Design Defect

Distinguish:

```text
architecture may be correct but unproven
```

from:

```text
architecture contradicts requirement
```

These require different remediation.

# Step 69 — Validation Finding Types

Use:

```text
DESIGN_DEFECT
MODEL_CONFLICT
MISSING_DECISION
MISSING_EVIDENCE
UNSUPPORTED_CLAIM
CONSTRAINT_VIOLATION
SECURITY_RISK
TRACEABILITY_GAP
DOCUMENTATION_GAP
```

# Step 70 — Finding Ownership

Record owner only if known.

Do not invent architect/team ownership.

# Step 71 — Finding Remediation

Recommend the smallest appropriate next action:

```text
clarify requirement
measure target
amend ADR
update C4
add failure sequence
resolve state transition
clarify data ownership
complete deployment decision
run architecture spike
address STRIDE threat
```

Do not redesign unrelated architecture.

# Step 72 — Validation Blocking Rules

Typical blockers:

```text
hard constraint violation
primary driver unaddressed
critical security threat open
conflicting accepted ADR
impossible critical sequence
cross-tenant isolation contradiction
deployment topology incompatible with accepted architecture
critical state/data inconsistency
```

# Step 73 — Conditional Acceptance

Valid when:

```text
core architecture coherent
remaining gaps are explicit
gaps do not invalidate primary decisions
owners/evidence actions exist where required
```

# Step 74 — Do Not Hide TBDs

Architecture can be valid with TBD implementation choices.

But architecture-significant TBDs remain conditions/blockers.

# Step 75 — Architecture Spike Recommendation

Use when a material claim needs empirical evidence:

```text
load test
failure simulation
provider proof
latency benchmark
migration rehearsal
recovery drill
```

Only recommend if it can resolve decision uncertainty.

# Step 76 — Validation Profile: Lightweight

Typical minimum:

```text
drivers
constraints
ADRs
C4 L1/L2
key data model
key sequence/flow if needed
deployment implications if meaningful
security check if trust risk
```

# Step 77 — Validation Profile: Standard

Typical:

```text
drivers
NFR/QA scenarios
trade-offs
ADRs
C4
key sequences
state model if applicable
domain data
deployment
DFD/STRIDE for security-relevant architecture
```

# Step 78 — Validation Profile: Critical / Complex

May additionally require:

```text
full DFD
event flows
failure sequences
detailed recovery topology
explicit performance/reliability evidence
complete threat model
architecture spikes
```

# Step 79 — Not-Applicable Discipline

A missing model can be:

```text
NOT_APPLICABLE
```

only with rationale.

Do not mark absent state/event models as defects when the system has no relevant lifecycle/event architecture.

# Step 80 — Traceability Coverage

For each primary driver:

```text
driver
→ decision
→ model
→ evidence
→ threat/control if relevant
```

# Step 81 — Contradiction Priority

A contradiction outranks a documentation gap.

Example:

```text
ADR says single deployable
deployment shows five services
```

is not merely stale documentation.

# Step 82 — Validation Report Finding Format

Each finding:

```text
ID
severity
type
title
evidence
affected drivers/requirements
affected artifacts
impact
recommended next action
blocking?
```

# Step 83 — Validation Evidence Matrix

Record:

```text
claim
expected evidence
actual evidence
result
```

# Step 84 — Architecture Acceptance Recommendation

Use:

```text
ACCEPT
ACCEPT_WITH_CONDITIONS
REJECT_PENDING_REWORK
BLOCKED_PENDING_DECISION
BLOCKED_PENDING_EVIDENCE
```

# Step 85 — Final Status

Use:

```text
ARCHITECTURE_VALIDATED
ARCHITECTURE_VALIDATED_WITH_CONDITIONS
ARCHITECTURE_REQUIRES_REWORK
ARCHITECTURE_REQUIRES_DECISIONS
ARCHITECTURE_REQUIRES_EVIDENCE
ARCHITECTURE_SECURITY_BLOCKED
ARCHITECTURE_CONFLICTED
BLOCKED
```

# Step 86 — Accepted Architecture Package Gate

Only return:

```text
ARCHITECTURE_VALIDATED
```

when:

```text
primary drivers addressed
hard constraints respected
critical models coherent
no blocking security threats
critical sequences feasible
data/state/deployment consistent
material claims evidence-backed
```

# Step 87 — Conditional Package Gate

Use:

```text
ARCHITECTURE_VALIDATED_WITH_CONDITIONS
```

when remaining conditions are explicit and non-blocking for the next planned phase.

# Step 88 — OpenSpec / Implementation Handoff

Validation output should identify:

```text
accepted architecture constraints
ADRs implementation must respect
required security controls
quality scenarios to verify
critical flows
data/tenant invariants
deployment assumptions
known deferred decisions
```

Then implementation planning/OpenSpec can proceed without losing architecture intent.

# Output

Use:

```text
assets/architecture-validation-report.md
```

## Completion Criteria

- [ ] Validation scope/profile/version are explicit.
- [ ] Architecture-package inventory is risk-based rather than ritualistic.
- [ ] Artifact versions/authority are checked.
- [ ] Every primary driver maps to decision/model/evidence.
- [ ] Architecture-by-preference decisions are detected.
- [ ] Quality attributes are checked against measurable scenarios.
- [ ] Unknown quality measures do not pass as satisfied.
- [ ] Unsupported scalability/availability/performance claims are detected.
- [ ] Hard constraints are checked and violations block unless explicitly waived.
- [ ] Assumptions remain explicit and have impact/revisit treatment.
- [ ] Trade-offs and negative consequences are explicit.
- [ ] ADR status/scope/supersession/consistency are audited.
- [ ] C4 aligns with ADRs/deployment.
- [ ] Critical sequences are feasible.
- [ ] Missing critical failure paths are detected.
- [ ] Authorization is authoritative, not frontend-only.
- [ ] Concurrency/idempotency gaps are classified rather than invented.
- [ ] State models align with use cases/sequences/data.
- [ ] Data relationships/ownership/tenant/lifecycle are consistent.
- [ ] DFD/privacy/trust boundaries align with architecture/deployment.
- [ ] Event flows align with state/domain/deployment where applicable.
- [ ] Deployment places accepted logical elements without phantom infrastructure.
- [ ] Recovery/observability/secrets claims are evidence-backed or conditional.
- [ ] STRIDE exists when required.
- [ ] Threats are not considered addressed merely because a threat model exists.
- [ ] Security threats have design response/control requirement/risk acceptance.
- [ ] Residual risk is explicit.
- [ ] Cross-model identity/relationship consistency is checked.
- [ ] Current/target/transition states are not mixed.
- [ ] Architecture claims have explicit evidence status.
- [ ] Evidence gaps are distinguished from design defects.
- [ ] Findings have severity/type/impact/evidence/action/blocking status.
- [ ] Blockers use architecture significance, not documentation preference.
- [ ] Missing optional models can be NOT_APPLICABLE with rationale.
- [ ] Final acceptance recommendation/status is explicit.
- [ ] OpenSpec/implementation handoff preserves architecture constraints and controls.

## References

- Read `references/validation-scope-profiles-evidence-and-package-inventory.md` first.
- Read `references/drivers-quality-attributes-constraints-and-unsupported-claims.md`.
- Read `references/adrs-tradeoffs-c4-and-cross-model-consistency.md`.
- Read `references/sequence-state-data-dfd-event-and-deployment-feasibility.md`.
- Read `references/security-threat-treatment-residual-risk-and-control-handoff.md`.
- Read `references/findings-blockers-conditional-acceptance-and-rework.md`.
- Read `references/traceability-claims-evidence-and-openspec-handoff.md`.
- Read `references/architecture-validation-report-audit.md` before completion.
