---
name: implementing-frontend-repository-adapters
description: Implements frontend repository ports for remote APIs, browser storage, IndexedDB, cache-backed collections, BFFs, or offline persistence. Use when an accepted port and frontend slice require concrete Infrastructure code. Map transport/storage data inward and internal data outward, validate untrusted payloads when required, preserve not-found, cancellation, conflict, unavailable, and malformed-data semantics, support pagination and abort signals, and reuse the approved HTTP/storage abstraction. Do not leak raw responses, provider enums, snake_case, nullable transport quirks, browser handles, or technical exceptions inward; do not add business rules, invent retry policy, call React APIs, or introduce new libraries without an accepted decision.
---

# Implementing Frontend Repository Adapters

## Purpose

Implement a concrete frontend Infrastructure adapter for an accepted repository port.

Supported implementations include:

```text
HTTP API
BFF
IndexedDB
localStorage/sessionStorage
Cache Storage
in-memory/cache-backed collection
offline persistence
```

The adapter must:

- implement the port exactly;
- use product language at the inward boundary;
- own provider/storage details;
- map external data inward;
- map internal data outward;
- preserve stable absence and failure semantics;
- remain replaceable;
- contain no business policy.

## Governing Direction

```text
Presentation / Infrastructure
→ Application
→ Domain
```

For a repository:

```text
Domain or Application port
← Infrastructure adapter
← HTTP / browser storage / IndexedDB / cache
```

Infrastructure may depend inward.

Domain and Application must not import the adapter.

## Use When

- A repository port is accepted.
- A vertical slice needs a concrete remote or browser-backed implementation.
- Raw API or storage data must be mapped before crossing inward.
- An HTTP client, IndexedDB wrapper, or storage abstraction is already approved.
- Pagination, dates, enums, optional fields, abort signals, or stable errors require implementation.
- A remote implementation must coexist with local/offline storage.
- A legacy API must be isolated behind a semantic port.

## Do Not Use When

- The port has not been designed or accepted.
- The task is to select an HTTP or validation library.
- The task is to design server-state hooks.
- The behavior belongs directly to a simple approved data helper under Profile A and no repository port is justified.
- Business invariants or orchestration are unresolved.
- The request is only adapter design or architecture review.
- The task is backend-only.

## Inputs

- Accepted repository port.
- Request/response or Domain/Application types.
- Vertical-slice plan.
- Architecture-profile decision.
- External API/storage contract.
- Approved HTTP/storage/database abstraction.
- Runtime-validation decision.
- Stable application/domain errors.
- Pagination, cancellation, caching, and retry policy.
- Repository-local `AGENTS.md`.
- Existing adapter and testing conventions.

## Outputs

- Concrete repository adapter.
- Transport/storage types.
- Inbound and outbound mappers.
- Runtime validation where required.
- Stable absence/failure translation.
- Pagination and cancellation behavior.
- Resource lifecycle and cleanup.
- Focused adapter tests.
- Implementation record.

## Core Workflow

```text
accepted port and contract
→ inspect approved infrastructure
→ define exact external types
→ implement inbound/outbound mapping
→ translate absence and failures
→ add cancellation/pagination/lifecycle
→ test against real or faithful boundary
→ validate no technical leakage
```

## Readiness Gate

Use one:

```text
READY_TO_IMPLEMENT_FRONTEND_ADAPTER
READY_WITH_CONDITIONS
PORT_DECISION_REQUIRED
EXTERNAL_CONTRACT_REQUIRED
RUNTIME_VALIDATION_DECISION_REQUIRED
FAILURE_SEMANTICS_REQUIRED
PAGINATION_DECISION_REQUIRED
STORAGE_MIGRATION_DECISION_REQUIRED
BLOCKED
```

Stop when a missing decision changes the inward contract or data integrity.

## Port Compliance

The adapter must implement the accepted port without weakening it.

Verify:

- method names use product language;
- input/output types match;
- `undefined`, optional result, or semantic error behavior is preserved;
- cancellation and pagination are represented as accepted;
- no provider-only method is added to the inward contract;
- no generic `getJson(path)` or `request(options)` leaks inward.

Do not reshape the port merely because the provider API is inconvenient.

## Adapter Responsibilities

The adapter owns:

- URL/path or storage key construction;
- HTTP/storage/IndexedDB mechanics;
- transport/storage types;
- runtime decoding where required;
- naming conversion;
- date and enum mapping;
- optionality/nullability mapping;
- pagination envelopes/cursors;
- technical error translation;
- abort/cancellation forwarding;
- resource lifecycle;
- technical observability and redaction.

It does not own:

- eligibility;
- workflow decisions;
- authorization policy beyond forwarding trusted credentials/context through approved infrastructure;
- UI state;
- cache invalidation owned by server-state tooling;
- retry policy not defined by project infrastructure.

## External Types

External types should match the external contract exactly.

Example concerns:

```text
snake_case
nullable fields
provider status names
string dates
pagination envelope
legacy optional nesting
```

Keep them in Infrastructure.

Do not alias an external response type as a Domain entity merely because the shapes currently match.

## Inbound Mapping

Map:

```text
external payload
→ validation/decoding
→ external type
→ Domain/Application type
```

Handle explicitly:

- IDs;
- dates/time zones;
- numeric precision;
- enums/discriminated states;
- nullable versus optional;
- nested optional objects;
- unknown provider values;
- pagination;
- legacy fields;
- external references.

Do not spread raw payloads inward.

## Outbound Mapping

Map:

```text
Domain/Application input
→ transport/storage request
```

Handle:

- naming conventions;
- date serialization;
- enum/provider code translation;
- omitted versus explicit null fields;
- multipart/file payloads when accepted;
- optimistic or concurrency tokens;
- pagination and filters;
- stable idempotency/correlation values supplied by the caller.

Do not create business decisions while mapping.

## Runtime Validation

Use runtime validation when remote or stored data is untrusted or structurally important.

The adapter may use the project-approved validator.

Possible outcomes:

```text
VALID
CONTRACT_MISMATCH
UNSUPPORTED_VARIANT
CORRUPT_STORED_DATA
```

TypeScript interfaces alone do not validate runtime payloads.

Do not add a validation library without an accepted repository decision.

If validation is intentionally omitted, document why the boundary is trusted and what detects drift.

## Absence Semantics

Distinguish:

```text
FOUND
NOT_FOUND
EMPTY_COLLECTION
FORBIDDEN
UNAVAILABLE
MALFORMED_RESPONSE
```

Typical mapping:

```text
HTTP 404 for lookup
→ undefined
```

only when the port defines absence as optional.

A 404 for a command or nested endpoint may be a semantic error instead.

Do not convert every 404 to `undefined`.

Do not convert forbidden or unavailable to empty data.

## Failure Translation

Translate technical failures into stable semantics.

Potential stable categories:

```text
NotFound
Conflict
Forbidden
Unauthenticated
Unavailable
Timeout
Cancelled
ContractMismatch
StorageUnavailable
QuotaExceeded
Unknown
```

Preserve original cause internally when safe and useful.

Do not expose:

- raw `Response`;
- Axios/fetch error;
- DOMException as primary semantics;
- SDK exception;
- provider error payload;
- SQL/IndexedDB implementation details.

Do not swallow network or storage errors.

## Cancellation

Forward the accepted cancellation mechanism.

For HTTP this may be an `AbortSignal`.

Define:

- signal input;
- abort propagation;
- cancellation translation;
- whether cancellation is returned or thrown;
- no retry after caller cancellation;
- no logging as product failure unless policy requires it.

Cancellation does not prove a remote mutation did not complete.

## HTTP Adapter

Reuse the approved HTTP abstraction.

It may already own:

- base URL;
- authentication;
- headers;
- decoding;
- common error mapping;
- retry policy;
- correlation IDs;
- telemetry;
- abort propagation.

The repository adapter owns feature-specific:

- endpoint;
- request/response types;
- mapping;
- feature-specific error semantics;
- pagination.

Do not call raw `fetch` throughout feature code.

Direct `fetch` is acceptable only inside the approved HTTP layer or intentionally isolated adapter per project policy.

## Retry Policy

Do not invent retries in the repository adapter.

Follow the accepted HTTP/storage policy.

Never automatically retry unsafe mutations unless:

- idempotency semantics are explicit;
- the project policy allows it;
- duplicate side effects are controlled.

Expose retryable stable semantics to the caller when UI/server-state owns retry.

## Authentication and Tenant Context

Use the approved trusted infrastructure.

Do not:

- accept arbitrary auth tokens through component props;
- read user identity from feature form data;
- construct tenant authority from untrusted payloads;
- embed secrets.

The adapter may forward accepted tenant/resource identifiers required by the external contract, but authorization decisions remain in the proper boundary.

## Pagination

Map external pagination into the accepted inward model.

External examples:

```text
page/pageSize/total
offset/limit
cursor/next_cursor
links
continuation token
```

Inward examples:

```text
Page<T>
CursorPage<T>
{ items, nextCursor }
```

Define:

- empty page;
- missing next cursor;
- malformed cursor;
- stable ordering;
- duplicate items;
- cancellation;
- filters/sort mapping.

Do not expose the provider envelope directly.

## Streaming

When the accepted port supports streaming:

- preserve stream lifecycle;
- map each event/chunk;
- handle malformed frames;
- cancellation;
- reconnect policy owner;
- completion;
- partial failure;
- cleanup.

Do not buffer an unbounded stream merely to match a collection API.

Do not implement streaming if the port does not express it.

## File Uploads

For file/multipart adapters define:

- accepted file/browser type at the outer boundary;
- metadata mapping;
- content type;
- size limits from accepted policy;
- cancellation;
- progress ownership;
- retry/idempotency;
- response mapping.

Do not pass `File` or `Blob` into Domain unless the project explicitly models browser objects at an outer Application boundary.

## IndexedDB Adapter

The adapter owns:

- database name/version;
- object stores and indexes;
- transaction scope;
- request-to-promise mechanics;
- serialization;
- migrations;
- corrupt/legacy data handling;
- quota and blocked-upgrade failures;
- connection lifecycle.

The inward port must not expose:

- `IDBDatabase`;
- `IDBRequest`;
- object-store names;
- transaction handles.

## IndexedDB Transactions

Define:

- read/write transaction;
- stores involved;
- atomicity;
- abort behavior;
- error translation;
- connection close;
- version-change behavior.

Do not keep transactions open across remote network calls.

Do not claim atomic behavior across IndexedDB and a remote API.

## Browser Storage Adapter

For local/session storage define:

- key ownership;
- schema/version;
- serialization;
- parsing;
- quota;
- privacy;
- SSR availability;
- cross-tab behavior;
- cleanup/removal;
- corrupt data policy.

Do not treat browser storage as trusted.

Do not store secrets or sensitive tokens unless an accepted security design explicitly permits it.

## Cache-Backed Adapter

A cache-backed implementation must define:

- authoritative source;
- read-through/write-through/write-back behavior;
- TTL/staleness;
- invalidation;
- cache miss;
- conflict;
- offline semantics;
- reconciliation owner.

Do not create a second competing cache over SWR/React Query without an accepted architecture.

## Offline Adapter

When offline behavior is accepted, define:

- local authoritative or provisional state;
- operation queue;
- identity;
- ordering;
- duplicate prevention;
- retry;
- reconciliation;
- conflict policy;
- tombstones/deletes;
- migration;
- observability.

Do not infer offline support because IndexedDB exists.

## Dates and Time Zones

Map string dates explicitly.

Define:

- accepted format;
- UTC/offset behavior;
- invalid date handling;
- business date versus timestamp;
- serialization;
- clock ownership.

Do not allow invalid `Date` objects inward silently.

Do not remove offsets without an accepted semantic decision.

## Enums and Unknown Values

Map external enum values explicitly.

Use one policy:

```text
MAP
REJECT
PRESERVE_AS_UNKNOWN
COMPATIBILITY_MAP
```

Do not use unchecked type casts.

Unknown provider values must not silently become a valid Domain state.

## Nullability and Optionality

Distinguish:

```text
field absent
field present as null
field present with value
```

Map according to accepted semantics.

Do not convert every `null` to `undefined` automatically if the distinction matters.

Do not let optional nested response access crash mapping.

## Numeric Values

For money, percentages, large IDs, and precise quantities:

- inspect external representation;
- avoid unsafe floating-point conversion;
- preserve precision;
- validate range;
- map units explicitly.

Do not coerce malformed values silently.

## Observability

Record technical evidence without leaking sensitive data.

Potential telemetry:

- endpoint/storage operation;
- duration;
- failure category;
- contract mismatch;
- cancellation;
- cache source;
- migration result.

Do not log:

- tokens;
- secrets;
- complete sensitive payloads;
- personal data without policy;
- raw provider errors containing credentials.

## Error Ownership

The adapter translates technical failures.

Application/Domain decide semantic workflow response.

Presentation decides how stable errors are displayed.

Do not map errors directly to localized UI strings inside the repository adapter.

## Testing Strategy

Test the adapter boundary directly.

### HTTP Repository

Use a faithful HTTP boundary or approved request-mocking layer.

Verify:

- path/method/headers through approved client;
- request mapping;
- response mapping;
- not-found;
- forbidden/unavailable;
- malformed JSON/schema;
- abort;
- date/enum/null mapping;
- pagination;
- no raw response leakage.

Do not mock the adapter itself.

### IndexedDB/Storage

Use a real isolated browser-like implementation where feasible.

Verify:

- round trip;
- missing value;
- migration;
- corrupt data;
- transaction failure;
- quota/storage unavailable;
- cleanup;
- SSR unavailable behavior where applicable.

A plain object mock does not prove IndexedDB/storage mapping or transaction behavior.

## Contract Tests

When several adapters implement one port, reuse a shared semantic contract suite.

The suite should assert:

- input/output semantics;
- absence;
- stable errors;
- ordering/pagination;
- cancellation when supported;
- no provider leakage.

Adapter-specific suites still verify technical integration.

## Test Doubles

Application/Use Case tests should use InMemory implementations or explicit doubles.

Adapter tests should exercise the real adapter against a faithful boundary.

Do not use an InMemory repository as proof that the HTTP or IndexedDB adapter works.

## Implementation Order

Preferred order:

```text
1. accepted port and semantics
2. exact external/storage types
3. inbound mapper tests
4. outbound mapper tests
5. adapter happy path
6. absence and stable failures
7. cancellation
8. pagination/stream/file behavior
9. real boundary tests
10. architecture and type checks
```

Use TDD according to repository policy.

## Architecture Constraints

Verify:

- adapter lives in Infrastructure;
- it imports inward types/ports only;
- Domain/Application do not import it;
- React components/hooks do not instantiate it directly unless they are the explicit composition boundary;
- composition chooses the concrete implementation;
- transport/storage types remain Infrastructure-local.

## Completion Status

Use:

```text
FRONTEND_ADAPTER_IMPLEMENTED
FRONTEND_ADAPTER_IMPLEMENTED_WITH_CONDITIONS
PORT_OR_CONTRACT_DECISION_REQUIRED
VALIDATION_FAILED
BOUNDARY_TEST_BLOCKED
BLOCKED
```

## Output

Use `assets/frontend-repository-adapter-implementation-record.md`.

## Completion Criteria

- [ ] Accepted port and external/storage contract were inspected.
- [ ] Approved HTTP/storage abstraction is reused.
- [ ] External types match the actual contract.
- [ ] Inbound and outbound mapping are explicit.
- [ ] Runtime validation follows the accepted policy.
- [ ] Dates, enums, nullability, nesting, numeric precision, and pagination are handled.
- [ ] Absence is distinct from forbidden, unavailable, malformed, and empty.
- [ ] Technical failures become stable semantics and are not swallowed.
- [ ] Cancellation is forwarded and classified correctly.
- [ ] Retry policy is not invented.
- [ ] HTTP/storage/browser implementation details do not leak inward.
- [ ] No business rules, React state, or UI strings exist in the adapter.
- [ ] IndexedDB/storage lifecycle and migrations are explicit when applicable.
- [ ] Cache/offline authority and reconciliation are explicit when applicable.
- [ ] Sensitive values are redacted.
- [ ] Focused mapper and real/fidelity boundary tests pass.
- [ ] Shared port contract tests are used when multiple implementations exist.
- [ ] Dependency direction and composition are correct.
- [ ] No new library or architecture policy was introduced silently.

## References

- Read `references/adapter-boundaries-and-mapping.md` first.
- Read `references/http-errors-cancellation-and-pagination.md` for remote adapters.
- Read `references/indexeddb-storage-cache-and-offline.md` for browser persistence.
- Read `references/runtime-validation-dates-enums-and-nullability.md` for data safety.
- Read `references/frontend-adapter-testing-and-contracts.md` before completion.
- Read `references/frontend-repository-adapter-audit.md` before finalizing.
