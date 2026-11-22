---
name: reviewing-full-stack-change
description: Performs the final cross-stack review of an implemented change by validating the accepted specification, backend implementation, frontend implementation, shared API/contracts, adversarial failure modes, overlooked details, and required documentation updates. Use after backend and frontend implementation evidence exists and before merge/release when the change spans both stacks. Aggregate specialist evidence rather than duplicating backend/frontend/security/performance/testing rules; detect contract drift, ownership mismatches, incompatible error/authorization semantics, rollout hazards, and acceptance-criteria gaps that can remain invisible when each stack is reviewed in isolation. Do not implement fixes, rerun every specialist review mechanically, invent requirements, or declare the change ready when specification, contract, validation, or blocking evidence is missing.
...
---

# Reviewing Full-Stack Change

## Purpose

Perform the final integrated review of a completed full-stack change.

Roadmap workflow:

```text
validate specification
→ validate backend
→ validate frontend
→ validate API contract
→ adversarial review
→ detail analysis
→ documentation update
```

This skill answers:

```text
Does the implemented backend + frontend change,
as one system,
actually satisfy the accepted specification and shared contract?
```

It is not a replacement for stack-specific review.

## Core Principle

```text
backend individually correct
+
frontend individually correct
≠
full-stack integration correct
```

The cross-stack review must verify the seams.

## Use When

- A backend + frontend change is implemented and ready for final review.
- A PR spans API, backend behavior, and frontend behavior.
- Stack-specific validations exist but integration confidence is still needed.
- A shared contract changed.
- A rollout includes compatibility/migration concerns.
- A critical user journey crosses both stacks.
- Final adversarial and detail analysis are required before release.
- Documentation may need synchronization after implementation.

## Do Not Use When

- The change is frontend-only.
- The change is backend-only.
- Implementation is not complete enough to review.
- The specification/acceptance criteria are unavailable.
- The task is to prepare the change before implementation.
- The user wants code fixes rather than review.
- The task is only mechanical validation.
- The task is only security/performance review.

## Inputs

- Accepted specification/OpenSpec change.
- Acceptance criteria.
- Full-stack preparation record if available.
- Backend implementation/diff.
- Frontend implementation/diff.
- Backend validation/review artifacts.
- Frontend validation/review artifacts.
- API/request/response/error contracts.
- Contract tests/runtime validation evidence.
- Security/privacy/performance evidence when triggered.
- Mechanical validation evidence.
- Documentation state.
- Applicable `AGENTS.md`.

## Outputs

- Specification validation result.
- Backend validation aggregation.
- Frontend validation aggregation.
- API-contract compatibility result.
- Cross-stack integration findings.
- Adversarial review findings.
- Detail-analysis findings.
- Documentation update requirements.
- Acceptance-criteria traceability matrix.
- Release/readiness decision.
- Full-stack review record.

# Orchestrator Boundary

This skill owns:

```text
cross-stack evidence aggregation
spec-to-implementation traceability
contract seam review
integration inconsistency detection
final adversarial challenge
detail completeness analysis
documentation synchronization decision
readiness conclusion
```

It does NOT own detailed specialist policy.

# Focused Skills / Evidence Sources

Potential specification validation:

```text
validating-changes
```

Potential backend evidence:

```text
validating-backend-change
reviewing-backend-code
reviewing-backend-architecture
```

Potential frontend evidence:

```text
validating-frontend-architecture
reviewing-frontend-architecture
reviewing-web-accessibility
```

Potential cross-cutting:

```text
reviewing-adversarially
analyzing-details
updating-documentation
```

Risk-specific evidence when triggered:

```text
reviewing-application-security
verifying-security-controls
reviewing-frontend-security
reviewing-frontend-performance
reviewing-frontend-privacy-and-analytics
analyzing-algorithmic-complexity
```

Do not reimplement these skills inside this orchestrator.

# Readiness Gate

Before final full-stack review require:

```text
accepted specification
backend implementation scope
frontend implementation scope
shared contract
stack-specific validation evidence
```

Use:

```text
READY_TO_REVIEW_FULL_STACK_CHANGE
READY_WITH_CONDITIONS
SPECIFICATION_REQUIRED
BACKEND_EVIDENCE_REQUIRED
FRONTEND_EVIDENCE_REQUIRED
CONTRACT_EVIDENCE_REQUIRED
RISK_REVIEW_REQUIRED
BLOCKED
```

# Step 1 — Validate Specification

Use:

```text
validating-changes
```

or equivalent accepted specification-validation evidence.

Confirm:

```text
accepted change exists
requirements are internally consistent
implementation scope matches accepted delta
no unresolved blocking spec question remains
```

