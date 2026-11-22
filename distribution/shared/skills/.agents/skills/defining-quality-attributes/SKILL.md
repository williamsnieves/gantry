---
name: defining-quality-attributes
description: "Converts accepted or review-ready non-functional requirements into architecture-relevant quality-attribute scenarios using the source \u2192 stimulus \u2192 environment \u2192 artifact \u2192 response \u2192 response measure structure. Use before identifying architecture drivers, comparing candidate architectures, or validating an architecture when qualities such as availability, performance, scalability, reliability, modifiability, maintainability, security, privacy, observability, recoverability, interoperability, testability, usability, accessibility, or cost efficiency need concrete scenarios. Preserve unsupported measures as TBD, distinguish quality attributes from constraints and implementation tactics, expose trade-off tensions, and produce scenarios that can later be used to evaluate architecture decisions. Do not choose architecture, invent targets, prescribe tactics, or treat every NFR as architecture-significant."
---

# Defining Quality Attributes

## Purpose

Turn NFRs into concrete, architecture-relevant quality-attribute scenarios.

Core model:

```text
source
→ stimulus
→ environment
→ artifact
→ response
→ response measure
```

These scenarios become direct inputs to:

```text
identifying-architecture-drivers
analyzing-architecture-tradeoffs
validating-architecture-design
```

## Core Principle

A quality attribute is useful to architecture only when it describes a situation the architecture must handle and an observable response that can be evaluated.

Bad:

```text
The system must be scalable.
```

Better:

```text
Source:
customer traffic

Stimulus:
request volume increases to the accepted peak profile

Environment:
production during peak operation

Artifact:
conversation-query capability

Response:
the system continues serving requests without violating the accepted latency/error targets

Response measure:
throughput/latency/error targets from NFRs, or TBD if not yet approved
```

## Use When

- Formal NFRs exist and architecture work needs scenario-based quality inputs.
- Availability/recovery/failure behavior needs to be made concrete.
- Performance/scalability concerns need context and measurable response.
- Security/privacy/observability qualities need architecture-oriented scenarios.
- Modifiability/maintainability/testability need change scenarios.
- Candidate architecture options will later be compared against qualities.
- Architecture validation will need traceable scenarios.

## Do Not Use When

- Requirements discovery is still vague.
- NFRs have not yet been defined.
- The task is to identify final architecture drivers; use `identifying-architecture-drivers`.
- The task is to choose architecture.
- The task is to perform STRIDE threat modeling.
- The task is detailed performance/security testing.
- The task is to invent numerical SLOs.

## Inputs

Preferred:

- PRD;
- functional requirements catalog;
- non-functional requirements catalog;
- constraints;
- assumptions;
- risks;
- policy requirements;
- external dependency evidence;
- existing baselines/targets;
- applicable `AGENTS.md`.

Optional:

- incident history;
- production metrics;
- existing architecture;
- provider limits;
- current operational procedures.

## Outputs

- Quality Attribute Scenario Catalog.
- Quality-attribute priority/importance record where authoritative.
- Trade-off tension matrix.
- Scenario-to-NFR traceability.
- Scenario completeness/measurability audit.
- Architecture-driver candidate handoff.
- Architecture-validation handoff.

# Scenario Structure

Use:

```text
source
stimulus
environment
artifact
response
response measure
```

## Source

Who or what generates the stimulus?

Examples:

```text
end user
traffic spike
external provider
attacker
operator
deployment team
new business requirement
hardware/network failure
regulatory request
```

Do not confuse source with stakeholder authority.

## Stimulus

What event/change/failure occurs?

Examples:

```text
email provider becomes unavailable
traffic increases
operator must diagnose failed ingestion
new messaging provider must be added
tenant user attempts cross-tenant access
regional dependency fails
```

## Environment

Under what conditions?

Examples:

```text
normal production operation
peak load
degraded mode
deployment
incident recovery
partial provider outage
maintenance window
```

Do not assume all scenarios run under normal conditions.

## Artifact

Which part of the system is affected?

Examples:

```text
conversation read capability
message-ingestion capability
tenant authorization boundary
deployment pipeline
data-recovery subsystem
support-agent UI/API journey
```

Stay architecture-neutral enough not to invent containers/services prematurely.

## Response

What must the system do?

Examples:

```text
remain readable
reject unauthorized access
restore service
detect and expose failure context
continue degraded manual workflow
accept a new provider with bounded change impact
```

## Response Measure

