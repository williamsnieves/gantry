---
name: testing-frontend-adapters
description: Tests frontend Infrastructure adapters against faithful external boundaries. Use for HTTP repositories, browser storage, IndexedDB, cache/offline adapters, and third-party/provider integrations. Verify request/response mapping, runtime payload validation, stable error semantics, cancellation, auth refresh behavior, offline/storage failures, IndexedDB serialization/migrations, and real provider sandbox compatibility where appropriate. Prefer MSW/test servers/emulators/real browser-like storage or documented sandboxes over mocking fetch internals or mocking the adapter itself. Do not test React/UI behavior, Domain rules, or Use Case orchestration here.
---

# Testing Frontend Adapters

## Purpose

Test the actual Infrastructure adapter at the boundary where provider/storage behavior matters.

Core model:

```text
real adapter under test
→ faithful technical boundary
→ external/storage contract behavior
→ inward semantic result/error
```

Examples of faithful boundaries:

```text
MSW
test HTTP server
contract fixture
browser-like IndexedDB
storage emulator
provider emulator
real provider sandbox
documented test environment
```

The test should prove:

```text
external detail
→ correct mapping
→ stable inward semantics
```

## Governing Standard

Frontend adapter tests SHOULD use:

- a real sandbox;
- a test server;
- MSW;
- a contract fixture;
- an emulator;
- another documented realistic boundary.

The chosen strategy MUST verify:

- mapping;
- failure semantics.

MSW or equivalent is preferred over mocking `fetch` internals for HTTP-facing UI tests.

HTTP and storage adapters should verify:

- path/method/headers through approved client;
- request mapping;
- response mapping;
- not-found;
- forbidden/unavailable;
- malformed JSON/schema;
- abort;
- date/enum/null mapping;
- pagination where relevant;
- no raw response leakage.

IndexedDB/storage tests should verify:

- round trip;
- missing value;
- migration;
- corrupt data;
- transaction failure;
- quota/storage unavailable;
- cleanup;
- SSR unavailable behavior where applicable.

## Use When

- Testing an HTTP repository adapter.
- Testing a third-party API/provider adapter.
- Testing request/response mapping.
- Testing runtime validation at external boundary.
- Testing 404 or other transport-to-semantic mapping.
- Testing token refresh/re-auth retry semantics.
- Testing request cancellation.
- Testing browser storage mapping.
- Testing IndexedDB serialization/migrations.
- Testing offline/local persistence behavior.
- Running a provider sandbox/contract compatibility check.
- Testing multiple implementations of one port against shared semantic contract tests.

## Do Not Use When

- Testing Domain models.
- Testing Application Use Cases.
- Testing React hooks/components.
- Testing query-cache behavior.
- Testing visual rendering.
- Testing E2E user journeys.
- Testing only a mapper function when no adapter integration behavior is involved.
- The test replaces the adapter with a mock.
- The test calls a production provider when a safe sandbox/test boundary is required.

## Inputs

- Accepted port contract.
- Adapter implementation.
- Exact provider/storage types.
- Runtime-validation policy.
- Stable Infrastructure/Application error semantics.
- Approved HTTP/storage abstraction.
- Authentication/refresh policy.
- Cancellation policy.
- Offline/cache authority policy.
- IndexedDB/storage schema/version.
- Provider sandbox/emulator policy.
- Test-environment credentials policy.
- Existing adapter testing conventions.
- Applicable `AGENTS.md`.

## Outputs

- Boundary-strategy decision.
- HTTP/storage/provider test inventory.
- Mapping/error/cancellation tests.
- Auth-refresh tests when applicable.
- Offline/state tests.
- IndexedDB integration tests.
- Provider sandbox compatibility tests.
- Shared port contract suite where multiple implementations exist.
- Adapter testing record.

# Boundary Strategy

Choose one or more:

```text
MSW
TEST_SERVER
CONTRACT_FIXTURE
BROWSER_STORAGE_RUNTIME
INDEXEDDB_EMULATOR_OR_REAL_BROWSER
PROVIDER_EMULATOR
PROVIDER_SANDBOX
OTHER_DOCUMENTED_FAITHFUL_BOUNDARY
```

Record why.

Do not select:

```text
MOCK_THE_ADAPTER
MOCK_FETCH_INTERNALS_ONLY
PLAIN_OBJECT_AS_INDEXEDDB
PRODUCTION_PROVIDER
```

