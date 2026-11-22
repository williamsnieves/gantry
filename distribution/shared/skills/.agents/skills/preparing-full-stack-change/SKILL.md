---
name: preparing-full-stack-change
description: Prepares a full-stack change before implementation by enriching an incomplete request, exploring the existing OpenSpec/specification context, creating or editing the change specification, identifying backend and frontend vertical slices, stabilizing API/contracts and ownership, ordering work by dependencies, and producing bounded handoffs to stack-specific implementation skills. Use when a feature or change spans frontend and backend or when one stack depends on an unresolved contract from the other. Do not implement the feature itself, duplicate backend/frontend specialist rules, let each stack invent incompatible contracts independently, or proceed while critical specification/contract decisions remain unresolved.
...
---

# Preparing Full-Stack Change

## Purpose

Prepare a cross-stack change so frontend and backend can implement independently where possible without diverging on contracts, ownership, or acceptance criteria.

Roadmap workflow:

```text
enrich request
→ explore OpenSpec
→ create/edit change
→ identify backend and frontend slices
→ plan contracts and sequence
→ hand off to stack-specific skills
```

This skill owns preparation and orchestration.

It does not implement frontend/backend code.

## Core Principle

```text
one accepted change contract
→ backend slice
→ frontend slice
→ coordinated implementation
```

Not:

```text
frontend guesses contract
+
backend guesses contract
→ integration conflict
```

## Use When

- A feature requires coordinated frontend and backend changes.
- A user story is too vague for implementation.
- API request/response/error contracts are not yet stable.
- Both stacks need OpenSpec traceability.
- A frontend change depends on a new backend endpoint.
- A backend change changes a frontend-facing contract.
- A change introduces a new workflow spanning UI, API, domain, persistence, provider integration, or authorization.
- Work can be parallelized after shared contracts stabilize.
- A full-stack change must be decomposed into stack-specific implementation handoffs.

## Do Not Use When

- The change is frontend-only.
- The change is backend-only.
- The task is final full-stack review.
- The user only wants to enrich a story.
- The user only wants to create an OpenSpec change.
- The contracts are already finalized and stack-specific implementation is ready.
- The request is still too ambiguous to identify acceptance criteria and enrichment cannot resolve it.

## Inputs

- User request / story / bug.
- Acceptance criteria if available.
- Existing OpenSpec specs/changes.
- Repository `AGENTS.md`.
- Full-stack engineering standard.
- Backend engineering standard.
- Frontend engineering standard.
- Current API contracts.
- Current architecture.
- Backend/frontend ownership boundaries.
- Security/privacy/performance constraints.
- External-provider contracts.
- Delivery/deployment constraints.
- Migration/backward-compatibility constraints.

## Outputs

- Enriched change request.
- OpenSpec exploration findings.
- Change-spec decision: create/edit/use existing.
- Backend slice plan.
- Frontend slice plan.
- Shared contract plan.
- Dependency/sequence graph.
- Parallelization decision.
- Compatibility/migration plan.
- Stack-specific handoff artifacts.
- Full-stack preparation record.

# Orchestrator Boundary

This skill owns:

```text
cross-stack scope
shared acceptance criteria
specification ownership
contract stabilization
slice decomposition
dependency ordering
handoffs
```

It does not own:

```text
backend implementation details
frontend implementation details
specialist security/performance/testing rules
```

# Focused Skills

Potential upstream specification skills:

```text
enriching-user-stories
exploring-openspec-changes
creating-openspec-changes
editing-openspec-changes
```

Potential frontend handoff:

```text
implementing-frontend-change
```

Potential backend handoff may use:

```text
applying-backend-engineering-standard
planning-backend-vertical-slices
implementing-backend-inside-out
validating-backend-change
```

plus focused backend skills selected by the backend workflow.

Do not duplicate their specialist rules here.

# Step 1 — Enrich Request

If the request lacks implementation-grade detail, delegate to:

```text
enriching-user-stories
```

The enriched request should establish:

```text
problem
actor
goal
business outcome
acceptance criteria
constraints
edge cases
non-goals
unknowns
```

Do not invent product requirements silently.

# Enrichment Gate

Use:

```text
REQUEST_READY
REQUEST_READY_WITH_OPEN_QUESTIONS
REQUIREMENTS_REQUIRED
ACCEPTANCE_CRITERIA_REQUIRED
PRODUCT_DECISION_REQUIRED
```

Open questions that affect implementation contracts block downstream work.

# Step 2 — Explore OpenSpec

Delegate:

```text
exploring-openspec-changes
```

Determine:

```text
existing capability/spec
existing change
related deltas
conflicts
accepted terminology
existing API/business rules
```

Do not create a duplicate change if one already owns the requirement.

