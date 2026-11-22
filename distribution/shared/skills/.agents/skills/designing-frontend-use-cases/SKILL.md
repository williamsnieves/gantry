---
name: designing-frontend-use-cases
description: Designs frontend Application Use Cases around one user or system intention. Use when a frontend feature needs application-level orchestration across Domain behavior and ports. Define one primary operation, boundary-friendly input, Request DTOs when justified, Application DTO or explicit result output, failure semantics, cancellation, idempotency or duplicate-command behavior, and test seams. Keep Use Cases independent of React, JSX, browser globals, HTTP libraries, concrete adapters, component state, and presentation formatting. Do not chain Use Cases as implementation shortcuts, mirror endpoints mechanically, create Use Cases for trivial UI-only behavior, or move pure Domain rules into Application orchestration.
...
---

# Designing Frontend Use Cases

## Purpose

Design one frontend Application Use Case around one user or system intention.

A Use Case should answer:

```text
What is the user or system trying to accomplish?
```

not:

```text
Which endpoint are we calling?
Which component clicked?
Which hook owns this?
```

A Use Case coordinates:

```text
boundary-friendly input
→ ports
→ Domain behavior
→ application result
```

It remains independent of:

- React;
- JSX;
- browser globals;
- HTTP libraries;
- concrete adapters;
- CSS;
- routing;
- component state;
- view formatting.

## Governing Standard

A Use Case represents one user or system intention.

It SHOULD:

- expose one primary operation, commonly `execute`;
- orchestrate ports and Domain behavior;
- accept boundary-friendly input;
- return an Application DTO or `void`;
- remain independent from React and HTTP libraries.

A Use Case MUST NOT:

- call another Use Case as an implementation shortcut;
- import concrete adapters;
- contain presentation logic;
- return JSX;
- manage React state;
- depend on browser globals directly.

## Use When

- A user intention spans more than one lower-level operation.
- The frontend has an Application layer.
- Domain behavior and one or more ports must be coordinated.
- A workflow needs stable application-level failure semantics.
- A command or query needs cancellation semantics.
- Several presentation surfaces should invoke the same user intention.
- A feature needs orchestration independent from React.
- Offline/local behavior needs coordination with persistence or sync ports.
- A package boundary benefits from a stable application contract.

## Do Not Use When

- The behavior is a trivial UI interaction.
- The component only toggles local presentation state.
- The hook only synchronizes with an external system.
- A pure business rule belongs in Domain.
- The “Use Case” would only forward one repository call with no boundary value.
- The feature is Profile A and does not justify an Application layer.
- The operation is merely an adapter mapping concern.
- The proposed Use Case exists only because the backend has one.
- The proposed Use Case name mirrors an endpoint rather than an intention.

## Inputs

- Accepted user/system behavior.
- Architecture profile.
- Frontend Domain model, when present.
- Frontend ports/repository contracts, when present.
- Server-authority rules.
- Failure and cancellation semantics.
- Offline/local requirements.
- Idempotency or duplicate-command policy.
- Package/public-boundary requirements.
- Existing Application conventions.
- Test strategy.
- Repository-local `AGENTS.md`.

## Outputs

- Use Case justification decision.
- User/system intention statement.
- Primary operation.
- Input decision.
- Request DTO when justified.
- Port dependencies.
- Domain interaction.
- Output DTO/result decision.
- Failure semantics.
- Cancellation/race semantics.
- Duplicate-command/idempotency policy.
- Use Case test matrix.
- Frontend Use Case design record.

## Core Workflow

```text
accepted behavior
→ identify one intention
→ confirm Application-layer value
→ define input boundary
→ identify ports and Domain behavior
→ define orchestration
→ define output/result
→ define errors and cancellation
→ define tests
```

## Readiness Gate

Use one:

```text
READY_TO_DESIGN_FRONTEND_USE_CASE
READY_WITH_CONDITIONS
NO_USE_CASE_REQUIRED
INTENTION_REQUIRED
PORT_CONTRACT_REQUIRED
DOMAIN_DECISION_REQUIRED
FAILURE_SEMANTICS_REQUIRED
CANCELLATION_POLICY_REQUIRED
BLOCKED
```

