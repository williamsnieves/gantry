---
name: designing-frontend-ports
description: Designs frontend repository and external-service ports around what Domain/Application needs rather than how browser, provider, transport, storage, analytics, clipboard, files, notifications, geolocation, clock, cache, or sync implementations work. Use to define product-language contracts, port ownership, stable inputs/outputs, not-found semantics, failure categories, cancellation, cache-awareness, idempotency, subscriptions, and test doubles. Keep provider SDKs, fetch/HTTP, localStorage/IndexedDB APIs, navigator/window/document, analytics vendor events, browser File handles, and concrete cache libraries outside ports. Do not mirror provider APIs, expose generic getJson/request methods, make every browser capability a port, or create repository interfaces for endpoints with no meaningful application/domain contract.
...
---

# Designing Frontend Ports

## Purpose

Design frontend ports that express:

```text
what the application needs
```

rather than:

```text
how a provider/browser API works
```

A port is an inward-facing contract.

It hides:

- transport;
- browser APIs;
- provider SDKs;
- storage implementation;
- analytics vendor;
- cache implementation;
- synchronization protocol.

Typical frontend ports may represent:

- repositories;
- remote data access;
- browser persistence;
- offline collections;
- cache-backed collections;
- BFF access;
- analytics;
- clipboard;
- files;
- notifications;
- geolocation;
- clock/time;
- IDs;
- connectivity;
- synchronization.

## Governing Standard

Ports describe what the application needs, not how a provider works.

Port names and methods SHOULD use product language.

Avoid:

```ts
interface OrderRepository {
  getJson(path: string): Promise<unknown>
}
```

Prefer:

```ts
interface OrderRepository {
  findById(id: Id): Promise<Order | undefined>
  save(order: Order): Promise<void>
}
```

A frontend repository may represent:

- remote API access;
- browser persistence;
- cache-backed collections;
- offline synchronization;
- a BFF;
- local indexed storage.

The port MUST hide those implementation details.

## Use When

- A Use Case needs an external capability.
- Domain models persistence or collection access.
- A feature needs browser storage without coupling inward to storage APIs.
- Analytics should be replaceable and product-semantic.
- Clipboard/files/geolocation/notifications are part of an application intention.
- Time or IDs must be deterministic/testable.
- Offline sync needs an explicit contract.
- Cache behavior affects application semantics.
- Provider replacement or testability matters.
- Application needs stable failure/cancellation semantics.

## Do Not Use When

- A component only needs local presentation state.
- The proposed interface simply mirrors one endpoint.
- The capability is used only inside one Infrastructure adapter.
- The port would expose `fetch`, Axios, `Response`, `localStorage`, IndexedDB transactions, browser `FileSystemHandle`, or provider SDK objects.
- The feature is Profile A and a direct approved Infrastructure abstraction is sufficient.
- A Domain repository is proposed with no meaningful Domain collection/persistence concept.
- A browser capability has no Application-level meaning.
- The abstraction exists only “for testability” but has no stable semantic boundary.

## Inputs

- Accepted user/system intention.
- Architecture profile.
- Domain model.
- Use Case design.
- DTO/result design.
- External provider/browser capability.
- Failure semantics.
- Cancellation/race policy.
- Offline/cache policy.
- Security/privacy requirements.
- Package/public boundary.
- Existing port conventions.
- Existing Infrastructure capabilities.
- Test strategy.
- Repository-local `AGENTS.md`.

## Outputs

- Port justification.
- Port owner: Domain or Application.
- Port category.
- Product-language name.
- Method contract(s).
- Input/output boundary types.
- Not-found semantics.
- Failure semantics.
- Cancellation semantics.
- Cache/sync semantics where applicable.
- Subscription/lifecycle semantics where applicable.
- Security/privacy constraints.
- Test-double strategy.
- Frontend port design record.

## Core Workflow

```text
accepted intention
→ identify external capability
→ decide whether a port is justified
→ decide Domain vs Application ownership
→ name in product language
→ design narrow methods
→ define data/error/cancellation semantics
→ define cache/sync/lifecycle rules
→ define test doubles
```

## Readiness Gate

Use one:

```text
READY_TO_DESIGN_FRONTEND_PORT
READY_WITH_CONDITIONS
NO_PORT_REQUIRED
PORT_OWNER_REQUIRED
CAPABILITY_SEMANTICS_REQUIRED
FAILURE_SEMANTICS_REQUIRED
CANCELLATION_POLICY_REQUIRED
CACHE_POLICY_REQUIRED
SECURITY_POLICY_REQUIRED
BLOCKED
```