as the primary proof when a more faithful boundary is available.

# Test the Real Adapter

The System Under Test should be:

```text
HttpSubscriptionRepository
IndexedDbDraftRepository
VendorAnalyticsAdapter
BrowserStoragePreferencesRepository
```

not:

```text
jest.mock("HttpSubscriptionRepository")
```

The adapter itself must execute.

# HTTP Boundary

For HTTP adapters, test through the approved HTTP abstraction.

Possible:

```text
adapter
→ project HttpClient
→ MSW/test server
```

This verifies more faithfully than stubbing repository methods.

Do not mock `fetch` implementation details unless repository policy explicitly uses that boundary.

# MSW

MSW is useful for:

- request path;
- method;
- query params;
- headers;
- body;
- response payload;
- status;
- malformed response;
- delays/cancellation;
- network errors.

Keep handlers close to accepted contract fixtures.

Do not use MSW handlers to implement Application business rules.

# Test Server

A test HTTP server may be better when you need to verify:

- redirects;
- streaming;
- cookies;
- binary behavior;
- lower-level protocol edge cases;
- actual HTTP-client integration.

Do not use a server if MSW already proves the accepted behavior more cheaply.

# Contract Fixtures

Use exact provider fixtures for:

- DTO mapping;
- version differences;
- malformed/null/optional fields;
- provider enums;
- pagination envelopes.

Fixtures should represent external contracts, not inward Domain objects.

# Mapper Tests

Pure mapper tests may exist alongside adapter integration tests.

Typical:

```text
provider payload
→ mapper
→ Application/Domain-safe data
```

Do not treat pure mapper tests as proof that URL, headers, auth, cancellation, storage, or actual adapter wiring works.

# HTTP 404

Roadmap case:

```text
404
```

A 404 must map according to the port contract.

Examples:

```text
findById 404
→ undefined / Maybe.none
```

if absence is defined.

But:

```text
command endpoint 404
→ stable NOT_FOUND error
```

may be correct.

Do not globally map every 404 to `undefined`.

Test endpoint-specific semantics.

# Other Statuses

Where accepted, verify:

```text
401 unauthenticated
403 forbidden
409 conflict
429 rate limit
5xx unavailable/server
```

Do not require every adapter to test every status if the port cannot observe them.

# Transport vs Semantic Error

Assert inward stable semantics.

Example:

```text
MSW returns 409
→ adapter returns SubscriptionConflict
```

Do not leak:

```text
AxiosError
Response
statusText
provider message
```

unless the outer port explicitly exposes transport metadata.

# Malformed JSON

The HTTP client may own invalid JSON decoding semantics.

If adapter receives already-decoded unknown data, adapter tests should still verify provider schema mismatch where runtime validation is accepted.

Distinguish:

```text
MALFORMED_JSON
```

from:

```text
SCHEMA_MISMATCH
```

if architecture does.

# Malformed Payload

Roadmap case:

```text
malformed payload
```

Test:

```text
provider returns structurally invalid payload
→ runtime validator/mapper rejects
→ stable malformed/external-contract error
→ no malformed data crosses inward
```

Do not force invalid payload into Domain constructors and rely on later crashes.

# Runtime Validation

When adapter owns runtime validation:

```text
unknown payload
→ validate provider contract
→ map inward
```

Test both:

```text
valid external payload
invalid external payload
```

Avoid asserting validation-library-specific issue trees unless they are part of adapter behavior.

# Nullable / Optional Fields

Test external `null`/missing semantics explicitly where important.

Do not let optional chaining accidentally create silent `undefined` mappings.

# Provider Enums

Verify exact mapping:

```text
"ACTIVE"
→ SubscriptionStatus.Active
```

and unknown behavior:

```text
UNKNOWN_PROVIDER_ENUM
→ accepted fallback or stable malformed-contract error
```

Do not leak provider enum strings inward.

# Date Mapping

Test:

```text
ISO timestamp
UTC/offset behavior
invalid date
business date vs timestamp
serialization outward
```

Use fixed values and explicit timezone expectations.

# Request Mapping

Verify:

- path;
- method;
- query;
- request body;
- headers;
- tenant/resource identifiers;
- pagination;
- dates/enums;
- optional fields.

Do not assert incidental header order.

# Authentication

