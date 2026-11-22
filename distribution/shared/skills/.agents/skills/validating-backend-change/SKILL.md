---
name: validating-backend-change
description: Runs and reports the backend-specific validation matrix required by the changed layers, composing the generic validating-changes skill. Use before merge, release, or completion claims for backend changes. Determine affected Domain, Application, repository-adapter, external-adapter, HTTP, composition, migration, and architecture checks; verify acceptance coverage at the cheapest reliable test level; distinguish passed, failed, blocked, skipped, unavailable, and inconclusive evidence; and produce a strict completion decision. Do not judge code quality broadly, rewrite the change, invent repository commands, duplicate every test across layers, or report an unexecuted check as passed.
...
---

# Validating Backend Change

## Purpose

Establish whether a backend change is ready to merge or release by running the correct repository-native validation matrix for the layers it changed.

This skill composes:

```text
validating-changes
```

and adds backend-specific decisions for:

- layer-aware test selection;
- acceptance-criterion coverage;
- database and provider evidence;
- HTTP and architecture checks;
- failure classification;
- merge/release readiness.

## Core Flow

```text
changed behavior and layers
→ applicable validation matrix
→ repository-native commands
→ execution evidence
→ acceptance coverage
→ strict completion status
```

## Use When

- A backend change is ready for completion validation.
- A pull request needs merge evidence.
- A release candidate changes backend behavior.
- A vertical slice has completed implementation.
- Several backend test layers must be selected proportionally.
- Database, sandbox, HTTP, migration, or architecture checks may be required.
- Blocked and unavailable checks must be separated from product failures.

## Do Not Use When

- The task is implementation or repair.
- The task is code review.
- The task is architecture review.
- The task is only architecture-boundary validation.
- The change/specification is unavailable.
- Repository-native commands cannot be discovered yet.
- The request is to weaken required checks.
- The goal is to claim quality from test execution alone.

## Inputs

- Accepted specification and acceptance criteria.
- Current diff or changed-file scope.
- Applicable `AGENTS.md`.
- Repository manifests, CI workflows, scripts, and tooling.
- Focused implementation/testing records.
- Backend architecture validation report.
- Database, provider, auth, and external-service environment capabilities.
- Baseline branch or prior evidence when failure ownership matters.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Read the accepted behavior and acceptance criteria.
3. Inspect the diff and classify changed backend layers.
4. Discover commands from repository-native evidence.
5. Inspect CI for mandatory completion checks.
6. Read focused testing records when available.
7. Confirm required database, provider, credentials, and network capabilities.
8. Identify generated artifacts, migrations, and public contracts.
9. Do not invent commands or infer successful execution.

## Outputs

- Changed-layer map.
- Acceptance-to-test traceability matrix.
- Backend validation matrix.
- Exact commands and execution results.
- Failure and blocker classification.
- Coverage gaps.
- Residual risk.
- Merge/release readiness decision.
- Backend change validation report.

## Changed-Layer Classification

Classify each changed area:

```text
DOMAIN
APPLICATION
REPOSITORY_PORT
REPOSITORY_ADAPTER
EXTERNAL_SERVICE_PORT
EXTERNAL_SERVICE_ADAPTER
HTTP_DELIVERY
COMPOSITION
DATABASE_SCHEMA_MIGRATION
PUBLIC_API_CONTRACT
GENERATED_ARTIFACT
CONFIGURATION
DOCUMENTATION
TEST_HARNESS
ARCHITECTURE_RULE
```

One change may affect several layers.

Do not classify by filename alone; inspect responsibility and dependencies.

## Validation Matrix

### Always Consider

```text
format/check
lint
typecheck/static analysis
focused tests
relevant neighboring tests
build/package check
```

Use only repository-native commands that apply.

### Domain Changed

Require:

- focused Domain unit tests;
- affected Domain suite;
- typecheck;
- lint/static checks.

Consider property/boundary/regression tests when accepted behavior requires them.

### Application Changed

Require:

- focused Use Case tests;
- relevant Domain tests;
- DTO/type checks;
- typecheck and lint.

Verify real Domain objects, InMemory repositories, and external-port doubles are used according to policy.

### Repository Port Changed

Require:

- Use Case contract impact;
- InMemory contract tests;
- real repository-adapter contract/integration tests;
- affected implementations and callers;
- architecture checks.

### Repository Adapter Changed

Require:

- real isolated persistence integration tests;
- authoritative migrations;
- round-trip and failure semantics;
- relevant shared repository contracts;
- cleanup/open-handle evidence.

Mocks do not satisfy this requirement.

### Database Schema or Migration Changed

Require applicable:

- migration on a clean database;
- upgrade from representative previous state;
- schema/constraint checks;
- adapter integration tests;
- backfill/verification;
- mixed-version compatibility;
- rollback or forward-fix evidence;
- generated client/schema consistency.

### External-Service Port Changed

Require:

- affected Use Case tests;
- all implementing adapters;
- provider-neutral contract checks;
- architecture checks for provider leakage.

### External Adapter Changed

