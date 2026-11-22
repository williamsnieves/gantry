---
name: implementing-frontend-change
description: Portable engineering capability `implementing-frontend-change`. Use when
  the harness or a specialist agent explicitly requires this named capability.
---
# Implementing Frontend Change

## Purpose

Orchestrate a complete frontend implementation using the existing focused skill system.

Roadmap workflow:

```text
apply standard
→ classify profile
→ plan vertical slices
→ select domain/application work
→ implement adapters
→ implement hooks/components
→ apply styling profile
→ test
→ validate accessibility and architecture
→ review
```

This skill MUST delegate to focused skills rather than embed all detailed rules.

## Core Principle

```text
orchestrator
→ decides what work is needed
→ selects focused skill
→ passes bounded context
→ consumes structured output
→ updates implementation state
```

Not:

```text
orchestrator
→ contains every frontend rule
→ performs every specialist task itself
```

## Use When

- Implementing a new frontend feature end to end.
- Implementing a significant frontend user story.
- Applying a frontend bug fix that crosses multiple layers.
- Implementing a frontend refactor requiring multiple specialist skills.
- Implementing a vertical slice after an OpenSpec/user-story plan.
- Coordinating Domain/Application/Infrastructure/React work.
- Coordinating frontend testing and validation.
- Preparing a frontend change for review.
- Coordinating focused security/performance/privacy checks when the change warrants them.

## Do Not Use When

- The user needs only one focused task.
- The task is only component design.
- The task is only a security review.
- The task is only architecture validation.
- The task is only frontend performance investigation.
- The change is not sufficiently specified to identify acceptance criteria or scope.
- A full-stack change has significant backend/API sequencing that should use `preparing-full-stack-change`.
- The task is final cross-stack review; use `reviewing-full-stack-change`.

## Inputs

- User story / change request.
- Acceptance criteria.
- OpenSpec change/spec if available.
- Repository-local `AGENTS.md`.
- Frontend engineering standard.
- Existing architecture profile/decision register.
- Current frontend architecture.
- Existing feature boundaries.
- API/contracts relevant to the change.
- Styling/design-system profile.
- Existing tests.
- Security/privacy/performance constraints where known.
- Repository validation commands.
- Delivery constraints.

## Outputs

- Frontend change implementation plan.
- Skill-routing decision.
- Ordered execution graph.
- Handoff contracts.
- Implementation-state ledger.
- Test/validation plan.
- Risk-triggered specialist reviews.
- Completion/readiness decision.
- Frontend change orchestration record.

# Orchestrator Responsibilities

This skill owns:

```text
scope
sequence
routing
handoffs
readiness gates
dependency ordering
evidence aggregation
completion decision
```

It does NOT own detailed specialist policy.

# Focused Skill Registry

The orchestrator may delegate to:

## Standard / Architecture

```text
applying-frontend-engineering-standard
classifying-frontend-architecture-profile
planning-frontend-vertical-slices
validating-frontend-architecture
reviewing-frontend-architecture
```

## Domain / Application

```text
modeling-frontend-domain
designing-frontend-use-cases
designing-frontend-dtos-and-view-data
designing-frontend-ports
```

## Infrastructure / Data

```text
implementing-frontend-http-clients
validating-external-frontend-data
modeling-frontend-async-state
implementing-frontend-repository-adapters
integrating-frontend-server-state
composing-frontend-dependencies
```

## React / UI

```text
designing-react-components
designing-react-custom-hooks
designing-react-effects
composing-react-feature-containers
```

## Styling

```text
selecting-frontend-styling-profile
implementing-css-modules-ui
implementing-tailwind-ui
integrating-headless-ui-primitives
designing-component-variants
designing-responsive-layouts
managing-frontend-design-tokens
```

## Accessibility

```text
designing-accessible-web-interfaces
designing-accessible-forms
reviewing-web-accessibility
```

## Testing

```text
planning-frontend-test-strategy
testing-frontend-domain-and-use-cases
testing-frontend-adapters
testing-react-hooks
testing-react-components
testing-frontend-visual-regressions
testing-frontend-user-journeys
```

## Quality / Risk

```text
reviewing-frontend-performance
reviewing-frontend-security
reviewing-frontend-privacy-and-analytics
analyzing-algorithmic-complexity
```

## Brownfield / Refactoring

```text
migrating-to-frontend-vertical-slices
refactoring-react-features
```

## Cross-Cutting Security

When triggered:

```text
threat-modeling-with-stride
reviewing-application-security
verifying-security-controls
```

