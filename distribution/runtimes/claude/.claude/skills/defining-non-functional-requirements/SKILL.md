---
name: defining-non-functional-requirements
description: Converts PRD quality expectations, operational needs, constraints, risks, and system-level concerns into an explicit catalog of measurable, owned, and testable non-functional requirements. Use after a PRD exists and before detailed quality-attribute scenarios, architecture-driver identification, architecture design, or validation. Formalize performance, availability, scalability, reliability, recoverability, security, privacy, observability, maintainability, interoperability, cost, accessibility, and usability requirements only to the precision supported by evidence. Preserve TBD values and targeted clarification questions instead of inventing latency, availability, RTO/RPO, scale, security, cost, or accessibility targets. Do not select architecture, technologies, topology, or implementation mechanisms.
---

# Defining Non-Functional Requirements

## Purpose

Turn PRD-level quality expectations into explicit non-functional requirements that are measurable, owned, and testable enough to guide architecture and later verification.

Core workflow:

```text
PRD quality expectations
→ classify quality concern
→ define scope + stimulus/context
→ define measurable response/constraint
→ preserve unknown measures as TBD
→ identify owner/source
→ define verification approach
→ identify trade-off tension
→ trace to goals / FRs / risks
→ audit measurability and feasibility
→ produce NFR catalog
```

Output:

```text
non-functional-requirements-catalog.md
```

## Core Principle

A non-functional requirement should make clear:

```text
what quality or constraint matters
for which part of the system
under what conditions
how success will be measured
who owns/approved it
how it can eventually be verified
```

without deciding the architecture.

## Use When

- A PRD contains vague or explicit quality expectations.
- Architecture work needs measurable performance/availability/scale/recovery/security/privacy/observability/cost constraints.
- Product/system goals imply system-level qualities.
- Operations, security, privacy, accessibility, or platform stakeholders have quality requirements.
- Existing NFRs need normalization and traceability.
- A brownfield system needs current/target quality requirements separated.

## Do Not Use When

- Product discovery is still vague.
- The task is to define functional behavior.
- The task is to turn NFRs into detailed quality-attribute scenarios; use `defining-quality-attributes`.
- The task is to identify architecture drivers.
- The task is to choose a database, cloud, architecture style, cache, queue, or deployment topology.
- The task is detailed security control verification.
- The task is performance tuning of implemented code.

## Inputs

Preferred:

- PRD;
- PRD goals;
- PRD NFR/quality section;
- functional requirements catalog;
- constraints;
- assumptions;
- risks;
- success metrics;
- operational requirements;
- security/privacy requirements;
- accessibility/usability expectations;
- existing SLO/SLA/policy evidence where authoritative;
- applicable `AGENTS.md`.

Optional:

- current production metrics;
- current incident history;
- existing compliance/policy requirements;
- provider limits;
- cost/budget evidence;
- brownfield baseline measurements.

## Outputs

- Non-functional requirements catalog.
- Measurability gap ledger.
- NFR traceability matrix.
- Trade-off/tension map.
- Verification-intent matrix.
- Quality-attribute handoff.
- Architecture-driver candidate handoff.

# NFR Identity

Use stable IDs:

```text
NFR-001
NFR-002
NFR-003
```

Do not reuse IDs for different semantics.

# NFR Status

Use:

```text
PROPOSED
REVIEW_REQUIRED
ACCEPTED
DEFERRED
REJECTED
SUPERSEDED
```

Only use `ACCEPTED` with authoritative evidence.

# NFR Quality Status

Use:

```text
MEASURABLE
PARTIALLY_MEASURABLE
MEASURE_REQUIRED
SCOPE_REQUIRED
ENVIRONMENT_REQUIRED
OWNER_REQUIRED
CONFLICTED
DEFERRED
```

# NFR Anatomy

Each meaningful NFR should include:

```text
ID
quality category
status
priority
scope/artifact
environment/context
stimulus/load/failure condition
required response/constraint
response measure / target
measurement method or verification intent
source/owner
linked goals
linked FRs
linked risks/constraints
assumptions
open questions
```

