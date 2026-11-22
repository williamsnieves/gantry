---
name: implementing-frontend-http-clients
description: Portable engineering capability `implementing-frontend-http-clients`.
  Use when the harness or a specialist agent explicitly requires this named capability.
---
# Implementing Frontend HTTP Clients

## Purpose

Implement or evolve the repository-approved frontend HTTP abstraction.

The HTTP client is Infrastructure.

It centralizes transport concerns such as:

```text
base URL
headers
authentication
abort signals
decoding
retry policy
correlation IDs
common error translation
observability
file upload
streaming
```

It should prevent repeated raw `fetch` or vendor-client code across features.

The HTTP client is not:

- a repository;
- a Use Case;
- a Domain service;
- a server-state cache;
- a React hook;
- a provider-specific business mapper.

## Governing Standard

Application and feature adapters SHOULD use a project HTTP abstraction rather than calling `fetch` or a vendor client everywhere.

Direct `fetch` is allowed inside:

```text
approved HTTP implementation
OR
intentionally isolated adapter
```

The HTTP abstraction MAY own:

- base URL;
- headers;
- authentication;
- abort signals;
- decoding;
- retry policy;
- correlation IDs;
- common error translation;
- observability.

Network failure, authorization failure, malformed payload, and cancellation MUST remain distinguishable where the application needs to react differently.

## Use When

- The project lacks one approved HTTP abstraction.
- Raw `fetch` is duplicated across multiple adapters/features.
- Auth/header injection is repeated.
- Cancellation semantics are inconsistent.
- HTTP errors leak directly into repositories/Application.
- JSON decoding is duplicated.
- Retry behavior needs centralized policy.
- Correlation IDs or tracing must be standardized.
- Upload behavior needs a consistent transport API.
- Streaming responses need an explicit transport boundary.
- Existing HTTP abstraction needs to evolve without changing inward contracts.

## Do Not Use When

- The task is to design repository ports.
- The task is to map provider payloads into Domain/Application models.
- The task is runtime-validation policy for external data.
- The task is server-state caching or SWR/React Query.
- The task is component/hook data fetching.
- A direct `fetch` inside one intentionally isolated adapter is already the accepted project policy and no shared abstraction is needed.
- The proposed change would introduce a new HTTP library without approval.
- The proposed HTTP client is merely a generic business service layer.

## Inputs

- Existing HTTP abstraction, if any.
- Existing HTTP/vendor library choice.
- Base URL/configuration strategy.
- Authentication strategy.
- Header policy.
- Correlation/tracing policy.
- Error taxonomy.
- Cancellation policy.
- Retry policy.
- Runtime validation policy.
- Upload requirements.
- Streaming requirements.
- Observability/logging policy.
- Security/privacy requirements.
- Existing adapter contracts.
- Test strategy.
- Repository-local `AGENTS.md`.

## Outputs

- HTTP abstraction implementation/evolution.
- Stable request/response transport contract.
- Authentication/header behavior.
- Abort/cancellation support.
- Decode behavior.
- Stable transport error taxonomy.
- Retry behavior.
- Upload support when required.
- Streaming support when required.
- Observability/correlation behavior.
- Focused HTTP client tests.
- HTTP client implementation record.

## Core Workflow

```text
inspect existing abstraction
→ confirm transport policy
→ define request contract
→ define authentication/headers
→ define cancellation
→ define decode/error semantics
→ define retry
→ implement upload/streaming when required
→ add observability
→ test transport behaviors
```

## Readiness Gate

Use one:

```text
READY_TO_IMPLEMENT_FRONTEND_HTTP_CLIENT
READY_WITH_CONDITIONS
NO_SHARED_HTTP_CLIENT_REQUIRED
HTTP_LIBRARY_POLICY_REQUIRED
AUTH_POLICY_REQUIRED
ERROR_TAXONOMY_REQUIRED
RETRY_POLICY_REQUIRED
STREAMING_POLICY_REQUIRED
SECURITY_POLICY_REQUIRED
BLOCKED
```

