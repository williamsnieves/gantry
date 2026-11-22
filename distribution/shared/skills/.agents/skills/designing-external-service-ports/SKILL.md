---
name: designing-external-service-ports
description: Portable engineering capability `designing-external-service-ports`. Use
  when the harness or a specialist agent explicitly requires this named capability.
---
# Designing External Service Ports

## Purpose

Design an Application-owned port that expresses an external capability in provider-neutral terms.

A well-designed external-service port:

- is owned by the Application layer that needs it;
- describes an intention, not a vendor API;
- uses Application or Domain language;
- accepts primitives, Value Objects, or Application-owned DTOs;
- returns semantic results or failures;
- keeps SDK, HTTP, authentication, retry, and serialization details in Infrastructure;
- enables deterministic Use Case tests;
- supports replacement of one provider without changing the Use Case contract.

## Use When

- A Use Case must call an external payment, notification, identity, campaign, storage, clock, geolocation, search, AI, or remote policy service.
- Provider-specific types are leaking into Application.
- A concrete SDK client is injected into a Use Case.
- External failures need stable Application meanings.
- A provider may be replaced or multiple adapters may exist.
- Use Case tests need a fake, stub, or spy for external collaboration.
- Time, randomness, ID generation, or remote configuration needs an explicit port.
- Retry, timeout, idempotency, or fallback behavior must be assigned clearly.

## Do Not Use When

- The collaboration is persistence of Domain Entities; use a repository port.
- The behavior is pure Domain logic.
- The task is to implement a provider adapter.
- The task is to design an HTTP controller.
- The request is to reuse a provider SDK interface directly.
- No accepted Use Case consumes the proposed operation.
- A generic “ExternalService” interface is requested without one clear capability.
- The required provider behavior or failure semantics are unresolved.

## Inputs

- Accepted specification or OpenSpec change.
- Backend Rule Applicability Report.
- Backend Vertical Slice Plan.
- Application Use Case design.
- Relevant Domain and Application DTOs.
- Provider-neutral business expectations.
- Project policies for errors, timeouts, retries, idempotency, clocks, IDs, logging, and security.
- Existing provider adapters and test doubles.
- Applicable `AGENTS.md` and backend standards.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Read the accepted behavior and consuming Use Case.
3. Identify the exact external capability required.
4. Inspect current provider integrations and existing ports.
5. Confirm Application error/result conventions.
6. Confirm retry, timeout, idempotency, and fallback ownership.
7. Identify sensitive data and credential boundaries.
8. Distinguish provider-neutral semantics from provider implementation details.
9. Derive every operation from a real Use Case need.
10. Do not copy a provider SDK or OpenAPI interface into Application.

## Outputs

- Port suitability and ownership decision.
- Capability responsibility.
- Intention-revealing operations.
- Application-owned input and output types.
- Semantic success and failure taxonomy.
- Timeout, retry, idempotency, cancellation, and fallback expectations.
- Security and privacy constraints.
- Fake/stub/spy design for Use Case tests.
- Adapter implementation obligations.
- External-service port design report.

## Core Principle

Design inward from the Use Case:

```text
Use Case need
→ provider-neutral intention
→ Application port
→ fake/stub for tests
→ provider-specific Infrastructure adapter
```

Do not design outward from a vendor:

```text
SDK method
→ copied request/response types
→ provider errors
→ Application coupling
```

## Workflow

1. **Confirm port suitability:** Verify the need is external collaboration rather than persistence or Domain logic.
2. **Resolve ownership:** Identify the Application capability and consuming Use Cases.
3. **Define one capability:** State the provider-neutral responsibility.
4. **Derive operations:** Add only operations required by accepted behavior.
5. **Design inputs:** Use primitives, Domain values, or Application-owned request types.
6. **Design outputs:** Use semantic Application results, primitives, or DTOs.
7. **Define failure taxonomy:** Translate provider possibilities into stable Application meanings.
8. **Assign resilience ownership:** Timeout, retry, cancellation, idempotency, fallback, and circuit breaking.
9. **Define security boundaries:** Credentials, tokens, PII, audit, and redaction.
10. **Design test doubles:** Deterministic fake/stub/spy behavior.
11. **Define adapter obligations:** Mapping, authentication, observability, resilience, and technical translation.
12. **Check proportionality:** Avoid generic interfaces and unused operations.
13. **Audit boundaries:** Remove SDK, HTTP, provider, and Infrastructure leakage.
14. **Report:** Use the external-service port design report.

## Port Suitability

Use an external-service port when an Application intention requires an external capability.

Examples:

```text
PaymentGateway
NotificationSender
CampaignProvider
IdentityVerifier
Clock
IdGenerator
ObjectStorage
AddressGeocoder
FeaturePolicyProvider
```

Route elsewhere when:

```text
Entity persistence
→ repository port

pure calculation
→ Entity, Value Object, or Domain Service

HTTP delivery
→ controller

provider implementation
→ Infrastructure adapter
```

## Ownership

The Application layer owns the port because the Use Case defines what it needs.

Infrastructure owns the adapter.

The provider does not own the Application contract.

Good:

```text
Application/CampaignProvider
Infrastructure/AcmeCampaignProvider
```

Poor:

```text
Application/AcmeSdkClient
```

## One Capability Per Port

Prefer focused capability interfaces.

Good:

```text
PaymentGateway
EmailSender
Clock
ExternalIdentityVerifier
```

Avoid:

```text
ExternalServices
ThirdPartyClient
IntegrationManager
ApiGatewayService
```

Split when operations have different:

- security boundaries;
- credentials;
- failure semantics;
- lifecycle;
- ownership;
- resilience policies;
- test behavior.

Do not split trivial related operations that clearly form one capability.

## Intention-Revealing Operations

Name operations after Application intent.

Good:

```text
authorizePayment
capturePayment
sendPasswordReset
applyCampaignPromotion
verifyIdentity
now
generateId
```

Avoid:

```text
post
request
execute
callApi
sendPayload
invokeEndpoint
```

Each operation must cite a consuming Use Case.

## Inputs

Inputs should use:

- primitives;
- Value Objects where Application already owns them safely;
- Application-owned request DTOs;
- immutable plain data.

Examples:

```ts
type ApplyCampaignPromotionRequest = {
  subscriptionId: string
  campaignId: string
  idempotencyKey: string
}
```

Do not use:

- provider request classes;
- SDK enums;
- HTTP headers;
- transport response objects;
- framework request context;
- database rows.

## Domain Types in Port Inputs

Using Domain Value Objects may be acceptable when:

- Application already depends on Domain;
- the type expresses stable business meaning;
- the provider adapter can map it cleanly;
- project policy supports it.

Use Application-owned primitives or DTOs when:

- the external interaction should remain independent from a specific aggregate shape;
- the operation has its own stable contract;
- output/input selection matters.

Do not pass whole Entities to provider ports unless accepted architecture clearly requires it.

Prefer explicit fields over `send(entity)`.

## Outputs

Outputs should represent what Application needs.

Examples:

```text
PaymentAuthorization
DeliveryReceipt
CampaignApplicationResult
IdentityVerificationResult
CurrentTime
GeneratedId
```

They may be:

- primitives;
- Application DTOs;
- Value Objects;
- semantic enums;
- Result types according to project policy.

Do not return:

- provider SDK response;
- raw HTTP response;
- provider payload;
- provider-specific IDs unless their meaning is explicitly required and wrapped or renamed;
- opaque `unknown` without translation.

## Success Semantics

Define exactly what success means.

For example:

```text
accepted by provider
completed synchronously
queued for delivery
authorized but not captured
applied and externally visible
```

Do not collapse these into a generic `success: true` when Application behavior depends on the distinction.

## Failure Taxonomy

Map provider failures into stable Application meanings.

Possible categories:

```text
REJECTED
UNAUTHORIZED_WITH_PROVIDER
RATE_LIMITED
TIMEOUT
UNAVAILABLE
INVALID_EXTERNAL_REQUEST
DUPLICATE
CONFLICT
NOT_FOUND
PERMANENT_FAILURE
RETRYABLE_FAILURE
UNKNOWN_EXTERNAL_FAILURE
```

Expose only distinctions needed by accepted Application behavior.

Do not leak:

- provider exception classes;
- HTTP status codes;
- vendor error strings;
- SDK error objects;
- endpoint names.

## Retryability

A failure category should communicate retryability only when Application needs that distinction.

Possible models:

```text
RetryableExternalFailure
PermanentExternalFailure
```

or explicit semantic errors.

Do not let Use Cases parse provider messages to decide retry behavior.

Infrastructure translates provider-specific responses into the accepted taxonomy.

## Timeout Ownership

Define:

- operation timeout expectation;
- which layer enforces it;
- timeout result meaning;
- whether timeout is retryable;
- whether provider operation may still complete after timeout;
- reconciliation requirements.

Timeout mechanisms belong in Infrastructure.

Application owns the semantic reaction.

Do not place Axios/fetch timeout configuration in the port interface.

## Retries

Clarify:

- adapter-level retry;
- Application/workflow-level retry;
- job retry;
- maximum attempts;
- backoff policy;
- idempotency requirement;
- retryable categories;
- observability.