A valid outcome may be:

```text
NO_PORT_REQUIRED
```

Do not create interfaces merely because hexagonal architecture exists.

# Port Ownership

Use:

```text
DOMAIN_PORT
APPLICATION_PORT
NO_PORT_REQUIRED
OWNERSHIP_REQUIRES_DECISION
```

## Domain Repository Port

A repository MAY belong to Domain when the frontend genuinely models:

- persistence of Domain entities/aggregates;
- Domain collections;
- offline Domain storage;
- remote collection access expressed in Domain language.

Example:

```text
DraftRepository {
  findById(id: DraftId): Promise<LessonPlanDraft | undefined>
  save(draft: LessonPlanDraft): Promise<void>
}
```

It should remain meaningful even if the implementation changes from:

```text
IndexedDB
→ remote API
→ cache-backed adapter
```

## Application Port

Application owns external-service capabilities used for orchestration.

Examples:

```text
PaymentPort
AnalyticsPort
ClipboardPort
NotificationPort
GeolocationPort
Clock
IdGenerator
ConnectivityPort
SyncPort
```

Application ports can also model remote capabilities that are not naturally Domain repositories.

## Ownership Heuristic

Ask:

```text
Would Domain need this abstraction without the current Use Case?
```

If yes, Domain ownership may be justified.

If the abstraction exists because Application orchestrates an external capability, Application is usually the better owner.

Do not move all ports into Domain mechanically.

# Port Categories

Classify:

```text
REPOSITORY
EXTERNAL_SERVICE
BROWSER_CAPABILITY
TIME
IDENTITY
ANALYTICS
CACHE
SYNC
CONNECTIVITY
SUBSCRIPTION
FILE_ACCESS
NOTIFICATION
OTHER_SEMANTIC_CAPABILITY
```

The category does not dictate folder structure by itself.

# Product-Language Contracts

Good:

```text
ProfileRepository.findById(userId)
PromotionRepository.apply(...)
LessonDraftRepository.save(draft)
ClipboardPort.copyText(text)
PaymentPort.submit(request)
```

Weak:

```text
ApiService.get(url)
StorageService.setItem(key, value)
BrowserService.execute(action)
AnalyticsService.track(name, payload)
```

Names should reveal product/capability semantics.

# Narrow Interfaces

Prefer narrow contracts.

Good:

```text
interface ClipboardPort {
  copyText(text: string): Promise<void>
}
```

Avoid:

```text
interface BrowserPort {
  clipboard: ...
  geolocation: ...
  notifications: ...
  files: ...
}
```

unless the project has an intentional capability facade with stable semantics.

Interface Segregation applies.

# Repository Contracts

Repositories should speak collection/persistence language.

Potential operations:

```text
findById
findAll
search
save
remove
exists
listPending
```

Only include methods required by accepted behavior.

Do not add CRUD completeness automatically.

Bad:

```text
create
read
update
delete
list
search
count
bulkUpdate
```

when the feature only needs `findById`.

# Endpoint Mirroring

Reject endpoint-shaped ports such as:

```text
getSubscriptionEndpoint()
postPromotionEndpoint()
callV2CampaignApi()
```

A port should survive URL/verb/provider changes.

Good:

```text
PromotionRepository.apply(subscriptionId, campaignCode)
```

if applying a promotion is genuinely repository semantics.

But if it represents a command-oriented remote capability rather than persistence, an Application service port may be clearer.

# Repository vs External-Service Port

Use repository when the abstraction represents:

- collection access;
- persistence;
- retrieval by identity;
- save/remove semantics.

Use external-service port when it represents:

- an action/capability;
- payment;
- analytics;
- notification delivery;
- geolocation lookup;
- clipboard;
- file picker;
- sync command.

Do not call every HTTP-backed dependency a repository.

# Inputs

Port inputs SHOULD use:

- Domain types;
- Application DTOs/request values;
- primitives;
- serialization-safe boundary types.

They SHOULD NOT use:

```text
Request
Response
AxiosRequestConfig
FormData
DOM Event
React SyntheticEvent
HTMLElement
provider SDK object
```

unless the port is explicitly a low-level outer abstraction and not an inward Application/Domain port.

# Outputs

Port outputs SHOULD use:

- Domain entities/Value Objects for Domain repository ports;
- Application-safe DTOs/results/primitives for Application ports;
- `void` when no result is semantically needed.