The exact registry may evolve, but routing should remain explicit.

# Skill Selection Rule

Do not invoke every skill.

Use:

```text
change needs concern
→ invoke focused skill
```

Skip irrelevant skills explicitly.

Example:

```text
simple presentational change
→ no Domain modeling
→ no repository adapter
→ no E2E
→ maybe component + styling + accessibility + component test
```

# Change Classification

First classify:

```text
NEW_FEATURE
FEATURE_EXTENSION
BUG_FIX
REFACTOR
MIGRATION
ACCESSIBILITY_CHANGE
PERFORMANCE_CHANGE
SECURITY_CHANGE
PRIVACY_ANALYTICS_CHANGE
VISUAL_CHANGE
DATA_INTEGRATION_CHANGE
```

Multiple classifications may apply.

# Readiness Gate

Before orchestration begins, verify:

```text
scope known
acceptance criteria known
repository available
standard available
architecture profile known or classifiable
contracts known enough
```

Use:

```text
READY_TO_IMPLEMENT_FRONTEND_CHANGE
READY_WITH_CONDITIONS
REQUIREMENTS_REQUIRED
ACCEPTANCE_CRITERIA_REQUIRED
ARCHITECTURE_PROFILE_REQUIRED
API_CONTRACT_REQUIRED
DESIGN_CONTRACT_REQUIRED
SECURITY_DECISION_REQUIRED
BLOCKED
```

# Step 1 — Apply Frontend Engineering Standard

Delegate:

```text
applying-frontend-engineering-standard
```

Goal:

- identify applicable standard rules;
- identify project overrides;
- identify non-negotiable constraints;
- avoid loading irrelevant rules.

Output becomes orchestration context.

# Step 2 — Classify Architecture Profile

If already explicitly accepted:

```text
reuse accepted profile
```

Otherwise delegate:

```text
classifying-frontend-architecture-profile
```

Do not assume Profile C for every feature.

# Profile Impact

Profile influences:

```text
Domain/Application layers
ports/adapters
composition
testing boundaries
public feature surfaces
```

The orchestrator must retain this decision throughout the workflow.

# Step 3 — Plan Vertical Slice

Delegate:

```text
planning-frontend-vertical-slices
```

Output should identify:

```text
capability
feature owner
route/screen
Domain/Application/Infrastructure/UI work
public surface
tests
dependencies
```

For brownfield structural migration, use:

```text
migrating-to-frontend-vertical-slices
```

instead.

# Step 4 — Select Domain/Application Work

Do not invoke Domain skills mechanically.

Ask:

```text
Does this change contain business concepts/invariants?
Does it contain framework-independent orchestration?
Does it need explicit DTO/view-data mapping?
Does it need a port?
```

Potential routing:

```text
business invariant
→ modeling-frontend-domain

application workflow
→ designing-frontend-use-cases

API→UI transformation
→ designing-frontend-dtos-and-view-data

external capability dependency
→ designing-frontend-ports
```

# Simple Feature Rule

A simple Profile A feature may need none of these.

Do not create ceremonial Domain/Application artifacts.

# Step 5 — Plan Infrastructure

Select only required infrastructure skills.

Potential:

```text
HTTP endpoint
→ implementing-frontend-http-clients

external payload trust boundary
→ validating-external-frontend-data

repository abstraction needed
→ implementing-frontend-repository-adapters

remote lifecycle
→ modeling-frontend-async-state
→ integrating-frontend-server-state

dependency construction
→ composing-frontend-dependencies
```

# Direct API Boundary

Do not let components bypass accepted infrastructure strategy.

The orchestrator should catch a plan that says:

```text
component → fetch
```

when repository standard requires a different boundary.

# Step 6 — Plan React Layer

Potential routing:

```text
component contract
→ designing-react-components

custom React behavior
→ designing-react-custom-hooks

Effect/external synchronization
→ designing-react-effects

feature route/container wiring
→ composing-react-feature-containers
```

Do not force a custom hook for every component.

# Step 7 — Apply Styling Profile

If styling approach is already established:

```text
reuse accepted profile
```

Otherwise:

```text
selecting-frontend-styling-profile
```

Then route only to relevant implementation skill:

```text
CSS Modules
→ implementing-css-modules-ui

Tailwind
→ implementing-tailwind-ui

headless primitive
→ integrating-headless-ui-primitives
```

Use variants/responsive/tokens skills only when needed.

# Step 8 — Accessibility by Design

Accessibility is not a final lint step.

During design/implementation route:

```text
interactive UI
→ designing-accessible-web-interfaces

form
→ designing-accessible-forms
```

Then later:

```text
reviewing-web-accessibility
```

for verification/review.

# Step 9 — Plan Tests

Delegate:

```text
planning-frontend-test-strategy
```

The output decides the lowest reliable test boundaries.

Potential execution:

```text
Domain/Application
→ testing-frontend-domain-and-use-cases

Infrastructure adapter
→ testing-frontend-adapters

Hook
→ testing-react-hooks

Component
→ testing-react-components

visual contract
→ testing-frontend-visual-regressions

critical cross-boundary journey
→ testing-frontend-user-journeys
```

Do not create all test types automatically.

# Testing Order

Prefer:

```text
lowest reliable boundary first
→ broader integration only where risk requires
```

Do not duplicate the same behavior across every layer.

# Step 10 — Risk Triggers

Run specialist reviews only when triggered.

## Performance Trigger

Examples:

```text
large collection
chart
large dependency
route bundle
high-frequency interaction
expensive transform
network duplication
```

→

```text
reviewing-frontend-performance
```

If computational scaling is material:

```text
analyzing-algorithmic-complexity
```

## Security Trigger

Examples:

```text
auth/session
HTML rendering
browser secret
redirect
upload
third-party script
privileged UI
new trust boundary
```

→

```text
reviewing-frontend-security
```

and when broader taxonomy/control work is required:

```text
reviewing-application-security
verifying-security-controls
```

If architecture changes trust boundaries:

```text
threat-modeling-with-stride
```

## Privacy Trigger

Examples:

```text
analytics
telemetry
consent
user identifiers
session replay
third-party analytics SDK
```

→

```text
reviewing-frontend-privacy-and-analytics
```

# Step 11 — Architecture Validation

After implementation structure stabilizes:

```text
validating-frontend-architecture
```

This is mandatory for meaningful architecture-affecting changes.

For trivial styling/text changes it may be skipped with rationale.

# Step 12 — Accessibility Review

For interactive/UI changes:

```text
reviewing-web-accessibility
```

Consume findings before final review.

# Step 13 — Final Architecture Review

For meaningful feature/change scope:

```text
reviewing-frontend-architecture
```

Use as design/code review, not as implementation driver.

# Orchestration Graph

Represent dependencies explicitly.

Example:

```text
apply-standard
      ↓
classify-profile
      ↓
plan-slice
  ┌───┼────────┐
  ↓   ↓        ↓
domain app   infrastructure
  └───┼────────┘
      ↓
react/ui
      ↓
styling/accessibility
      ↓
tests
      ↓
risk reviews
      ↓
architecture validation
      ↓
final review
```

Parallelize only independent branches.

# Parallel Work

Potential parallel work:

```text
Domain model
+
DTO contract analysis
```

if dependencies are clear.

Potential:

```text
component contract
+
adapter implementation
```

only if the view/data contract is stable.

Do not parallelize work whose upstream contract is unresolved.

# Dependency Gate

Example:

```text
DTO/view-data contract unresolved
→ component implementation blocked
```

Do not let parallel agents invent incompatible shapes.

# Handoff Contract

Every skill handoff should contain:

```text
goal
scope
inputs
decisions already fixed
open questions
expected artifact
acceptance criteria
downstream consumers
```

# Handoff Minimality

Send only needed context.

Do not dump entire repository history into every specialist.

# Decision Ledger

Track important decisions:

```text
architecture profile
feature ownership
Domain/Application presence
port/repository decision
server-state owner
styling profile
accessible primitive
test boundary
security/privacy/performance requirements
```

Downstream skills should consume, not re-decide, accepted decisions unless evidence requires escalation.

# Decision Conflict

If a focused skill finds a conflict with an upstream decision:

```text
do not silently override
→ return decision conflict
→ reopen owning decision
```

# Evidence Ledger

Track:

```text
artifact
skill
status
finding
required follow-up
```

Example:

```text
frontend-test-strategy.md
→ planning-frontend-test-strategy
→ READY
```

# State Machine

Use orchestration states:

```text
PLANNING
IMPLEMENTING
TESTING
VALIDATING
REVIEWING
BLOCKED
READY
```

# Task State

Each task:

```text
PENDING
READY
IN_PROGRESS
DONE
BLOCKED
SKIPPED_WITH_REASON
FAILED
```

# Skip Reason

Skipped skills must record why.

Good:

```text
modeling-frontend-domain
→ skipped: no business invariant; simple presentation mapping only
```

