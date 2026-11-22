---
name: testing-backend-http-e2e
description: Designs and implements backend HTTP end-to-end tests against a composed application using real HTTP requests. Use when critical routes must prove request parsing, authentication context, controller mapping, Use Case orchestration, persistence side effects, response status/body/headers, idempotency, and representative failure paths. Keep the E2E suite selective and evidence-oriented: cover critical cross-layer behavior without duplicating every Domain, Use Case, repository, or provider-adapter case. Do not bypass HTTP by calling controllers directly, expose real provider credentials, depend on production data, or claim blocked environment checks passed.
---

# Testing Backend HTTP E2E

## Purpose

Prove that a backend capability works through the complete HTTP delivery path.

A correct backend HTTP E2E test validates:

```text
real HTTP request
→ routing and middleware
→ authentication/context
→ controller
→ Application Use Case
→ Domain behavior
→ selected Infrastructure adapters
→ real HTTP response
```

Depending on the accepted test composition, selected external providers may be replaced with provider-neutral test doubles while persistence and HTTP remain real.

The suite must be selective. It should prove cross-layer integration without repeating every lower-level case.

## Use When

- Testing a critical REST endpoint end to end.
- Verifying route, method, request parsing, authentication, status, body, and headers.
- Verifying controller-to-Use Case wiring.
- Verifying real persistence side effects through HTTP.
- Verifying idempotency at the public boundary.
- Verifying representative authorization, business rejection, conflict, and dependency-failure paths.
- Verifying startup composition and test environment.
- Verifying an accepted API contract after a cross-layer change.
- Adding a regression test whose failure only appears across several layers.

## Do Not Use When

- Testing a Domain invariant in isolation.
- Testing a Use Case orchestration case that does not require HTTP.
- Testing a repository adapter contract.
- Testing provider protocol details.
- Testing a controller by calling its method directly.
- Exhaustively repeating all lower-level success and failure cases.
- Using production credentials, data, or shared environments.
- The route, auth, error, or response contract is unresolved.
- The application cannot be composed safely and the missing evidence is being presented as passed.

## Inputs

- Accepted HTTP/API contract.
- Composed backend application or test bootstrap.
- Controllers, Use Cases, ports, adapters, and composition root.
- Test persistence strategy and migrations.
- Authentication test mechanism.
- Provider test strategy:
  - provider-neutral fake/stub in composed app;
  - sandbox only when explicitly required and safe.
- Test data builders and cleanup policy.
- Existing E2E commands, CI capabilities, and server lifecycle conventions.
- Applicable `AGENTS.md` and backend standards.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Read the accepted route and response/error contract.
3. Inspect the production composition root and test composition support.
4. Inspect authentication middleware/guards and trusted context shape.
5. Confirm test persistence provisioning and migrations.
6. Confirm which Infrastructure adapters are real in E2E.
7. Confirm which external ports use deterministic test doubles.
8. Confirm server startup, readiness, shutdown, and reset.
9. Inspect existing HTTP/E2E conventions.
10. Identify lower-level cases already covered to avoid duplication.
11. Do not infer missing public contract behavior.

## Outputs

- Critical HTTP scenario inventory.
- Composed test application strategy.
- Safe test environment and data lifecycle.
- Real HTTP E2E tests.
- Contract assertions for status, body, headers, and side effects.
- Representative failure-path evidence.
- Failure/environment classification.
- Backend HTTP E2E testing record.

## Core Principle

Test the public behavior through real HTTP.

```text
HTTP client
→ bound test server
→ complete delivery path
→ observable response and durable side effects
```

Do not call:

- controller methods directly;
- Use Cases directly;
- repositories directly as the primary action.

Repositories may be inspected after the HTTP call only to verify durable side effects when no public read endpoint exists.

## Workflow

