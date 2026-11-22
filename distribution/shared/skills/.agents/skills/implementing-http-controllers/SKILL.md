---
name: implementing-http-controllers
description: Implements thin backend REST controllers that validate transport shape, extract authenticated context, build Application Request DTOs, invoke one Use Case intention, map Application Response DTOs to stable HTTP responses, and translate semantic errors safely. Use when accepted Application Use Cases and DTOs must be exposed through HTTP. Do not use to implement business rules, call repositories or provider adapters directly, expose Domain objects, leak technical errors, or invent REST contracts.
...
---

# Implementing HTTP Controllers

## Purpose

Implement a thin HTTP delivery adapter around an accepted Application Use Case.

A correct controller:

- owns route, method, headers, path/query/body parsing, and transport validation;
- extracts trusted authentication and request context according to project policy;
- builds an Application Request DTO composed of primitives/plain data;
- invokes one Use Case intention;
- maps an Application Response DTO or `void` to the accepted HTTP contract;
- translates Domain/Application errors into stable HTTP status and safe error bodies;
- does not contain business rules, persistence access, provider calls, or Domain mutation;
- is validated through controller/contract tests and critical HTTP integration or E2E evidence.

## Use When

- An existing Use Case must be exposed as a REST endpoint.
- A controller currently calls a repository or provider directly.
- Business validation is duplicated in controllers.
- HTTP request objects or framework DTOs leak into Application.
- A route, status, response, headers, or error mapping must be implemented.
- Authentication context must be converted into a trusted Application field.
- An endpoint must preserve an accepted public contract.

## Do Not Use When

- The Use Case or Application DTOs are not ready.
- The task is to design Domain behavior.
- The task is to implement persistence or provider adapters.
- The HTTP contract is materially unresolved.
- The request is to create a generic controller abstraction for future endpoints.
- The endpoint is GraphQL, event, CLI, or job delivery unless the repository explicitly treats it through the same transport conventions.
- The controller would need to invent business behavior or error semantics.

## Inputs

- Accepted HTTP/API contract.
- Application Use Case.
- Application Request and Response DTOs.
- Accepted Application and Domain error taxonomy.
- Authentication and authorization boundary policy.
- Framework routing, validation, middleware, and response conventions.
- OpenAPI/schema definitions when present.
- Existing controller and HTTP test conventions.
- Applicable `AGENTS.md` and backend standards.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Read the accepted endpoint contract completely.
3. Read the Application Use Case and DTOs.
4. Inspect framework-specific routing, validation, auth, and error conventions.
5. Confirm:
   - route and HTTP method;
   - path/query/body fields;
   - success status and body;
   - headers;
   - authentication context;
   - semantic error-to-HTTP mapping;
   - idempotency header policy;
   - pagination and versioning when applicable.
6. Inspect existing global middleware and exception filters before duplicating behavior.
7. Identify public consumer compatibility requirements.
8. Do not infer missing HTTP semantics from framework defaults.

## Outputs

- Thin controller or route handler.
- Transport request schema/validation.
- HTTP-to-Application mapping.
- Application-to-HTTP response mapping.
- Semantic error mapping.
- Authentication/context mapping.
- Controller and HTTP contract tests.
- HTTP controller implementation record.

## Core Boundary

```text
HTTP request
→ transport parsing and shape validation
→ Application Request DTO
→ one Use Case
→ Application Response DTO / void
→ HTTP response
```

The controller is a delivery adapter, not a business service.

## Workflow

1. **Confirm readiness:** HTTP contract, Use Case, DTOs, auth policy, and error mapping are resolved.
2. **Define route semantics:** Method, resource URL, status, headers, and versioning.
3. **Define transport schema:** Path, query, headers, and body validation.
4. **Extract trusted context:** Actor, tenant, correlation, and idempotency values.
5. **Build Application Request DTO:** Primitives/plain data only.
6. **Invoke one Use Case:** No repository, provider, or Use Case chaining.
7. **Map success response:** Correct status, body, headers, and empty-response semantics.
8. **Translate errors:** Semantic and safe; technical details remain internal.
9. **Apply security controls:** Authentication, body limits, sensitive-field handling, and safe logging.
10. **Add tests:** Mapping, validation, status/body/headers, auth, errors, and critical HTTP integration.
11. **Audit thinness:** Remove duplicated Domain/Application logic.
12. **Report:** Use the controller implementation record.