Bad:

```text
skipped
```

# Failure Handling

If specialist returns blocker:

```text
stop dependent tasks
→ update state
→ route to required upstream skill
```

Example:

```text
testing adapter
→ contract ambiguous
→ reopen DTO/port/adapter decision
```

# No Silent Scope Growth

If implementation reveals new capability:

```text
record scope change
→ request/accept new scope
→ replan affected tasks
```

Do not absorb unbounded cleanup.

# Brownfield Change

If existing feature violates architecture, distinguish:

```text
required for this change
pre-existing debt
optional cleanup
```

Use `refactoring-react-features` or migration skill only when necessary.

# Refactor Trigger

Use:

```text
refactoring-react-features
```

when implementation is blocked or made unsafe by:

- god hook;
- oversized mixed component;
- direct fetch;
- duplicated async state;
- inaccessible widget;
- shared abstraction overreach.

Do not refactor unrelated code opportunistically.

# Migration Trigger

Use:

```text
migrating-to-frontend-vertical-slices
```

when capability ownership itself must change.

# Existing Architecture Adaptation

If repo is legacy and standard cannot be applied directly, use appropriate adaptation/migration skills.

Do not force target architecture in one change.

# Implementation Sequence

A typical feature sequence:

```text
1. standard/profile
2. slice plan
3. contracts
4. Domain/Application
5. Infrastructure
6. server-state
7. hooks/container
8. components
9. styling/accessibility
10. tests
11. risk reviews
12. validation
13. review
```

Adapt according to actual dependency graph.

# Inside-Out Preference

When business/application complexity exists, prefer:

```text
Domain/Application
→ Infrastructure
→ React/UI
```

because inner contracts stabilize outer implementation.

For simple UI-only changes, this is unnecessary.

# User Story Traceability

Map acceptance criteria to implementation/test evidence.

Example:

| Acceptance criterion | Implementation owner | Test evidence |
|---|---|---|
| user sees upgrade eligibility | Application + UI | use-case + component |
| invalid upgrade shows conflict | adapter/use-case/UI | adapter + component |
| keyboard can select plan | UI | component/accessibility |

# Acceptance Criteria Coverage

Before completion:

```text
every AC
→ implementation evidence
→ test/validation evidence
```

No orphan acceptance criteria.

# OpenSpec Traceability

If OpenSpec change exists:

```text
delta/spec requirement
→ frontend slice/task
→ implementation
→ verification
```

Do not reinterpret spec silently.

# API Contract Traceability

Record:

```text
endpoint
request DTO
response DTO
runtime validation
error mapping
consumer
```

If backend contract changes are required, escalate to full-stack orchestration.

# Styling Traceability

Record:

```text
accepted styling profile
tokens/primitives
responsive behavior
variants
```

Do not let implementation choose a new styling system ad hoc.

# Accessibility Traceability

For relevant AC:

```text
semantic element/pattern
keyboard behavior
focus
accessible name/status
test/review evidence
```

# Performance Budget Trigger

If requirements include performance budget:

```text
route bundle
interaction latency
large dataset
CWV
```

performance review becomes required, not optional.

# Security Trigger Matrix

| Change | Security skill |
|---|---|
| raw HTML | frontend security |
| token/session | frontend + app security |
| upload | frontend + app security/control verification |
| redirect | frontend security |
| new provider | STRIDE + security/privacy as relevant |
| privileged operation | app security + control verification |

# Privacy Trigger Matrix

| Change | Privacy skill |
|---|---|
| page tracking | privacy/analytics |
| form telemetry | privacy/analytics |
| user ID | privacy/analytics |
| session replay | privacy/analytics + security if script risk |
| third-party SDK | privacy + security where applicable |

# Completion Gate

Do not mark complete until:

```text
accepted scope implemented
acceptance criteria covered
required tests pass
required architecture validation passes
required accessibility review addressed
required risk reviews addressed
no unresolved blocking finding
```

# Validation Commands

The orchestrator records repository-approved commands but does not replace Validator Agent execution.

Possible:

```text
lint
format/check
typecheck
unit/integration
build
E2E
architecture checks
```

# Validator Agent Boundary

Later orchestration may hand final command execution to:

```text
validator-agent
```

The Validator confirms:

```text
nothing broken
```

It does not judge test quality or architecture quality.

# Reviewer Boundary

Final Reviewer Agent later aggregates:

- code review;
- architecture review;
- QA;
- security;
- performance;
- detail analysis.

This skill prepares frontend implementation evidence for that flow.

