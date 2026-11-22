---
name: validating-external-frontend-data
description: Decides when frontend runtime validation is necessary and validates untrusted or structurally important external payloads before mapping them into Application or Domain. Use for APIs, BFF responses, browser storage, postMessage, third-party SDK payloads, feature flags, persisted drafts, imported files, or other external boundaries where TypeScript types alone are insufficient. Keep transport validation at the boundary that owns the external contract, report contract mismatches safely, preserve optionality/version semantics, and avoid leaking validation-library types inward. Reuse the repository-approved validator when one exists; do not introduce Zod, Valibot, io-ts, ArkType, or another library without approval.
...
---

# Validating External Frontend Data

## Purpose

Decide whether runtime validation is needed for an external frontend boundary and, when justified, validate the payload before mapping it inward.

The core flow is:

```text
external payload
→ decode transport
→ runtime validate external contract
→ map to stable inward semantics
→ Application / Domain
```

TypeScript alone cannot prove runtime payload validity.

This skill is about external trust boundaries, not general form validation.

## Governing Standard

Transport response types belong in Infrastructure and SHOULD match the external contract exactly.

Transport types MUST be mapped before entering Application or Domain.

Do not let:

```text
snake_case
provider enums
pagination envelopes
nullable transport semantics
```

leak silently inward.

Runtime validation SHOULD be used when remote data is untrusted or structurally important.

## Use When

- API/BFF payloads are externally controlled.
- A provider contract is known to drift.
- Data is structurally important to correct rendering or behavior.
- Persisted browser data may be stale or from older versions.
- postMessage data crosses an origin/frame boundary.
- Imported JSON/file data is user-controlled.
- Third-party SDK returns runtime data with weak typing.
- Feature-flag/config payloads can alter behavior.
- IndexedDB/localStorage data survives app versions.
- A contract mismatch should produce a safe stable failure rather than downstream undefined behavior.
- A package boundary receives unknown JSON.
- Security/privacy risk increases if malformed data is trusted.

## Do Not Use When

- Data is fully internal and created by typed code in the same process.
- The value is a trusted literal/config compiled with the application.
- The task is UI form validation.
- The task is Domain invariant modeling.
- The task is HTTP decoding only.
- The task is repository mapping with no runtime-validation decision.
- Validation would merely duplicate an already authoritative validated boundary.
- The repository has accepted structural trust for a low-risk internal source.
- The proposal adds a validation library without approval.

## Inputs

- External data source.
- Transport/provider contract.
- Runtime trust level.
- Structural importance.
- Versioning/backward-compatibility behavior.
- Existing validator/library policy.
- HTTP client decode behavior.
- Repository/adapter mapping contract.
- Application/Domain target.
- Error taxonomy.
- Observability/privacy policy.
- Performance constraints.
- Existing tests/fixtures.
- Repository-local `AGENTS.md`.

## Outputs

- Runtime-validation decision.
- Trust/criticality classification.
- Validation boundary.
- External schema/validator contract when justified.
- Unknown-field policy.
- Optional/null/missing semantics.
- Version compatibility policy.
- Contract-mismatch semantics.
- Safe observability policy.
- Mapping sequence.
- Focused validation tests.
- External-data validation record.

## Core Workflow

```text
identify external source
→ assess trust and structural importance
→ inspect existing validation policy/tooling
→ decide whether runtime validation is justified
→ define exact external contract
→ define optionality/version behavior
→ validate before inward mapping
→ translate mismatch safely
→ test valid/invalid/versioned payloads
```

## Readiness Gate

Use one:

```text
READY_TO_VALIDATE_EXTERNAL_FRONTEND_DATA
READY_WITH_CONDITIONS
RUNTIME_VALIDATION_NOT_REQUIRED
VALIDATION_POLICY_REQUIRED
EXTERNAL_CONTRACT_REQUIRED
VERSION_POLICY_REQUIRED
ERROR_POLICY_REQUIRED
PRIVACY_POLICY_REQUIRED
BLOCKED
```

A valid outcome may be:

```text
RUNTIME_VALIDATION_NOT_REQUIRED
```

Do not validate everything indiscriminately.

# Validation Decision

Classify each boundary:

```text
VALIDATE_REQUIRED
VALIDATE_RECOMMENDED
VALIDATE_OPTIONAL
RUNTIME_VALIDATION_NOT_REQUIRED
UNKNOWN_REQUIRES_DECISION
```

## Strong Validation Signals

Runtime validation is strongly justified when data is:

- untrusted;
- third-party controlled;
- user-provided;
- persisted across application versions;
- structurally critical;
- security-sensitive;
- used to construct Domain entities/Value Objects;
- consumed by many features;
- known to drift;
- versioned independently from frontend deployment.

## Weaker Validation Signals

Validation may be optional when:

- source is an internal BFF deployed atomically with the frontend;
- payload is simple and low-risk;
- another trusted boundary already validates and guarantees the contract;
- malformed data can be safely rejected through a narrow parser without a schema library.

Document why.

# TypeScript Is Not Runtime Validation

This is not validation:

```ts
const data = await response.json() as ProfileApiResponse
```

This only tells TypeScript to trust the value.

Likewise:

```ts
JSON.parse(raw) as DraftRecord
```

does not validate persisted data.

Use:

```text
unknown
→ validate/parse
→ typed external contract
```

at untrusted boundaries.

# Boundary Ownership

Typical ownership:

```text
HTTP client
→ decode bytes/text/JSON

Repository/Infrastructure adapter
→ validate provider payload
→ map provider data inward
```

Alternative accepted boundary:

```text
dedicated external-contract parser module
```

owned by Infrastructure.

Do not put provider schemas into Domain.

Do not make the common HTTP client aware of feature-specific schemas unless repository policy explicitly centralizes schema-aware requests.

# Decode Versus Validate

Distinguish:

```text
decode
→ Is this syntactically valid JSON/text/binary?

validate
→ Does this decoded value satisfy the expected external structure and semantics?
```

Example:

```json
{"id": 17, "name": null}
```

may be valid JSON but invalid for:

```text
id: string
name: string
```

The HTTP client should handle malformed JSON.

The adapter/parser should usually handle provider schema mismatch.

# Validate Before Mapping

Preferred:

```text
unknown provider payload
→ validate external schema
→ typed transport object
→ map to Application/Domain
```

Avoid:

```text
unknown payload
→ partial destructuring/mapping
→ discover errors deep inside Domain/UI
```

Validation should fail near the trust boundary.

# Exact External Contract

External validation should describe the provider contract, not the desired inward model.

Transport schema may intentionally contain:

```text
snake_case
provider enum codes
nullable fields
version envelope
pagination metadata
legacy fields
```

Then mapping converts those into stable inward semantics.

Do not validate the payload directly against an Application DTO merely because the shapes look similar.

# Unknown Fields

Choose one policy:

```text
ALLOW_UNKNOWN_FIELDS
STRIP_UNKNOWN_FIELDS
REJECT_UNKNOWN_FIELDS
PRESERVE_UNKNOWN_FOR_FORWARD_COMPAT
```

Default depends on provider/versioning policy.

Be cautious with strict rejection for APIs that may add fields compatibly.

Strictness should protect correctness without creating unnecessary breakage.

## Strict Objects

Strict object validation may be justified for:

- signed configuration;
- imported documents with a frozen format;
- security-sensitive messages;
- internal protocols with explicit version negotiation.

It may be harmful for additive public API evolution.

# Missing vs Null vs Undefined

Validate exact external semantics.

Distinguish:

```text
missing property
null
empty string
empty list
false
0
```

Do not normalize these accidentally at validation time.

Mapping may normalize later when the inward contract explicitly defines it.

# Optional Fields

Optional should reflect provider behavior.

Do not mark every field optional to make validation “pass”.

This weakens the boundary and hides contract breakage.

If a required field is absent, surface a contract mismatch.

# Nullable Fields

If provider uses `null`, validate `null` explicitly.

Then decide whether inward mapping becomes:

```text
undefined
null
Maybe
semantic default
```

according to the target contract.

Do not silently replace provider nullability without an explicit mapping decision.

# Primitive Validation

Validate primitive type and important structural constraints when relevant.

Examples:

```text
string
number
boolean
array
object
record
enum
literal
```

Semantic business invariants remain Domain/backend concerns unless the external contract itself specifies them.

Do not turn provider schema validation into duplicated Domain policy.

# Enum Validation

Provider enums should be validated against accepted external values.

Unknown enum handling must be explicit:

```text
CONTRACT_MISMATCH
MAP_TO_UNKNOWN
PRESERVE_UNKNOWN_VALUE
VERSION_FALLBACK
```

Do not silently cast:

```ts
status as SubscriptionStatus
```

# Dates

External timestamps are usually strings/numbers at validation time.

Validate:

- expected primitive;
- parseability when structurally important;
- known format if contract guarantees it.

Then map into stable inward date semantics.