Retries should usually be implemented in Infrastructure or workflow orchestration according to policy.

Do not retry permanent business rejection.

Do not hide retry behavior when duplicate side effects are possible.

## Idempotency

When the external operation changes state, define:

- idempotency key;
- key source;
- whether provider supports it;
- adapter mapping;
- duplicate response semantics;
- persistence/reconciliation needs;
- retry behavior.

The port may include a provider-neutral idempotency field:

```ts
applyPromotion({
  subscriptionId,
  campaignId,
  idempotencyKey
})
```

Do not expose a vendor-specific header name.

## Cancellation

When operations are long-running or user-cancellable, define:

- whether cancellation is supported;
- cancellation token/abstraction policy;
- what cancellation means semantically;
- partial completion risk;
- cleanup/reconciliation.

Do not leak framework-specific AbortSignal unless project policy explicitly accepts it at the Application boundary.

## Fallbacks

Fallback is an Application or architecture decision.

Define:

- when fallback is permitted;
- alternate adapter/capability;
- semantic differences;
- data consistency;
- user-visible impact;
- observability.

Do not implement silent fallback in an adapter if it changes accepted behavior.

## Circuit Breaking

Circuit breakers are Infrastructure concerns.

The port should expose semantic unavailability, not circuit-breaker library state.

Application may react to `UNAVAILABLE` or `RETRYABLE_FAILURE`.

## Authentication and Credentials

Credentials remain in Infrastructure.

The port must not accept:

- API keys;
- provider secrets;
- OAuth client secrets;
- SDK credential objects.

Application may pass actor or tenant context when it is part of business meaning.

Infrastructure resolves provider authentication.

## Security and Privacy

Define:

- minimum required outbound data;
- PII fields;
- sensitive identifiers;
- tokenization/redaction;
- region/residency constraints;
- logging restrictions;
- provider retention assumptions;
- audit requirements.

Do not send entire Entities or Request DTOs when the provider needs only selected fields.

## Multi-Tenancy

When provider configuration varies by tenant, define provider-neutral tenant context.

Do not expose provider account IDs unless they are accepted Application concepts.

Infrastructure selects credentials/account mapping.

## Clocks

A Clock port is a valid external Application port.

Example:

```ts
interface Clock {
  now(): Instant
}
```

or project-approved primitive/Value Object result.

It should:

- be deterministic in tests;
- have no provider terminology;
- use accepted timezone/precision policy.

Do not call `Date.now()` directly in Use Cases when the project requires a Clock.

## ID Generators

An ID generator port may be used when ID creation is an Application concern.

Example:

```ts
interface IdGenerator {
  next(): string
}
```

or Domain `Id`.

Do not expose UUID-library-specific options unless accepted.

Tests use deterministic generators.

## Notifications

Define delivery semantics precisely.

Possible outcomes:

```text
queued
accepted
delivered
failed
```

Do not claim synchronous delivery when the provider only queues.

Define whether notification failure blocks the Use Case, becomes follow-up work, or is handled asynchronously.

## Payments

Distinguish:

```text
authorize
capture
refund
void
```

Do not use one generic `pay()` if accepted behavior depends on stages.

Define:

- Money representation;
- provider-neutral payment reference;
- idempotency;
- partial success;
- reconciliation;
- permanent versus retryable failure.

## External Identity

Define Application meaning:

```text
verified
not verified
requires further review
provider unavailable
```

Do not return raw provider risk scores or document types unless accepted consumers require them.

## Remote Read Versus Command

Distinguish:

### External Query

Fetches external data without accepted side effects.

### External Command

Requests a state change or side effect.

Commands typically require stronger idempotency, timeout, retry, and reconciliation semantics.

## Asynchronous Operations

If the provider returns a pending state, model it explicitly.

Example:

```text
COMPLETED
PENDING
REJECTED
```

Define:

- polling or webhook ownership;
- correlation ID;
- state reconciliation;
- timeout;
- duplicate event handling.

Do not pretend asynchronous completion is synchronous.

## Webhooks

The external-service port normally represents outbound Application need.

Inbound provider webhooks are delivery boundaries.

The webhook controller/consumer validates transport and invokes an Application Use Case.

Provider webhook payload types stay in Infrastructure/delivery mapping.

## Test Doubles

Use deterministic Application-level doubles.

### Stub

Returns a configured result or failure.

### Spy

Records provider-neutral calls for meaningful interaction assertions.

### Fake

Implements simple provider-neutral behavior when useful.

Test doubles should:

- use port types;
- avoid provider SDK types;
- allow configured success/failure;
- record calls safely;
- support deterministic timestamps/IDs;
- avoid implementing irrelevant provider behavior.