A valid result may be:

```text
NO_USE_CASE_REQUIRED
```

Do not create Application ceremony when the behavior does not justify it.

## One Intention

A Use Case should represent one intention such as:

```text
LoadProfile
SubmitPayment
ApplyPromotion
SaveDraft
PublishDraft
RefreshDashboard
RestoreOfflineSession
```

The intention should be recognizable in product language.

Avoid names such as:

```text
CallProfileEndpoint
HandleButtonClick
ProcessData
DoRequest
UseCaseManager
```

## Command Versus Query

Classify:

```text
QUERY
COMMAND
COMMAND_WITH_RESULT
SYNC_ORCHESTRATION
LOCAL_WORKFLOW
```

### Query

Reads data without changing authoritative state.

Example:

```text
LoadProfile
```

### Command

Changes state and may return `void`.

Example:

```text
DismissLocalDraft
```

### Command with result

Changes state and returns an application result.

Example:

```text
SubmitPayment
→ PaymentSubmissionResult
```

Do not force CQRS terminology into repositories that do not use it.

## Use Case Justification

A Use Case is justified when it provides at least one:

- orchestration boundary;
- reusable intention across UI surfaces;
- stable failure contract;
- stable package boundary;
- Domain coordination;
- port coordination;
- local/offline workflow;
- deterministic application decision.

It may not be justified when:

```text
execute()
→ repository.get()
→ return unchanged data
```

unless that boundary itself has real stability/reuse value.

Use:

```text
USE_CASE_JUSTIFIED
USE_CASE_BOUNDARY_VALUE_ONLY
USE_CASE_OVERMODELED
NO_USE_CASE_REQUIRED
```

## Primary Operation

Prefer one primary operation:

```text
execute(input)
```

or repository-standard equivalent.

The operation should expose the intention directly.

Do not create a public API such as:

```text
prepare()
load()
validate()
send()
finalize()
```

when these are internal steps of one intention.

Internal pure helper functions are acceptable when they improve clarity.

## Input Boundary

For a few clear values, primitives are acceptable.

Example:

```text
execute(subscriptionId, campaignCode)
```

Use a named Request DTO when:

- parameter count harms readability;
- optional values exist;
- input has semantic meaning;
- the contract will evolve;
- input crosses a package boundary.

The “more than three parameters” rule is a heuristic, not a law.

## Primitive Input

Primitive input is appropriate when:

- there are one or two clear values;
- ordering is obvious;
- no optional/conditional fields exist;
- the contract is unlikely to evolve;
- no package boundary needs a named type.

Do not wrap one string in a Request DTO merely for ceremony.

## Request DTO

A Request DTO should:

- be serializable;
- express application intent;
- use stable Application language;
- avoid React/browser/provider types;
- avoid transport casing;
- avoid concrete adapter types.

Example:

```text
ApplyPromotionRequest
{
  subscriptionId: string
  campaignCode: string
}
```

Not:

```text
ApplyPromotionHttpRequest
{
  subscription_id: string
  code_from_form: string
  onSuccess: () => void
}
```

## Request DTO Evolution

A Request DTO is useful when the contract may evolve.

Example:

```text
PublishDraftRequest
{
  draftId
  expectedVersion?
  publishMode?
}
```

Optional fields should have clear semantics.

Do not use catch-all option bags with unrelated flags.

## Domain Types as Input

A Use Case may accept Domain types when that is the accepted boundary.

Example:

```text
execute(draft: LessonPlanDraft)
```

But do not force presentation to construct complex Domain objects merely to invoke a simple intention.

The boundary should remain ergonomic and stable.

## Input Validation

Separate:

```text
boundary shape
domain invariant
server authority
```

The Use Case may:

- validate required Application input shape;
- create/parse Domain Value Objects;
- call Domain behavior;
- return stable input/domain errors.

Do not duplicate server-only authority rules.

## Port Dependencies

