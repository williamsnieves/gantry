---
name: testing-external-service-adapters
description: Portable engineering capability `testing-external-service-adapters`.
  Use when the harness or a specialist agent explicitly requires this named capability.
---
# Testing External Service Adapters

## Purpose

Prove that a concrete external-service adapter satisfies its provider-neutral Application port while interacting correctly with the provider protocol.

A correct test strategy validates:

- Application request to provider payload mapping;
- provider response to semantic Application result mapping;
- provider error to stable failure translation;
- authentication and tenant/account selection;
- timeout and cancellation behavior;
- bounded retries and rate-limit handling;
- idempotency-key propagation and reuse;
- ambiguous completion and reconciliation;
- asynchronous pending/completed states;
- redaction and safe observability;
- SDK/client lifecycle;
- realistic provider behavior through sandbox, emulator, protocol tests, or contract fixtures;
- honest separation of product, provider, credential, network, and environment failures.

## Core Test Boundary

```text
Application port
→ concrete Infrastructure adapter
→ provider protocol / SDK
→ semantic Application outcome
```

Use Case tests exercise port doubles.

Adapter tests exercise the real adapter and strongest available provider boundary.

## Use When

- Testing a payment, notification, campaign, identity, storage, AI, clock, or similar adapter.
- Verifying SDK/HTTP request mapping.
- Verifying provider result and error translation.
- Verifying provider idempotency and duplicate semantics.
- Verifying retries, rate limits, timeouts, and ambiguous outcomes.
- Verifying tenant-specific credential/account selection.
- Testing asynchronous provider states or reconciliation.
- Adding a provider sandbox or emulator suite.
- Replacing mock-only adapter tests with stronger contract evidence.
- Diagnosing whether a failure belongs to product code or the test environment.

## Do Not Use When

- Testing Application Use Cases with port stubs/spies.
- Designing the provider-neutral port.
- Testing repository persistence.
- Testing HTTP controllers.
- The provider contract or adapter semantics are unresolved.
- Production credentials are required or exposed.
- The only evidence is a mocked adapter method and it is presented as real integration proof.
- Sandbox or network failure is being reported as a product defect without evidence.
- The adapter leaks SDK types through the Application port.

## Inputs

- Accepted Application port and port design report.
- Concrete provider adapter and implementation record.
- Provider API/SDK documentation and pinned version.
- Provider sandbox, official emulator, protocol, or schema/fixture documentation.
- Accepted semantic success and failure taxonomy.
- Timeout, retry, idempotency, rate-limit, fallback, and async policies.
- Test credential and secret-management policy.
- Tenant/account-selection rules.
- Existing test commands and CI capabilities.
- Applicable `AGENTS.md` and backend standards.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Read the Application port and concrete adapter.
3. Read the adapter handoff and accepted failure semantics.
4. Confirm the provider API/SDK version.
5. Identify the strongest available test capability:
   - real sandbox;
   - official emulator;
   - provider test mode;
   - protocol-compatible local server;
   - contract/schema fixtures.
6. Confirm credential source, scope, rotation, and cleanup.
7. Confirm retry, timeout, idempotency, and asynchronous behavior.
8. Confirm provider cost, rate limits, and destructive-operation restrictions.
9. Inspect CI network and secret availability.
10. Do not invent provider behavior not supported by documentation or observed evidence.

## Outputs

- Adapter behavior inventory.
- Test capability selection and limitations.
- Safe test credential plan.
- Pure mapping tests.
- Protocol/emulator/sandbox integration tests.
- Failure and retry evidence.
- Idempotency and ambiguous-outcome evidence.
- Async/reconciliation evidence.
- Failure classification.
- External-service adapter testing record.
- Optional provider test harness helpers.

## Workflow