# Implementation Artifact

Maintain a structured orchestration record instead of scattered notes.

# Finding / Blocker Severity

Use:

```text
BLOCKING
HIGH
MEDIUM
LOW
ADVISORY
```

for orchestration priority, not specialist domain severity.

# Change Risk

Classify overall change:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

Inputs:

- critical journey;
- auth/security;
- data mutation;
- architecture change;
- external integration;
- performance;
- breadth;
- test coverage.

# Low-Risk Change

Example:

```text
copy/style change
→ existing component
→ no behavior
```

Possible minimal path:

```text
standard
→ component/styling
→ component/visual/accessibility validation
```

# High-Risk Change

Example:

```text
subscription upgrade flow
+ payment provider
+ permissions
+ analytics
```

Likely requires:

```text
Domain/Application
Infrastructure
React
testing layers
security
privacy
E2E
architecture review
```

# No Mechanical Orchestration

Do not create a 30-skill plan because 30 skills exist.

The goal is:

```text
smallest complete skill graph
```

# Delegation Audit

For every specialist concern ask:

```text
Did the orchestrator delegate
or accidentally reimplement detailed policy?
```

If reimplemented, move details back to focused skill/reference.

# Missing Skill

If a required concern has no focused skill:

```text
MISSING_CAPABILITY
```

Record it explicitly.

Do not hide the gap by overloading this orchestrator.

# Final Decision

Use:

```text
FRONTEND_CHANGE_READY_TO_IMPLEMENT
FRONTEND_CHANGE_IMPLEMENTATION_IN_PROGRESS
FRONTEND_CHANGE_READY_FOR_VALIDATION
FRONTEND_CHANGE_READY_FOR_REVIEW
FRONTEND_CHANGE_COMPLETE
FRONTEND_CHANGE_REQUIRES_REQUIREMENTS
FRONTEND_CHANGE_REQUIRES_ARCHITECTURE_DECISION
FRONTEND_CHANGE_REQUIRES_API_CONTRACT
FRONTEND_CHANGE_REQUIRES_SECURITY_DECISION
FRONTEND_CHANGE_BLOCKED
```

## Output

Use `assets/frontend-change-orchestration-record.md`.

## Completion Criteria

- [ ] Change scope and acceptance criteria are explicit.
- [ ] Change type/risk are classified.
- [ ] Frontend engineering standard is applied.
- [ ] Architecture profile is accepted or classified.
- [ ] Vertical slice/capability ownership is planned.
- [ ] Domain/Application work is selected only when justified.
- [ ] Infrastructure/data skills are selected only when required.
- [ ] React component/hook/effect/container skills are routed appropriately.
- [ ] Styling profile is reused or selected deliberately.
- [ ] Accessibility is designed before final validation.
- [ ] Test strategy is delegated to `planning-frontend-test-strategy`.
- [ ] Test layers are selected rather than invoked mechanically.
- [ ] Performance/security/privacy reviews are triggered by risk, not always-on ritual.
- [ ] Algorithmic complexity is delegated when computational scaling matters.
- [ ] Brownfield migration/refactoring skills are used only when scope requires.
- [ ] Architecture validation occurs after meaningful structural implementation.
- [ ] Accessibility review occurs for relevant UI behavior.
- [ ] Final architecture review occurs for meaningful changes.
- [ ] Every focused skill receives a bounded handoff contract.
- [ ] Accepted upstream decisions are preserved downstream.
- [ ] Decision conflicts reopen the owning decision rather than silently override it.
- [ ] Blockers stop dependent tasks.
- [ ] Skipped skills include explicit rationale.
- [ ] Acceptance criteria map to implementation and test/validation evidence.
- [ ] OpenSpec/API/design contracts remain traceable where applicable.
- [ ] No unresolved blocking findings remain.
- [ ] Orchestrator delegates detailed rules instead of duplicating specialist content.
- [ ] Final frontend-change state is explicit.

## References

- Read `references/frontend-change-classification-risk-and-readiness.md` first.
- Read `references/focused-skill-routing-registry.md`.
- Read `references/orchestration-graph-dependencies-and-parallelism.md`.
- Read `references/handoff-contracts-decision-ledger-and-conflicts.md`.
- Read `references/testing-accessibility-risk-review-and-validation-routing.md`.
- Read `references/brownfield-refactor-migration-and-scope-control.md`.
- Read `references/acceptance-criteria-openspec-and-evidence-traceability.md`.
- Read `references/frontend-change-orchestration-audit.md` before completion.