Do not locale-format during validation.

# Numbers

Validate number semantics carefully:

- integer vs floating;
- finite;
- positive/non-negative when part of external contract;
- string-encoded numbers if provider does that;
- money units when transport contract specifies them.

Do not enforce business ranges that belong to Domain unless they are also part of the external contract.

# Arrays

For arrays, validate:

- array shape;
- element schema;
- nullable/empty semantics.

For huge arrays, consider performance and whether full eager validation is appropriate.

Do not introduce expensive validation without understanding payload size.

# Recursive/Nested Data

For nested provider data, validate only the structure needed by the accepted adapter behavior plus necessary contract integrity.

Avoid giant schemas copied mechanically from an enormous provider object if the adapter consumes a narrow subset and unknown fields are allowed.

# Pagination

Validate provider pagination envelope separately from inward pagination semantics.

Example transport:

```text
items
next_cursor
total_count?
```

Then map to:

```text
items
nextCursor?
```

Do not let transport casing or sentinel values leak inward.

# Versioned Payloads

Persisted/client-side data often requires explicit version handling.

Use:

```text
version field
→ validate known version
→ migrate if supported
→ reject safely if unsupported
```

Do not parse legacy persisted data as the latest type through a TypeScript assertion.

# Persisted Browser Data

Treat:

```text
localStorage
IndexedDB
Cache Storage
serialized session data
```

as external/untrusted at runtime because:

- old versions persist;
- users/extensions can modify values;
- partial writes can occur;
- migrations can fail.

Validate before using persisted data as current Domain/Application state.

# Persisted Data Migration

Typical flow:

```text
raw persisted unknown
→ identify version
→ validate version-specific schema
→ migrate
→ validate latest internal persistence contract
→ map to Domain/Application
```

Migration should be explicit.

Do not hide migrations inside a giant forgiving schema that accepts every historical shape.

# postMessage

Treat `message.data` as untrusted.

Validate:

- allowed origin separately;
- message discriminator/type;
- payload structure;
- version if applicable.

Do not cast `event.data`.

Security-sensitive message contracts should prefer explicit discriminated messages.

# Cross-Origin Messages

Schema validation does not replace origin validation.

Need both:

```text
origin/source validation
+
payload validation
```

Do not claim safe postMessage handling from schema validation alone.

# Imported Files / JSON

User-imported files are untrusted.

Validate:

- parseability;
- expected document version;
- structure;
- size/limits according to policy;
- required fields.

Do not inject file content into logs on validation failure.

# Third-Party SDK Payloads

SDK TypeScript types may still not guarantee runtime behavior.

Runtime validation is useful when:

- SDK returns loosely typed metadata;
- remote config drives behavior;
- webhooks/messages arrive through client channel;
- SDK version/provider drift is possible.

Do not duplicate strongly guaranteed SDK runtime contracts without value.

# Feature Flags / Remote Config

Remote config can alter application behavior.

Validate:

- key presence where required;
- primitive type;
- enum values;
- nested config schema;
- version.

Use safe defaults only when product policy explicitly defines them.

Do not silently default malformed critical config.

# HTML / Rich Content

Schema validation of a string does not make HTML safe.

If external data includes HTML:

```text
validate structure/type
+
sanitize/safely render according to security policy
```

Sanitization is a separate security concern.

Do not treat validation as XSS protection.

# URLs

A string URL may require parsing/allowlist checks if security-sensitive.

Schema-level `string` is not enough for:

- redirect destinations;
- iframe sources;
- image origins;
- download URLs.

The exact security policy belongs to the frontend security skill.

# Validation Library Policy

Potential tools include:

```text
Zod
Valibot
io-ts
ArkType
custom validators
```

Use the repository-approved choice.

Do not introduce a new library merely because one appears in the roadmap.

If no library exists and validation is simple, a narrow custom parser may be sufficient.

# Library Leakage

Validation-library types should remain Infrastructure-local unless the project explicitly standardizes them as public contracts.

Avoid returning:

```text
ZodError
ValiError
io-ts Errors
```

to Application or Presentation.

Translate to stable contract-mismatch semantics.

# Schema Reuse

Reuse external schemas when:

- they describe the same external contract;
- ownership is stable;
- versioning matches.

Do not create a global schema registry speculatively.

Feature-local provider schemas are often appropriate.

# Generated Schemas

If OpenAPI/GraphQL/codegen produces runtime validators, use them when repository policy supports them.

Do not assume generated TypeScript interfaces are runtime validators.

Check whether runtime parser artifacts actually exist.