# OpenSpec Decision

Use:

```text
USE_EXISTING_CHANGE
EDIT_EXISTING_CHANGE
CREATE_NEW_CHANGE
NO_OPENSPEC_REQUIRED_BY_REPOSITORY
OPENSPEC_DECISION_BLOCKED
```

Follow repository policy.

# Step 3 — Create or Edit Change

If needed:

```text
creating-openspec-changes
```

or:

```text
editing-openspec-changes
```

The change must represent accepted behavior before stack-specific implementation begins.

# Specification Content

Ensure the spec/change contains enough detail for:

```text
behavior
acceptance criteria
domain terminology
API-visible behavior
failure behavior
permissions
state transitions
compatibility
```

Do not turn OpenSpec into implementation pseudocode unless repository convention requires it.

# Step 4 — Identify Full-Stack Capability

Define the end-to-end capability.

Example:

```text
subscription upgrade
```

not:

```text
POST endpoint + React modal
```

The capability owns the business journey; stack slices implement parts of it.

# Step 5 — Identify Backend Slice

Backend slice may include:

```text
Domain
Application Use Case
DTOs
ports
repositories
provider adapters
HTTP controller
composition
tests
```

Use actual backend roadmap skills downstream.

Do not decide every backend layer mechanically.

# Backend Slice Questions

Ask:

```text
new/changed invariant?
new use case?
persistence change?
external provider?
API/controller?
authorization?
migration?
```

# Step 6 — Identify Frontend Slice

Frontend slice may include:

```text
Domain/Application
DTO/view-data
HTTP/repository adapter
server state
hook/container
components
styling
accessibility
tests
```

Handoff implementation to:

```text
implementing-frontend-change
```

# Frontend Slice Questions

Ask:

```text
new route/screen?
new interaction?
new remote state?
new permissions UX?
new accessible pattern?
new analytics?
```

# Step 7 — Stabilize Shared Contract

Shared contracts may include:

```text
HTTP method/path
request DTO
response DTO
error taxonomy
status codes
authorization semantics
idempotency
pagination
sorting/filtering
provider redirect/callback
event/message contract
```

Contract ownership must be explicit.

# Contract-First Rule

When both stacks depend on the same contract:

```text
contract decision
→ backend implementation
→ frontend implementation
```

Frontend/backend may run in parallel after the contract is stable.

# Request DTO

Define:

```text
field
type
required/optional
validation semantics
business meaning
```

Do not expose persistence/provider implementation accidentally.

# Response DTO

Define stable consumer-facing semantics.

Do not force frontend to understand provider/database fields unnecessarily.

# Error Contract

Specify errors that alter frontend behavior.

Example:

```text
409 UPGRADE_CONFLICT
403 FORBIDDEN
422 INVALID_PLAN
```

Do not expose arbitrary internal exception names.

# Authorization Contract

Clarify:

```text
who may call
what resource ownership is required
where enforced
what frontend may display
```

Frontend permission checks remain UX; backend is authoritative.

# Idempotency

If operations can be retried or duplicated, decide whether idempotency is required before implementation.

Examples:

```text
payment initiation
subscription upgrade
webhook processing
```

Do not add idempotency mechanically to read-only operations.

# Pagination / Large Data

Stabilize ownership:

```text
server pagination?
client pagination?
cursor/page?
sort/filter semantics?
```

Avoid frontend implementing assumptions that backend later contradicts.

# External Provider Contract

If provider involved:

```text
backend/provider responsibility
frontend redirect responsibility
callback/return flow
provider identifiers
error/cancel flow
```

Never expose provider secret/private credentials to frontend.

# Step 8 — Compatibility

Classify contract change:

```text
ADDITIVE
BACKWARD_COMPATIBLE
BREAKING
MIGRATION_REQUIRED
```

For breaking changes define:

```text
versioning
dual-read/write
compatibility adapter
deployment order
deprecation
```

# Deployment Sequence

Potential:

```text
backend additive contract first
→ frontend consumes new contract
→ remove old backend contract later
```

This is often safer than synchronized breaking deploy.

But use actual system constraints.

# Feature Flags

Feature flags may coordinate rollout.

Define:

```text
owner
frontend/backend behavior
default
compatibility
removal
```

Do not use a frontend flag as authorization.

# Database Migration

If backend persistence changes, record:

```text
migration before/after deploy
backfill
old/new code compatibility
rollback
```

Detailed migration design belongs to backend/infra ownership.

# Step 9 — Dependency Graph

Represent:

```text
spec
↓
contract
├── backend
└── frontend
```

with finer dependencies as needed.

# Parallelization

Safe:

```text
stable request/response/error contract
→ backend adapter/controller work
+
frontend DTO/mock/adapter/UI work
```

