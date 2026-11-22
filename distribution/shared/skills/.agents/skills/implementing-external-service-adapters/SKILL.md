---
name: implementing-external-service-adapters
description: Implements provider-specific Infrastructure adapters behind accepted Application ports. Use when an external-service port already exists and must be backed by an SDK, HTTP API, messaging service, cloud service, clock, identity provider, payment provider, or notification provider. Maps Application inputs to provider payloads, translates provider results and failures into semantic port outcomes, isolates credentials and SDK types, applies safe timeout, retry, idempotency, rate-limit, observability, and lifecycle policies, and adds sandbox, emulator, contract, or deterministic integration tests. Do not use to redesign the port, leak vendor types inward, hide ambiguous outcomes, invent fallback behavior, or claim mock-only tests prove the integration.
...
---

# Implementing External Service Adapters

## Purpose

Implement a concrete Infrastructure adapter that satisfies an existing provider-neutral Application port.

A correct adapter:

- preserves the exact Application port contract;
- contains all SDK, HTTP, authentication, and provider-specific details;
- maps Application-owned input into provider payloads;
- maps provider output into stable Application results;
- translates provider failures into the accepted semantic taxonomy;
- implements timeout, retry, idempotency, rate-limit, and reconciliation policies safely;
- protects credentials and sensitive data;
- manages client lifecycle explicitly;
- is validated through the strongest available realistic environment.

## Use When

- An accepted external-service port needs a real provider implementation.
- A Use Case currently imports an SDK or raw HTTP client.
- Provider payloads, enums, status codes, or errors leak into Application.
- A payment, notification, campaign, identity, storage, AI, clock, or similar adapter is required.
- Retryable and permanent failures must be translated consistently.
- Provider idempotency, timeout, pending states, or webhooks require implementation.
- A provider sandbox, emulator, contract test, or recorded fixture strategy must be established.

## Do Not Use When

- The Application port is not yet designed.
- The task is repository persistence.
- The task is HTTP controller implementation.
- The provider contract, credentials strategy, or retry policy is unresolved.
- The request is to copy SDK types into Application.
- The request is to create a generic API client rather than a capability adapter.
- Mock-only tests are being proposed as proof of real provider behavior.
- The adapter would silently introduce fallback or business behavior.

## Inputs

- Accepted Application port and design report.
- Consuming Use Case semantics.
- Provider documentation, SDK/API contract, sandbox or emulator details.
- Project policies for configuration, credentials, timeout, retries, idempotency, rate limiting, logging, telemetry, and lifecycle.
- Accepted semantic result and failure taxonomy.
- Test credentials and secret-management approach.
- Applicable `AGENTS.md` and backend standards.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Read the Application port completely.
3. Read the adapter handoff from the port design.
4. Inspect existing provider integration and local Infrastructure conventions.
5. Confirm provider API/SDK version and lifecycle.
6. Confirm timeout, retry, idempotency, cancellation, fallback, and async ownership.
7. Confirm secret storage, tenant selection, and redaction policy.
8. Identify the strongest available test environment:
   - provider sandbox;
   - official emulator;
   - local fake server;
   - contract test;
   - recorded deterministic fixtures.
9. Identify provider limits and ambiguous outcomes.
10. Do not alter the Application contract to match SDK convenience.

## Outputs

- Concrete external-service adapter.
- Application-to-provider request mapper.
- Provider-to-Application result mapper.
- Technical-to-semantic error translator.
- Timeout, retry, idempotency, rate-limit, and reconciliation implementation.
- Secure configuration and client lifecycle handling.
- Integration, sandbox, emulator, or contract tests.
- External-service adapter implementation record.

## Core Boundary

```text
Application port
← Infrastructure adapter
↔ SDK / HTTP / provider protocol
```

Provider-specific details stop at the adapter.

## Workflow

1. **Confirm readiness:** Port, provider contract, policies, credentials, and test environment are resolved.
2. **Map contract obligations:** List every operation, success meaning, failure, and resilience rule.
3. **Inspect provider behavior:** API stages, status model, limits, idempotency, async completion, and ambiguous outcomes.
4. **Design request mapping:** Convert Application input into minimal provider payload.
5. **Design response mapping:** Convert provider outcomes into semantic Application results.
6. **Implement failure translation:** Stable, minimal, and retry-aware.
7. **Implement timeout and cancellation:** Without leaking transport abstractions inward.
8. **Implement retries safely:** Only for accepted retryable outcomes.
9. **Implement idempotency and reconciliation:** Especially for state-changing commands.
10. **Implement authentication and tenant selection:** Entirely in Infrastructure.
11. **Implement observability and redaction:** Semantic telemetry, no secrets.
12. **Manage client lifecycle:** Shared or transient according to composition policy.
13. **Add realistic tests:** Sandbox/emulator/contract plus deterministic unit mapping tests.
14. **Validate provider replacement boundary:** No vendor leakage through the port.
15. **Report:** Use the implementation record.

## Readiness Gate

Use one:

```text
READY_TO_IMPLEMENT_ADAPTER
READY_WITH_CONDITIONS
RETURN_TO_PORT_DESIGN
PROVIDER_CONTRACT_DECISION_REQUIRED
CREDENTIALS_OR_ENVIRONMENT_REQUIRED
RESILIENCE_DECISION_REQUIRED
BLOCKED
```

Stop when:

- port semantics and provider capabilities conflict;
- timeout or retry ownership is unclear;
- idempotency is required but unsupported and no reconciliation strategy exists;
- credentials cannot be handled safely;
- provider behavior cannot be validated realistically;
- fallback behavior is requested but not accepted.

## Contract Fidelity

For every port operation document:

- Application request;
- provider operation;
- exact success meaning;
- provider states;
- semantic result;
- semantic failures;
- retryability;
- idempotency;
- timeout ambiguity;
- test evidence.

Do not add provider-only meanings to the Application contract unless consumers need them and the port is intentionally revised.

## Request Mapping

Map only required fields.

Good:

```text
Application request
→ selected provider payload
→ provider authentication metadata
```

Do not send:

- whole Entities;
- unrelated DTO fields;
- secrets from Application;
- internal audit metadata;
- unsupported nulls/defaults;
- provider fields invented by guessing.

Provider headers, SDK builders, and serialization live inside Infrastructure.

## Response Mapping

Translate provider output into stable Application meaning.

Examples:

```text
provider accepted → QUEUED
provider completed → APPLIED
provider duplicate → IDEMPOTENT_SUCCESS
provider rejected → REJECTED
```

Do not return raw provider payloads.

Preserve external references only when Application needs reconciliation or audit meaning.

## Failure Translation

Translate:

```text
HTTP/SDK/provider condition
→ semantic Application failure
```

Possible meanings:

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

Do not leak:

- HTTP status;
- provider exception class;
- vendor error code;
- endpoint name;
- request ID unless explicitly exposed as a neutral external reference;
- raw response body.

Keep technical cause internally for safe diagnostics.

## Retry Classification

Retries may apply only to accepted categories.

Typical candidates:

- rate limited;
- transient unavailable;
- connection reset;
- selected timeout scenarios.

Do not retry:

- business rejection;
- invalid provider request;
- permanent authorization/configuration failure;
- non-idempotent command without protection.

Use bounded attempts and accepted backoff policy.

Do not invent retry counts.

## Timeout

Implement timeout in Infrastructure.

Define:

- connect/request/overall timeout where relevant;
- semantic timeout result;
- whether the provider may still complete;
- whether retry is safe;
- reconciliation action;
- telemetry.

Do not treat every timeout as definite failure.

## Idempotency

For state-changing commands:

- map provider-neutral idempotency key to provider mechanism;
- preserve the same key across safe retries;
- define duplicate response translation;
- store/reconcile external reference when required;
- avoid generating a new key inside the adapter per retry.

Never expose vendor header names to Application.

## Ambiguous Outcomes

When timeout or connection loss can occur after provider acceptance:

- classify outcome as ambiguous;
- use idempotency for safe retry;
- query/reconcile when supported;
- persist external correlation when required;
- avoid reporting permanent failure prematurely.

## Rate Limiting

Handle provider limits through:

- semantic `RATE_LIMITED`;
- retry-after parsing inside adapter;
- accepted backoff;
- metrics;
- bounded retries;
- queue/job ownership where applicable.

Do not expose raw provider headers through Application unless explicitly modeled neutrally.

## Authentication and Configuration

Credentials remain in Infrastructure.

Use:

- secret manager;
- environment/config abstraction;
- workload identity;
- provider credential chain;
- tenant-to-account resolver.

Do not:

- accept API keys in Application DTOs;
- log secrets;
- hard-code credentials;
- expose SDK credential types inward.

Validate required configuration at composition/startup where possible.

## Multi-Tenant Provider Selection

Map neutral tenant context to:

- provider account;
- credentials;
- region;
- endpoint;
- configuration.

Define cache and lifecycle behavior safely.

Do not let Use Cases choose vendor account IDs unless they are accepted Application concepts.

## SDK and HTTP Client Lifecycle

Clarify:

- singleton/shared client;
- tenant-scoped client;
- request-scoped client;
- connection pool;
- cleanup;
- thread/concurrency safety.

Composition root usually owns long-lived clients.

Do not create expensive unmanaged clients on every operation unless required.

## Asynchronous Provider Behavior

Map provider stages honestly:

```text
PENDING
QUEUED
COMPLETED
REJECTED
```

Define:

- external correlation;
- polling;
- webhook processing;
- final-state reconciliation;
- duplicate webhook handling;
- stale pending timeout;
- ownership of follow-up Use Cases/jobs.

Do not report `DELIVERED` when the provider only reports `QUEUED`.

## Webhook Relationship

Outbound adapter implementation does not directly own inbound webhook delivery.

Webhook controller/consumer:

```text
provider payload
→ transport verification
→ Application Request DTO
→ reconciliation Use Case
```

The adapter may share provider-specific signature verification utilities in Infrastructure when architecture supports it.

## Fallbacks

Do not introduce fallback silently.

When accepted:

- define trigger;
- alternate adapter;
- semantic differences;
- idempotency across providers;
- duplicate risk;
- observability;
- data reconciliation.

A fallback that changes business behavior requires explicit Application/architecture design.

## Circuit Breaker

Implement in Infrastructure only when accepted.

Translate open-circuit behavior into semantic unavailability.

Do not expose circuit-breaker library types or state to Application.

## Security and Privacy

Review:

- minimum outbound fields;
- PII;
- tokenization;
- encryption;
- regional endpoint;
- provider retention;
- payload logging;
- webhook authenticity;
- SSRF/request construction;
- secret rotation;
- least privilege.

Redact payloads and errors according to policy.

## Observability

Record:

- Application operation name;
- selected provider;
- semantic outcome;
- latency;
- retry count;
- timeout;
- rate limit;
- idempotency/correlation reference;
- safe provider request ID;
- reconciliation status.

Do not log secrets or unrestricted payloads.

## Clock and ID Adapters

For simple ports such as Clock or ID generator:

- implement exact precision/format policy;
- keep library-specific types inside Infrastructure;
- add deterministic test implementation separately;
- avoid unnecessary retry/resilience machinery.

Proportionality still applies.

## Test Strategy

Use multiple levels.

### Pure Mapping Tests

Test:

- Application request → provider payload;
- provider response → Application result;
- provider error → semantic failure;
- no sensitive/unnecessary fields.

### Client/Protocol Tests

Use:

- official sandbox;
- official emulator;
- local protocol fake;
- mock server;
- contract fixtures.

Verify:

- authentication shape;
- serialization;
- headers;
- endpoint/version;
- timeout;
- retry;
- idempotency;
- rate limit;
- async states.

### Provider Sandbox Tests

When available, validate real behavior with safe test credentials.

Keep them:

- isolated;
- identifiable;
- cost-controlled;
- non-destructive;
- separately classifiable from product tests.

### No Sandbox

When unavailable:

1. use official documented emulator if faithful;
2. use schema/contract tests;
3. use local fake server with provider fixtures;
4. document residual uncertainty;
5. do not claim full real-provider verification.

## Failure Classification in Tests

Distinguish:

```text
PRODUCT_FAILURE
PROVIDER_SANDBOX_FAILURE
CREDENTIALS_BLOCKED
NETWORK_BLOCKED
RATE_LIMIT_BLOCKED
UNAVAILABLE_TEST_CAPABILITY
```

Do not hide blocked integration evidence as passing.

## Required Test Cases

- success mapping;
- rejection;
- duplicate/idempotent result;
- retryable failure;
- permanent failure;
- timeout;
- ambiguous completion;
- bounded retry;
- rate limit;
- credentials/config validation;
- tenant selection;
- redaction;
- async pending/completed mapping;
- SDK/client lifecycle when relevant.

## Test Doubles Versus Adapter Tests

Use Case tests use Application-level stubs/spies.

Adapter tests validate provider mapping and protocol behavior.

Do not test an adapter only through the Use Case fake.

## Provider Versioning

Pin or constrain provider SDK/API version according to project policy.

Review:

- deprecations;
- changed enums;
- field additions/removals;
- webhook version;
- backward compatibility;
- migration plan.

Do not let a provider SDK upgrade silently change Application semantics.

## Error Safety

Unexpected technical errors should:

- map to accepted unknown/unavailable failure;
- preserve safe internal cause;
- redact sensitive details;
- emit telemetry;
- never expose raw provider response to the caller.

## Existing Coupled Integration Refactoring

Incremental recovery:

```text
characterize current provider behavior
→ implement accepted port adapter
→ add mapping/error tests
→ migrate one Use Case
→ remove SDK types from Application
→ remove old integration path
```

Avoid broad provider rewrites unrelated to the accepted slice.

## Boundary Guardrails

Adapter may import:

- Application port and DTOs;
- Domain Value Objects when required;
- provider SDK/HTTP client;
- Infrastructure config, telemetry, resilience utilities.

Adapter must not make Application import:

- SDK types;
- HTTP status;
- provider enums;
- credential/config types;
- transport response objects.

## Output

Use `assets/external-service-adapter-implementation-record.md`.

## Completion Criteria

- [ ] Accepted Application port and adapter handoff confirmed.
- [ ] Provider contract/version and test environment inspected.
- [ ] Every port operation maps to provider behavior.
- [ ] Request and response mapping is explicit.
- [ ] Provider errors translate to stable Application semantics.
- [ ] Timeout, retry, idempotency, rate limiting, cancellation, and async behavior follow accepted policy.
- [ ] Ambiguous outcomes have reconciliation behavior.
- [ ] Credentials, tenant selection, and secrets remain in Infrastructure.
- [ ] Logs and telemetry are redacted and semantic.
- [ ] Client lifecycle is explicit.
- [ ] Mapping and protocol tests pass.
- [ ] Sandbox/emulator/contract evidence is recorded honestly.
- [ ] No provider, SDK, HTTP, credential, or transport types leak inward.
- [ ] No unapproved fallback or Application behavior was introduced.