Do not select a new HTTP library automatically.

# HTTP Client Scope

The HTTP client owns transport-level concerns.

Typical API:

```text
get
post
put
patch
delete
request
upload
stream
```

according to repository conventions.

It may expose a single typed `request` primitive plus convenience helpers.

Do not add methods for product intentions such as:

```text
applyPromotion
saveDraft
submitPayment
```

Those belong to repositories/adapters/ports.

# Request Contract

A transport request may include:

```text
path/url
method
query
headers
body
signal
timeout
response mode
```

Keep the contract generic enough for Infrastructure but not provider/business-specific.

Do not include:

- React callbacks;
- Domain entities;
- component state;
- Use Cases;
- business status enums;
- design-system concerns.

## URL Ownership

The HTTP client may own:

```text
base URL
common path joining
query serialization
```

Adapters own endpoint paths for their providers unless repository architecture centralizes endpoint definitions.

Do not place business endpoint names into the HTTP core.

# Authentication

Authentication injection should follow the accepted project strategy.

Possible patterns:

```text
Authorization header
cookie-based session
signed request
CSRF header
service-specific token
```

Do not assume bearer tokens.

The HTTP client may receive a semantic token provider/config dependency.

Avoid importing user session UI state directly.

## Token Injection

Token injection must:

- occur at request time when tokens can rotate;
- avoid stale module-level token capture;
- avoid logging tokens;
- avoid copying secrets into URLs;
- preserve requests that intentionally require no auth.

Classify:

```text
AUTH_REQUIRED
AUTH_OPTIONAL
AUTH_DISABLED
```

Do not force auth on public endpoints.

## Token Refresh

Do not implement refresh automatically unless repository policy defines it.

If refresh exists, define:

- single-flight behavior;
- retry after refresh;
- refresh failure;
- logout/session invalidation ownership;
- cancellation.

Avoid infinite 401 → refresh loops.

# Headers

Centralize stable common headers where appropriate:

```text
Accept
Content-Type
Authorization
correlation/request ID
locale
client/version
```

Only inject headers justified by policy.

Adapters may add provider-specific headers through request options.

Do not allow arbitrary higher layers to mutate global header state unsafely.

# Content Type

Do not set JSON `Content-Type` blindly for:

- FormData;
- multipart uploads;
- binary bodies;
- streaming bodies;
- requests with no body.

Let the runtime/library generate multipart boundaries.

# Query Serialization

Define consistent behavior for:

- arrays;
- booleans;
- null/undefined;
- dates;
- repeated keys;
- encoding.

Do not leak provider query conventions into Application.

Adapters map semantic filter objects to transport query values.

# Body Serialization

The HTTP client may serialize JSON for plain transport payloads.

Do not serialize Domain classes blindly.

Adapters should map internal models into outward transport-safe shapes first.

# Response Modes

Potential transport response modes:

```text
json
text
blob
arrayBuffer
stream
empty
```

Only support modes the repository needs.

Do not assume every 2xx response contains JSON.

# JSON Decoding

JSON decoding should distinguish:

```text
valid JSON
empty body
malformed JSON
wrong content type
```

according to accepted policy.

A malformed payload should not become:

```text
undefined
{}
null
```

silently.

Expose a stable transport/contract error.

# Runtime Validation Boundary

The HTTP client may decode JSON but should not automatically own provider schema validation unless repository policy explicitly places it there.

Typical separation:

```text
HTTP client
→ decode transport

adapter
→ validate/map provider payload
```

The later `validating-external-frontend-data` skill decides runtime validation.

Do not embed feature schemas into the common HTTP client.

# Stable Error Taxonomy

Define transport errors that adapters can translate further if needed.

Possible categories:

```text
NETWORK
TIMEOUT
UNAUTHENTICATED
FORBIDDEN
NOT_FOUND
CONFLICT
RATE_LIMITED
SERVER
MALFORMED_RESPONSE
CANCELLED
UNKNOWN
```

Use only distinctions the infrastructure/application architecture needs.

Do not expose vendor-native errors directly.