How is the response judged?

May be:

```text
numeric
boolean/pass-fail
time bound
error-rate bound
data-loss bound
change-effort bound
inspection/control evidence
```

If missing:

```text
TBD
```

Do not invent.

# Scenario Identity

Use stable IDs:

```text
QA-001
QA-002
QA-003
```

# Scenario Status

Use:

```text
PROPOSED
REVIEW_REQUIRED
ACCEPTED
DEFERRED
REJECTED
SUPERSEDED
```

# Scenario Quality Status

Use:

```text
READY
READY_WITH_TBD_MEASURE
SOURCE_REQUIRED
STIMULUS_REQUIRED
ENVIRONMENT_REQUIRED
ARTIFACT_REQUIRED
RESPONSE_REQUIRED
MEASURE_REQUIRED
CONFLICTED
```

# Quality Attributes

Typical categories:

```text
AVAILABILITY
PERFORMANCE
SCALABILITY
RELIABILITY
MODIFIABILITY
MAINTAINABILITY
SECURITY
PRIVACY
OBSERVABILITY
RECOVERABILITY
INTEROPERABILITY
TESTABILITY
USABILITY
ACCESSIBILITY
COST_EFFICIENCY
```

Use only those supported by NFRs.

# Step 1 — Establish Authoritative NFR Inputs

Record:

```text
NFR catalog version/status
PRD version/status
accepted constraints
accepted measures/targets
TBDs
risks
external dependencies
```

Do not upgrade a proposed NFR into an accepted quality scenario.

# Step 2 — Select Scenario-Worthy NFRs

Not every NFR needs a separate scenario.

Prefer scenarios for qualities where architecture behavior under context matters.

Examples:

```text
provider outage
traffic spike
recovery
cross-tenant access
new integration/change
diagnostic incident
regional failure
```

Simple static policy constraints may remain constraints instead.

# Step 3 — Preserve Traceability

Each scenario must trace to one or more:

```text
NFR
PRD goal
FR/capability
risk
constraint
policy
source
```

# Step 4 — Availability Scenarios

A good availability scenario may capture:

```text
source:
external dependency

stimulus:
provider becomes unavailable

environment:
production

artifact:
affected capability

response:
system continues/degrades/rejects safely

measure:
availability/degraded-mode criterion
```

## Example

```text
QA-AV-001

Source:
email provider

Stimulus:
provider is unavailable

Environment:
production during normal support operation

Artifact:
conversation-reading capability

Response:
agents can continue reading previously accepted conversations

Response measure:
successful read behavior remains available; exact service-level target TBD
```

Do not prescribe cache/queue/database replication.

# Step 5 — Performance Scenarios

Include:

```text
source/load generator
stimulus/load profile
environment
artifact/operation
response
measure
```

If NFR has no accepted load/percentile/target:

```text
READY_WITH_TBD_MEASURE
```

or:

```text
MEASURE_REQUIRED
```

Do not invent them.

# Step 6 — Scalability Scenarios

Focus on growth/change in load dimension.

Examples:

```text
tenant count increases
message volume grows
concurrent users peak
geographic distribution expands
```

Response should describe preserved quality properties, not “scale horizontally.”

# Step 7 — Reliability Scenarios

Useful stimuli:

```text
duplicate message
transient provider failure
retry
partial operation failure
out-of-order event
```

Response should describe correct business outcome.

Do not prescribe idempotency implementation unless already a contract requirement.

# Step 8 — Recoverability Scenarios

Useful:

```text
data store unavailable
regional failure
operator restores backup
deployment rollback
```

Response measures can include:

```text
RTO
RPO
restore correctness
recovery verification
```

Only use values from NFR evidence.

# Step 9 — Security Scenarios

Security QA scenarios should describe required security behavior, not replace STRIDE.

Example:

```text
Source:
authenticated user from tenant A

Stimulus:
attempts to access tenant B conversation

Environment:
production

Artifact:
tenant data access boundary

Response:
access is denied and protected data is not disclosed

Measure:
no unauthorized data returned; relevant security/audit evidence produced per accepted requirements
```

Threat discovery still belongs to:

```text
threat-modeling-with-stride
```

# Step 10 — Privacy Scenarios

Possible stimuli:

```text
retention period expires
user requests deletion/export
analytics consent withdrawn
third-party transfer attempted
```

Only create scenario if policy/behavior is accepted enough.

If retention policy unresolved:

```text
POLICY_DECISION_REQUIRED
```