# Schema Composition

Compose schemas when external contracts are genuinely composed.

Avoid overabstracting every primitive into shared schema helpers.

# Defaults

Validation-time defaults can hide provider breakage.

Use defaults only when:

- external contract explicitly allows omission;
- product behavior defines a safe default;
- backward compatibility requires it.

Record the default owner.

Do not default required structural fields just to keep the app running.

# Coercion

Be cautious with coercion:

```text
"123" → 123
"false" → false
```

Coercion may hide contract mismatches.

Use only when the external contract legitimately permits multiple representations.

# Safe Failure Semantics

A validation failure should become a stable Infrastructure/Application error such as:

```text
CONTRACT_MISMATCH
MALFORMED_EXTERNAL_DATA
UNSUPPORTED_VERSION
```

according to repository conventions.

Do not expose raw validator diagnostics directly to users.

# User-Facing Behavior

Presentation may receive a stable semantic failure:

```text
unavailable
contract mismatch
unsupported data version
```

depending on accepted UX.

Do not show:

```text
Expected string, received number at path ["foo", "bar", 2]
```

to end users.

# Observability

Contract mismatch is valuable telemetry.

Safe observability may record:

```text
provider/source
endpoint or source category
schema/version
failure category
field path
correlation ID
app version
```

Do not log full payloads by default.

## Sensitive Payloads

Never log full:

- auth/session data;
- payment data;
- PII;
- user-generated documents;
- file content;
- campaign codes if policy forbids;
- private messages.

Prefer redacted structural diagnostics.

# Validation Error Redaction

A safe diagnostic may include:

```text
path: ["subscription_status"]
expected: enum
receivedType: string
source: subscriptions-api
```

without logging actual sensitive value.

# Contract Drift

When validation failures increase after provider change:

- capture evidence;
- inspect provider version/release;
- update schema/mapping deliberately;
- do not weaken schema immediately with `unknown`/optional everywhere.

Treat frequent mismatch as contract-management signal.

# Backward Compatibility

For external APIs:

- additive unknown fields may be safe;
- removed/renamed required fields are breaking;
- enum expansion may need forward-compatible handling.

Define compatibility policy intentionally.

# Forward-Compatible Enums

For fast-evolving providers, consider:

```text
known enum
+
unknown fallback
```

when product can safely handle unknown values.

Do not do this when unknown state would be unsafe.

# Validation and Domain

Runtime external validation protects the external contract.

Domain validation protects business invariants.

Example:

```text
provider:
quantity is number

Domain:
quantity must be between 1 and 10
```

Both may exist, but they solve different problems.

Do not collapse them.

# Validation and Application DTOs

Do not validate provider payload directly as Application DTO when Infrastructure mapping is intended.

Preferred:

```text
unknown
→ ProviderResponse schema
→ ProviderResponse
→ map
→ ApplicationDTO
```

# Validation and HTTP Client

The common HTTP client may return:

```text
unknown JSON
```

or a generic decoded type depending on project design.

It should not know feature schemas by default.

The adapter owns the validation parser.

# Validation and Repository Adapters

Repository adapters are a natural place to:

```text
decode via HTTP client
→ validate provider response
→ map
→ translate contract mismatch
```

This keeps provider details outward.

# Validation and Server State

SWR/React Query/etc. should consume already-valid adapter/Application semantics when architecture uses repositories.

Do not put provider schema validation into presentation hooks merely because data arrives there.

In Profile A direct server-state integrations, validation may live in the fetcher/adapter boundary if that is the accepted architecture.

# Partial Validation

Partial validation may be appropriate when:

- payload is huge;
- only a narrow subset is consumed;
- provider guarantees unrelated sections independently.

But validate enough to ensure consumed data is safe.

Document why the rest is ignored.

# Lazy Validation

Lazy validation may help very large data sets.

Do not optimize validation prematurely.

Measure first.

# Performance

Runtime validation has cost.

Assess:

- payload size;
- frequency;
- device class;
- schema complexity;
- recursive depth;
- repeated revalidation.

Avoid validating the exact same immutable payload repeatedly at multiple layers.

# Validation Caching

Do not introduce schema-result caches unless measured need exists.

Validation should normally happen once per external boundary crossing.

# Error Boundaries

React error boundaries do not replace external-data validation.

A schema mismatch should be handled before malformed data causes rendering exceptions where possible.

# Security

Runtime validation improves structural safety but does not replace:

- authorization;
- authentication;
- sanitization;
- CSP;
- origin checks;
- CSRF;
- output encoding.