Auth may be owned by HTTP client rather than adapter.

Adapter tests should test only accepted integration responsibility.

If adapter passes:

```text
auth required
```

or resource context into HTTP client, verify that contract.

Do not duplicate HTTP-client unit tests at every repository adapter.

# Auth Refresh

Roadmap case:

```text
auth refresh
```

Only test refresh if project HTTP policy actually supports it.

Typical integration:

```text
request
→ 401
→ one refresh
→ retry original request
→ mapped success
```

or:

```text
refresh fails
→ stable unauthenticated result
```

# Refresh Test Cases

Where accepted:

```text
successful refresh
failed refresh
only one retry
no infinite loop
concurrent 401 refresh coalescing if supported
cancellation during refresh
```

Do not invent refresh behavior if project policy says caller/session layer owns it.

# Refresh Boundary

If refresh is entirely HTTP-client responsibility:

- HTTP-client tests own detailed refresh algorithm;
- adapter tests may include one representative integration case proving repository call survives approved refresh flow.

Avoid duplicating every HTTP-client refresh test per adapter.

# Token Lifecycle

Never use real production tokens.

Use:

```text
fake test token
sandbox token
test identity
```

according to approved environment.

Do not log credentials.

# Cancellation

Verify caller cancellation reaches the technical request when the port supports it.

Example:

```text
AbortSignal
→ adapter
→ HttpClient
→ request abort
→ stable cancellation semantic
```

# Cancellation Result

Cancellation should remain distinguishable from:

```text
network failure
timeout
server error
```

where the Application reacts differently.

Do not assert only that `AbortController.abort()` was called; assert resulting semantic behavior.

# Stale Response

Adapters themselves may not own latest-wins UI semantics, but they should support cancellation required by consumers.

Do not test hook-level stale-response state here.

# Offline State

Roadmap case:

```text
offline state
```

Applicable to:

- offline adapters;
- local-first repositories;
- storage fallback;
- cache-backed implementations;
- explicitly offline-aware HTTP behavior.

Do not infer offline support merely because IndexedDB exists.

# Offline Semantics

Define accepted result:

```text
OFFLINE_WITH_LOCAL_DATA
OFFLINE_NO_DATA
OFFLINE_QUEUED
OFFLINE_UNAVAILABLE
```

or project equivalent.

Test exactly the accepted port semantics.

# Network Offline

For pure remote adapters, offline may map to:

```text
NetworkUnavailable
```

No automatic IndexedDB fallback unless architecture defines it.

# Offline Queue

If adapter queues mutations offline, test:

```text
operation persisted
identity retained
ordering
duplicate prevention
retry metadata
delete/tombstone
```

Do not test full reconciliation business policy if it belongs elsewhere.

# Cache Authority

For cache-backed adapters, establish:

```text
authoritative source
local provisional source
read-through/write-through/write-back
TTL/staleness
```

Tests must reflect that policy.

Do not create a second server-state cache over SWR/React Query accidentally.

# Browser Storage

Storage adapters should test actual serialization boundary.

Examples:

```text
localStorage
sessionStorage
```

Use a browser-like environment or project-approved storage implementation.

Verify:

- key;
- serialization;
- missing;
- corrupt JSON;
- schema version;
- quota/failure where simulatable;
- cleanup;
- SSR unavailable behavior.

Do not treat stored data as trusted.

# Storage Corruption

Test:

```text
invalid JSON
wrong version
wrong shape
```

and accepted result:

```text
discard
migrate
stable corruption error
```

Do not silently default critical values if contract says corruption is meaningful.

# SSR Storage

If adapter can be imported server-side, test accepted behavior:

```text
STORAGE_UNAVAILABLE
lazy browser access
server-safe no-op
```

according to architecture.

Do not access `window.localStorage` at module import time if SSR-safe behavior is required.

# IndexedDB

Roadmap case:

```text
IndexedDB mapping
```

Test the real adapter against:

```text
real browser IndexedDB
fake-indexeddb / approved emulator
browser component test
```

depending on repository policy.

A plain object map is not enough.

# IndexedDB Round Trip

Verify:

```text
Domain/Application-safe input
→ adapter serialization
→ object store
→ adapter read
→ inward semantic result
```

# IndexedDB Mapping

Test:

- object store shape;
- key mapping;
- dates;
- enums;
- nullable fields;
- nested data;
- version field;
- deleted/tombstone state if used.