Do not invent behavior.

# Step 11 — Observability Scenarios

Example:

```text
Source:
email provider / ingestion pipeline

Stimulus:
inbound processing fails

Environment:
production incident

Artifact:
email-ingestion capability

Response:
operator can detect failure and identify affected tenant/provider

Response measure:
diagnostic window TBD if not accepted
```

Do not choose Datadog/Splunk/etc.

# Step 12 — Modifiability Scenarios

Modifiability quality scenarios describe a requested change.

Canonical shape:

```text
Source:
product/engineering request

Stimulus:
new messaging provider must be added

Environment:
normal development

Artifact:
messaging integration capability

Response:
system accommodates new provider without changing unrelated business rules

Response measure:
accepted change-effort/affected-scope measure, or TBD
```

Do not prescribe plugin architecture yet.

# Step 13 — Maintainability Scenarios

May cover:

```text
defect diagnosis
localized change
dependency upgrade
routine maintenance
```

Avoid vague “clean code.”

# Step 14 — Interoperability Scenarios

Possible stimulus:

```text
external system sends/requests data using an accepted standard/version
```

Response:

```text
system exchanges/validates data correctly
```

Do not invent protocol.

# Step 15 — Testability Scenarios

Example:

```text
Source:
engineering team

Stimulus:
critical business rule changes

Environment:
development/CI

Artifact:
business capability

Response:
rule can be verified independently at an appropriate boundary

Response measure:
verification evidence/effort target if accepted
```

Do not force a specific test framework.

# Step 16 — Usability Scenarios

Use observable user outcomes if supported.

Example:

```text
new support agent performs first conversation reply
```

Measures may include:

```text
task completion
time on task
error rate
assistance needed
```

Do not invent targets.

# Step 17 — Accessibility Scenarios

Possible source/stimulus:

```text
keyboard-only user performs a critical workflow
screen-reader user encounters form validation
```

Response:

```text
workflow remains operable/perceivable according to accepted accessibility requirement
```

Only name standards/levels when sourced.

# Step 18 — Cost Efficiency Scenarios

Example:

```text
Source:
usage growth

Stimulus:
monthly message volume doubles

Environment:
production

Artifact:
system operating footprint

Response:
system continues meeting accepted quality requirements within approved cost objective

Response measure:
approved cost ceiling/efficiency target, or TBD
```

Do not select infrastructure tactic.

# Step 19 — General vs Concrete Scenarios

Prefer concrete system-specific scenarios.

Avoid cataloging only generic forms like:

```text
a failure occurs
→ system recovers
```

A scenario should refer to a meaningful capability/risk.

# Step 20 — Scenario Variants

One NFR can produce multiple scenarios when environments/stimuli differ materially.

Example:

```text
availability under provider outage
availability under deployment
availability under regional failure
```

Do not multiply scenarios without value.

# Step 21 — Merge Duplicates

If multiple NFRs describe the same architecture situation, one scenario may trace to several NFRs.

Preserve traceability.

# Step 22 — Response Measure Discipline

Never infer a response measure from industry convention.

Examples prohibited without evidence:

```text
99.99%
p95 200 ms
RTO 5 min
RPO 0
WCAG AA
< 2 engineer-days
```

# Step 23 — Qualitative Measures

Valid when precise enough:

```text
no cross-tenant data disclosed
manual reply remains available
accepted messages are not lost
operator can identify affected tenant/provider
```

Not everything needs a number.

# Step 24 — Scenario Priority

Use authoritative priority if present.

Otherwise:

```text
TBD
```

Architecture-driver identification later can assess architectural significance.

# Step 25 — Business Criticality

Record where sourced:

```text
CRITICAL
HIGH
MEDIUM
LOW
TBD
```

Do not derive it from intuition alone.

# Step 26 — Trade-Off Tension

Each scenario may link to tensions.

Examples:

```text
availability ↔ cost
consistency ↔ latency
privacy ↔ observability
security ↔ usability
modifiability ↔ simplicity
```

Do not resolve them here.

# Step 27 — Constraint Interaction

Record constraints that restrict satisfying the scenario.

Example:

```text
mandatory external provider
single-region policy
fixed budget
legacy client compatibility
```

Do not choose tactics.

# Step 28 — Assumptions

Architecture-significant assumptions should remain visible.

Example:

```text
provider outage expected to be transient
```

If unsupported, keep as assumption with validation needed.

# Step 29 — External Dependency Feasibility