A Use Case may depend on:

- repository ports;
- external-service ports;
- clock;
- ID generator;
- feature flags;
- analytics port;
- local persistence port;
- sync port;
- authorization capability abstraction.

Dependencies should speak Application or Domain language.

Do not inject:

```text
fetch
AxiosInstance
HttpClient
localStorage
window
router
SWR cache
React Query client
```

unless the accepted architecture explicitly defines an outer adapter around them and the Use Case depends on that semantic port instead.

## Concrete Adapters

Use Cases MUST NOT import concrete adapters.

Bad:

```text
import { HttpPromotionRepository } from "../infrastructure/..."
```

Preferred:

```text
constructor(private promotionRepository: PromotionRepository)
```

or the repository's accepted explicit dependency pattern.

## Domain Interaction

A Use Case orchestrates Domain behavior.

Example:

```text
load draft
→ draft.publishCandidate()
→ persist/send
→ return application result
```

It should not reimplement Domain invariants.

If a rule is pure and belongs to one Domain concept, put it there.

## No-Domain Use Cases

A Use Case may exist without a Domain layer.

Example:

```text
LoadProfile
→ ProfileRepository
→ ProfileDTO
```

This can be valid when the Application boundary has reuse/package/failure value.

Do not invent Domain solely because a Use Case exists.

## Orchestration

Application orchestration may include:

- load;
- call Domain behavior;
- save;
- call external service;
- translate stable outcomes;
- coordinate local and remote ports;
- emit analytics through a port when accepted;
- handle cancellation.

Do not include:

- JSX construction;
- toast rendering;
- focus management;
- CSS decision;
- router navigation;
- modal open/close state.

Those belong outward.

## Presentation Logic

A Use Case MUST NOT decide:

```text
show red banner
open modal
focus campaign input
render <ErrorAlert />
navigate("/success")
```

It may return semantic outcomes such as:

```text
INVALID
EXPIRED
FORBIDDEN
UNAVAILABLE
SUCCESS
```

Presentation decides how to render them.

## Chained Use Cases

A Use Case MUST NOT call another Use Case as an implementation shortcut.

Bad:

```text
PublishDraft.execute()
→ SaveDraft.execute()
→ SyncDraft.execute()
```

This creates:

- hidden orchestration;
- circular application dependencies;
- unclear ownership;
- difficult testing;
- duplicated policy.

Instead extract:

- shared Domain behavior;
- a lower-level port;
- a shared pure helper;
- one higher-level Use Case that owns the orchestration.

## Legitimate Reuse

If two Use Cases share behavior, ask where it belongs:

```text
pure business rule
→ Domain

shared external capability
→ port

pure application mapping
→ Application helper

common provider behavior
→ Infrastructure
```

Do not use Use Case composition as a general reuse mechanism.

## Output

Use Cases SHOULD return:

```text
Application DTO
explicit Application result
primitive
void
```

according to repository conventions.

They SHOULD NOT return:

- transport responses;
- provider SDK objects;
- JSX;
- ReactNode;
- component props tied to a design system;
- browser objects.

## Application DTO

An Application DTO should contain:

- serializable data;
- stable boundary semantics;
- primitives and application-safe structures.

Example:

```text
ProfileDTO
{
  id: string
  displayName: string
  avatarUrl?: string
}
```

Do not return snake_case provider responses directly.

## Explicit Result Types

Use an explicit result type when callers need to distinguish semantic outcomes.

Example:

```text
ApplyPromotionResult =
  | { type: "applied"; promotion: PromotionDTO }
  | { type: "invalid" }
  | { type: "expired" }
  | { type: "forbidden" }
  | { type: "unavailable" }
```

This may be preferable to exceptions when outcomes are expected and recoverable.

Follow repository conventions.

## Result Type Restraint

Do not create a union for every function merely because unions are explicit.

Use them when callers need differentiated outcomes.

If the operation either succeeds or throws a stable application error by project convention, preserve that convention.

## `void`

Return `void` when:

- caller only needs completion/failure;
- no meaningful application result exists.