Unsafe:

```text
response schema unresolved
→ both stacks implement independently
```

# Contract Mock

Frontend may use an approved mock/fixture based on the accepted contract.

Do not let mocks become a second undocumented contract.

# Contract Tests

Plan contract verification when valuable:

```text
backend response/schema test
frontend runtime decode test
integration/consumer-provider test
```

Do not duplicate every behavior.

# Step 10 — Risk Triggers

Cross-stack change may require:

```text
security
privacy
performance
threat modeling
algorithmic complexity
```

The preparation skill identifies triggers and assigns them to the correct stack/workflow.

It does not perform detailed review.

# Security Trigger

Examples:

```text
auth/authorization
new public endpoint
upload
webhook
payment
redirect
third-party
sensitive data
```

Potential preparation handoff:

```text
threat-modeling-with-stride
reviewing-application-security
verifying-security-controls
reviewing-frontend-security
```

# Privacy Trigger

Examples:

```text
analytics
PII
user identifier
consent
third-party tracking
```

→ frontend/privacy or broader data-governance owner.

# Performance Trigger

Examples:

```text
large list
batch endpoint
expensive aggregation
new route bundle
high request volume
```

Route downstream review appropriately.

# Step 11 — Acceptance Criteria Decomposition

Every shared AC must map to:

```text
backend responsibility
frontend responsibility
contract responsibility
verification
```

Example:

```text
"User without permission cannot upgrade"
backend:
→ authoritative 403

frontend:
→ hide/disable UX

verification:
→ backend auth test + frontend component behavior
```

# AC Ownership Types

Use:

```text
BACKEND
FRONTEND
SHARED_CONTRACT
CROSS_STACK_JOURNEY
PRODUCT
INFRASTRUCTURE
THIRD_PARTY
```

# Cross-Stack Journey

Reserve end-to-end journey evidence for critical integration behavior.

Do not use E2E as the only proof of backend/frontend rules.

# Step 12 — Produce Backend Handoff

Handoff should contain:

```text
goal
backend capability
accepted spec
request/response/error contracts
authorization
persistence/provider changes
acceptance criteria owned
dependencies
compatibility
expected backend validation
```

# Step 13 — Produce Frontend Handoff

Handoff to:

```text
implementing-frontend-change
```

Include:

```text
goal
accepted spec
frontend slice
stable API contract
view behavior
permissions UX
accessibility
analytics/privacy
acceptance criteria owned
dependencies
mock/fixture contract
```

# Handoff Minimality

Each stack receives shared context plus stack-relevant detail.

Do not dump every backend internal detail into frontend handoff.

# Stack Decision Independence

Once shared contracts are fixed, each stack should make local architecture decisions using its own standards.

Preparation should not dictate internal class/component names.

# Decision Ledger

Track:

```text
spec/change
capability
API path/method
request DTO
response DTO
error taxonomy
authorization semantics
idempotency
compatibility
deployment sequence
frontend/backend ownership
```

# Decision Conflict

If frontend/backend specialist detects a contract problem:

```text
return CONTRACT_CONFLICT
→ reopen shared contract decision
```

Do not let one stack silently change it.

# Open Questions

Classify:

```text
BLOCKING
NON_BLOCKING
PRODUCT
ARCHITECTURE
CONTRACT
THIRD_PARTY
```

Only non-blocking questions may remain when implementation handoff occurs.

# Scope Growth

If preparation reveals additional capability:

```text
record it
→ decide include/defer
```

Do not silently expand the change.

# Non-Goals

Explicit non-goals reduce cross-stack creep.

# Existing Behavior

For brownfield changes record:

```text
must preserve
intentionally change
deprecated
unknown
```

# Migration / Refactor

If stack architecture needs cleanup:

```text
backend refactor/migration skill
frontend refactor/migration skill
```

but keep cleanup bounded to what the change requires.

# Test Strategy Handoff

Preparation specifies cross-stack evidence needs, while each stack selects its detailed tests.

Potential:

```text
backend invariant test
backend use-case test
HTTP E2E
frontend adapter test
component test
critical browser journey
contract test
```

# API Contract Verification

At minimum ensure:

```text
backend produces accepted DTO/errors
frontend decodes/handles accepted DTO/errors
```

Use runtime validation where frontend standard requires it.

# Mock Drift

Mocks must derive from or be checked against accepted contract.

Flag:

```text
MOCK_CONTRACT_DRIFT
```

when fixtures diverge.

# Versioning

If API is public/external, versioning/deprecation policy may be stronger than internal API.

Do not invent versioning if repository has an established policy.

# Rollback

For high-risk changes plan:

```text
backend rollback compatibility
frontend rollback compatibility
feature flag
database/provider implications
```

# Readiness States

Use:

```text
FULL_STACK_CHANGE_READY_FOR_HANDOFF
FULL_STACK_CHANGE_READY_WITH_CONDITIONS
REQUEST_ENRICHMENT_REQUIRED
OPENSPEC_EXPLORATION_REQUIRED
OPENSPEC_CHANGE_REQUIRED
CONTRACT_DECISION_REQUIRED
BACKEND_SLICE_REQUIRED
FRONTEND_SLICE_REQUIRED
COMPATIBILITY_PLAN_REQUIRED
DEPLOYMENT_SEQUENCE_REQUIRED
PRODUCT_DECISION_REQUIRED
BLOCKED
```

# Preparation vs Implementation

This skill stops at:

```text
bounded implementation-ready handoffs
```

It does not continue into code changes.

# Preparation vs Review

After implementation, use:

```text
reviewing-full-stack-change
```

for final cross-stack validation/review.

# Minimal Change Example

Frontend needs one new optional response field.

Possible preparation:

```text
explore existing spec
→ edit change if required
→ define additive optional field
→ backend handoff
→ frontend handoff
```

No need for elaborate Domain redesign.

# Complex Change Example

Subscription upgrade with payment:

```text
enrich story
→ OpenSpec
→ upgrade capability
→ backend use case/provider/API
→ frontend interaction/state/accessibility
→ request/response/error/redirect contract
→ auth/idempotency
→ backend-first additive deploy
→ stack handoffs
```

# Anti-Pattern — Contract by Implementation

Bad:

```text
backend implements endpoint
→ frontend reads actual JSON
→ spec updated afterward
```

when contract decisions were known to be shared.

Prefer accepted contract before dependent implementation.

# Anti-Pattern — Spec Without Ownership

A spec saying:

```text
system upgrades subscription
```

is insufficient for coordination.

Preparation must identify stack responsibilities.

# Anti-Pattern — Over-Specifying Internals

Do not put:

```text
React hook name
repository class name
SQL table name
```

into shared spec unless they are actual cross-stack/public requirements.

# Anti-Pattern — Full-Stack God Orchestrator

Do not embed:

- all backend rules;
- all frontend rules;
- all security rules;
- all testing rules.

Delegate.

# Final Decision

Use:

```text
FULL_STACK_PREPARATION_READY
FULL_STACK_PREPARATION_READY_WITH_CONDITIONS
FULL_STACK_PREPARATION_REQUIRES_REQUIREMENTS
FULL_STACK_PREPARATION_REQUIRES_OPENSPEC
FULL_STACK_PREPARATION_REQUIRES_CONTRACT
FULL_STACK_PREPARATION_REQUIRES_COMPATIBILITY_PLAN
FULL_STACK_PREPARATION_REQUIRES_SEQUENCE
FULL_STACK_PREPARATION_BLOCKED
```

## Output

Use `assets/full-stack-change-preparation-record.md`.

## Completion Criteria

- [ ] Request is enriched enough for implementation.
- [ ] Acceptance criteria are explicit.
- [ ] OpenSpec context is explored.
- [ ] Existing vs new change decision is explicit.
- [ ] OpenSpec change is created/edited when required.
- [ ] Full-stack capability is named in business terms.
- [ ] Backend slice is identified.
- [ ] Frontend slice is identified.
- [ ] Shared API/event/provider contracts are explicit.
- [ ] Request DTO semantics are explicit where applicable.
- [ ] Response DTO semantics are explicit where applicable.
- [ ] Error taxonomy needed by consumers is explicit.
- [ ] Authorization semantics are explicit.
- [ ] Idempotency is decided where retries/duplicates matter.
- [ ] Compatibility is classified.
- [ ] Breaking changes include migration/deployment strategy.
- [ ] Database/provider sequencing is identified when relevant.
- [ ] Dependency graph is explicit.
- [ ] Parallelization occurs only after shared contracts stabilize.
- [ ] Frontend mocks/fixtures derive from accepted contracts.
- [ ] Security/privacy/performance triggers are assigned rather than implemented here.
- [ ] Every acceptance criterion has stack/contract ownership.
- [ ] Backend handoff is bounded and implementation-ready.
- [ ] Frontend handoff is bounded and implementation-ready.
- [ ] Stack-specific architecture decisions remain local after shared contracts.
- [ ] Decision conflicts reopen shared contract ownership.
- [ ] Blocking open questions are resolved before handoff.
- [ ] Scope growth/non-goals are explicit.
- [ ] Cross-stack verification expectations are defined.
- [ ] Orchestrator does not duplicate specialist rules.
- [ ] Final preparation status is explicit.