If scenario depends on provider behavior, flag whether the provider can support it.

Use:

```text
SUPPORTED
AT_RISK
UNKNOWN
```

Do not claim feasibility without evidence.

# Step 30 — Scenario Conflict

If two scenarios impose incompatible responses/measures:

```text
QUALITY_SCENARIO_CONFLICT_REQUIRES_DECISION
```

Do not resolve silently.

# Step 31 — Architecture Tactic Leakage Audit

Remove premature tactics:

```text
cache
replica
queue
circuit breaker
active-active
sharding
CQRS
microservices
Kubernetes
CDN
```

unless already an accepted constraint.

The scenario should describe the required quality outcome.

# Step 32 — Completeness Audit

For every scenario verify:

```text
source
stimulus
environment
artifact
response
response measure
traceability
status
```

# Step 33 — Scenario Testability

Ask:

```text
Could a later architecture review/test determine whether this scenario is satisfied?
```

If not, identify the missing field.

# Step 34 — Scenario Set Balance

Do not generate only happy-path performance scenarios.

For systems where evidence supports it, include:

```text
normal
peak
failure
recovery
change
security/privacy
operations
```

But do not force all categories.

# Step 35 — Architecture Driver Candidate Handoff

Flag scenarios potentially architecture-significant because of:

```text
strict measure
high business criticality
large scope
cross-cutting impact
failure/recovery requirement
security/privacy boundary
external dependency
high change pressure
```

Do not decide final driver classification.

# Step 36 — Trade-Off Analysis Handoff

Provide scenario pairs/groups likely to compete.

Example:

```text
QA-AV-001
↔ QA-COST-003
```

Later:

```text
analyzing-architecture-tradeoffs
```

evaluates candidate architectures.

# Step 37 — Architecture Validation Handoff

Scenarios become validation probes.

Example:

```text
Architecture decision claims provider outage resilience.
→ validate against QA-AV-001.
```

# Final Decision

Use:

```text
QUALITY_ATTRIBUTES_READY
QUALITY_ATTRIBUTES_READY_WITH_TBDS
QUALITY_ATTRIBUTES_REQUIRE_NFR_MEASURES
QUALITY_ATTRIBUTES_REQUIRE_POLICY_DECISION
QUALITY_ATTRIBUTES_REQUIRE_SCOPE_CLARIFICATION
QUALITY_ATTRIBUTES_CONFLICTED
BLOCKED
```

# Output

Use:

```text
assets/quality-attribute-scenarios.md
```

## Completion Criteria

- [ ] NFR catalog version/status is recorded.
- [ ] Only scenario-worthy quality concerns are modeled.
- [ ] Stable scenario IDs are assigned.
- [ ] Scenario status/priority preserve authority.
- [ ] Every scenario identifies source.
- [ ] Every scenario identifies stimulus.
- [ ] Every scenario identifies environment.
- [ ] Every scenario identifies artifact.
- [ ] Every scenario identifies response.
- [ ] Every scenario identifies response measure or explicit TBD.
- [ ] Measures are never invented from convention.
- [ ] Qualitative pass/fail measures are allowed where appropriate.
- [ ] Availability scenarios model real failure/degraded contexts.
- [ ] Performance scenarios preserve load/statistic/target gaps.
- [ ] Scalability scenarios describe growth dimensions without implementation tactics.
- [ ] Reliability scenarios describe correct business behavior.
- [ ] Recoverability scenarios use only sourced RTO/RPO.
- [ ] Security scenarios describe required behavior and do not replace STRIDE.
- [ ] Privacy scenarios do not invent policy.
- [ ] Observability scenarios describe detection/diagnosis outcomes rather than tools.
- [ ] Modifiability/maintainability scenarios describe concrete changes.
- [ ] Interoperability/testability/usability/accessibility/cost scenarios are created only when supported.
- [ ] Duplicate scenarios are consolidated with traceability.
- [ ] Business criticality/priority are not invented.
- [ ] Trade-off tensions and constraint interactions are visible.
- [ ] Assumptions/dependency feasibility are explicit.
- [ ] Conflicting quality scenarios are not silently reconciled.
- [ ] Architecture tactics are removed unless accepted constraints.
- [ ] Scenario set is balanced according to actual system risks.
- [ ] Architecture-driver candidates are flagged without final classification.
- [ ] Trade-off and architecture-validation handoffs are explicit.
- [ ] Final quality-attribute readiness is explicit.