Do not return:

- raw API payload;
- AxiosResponse;
- Firebase object;
- browser-specific handle;
- analytics SDK result;
- cache library object.

# Not-Found Semantics

Define not-found intentionally.

Use one accepted model:

```text
undefined
null
Maybe<T>
NOT_FOUND result
stable typed error
```

according to repository conventions.

`undefined` may be appropriate for repository lookup:

```text
findById(id): Promise<Entity | undefined>
```

Do not use the same absence representation for:

```text
network failure
forbidden
malformed payload
cancelled
```

## Not Found Is Not Failure by Default

Repository lookup:

```text
findById
```

may treat absence as a valid result.

But commands such as:

```text
applyPromotion
submitPayment
```

may require an explicit semantic `not_found`/`invalid_target` outcome.

Define per capability.

# Failure Semantics

Failures MUST remain distinguishable when caller behavior differs.

Potential stable categories:

```text
UNAVAILABLE
UNAUTHENTICATED
FORBIDDEN
NOT_FOUND
CONFLICT
TIMEOUT
CANCELLED
CONTRACT_MISMATCH
RATE_LIMITED
UNKNOWN
```

Use only what the application needs.

Ports SHOULD NOT expose:

```text
HTTP 401
HTTP 409
AxiosError
DOMException name
Firebase error code
provider SDK exception
```

Adapters translate provider failures to stable port semantics.

# Typed Results vs Errors

Use the repository's accepted convention.

Possible designs:

```text
Promise<Result<T, PortError>>
```

or:

```text
Promise<T>
throws stable typed errors
```

or command-specific discriminated result.

Do not invent a new universal `Result` abstraction for one port.

# Error Granularity

Granularity should match caller decisions.

If the application treats:

```text
network unavailable
provider maintenance
DNS failure
```

identically, one stable `UNAVAILABLE` category may be enough.

Do not preserve provider detail without application value.

# Cancellation

Async ports SHOULD support cancellation where operations can become obsolete.

Potential contract:

```text
findById(id, signal?)
```

or:

```text
execute(request, cancellation)
```

according to project conventions.

Keep cancellation abstraction out of Domain Value Objects/entities.

## AbortSignal

`AbortSignal` is a web-platform type.

Whether it may appear in an Application port is a project architecture decision.

Options:

```text
ALLOW_WEB_STANDARD_ABORT_SIGNAL
USE_APPLICATION_CANCELLATION_PORT
ADAPTER_OWNS_CANCELLATION_ONLY
```

Prefer consistency.

Do not expose Axios cancellation tokens or vendor-specific cancel objects inward.

## Cancellation Semantics

Define:

```text
cancelled result
stable cancellation error
silent cancellation
```

Cancellation MUST NOT be collapsed into generic unavailable if the application reacts differently.

# Race Ownership

Ports provide cancellation capability where appropriate.

They do not necessarily own latest-wins UI policy.

Classify:

```text
PORT_SUPPORTS_CANCELLATION
USE_CASE_OWNS_RACE_POLICY
HOOK_SERVER_STATE_OWNS_RACE_POLICY
ADAPTER_OWNS_DEDUPLICATION
```

Do not embed React-specific request sequencing into a port.

# Browser Storage Ports

Do not expose:

```text
localStorage.getItem
localStorage.setItem
IDBDatabase
IDBTransaction
```

inward.

Bad:

```text
StoragePort {
  getItem(key: string): string | null
}
```

when the application actually needs:

```text
DraftRepository.findById(draftId)
DraftRepository.save(draft)
```

However, a generic storage port may be justified for a truly generic application capability such as feature preferences.

Use semantic naming:

```text
UserPreferenceStore
SessionPersistencePort
DraftRepository
```

# localStorage Example

Weak:

```text
LocalStoragePort {
  getItem(key)
  setItem(key, value)
}
```

Preferred if product semantics are:

```text
ThemePreferenceStore {
  load(): Promise<ThemePreference | undefined>
  save(preference: ThemePreference): Promise<void>
}
```

Infrastructure can implement it with localStorage.

# IndexedDB Example

Domain/Application contract:

```text
DraftRepository
```

Infrastructure:

```text
IndexedDbDraftRepository
```

The port knows nothing about object stores, indexes, versions, transactions, or browser upgrade events.

# Analytics Ports

Analytics ports should express semantic product events.

Weak:

```text
AnalyticsPort.track(eventName: string, payload: Record<string, unknown>)
```

Preferred when stable event semantics matter:

```text
PromotionAnalyticsPort {
  recordApplied(category: PromotionCategory): Promise<void>
  recordRejected(reason: PromotionRejection): Promise<void>
}
```

or an accepted typed event union.

Do not expose vendor event names/properties inward.

## Analytics Failure

Define whether analytics is:

```text
BEST_EFFORT
REQUIRED_FOR_INTENTION
OUTER_LAYER_ONLY
```

Usually analytics failure SHOULD NOT fail the user intention unless policy explicitly requires it.

# Analytics Privacy

Port design should constrain payloads to allowed semantic data.

Do not create:

```text
track(name, anyPayload)
```

if privacy policy requires strict fields.

Prefer types that make prohibited PII difficult to send.

# Clipboard Port

Application-level need:

```text
ClipboardPort {
  copyText(text: string): Promise<void>
}
```

Stable failures may include:

```text
PERMISSION_DENIED
UNAVAILABLE
CANCELLED
UNKNOWN
```

Do not expose `navigator.clipboard`.

Do not return `ClipboardItem` unless that is intentionally part of an outer framework boundary rather than Application.

# File Access Ports

Decide whether Application needs:

- selected file metadata/content;
- uploadable byte stream;
- semantic document input.

Avoid leaking:

```text
FileSystemFileHandle
showOpenFilePicker
input[type=file] event
```

into Application.

A browser `File` may or may not be acceptable depending on project policy and package/server boundaries.

Prefer stable application representation when portability matters.

Examples:

```text
SelectedFile {
  name
  mediaType
  size
  bytes/stream abstraction
}
```

Do not invent a binary abstraction if the browser `File` is deliberately accepted at the outer Presentation boundary.

# Geolocation Port

Application need:

```text
GeolocationPort {
  getCurrentPosition(): Promise<GeoPosition>
}
```

Define:

```text
permission denied
unavailable
timeout
cancelled
```

Do not expose `GeolocationPosition` provider/browser object unless explicitly accepted.

Domain may define semantic coordinates/value objects if location has business meaning.

# Notification Port

Potential application contract:

```text
NotificationPort {
  requestPermission(): Promise<NotificationPermissionResult>
  notify(message: NotificationMessage): Promise<void>
}
```

But ask whether permission prompting belongs in Presentation.

Do not create a notification port automatically because browser Notifications exist.

Port only the capability that Application actually owns.

# Time / Clock Port

Use a Clock when Application behavior depends on current time.

Example:

```text
Clock {
  now(): Instant
}
```

Benefits:

- deterministic tests;
- no direct `Date.now()` in Application;
- stable time semantics.

Do not create Clock merely because a timestamp is displayed.

Presentation formatting does not justify an Application Clock.

# ID Generator

Use:

```text
IdGenerator {
  next(): Id
}
```

when Application needs locally generated identity.

Do not inject random ID generators into Domain entities globally unless identity creation semantics require it.

# Connectivity Port

Use when offline behavior needs meaningful connectivity information.

Example:

```text
ConnectivityPort {
  getStatus(): ConnectivityStatus
  subscribe(listener): Unsubscribe
}
```

Do not assume `navigator.onLine` is authoritative connectivity.

Adapter may combine browser/network/provider signals.

Application contract should describe product-meaningful connectivity semantics.

# Sync Port

Sync ports should hide protocol details.

Good:

```text
DraftSyncPort {
  sync(draft: LessonPlanDraft, options?): Promise<DraftSyncResult>
}
```

Avoid:

```text
postToSyncV2(payload)
```

Define partial success/conflict semantics.

# Subscription Ports

For ongoing external events, define lifecycle.

Example:

```text
PromotionStatusPort {
  subscribe(
    subscriptionId,
    listener
  ): Unsubscribe
}
```

or an async-iterable/stream abstraction according to project conventions.

Specify:

- subscription key;
- event semantics;
- unsubscribe;
- error behavior;
- reconnection ownership;
- ordering;
- duplicate event policy.

Do not expose vendor observable types inward unless explicitly accepted.

# Cache-Aware Contracts

A port may be cache-aware only when cache semantics matter to Application.

Possible distinctions:

```text
CACHE_TRANSPARENT
CACHE_POLICY_APPLICATION_VISIBLE
STALE_WHILE_REVALIDATE_VISIBLE
OFFLINE_CACHE_VISIBLE
```

Default:

```text
cache is Infrastructure detail
```

Do not add:

```text
forceCache
cacheKey
staleTime
queryKey
```