1. **Confirm readiness:** Route, composition, auth, persistence, and environment are resolved.
2. **Select critical scenarios:** Cross-layer value, not lower-level completeness.
3. **Define test composition:** Real HTTP, real Application/Domain, real persistence, controlled external ports.
4. **Provision isolated environment:** Database/schema, migrations, server port, secrets, and test identities.
5. **Start application:** Validate readiness before requests.
6. **Arrange through public or safe test setup:** Seed minimum valid state.
7. **Issue real HTTP request.**
8. **Assert status, body, headers, and content type.**
9. **Assert durable side effects:** Public read API preferred; repository inspection allowed as secondary verification.
10. **Assert representative failures:** Auth, validation, business rejection, conflict, dependency failure.
11. **Verify idempotency/replay behavior where applicable.**
12. **Clean state and shut down deterministically.**
13. **Classify blocked or environment failures honestly.**
14. **Audit duplication:** Remove scenarios already proven adequately below the HTTP boundary.
15. **Record exact commands and evidence.**

## Readiness Gate

Use one:

```text
READY_TO_TEST_HTTP_E2E
READY_WITH_CONDITIONS
RETURN_TO_CONTROLLER_IMPLEMENTATION
RETURN_TO_COMPOSITION
HTTP_CONTRACT_DECISION_REQUIRED
AUTH_TEST_STRATEGY_REQUIRED
TEST_PERSISTENCE_REQUIRED
EXTERNAL_DEPENDENCY_STRATEGY_REQUIRED
BLOCKED
```

Stop when:

- server cannot start deterministically;
- auth context cannot be created safely;
- migrations are unavailable;
- test database is not isolated;
- external provider behavior cannot be controlled safely;
- route/status/error contract is unresolved;
- composition still bypasses intended adapters.

## What E2E Must Prove

A critical scenario may prove:

- route registration;
- HTTP method;
- request parsing;
- validation;
- authentication middleware;
- trusted actor/tenant propagation;
- controller Request DTO mapping;
- Use Case wiring;
- Domain behavior;
- persistence integration;
- external-port integration or controlled semantic outcome;
- response DTO mapping;
- HTTP error mapping;
- headers;
- idempotency;
- cleanup and lifecycle.

Not every scenario needs to prove every item.

## What E2E Should Not Duplicate

Do not repeat every:

- Entity invalid transition;
- Value Object boundary;
- Use Case missing-state branch;
- database constraint variant;
- provider error code;
- serializer edge case.

Those belong to focused lower-level suites.

E2E selects representative scenarios that prove layers work together.

## Scenario Selection

Prioritize:

1. critical business success;
2. authentication/authorization failure;
3. transport validation failure;
4. representative Domain/Application rejection;
5. conflict/idempotency;
6. representative dependency failure;
7. regression involving cross-layer wiring;
8. async accepted/pending contract when applicable.

A small endpoint may need only three to five scenarios.

A high-risk payment or identity route may require more.

## Scenario Traceability

Each E2E scenario should cite:

- accepted behavior;
- public contract;
- lower-level coverage it complements;
- cross-layer risk it proves.

Avoid scenarios whose only purpose is increasing E2E count.

## Test Composition

Recommended:

```text
real HTTP server
real routing/middleware/controllers
real Use Cases and Domain
real repository adapters
isolated real database
provider-neutral external-service doubles
fixed Clock / ID generator when composition permits
```

Use a real provider sandbox only when:

- the public behavior specifically depends on live-provider behavior;
- a separate adapter suite is insufficient;
- credentials and cost are controlled;
- CI policy permits it.

Most backend HTTP E2E tests should not require live providers.

## Production-Like Composition

Reuse production wiring as much as practical.

Test composition may override:

- external-service ports;
- Clock;
- ID generator;
- authentication verifier;
- telemetry exporters.

Overrides must be:

- typed;
- explicit;
- narrow;
- resettable;
- unavailable to production runtime;
- not a generic Service Locator.

Do not rebuild a separate application architecture solely for E2E.

## Persistence

Prefer real isolated persistence.

Use:

- Testcontainers;
- ephemeral database;
- unique schema/database;
- faithful emulator when accepted.

Apply authoritative migrations.

Do not use in-memory persistence if the goal is proving repository wiring and durable behavior.

A lightweight E2E tier may use InMemory repositories only when explicitly classified as HTTP integration rather than full persistence E2E.