## Use Case Test Expectations

Use Case tests should cover:

- successful collaboration;
- semantic rejection;
- retryable failure;
- permanent failure;
- timeout;
- duplicate/idempotency;
- no call after earlier Domain rejection;
- selected outbound fields;
- result mapping;
- follow-up behavior for pending/asynchronous results.

Do not assert provider HTTP details in Use Case tests.

## Adapter Handoff

The design must tell the future adapter how to:

- map Application request to provider request;
- map provider result to semantic output;
- translate failures;
- authenticate;
- set timeout;
- apply retries;
- map idempotency;
- redact logs;
- emit metrics/traces;
- handle rate limits;
- support cancellation;
- reconcile ambiguous outcomes;
- manage SDK lifecycle.

## Observability

Define provider-neutral observability expectations:

- operation name;
- correlation/idempotency ID;
- success/failure category;
- latency;
- retry count;
- provider selected;
- redacted error context.

Infrastructure implements metrics/logging/tracing.

Do not expose provider secrets or sensitive payloads.

## Versioning and Provider Replacement

A good port should survive provider replacement.

Review for vendor leakage in:

- operation names;
- request fields;
- enums;
- IDs;
- error taxonomy;
- pagination;
- asynchronous states.

Provider-specific capability differences may require:

- adapter-specific configuration;
- a narrower common contract;
- separate ports;
- explicit architecture decision.

Do not force a false lowest-common-denominator abstraction when providers have materially different semantics.

## Generic Client Anti-Pattern

Avoid:

```ts
interface ExternalApiClient {
  request<T>(method: string, path: string, body: unknown): Promise<T>
}
```

This is an Infrastructure abstraction, not an Application capability.

Application ports should express business or system intent.

## Existing Provider-Coupled Code

Warning signs:

- SDK client injected into Use Case;
- provider request/response in Application;
- Use Case parses HTTP status;
- provider enum drives business logic;
- credentials passed through DTOs;
- generic API client port;
- retries hidden inside business code.

Incremental recovery:

```text
identify one Application intention
→ define provider-neutral port
→ define semantic result/failures
→ add test double
→ wrap existing provider in adapter
→ migrate Use Case
→ remove SDK leakage
```

Avoid broad replacement of unrelated integrations.

## Boundary Guardrails

Application port must not import:

- Infrastructure;
- provider SDK;
- HTTP client;
- framework transport types;
- environment/config services;
- credential types;
- ORM/database types.

It may depend on:

- Domain Value Objects;
- Application DTOs;
- Application errors/results;
- stable shared primitive contracts.

## Readiness Decision

Use one:

```text
READY_TO_IMPLEMENT_EXTERNAL_PORT
READY_WITH_CONDITIONS
NOT_AN_EXTERNAL_SERVICE_PORT
ROUTE_TO_REPOSITORY_PORT
ROUTE_TO_DOMAIN_SERVICE
RETURN_TO_USE_CASE_DESIGN
RETURN_TO_SPECIFICATION
DECISION_REQUIRED
BLOCKED
```

## Output

Use `assets/external-service-port-design-report.md`.

## Completion Criteria

- [ ] External collaboration need confirmed.
- [ ] Application ownership and consuming Use Cases identified.
- [ ] One focused provider-neutral capability defined.
- [ ] Every operation traced to accepted behavior.
- [ ] Inputs and outputs exclude SDK, HTTP, provider, ORM, and credential types.
- [ ] Success semantics are precise.
- [ ] Failure taxonomy is stable and minimal.
- [ ] Timeout, retry, idempotency, cancellation, fallback, and asynchronous behavior are assigned explicitly when applicable.
- [ ] Security, privacy, multi-tenancy, and logging restrictions are explicit.
- [ ] Deterministic stubs, spies, or fakes are designed.
- [ ] Future adapter mapping and resilience obligations are documented.
- [ ] Port can survive provider replacement without changing Application intent.
- [ ] No generic API client, unused operation, or provider-shaped contract was introduced.

## References

- Read `references/port-suitability-and-ownership.md` first.
- Read `references/operation-input-output-design.md` for contract shape.
- Read `references/success-and-failure-semantics.md` for result modeling.
- Read `references/resilience-idempotency-and-async.md` when side effects or unreliable networks apply.
- Read `references/security-privacy-and-tenancy.md` for outbound data constraints.
- Read `references/test-doubles-and-use-case-testing.md` before completion.
- Read `references/adapter-handoff.md` for Infrastructure obligations.
- Read `references/refactoring-provider-coupling.md` only for existing integrations.
