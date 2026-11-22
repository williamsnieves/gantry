---
name: practicing-backend-tdd
description: Portable engineering capability `practicing-backend-tdd`. Use when the
  harness or a specialist agent explicitly requires this named capability.
---
# Practicing Backend TDD

## Purpose

Execute one backend behavioral case through the default cycle:

```text
0. Reason
1. Red
2. Green
3. Refactor
4. Re-evaluate
```

The skill keeps the active cycle small, observable, and evidence-driven.

It does not replace:

- Domain modeling skills;
- Use Case design;
- adapter implementation;
- HTTP implementation;
- focused backend testing skills;
- architecture validation.

It coordinates the test-first rhythm for one behavior inside the current layer.

## Use When

- Implementing a new backend business behavior.
- Fixing a regression with an observable behavioral contract.
- Evolving an Entity, Value Object, Domain Service, Use Case, adapter, or controller.
- Adding a repository query or provider result mapping.
- Implementing one accepted edge case.
- Refactoring behavior after first proving it with a test.
- Continuing an inside-out vertical slice one layer at a time.
- A developer needs a concise record of the active TDD case.

## Do Not Use When

- The change is pure documentation.
- The change is a generated artifact with no meaningful behavior.
- The change is mechanical configuration where behavior-driven TDD is not meaningful.
- Several unrelated behaviors are being implemented at once.
- The intended behavior is unresolved.
- The relevant test environment is unavailable and no truthful substitute exists.
- The request is to design the architecture rather than execute one test cycle.
- The active test already passes before implementation and does not characterize a regression.
- Refactoring is requested while the suite is red.

## Inputs

- Accepted behavior or bug reproduction.
- Current layer and focused implementation/testing skill.
- Existing test commands and repository conventions.
- Current code and tests.
- Applicable backend standard and `AGENTS.md`.
- Known dependencies, test doubles, and environment capabilities.
- Current vertical-slice plan when available.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Read the accepted behavior for the current case.
3. Identify the current layer:
   - Domain;
   - Application;
   - repository adapter;
   - external-service adapter;
   - HTTP/controller;
   - composition;
   - architecture boundary.
4. Read the focused skill for that layer.
5. Discover the narrowest relevant test command.
6. Inspect neighboring tests and fixtures.
7. Confirm the current suite baseline when practical.
8. Identify whether the case is testable through behavior.
9. Do not invent missing acceptance criteria.

## Outputs

- One active TDD case.
- Reason inventory.
- Red evidence.
- Green implementation boundary.
- Refactor evidence.
- Re-evaluation decision.
- TDD progress record.
- Explicit stop/blocker when a material decision is missing.

## Core Discipline

Only one behavioral case is active.

```text
one case
→ one intentional failure
→ minimum implementation
→ safe refactor
→ next decision
```

Do not use one cycle to implement an entire feature.

## Workflow

1. **Select the current layer:** Confirm where the behavior belongs.
2. **Reason:** Enumerate cases and choose the simplest meaningful one.
3. **Define observable behavior:** State input, action, and expected outcome.
4. **Select the cheapest proving test:** Match the test level to the boundary.
5. **Write Red:** Add one focused failing test.
6. **Run Red:** Verify it fails for the intended behavioral reason.
7. **Repair bad Red if needed:** Wrong reason, setup failure, false positive, or already green.
8. **Implement Green:** Add the minimum necessary production behavior.
9. **Run focused tests:** Confirm the active test and nearby regressions pass.
10. **Refactor while green:** Improve naming, duplication, boundaries, and design.
11. **Run tests again:** Preserve observable behavior.
12. **Re-evaluate:** Close the case, choose the next one, move outward, or stop.
13. **Record evidence:** Use the TDD progress record.

## 0. Reason

Before writing the test:

- restate the accepted behavior;
- identify the owning layer;
- enumerate happy, failure, and edge cases;
- select the simplest meaningful case;
- identify prerequisites;
- identify what is explicitly out of scope;
- choose the proving test level.