Do not review implementation against an unvalidated or stale spec.

# Spec Drift

Detect:

```text
implementation added behavior not in spec
implementation omitted accepted behavior
spec still describes old contract
acceptance criterion changed informally
```

Classify:

```text
SPEC_IMPLEMENTATION_ALIGNED
SPEC_DRIFT_IMPLEMENTATION_AHEAD
SPEC_DRIFT_SPEC_AHEAD
SPEC_CONFLICT
```

# Step 2 — Validate Backend Evidence

Consume stack-specific evidence rather than reproducing backend review.

Minimum relevant signals:

```text
backend change validation
backend architecture validation/review
backend code review for meaningful changes
tests/build/runtime evidence
security/performance evidence when triggered
```

Record:

```text
PASS
PASS_WITH_FINDINGS
FAIL
NOT_AVAILABLE
```

# Backend Blocking Findings

Any unresolved backend finding that can violate:

- accepted behavior;
- data integrity;
- authorization;
- idempotency;
- compatibility;
- provider semantics;
- public API;

blocks full-stack readiness.

# Step 3 — Validate Frontend Evidence

Consume:

```text
frontend architecture validation
frontend architecture review
frontend tests
accessibility review
security/privacy/performance review when triggered
```

Record evidence and unresolved findings.

# Frontend Blocking Findings

Block when unresolved issues can violate:

- accepted UI behavior;
- API interpretation;
- authorization assumptions;
- accessibility requirement;
- critical journey;
- security/privacy requirement;
- compatibility;
- runtime correctness.

# Step 4 — Validate API / Shared Contract

This is a primary responsibility of this skill.

Compare:

```text
accepted contract
backend producer
frontend consumer
tests/mocks
runtime schema
docs
```

for exact semantic compatibility.

# Contract Dimensions

Review as applicable:

```text
method/path
request shape
response shape
required/optional fields
enum values
nullability
status codes
error codes
authorization semantics
idempotency
pagination
sorting/filtering
redirect/callback
webhook/event
date/time format
money/precision
locale/timezone assumptions
```

# Producer / Consumer Matrix

For every contract element ask:

```text
spec says?
backend emits/accepts?
frontend sends/expects?
test fixture says?
docs say?
```

Any disagreement is contract drift.

# DTO Compatibility

Check:

```text
field name
type
required/optional
nullability
semantic meaning
default
unknown fields
version
```

Do not treat TypeScript compile success as cross-stack contract proof.

# Runtime Validation

If frontend standard requires runtime validation of external data, confirm it matches the backend response.

A runtime schema that rejects valid backend output is a full-stack defect.

A schema that accepts impossible unsafe variants may weaken correctness.

# Error Contract

Verify exact consumer-relevant errors.

Example:

```text
backend:
409 UPGRADE_CONFLICT

frontend:
expects 422 INVALID_PLAN
```

Both implementations may be locally coherent but integration is broken.

# Authorization Contract

Verify:

```text
backend authoritative rule
frontend UX behavior
negative server evidence
frontend handling of 401/403
tenant/resource ownership
```

Do not accept matching hidden-button behavior as proof of server authorization.

# Idempotency Contract

For retryable mutations verify:

```text
client sends key/token if required
backend interprets it consistently
retry behavior is safe
UI does not duplicate side effects
```

# Redirect / Callback Contract

Verify:

```text
backend response field
frontend navigation
provider callback
cancel flow
success flow
state/correlation
```

Avoid dead-end states where each stack assumes the other handles continuation.

# Pagination Contract

Check:

```text
cursor/page semantics
sort order
filter encoding
empty page
next token
total count
```

# Date / Time Contract

Verify:

```text
timezone
UTC/local
ISO representation
date-only semantics
DST-sensitive behavior
```

# Money Contract

Verify:

```text
integer minor units vs decimal
currency
rounding
locale only in presentation
```

Do not let frontend infer financial semantics from formatted strings.

# Feature Flags / Rollout Contract

If rollout is coordinated:

```text
backend supports old/new client
frontend flag behavior
default
mixed-version compatibility
removal condition
```

# Compatibility Review

Consume preparation decisions and verify actual implementation.

Classify:

```text
ADDITIVE
BACKWARD_COMPATIBLE
BREAKING
MIGRATION_REQUIRED
```

Then verify deployment sequence remains safe.

# Mixed-Version Window

Ask:

```text
old frontend + new backend?
new frontend + old backend?
```

If rolling deploy can produce either combination, verify safe behavior or enforce ordering.

# Database / Migration Seam

Review only cross-stack impact:

```text
does API remain compatible during migration?
does frontend encounter transitional null/old values?
```

Detailed DB correctness belongs to backend/infra review.