to ports unless the application intention genuinely depends on those semantics.

# Cache Transparent Repository

Application:

```text
ProfileRepository.findById(id)
```

Infrastructure may use:

```text
memory cache
IndexedDB
HTTP
SWR cache
```

without changing the port.

Preferred when callers only need the latest acceptable semantic data.

# Cache-Aware Example

If product behavior explicitly distinguishes:

```text
fresh
stale but usable
offline cached
```

the port may return semantic freshness:

```text
CachedResult<T> {
  value: T
  freshness: "fresh" | "stale" | "offline"
}
```

Do not return cache-library metadata.

# Invalidation

Application-visible invalidation is justified only when it is part of product semantics.

Avoid:

```text
invalidateQuery(["profile", id])
```

inside Application.

Prefer semantic command:

```text
ProfileCachePort.invalidate(userId)
```

only if Application genuinely owns cache invalidation.

Often server-state infrastructure should own this instead.

# Pagination

Repositories may expose stable pagination semantics when application behavior needs them.

Example:

```text
search(request): Promise<Page<Order>>
```

with:

```text
items
nextCursor?
```

Do not expose provider envelopes or page headers.

Do not invent a universal page abstraction if semantics differ materially.

# Search / Filtering

Port filters should express product query semantics.

Good:

```text
OrderSearch {
  status?
  customerId?
  cursor?
}
```

Avoid:

```text
Record<string, string>
URLSearchParams
queryString
```

in inward contracts.

# Batch Operations

Add batch methods only when accepted behavior needs them.

Do not optimize API request count by adding port methods with no product/application contract.

Infrastructure may batch under a single semantic method transparently.

# Transactions

Frontend ports must not promise backend atomic transactions they cannot guarantee.

If an operation requires atomicity, the backend/provider contract must support it.

Name/result should reflect partial success honestly.

# Idempotency

A port may expose idempotency input if the underlying capability and Application contract support it.

Example:

```text
submitPayment(request, idempotencyKey)
```

or include key in request DTO.

Do not claim idempotency from local duplicate suppression alone.

# Security

Port design should minimize sensitive exposure.

Avoid returning:

- access tokens;
- refresh tokens;
- provider credentials;
- raw auth headers;
- secret config.

Prefer capability-semantic results.

Do not put secrets in frontend ports at all if they should never enter the client.

# Authorization

Ports may expose capability results:

```text
PermissionPort.canPublish(...)
```

when UX needs them.

But frontend permission results do not replace backend authorization.

Do not model server security as a client guarantee.

# Privacy

Analytics, files, geolocation, notifications, and storage ports may handle sensitive data.

Record:

- permitted fields;
- retention assumptions;
- user consent;
- redaction;
- third-party boundary.

Do not widen port inputs beyond actual need.

# Server / Client Boundary

For SSR/server-client projects, classify the port runtime:

```text
SERVER_ONLY
CLIENT_ONLY
ISOMORPHIC
SPLIT_IMPLEMENTATION
```

Application contract may be shared while adapters differ.

Example:

```text
ProfileRepository
→ server adapter
→ client adapter
```

only when semantics are equivalent.

Do not resolve browser-only ports on the server.

# Lifecycle

Define dependency lifecycle where relevant:

```text
PER_CALL
PER_COMPONENT_TREE
PER_ROUTE
PER_REQUEST
PER_USER_SESSION
APPLICATION_SINGLETON
```

Port contract itself is usually lifecycle-agnostic, but design should identify adapter constraints.

Avoid singleton contracts carrying request/user mutable state.

# Provider Replacement

A good port should survive provider replacement when semantics remain.

Diagnostic:

```text
If we replace provider X,
does the port name/method still make sense?
```

If no, provider details may have leaked.

Do not abstract provider-unique semantics into fake generic language if the product itself truly depends on those semantics.

# Provider-Specific Product Semantics

Sometimes a provider concept becomes product semantics.

Example:

```text
PaymentRequiresAction
```

may be meaningful even if originally provider-driven.

Decide whether product behavior has adopted the concept.

Do not erase meaningful distinctions merely to appear provider-independent.

# Generic Port Anti-Pattern

Reject interfaces such as:

```text
ServicePort {
  execute<T>(action: string, payload: unknown): Promise<T>
}
```

They hide dependency meaning and destroy type safety.

# God Port Anti-Pattern

Reject:

```text
BrowserCapabilitiesPort
```