This is deliberately close to architecture-quality language without replacing the later quality-attribute scenario skill.

# Functional vs Non-Functional

Functional:

```text
what behavior occurs
```

NFR:

```text
how well
under what load/failure/security/privacy/operational constraint
```

Example:

```text
FR:
Agent can view a conversation.

NFR:
Conversation viewing remains available during an email-provider outage.
```

# Step 1 — Establish Scope and Authority

Record:

```text
PRD version/status
functional catalog version
existing quality requirements
stakeholder/policy authority
known baselines
constraints
```

Do not create quality targets from unsupported intuition.

# Step 2 — Classify Quality Categories

Supported categories include:

```text
PERFORMANCE
AVAILABILITY
SCALABILITY
RELIABILITY
RECOVERABILITY
SECURITY
PRIVACY
OBSERVABILITY
MAINTAINABILITY
MODIFIABILITY
INTEROPERABILITY
TESTABILITY
ACCESSIBILITY
USABILITY
COST_EFFICIENCY
DATA_RESIDENCY
COMPLIANCE
OPERABILITY
```

Use only relevant categories.

# Step 3 — Performance

Performance NFRs should identify, where known:

```text
operation
user/system context
load
percentile/statistic
target
measurement boundary
```

Good:

```text
At the accepted normal-load profile,
95% of conversation-list requests complete within [TBD] ms.
```

Better only when target is accepted:

```text
p95 ≤ 300 ms at 200 requests/sec
```

Do not invent the numbers.

# Vague “Fast” Requirement

Roadmap evaluation:

Input:

```text
dashboard must be very fast
```

Output:

```text
NFR category: PERFORMANCE
scope: dashboard interaction(s) TBD
load: TBD
measure: TBD
target: TBD
status: MEASURE_REQUIRED
questions:
- which interaction?
- what percentile?
- what load?
- what target?
```

Do not normalize “very fast” into an arbitrary latency.

# Client vs Server Performance

Preserve the actual measurement boundary.

Examples:

```text
API latency
page load
interaction latency
job completion
message processing
```

Do not mix them.

# Step 4 — Availability

Availability should identify:

```text
service/capability
operating window
failure context
availability measure
allowed downtime/exclusions
```

Example:

```text
Conversation reading remains available while the email provider is unavailable.
```

This may be a degraded-mode requirement even before an SLA percentage exists.

# Availability Target

Roadmap evaluation:

If authoritative target exists:

```text
99.9% monthly availability
```

record it with source and measurement window.

If not:

```text
target = TBD
```

Do not invent `99.99%`.

# Availability vs Reliability

Availability:

```text
service is usable when needed
```

Reliability:

```text
service behaves correctly over time / operations
```

Keep them distinct when useful.

# Step 5 — Scalability

Scalability NFRs need dimensions.

Potential:

```text
tenants
users
requests/sec
concurrent sessions
messages/day
dataset size
event throughput
geographies
growth rate
```

Do not write:

```text
system must scale horizontally
```

That is an implementation direction, not the need.

# Scalability Target

Roadmap evaluation:

Good:

```text
support X concurrent users / Y messages per day
with accepted performance targets
```

only when X/Y are sourced.

If scale forecast is unknown:

```text
SCALE_FORECAST_REQUIRED
```

# Step 6 — Reliability

Capture requirements such as:

```text
no lost accepted customer messages
duplicate processing does not create duplicate business effect
existing data remains readable during provider outage
```

Use product semantics.

Do not prescribe queues/idempotency implementation unless already contractually required.

# Step 7 — Recoverability

Recoverability may include:

```text
RTO
RPO
recovery mode
restore verification
manual fallback
dependency recovery
```

Do not invent RTO/RPO.

# Recovery Objective

Roadmap evaluation:

If stakeholder says:

```text
we can tolerate at most 15 minutes of data loss
```

record:

```text
RPO ≤ 15 min
```