Do not return `{ success: true }` without semantic value.

## View Models

Use Cases SHOULD NOT return UI view models tied to:

- React;
- component library;
- locale rendering;
- icons;
- colors;
- CSS.

UI-specific formatting belongs outward.

Application DTOs may include semantic data that Presentation formats.

## Date Output

Decide whether Application DTOs return:

- ISO string;
- epoch;
- domain-safe serialized date;
- stable date primitive.

Presentation may format for locale.

Do not return already-localized `"7 Aug 2026, 14:00"` unless localization is explicitly Application-owned in that repository.

## Errors

Failures should remain distinguishable where callers need different behavior.

Potential categories:

```text
VALIDATION
NOT_FOUND
FORBIDDEN
UNAUTHENTICATED
CONFLICT
UNAVAILABLE
TIMEOUT
CANCELLED
CONTRACT_MISMATCH
UNKNOWN
```

Use only categories relevant to the intention.

Do not collapse every failure to:

```text
undefined
false
"Something went wrong"
```

## Domain Errors

A Use Case may translate Domain errors into stable Application results/errors when the application boundary benefits.

Do not erase semantic meaning.

Example:

```text
InvalidCampaignCode
→ { type: "invalid" }
```

if that is the accepted Application contract.

## Infrastructure Errors

Concrete adapter errors should already be translated to stable port semantics.

The Use Case should not inspect:

```text
HTTP 409
AxiosError
Response.status
provider error code
```

unless such details are explicitly part of the port contract, which is normally discouraged.

## Cancellation

Async Use Cases and their consumers SHOULD support cancellation where requests can become obsolete.

Possible input:

```text
execute(request, signal)
```

or an accepted semantic cancellation abstraction.

Do not force AbortSignal into Domain.

Cancellation may be part of Application or port boundary according to project conventions.

## Cancellation Semantics

Define what cancellation means:

```text
CANCELLED_RESULT
THROW_STABLE_CANCELLED_ERROR
SILENT_ABORT_TO_CALLER
```

Do not expose cancellation as generic unavailable/system failure if callers need to distinguish it.

## Stale Responses

The UI MUST prevent stale responses from overwriting newer state.

The Use Case may participate by:

- accepting cancellation;
- exposing request identity if accepted;
- ensuring port operations can abort.

But Presentation/hook/server-state orchestration may own latest-wins policy.

Do not move UI race state into the Use Case unnecessarily.

## Duplicate Commands

For commands such as payment/submission/publish, define duplicate policy:

```text
ALLOW_CONCURRENT
REJECT_WHILE_PENDING
IDEMPOTENT_BY_KEY
QUEUE
OUTER_LAYER_OWNS
```

The Use Case should own duplicate policy only if it is application semantics.

If duplicate prevention is purely UI interaction state, Presentation may own it.

## Idempotency

Idempotency may require:

- idempotency key;
- stable command ID;
- repository/server support.

Do not invent client-only idempotency when backend semantics are required.

Record authority explicitly.

## Loading State

Use Cases do not manage React loading state.

They may expose async lifecycle through Promise completion/failure.

Presentation or hook decides:

```text
idle
loading
success
error
```

Do not return mutable loading flags from the Use Case.

## Progress

Long-running operations may expose progress through an accepted semantic port/stream when needed.

Do not make Use Case APIs framework-specific.

Possible semantic interface:

```text
UploadProgressPort
```

or async iterable according to repository conventions.

Do not use React callbacks merely because the caller is React.

## Browser Globals

Use Cases MUST NOT access:

```text
window
document
navigator
localStorage
sessionStorage
location
history
clipboard
Notification
```

directly.

If browser capability matters, inject a semantic port.

Examples:

```text
ClipboardPort
GeolocationPort
BrowserStoragePort
NavigationIntentPort
```

Only create these when Application truly owns the capability.

## Routing

Navigation is usually Presentation/Infrastructure composition.

A Use Case may return:

```text
{ type: "completed"; destinationId }
```

but should not call router APIs directly.