## Readiness Gate

Use one:

```text
READY_TO_IMPLEMENT_CONTROLLER
READY_WITH_CONDITIONS
RETURN_TO_USE_CASE_DESIGN
RETURN_TO_DTO_DESIGN
HTTP_CONTRACT_DECISION_REQUIRED
AUTH_BOUNDARY_DECISION_REQUIRED
ERROR_MAPPING_DECISION_REQUIRED
BLOCKED
```

Stop when:

- route or method is unresolved;
- public response/error shape is unresolved;
- authenticated actor trust boundary is unclear;
- idempotency source is required but undefined;
- Use Case still returns an Entity or provider type;
- Application errors cannot be mapped safely.

## REST Resource Design

Use accepted resource-oriented conventions.

Prefer nouns and stable resource hierarchy:

```text
POST /subscriptions/{subscriptionId}/promotions
GET /subscriptions/{subscriptionId}/promotions/active
DELETE /subscriptions/{subscriptionId}/promotions/{promotionId}
```

Avoid RPC-like URLs unless explicitly accepted:

```text
POST /applyPromotion
POST /doCampaignAction
```

Do not redesign an already accepted public route solely for stylistic preference.

## HTTP Method Semantics

Follow accepted semantics:

- `GET`: safe read;
- `POST`: create/command where server or operation semantics fit;
- `PUT`: full idempotent replacement where accepted;
- `PATCH`: partial update;
- `DELETE`: deletion/cancellation semantics.

Do not assume idempotency only from the method; define operation behavior explicitly.

## Transport Validation

Validate transport concerns:

- required path/query/body/header fields;
- primitive type and basic shape;
- body size;
- allowed enum strings;
- array/object shape;
- format such as UUID syntax or ISO timestamp when the transport contract requires it.

Do not make transport validation the sole authority for Domain invariants.

Application and Domain remain authoritative.

## Validation Ownership

```text
HTTP layer
→ transport shape and parsing

Application
→ primitive interpretation and Use Case semantics

Domain
→ invariants, lifecycle, eligibility, value rules
```

Avoid duplicating complex business validation in decorators, schemas, or controller conditionals.

## Request Mapping

Map path, query, body, headers, and trusted auth context into one Application Request DTO.

Example:

```ts
const request: ApplyPromotionRequest = {
  subscriptionId: params.subscriptionId,
  campaignId: body.campaignId,
  actorId: auth.actorId,
  idempotencyKey: headers["idempotency-key"]
}
```

Do not pass the framework request object into Application.

Do not construct repositories, adapters, or Domain Entities in the controller.

Domain Value Object construction normally belongs in Application according to the standard.

## Authentication Versus Authorization

### Authentication

Usually performed by middleware/guard.

The controller receives trusted identity context.

### Authorization

Operation-level authorization normally belongs in Application when it depends on resource ownership, tenant, actor, or business operation.

The controller should not duplicate that decision.

It may enforce coarse transport-level scopes only when the project policy explicitly places them there.

Do not pass raw tokens or framework principal objects to Application.

## Tenant Context

Map trusted tenant context to a primitive Application field.

Do not trust tenant IDs supplied in the body when they should come from authentication.

Define conflict behavior when path/body tenant data differs according to accepted policy.

## Idempotency Headers

When accepted:

- read the configured header;
- validate basic presence/format;
- map it to a provider-neutral Application field;
- return accepted replay/duplicate headers or status;
- never generate a new key silently in the controller unless policy says so.

Do not expose vendor-specific idempotency header names inward.