with unrelated clipboard, notifications, geolocation, files, storage, and navigation methods unless a deliberate facade is accepted.

Prefer capability-specific ports.

# Test Doubles

Port design should make focused tests easy.

Potential doubles:

```text
IN_MEMORY_IMPLEMENTATION
FAKE
STUB
SPY
VIRTUAL_CLOCK
CONTROLLED_SUBSCRIPTION_SOURCE
```

Use Case tests SHOULD prefer InMemory repository implementations.

True external-service ports may use stubs/spies/fakes.

Do not design ports solely around mocking-framework convenience.

# InMemory Repositories

An InMemory repository should preserve meaningful repository semantics:

- save;
- find;
- removal;
- identity;
- optional uniqueness;
- ordering when contract defines it.

It is not merely:

```text
jest.fn()
```

Use it to test Application behavior realistically.

# Contract Tests

When multiple adapters implement one important port, consider shared contract tests.

Examples:

```text
HttpDraftRepository
IndexedDbDraftRepository
InMemoryDraftRepository
```

Shared contract tests may verify:

- save/find semantics;
- not found;
- ordering;
- error-independent behavior.

Only use when multiple implementations genuinely need semantic equivalence.

# Adapter-Specific Behavior

Do not put adapter-only behavior into port contract just so one implementation can expose it.

Example:

```text
getIndexedDbVersion()
```

does not belong in `DraftRepository`.

Keep diagnostics/maintenance at Infrastructure boundary.

# Versioning

Public package ports should evolve carefully.

Prefer additive compatible changes when possible.

A Request object may help evolve input.

Do not add optional flags with unclear interactions just to preserve one interface forever.

# Exceptions

A provider-specific adapter may need a narrower custom boundary.

Record deviations explicitly.

Do not weaken every port to accommodate one awkward provider.

# Port Design Decision Matrix

For each capability answer:

```text
1. Is an inward abstraction needed?
2. Who owns it: Domain or Application?
3. What product capability does it express?
4. What inputs/outputs are stable?
5. What does not-found mean?
6. Which failures need distinction?
7. Does cancellation matter?
8. Are cache/offline semantics visible?
9. Is it one-shot or subscription-based?
10. What security/privacy constraints exist?
11. Which test double is appropriate?
```

# Final Decision

Use:

```text
FRONTEND_PORT_READY
FRONTEND_PORT_READY_WITH_CONDITIONS
NO_PORT_REQUIRED
RETURN_TO_USE_CASE_OR_DOMAIN_DESIGN
PORT_OWNER_REQUIRED
FAILURE_CONTRACT_REQUIRED
CANCELLATION_CONTRACT_REQUIRED
CACHE_OR_SYNC_CONTRACT_REQUIRED
SECURITY_OR_PRIVACY_DECISION_REQUIRED
BLOCKED
```

## Output

Use `assets/frontend-port-design-record.md`.

## Completion Criteria

- [ ] Port justification is explicit.
- [ ] `NO_PORT_REQUIRED` is accepted as valid.
- [ ] Domain vs Application ownership is explicit.
- [ ] Name and methods use product/capability language.
- [ ] Interface is narrow and purpose-specific.
- [ ] Repository methods model persistence/collection semantics rather than endpoints.
- [ ] External-service ports model actions/capabilities rather than transport.
- [ ] Browser/provider APIs do not leak inward.
- [ ] Inputs/outputs use stable Domain/Application-safe types.
- [ ] Not-found semantics are explicit.
- [ ] Failure categories preserve only distinctions callers need.
- [ ] Provider/HTTP/browser errors are translated outward.
- [ ] Cancellation semantics are explicit when requests can become obsolete.
- [ ] Race-policy ownership is explicit.
- [ ] Browser storage ports hide localStorage/IndexedDB details.
- [ ] Analytics ports constrain semantic events and privacy-sensitive payloads.
- [ ] Clipboard/files/geolocation/notifications expose only required capabilities.
- [ ] Clock/ID/connectivity ports exist only when Application behavior needs them.
- [ ] Cache semantics remain Infrastructure detail unless product behavior makes freshness/offline state visible.
- [ ] Sync/subscription lifecycle and error semantics are explicit where applicable.
- [ ] Server/client runtime constraints are explicit.
- [ ] Security/privacy constraints are explicit.
- [ ] Test-double strategy is defined without mock-driven API design.
- [ ] No generic ServicePort, god capability port, endpoint mirror, provider SDK, or speculative abstraction is introduced.
- [ ] Final port decision is explicit.