Require:

- pure mapping tests;
- protocol/contract tests;
- emulator/test mode when available;
- sandbox smoke when required and safe;
- retry/timeout/idempotency cases;
- redaction and lifecycle checks.

Unavailable credentials or sandbox are `BLOCKED` or `UNAVAILABLE`, never `PASSED`.

### HTTP Delivery or Public Contract Changed

Require:

- focused controller/contract checks;
- real HTTP E2E for critical scenarios;
- authentication/tenant-context checks;
- status/body/header/schema validation;
- relevant Use Case tests;
- public contract/generated artifact checks.

Direct controller invocation is not real HTTP E2E.

### Composition Changed

Require:

- composition/startup test;
- configuration validation;
- lifecycle and reset checks;
- representative HTTP smoke/E2E;
- architecture validation.

### Architecture Rule or Boundary Changed

Require:

- repository-native architecture checks;
- full or appropriately expanded scope;
- cycle/import graph checks where available;
- `validating-backend-architecture`.

Changed-file-only evidence is insufficient for repository-wide rule changes.

### Test Harness Changed

Require:

- self-test of helpers/fixtures where available;
- representative tests from every affected test level;
- isolation, cleanup, and deterministic behavior;
- no new skipped/focused tests.

## Acceptance Coverage

Map each acceptance case to the cheapest reliable level.

```text
Domain invariant
→ Domain test

Application orchestration
→ Use Case test

persistence mapping/constraint
→ repository adapter integration

provider protocol
→ external adapter contract/sandbox

public cross-layer behavior
→ HTTP E2E
```

For every criterion record:

```text
COVERED
PARTIALLY_COVERED
NOT_COVERED
BLOCKED
NOT_APPLICABLE
```

Do not duplicate every case in every layer.

A passing suite does not prove an acceptance criterion unless an assertion actually covers it.

## Check Ordering

Default order:

```text
1. environment and command discovery
2. format/check
3. lint/static analysis
4. typecheck
5. focused unit tests
6. neighboring unit tests
7. repository integration/migrations
8. external adapter contract/sandbox
9. HTTP E2E
10. architecture checks
11. build/package/generated-artifact checks
12. broader regression suite proportional to risk
```

Adapt to repository dependencies.

Fail-fast may be used locally, but completion reporting must give every applicable mandatory check a terminal status.

## Check Status

Use exactly:

```text
PASSED
FAILED
BLOCKED
SKIPPED
UNAVAILABLE
INCONCLUSIVE
NOT_APPLICABLE
```

Definitions:

- `PASSED`: executed and succeeded.
- `FAILED`: executed and found a product/test/tooling defect.
- `BLOCKED`: should run, but a resolvable environment/dependency condition prevents it.
- `SKIPPED`: intentionally not executed under an accepted policy.
- `UNAVAILABLE`: repository or provider currently has no capability to execute it.
- `INCONCLUSIVE`: evidence ran but cannot establish the required claim.
- `NOT_APPLICABLE`: the changed scope does not require it.

Only `PASSED` is a pass.

## Failure Classification

Classify failures as:

```text
PRODUCT_FAILURE
TEST_FAILURE
ARCHITECTURE_FAILURE
HTTP_CONTRACT_FAILURE
MIGRATION_PRODUCT_FAILURE
DATABASE_ENVIRONMENT_BLOCKED
PROVIDER_ENVIRONMENT_BLOCKED
CREDENTIALS_BLOCKED
NETWORK_BLOCKED
RATE_LIMIT_BLOCKED
TEST_SETUP_FAILURE
CLEANUP_FAILURE
FLAKY_TEST
PRE_EXISTING_FAILURE
TOOLING_BLOCKED
UNKNOWN_FAILURE_OWNERSHIP
UNAVAILABLE_TEST_CAPABILITY
```

Do not classify a provider outage as a product defect without evidence.

Do not normalize flaky tests with retries.

## Failure Ownership

When a check fails:

1. reproduce in changed scope;
2. compare with baseline when practical;
3. inspect whether the changed path is involved;
4. classify as introduced, worsened, pre-existing, or unknown.

Use:

```text
INTRODUCED
WORSENED
PRE_EXISTING
UNKNOWN
```

Do not expand implementation scope to fix unrelated pre-existing failures.

## Blocked Evidence

A blocked mandatory check must include:

- exact check;
- why it is required;
- missing capability or credential;
- command that should run;
- residual risk;
- owner or unblock action;
- whether merge/release may proceed under policy.

Never write “all checks pass” while a required suite is blocked.

## Skipped Checks

A skipped check needs an accepted reason:

- explicit repository/CI policy;
- not run on untrusted forks;
- scheduled/live suite cadence;
- documented environment exception.

A skipped test inside a suite must not be silently ignored.

Detect or inspect:

```text
.only
.skip
xit
xdescribe
pending tests
quarantine markers
```

Record issue/reference where policy requires it.

## Static and Mechanical Validation

Discover from:

- package scripts;
- task runners;
- Makefiles;
- CI workflows;
- language manifests;
- repository docs.

