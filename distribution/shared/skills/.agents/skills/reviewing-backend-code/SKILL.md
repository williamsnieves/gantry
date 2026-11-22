---
name: reviewing-backend-code
description: Reviews backend changes against the definitive backend engineering standard using evidence-oriented code audit, adversarial challenge, and detailed inspection. Use for pull requests, diffs, branches, modules, or focused backend changes after implementation. Classify findings across correctness, architecture, security, maintainability, testing, compatibility, and operations; prioritize defects that can change behavior, corrupt data, leak boundaries, weaken tenant isolation, duplicate side effects, or leave required evidence missing. Compose auditing-code, reviewing-adversarially, and analyzing-details when available. Do not report personal style preferences, rewrite the change, invent requirements, or mark unavailable validation as passed.
...
---

# Reviewing Backend Code

## Purpose

Review a backend change against:

- the accepted specification;
- repository-local rules;
- the definitive backend engineering standard;
- the actual diff and surrounding code;
- executed validation evidence.

The review must identify actionable defects and risks.

It must not become:

- a style critique;
- an architecture redesign;
- an implementation task;
- a speculative requirements exercise;
- a list of generic best practices.

## Composition

This skill should compose the reusable workflow skills:

```text
auditing-code
reviewing-adversarially
analyzing-details
```

Use them as complementary modes:

```text
audit
→ establish evidence and changed behavior

adversarial review
→ challenge failure modes and assumptions

detail analysis
→ inspect mappings, branches, boundaries, and edge cases
```

The backend standard remains the governing rule source.

## Use When

- Reviewing a backend pull request or diff.
- Reviewing one completed backend vertical slice.
- Reviewing Domain, Application, Infrastructure, HTTP, composition, or tests.
- Verifying a brownfield change did not worsen architecture.
- Investigating whether implementation matches accepted behavior.
- Checking transaction, idempotency, migration, security, or error-handling risks.
- Reviewing code before merge or release.
- Reviewing changes after architecture and behavioral validation.

## Do Not Use When

- The task is to implement or refactor the code.
- The task is only architecture validation.
- The task is only running the validation matrix.
- No specification, diff, files, or review scope is available.
- The user asks for a general tutorial.
- The finding is based solely on personal naming or formatting preference.
- A missing product decision would require guessing intended behavior.
- The request is to review frontend or non-backend code.

## Inputs

- Accepted change/specification.
- Pull request diff, branch diff, files, or module scope.
- Repository-local `AGENTS.md`.
- Definitive backend engineering standard.
- Relevant implementation records.
- Architecture-validation report.
- Validation commands and results.
- Existing tests.
- Decision register and accepted exceptions.
- Migration, rollout, and compatibility notes.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Read the accepted change or specification.
3. Identify exact review scope:
   - diff;
   - changed files;
   - one capability;
   - full module.
4. Read changed files with enough surrounding context.
5. Inspect tests changed or required by the behavior.
6. Inspect relevant ports, DTOs, schemas, migrations, and composition.
7. Read architecture and validation reports when available.
8. Identify accepted exceptions and unresolved decisions.
9. Distinguish changed behavior from pre-existing code.
10. Do not infer intent from implementation alone when requirements exist.

## Outputs

- Review scope summary.
- Evidence and validation summary.
- Prioritized findings.
- Finding classification and severity.
- File/line or symbol evidence.
- Impact and failure scenario.
- Suggested remediation direction.
- Missing evidence and unresolved questions.
- Final review decision.
- Backend code review report.

## Review Workflow

1. **Confirm review basis:** Specification, scope, standard, and accepted decisions.
2. **Understand the change:** Trigger, behavior, layers, data, side effects, and public contracts.
3. **Audit changed paths:** Trace input to output and all state transitions.
4. **Run or inspect validation evidence:** Do not assume passing checks.
5. **Review correctness:** Happy path, failures, boundaries, and state.
6. **Review architecture:** Dependency direction, ownership, ports, DTOs, composition.
7. **Review security and privacy:** Authorization, tenancy, secrets, validation, error exposure.
8. **Review persistence and migrations:** Constraints, transactions, compatibility, rollback.
9. **Review external effects:** Idempotency, retries, ambiguous outcomes, reconciliation.
10. **Review HTTP/API behavior:** Contract, auth context, status/body/headers, safe errors.
11. **Review tests:** Correct level, missing cases, false confidence, environment truthfulness.
12. **Review maintainability:** Complexity, duplicated rules, hidden coupling, cleanup.
13. **Challenge adversarially:** Ask how the change fails under retries, concurrency, partial failure, malformed data, and unavailable dependencies.
14. **Classify findings:** Severity, category, confidence, status, and scope.
15. **Remove unsupported findings:** No style-only or speculative comments.
16. **Produce decision:** Approve, approve with conditions, request changes, or blocked.