Do not expose `IDBDatabase`/`IDBRequest` inward.

# IndexedDB Missing

Test missing records according to port:

```text
undefined / Maybe.none / stable not-found
```

# IndexedDB Migrations

If schema versions exist, test:

```text
old version
→ upgrade
→ data preserved/transformed
→ new adapter reads correctly
```

Do not only test fresh database creation.

# IndexedDB Transaction Failure

Where architecture relies on transaction semantics, verify:

```text
transaction abort
→ no partial committed state
→ stable storage error
```

Do not claim atomicity across IndexedDB and remote API.

# IndexedDB Blocked Upgrade

Test blocked/versionchange behavior if project supports recovery/reporting.

Do not create brittle browser-internal tests if the app has no accepted behavior for this case.

# Quota / Storage Unavailable

Simulate only through a faithful mechanism when project behavior exists.

Do not write implementation-only monkey patches that prove nothing about adapter translation.

# Storage Cleanup

Each test must isolate and clean:

```text
database
object store state
local/session storage keys
```

No cross-test state.

# Provider Adapter

Third-party/provider adapters may be tested at three levels:

```text
contract fixture
provider emulator
provider sandbox
```

Use the cheapest boundary that proves the behavior.

# Provider Sandbox

Roadmap case:

```text
provider sandbox
```

Use only when:

- vendor offers a safe sandbox/test project;
- credentials are test-only;
- calls are deterministic enough;
- cost/rate limits are acceptable;
- CI/network policy permits;
- sandbox adds confidence beyond fixtures/emulators.

# Sandbox Is Not Unit Test

Sandbox tests are typically:

```text
integration
contract compatibility
nightly/pre-merge selective
```

not fast unit tests.

Keep them tagged/separated.

# Sandbox Assertions

Verify stable contract aspects:

- authentication works;
- endpoint/action available;
- expected provider shape;
- mapper accepts current version;
- stable error case if sandbox supports it.

Do not depend on volatile provider data unless seeded/owned.

# Sandbox Safety

Never:

- mutate production resources;
- use production credentials;
- assume sandbox isolation without documentation;
- leak secrets into logs/artifacts;
- run destructive tests without explicit test resource lifecycle.

# Sandbox Data Lifecycle

Define:

```text
seed/create
use
cleanup
idempotent naming
retry-safe cleanup
```

If sandbox cannot be reliably cleaned, avoid destructive integration tests.

# Sandbox Availability

If sandbox is down:

```text
integration unavailable
```

is not the same as adapter failure.

Classify infrastructure/test-environment outage separately.

# Contract Tests

If several adapters implement one port:

```text
HttpRepository
IndexedDbRepository
InMemoryRepository
```

shared semantic contract tests may verify:

```text
find missing
save/read round trip
ordering
stable conflict
```

Adapter-specific tests still verify technical details.

# Contract Suite Input

Design a factory:

```text
createAdapterHarness()
```

or project equivalent.

Do not force technical behavior (HTTP status, DB version) into shared semantic contract suite.

# Shared Contract Example

```text
port.findById(missing)
→ same semantic absence across implementations
```

But:

```text
HTTP adapter 404 translation
```

remains HTTP-specific.

# InMemory Distinction

InMemory repositories support Use Case tests.

They are not proof that:

```text
HTTP mapping
storage mapping
IndexedDB lifecycle
auth
cancellation
provider integration
```

works.

Do not substitute one for the other.

# Error Matrix

Build only accepted error cases.

Example:

| External/storage event | Inward semantic |
|---|---|
| 404 lookup | none |
| 401 after refresh failure | unauthenticated |
| network offline | unavailable |
| schema mismatch | malformed_external_data |
| abort | cancelled |
| corrupt storage | corrupt_data |

Do not make every adapter expose the same exhaustive error taxonomy if the port does not need it.

# Error Identity

Prefer typed/stable errors/codes.

Avoid localized text assertions.

Do not assert vendor stack traces.

# Network Error

Simulate using MSW/test server network failure.

Do not simulate with:

```ts
jest.spyOn(global, "fetch").mockRejectedValue(...)
```

unless fetch itself is the approved adapter boundary under test.

# Timeout

If timeout belongs to HTTP client, keep detailed tests there.

Adapter may need only representative semantic propagation.