Potential checks:

```text
format
lint
typecheck
static analysis
dependency/architecture checks
generated code drift
schema validation
build
package
```

Do not add arbitrary generic commands when repository-native equivalents exist.

## Database Validation

Before integration tests confirm:

- safe test target;
- isolation strategy;
- migrations;
- cleanup;
- parallelism;
- readiness.

If Testcontainers/Docker/database is unavailable:

```text
BLOCKED
DATABASE_ENVIRONMENT_BLOCKED
```

not `PASSED` and not a product failure.

## External Provider Validation

Separate suites:

```text
mapping
protocol/contract
emulator/test mode
sandbox smoke
sandbox extended
```

Record which evidence level actually ran.

Missing sandbox credentials:

```text
BLOCKED
CREDENTIALS_BLOCKED
```

A local mock server does not count as sandbox evidence.

## HTTP Validation

For critical public behavior require real HTTP evidence when applicable.

Verify:

- application starts;
- readiness;
- request over HTTP;
- auth/tenant context;
- exact status/body/headers;
- durable side effects;
- cleanup/shutdown.

A controller-method test may supplement but does not replace HTTP E2E.

## Architecture Validation

Invoke or consume:

```text
validating-backend-architecture
```

Require it when the change touches:

- module/layer boundaries;
- ports/adapters;
- DTO ownership;
- composition;
- controller dependencies;
- Use Case dependencies;
- aliases/package exports;
- architecture tooling.

Architecture review is separate and may be required by governance, but validation focuses on defined structural rules.

## Build and Generated Artifacts

When affected, verify:

- backend build/package;
- generated clients/types;
- OpenAPI/schema output;
- ORM generated client;
- migrations;
- no uncommitted generation drift.

Do not hand-edit generated output.

## Security-Sensitive Changes

For auth, authorization, tenancy, credentials, signatures, or sensitive data:

- run relevant focused tests;
- verify negative cases;
- verify error/log redaction;
- run required security checks from repository policy;
- require public-boundary evidence where applicable.

This skill records required security evidence but does not replace a dedicated security review.

## Scope Levels

Use:

```text
ITERATION
PULL_REQUEST
RELEASE
```

### Iteration

Fast focused checks for the active layer.

### Pull Request

All mandatory changed-layer checks and relevant neighboring regression.

### Release

Full required integration/E2E/migration/live-provider and operational checks according to policy.

Do not use iteration evidence as release evidence.

## Evidence Record

For each check capture:

- ID;
- requirement source;
- command;
- working directory;
- environment;
- scope;
- start/end or duration when available;
- exit code;
- result;
- classification;
- relevant output;
- artifact/report path;
- rerun status.

Do not include secrets or sensitive raw payloads.

## Reruns

When a failure is repaired:

- rerun the focused failed check;
- rerun dependent checks;
- replace stale status;
- preserve the earlier failure in history if useful;
- mark the final current evidence clearly.

Do not cite an old green run after code changed.

## Completion Decisions

Use one:

```text
BACKEND_CHANGE_VALIDATED
BACKEND_CHANGE_VALIDATED_WITH_CONDITIONS
BACKEND_CHANGE_FAILED_VALIDATION
BACKEND_CHANGE_BLOCKED
BACKEND_CHANGE_INCONCLUSIVE
```

### Validated

All applicable mandatory checks passed and acceptance coverage is sufficient.

### Validated With Conditions

Only explicitly accepted non-blocking conditions remain.

### Failed Validation

One or more blocking executed checks failed.

### Blocked

Required checks could not run.

### Inconclusive

Evidence is insufficient or conflicting.

## Merge/Release Recommendation

Use:

```text
READY_TO_MERGE
READY_TO_MERGE_WITH_CONDITIONS
NOT_READY_TO_MERGE
READY_TO_RELEASE
READY_TO_RELEASE_WITH_CONDITIONS
NOT_READY_TO_RELEASE
```

Never recommend merge/release with unresolved critical/high product failures or mandatory blocked evidence unless an explicit governance exception exists.

## Output

Use `assets/backend-change-validation-report.md`.

## Completion Criteria

- [ ] Accepted behavior and exact changed scope were inspected.
- [ ] Changed backend layers were classified.
- [ ] Commands came from repository-native evidence.
- [ ] The validation matrix is proportional to changed layers and risk.
- [ ] Every mandatory check has a terminal status.
- [ ] Acceptance criteria are mapped to assertions at the cheapest reliable levels.
- [ ] Database, provider, HTTP, migration, and architecture evidence is included where applicable.
- [ ] Failed, blocked, skipped, unavailable, inconclusive, and not-applicable checks are distinguished.
- [ ] Failure ownership is classified where evidence permits.
- [ ] Skipped/focused/quarantined tests were considered.
- [ ] Rerun evidence is current.
- [ ] No unexecuted or blocked check is described as passed.
- [ ] Test execution is not presented as code-review or test-quality proof.
- [ ] Final validation and merge/release decisions match the strictest mandatory evidence.