## Server Lifecycle

Tests must control:

- application construction;
- server binding;
- readiness;
- base URL;
- graceful shutdown;
- open handles;
- composition reset.

Use an ephemeral port when possible.

Do not assume a developer server is already running.

## Startup Failure

Classify startup failures:

```text
PRODUCT_STARTUP_FAILURE
CONFIGURATION_FAILURE
DATABASE_ENVIRONMENT_BLOCKED
CREDENTIALS_BLOCKED
PORT_BIND_FAILURE
TOOLING_BLOCKED
```

Do not send requests before readiness.

## Authentication Strategy

Use the repository-approved mechanism.

Possible approaches:

- test JWT signed with test key;
- test identity provider adapter;
- explicit test auth middleware;
- session/cookie fixture;
- service token fixture.

Requirements:

- no production secrets;
- trusted actor/tenant context matches production shape;
- expired/invalid token cases are testable;
- test override cannot ship enabled in production.

Do not bypass authentication by calling the controller directly.

## Authorization

Authorization is proved through the public request.

Arrange a trusted actor and resource ownership/tenant state.

Verify:

- allowed actor succeeds;
- forbidden actor receives accepted status/body;
- no durable side effect occurs after denial.

Do not test every role permutation at E2E when Application tests already cover the matrix.

## Request Validation

Test representative transport failures:

- missing required header;
- malformed path or body;
- unsupported content type;
- invalid enum string;
- body size limit when critical.

Do not duplicate every Domain validation rule.

A malformed primitive that reaches Application may be tested at Use Case level.

## Success Assertions

Verify exact accepted contract:

- status;
- content type;
- body fields;
- required/optional/nullability;
- headers;
- `Location`;
- correlation or replay metadata;
- no internal fields;
- no Entity/Value Object leakage.

Avoid broad snapshots when explicit contract assertions are more diagnostic.

## Side-Effect Verification

Preferred order:

1. call a public read endpoint;
2. inspect an accepted query/read-model port through test harness;
3. inspect repository state through the composed test environment;
4. inspect raw persistence only for a truly technical assertion.

The primary action remains the HTTP request.

Do not assert only that a mock function was called.

## External Side Effects

For external ports in HTTP E2E:

- use a provider-neutral spy/fake;
- record semantic calls;
- configure stable outcomes;
- verify meaningful payload/idempotency propagation;
- avoid SDK/provider details.

Live provider behavior belongs mainly to external-adapter tests.

## Idempotency

For an idempotent HTTP command, test:

- required public header;
- first request success;
- same request/key replay;
- accepted duplicate/replay status and body;
- no duplicated durable state;
- same external semantic operation/ref;
- different key behavior if accepted.

Do not rely only on provider-spy call counts; verify durable outcome.

## Conflict and Concurrency

Representative E2E may test:

- duplicate request;
- optimistic conflict;
- concurrent HTTP commands.

Use real persistence when claiming concurrency.

Avoid making the E2E suite the primary place for exhaustive database race testing.

Detailed constraint behavior remains in repository-adapter tests.

## Dependency Failures

Select representative semantic failures:

- external unavailable;
- timeout;
- rate limited;
- persistence unavailable when safely testable.

Use controlled test composition or fault injection.

Verify:

- accepted HTTP status/body;
- no technical detail leakage;
- no invalid side effect;
- correlation/telemetry behavior when contractual.

Do not inject raw provider HTTP errors into controllers.

## Error Safety

Unexpected error tests should assert:

- generic public error;
- stable code/body;
- no stack trace;
- no SQL/ORM/provider detail;
- safe correlation ID when accepted.

Logs may be captured securely to verify internal diagnostics without exposing them publicly.

## Async Endpoints

For `202 Accepted`:

- verify status and response body;
- correlation/job/resource location;
- initial pending state;
- eventual completion through polling or public read endpoint when practical;
- bounded waiting;
- duplicate/idempotency behavior.

Do not use arbitrary sleeps.

Use bounded polling with clear deadline and diagnostic state.

## Eventual Consistency

When persistence or external processing is eventually consistent:

- poll a public read endpoint;
- use stable correlation;
- bound duration;
- distinguish pending from failed;
- record timeout semantics;
- clean pending resources.

Do not treat immediate absence as permanent failure.

## Webhooks

For inbound webhook E2E, test:

```text
real HTTP request
→ signature verification
→ controller
→ reconciliation Use Case
→ durable result
```

Use provider fixture signatures or test secrets.

Cover representative:

- valid event;
- invalid signature;
- duplicate event;
- unsupported event;
- stale/replayed event.

Provider protocol details remain additionally covered in adapter/utility tests.

## Pagination and Query Endpoints

Representative E2E may verify:

- query parsing;
- default limit;
- stable response shape;
- next cursor/link;
- authorization/tenant filtering.

Detailed ordering and pagination edge cases remain in repository/read-model tests.

## Data Setup

Preferred setup order:

1. public setup API, when stable and cheap;
2. approved test fixture service/port;
3. repository seeding through test composition;
4. raw database insertion only for technical or invalid-state scenarios.

Do not make every E2E depend on a long chain of unrelated public APIs.

Setup helpers must be explicit and deterministic.

## Test Data Builders

Use deterministic:

- IDs;
- timestamps;
- actors;
- tenants;
- idempotency keys;
- resource names;
- request bodies.

Avoid global mutable fixtures.

Each scenario should own or isolate its state.

## Cleanup

Clean:

- database/schema;
- server;
- composition caches;
- provider-neutral doubles;
- test auth state;
- temporary files;
- message consumers/jobs;
- telemetry exporters.

Cleanup must run after success and failure.

Do not let cleanup failure hide the primary assertion failure.

Record open handles.

## Parallelism

Define:

- unique schema/database per worker;
- unique server port;
- unique actor/tenant/resource IDs;
- isolated external-port spies;
- migration serialization;
- cleanup ownership.

If a suite cannot run safely in parallel, configure it explicitly.

Do not tolerate random cross-test contamination.

## Test Layers

Classify tests accurately:

```text
HTTP integration
→ real HTTP + Application + controlled in-memory Infrastructure

HTTP E2E
→ real HTTP + Application + real persistence + controlled external ports

live-system E2E
→ real HTTP + real persistence + live external providers
```

Do not call every controller test “E2E.”

## Test Naming

Preferred:

```text
applies a promotion through HTTP and persists the accepted state
returns 403 and creates no promotion for a non-owner
returns 409 and preserves one promotion on idempotent replay
maps provider unavailability to a safe 503 response
```

Avoid:

```text
endpoint works
POST test
full flow
```

## Assertions Against Lower Layers

Direct repository inspection is acceptable only after the HTTP action and only as secondary evidence.

Do not:

- invoke Use Case to arrange the main action;
- invoke controller directly;
- assert private Domain fields;
- assert raw ORM error;
- assert SDK request objects.

## OpenAPI and Contract Alignment

When a schema exists, verify:

- runtime response matches schema;
- required/optional fields;
- enums;
- error body;
- content type;
- headers when supported.

Use source schema or generated validator according to repository policy.

Do not hand-edit generated OpenAPI output.

## Regression Cases

Use HTTP E2E for regressions involving:

- route not registered;
- auth context not forwarded;
- wrong controller mapping;
- wrong status/header;
- composition selects wrong adapter;
- transaction not committed;
- response leaks internal fields;
- idempotency breaks across layers.

Do not use HTTP E2E for a pure Domain regression already proven by a unit test.

## Test Execution

Run:

1. environment/bootstrap check;
2. focused scenario;
3. endpoint E2E suite;
4. relevant repository/adapter suites when changed;
5. contract/schema validation;
6. cleanup/open-handle verification;
7. broader E2E smoke according to risk.

Record exact commands and actual outcomes.

## Failure Classification

Use:

```text
PRODUCT_FAILURE
HTTP_CONTRACT_FAILURE
AUTH_FAILURE
COMPOSITION_FAILURE
DATABASE_ENVIRONMENT_BLOCKED
EXTERNAL_TEST_DOUBLE_FAILURE
PROVIDER_SANDBOX_FAILURE
CREDENTIALS_BLOCKED
NETWORK_BLOCKED
PORT_BIND_FAILURE
TEST_SETUP_FAILURE
CLEANUP_FAILURE
FLAKY_TEST
TOOLING_BLOCKED
UNAVAILABLE_TEST_CAPABILITY
```

Do not mark blocked checks as passed.

## Avoiding Duplicate Coverage

Before adding a scenario, ask:

```text
Does this fail only when multiple layers interact?
```

If no:

- Domain rule → Domain test;
- orchestration → Use Case test;
- persistence mapping/constraint → repository adapter test;
- provider protocol → external adapter test;
- controller mapping only → controller test.

Keep E2E focused on cross-layer risks.

## Coverage Matrix

A useful matrix:

| Scenario | HTTP | Auth | Application | Persistence | External | Why E2E |
|---|---|---|---|---|---|---|
| Success | yes | yes | yes | yes | controlled | proves full wiring |
| Forbidden | yes | yes | yes | no write | none | proves trusted context and mapping |
| Conflict | yes | yes | yes | yes | controlled | proves public idempotency |
| Provider unavailable | yes | yes | yes | no invalid write | controlled | proves error translation |

Avoid dozens of rows duplicating unit suites.

## CI Strategy

Classify:

- endpoint smoke;
- full HTTP E2E;
- migration-backed E2E;
- live-provider E2E.

Choose cadence:

- pull request;
- protected branch;
- scheduled;
- release.

Keep external sandbox suites separate unless required.

## Security

Verify:

- production endpoints are not targeted;
- production credentials are unavailable;
- auth bypass is test-only and guarded;
- PII is synthetic;
- logs are redacted;
- errors are safe;
- tenant isolation is preserved;
- cleanup does not cross namespaces.

## Boundary Audit

The composed application should preserve:

- controller depends on Use Case;
- Use Case depends on ports;
- adapters implement ports;
- Domain/Application do not import composition;
- HTTP response contains DTO primitives;
- provider/database technical details stay inside Infrastructure.

An E2E pass does not excuse a boundary violation; architecture validation remains separate.

## Readiness Decision

Use one:

```text
HTTP_E2E_COMPLETE
HTTP_E2E_COMPLETE_WITH_CONDITIONS
MORE_CRITICAL_SCENARIOS_REQUIRED
RETURN_TO_CONTROLLER
RETURN_TO_COMPOSITION
RETURN_TO_LOWER_LEVEL_TEST
TEST_ENVIRONMENT_REPAIR_REQUIRED
BLOCKED
```

## Output

Use `assets/backend-http-e2e-testing-record.md`.

## Completion Criteria

- [ ] Application is composed and started through the real HTTP entry point.
- [ ] Requests are issued over HTTP rather than direct controller calls.
- [ ] Test authentication and trusted context are representative and safe.
- [ ] Persistence is isolated and real when claiming full E2E.
- [ ] External dependencies use controlled provider-neutral doubles unless live evidence is explicitly required.
- [ ] Critical success and representative failure paths are covered.
- [ ] Status, body, headers, content type, and error safety are asserted.
- [ ] Durable side effects and absence of invalid side effects are verified.
- [ ] Idempotency/replay is covered where applicable.
- [ ] Startup, readiness, shutdown, reset, and cleanup are deterministic.
- [ ] Scenarios do not duplicate every lower-level test.
- [ ] Failure and blocked evidence are classified honestly.
- [ ] Exact commands and outcomes are recorded.
- [ ] Production credentials, data, and endpoints are never used.
- [ ] No technical provider/database details leak through the HTTP contract.

## References

- Read `references/e2e-scope-and-scenario-selection.md` first.
- Read `references/test-composition-and-environment.md` for application setup.
- Read `references/http-contract-auth-and-errors.md` for public assertions.
- Read `references/side-effects-idempotency-and-async.md` for cross-layer outcomes.
- Read `references/data-isolation-cleanup-and-ci.md` for reliable execution.
- Read `references/failure-classification-and-duplication-audit.md` before completion.