If only:

```text
must recover quickly
```

use `MEASURE_REQUIRED`.

# RTO vs RPO

```text
RTO
→ acceptable time to restore service

RPO
→ acceptable amount of data loss expressed as time
```

Do not conflate them.

# Step 8 — Security

System-level security NFRs can include:

```text
tenant isolation
authentication expectations
authorization properties
auditability
confidentiality
integrity
secret handling
abuse resistance
security monitoring
```

Keep them at required-property level.

Detailed threats:

```text
threat-modeling-with-stride
```

Detailed implemented weaknesses:

```text
reviewing-application-security
```

Control verification:

```text
verifying-security-controls
```

Do not duplicate those skills.

# Security Measurability

Not every security NFR is numeric.

Example:

```text
A user from one tenant must not access another tenant's conversation data.
```

Verification can be behavioral/negative testing.

Measurable means verifiable, not necessarily numerical.

# Step 9 — Privacy

Privacy NFRs may include:

```text
data minimization
retention
deletion
consent
purpose limitation
third-party transfer
data residency
access/export
logging restrictions
```

Do not invent retention periods or legal requirements.

If policy is unresolved:

```text
PRIVACY_DECISION_REQUIRED
```

# Step 10 — Observability

Roadmap evaluation:

Observability requirements should state what operators must be able to detect/diagnose, not which tool to install.

Good:

```text
Operators can determine whether inbound email processing is failing
and identify the affected tenant/provider within the accepted diagnostic window.
```

Target/tool may remain TBD.

Bad:

```text
Use Datadog.
```

unless Datadog is a hard organizational constraint.

# Observability Dimensions

Potential:

```text
detection
diagnosis
traceability
audit
alerting
business metrics
correlation
```

# Step 11 — Maintainability / Modifiability

Avoid vague:

```text
code should be maintainable
```

Prefer architecture/product change scenarios or constraints such as:

```text
adding a new messaging provider should not require changing tenant/business rules
```

Exact scenario formalization belongs in `defining-quality-attributes`.

# Step 12 — Interoperability

Capture:

```text
external standards
supported protocols
data formats
compatibility windows
version expectations
```

only when accepted.

Do not choose protocol unless required.

# Step 13 — Cost

Roadmap evaluation:

A cost NFR must trace to an accepted budget/ceiling/objective.

Examples:

```text
monthly infrastructure cost ≤ accepted budget
cost per tenant ≤ target
provider spend stays within approved ceiling
```

If no budget exists:

```text
COST_TARGET_REQUIRED
```

Do not invent one.

# Cost Ceiling vs Architecture

A cost ceiling is a constraint/NFR.

Choosing serverless/Kubernetes/reserved instances is architecture/design.

# Step 14 — Accessibility

System-level accessibility requirements may capture:

```text
accepted conformance standard
keyboard operability
assistive-technology support
product-scope accessibility obligation
```

Only use a standard/level if explicitly accepted.

Detailed UI design belongs to frontend accessibility skills.

# Step 15 — Usability

Avoid:

```text
easy
intuitive
seamless
```

without measurable/observable criteria.

Potential measures:

```text
task completion
error rate
time on task
support burden
```

Only when evidence supports them.

# Step 16 — Data Residency / Compliance

Record policy/regulatory constraints only when authoritative.

Include:

```text
data category
location/jurisdiction
scope
source/policy
```

Do not infer compliance regimes from company geography.

# Step 17 — Operability

Potential requirements:

```text
manual fallback
support diagnosis
safe operational controls
maintenance windows
rollout/rollback expectations
```

Keep them outcome-based.

# Step 18 — Environment

Every NFR should identify where it applies when material.

Examples:

```text
production normal load
peak load
provider outage
regional failure
deployment window
incident recovery
```

Do not assume all NFRs apply identically in all environments.

# Step 19 — Stimulus / Condition

A useful NFR often needs the condition that activates it.

Examples:

```text
traffic spike
dependency outage
node failure
large tenant
operator incident
new provider integration
```