1. **Confirm readiness:** Port, adapter, provider contract, policies, and safe test capability exist.
2. **Select evidence levels:** Mapping, protocol, emulator, sandbox.
3. **Classify credentials and environment:** Safe, isolated, available, and non-production.
4. **Inventory provider outcomes:** Success, rejection, duplicate, rate limit, timeout, unavailable, pending, unknown.
5. **Test request mapping:** Minimal fields, headers, auth, tenant/account, idempotency.
6. **Test response mapping:** Stable semantic results and external references.
7. **Test failure translation:** Provider codes/statuses/exceptions never leak inward.
8. **Test retries and rate limits:** Bounded, policy-compliant, and idempotency-safe.
9. **Test timeout and ambiguous completion:** Reuse keys and reconcile when supported.
10. **Test async states:** Pending, callback/webhook correlation, final reconciliation.
11. **Test security:** Credentials, PII, redaction, and safe diagnostics.
12. **Test client lifecycle:** Construction, reuse, cleanup, and resource safety.
13. **Run sandbox/emulator/contract evidence.**
14. **Classify failures honestly.**
15. **Record residual uncertainty and exact missing evidence.**
16. **Audit Application boundary:** No SDK/provider leakage.

## Readiness Gate

Use one:

```text
READY_TO_TEST_EXTERNAL_ADAPTER
READY_WITH_CONDITIONS
RETURN_TO_ADAPTER_IMPLEMENTATION
RETURN_TO_PORT_DESIGN
TEST_CREDENTIALS_REQUIRED
PROVIDER_SANDBOX_REQUIRED
PROVIDER_CONTRACT_DECISION_REQUIRED
RESILIENCE_DECISION_REQUIRED
BLOCKED
```

Stop when:

- test credentials are production-scoped or unsafe;
- the provider sandbox can cause real charges or user-visible effects without explicit controls;
- the provider contract conflicts with the Application port;
- idempotency is required but cannot be verified or reconciled;
- failure taxonomy is unresolved;
- tests would expose secrets or sensitive payloads;
- no truthful evidence level can be executed.

## Evidence Levels

Use a layered strategy.

### Level 1 — Pure Mapping Tests

Validate:

```text
Application input
→ provider request

provider response/error
→ semantic Application result/failure
```

Fast and deterministic, but they do not prove the actual provider protocol.

### Level 2 — Protocol-Compatible Tests

Use:

- local HTTP fake server;
- mock server;
- SDK transport interceptor;
- provider contract fixtures;
- schema validation.

Validate method, path, headers, serialization, retry, timeout, and parsing.

These prove adapter protocol behavior against the modeled contract, not the live provider.

### Level 3 — Official Emulator or Provider Test Mode

Use an official tool when it faithfully supports required behavior.

Document unsupported behaviors and version differences.

### Level 4 — Real Sandbox

Strongest evidence for real provider behavior.

Use only safe test accounts, data, regions, credentials, and cleanup.

## Sandbox Preference

Use a real sandbox when:

- officially supported;
- credentials can be managed safely;
- operations are isolated;
- costs are controlled;
- test data can be cleaned or expired;
- CI access is reliable enough;
- provider terms permit automation.

A sandbox may differ from production.

Record differences explicitly.

## When No Sandbox Exists

Use this order:

```text
official emulator
→ documented test mode
→ protocol-compatible fake server
→ schema/contract fixtures
→ pure mapping tests
```

Then record:

- behavior not verified against the provider;
- assumptions based on documentation;
- missing failure modes;
- command/evidence required later.

Do not call this full provider integration verification.

## Credentials

Test credentials must:

- come from an approved secret manager or CI secret store;
- be scoped to test/sandbox resources;
- use least privilege;
- be rotatable;
- never appear in code, fixtures, logs, snapshots, or artifacts;
- be unavailable to untrusted pull requests when policy requires;
- be cleaned/revoked when compromised.

Do not use personal developer tokens as a permanent CI strategy.

## Credential Validation

Test startup/configuration behavior for:

- missing credential reference;
- invalid credential;
- unauthorized account;
- expired token;
- wrong tenant/account mapping.

Do not assert or print the secret value.

## Tenant and Account Selection

When adapters select accounts by tenant, test:

- accepted tenant mapping;
- unknown tenant;
- disabled tenant;
- wrong region/account;
- credentials selected only in Infrastructure;
- no provider account ID leakage inward unless explicitly accepted.

Use isolated test tenants.

## Request Mapping

Verify:

- provider operation/endpoint;
- selected fields only;
- headers and content type;
- provider API version;
- idempotency header;
- correlation/reference;
- tenant/account;
- enum/date/Money mapping;
- omitted versus null fields;
- sensitive field minimization.

Do not assert whole payload snapshots when targeted assertions are clearer.

## Response Mapping

Test provider states such as:

```text
accepted
queued
pending
completed
duplicate
rejected
not found
```

Map them to stable Application meanings.

Do not overstate provider semantics:

```text
provider queued
≠ delivered
```

External references may be exposed only as the neutral contract defines.

## Failure Translation

Cover accepted categories:

```text
REJECTED
RATE_LIMITED
TIMEOUT
UNAVAILABLE
DUPLICATE
CONFLICT
UNAUTHORIZED_WITH_PROVIDER
INVALID_EXTERNAL_REQUEST
PERMANENT_FAILURE
RETRYABLE_FAILURE
UNKNOWN_EXTERNAL_FAILURE
```

Verify the Application sees:

- semantic type/code;
- safe metadata only;
- no HTTP status;
- no provider error enum;
- no raw SDK exception;
- no response body;
- no secret.

## Retry Tests

Verify:

- only accepted retryable failures retry;
- permanent rejection does not retry;
- attempts are bounded;
- backoff policy is applied through controllable timing;
- `Retry-After` or equivalent is interpreted internally;
- same idempotency key is reused;
- success after transient failure maps correctly;
- exhaustion maps to the accepted semantic failure.

Use fake timers only for Infrastructure retry scheduling when deterministic and supported.

Do not use real sleeps.

## Retry Test Boundary

A protocol fake can count attempts and return a sequence:

```text
429
→ 503
→ 201
```

Assertions may verify semantically required attempt count and idempotency-key reuse.

Avoid coupling to incidental internal helper calls.

## Rate Limits

Test:

- status/error translation;
- retry-after parsing;
- bounded retry;
- no busy loop;
- metrics classification;
- permanent exhaustion behavior.

Do not expose raw rate-limit headers inward unless the port models a neutral equivalent.

## Timeout Tests

Test:

- configured timeout reaches transport/SDK;
- timeout maps semantically;
- request cancellation/resource cleanup;
- safe retry only when accepted;
- provider may have accepted the operation;
- reconciliation or status query occurs when supported.

Do not assume timeout means the provider did nothing.

## Ambiguous Outcomes

For state-changing operations:

```text
request may have been accepted
→ connection lost / timeout
→ result unknown
```

Verify:

- same idempotency key is preserved;
- duplicate on retry maps to idempotent success when accepted;
- external reference is retained;
- reconciliation query is used when supported;
- no second side effect is created.

A local protocol test can model this sequence.

Sandbox evidence should be used when provider supports deterministic idempotency tests.

## Idempotency

Test:

- key mapping to provider mechanism;
- exact reuse across retries;
- duplicate response translation;
- repeated invocation outcome;
- external reference consistency;
- no key generation inside retry loop;
- behavior when key is missing or malformed according to adapter contract.

Do not expose vendor header names through the Application port.

## Asynchronous Operations

Test states such as:

```text
QUEUED
PENDING
COMPLETED
REJECTED
```

Verify:

- initial adapter result;
- correlation ID;
- status lookup mapping;
- stale pending behavior;
- final reconciliation;
- duplicate callback/event handling where the adapter owns relevant provider utilities.

Inbound webhook controller tests belong to HTTP/delivery testing.

Provider-specific signature utilities may have focused Infrastructure tests.

## Webhook Contract Support

When adapter-related utilities verify provider signatures or parse provider events, test:

- valid signature;
- invalid signature;
- timestamp/replay window;
- payload version;
- event type mapping;
- secret redaction.

Do not test the full controller here.

## Fallback

Test fallback only when explicitly accepted.

Verify:

- trigger condition;
- alternate adapter selection ownership;
- idempotency across providers;
- semantic differences;
- duplicate risk;
- observability.

No accepted fallback means tests should assert none is attempted.

## Circuit Breaker

When accepted, test:

- opening after configured failures;
- semantic `UNAVAILABLE`;
- no provider call while open;
- half-open recovery;
- metrics;
- no circuit-library type leakage.

Do not add circuit-breaker testing when the adapter does not own one.

## Security and Privacy

Test or audit:

- no secrets in request logs;
- no full sensitive payloads;
- PII redaction;
- safe error messages;
- restricted provider response logging;
- test data minimization;
- region/account correctness;
- no production endpoints in test mode.

A log capture can assert absence of sensitive values.