## Correlation and Trace Context

Infrastructure/middleware usually manages trace headers.

The controller may pass a neutral correlation ID only when Application behavior requires it.

Do not couple Application to tracing SDK types.

## Success Status

Use the accepted status:

- `200 OK`;
- `201 Created`;
- `202 Accepted`;
- `204 No Content`.

Define:

- response body;
- `Location` header;
- async/pending semantics;
- empty body;
- replay/idempotency metadata.

Do not return `200` by default when the contract requires another status.

## Response Mapping

Application Response DTOs are already primitive/plain.

The controller may:

- pass them through when HTTP shape matches;
- wrap them according to accepted transport envelope;
- rename/version fields only through explicit mapping;
- set headers.

Do not serialize Entities or call Domain behavior.

Do not spread unknown objects into the response.

## Error Mapping

Create one authoritative semantic mapping.

Example:

```text
INVALID_INPUT → 400
UNAUTHENTICATED → 401
FORBIDDEN → 403
NOT_FOUND → 404
DUPLICATE / CONFLICT → 409
BUSINESS_REJECTION → 422
RATE_LIMITED → 429
DEPENDENCY_UNAVAILABLE → 503
DEPENDENCY_TIMEOUT → 504
UNKNOWN → 500
```

Exact mappings follow the accepted API policy.

Do not invent status choices when the public contract already defines them.

## Safe Error Body

Expose stable public fields only, for example:

```json
{
  "code": "PROMOTION_EXPIRED",
  "message": "The promotion is expired.",
  "correlationId": "..."
}
```

According to policy, messages may be generic.

Never expose:

- stack traces;
- SQL/ORM errors;
- provider response bodies;
- credentials;
- internal paths;
- raw exception objects;
- constraint names.

## Technical Errors

Unexpected errors map to a safe generic server response.

Technical details go to protected logs/telemetry.

Do not use `error.message` directly as a public response.

## Error Mapping Ownership

Prefer one of the accepted patterns:

- controller-local explicit mapper for one route family;
- shared HTTP exception mapper/filter;
- middleware;
- framework exception filter.

Do not duplicate inconsistent mappings across controllers.

The controller must know whether the global layer already owns translation.

## Framework DTOs

When the framework requires decorated request classes, keep them in the delivery layer.

Map them to Application Request DTOs.

Do not import decorated HTTP classes into Application.

## OpenAPI and Schema

When applicable:

- update source schema/decorators;
- keep required/optional/nullability accurate;
- document enums and error responses;
- regenerate generated output;
- do not hand-edit generated clients/spec files.

Schema must reflect actual runtime behavior.

## Pagination

Map HTTP query values to Application pagination DTOs.

Define:

- default and maximum limit ownership;
- cursor opacity;
- invalid cursor behavior;
- response links or next cursor;
- stable ordering.

Do not expose database offsets/cursors unless the public contract accepts them.

## Filtering and Sorting

Allow only accepted fields and operators.

Do not pass arbitrary query keys into repositories or query builders.

Map transport strings into explicit Application criteria.

## File Uploads

When applicable:

- enforce size/type limits;
- stream safely;
- avoid loading unbounded content;
- map metadata to Application;
- keep framework file objects outside Application;
- define cleanup on failure.

Use a storage port for external persistence.

## Streaming and Downloads

Define:

- media type;
- content length/range;
- filename/content disposition;
- authorization;
- lifecycle and cancellation;
- error behavior after streaming starts.

Do not expose Infrastructure streams inward unless architecture explicitly supports a neutral stream abstraction.

## Caching Headers

Set `ETag`, `Cache-Control`, or conditional headers only when accepted contract and consistency semantics are defined.

Do not add caching opportunistically.

## CORS, CSRF, and Security Headers

Usually managed globally.

The controller should not override them casually.

For cookie-authenticated state-changing routes, confirm CSRF policy.

## Rate Limiting

Transport-level rate limiting usually belongs to middleware/gateway.