This prepares input for `defining-quality-attributes`.

# Step 20 — Response / Constraint

State what the system should guarantee.

Examples:

```text
remain readable
restore within accepted time
prevent cross-tenant access
detect failure
stay within cost ceiling
maintain response-time target
```

# Step 21 — Measurement

Measurement may be:

```text
numeric
boolean/pass-fail
policy compliance
scenario verification
operational exercise
test
inspection
```

Do not treat only numerical requirements as valid NFRs.

# Step 22 — Verification Intent

For each NFR, identify a likely future verification class:

```text
LOAD_TEST
SYNTHETIC_MONITOR
CHAOS/FAILURE_TEST
RECOVERY_DRILL
SECURITY_TEST
PRIVACY_REVIEW
ACCESSIBILITY_AUDIT
CONTRACT_TEST
OBSERVABILITY_DRILL
COST_ANALYSIS
ARCHITECTURE_REVIEW
INSPECTION
```

This is intent, not a final test plan.

# Step 23 — Baseline vs Target

For brownfield systems separate:

```text
current baseline
target
```

Example:

```text
current p95: 900 ms
target: TBD
```

Do not imply current baseline is accepted target.

# Step 24 — Hard Requirement vs Objective

Classify:

```text
HARD_REQUIREMENT
TARGET
OBJECTIVE
ASPIRATION
TBD
```

Only use `HARD_REQUIREMENT` with authority.

# Step 25 — Constraint vs NFR

Some constraints are NFR-like.

Example:

```text
must run in approved EU region
```

can be:

```text
constraint + data residency NFR
```

Cross-reference rather than duplicate inconsistently.

# Step 26 — Trade-Off Tensions

Identify tensions without resolving architecture.

Examples:

```text
availability ↔ cost
consistency ↔ latency
privacy retention ↔ product history
observability detail ↔ privacy
security friction ↔ usability
```

Use:

```text
TRADEOFF_REQUIRES_ARCHITECTURE_ANALYSIS
```

Do not choose a side.

# Step 27 — Conflicts

If two accepted-looking NFRs conflict:

```text
NFR_CONFLICT_REQUIRES_DECISION
```

Examples:

```text
retain indefinitely
vs
delete after policy period

zero downtime
vs
fixed single maintenance window
```

Do not silently reconcile.

# Step 28 — Dependency Feasibility

If an NFR depends on external provider behavior, record it.

Example:

```text
99.99% end-to-end availability
```

may be impossible if a mandatory provider offers lower availability.

Flag:

```text
DEPENDENCY_FEASIBILITY_REQUIRED
```

Do not fabricate feasibility.

# Step 29 — Quality Ownership

Record owner/authority where known:

```text
product
security
privacy
SRE/platform
finance
legal
accessibility/design
engineering
```

Do not invent approvers.

# Step 30 — Traceability

Each NFR should trace to:

```text
PRD goal
PRD NFR/quality expectation
functional capability/FR
constraint
risk
source/policy
```

# Step 31 — Coverage Audit

Audit relevant PRD quality categories:

```text
COVERED
PARTIALLY_COVERED
NO_NFR_REQUIRED
MEASURE_REQUIRED
DECISION_REQUIRED
```

Do not create NFRs for every possible category.

# Step 32 — Measurability Audit

For each NFR ask:

```text
Can this be verified?
Is scope clear?
Is environment clear?
Is target/criterion clear enough?
If not, is the gap explicitly recorded?
```

A draft NFR may be valuable even with `TBD`, but it must not masquerade as measurable.

# Step 33 — Feasibility Audit

Do not certify feasibility without evidence.

Potential status:

```text
FEASIBILITY_UNKNOWN
FEASIBILITY_SUPPORTED
FEASIBILITY_AT_RISK
```

Architecture trade-off analysis later owns solution feasibility.

# Step 34 — Architecture Leakage Audit

Remove:

```text
microservices
Kubernetes
Redis
Kafka
PostgreSQL
multi-region active-active
CDN
serverless
```

unless they are already accepted constraints.

Keep the underlying NFR.

# Step 35 — Quality-Attribute Handoff

Group NFRs that need detailed scenarios for:

```text
defining-quality-attributes
```

Typical:

```text
availability
performance
recoverability
modifiability
security
operability
```

# Step 36 — Architecture-Driver Candidate Handoff

Flag NFRs likely to be architecture-significant because of:

```text
extreme target
strict quality constraint
broad system scope
high failure impact
cross-cutting security/privacy requirement
external dependency
regulatory/platform constraint
```

Do not decide final architecture-driver status here.

# NFR Catalog Decision

Use:

```text
NON_FUNCTIONAL_REQUIREMENTS_READY
NON_FUNCTIONAL_REQUIREMENTS_READY_WITH_TBDS
NON_FUNCTIONAL_REQUIREMENTS_REQUIRE_MEASURES
NON_FUNCTIONAL_REQUIREMENTS_REQUIRE_PRODUCT_DECISION
NON_FUNCTIONAL_REQUIREMENTS_REQUIRE_POLICY_DECISION
NON_FUNCTIONAL_REQUIREMENTS_CONFLICTED
BLOCKED
```

# Output

Use:

```text
assets/non-functional-requirements-catalog.md
```

## Completion Criteria

- [ ] PRD/version/status and authoritative sources are recorded.
- [ ] Only relevant quality categories are used.
- [ ] Stable NFR IDs are assigned.
- [ ] NFR status/priority preserve authority.
- [ ] Each NFR has scope/artifact when material.
- [ ] Environment/context is explicit when material.
- [ ] Stimulus/load/failure condition is explicit when material.
- [ ] Required response/constraint is explicit.
- [ ] Measurement/verification criterion is explicit or marked TBD.
- [ ] Vague “fast” language does not receive invented latency.
- [ ] Availability targets are source-backed.
- [ ] Scalability dimensions/targets are source-backed.
- [ ] RTO/RPO are not invented.
- [ ] Security NFRs remain required properties rather than detailed controls.
- [ ] Privacy NFRs do not invent retention/legal obligations.
- [ ] Observability requirements state detection/diagnosis outcomes rather than tools.
- [ ] Maintainability/modifiability language is made concrete enough for later scenarios.
- [ ] Interoperability requirements preserve accepted external constraints only.
- [ ] Cost ceilings/targets are not invented.
- [ ] Accessibility standards/levels are not invented.
- [ ] Usability language is not left as untestable adjectives without a gap.
- [ ] Brownfield baseline is separated from target.
- [ ] Hard requirement/target/objective/aspiration are distinguished.
- [ ] Constraints are cross-referenced consistently.
- [ ] Trade-off tensions are surfaced without architecture resolution.
- [ ] Conflicts are preserved.
- [ ] External dependency feasibility concerns are visible.
- [ ] Owner/source is recorded where known.
- [ ] NFRs trace to PRD/goals/FRs/risks/constraints.
- [ ] Relevant quality coverage is audited.
- [ ] Measurability gaps are explicit.
- [ ] Architecture implementation leakage is removed unless accepted constraint.
- [ ] Quality-attribute scenario candidates are identified.
- [ ] Architecture-driver candidates are identified without final classification.
- [ ] Final catalog readiness is explicit.

## References

- Read `references/nfr-anatomy-measurability-authority-and-verification.md` first.
- Read `references/performance-availability-scalability-and-reliability.md`.
- Read `references/recoverability-security-privacy-and-residency.md`.
- Read `references/observability-maintainability-interoperability-and-operability.md`.
- Read `references/cost-accessibility-usability-and-compliance.md`.
- Read `references/conflicts-tradeoffs-dependencies-and-brownfield-baselines.md`.
- Read `references/traceability-quality-attribute-and-architecture-driver-handoffs.md`.
- Read `references/non-functional-requirements-catalog-audit.md` before completion.