## Error Object

A stable error may include:

```text
kind
status?
correlationId?
retryAfter?
safeMessage?
cause? (Infrastructure-only)
```

Avoid returning raw response bodies with sensitive data.

Do not make `message` the only machine-readable discriminator.

# HTTP Status Mapping

Common mapping may be centralized when semantics are transport-generic:

```text
401 → UNAUTHENTICATED
403 → FORBIDDEN
404 → NOT_FOUND
409 → CONFLICT
429 → RATE_LIMITED
5xx → SERVER
```

But provider-specific semantic meanings belong in adapters.

Example:

```text
409 = promotion already applied
```

is not a generic HTTP-client interpretation.

The HTTP client can expose `CONFLICT` plus safe status; the adapter interprets provider semantics.

# 401 Handling

Define one policy:

```text
RETURN_UNAUTHENTICATED_ERROR
TRIGGER_ACCEPTED_REFRESH_FLOW
DELEGATE_TO_SESSION_BOUNDARY
```

Do not:

- redirect from the HTTP core unless project policy explicitly requires it;
- call React router;
- mutate component state;
- swallow and return undefined.

# 403 Handling

403 should remain distinguishable from 401 when the UI/Application may react differently.

Do not collapse both to generic auth failure without accepted policy.

# 404 Handling

The HTTP client generally exposes transport `NOT_FOUND`.

Repository adapters decide whether:

```text
NOT_FOUND → undefined
```

according to the repository port contract.

The HTTP client should not return `undefined` for all 404 responses globally.

# 409 Handling

Expose stable conflict semantics.

Do not infer domain meaning globally.

Adapters map conflict to:

```text
duplicate
already applied
version conflict
```

when provider contract defines it.

# 429 Handling

Expose rate-limit semantics when useful.

Potential metadata:

```text
retryAfter
```

if safely parseable.

Do not automatically retry non-idempotent operations merely because the server returned 429.

# 5xx Handling

Keep server failure distinct from network failure.

This helps higher layers choose:

- retry;
- user messaging;
- telemetry.

Do not expose provider stack traces.

# Network Errors

Differentiate request transport failure from HTTP response errors.

Network failures may include:

- DNS;
- connection reset;
- offline;
- browser transport rejection.

Map vendor/runtime details into stable `NETWORK`.

Do not claim precise cause unless reliably known.

# Timeout

If timeouts are supported, define:

- source: client timeout versus server status;
- error kind;
- cancellation interaction;
- cleanup.

Do not simulate timeouts with leaked timers.

A timeout is usually distinct from user cancellation.

# Cancellation

Support abort/cancellation where requests can become obsolete.

For native fetch this is typically `AbortSignal`.

For vendor clients, adapt accepted cancellation into stable behavior.

Cancellation should map to:

```text
CANCELLED
```

not `NETWORK` or `UNKNOWN`.

## Abort Signal Propagation

If caller provides a signal:

```text
adapter
→ HTTP client
→ transport
```

must preserve it.

Do not create a new unrelated AbortController that ignores caller cancellation.

If timeout and caller cancellation coexist, define signal composition.

# Retry Policy

Retry must be intentional.

Classify:

```text
NO_RETRY
SAFE_IDEMPOTENT_RETRY
RETRY_WITH_POLICY
ADAPTER_OWNS_RETRY
SERVER_STATE_OWNS_RETRY
```

Do not create hidden retry layers.

## Safe Retry Defaults

Potentially retryable:

- selected network failures;
- selected 5xx;
- 429 with policy;
- idempotent GET/HEAD;
- explicitly idempotent commands with server support.

Do not automatically retry:

- payment submit;
- non-idempotent POST;
- destructive commands;
- upload finalize;
- provider action with unknown idempotency.

## Retry Count

Use bounded attempts.

No infinite loops.

Record:

- attempts;
- backoff;
- jitter;
- retryable kinds/statuses;
- idempotency requirement;
- cancellation.

Do not invent numbers if repository policy already defines them.

# Backoff

If accepted:

```text
fixed
linear
exponential
exponential + jitter
retry-after-aware
```

Tests should use fake/virtual time when practical.

Do not make tests sleep real seconds.

# Retry-After

When policy supports 429/503 `Retry-After`:

- parse safely;
- cap according to policy;
- remain cancellable.

Do not trust arbitrary huge values blindly.

# Correlation IDs

The client MAY own correlation/request IDs.

Possible behavior:

- generate if absent;
- propagate provided ID;
- capture response ID;
- attach safe ID to error.

Do not use personally identifying data in correlation IDs.

# Observability

HTTP client observability may record:

```text
method
route template or sanitized path
status
duration
error kind
retry count
correlation ID
```

Do not log:

- access tokens;
- cookies;
- request bodies by default;
- PII;
- sensitive query params;
- file contents.

Follow accepted privacy policy.

# Logging

Avoid `console.log` in production transport code unless repository policy explicitly allows it.

Use project logging/observability abstraction if one exists.

Do not create a new observability stack as part of the HTTP client task.

# File Upload

File upload behavior must be explicit.

Potential input:

```text
FormData
Blob
File
ArrayBuffer
stream
```

depending on repository/runtime policy.

The common HTTP client may support multipart or binary requests.

Adapters should own:

- provider field names;
- endpoint path;
- semantic metadata mapping.

## Multipart

Do not set multipart boundary manually when using browser `FormData`.

Do not JSON-stringify files.

Define:

- auth/header behavior;
- cancellation;
- progress support;
- retry policy.

## Upload Progress

Progress is transport-specific.

If project HTTP library/browser capability supports it and product needs it, expose a transport-level progress callback/stream to Infrastructure consumers.

Do not expose React state setters.

Do not promise upload progress with `fetch` where runtime does not provide it unless another approved mechanism exists.

# Streaming Responses

Streaming must be modeled separately from ordinary JSON.

Possible forms:

```text
ReadableStream
AsyncIterable
text/event stream
line-delimited JSON
binary stream
```

The common HTTP abstraction may expose a transport stream.

Adapters own:

- provider protocol;
- event decoding;
- semantic mapping.

Do not return provider-specific stream events from the common client.

## Stream Cancellation

Streaming must support cancellation and resource cleanup.

On cancellation:

- abort transport;
- close readers where required;
- stop decode loops;
- expose stable cancellation semantics.

# SSE

If SSE is used, decide whether the project uses:

- native EventSource;
- fetch streaming;
- provider library.

Do not force SSE into generic `getJson`.

A specialized transport abstraction may be appropriate.

# File Download

Downloads may use:

```text
blob
arrayBuffer
stream
```

according to product need.

Filename/content-disposition parsing may belong to a provider adapter if provider-specific.

Do not trigger browser download/navigation inside the core HTTP client.

# Credentials and Cookies

Define fetch/vendor credentials policy:

```text
same-origin
include
omit
```

according to backend/session architecture.

Do not enable cross-origin credential sending universally without policy.

# CSRF

If cookie-authenticated mutation requires CSRF protection, the HTTP abstraction may inject accepted CSRF headers/tokens.

Do not invent CSRF behavior without backend policy.

# CORS

CORS is enforced by browser/server configuration.

The HTTP client should not attempt fake client-side “CORS fixes.”

Do not add unsafe proxy behavior to bypass policy.

# Base URL

Base URLs should come from accepted configuration.

Avoid hardcoding production origins.

Do not expose secret backend credentials via public environment variables.

Validate environment handling according to framework/runtime.

# Environment Separation

Support accepted environment configuration:

```text
development
test
staging
production
```

without changing application contracts.

Do not make feature code choose environment URLs.

# Server / Client Runtime

If the frontend supports SSR/server execution, classify the client:

```text
CLIENT_ONLY_HTTP_CLIENT
SERVER_ONLY_HTTP_CLIENT
ISOMORPHIC_HTTP_CLIENT
SPLIT_CLIENTS
```

Account for:

- cookies;
- request headers;
- per-request auth;
- server secrets;
- absolute URLs;
- request-scoped correlation.

Do not use a singleton server HTTP client that captures first-request auth state.

# Per-Request Context

On server runtime, mutable request context MUST NOT leak through accidental singletons.

Safe patterns:

```text
create client per request
OR
stateless singleton + explicit per-request auth/context
```

according to project design.

# Client Singleton

A stateless browser HTTP client may be safely shared if auth/config lookup happens per request.

Do not cache stale user tokens inside singleton construction.

# Interceptors / Middleware

If the chosen library supports interceptors/middleware, use them carefully for cross-cutting transport concerns.

Good:

- auth injection;
- correlation;
- timing;
- stable error normalization.

Weak:

- feature-specific DTO mapping;
- navigation;
- toast display;
- business retries;
- repository semantics.

Avoid hidden global mutable interceptor registration.

# Vendor Library Independence

The HTTP abstraction may wrap:

```text
fetch
Axios
ky
ofetch
framework fetch
```

according to repository choice.

Do not expose vendor request/response/error types inward.

Changing the underlying transport should not require rewriting repositories except where behavior genuinely differs.

# Native Fetch

Direct `fetch` inside the approved client is valid.

Important fetch behaviors to handle explicitly:

- fetch does not reject on HTTP 4xx/5xx;
- abort throws runtime-specific error;
- body can be consumed once;
- malformed JSON throws during decode;
- empty body needs explicit handling;
- credentials differ by configuration.

# Axios-like Clients

If repository uses Axios or similar:

- normalize vendor errors;
- do not expose `AxiosError`;
- normalize cancellation;
- avoid feature-specific interceptors in the global client;
- respect upload progress support.

Do not migrate away merely because fetch exists.

# Framework Fetch

Framework-enhanced fetch may add:

- cache;
- revalidation;
- server tags;
- deduplication.

Decide whether those semantics belong in this HTTP abstraction or a higher Infrastructure/server-state layer.

Do not leak framework cache options into Application ports.

# Security

The HTTP client MUST avoid:

- token logging;
- secret query params;
- unsafe credential forwarding;
- leaking response bodies in public errors;
- including server-only secrets in client bundles.

Redact sensitive headers in observability.

# Privacy

Do not log request/response payloads by default.

If diagnostics require payload logging, follow explicit redaction and environment policy.

# Error Causes

Infrastructure may preserve an internal `cause` for diagnostics.

Do not expose raw causes to Presentation.

Ensure serialized errors sent across server/client boundaries are safe.

# API Surface Restraint

Prefer a small stable API.

Do not create:

```text
100 convenience methods
provider-specific helpers
business endpoint methods
feature callbacks
```

The abstraction should be boring and predictable.

# Migration From Raw Fetch

When migrating:

```text
raw fetch adapters
→ approved HTTP client
```

preserve:

- endpoint behavior;
- auth;
- headers;
- cancellation;
- status handling;
- decoding;
- tests.

Do not combine migration with unrelated repository redesign unless necessary.

# Direct Fetch Exception

Direct `fetch` may remain in an intentionally isolated adapter when:

- project policy permits it;
- sharing adds no value;
- behavior is specialized;
- no cross-cutting transport concern is duplicated.

Record the exception.

Do not force all network traffic through one abstraction dogmatically.

# Test Strategy

HTTP client tests should focus on transport behavior.

Test:

- token injection;
- headers;
- abort signal;
- malformed JSON;
- 401;
- 403/404/409/429 when relevant;
- network failure;
- timeout;
- retry policy;
- empty response;
- upload;
- streaming;
- correlation/observability safely.

Do not test business mapping here.

# Test Boundary

Prefer a realistic transport boundary:

```text
mock server
test server
fetch stub only if repository convention accepts it
```

The HTTP implementation itself may need lower-level transport substitution.

Use the repository-approved approach.

Do not mock the HTTP client when testing the HTTP client.

# Token Injection Evaluation

Verify:

```text
current token
→ request header
```

including:

- token rotation;
- no stale capture;
- no header when auth disabled;
- redaction from logs.

# Abort Signal Evaluation

Verify:

```text
caller signal
→ transport request
→ abort
→ stable CANCELLED error
```

No arbitrary sleep.

# Malformed JSON Evaluation

Verify a 2xx response with malformed JSON becomes:

```text
MALFORMED_RESPONSE
```

or repository-approved stable equivalent.

Do not return empty success.

# 401 Evaluation

Verify accepted policy:

```text
401
→ UNAUTHENTICATED
```

or approved refresh flow.

No React redirect unless explicitly part of transport policy.

# Retry Evaluation

Verify:

- only accepted failures retry;
- attempt bound;
- cancellation stops retry;
- unsafe non-idempotent request does not retry by default;
- backoff uses controlled time.

# File Upload Evaluation

Verify:

- multipart/binary encoding;
- no incorrect JSON Content-Type;
- auth headers;
- cancellation;
- provider field mapping stays outside HTTP core.

# Streaming Response Evaluation

Verify:

- stream exposed according to abstraction;
- chunks/events can be consumed;
- cancellation closes/aborts;
- transport/provider event semantics remain outside core;
- malformed stream behavior is explicit.

# Completion Status

Use:

```text
FRONTEND_HTTP_CLIENT_COMPLETE
FRONTEND_HTTP_CLIENT_COMPLETE_WITH_CONDITIONS
NO_SHARED_HTTP_CLIENT_REQUIRED
RETURN_TO_HTTP_POLICY
RUNTIME_VALIDATION_REQUIRED
RETRY_POLICY_REQUIRED
SECURITY_REVIEW_REQUIRED
BLOCKED
```

## Output

Use `assets/frontend-http-client-implementation-record.md`.

## Completion Criteria

- [ ] Existing HTTP/library policy is preserved or explicitly approved.
- [ ] Raw transport usage is centralized or intentionally isolated.
- [ ] Base URL/configuration is explicit.
- [ ] Authentication injection is request-safe and does not capture stale user state.
- [ ] Sensitive tokens/headers are not logged.
- [ ] Common headers are deliberate.
- [ ] JSON/body encoding handles empty/non-JSON cases correctly.
- [ ] Malformed JSON produces stable failure.
- [ ] Network, timeout, unauthenticated, forbidden, not-found, conflict, rate-limit, server, malformed-response, cancellation, and unknown semantics are distinguishable where needed.
- [ ] 404 is not globally converted to `undefined`.
- [ ] Provider-specific meanings remain in adapters.
- [ ] Caller abort signal is propagated.
- [ ] Cancellation maps to stable cancellation semantics.
- [ ] Retry policy is explicit, bounded, cancellable, and idempotency-aware.
- [ ] Hidden duplicate retry layers are avoided.
- [ ] Correlation/observability is safe and redacted.
- [ ] Upload supports correct multipart/binary behavior when required.
- [ ] Streaming has explicit response and cancellation semantics when required.
- [ ] Server/client runtime and per-request auth lifecycle are safe.
- [ ] Vendor transport types do not leak to adapters/Application.
- [ ] Runtime provider validation remains outside the common client unless policy says otherwise.
- [ ] HTTP client contains no Domain/business mapping, UI state, routing, toast, or React behavior.
- [ ] Tests cover roadmap cases: token injection, abort, malformed JSON, 401, retry, upload, streaming.
- [ ] No new HTTP library, retry library, validation library, or observability stack is introduced without approval.
- [ ] Final implementation status is explicit.

## References

- Read `references/http-client-scope-and-request-contract.md` first.
- Read `references/authentication-headers-and-runtime-lifecycle.md`.
- Read `references/decoding-errors-and-status-mapping.md`.
- Read `references/cancellation-retries-and-idempotency.md`.
- Read `references/uploads-streaming-and-response-modes.md`.
- Read `references/observability-security-and-privacy.md`.
- Read `references/http-client-testing-and-migration.md`.
- Read `references/frontend-http-client-audit.md` before completion.