# Mocks / Fixtures

Compare frontend mocks to actual accepted/backend contract.

Flag:

```text
MOCK_CONTRACT_DRIFT
```

when mocks hide an integration problem.

# Step 5 — Cross-Stack Journey Trace

For critical ACs trace:

```text
user action
→ frontend state
→ request
→ backend controller
→ application/domain behavior
→ persistence/provider
→ response/error
→ frontend interpretation
→ final user-visible state
```

Do not rely on one E2E test as the only proof; use it as integration evidence.

# Acceptance Criteria Traceability

Every AC must map to:

```text
spec
backend evidence
frontend evidence
contract evidence
cross-stack journey evidence if required
```

No orphan ACs.

# Step 6 — Adversarial Review

Delegate/compose:

```text
reviewing-adversarially
```

Focus on cross-stack failure modes.

Relevant lenses:

```text
retry/replay
partial backend success
frontend timeout after server commit
stale frontend state
double submit
provider callback reordered
old/new version mix
authorization mismatch
error mapping mismatch
network cancellation
race/concurrency
rollback
```

Do not duplicate the generic adversarial skill; pass it the full-stack contract and evidence.

# Cross-Stack Adversarial Cases

Examples:

```text
backend succeeds
→ response lost
→ frontend retries
→ duplicate mutation?
```

```text
frontend optimistic state
→ backend rejects
→ rollback correct?
```

```text
provider succeeds
→ callback delayed
→ frontend return route loads stale state
```

# Step 7 — Detail Analysis

Delegate/compose:

```text
analyzing-details
```

Use it to detect overlooked propagation.

Typical full-stack details:

```text
enum added backend but missing frontend label
new error missing translation
new field missing mock
new permission missing route state
new endpoint missing API docs
new event missing analytics schema
new env/config missing deployment docs
old field still referenced in tests
```

# Detail vs Defect

Do not invent requirements.

A missing detail is actionable only when required by accepted behavior, contract, repository rule, or existing convention.

# Step 8 — Documentation Update

Determine whether docs are stale.

Potential affected surfaces:

```text
OpenSpec
API docs
README
runbook
architecture docs
environment/config docs
migration/deployment docs
analytics catalog
security notes
examples
```

If changes are required, delegate:

```text
updating-documentation
```

Do not manually patch generated docs when source/generator exists.

# Documentation Gate

Final status may be:

```text
DOCS_NOT_REQUIRED
DOCS_UPDATE_REQUIRED
DOCS_UPDATED
DOCS_BLOCKED
```

# Specialist Finding Aggregation

Do not copy entire specialist reports.

Aggregate only:

```text
finding ID/source
severity/priority
blocking?
cross-stack impact
status
```

# Duplicate Findings

If backend/frontend/security reviewers identify the same root issue:

```text
consolidate
→ preserve source references
```

Do not inflate issue count.

# Finding Ownership

Assign remediation owner:

```text
BACKEND
FRONTEND
SHARED_CONTRACT
FULL_STACK
INFRASTRUCTURE
SECURITY
PRODUCT
DOCUMENTATION
THIRD_PARTY
```

# Cross-Stack Finding Format

Each material finding:

```text
ID
title
source/evidence
spec/AC
backend state
frontend state
contract mismatch
user/system impact
severity
owner
required fix
verification
```

# Severity

Use specialist severity where already established.

For integration-only findings use:

```text
BLOCKING
HIGH
MEDIUM
LOW
ADVISORY
```

based on:

```text
accepted behavior failure
data/security impact
critical journey
compatibility
blast radius
recoverability
```

# Final Readiness

Use:

```text
FULL_STACK_CHANGE_ACCEPTABLE
FULL_STACK_CHANGE_ACCEPTABLE_WITH_CONDITIONS
FULL_STACK_CHANGE_REQUIRES_FIXES
FULL_STACK_CHANGE_REQUIRES_CONTRACT_REPAIR
FULL_STACK_CHANGE_REQUIRES_SPEC_UPDATE
FULL_STACK_CHANGE_REQUIRES_DOCUMENTATION
FULL_STACK_CHANGE_REQUIRES_RISK_REVIEW
FULL_STACK_CHANGE_REVIEW_INCOMPLETE
BLOCKED
```

# Mechanical Validation Boundary

Mechanical commands such as:

```text
lint
typecheck
tests
build
format
```

should come from existing validation evidence / Validator Agent.

This skill does not equate passing commands with quality.

# Validator Agent Handoff

If final command execution is still missing:

```text
validator-agent
```

may be required before readiness.

Record:

```text
MECHANICAL_VALIDATION_PENDING
```

# Reviewer Agent Boundary