# Retry

Same policy:

- HTTP client owns generic retry;
- adapter tests verify adapter-specific behavior only.

Do not duplicate generic retry matrix across every repository.

# Pagination

Test when port exposes pagination.

Verify:

```text
external cursor/page
→ inward page semantics
```

and next-page request mapping.

Do not leak provider page envelopes inward.

# Sorting / Filtering

Verify mapping where port supports semantic filters/sort.

Do not test feature UI filter state here.

# Upload

Adapter tests may verify:

```text
FormData
headers
filename/metadata
response mapping
cancellation
```

if adapter owns upload semantics.

Do not assert DOM file picker behavior here.

# Streaming

Adapter tests may verify:

```text
stream decode
semantic chunks
cancellation
cleanup
malformed stream
```

if applicable.

Use a real/test server where MSW cannot faithfully prove streaming behavior.

# Browser Capabilities

Adapters for clipboard/file picker/navigation/browser APIs should use:

- real browser integration test;
- project emulator;
- capability-specific fake only when it is the actual technical boundary.

Do not test React hook behavior here.

# Security

Adapter tests should verify security-sensitive boundary behavior when accepted:

- no auth header on public endpoint;
- auth on protected endpoint;
- tenant/resource identifier mapping;
- no token logging;
- sensitive storage not written;
- provider error sanitized inward.

Do not turn adapter tests into a full security audit.

# Privacy

For storage/provider integrations, verify sensitive fields are not persisted when architecture says they must not be.

Do not dump external payloads into snapshots.

# Test Credentials

Use environment-provided test credentials.

Never commit secrets into fixtures.

# Logging

Avoid logging:

```text
Authorization
cookies
tokens
PII payloads
provider error bodies
```

during tests.

# Determinism

Fast adapter tests should be deterministic.

Control:

```text
fixtures
clock when mapping time
DB lifecycle
network handlers
sandbox seed
```

Sandbox tests may be less deterministic; isolate and classify them.

# Parallelism

Ensure test data/resources do not collide.

For sandbox:

```text
unique test namespace
```

For IndexedDB:

```text
unique DB name per test/suite
```

or reliable reset.

# Cleanup

Always clean:

- server handlers;
- sandbox resources;
- IndexedDB database;
- storage keys;
- fake timers/listeners;
- open connections.

# Provider Contract Drift

A sandbox/contract test is useful to detect drift:

```text
provider changed field/type/enum
→ runtime validation/mapper fails
```

Treat this as boundary compatibility failure.

Do not “fix” by making everything optional.

# Malformed Payload Regression

When provider changes unexpectedly:

```text
fixture captures broken payload
→ regression test
→ mapper/validator update
```

if the new shape is accepted.

Do not weaken validation indiscriminately.

# Test Layering

Recommended:

```text
mapper tests
→ fast exact contract mapping

adapter boundary tests
→ MSW/emulator/storage

provider sandbox tests
→ selective compatibility
```

Do not require sandbox for every PR if cost/latency makes it inappropriate.

# Execution Strategy

Typical:

```text
focused mapper/adapter test
→ related adapter suite
→ browser/storage suite if applicable
→ sandbox suite only under its documented trigger
```

# CI Tags

Separate:

```text
unit
adapter
browser
sandbox
```

according to repository tooling.

Do not silently run credentialed sandbox tests in forks/untrusted PRs.

# Provider Sandbox Gate

Possible status:

```text
SANDBOX_NOT_CONFIGURED
SANDBOX_SKIPPED_BY_POLICY
SANDBOX_AVAILABLE
SANDBOX_UNAVAILABLE
SANDBOX_CONTRACT_PASS
SANDBOX_CONTRACT_FAIL
```

A skipped sandbox test is not proof of compatibility.

# Roadmap Evaluation — 404

Verify:

```text
external 404
→ correct port-specific absence/error semantic
```

# Roadmap Evaluation — Malformed Payload

Verify:

```text
invalid provider structure
→ rejected at boundary
→ stable malformed data semantic
```

# Roadmap Evaluation — Auth Refresh

Verify approved refresh integration without infinite retry and without duplicating the entire HTTP-client test matrix.

# Roadmap Evaluation — Offline State

Verify exact offline semantics:

```text
local data / no data / queued / unavailable
```

as defined.

# Roadmap Evaluation — IndexedDB Mapping