Do not hide route navigation inside Application orchestration without an accepted project policy.

## Analytics

Analytics may be a port when recording an event is part of the application intention.

Example:

```text
PromotionAnalytics.recordApplied(...)
```

Do not inject a provider SDK.

Do not let analytics failure accidentally fail the user intention unless that policy is explicit.

## Feature Flags

Feature flags may enter through a semantic port or configuration.

Avoid provider SDK imports.

Define whether the flag is:

- evaluated before Use Case;
- passed as input;
- queried through an Application port.

Do not scatter flag provider checks through Domain and Application.

## Authorization

Frontend authorization is never the final security authority.

A Use Case may use capability/permission data to support UX flow, but backend enforcement remains authoritative.

Do not assume a hidden button secures an operation.

## Offline Use Cases

Offline workflows may coordinate:

```text
local repository
Domain behavior
sync queue port
connectivity capability
```

Example:

```text
SaveDraft
```

may persist locally without remote availability.

Keep IndexedDB implementation outside Application.

## Sync Use Cases

A sync intention may:

- load pending domain items;
- invoke sync port;
- reconcile stable outcomes;
- persist results.

Do not embed provider-specific sync protocol in the Use Case.

## Payment Use Cases

Payment is high-impact.

A payment Use Case may coordinate:

- accepted payment input;
- payment port;
- order repository;
- stable result.

Frontend must not become the final authority for payment success.

Do not log or return sensitive provider details unnecessarily.

## Loading a Profile

A simple query Use Case may be valid:

```text
LoadProfile.execute(userId)
```

when it provides:

- stable port boundary;
- mapping to Application DTO;
- reusable intention;
- failure semantics.

It may be overkill in a tiny Profile A feature with one direct approved server-state adapter and no Application layer.

## Submitting a Payment

Good Application boundary:

```text
SubmitPayment.execute(request)
→ PaymentPort
→ OrderRepository
→ PaymentResult
```

No JSX.

No Stripe/Adyen SDK type.

No router navigation.

No button state.

## Request DTO Decision

Use a named Request DTO when it improves:

- readability;
- evolution;
- semantics;
- package stability.

Do not use a numeric parameter threshold mechanically.

Example:

```text
submitPayment(
  orderId,
  paymentMethodId,
  rememberMethod,
  returnUrl?
)
```

likely benefits from:

```text
SubmitPaymentRequest
```

But:

```text
loadProfile(userId)
```

does not need `LoadProfileRequest` by default.

## Chained Use Case Example

Reject:

```text
ApplyPromotion
→ ValidatePromotion
→ SavePromotion
```

if those are Use Cases.

Instead:

```text
ApplyPromotion
→ CampaignCode Value Object
→ PromotionRepository
→ Promotion result
```

or a lower-level Application/Domain helper.

## Transaction-Like Orchestration

Frontend Use Cases cannot create backend transactions merely by sequencing API calls.

If atomicity is required, backend must provide an appropriate contract.

The Use Case should model partial failure and recovery honestly.

Do not imply distributed transaction guarantees that do not exist.

## Partial Success

When one intention has several effects, define partial success.

Example:

```text
draft saved locally
remote sync failed
```

Possible result:

```text
{ type: "saved-locally-pending-sync" }
```

Do not report complete success if accepted behavior distinguishes it.

## Retries

Use Cases may expose retryable failure semantics.

Retry mechanism ownership may belong to:

- adapter;
- server-state library;
- hook;
- Use Case.

Choose one according to architecture.

Do not layer retries unknowingly.

## Side Effects

Use Cases are allowed to orchestrate side effects through ports.

They are not pure functions by definition.

But side effects should be explicit dependencies.

Examples:

```text
repository.save
analytics.record
sync.enqueue
payment.submit
```

Do not hide side effects through globals.

## Dependency Count

Many dependencies may signal that one Use Case owns too much.

Diagnostic:

```text
8+ unrelated ports
```

Ask whether the intention is too broad.

Do not impose a hard dependency-count limit.

## Use Case Granularity