The case inventory may be temporary, but unresolved TODO case lists must be completed or deliberately tracked before the layer is considered complete.

### Case Selection

Prefer:

1. simplest valid construction or happy path;
2. first meaningful rejection;
3. boundary case;
4. integration-specific failure;
5. regression case.

The sequence may differ when a bug reproduction is the safest first case.

### One Active Case

Mark exactly one case as active.

Example:

```text
[ACTIVE] active promotion can be redeemed once
[PENDING] draft promotion cannot be redeemed
[PENDING] redeemed promotion cannot be redeemed again
```

Do not implement pending cases during the current Green step.

## Observable Behavior

Define:

```text
Given
When
Then
```

Example:

```text
Given an active promotion
When it is redeemed
Then its status becomes redeemed
```

Include only observable effects relevant to the current layer.

Avoid private-field or incidental interaction expectations.

## Test Level Selection

Use the cheapest test that proves the behavior, but test the real boundary when that boundary is the subject.

| Subject | Default test level | Dependencies |
|---|---|---|
| Entity / Value Object | Unit | None |
| Domain Service | Unit | None |
| Use Case | Unit | InMemory repositories and explicit port doubles |
| Repository adapter | Integration | Real isolated database |
| External-service adapter | Integration/contract | Sandbox, emulator, or protocol test |
| HTTP/controller | HTTP integration/E2E | Composed application |
| Composition | Integration/architecture | Real graph or controlled constructors |

Do not use a unit mock to claim a database, provider protocol, or HTTP boundary works.

## 1. Red

Write one test that expresses the current behavior.

A valid Red must:

- compile or reach the intended execution point;
- fail;
- fail because the behavior is missing or wrong;
- produce a useful assertion or contract failure;
- avoid unrelated environment/setup failures;
- avoid depending on future cases;
- be deterministic.

## Red Quality Check

Classify the failure.

```text
EXPECTED_BEHAVIORAL_FAILURE
WRONG_ASSERTION_FAILURE
TEST_SETUP_FAILURE
COMPILATION_FAILURE
ENVIRONMENT_BLOCKED
TEST_ALREADY_GREEN
FLAKY_OR_NON_DETERMINISTIC
```

Only `EXPECTED_BEHAVIORAL_FAILURE` is a valid Red.

### Compilation Failure

A compilation failure may be an acceptable first Red only when the missing public API is itself the intended behavioral change and the project accepts compile-first TDD.

Once the API exists, rerun and verify a behavioral failure where meaningful.

Do not accept unrelated type errors as Red evidence.

### Test Already Green

When the new test passes before implementation:

- determine whether behavior already exists;
- check whether the test is too weak;
- check whether the bug reproduction is incorrect;
- inspect accidental coupling or fixture defaults;
- avoid changing production code merely to force Red.

Possible outcomes:

```text
BEHAVIOR_ALREADY_IMPLEMENTED
TEST_TOO_WEAK
WRONG_REPRODUCTION
CHARACTERIZATION_TEST_ONLY
SPECIFICATION_MISMATCH
```

## Test Isolation

The Red test must not fail because of:

- stale shared state;
- leaked database rows;
- real clock drift;
- uncontrolled randomness;
- network dependence;
- missing cleanup;
- non-deterministic ordering;
- incorrect global composition cache.

Fix the harness before proceeding when these obscure the behavior.

## 2. Green

Implement the minimum behavior required by the active test.

Green means:

- active test passes;
- previous relevant tests remain green;
- no pending cases are implemented speculatively;
- no broad abstraction is introduced without evidence;
- no unrelated cleanup is mixed in;
- boundaries are not knowingly violated.

### Minimum Does Not Mean Poor

The implementation must still preserve mandatory architecture and security invariants.

Do not make tests pass through:

- hard-coded test-only values;
- public setters that bypass invariants;
- adapter leakage inward;
- skipped validation;
- swallowed errors;
- disabled tests;
- fake production branches;
- broad `any` casts;
- sleeping/retrying tests blindly.

## Focused Verification

Run:

1. the active test;
2. the focused test file or layer suite;
3. affected nearby tests;
4. broader suite according to repository cost and risk.

Record exact commands and outcomes.

Do not claim Green from one test when nearby regressions are known.

## Speculative Green

Signs:

- implementing all listed cases before tests;
- adding unused methods;
- creating generic abstractions;
- adding provider/database options not required;
- completing future layers early;
- changing API contracts beyond the case.

Remove or defer speculative behavior.

## 3. Refactor

Refactor only while all relevant tests are green.

Possible improvements:

- intention-revealing names;
- duplication removal;
- smaller functions;
- clearer invariants;
- correct layer placement;
- explicit mapping;
- better fixture builders;
- safer error translation;
- reduced coupling;
- performance improvement without behavior change.

Do not add a new behavior during Refactor.

If a new behavior is discovered:

1. stop refactoring;
2. record it as a pending case;
3. start a new Red cycle later.

## Refactor Safety

After each meaningful refactor:

- run the focused tests;
- preserve public behavior;
- confirm no boundary was weakened;
- avoid snapshot churn unrelated to behavior.

If tests become red, restore Green before continuing.

## 4. Re-evaluate

After Green and Refactor:

- close the active case;
- review pending cases;
- decide whether the layer is complete;
- determine whether to stay in the layer;
- determine whether to move outward;
- identify missing decisions or environment blockers;
- check whether architecture validation is due.

Use one decision:

```text
CONTINUE_CURRENT_LAYER
MOVE_TO_NEXT_LAYER
CASE_COMPLETE_LAYER_COMPLETE
RETURN_TO_REASON
RETURN_TO_SPECIFICATION
ARCHITECTURE_DECISION_REQUIRED
ENVIRONMENT_BLOCKED
REGRESSION_DISCOVERED
```

## Moving Outward

Inside-out order for new business behavior:

```text
Domain
→ Use Case
→ Repository/External Adapters
→ HTTP
```

Move outward only when the current inner behavior is sufficiently proven for the slice.

This does not require completing the entire module before exposing one endpoint.

Do not start HTTP or persistence first unless the change is genuinely infrastructure-only and the reason is explicit.

## Layer Completion

A layer is complete for the current vertical behavior when:

- accepted cases for that layer are green;
- failures and edge cases are covered proportionally;
- temporary TODO case lists are resolved or deliberately tracked;
- no known boundary violation remains;
- relevant focused validation passes;
- outward dependencies can rely on the behavior.

Do not equate one passing happy path with layer completion.

## Regression Fix Cycle

For a bug:

```text
Reason
→ reproduce with failing test
→ verify intended failure
→ minimum fix
→ run regression neighborhood
→ refactor
→ re-evaluate systemic cases
```

Do not fix first and add a passing test afterward unless the environment makes prior reproduction impossible and that limitation is recorded.

## Existing Untested Behavior

When modifying untested legacy code:

1. add characterization tests for behavior that must remain;
2. add a failing test for the new or corrected behavior;
3. implement minimally;
4. refactor only after both remain green.

Characterization tests may start green; they are not the Red case.

## Wrong-Layer Discovery

If the test reveals behavior belongs elsewhere:

```text
Entity rule in Use Case test
→ move test/behavior to Domain

provider parsing in Use Case
→ move to adapter

HTTP status in Application test
→ move to controller/HTTP contract
```

Stop the current cycle and route to the correct focused skill.

Do not preserve wrong-layer code just because a test can be written for it.

## Configuration-Only Exception

Pure documentation, generated artifacts, and mechanical configuration changes may use validation-first when behavior-driven TDD is not meaningful.

Required sequence:

```text
Reason
→ define expected configuration/artifact state
→ make the minimum change
→ run validation
→ inspect output/diff
→ re-evaluate
```

The exception must not skip verification.

Examples:

- generated client regeneration;
- mechanical lint config;
- static route registration;
- non-behavioral metadata.

Do not classify composition lifecycle, adapter selection, startup failure, or runtime configuration behavior as “configuration-only”; those are testable behaviors.

## Environment Blockers

When the real boundary cannot run:

- classify the missing capability;
- run lower-level evidence that remains truthful;
- do not mark the real boundary as passing;
- record residual uncertainty;
- define the exact command/evidence still required.

Classifications:

```text
DATABASE_ENVIRONMENT_BLOCKED
PROVIDER_SANDBOX_BLOCKED
CREDENTIALS_BLOCKED
NETWORK_BLOCKED
HTTP_RUNTIME_BLOCKED
TOOLING_BLOCKED
```

## Flaky Red or Green

Do not accept a non-deterministic result.

Investigate:

- time;
- randomness;
- ordering;
- shared state;
- concurrency;
- ports;
- cleanup;
- external environment.

Stabilize the test or classify the environment limitation before proceeding.

Do not solve flakiness with arbitrary sleeps.

## Mocking Discipline

Do not mock:

- Entities;
- Value Objects;
- Domain Services.

For Use Cases:

- use InMemory repositories;
- use explicit stubs/spies for external ports.

For adapters and HTTP:

- test the real boundary or strongest available contract environment.

Mocks may support narrow interaction checks but cannot replace boundary evidence.

## Test Data

Prefer builders/factories that:

- produce valid defaults;
- make the active variation explicit;
- avoid hidden behavior;
- remain local or shared according to reuse evidence.

Do not create a giant universal fixture abstraction during one Green step.

## Assertion Quality

Assert observable semantics:

- returned result;
- Domain state;
- persisted state;
- translated failure;
- HTTP contract;
- provider-neutral call.

Avoid:

- private fields;
- exact internal call order without semantic relevance;
- implementation-specific SQL;
- SDK internals in Use Case tests;
- snapshots too broad to diagnose behavior.

## Progress Record

Use `assets/backend-tdd-progress-record.md`.

The record must contain:

- behavior and layer;
- active case;
- pending cases;
- Red command and intended failure;
- Green implementation scope;
- verification commands;
- refactor summary;
- re-evaluation decision;
- blockers and residual risks.

## TDD Status

Use one:

```text
REASON_READY
RED_CONFIRMED
RED_INVALID
GREEN_CONFIRMED
REFACTOR_CONFIRMED
CYCLE_COMPLETE
VALIDATION_FIRST_EXCEPTION
BLOCKED
```

## Completion Criteria

- [ ] Current behavior and owning layer confirmed.
- [ ] Cases enumerated and exactly one active case selected.
- [ ] Cheapest valid proving test chosen.
- [ ] Red test fails for the intended behavioral reason.
- [ ] Test setup, compilation, and environment failures are not mislabeled as Red.
- [ ] Green implementation is the minimum accepted behavior.
- [ ] Pending cases are not implemented speculatively.
- [ ] Relevant existing tests remain green.
- [ ] Refactoring occurs only while green.
- [ ] Refactor does not introduce new behavior.
- [ ] Re-evaluation decides whether to continue, move outward, or stop.
- [ ] Configuration-only exception, when used, still includes validation.
- [ ] Boundary limitations and residual uncertainty are reported honestly.
- [ ] Progress record contains commands and evidence.

## References

- Read `references/reason-and-case-selection.md` first.
- Read `references/red-quality.md` before accepting a failing test.
- Read `references/green-and-refactor-discipline.md` before production changes.
- Read `references/re-evaluation-and-layer-progression.md` before moving outward.
- Read `references/test-levels-and-doubles.md` when selecting evidence.
- Read `references/exceptions-blockers-and-flakiness.md` when normal TDD cannot proceed.