Do not overclaim.

# Forms

UI forms are a separate boundary.

Form shape validation may use the same library but follows the forms/accessibility strategy.

Do not reuse provider schemas as form schemas automatically; their semantics often differ.

# Contract Tests

Provider/adapter contract tests should include representative payloads.

Potential tests:

- valid payload;
- missing required field;
- wrong primitive type;
- unknown enum;
- null vs missing;
- additional field;
- malformed nested object;
- unsupported version;
- legacy persisted version;
- safe diagnostics.

# Golden Fixtures

Representative JSON fixtures can be useful.

Keep them:

- minimal;
- anonymized;
- versioned;
- free of secrets/PII.

Do not copy production payloads containing sensitive data into the repository.

# Fuzz / Property Testing

May be useful for parsers/migrations if existing tooling supports it.

Do not introduce a fuzzing/property library solely for this skill.

# Strictness Evaluation

Test expected policy explicitly.

Example:

```text
additional unknown field
→ accepted

missing required id
→ rejected
```

This protects forward-compatibility decisions.

# Version Migration Tests

For persisted data:

```text
v1 valid
→ migrate
→ current model

unknown v99
→ unsupported version
```

Do not only test the happy current version.

# Mismatch Test

Validation mismatch should verify:

- no Domain/Application object created;
- stable error emitted;
- safe observability recorded;
- raw sensitive payload not logged.

# No-Validation Decision

A valid record may say:

```text
RUNTIME_VALIDATION_NOT_REQUIRED
```

Example:

- value is created inside the same typed process;
- no serialization boundary;
- no external mutation;
- low structural risk.

Document the trust reasoning.

# Overvalidation Signals

Flag:

- validating internal constants;
- validating data already guaranteed by a trusted validated boundary every render;
- schema duplication at HTTP client + adapter + hook;
- huge provider schema when only two fields are consumed;
- strict unknown-field rejection for additive API evolution with no reason.

Use:

```text
PROPORTIONATE_VALIDATION
UNDERVALIDATED_BOUNDARY
OVERVALIDATED_BOUNDARY
RUNTIME_VALIDATION_NOT_REQUIRED
```

# Undervalidation Signals

Flag:

- `as SomeApiResponse` after JSON parse;
- unchecked localStorage JSON;
- unchecked postMessage;
- provider enum cast;
- Domain entity built from unvalidated external object;
- `any`/`unknown` passed directly into components;
- fallback `{}` after parse/validation failure.

# Final Decision

Use:

```text
EXTERNAL_FRONTEND_DATA_VALIDATION_READY
EXTERNAL_FRONTEND_DATA_VALIDATION_READY_WITH_CONDITIONS
RUNTIME_VALIDATION_NOT_REQUIRED
RETURN_TO_ADAPTER_OR_CONTRACT_DESIGN
VALIDATION_LIBRARY_POLICY_REQUIRED
VERSION_POLICY_REQUIRED
ERROR_POLICY_REQUIRED
SECURITY_REVIEW_REQUIRED
BLOCKED
```

## Output

Use `assets/external-frontend-data-validation-record.md`.

## Completion Criteria

- [ ] External source and trust level are explicit.
- [ ] Structural importance is explicit.
- [ ] Runtime-validation decision is justified.
- [ ] TypeScript assertions are not treated as runtime proof.
- [ ] Validation occurs at the external boundary before inward mapping.
- [ ] HTTP decode and feature/provider validation are separated.
- [ ] External schema matches provider/persisted contract rather than Application DTO.
- [ ] Unknown-field policy is explicit.
- [ ] Missing/null/optional semantics are explicit.
- [ ] Provider enums and version behavior are explicit.
- [ ] Persisted browser data is treated as runtime external data when applicable.
- [ ] postMessage checks origin and payload independently.
- [ ] Imported/user data is validated safely.
- [ ] Validation-library types do not leak inward.
- [ ] Existing validation library is reused; no new library is introduced without approval.
- [ ] Validation failure becomes a stable contract-mismatch/unsupported-version semantic.
- [ ] User-facing messages do not expose raw validator details.
- [ ] Observability is redacted and avoids full sensitive payloads.
- [ ] Validation does not duplicate Domain/server business authority.
- [ ] Validation performance and duplicate validation are considered.
- [ ] Tests cover valid, missing, wrong type, enum, unknown-field, version, and mismatch cases as applicable.
- [ ] No raw external payload reaches Domain/Application without the accepted trust decision.
- [ ] Final validation status is explicit.