Too broad:

```text
ManageAccount
```

with many unrelated operations.

Too narrow:

```text
SetLoadingTrue
```

Good:

```text
UpdateProfile
ChangePassword
DeleteAccount
```

Use product intentions.

## Public Surface

If the Use Case crosses a package boundary, expose:

- stable Request DTO;
- stable result DTO/type;
- port-free consumer API where possible.

Do not expose concrete adapter construction.

## Use Case Factory

Construction belongs at composition root.

Example:

```text
createApplyPromotionUseCase(...)
```

or DI registration according to project policy.

Use Case code itself must not access the Factory.

## Testability

Design Use Cases so tests can use:

- InMemory repositories;
- stubs/spies for true external service ports;
- fake clock/ID generator;
- deterministic data.

Do not require React render tests for Application behavior.

## Use Case Tests

Use Case tests SHOULD use InMemory repository implementations.

Do not mock repositories when an InMemory implementation can exercise the real port contract.

Stubs/spies are allowed for true external-service ports.

Test:

- intention success;
- meaningful semantic failures;
- orchestration;
- persisted state;
- cancellation;
- idempotency/duplicate behavior when Application-owned;
- partial success when applicable.

## Avoid Interaction-Only Tests

Do not test:

```text
repository.save called before analytics.record
```

unless ordering is part of accepted behavior.

Prefer final semantic outcome and resulting state.

## No JSX Evaluation

A Use Case returning:

```tsx
return <PaymentSuccess />
```

is a mandatory violation.

Return semantic data:

```text
{ type: "success"; receiptId }
```

Presentation decides rendering.

## No React State Evaluation

Reject Use Cases that:

- accept `setState`;
- return setters;
- use `useState`;
- use `useEffect`;
- expose `ReactNode`;
- manage component lifecycle.

## No HttpClient Evaluation

Reject:

```text
constructor(private httpClient: HttpClient)
```

when the Use Case should depend on a semantic port.

Application should not know:

- URL;
- HTTP verb;
- transport headers;
- provider DTO;
- response status.

## Final Decision

Use:

```text
FRONTEND_USE_CASE_READY
FRONTEND_USE_CASE_READY_WITH_CONDITIONS
NO_USE_CASE_REQUIRED
RETURN_TO_DOMAIN_OR_PORT_DESIGN
REQUEST_DTO_REQUIRED
RESULT_CONTRACT_REQUIRED
FAILURE_SEMANTICS_REQUIRED
CANCELLATION_POLICY_REQUIRED
BLOCKED
```

## Output

Use `assets/frontend-use-case-design-record.md`.

## Completion Criteria

- [ ] One user/system intention is explicit.
- [ ] Use Case justification is explicit.
- [ ] `NO_USE_CASE_REQUIRED` is accepted as valid.
- [ ] One primary operation is defined.
- [ ] Input is boundary-friendly.
- [ ] Request DTO is used only when readability, optionality, evolution, semantics, or package boundary justify it.
- [ ] Dependencies are semantic ports, not concrete adapters or browser/HTTP globals.
- [ ] Domain behavior is orchestrated rather than duplicated.
- [ ] Use Case does not call another Use Case as implementation reuse.
- [ ] Output is Application DTO, explicit result, primitive, or `void`.
- [ ] No transport response, JSX, ReactNode, or component-library view model leaks out.
- [ ] Presentation decisions remain outside.
- [ ] Failure categories are distinguishable where caller behavior differs.
- [ ] Cancellation semantics are explicit when work can become obsolete.
- [ ] Stale-response ownership is explicit.
- [ ] Duplicate-command/idempotency ownership is explicit when relevant.
- [ ] Offline/partial-success semantics are explicit when relevant.
- [ ] Browser capabilities are behind semantic ports when Application-owned.
- [ ] Use Case construction belongs to composition.
- [ ] Tests can use InMemory repositories and explicit external-port doubles.
- [ ] No new Domain rule, adapter, framework, library, or project policy is invented.
- [ ] Final Use Case decision is explicit.