Do not store real PII in fixtures.

## Observability

Verify semantic telemetry when required:

- operation;
- provider;
- latency;
- success/failure category;
- retry count;
- timeout;
- rate limit;
- correlation/idempotency reference;
- sandbox/test mode.

Do not assert provider secrets or full payloads.

Avoid brittle exact-log-string assertions unless logs are contractual.

## SDK/Client Lifecycle

Test relevant behavior:

- client constructed once when shared;
- tenant-scoped clients cached safely if accepted;
- no client created per operation accidentally;
- cleanup/close invoked;
- failed construction does not leak resources;
- adapter behaves safely after shutdown according to policy.

Composition lifecycle tests may own global sharing.

Adapter tests should validate adapter/client-specific lifecycle only.

## Provider Versioning

Pin or identify the tested version.

Test fixtures should state:

- API version;
- SDK version;
- webhook schema version;
- fixture source/date;
- compatibility assumptions.

When upgrading:

- rerun mapping/contract tests;
- compare enums and error shapes;
- run sandbox smoke tests;
- record deprecated fields.

Do not hand-edit generated SDK types.

## Test Data

Use clearly identifiable sandbox data:

```text
test-run-id
synthetic email/domain
test tenant
sandbox payment method
non-production resource prefix
```

Requirements:

- no real customer data;
- deterministic correlation;
- cleanup/expiry;
- provider rate/cost awareness.

## Cleanup

Clean or expire:

- provider test resources;
- pending operations;
- uploaded objects;
- test identities;
- subscriptions/webhooks;
- local mock servers;
- clients and connections.

Cleanup must:

- run after success or failure;
- avoid deleting shared resources;
- be idempotent;
- report cleanup failure;
- preserve the primary product failure.

Some providers do not allow deletion. Use tagged expiring resources and document it.

## Cost Controls

For metered providers:

- use sandbox/free test mode;
- cap test volume;
- separate smoke from exhaustive suites;
- avoid retries that create cost;
- schedule live sandbox suites appropriately;
- expose cost-related skips/blocks honestly.

Do not run expensive live suites on every local test by default unless policy says so.

## CI Strategy

Classify suites:

```text
unit mapping
protocol contract
emulator
sandbox smoke
sandbox extended
```

Define which run on:

- every commit;
- pull request;
- protected branch;
- scheduled job;
- release gate.

Credential-protected suites must not run for untrusted forks unless safely supported.

## Failure Classification

Use:

```text
PRODUCT_FAILURE
PROVIDER_CONTRACT_FAILURE
PROVIDER_SANDBOX_FAILURE
PROVIDER_OUTAGE
CREDENTIALS_BLOCKED
NETWORK_BLOCKED
RATE_LIMIT_BLOCKED
TEST_SETUP_FAILURE
CLEANUP_FAILURE
FLAKY_TEST
TOOLING_BLOCKED
UNAVAILABLE_TEST_CAPABILITY
```

Examples:

- wrong payload generated by adapter → `PRODUCT_FAILURE`;
- provider changed documented response schema → `PROVIDER_CONTRACT_FAILURE`;
- sandbox returns 500 independently → `PROVIDER_SANDBOX_FAILURE` or `PROVIDER_OUTAGE`;
- missing secret in CI → `CREDENTIALS_BLOCKED`.

Do not collapse all failures into “integration test failed.”

## Evidence Requirements

For every executed suite record:

- exact command;
- environment level;
- provider/test mode;
- API/SDK version;
- result;
- classification;
- sanitized correlation/reference;
- residual uncertainty.

Do not include secrets or raw sensitive payloads.

## Flakiness

Investigate:

- sandbox instability;
- asynchronous completion;
- rate limits;
- shared test account state;
- non-unique idempotency keys;
- cleanup lag;
- provider eventual consistency;
- network variability;
- time-dependent signatures;
- global SDK client state.

Use polling with accepted bounded deadlines for eventual consistency.

Do not use arbitrary fixed sleeps as the primary solution.

## Eventual Consistency

When the provider is eventually consistent:

- define a bounded polling policy;
- use stable correlation IDs;
- distinguish pending from failure;
- record final timeout semantics;
- clean up asynchronously if required.

Protocol tests should use deterministic virtual timing where possible.

## Test Doubles Versus Adapter Tests