Verify real serialization/round-trip/missing/migration or relevant mapping behavior against browser-like IndexedDB.

# Roadmap Evaluation — Provider Sandbox

Verify real vendor compatibility in a safe sandbox only when project policy requires/permits it.

# Overmocking Audit

Flag:

- adapter replaced by mock;
- `fetch` mocked instead of using approved MSW boundary;
- plain object used as IndexedDB proof;
- provider SDK mocked at every level;
- all technical semantics reduced to `jest.fn()` calls.

Use:

```text
FAITHFUL_ADAPTER_TEST_BOUNDARY
OVERMOCKED_ADAPTER_TEST
BOUNDARY_TOO_EXPENSIVE
SANDBOX_POLICY_REQUIRED
```

# Under-Testing Audit

Flag:

- only happy path;
- no malformed payload;
- no stable error mapping;
- no cancellation where supported;
- no storage corruption/migration;
- no provider drift check where sandbox is critical;
- no auth refresh integration where repository relies on it.

# Final Decision

Use:

```text
FRONTEND_ADAPTER_TESTS_READY
FRONTEND_ADAPTER_TESTS_READY_WITH_CONDITIONS
FAITHFUL_BOUNDARY_REQUIRED
MALFORMED_PAYLOAD_COVERAGE_REQUIRED
AUTH_REFRESH_COVERAGE_REQUIRED
OFFLINE_COVERAGE_REQUIRED
INDEXEDDB_RUNTIME_REQUIRED
PROVIDER_SANDBOX_REQUIRED
PROVIDER_SANDBOX_SKIPPED_BY_POLICY
BLOCKED
```

## Output

Use `assets/frontend-adapter-testing-record.md`.

## Completion Criteria

- [ ] Accepted port and adapter responsibilities were inspected.
- [ ] The real adapter is the System Under Test.
- [ ] A faithful boundary strategy is explicit.
- [ ] MSW/test server/emulator/storage runtime/sandbox is used appropriately.
- [ ] `fetch` internals are not mocked when MSW/equivalent is the approved HTTP test boundary.
- [ ] Request path/method/query/body/headers are verified where adapter-owned.
- [ ] Inbound/outbound mapping is tested.
- [ ] Provider enums/dates/nullability are mapped explicitly where relevant.
- [ ] 404 semantics match the specific port contract.
- [ ] Transport/provider errors become stable inward semantics.
- [ ] Malformed payload/schema mismatch is rejected before leaking inward.
- [ ] Runtime validator behavior is covered without leaking validator internals.
- [ ] Cancellation propagates and remains distinguishable where required.
- [ ] Auth-refresh integration is tested only when accepted by project policy.
- [ ] Refresh cannot loop infinitely.
- [ ] Offline behavior is tested only when the adapter/port actually defines offline semantics.
- [ ] IndexedDB/storage tests use a faithful browser-like boundary rather than a plain object mock.
- [ ] IndexedDB round-trip/missing/migration/transaction semantics are covered as applicable.
- [ ] Storage corruption/version failures are tested where applicable.
- [ ] Provider sandbox tests use test-only credentials/resources and safe lifecycle.
- [ ] Sandbox tests are separated from fast deterministic adapter tests.
- [ ] Shared semantic contract tests are reused when multiple adapters implement one port.
- [ ] Adapter-specific tests still cover technical integration.
- [ ] No React, hook, component, server-state, or Domain business behavior is tested here.
- [ ] No production provider credentials or resources are used.
- [ ] Test resources/handlers/connections are cleaned up.
- [ ] Roadmap evaluations are covered: 404, malformed payload, auth refresh, offline state, IndexedDB mapping, provider sandbox.
- [ ] Final adapter-test status is explicit.

## References

- Read `references/faithful-boundaries-msw-test-servers-and-contract-fixtures.md` first.
- Read `references/http-errors-malformed-payloads-and-cancellation.md`.
- Read `references/auth-refresh-and-http-client-integration-boundaries.md`.
- Read `references/offline-storage-and-cache-semantics.md`.
- Read `references/indexeddb-runtime-mapping-migrations-and-transactions.md`.
- Read `references/provider-sandboxes-emulators-and-contract-drift.md`.
- Read `references/shared-port-contract-tests-and-layering.md`.
- Read `references/frontend-adapter-testing-audit.md` before completion.