## Review Basis

Review against evidence in this order:

1. accepted specification and behavior;
2. mandatory backend invariants;
3. repository-local policies;
4. accepted architecture decisions;
5. tests and executable evidence;
6. implementation intent visible in code;
7. defaults from the definitive standard.

Do not elevate a default above an accepted project decision.

## Scope Discipline

Classify observations:

```text
IN_CHANGED_SCOPE
DIRECTLY_AFFECTED
PRE_EXISTING_ADJACENT
UNRELATED
```

Findings should normally be:

- introduced by the change;
- worsened by the change;
- directly affected by the change;
- blocking a safe implementation.

Do not fill the review with unrelated repository debt.

## Changed Versus Existing

Use:

```text
NEW
WORSENED
PRE_EXISTING_BLOCKING
PRE_EXISTING_NON_BLOCKING
FIXED
ACCEPTED_TEMPORARY
```

A pre-existing issue may be blocking when the change relies on or materially expands it.

Do not present unrelated pre-existing debt as if introduced by the author.

## Review Categories

Classify each finding under one primary category:

```text
CORRECTNESS
ARCHITECTURE
SECURITY
DATA_INTEGRITY
CONCURRENCY
TRANSACTION
IDEMPOTENCY
EXTERNAL_INTEGRATION
HTTP_CONTRACT
COMPATIBILITY_MIGRATION
TESTING
OPERABILITY
MAINTAINABILITY
```

Secondary categories may be included when useful.

## Severity

### Critical

Likely production compromise, data corruption, cross-tenant access, credential exposure, unrecoverable duplicate external effects, or catastrophic migration behavior.

Examples:

- tenant filter missing in a write/read path;
- production secret logged;
- non-idempotent retry can charge/send/apply twice;
- destructive migration without compatibility or rollback;
- public endpoint permits unauthorized mutation.

### High

Likely incorrect behavior, contract breakage, serious architecture violation, lost update, partial-failure inconsistency, or missing authoritative protection.

Examples:

- Use Case bypasses Domain invariant;
- controller calls repository and provider directly;
- provider succeeds but persistence failure has no accepted recovery;
- uniqueness enforced only by pre-check;
- Application imports concrete adapter;
- response leaks an Entity or technical error.

### Medium

Defect or maintainability risk with contained impact, weak evidence, incomplete edge handling, or new bounded architecture drift.

Examples:

- missing representative failure test;
- unstable ordering;
- inconsistent error mapping;
- test double defaults hide required calls;
- temporary deviation lacks monitoring.

### Low

Non-blocking clarity or local maintainability problem supported by the standard.

Examples:

- duplicate mapping likely to drift;
- misleading boundary name;
- local dead branch;
- missing focused comment on an accepted non-obvious tradeoff.

Do not use severity to express preference.

## Confidence

Use:

```text
HIGH
MEDIUM
LOW
```

High confidence requires direct code, test, schema, or executable evidence.

Low-confidence concerns should normally be questions or follow-up checks, not blocking findings.

## Correctness Review

Trace:

```text
input
→ validation
→ Domain conversion
→ decision
→ side effect
→ persistence
→ output
```

Check:

- missing branches;
- wrong conditions;
- boundary values;
- null/absence behavior;
- invalid transitions;
- incorrect defaults;
- stale state;
- error swallowing;
- wrong response mapping;
- unintended repeated work;
- state mutation before rejection;
- returned success before durable completion.

Prefer concrete failure scenarios.

## Domain Review

Check:

- invariants enforced at construction and behavior boundaries;
- no invalid partial Entity state;
- Value Object equality and immutability;
- transitions are legal;
- rejected operations preserve state;
- Domain Services are pure;
- no Infrastructure leakage;
- collections remain encapsulated;
- serialization is explicit and safe.

Do not demand a rich model when the behavior is truly simple and the standard does not require more.

## Application Review

Check:

- one intention per Use Case;
- no Use Case chaining;
- primitive-to-Domain conversion;
- authorization and tenancy;
- repository and external ports;
- Domain delegation;
- side-effect order;
- Response DTO or `void`;
- no concrete adapter, HTTP, ORM, SDK, config, or environment import;
- stable semantic failures.

Look for orchestration that implements business rules instead of delegating them inward.

## Repository Review

Check:

- Domain-oriented port;
- concrete adapter isolation;
- mappings and reconstitution;
- null/absence semantics;
- authoritative unique constraints;
- save/update/upsert meaning;
- ordering and pagination;
- transactions;
- concurrency/versioning;
- invalid stored data;
- technical error translation;
- migration compatibility.

Do not accept mock-only tests as proof of persistence behavior.

## External Adapter Review

Check:

- provider-neutral port;
- request/response mapping;
- semantic failure translation;
- credential/account selection;
- timeout;
- bounded retry;
- rate limits;
- idempotency-key reuse;
- ambiguous outcomes;
- async reconciliation;
- redaction;
- client lifecycle;
- strongest safe evidence level.

Do not assume timeout means the provider did nothing.

## HTTP Review

Check:

- route/method;
- transport validation;
- trusted auth/tenant context;
- one Use Case invocation;
- status, body, headers, content type;
- semantic error mapping;
- safe unknown errors;
- no repository/provider/business logic;
- no Entity or technical-detail leakage;
- idempotency header behavior.

The controller must not trust body fields for identities supplied by authentication.

## Composition Review

Check:

- concrete adapters selected centrally;
- typed configuration validated;
- shared Infrastructure cached deliberately;
- Use Cases transient according to policy;
- no runtime DI container or Service Locator;
- no environment reads inward;
- startup/readiness/shutdown;
- deterministic test reset;
- controller receives Use Case.

Look for clients constructed per request and cached Use Cases.

## Security Review

Check:

- authentication and authorization;
- tenant scoping;
- object ownership;
- input validation;
- secret handling;
- PII minimization;
- logging and error redaction;
- production/sandbox account selection;
- injection risks;
- insecure defaults;
- replay and signature verification;
- safe test-only overrides.

Security findings must be tied to actual code paths.

## Data Integrity Review

Check:

- authoritative constraints;
- transaction ownership;
- partial failures;
- duplicate protection;
- optimistic locking;
- lost updates;
- valid reconstitution;
- legacy/unknown data;
- precision/timezone;
- migration order;
- backfill verification;
- rollback compatibility.

A pre-check is not a substitute for a database constraint or atomic operation.

## Idempotency and Retry Review

Trace:

```text
public key
→ Application request
→ persistence/provider mechanism
→ retry/replay result
```

Check:

- stable key reuse;
- no key generation inside retry loop;
- duplicate semantics;
- one durable state;
- no duplicate remote side effect;
- retryable versus permanent failures;
- bounded attempts;
- ambiguous completion;
- reconciliation.

## Migration and Compatibility Review

Check:

- public API/event compatibility;
- schema compatibility;
- staged deployment order;
- old/new application coexistence;
- backfill;
- unknown enums;
- nullable/default behavior;
- generated client/schema changes;
- feature-flag cleanup;
- rollback feasibility;
- observability.

Do not assume code and schema deploy atomically.

## Testing Review

Evaluate whether tests prove the correct boundaries.

### Domain

Pure unit tests with real Domain objects and no mocks.

### Application

Real Domain, InMemory repositories, explicit external-port doubles.

### Repository Adapters

Real isolated persistence and authoritative migrations.

### External Adapters

Mapping plus strongest safe protocol/emulator/sandbox evidence.

### HTTP E2E

Real HTTP and composed application with isolated persistence when claiming full E2E.

Look for:

- missing active failure case;
- assertions against implementation details;
- tests already green because too weak;
- mock-only false confidence;
- uncontrolled time/randomness;
- shared state;
- skipped/blocked tests misreported as pass;
- no cleanup;
- no regression reproduction.

## Test Quality

A test is not strong merely because it exists.

Check:

- observable behavior;
- intended failure in Red;
- deterministic setup;
- meaningful assertions;
- correct test level;
- no over-mocking;
- exact commands and actual execution;
- representative edge cases;
- refactor resilience.

## Operability Review

Check:

- startup/config validation;
- readiness/liveness;
- shutdown;
- timeouts;
- retry exhaustion;
- observability;
- safe correlation IDs;
- metrics;
- cleanup;
- background jobs/consumers;
- resource leaks;
- actionable errors.

Do not request generic logging everywhere.

## Maintainability Review

Report maintainability findings only when they create real change risk.

Examples:

- duplicated business rule across controller and Domain;
- provider mapping spread across Use Case and adapter;
- hidden mutable global state;
- generic Service Locator;
- giant conditional with several intentions;
- duplicated DTO mapping likely to diverge;
- compatibility seam with no removal path;
- misleading abstraction that hides transaction ownership.

Avoid comments about minor formatting or subjective naming.

## Adversarial Questions

Challenge the implementation:

- What happens if the request is sent twice?
- What happens if two requests race?
- What happens if the provider succeeds and the database fails?
- What happens if the database commits and the response is lost?
- What happens if a timeout is ambiguous?
- What happens with stale version/state?
- What happens with an unknown persisted enum?
- What happens across tenants?
- What happens during mixed-version deployment?
- What happens when cleanup or shutdown fails?
- What happens when the test environment is unavailable?
- What information reaches logs and public errors?

Only create findings where evidence supports the risk.

## Finding Requirements

A valid finding contains:

- stable ID;
- concise title;
- severity;
- category;
- confidence;
- status;
- scope;
- rule or accepted behavior;
- evidence;
- concrete failure scenario;
- impact;
- recommended remediation direction;
- validation needed after remediation.

Example:

```text
BE-REV-004 — High — DATA_INTEGRITY

The duplicate check is non-atomic.

Evidence:
ApplyPromotionUseCase calls `existsForSubscriptionAndCampaign()` before
`save()`, while the migration adds no composite unique constraint.

Failure scenario:
Two concurrent requests both observe absence and persist duplicate promotions.

Impact:
Duplicate durable state and potentially duplicated provider operation.

Remediation:
Add authoritative uniqueness in the repository adapter/migration and translate
the losing write to the accepted duplicate semantic.

Validate:
Repository concurrency integration test plus public idempotency E2E.
```

## Evidence

Preferred evidence:

1. executable failing test or command;
2. exact changed code path;
3. schema/migration;
4. type/import graph;
5. existing contract/specification;
6. direct reproducible reasoning;
7. runtime log/metric when safely available.

Do not invent file lines, command outputs, or provider behavior.

## Questions Versus Findings

Use a question when:

- behavior is genuinely unresolved;
- evidence is incomplete;
- multiple valid policies exist;
- the review cannot determine the intended contract.

Use a finding when:

- accepted behavior or rule is clear;
- the code violates it;
- a concrete failure can be explained.

Do not disguise speculative criticism as a finding.

## Duplicate Findings

Merge findings that share one root cause.

Example:

```text
Application imports SDK types
provider errors leak inward
Use Case checks HTTP status
```

These may be one provider-boundary finding with several pieces of evidence.

Do not produce many comments for the same defect.

## Positive Evidence

The review may briefly acknowledge important correct decisions when they reduce uncertainty:

- authoritative constraint added;
- provider key reused;
- safe DTO mapping;
- architecture check added;
- migration is backward compatible.

Do not dilute the review with generic praise.

## Validation Evidence

Record:

- commands run;
- commands inspected but not run;
- results;
- blocked capabilities;
- environment;
- scope.

Use:

```text
PASSED
FAILED
BLOCKED
UNAVAILABLE
NOT_APPLICABLE
INCONCLUSIVE
```

Blocked or unavailable checks are not passes.

## Review Decision

Use one:

```text
APPROVE
APPROVE_WITH_NON_BLOCKING_COMMENTS
APPROVE_WITH_CONDITIONS
REQUEST_CHANGES
BLOCKED_PENDING_DECISION
BLOCKED_PENDING_EVIDENCE
```

### Approve

No blocking findings and required evidence is sufficient.

### Approve With Conditions

Implementation is acceptable only after explicit limited conditions are satisfied.

### Request Changes

At least one actionable blocking defect exists.

### Blocked Pending Decision

Product or architecture must decide unresolved behavior.

### Blocked Pending Evidence

Required validation could not be executed.

## Remediation Routing

Route findings to focused skills:

```text
Domain model
→ modeling-domain-entities
→ modeling-domain-value-objects
→ designing-domain-services

Repository boundary
→ designing-domain-repositories
→ implementing-repository-adapters
→ testing-repository-adapters

Application
→ designing-application-use-cases
→ designing-application-dtos
→ testing-application-use-cases

External provider
→ designing-external-service-ports
→ implementing-external-service-adapters
→ testing-external-service-adapters

HTTP
→ implementing-http-controllers
→ testing-backend-http-e2e

Composition
→ wiring-backend-composition

Architecture
→ validating-backend-architecture

Brownfield
→ adapting-backend-rules-to-existing-code
```

The review should not perform the remediation unless separately requested.

## Output

Use `assets/backend-code-review-report.md`.

## Completion Criteria

- [ ] Accepted behavior, scope, standard, and local rules were read.
- [ ] Changed code was inspected with relevant surrounding context.
- [ ] Correctness was traced from input through side effects and output.
- [ ] Domain, Application, Infrastructure, HTTP, and composition boundaries were reviewed where applicable.
- [ ] Security, tenancy, secrets, and error safety were reviewed.
- [ ] Transactions, concurrency, idempotency, and migrations were reviewed where applicable.
- [ ] Tests were evaluated at the correct boundaries.
- [ ] Validation evidence was recorded honestly.
- [ ] Findings are concrete, evidenced, actionable, and severity-ranked.
- [ ] Personal style preferences and unsupported rules were excluded.
- [ ] New/worsened issues are distinguished from unrelated pre-existing debt.
- [ ] Duplicate root-cause findings were merged.
- [ ] Missing product/architecture decisions are questions or blockers, not guessed.
- [ ] Final decision matches the findings and available evidence.
- [ ] No code was rewritten as part of the review.