Use Case tests:

```text
Application port stub/spy
```

Adapter tests:

```text
real adapter
+ protocol/emulator/sandbox
```

Do not call a port stub an adapter integration test.

## Mocks

Mocks may be used narrowly for:

- SDK constructor/lifecycle;
- secret resolver;
- telemetry;
- transport fault injection.

They cannot by themselves prove:

- provider accepts payload;
- idempotency works;
- real authentication works;
- sandbox semantics;
- provider error shape.

## Contract Fixtures

Fixtures should be:

- sanitized;
- versioned;
- minimal;
- traceable to provider documentation or observed sandbox responses;
- reviewed on SDK/API upgrade.

Do not store real tokens, emails, card data, identities, or unrestricted response dumps.

## Potential Test Harness Helpers

Roadmap-compatible helpers may include:

```text
scripts/check-provider-test-env
scripts/run-provider-contract-tests
scripts/run-provider-sandbox-smoke
scripts/create-sandbox-test-resource
scripts/cleanup-sandbox-test-resources
```

Use repository-native tooling.

Do not create new scripts when existing commands suffice.

## Test Naming

Preferred:

```text
maps an accepted campaign request to the provider payload and idempotency header
translates provider duplicate into idempotent success
reuses the same idempotency key after an ambiguous timeout
does not retry a permanent business rejection
reports sandbox unavailability separately from adapter failure
```

Avoid:

```text
sdk works
api test
calls post
```

## Test Execution

Run proportionally:

1. pure mapping tests;
2. protocol/contract tests;
3. official emulator/test mode;
4. sandbox smoke;
5. relevant extended sandbox cases;
6. cleanup verification;
7. typecheck/lint.

Record exact commands and outcomes.

Do not claim sandbox success when it was not run.

## Boundary Audit

Verify the Application port and test assertions do not expose:

- SDK request/response classes;
- HTTP status;
- provider enums/error codes;
- API keys or credentials;
- vendor-specific headers;
- raw transport objects.

Infrastructure tests may inspect them internally to prove translation, but inward results remain provider-neutral.

## Readiness Decision

Use one:

```text
EXTERNAL_ADAPTER_TESTS_COMPLETE
EXTERNAL_ADAPTER_TESTS_COMPLETE_WITH_CONDITIONS
MORE_ADAPTER_CASES_REQUIRED
RETURN_TO_ADAPTER_IMPLEMENTATION
RETURN_TO_PORT_DESIGN
TEST_CREDENTIALS_REQUIRED
PROVIDER_ENVIRONMENT_BLOCKED
TEST_HARNESS_REPAIR_REQUIRED
BLOCKED
```

## Output

Use `assets/external-service-adapter-testing-record.md`.

## Completion Criteria

- [ ] Accepted port, adapter, provider contract, and version are confirmed.
- [ ] Strongest safe available evidence level is selected.
- [ ] Test credentials are sandbox-scoped, protected, and never exposed.
- [ ] Request mapping is tested.
- [ ] Response and semantic failure translation are tested.
- [ ] Authentication and tenant/account selection are tested.
- [ ] Timeout, retry, rate-limit, and idempotency behavior are tested where applicable.
- [ ] Ambiguous outcomes and reconciliation are covered.
- [ ] Async pending/completed semantics are covered when applicable.
- [ ] Security, redaction, observability, and lifecycle are audited or tested.
- [ ] Sandbox/emulator/contract limitations are explicit.
- [ ] Product, provider, credential, network, rate-limit, and environment failures are distinguished.
- [ ] Cleanup and cost controls are defined.
- [ ] Exact commands and actual evidence are recorded.
- [ ] Mock-only tests are not represented as provider integration proof.
- [ ] No provider/SDK/credential detail leaks through the Application port.

## References

- Read `references/evidence-levels-and-sandbox-selection.md` first.
- Read `references/credentials-security-and-test-data.md` for safe environments.
- Read `references/mapping-and-failure-translation.md` for contract tests.
- Read `references/retries-timeouts-idempotency-and-rate-limits.md` for resilience.
- Read `references/async-reconciliation-and-eventual-consistency.md` for pending operations.
- Read `references/failure-classification-cleanup-and-ci.md` for operational evidence.
- Read `references/external-adapter-test-audit.md` before completion.