This orchestration can feed the future Reviewer Agent.

It aggregates stack review evidence but should remain reusable independently.

# Security Review

If preparation/implementation triggered security and evidence is missing:

```text
RISK_REVIEW_REQUIRED
```

Do not silently waive because functional tests pass.

# Performance Review

If accepted budget or known hot path was part of scope, unresolved performance evidence blocks according to accepted requirement.

Do not trigger performance ritual for every change.

# Privacy Review

Consent/analytics changes require relevant privacy evidence before completion.

# Architecture Validation

A cross-stack change can pass functional E2E while violating stack architecture.

Consume stack architecture validation.

Do not substitute E2E for architecture evidence.

# Test Quality

Passing tests do not prove appropriate test strategy.

Consume focused testing records/reviews when the change risk requires it.

# Review Ordering

Recommended:

```text
specification
→ backend evidence
→ frontend evidence
→ contract seam
→ critical journeys
→ adversarial
→ detail
→ docs
→ readiness
```

Do not run adversarial review before intended behavior/contract is established.

# Parallel Review

Backend and frontend evidence collection can happen in parallel if implementations are stable.

Contract seam review waits until both sides are available.

Adversarial/detail review should consume the integrated view.

# Reopen Contract Decision

When contract mismatch is found:

```text
do not pick frontend/backend winner silently
→ identify authoritative accepted contract
→ if contract itself wrong/ambiguous, reopen specification/shared decision
```

# Reopen Specification

If implementation evidence proves spec impossible or contradictory:

```text
SPEC_DECISION_REQUIRED
```

Do not “fix” the spec during review without an accepted decision.

# Scope Control

Review only the accepted change plus materially affected seams.

Do not turn final review into repository-wide audit.

# Pre-Existing Debt

Classify:

```text
PRE_EXISTING_NOT_WORSENED
PRE_EXISTING_WORSENED
CHANGE_INTRODUCED
CHANGE_REQUIRED_TO_FIX
```

Only relevant debt should affect readiness.

# No Style Nitpicking

Do not block on:

- naming preference;
- formatting already enforced;
- optional refactors;
- unrelated cleanup.

# Full-Stack Review Workflow

```text
1. establish authoritative spec and scope
2. load backend evidence
3. load frontend evidence
4. compare shared contracts
5. trace acceptance criteria
6. trace critical end-to-end journeys
7. run adversarial review
8. run detail analysis
9. reconcile duplicate findings
10. identify docs updates
11. confirm mechanical/risk evidence
12. issue readiness decision
```

# Final Decision Requirements

Before `FULL_STACK_CHANGE_ACCEPTABLE`:

- accepted spec valid;
- backend required evidence acceptable;
- frontend required evidence acceptable;
- shared contract aligned;
- all ACs covered;
- blocking adversarial findings resolved;
- blocking detail omissions resolved;
- required docs updated;
- required mechanical validation available;
- required risk reviews complete.

# Completion Criteria

- [ ] Accepted specification/OpenSpec is identified.
- [ ] Specification validation evidence exists.
- [ ] Implementation is reviewed against the accepted spec, not memory.
- [ ] Backend validation/review evidence is consumed.
- [ ] Frontend validation/review evidence is consumed.
- [ ] Specialist reports are aggregated rather than duplicated.
- [ ] API/shared contract is compared across spec, backend, frontend, mocks/tests, and docs.
- [ ] Method/path and request semantics align.
- [ ] Response field/type/nullability/meaning align.
- [ ] Consumer-relevant error codes/statuses align.
- [ ] Authorization semantics align with backend authority.
- [ ] Idempotency/retry semantics align where relevant.
- [ ] Redirect/callback/provider flow aligns where relevant.
- [ ] Pagination/date/time/money semantics align where relevant.
- [ ] Runtime validation matches accepted backend output.
- [ ] Frontend mocks/fixtures do not drift from contract.
- [ ] Mixed-version/deployment compatibility is reviewed where relevant.
- [ ] Every acceptance criterion maps to backend/frontend/contract evidence.
- [ ] Critical cross-stack journeys are traced.
- [ ] Adversarial review is performed for material changes.
- [ ] Detail analysis checks propagation/completeness.
- [ ] Duplicate root-cause findings are consolidated.
- [ ] Pre-existing debt is distinguished from change-introduced issues.
- [ ] Required security/privacy/performance evidence is present when triggered.
- [ ] Mechanical validation evidence is present or explicitly pending.
- [ ] Documentation impact is assessed.
- [ ] Required documentation is updated through `updating-documentation`.
- [ ] No unresolved blocking specification/contract/finding remains.
- [ ] Final full-stack readiness status is explicit.