Map exceeded limits to the accepted response.

Do not confuse provider rate limiting with client-facing API rate limiting.

## Input Security

Review:

- mass assignment;
- unbounded arrays/strings;
- prototype pollution;
- content type;
- path traversal;
- injection into downstream criteria;
- untrusted URLs;
- sensitive fields;
- tenant spoofing.

Allow-list input fields.

## Logging and Privacy

Log:

- route/operation;
- status;
- duration;
- safe actor/tenant/correlation identifiers;
- semantic error category.

Do not log:

- tokens;
- full bodies with PII;
- credentials;
- provider payloads;
- unrestricted error details.

## Controller Thinness Test

A controller is too thick if it:

- loads or saves via repository;
- calls provider adapter;
- calculates eligibility;
- mutates Entity state;
- opens transactions;
- chains Use Cases;
- maps provider errors;
- contains large branching business workflows.

Move those concerns to Application, Domain, or Infrastructure.

## One Use Case Per Intention

A route handler normally invokes one Use Case.

It may invoke a dedicated query Use Case for a read route.

Do not invoke several Use Cases to assemble one workflow unless an explicit higher-level Application workflow owns that intention.

## Tests

### Controller Unit/Integration Tests

Cover:

- path/query/body/header mapping;
- trusted actor/tenant extraction;
- Request DTO construction;
- one Use Case invocation;
- success status/body/headers;
- validation rejection;
- each semantic error mapping;
- safe unknown error;
- no technical detail leakage;
- no call when transport validation fails.

Use a focused Use Case stub/spy.

### HTTP Contract Tests

Verify:

- route and method;
- content type;
- status;
- response body/schema;
- headers;
- optionality/nullability;
- error body;
- OpenAPI/schema alignment.

### HTTP E2E

Use composed application for critical paths:

- main success;
- authorization failure;
- core business rejection;
- conflict/idempotency;
- dependency failure when practical.

Do not duplicate every lower-level case.

## Error Test Safety

When testing unknown technical errors, assert:

- stable generic body;
- no stack;
- no provider/database detail;
- correlation/trace behavior according to policy.

## Existing Controller Refactoring

Warning signs:

- repository or ORM calls;
- provider SDK calls;
- Entity construction/mutation;
- duplicated business validation;
- direct HTTP-to-Domain coupling;
- raw errors returned;
- many unrelated actions.

Incremental recovery:

```text
select one route
→ ensure Use Case/DTO exists
→ map transport to Request DTO
→ invoke one Use Case
→ map response/errors
→ add contract tests
→ remove direct dependencies
```

Avoid broad unrelated controller rewrites.

## Boundary Guardrails

Controller may import:

- Application Use Case;
- Application DTOs;
- Application error types/codes;
- framework HTTP types;
- delivery validation and auth context;
- HTTP error mapper.

Controller must not import:

- repository implementations or ports for direct use;
- provider adapters or SDKs;
- ORM/database clients;
- Domain Entities for mutation;
- transaction clients;
- environment secrets.

## Output

Use `assets/http-controller-implementation-record.md`.

## Completion Criteria

- [ ] Accepted HTTP contract, Use Case, and DTOs confirmed.
- [ ] Route, method, status, headers, and versioning implemented.
- [ ] Transport validation covers shape without duplicating Domain rules.
- [ ] Trusted authentication/tenant context is mapped safely.
- [ ] One Application Request DTO is built from primitives/plain data.
- [ ] Exactly one Use Case intention is invoked.
- [ ] Success Response DTO or `void` maps to the accepted HTTP response.
- [ ] Semantic errors map consistently to safe status/body contracts.
- [ ] Unknown technical errors reveal no internal details.
- [ ] No repository, provider, transaction, or Domain business logic exists in the controller.
- [ ] Controller, contract, and critical HTTP integration tests pass.
- [ ] OpenAPI/schema source matches runtime behavior when applicable.
- [ ] No speculative routes, fields, statuses, or framework leakage into Application were introduced.
