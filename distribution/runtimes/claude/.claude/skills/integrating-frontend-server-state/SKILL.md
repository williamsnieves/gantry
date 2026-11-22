---
name: integrating-frontend-server-state
description: Integrates the project's already-selected server-state strategy such as React Query, SWR, RTK Query, Apollo, Relay, or framework data loaders. Use to design query identities, caching, deduplication, invalidation, mutations, optimistic updates and rollback, dependent queries, prefetch, hydration, retry/error boundaries, and adapter integration while preserving Application/Domain/Infrastructure boundaries. Do not choose a new server-state library, rebuild its cache/status machine inside custom hooks, leak query-library types into Application or Domain, make query keys encode UI accidents, or bypass accepted repositories/Use Cases when the selected architecture requires them.
---

# Integrating Frontend Server State

## Purpose

Apply the project's selected server-state strategy correctly and proportionately.

This skill answers:

```text
How should remote server state be integrated
without breaking the application's architecture?
```

It covers:

```text
query identity
cache ownership
deduplication
freshness
invalidation
mutations
optimistic updates
rollback
dependent queries
prefetch
hydration
retry
error boundaries
adapter integration
```

The skill does not choose a new library.

The selected profile may be:

```text
React Query
SWR
RTK Query
Apollo
Relay
framework data loaders/actions
```

## Governing Standard

Remote server state SHOULD use the project's selected server-state strategy when caching, deduplication, invalidation, retries, or synchronization are required.

Do not rebuild a server-state library inside a custom hook.

Application and adapter boundaries MUST remain intact when the selected architecture requires them.

Server-state lifecycle is not automatically Domain or Application state.

## Use When

- Remote state needs caching or deduplication.
- Mutations need cache reconciliation.
- Invalidations are stale or too broad.
- Multiple components request the same resource.
- Dependent queries exist.
- Route/page prefetch is required.
- SSR/hydration uses a query/cache layer.
- Optimistic updates need rollback semantics.
- Existing hooks duplicate server-state lifecycle manually.
- A repository/Use Case must integrate with React Query/SWR/etc.
- Retry ownership is unclear.
- Error-boundary integration needs design.
- Query keys/identities are unstable or UI-coupled.

## Do Not Use When

- The project has not selected a server-state strategy.
- The task is to choose between React Query/SWR/Apollo/etc.
- Remote state is simple enough that the project intentionally uses a direct loader/adapter without cache.
- The task is custom-hook state modeling only.
- The task is repository-adapter implementation.
- The task is HTTP-client implementation.
- The task is Domain/Application orchestration design.
- A framework loader already owns the full lifecycle and no extra cache/query behavior is required.

## Inputs

- Selected server-state profile/library.
- Architecture profile.
- Accepted user behavior.
- Repository/Use Case contracts.
- Adapter composition.
- Async-state model.
- Query/read operations.
- Mutation operations.
- Resource identities.
- Cache/freshness requirements.
- Invalidation requirements.
- Optimistic behavior.
- Retry policy.
- Cancellation policy.
- Route/prefetch requirements.
- SSR/hydration requirements.
- Error-boundary strategy.
- Existing query/cache conventions.
- Test strategy.
- Repository-local `AGENTS.md`.

## Outputs

- Server-state integration strategy.
- Query-key/resource-identity design.
- Cache ownership and freshness policy.
- Deduplication policy.
- Invalidation matrix.
- Mutation integration.
- Optimistic update/rollback strategy.
- Dependent-query strategy.
- Prefetch/hydration strategy.
- Retry/error-boundary ownership.
- Adapter/Use Case integration decision.
- Server-state test matrix.
- Frontend server-state integration record.

## Core Workflow

```text
confirm selected profile
→ confirm architecture boundaries
→ identify remote resources and commands
→ define stable resource identity
→ define cache/freshness semantics
→ define invalidation
→ define mutations and optimistic behavior
→ define dependencies/prefetch/hydration
→ define retry/errors
→ verify adapter integration
→ test cache lifecycle
```

## Readiness Gate

Use one:

```text
READY_TO_INTEGRATE_FRONTEND_SERVER_STATE
READY_WITH_CONDITIONS
SERVER_STATE_LIBRARY_REQUIRED
ARCHITECTURE_BOUNDARY_REQUIRED
RESOURCE_IDENTITY_REQUIRED
INVALIDATION_POLICY_REQUIRED
OPTIMISTIC_POLICY_REQUIRED
ROUTE_PREFETCH_POLICY_REQUIRED
SSR_HYDRATION_POLICY_REQUIRED
BLOCKED
```

Do not select a library automatically when the project has not chosen one.

# Profile Confirmation

Record the selected profile:

```text
REACT_QUERY
SWR
RTK_QUERY
APOLLO
RELAY
FRAMEWORK_LOADERS
CUSTOM_APPROVED_SERVER_STATE
```

The skill should adapt terminology to the selected profile.

Examples:

```text
React Query
→ queryKey / staleTime / invalidateQueries / mutation

SWR
→ key / dedupingInterval / mutate

RTK Query
→ endpoint cache key / tags / invalidatesTags

Apollo
→ normalized cache / field policy / refetchQueries/cache.modify

Relay
→ fragments / records / connections / updater

Framework loaders
→ route key / loader cache / revalidation / action
```

Do not pretend all libraries have identical semantics.

# Architecture Preservation

First classify the integration path:

```text
PRESENTATION_DIRECT_TO_SERVER_STATE
SERVER_STATE_TO_USE_CASE
SERVER_STATE_TO_REPOSITORY
SERVER_STATE_TO_ADAPTER
FRAMEWORK_LOADER_TO_APPLICATION
ARCHITECTURE_REQUIRES_DECISION
```

## Profile A

A lightweight feature may legitimately use:

```text
component/hook
→ selected server-state fetcher
→ isolated Infrastructure adapter
```

when that is the accepted architecture.

Do not force Use Cases or repositories merely because a query library exists.

## Profile B/C

When Application/ports/repositories are part of the selected architecture, preserve them.

Preferred:

```text
queryFn
→ Use Case / repository port
→ adapter
→ HTTP client
```

not:

```text
queryFn
→ fetch("/api/...")
```

if direct transport bypasses accepted boundaries.

# Query Function Responsibility

A query function may:

- invoke a Use Case;
- invoke a repository/semantic adapter;
- return Application-safe data;
- propagate stable errors;
- honor cancellation.

It should not:

- implement Domain rules;
- map raw provider payloads when adapter owns mapping;
- construct HTTP headers;
- decide UI rendering;
- mutate unrelated cache entries secretly.

# Query Identity

A query key/resource identity should represent:

```text
the remote semantic resource
+
all inputs that materially change that resource
```

Good conceptual identity:

```text
profile + userId
orders + filters
subscription + subscriptionId
recommendations + locale + segment
```

Weak identity:

```text
component name
screen tab index
random object
render timestamp
```

The identity should survive component refactors.

# Query Key Stability

A query key MUST be deterministic.

Avoid:

```text
new Date()
Math.random()
unstable object identity
functions
DOM nodes
React elements
```

Use serialization-safe stable values.

When the library hashes structured keys safely, object filters may be valid if their semantic content is stable.

Follow library conventions.

# Query Key Completeness

Include every input that changes the fetched resource.

Example:

```text
["orders", { customerId, status, cursor }]
```

If `status` changes the response but is absent from the key, stale cross-query data may be reused incorrectly.

Do not include values that only change presentation.

Example:

```text
selectedAccordion
```

does not belong unless it changes the remote request.

# Query Key Factory

A query-key factory may be useful when:

- multiple features reuse the same resource;
- invalidation needs stable partial matching;
- package boundaries need consistency.

Do not introduce a global key-factory framework for one query.

Feature-local key helpers are often enough.

# Resource Identity vs Transport Identity

Prefer semantic identity:

```text
subscription(subscriptionId)
```

over:

```text
GET /v2/subscriptions/:id
```

Query identity should not encode URL/version unless transport version materially changes semantics.

# Cache Ownership

The selected server-state library owns remote cache lifecycle.

Do not copy remote data into:

```text
useState
Context
Redux
Zustand
another query cache
```

unless there is a clear transformation/ownership boundary.

A different local draft is not a duplicate if it intentionally represents editable local state.

# Cache as Infrastructure/Presentation Mechanism

Cache metadata usually remains outside Domain/Application.

Examples:

```text
staleTime
dedupingInterval
queryKey
cacheTime/gcTime
tags
normalized-record IDs
```

Do not put these into Use Case inputs or Domain entities.

# Freshness

Distinguish:

```text
library cache freshness
product-visible freshness
```

A cache can be stale for revalidation while still perfectly acceptable to display.

Use product-visible stale state only when user behavior requires it.

# Freshness Policy

Possible categories:

```text
ALWAYS_REVALIDATE
SHORT_LIVED
SESSION_STABLE
IMMUTABLE
EVENT_INVALIDATED
USER_INVALIDATED
ROUTE_INVALIDATED
OFFLINE_STALE_ALLOWED
```

Map these to the selected library's settings.

Do not start from arbitrary `staleTime` numbers without behavior or repository conventions.

# Deduplication

Server-state libraries should prevent duplicate requests for the same in-flight semantic resource when their profile supports it.

Evaluate:

- identical resource identity;
- simultaneous component mounts;
- route + component prefetch/fetch;
- dependent duplicate reads.

Do not solve duplicate requests with ad hoc module promises before checking library support.

# Duplicate Requests Evaluation

Given:

```text
Header → loadProfile(userId)
Sidebar → loadProfile(userId)
```

both should share the same semantic key/cache entry when they need the same data.

Do not create separate keys:

```text
["header-profile", userId]
["sidebar-profile", userId]
```

unless the data semantics truly differ.

# Request Scope

Do not over-deduplicate semantically different data.

Example:

```text
profile(userId, locale)
```

may differ if the backend localizes content.

Then locale belongs in identity.

# Invalidation

Invalidation should follow data dependencies.

Create an invalidation matrix:

| Mutation | Direct resource | Related lists | Aggregates | Prefetched routes |
|---|---|---|---|---|

Avoid:

```text
invalidate everything
```

unless the application is tiny and cost is acceptable.

Also avoid hyper-specific invalidation that leaves derived caches stale.

# Stale Invalidation

A common defect:

```text
mutation succeeds
→ detail cache updated
→ list cache remains stale
```

or:

```text
list invalidated
→ aggregate count/dashboard remains stale
```

Model all affected semantic resources.

# Invalidation Strategies

Use one or combine intentionally:

```text
INVALIDATE_AND_REFETCH
DIRECT_CACHE_UPDATE
SET_FROM_MUTATION_RESULT
OPTIMISTIC_PATCH_THEN_RECONCILE
TAG_INVALIDATION
NORMALIZED_CACHE_UPDATE
ROUTE_REVALIDATION
```

The selected library determines mechanisms.

# Invalidation Timing

Define:

```text
on mutation start
on success
on settled
on background event
```

Do not invalidate blindly both before and after every mutation.

# Mutation Result Reuse

If a successful mutation returns authoritative updated data, prefer updating cache from that result when safe rather than immediately refetching the same data.

Example:

```text
saveProfile
→ returns updated ProfileDTO
→ update profile cache
```

Still invalidate related lists/aggregates if their derived data may have changed.

# Mutations

A server-state mutation integrates a semantic command.

Preferred:

```text
mutationFn
→ Use Case / repository / semantic adapter
```

Do not make the mutation function the new Application layer.

It should not accumulate business branching that belongs in Use Case/Domain.

# Query vs Mutation

Use queries for remote reads.

Use mutations/actions for commands that change authoritative server state.

Do not model:

```text
POST search
```

as a mutation merely because HTTP method is POST if semantically it is a cacheable read.

Server-state semantics follow product intent, not HTTP verb.

# Optimistic Updates

Only use optimistic updates when accepted UX justifies them.

Define:

```text
optimistic apply
→ mutation
→ authoritative success reconcile
OR
→ rollback
```

Need:

- previous cache snapshot;
- affected resources;
- concurrency policy;
- rollback condition;
- authoritative merge behavior.

# Optimistic Ownership

One owner only.

Possible:

```text
SERVER_STATE_LIBRARY
DOMAIN
APPLICATION
LOCAL_WORKFLOW
```

When server-state cache owns the optimistic resource, do not duplicate an `optimisticItem` in local state.

# Optimistic Preconditions

Optimistic update is strongest when:

- operation is likely to succeed;
- reversal is safe;
- client can predict resulting state;
- server response can reconcile differences.

Use caution for:

- payments;
- irreversible actions;
- complex authorization;
- stock/inventory;
- server-calculated final price.

Do not optimistic-update high-risk authoritative outcomes casually.

# Optimistic Snapshot

Snapshot only what rollback needs.

Do not clone the entire application cache unnecessarily.

For libraries with transaction/update helpers, follow profile conventions.

# Optimistic Rollback

Rollback must restore:

- direct resource;
- affected list;
- aggregate counters if patched;
- derived semantic caches that were optimistically changed.

Do not rollback only the visible card while leaving list/detail caches inconsistent.

# Concurrent Optimistic Mutations

Define:

```text
SERIALIZE
KEYED_CONCURRENT
LATEST_WINS
QUEUE
LIBRARY_NATIVE_POLICY
```

Avoid stale snapshot rollback that overwrites a later successful optimistic mutation.

# Mutation Error

Mutation errors should remain semantic.

Do not expose raw query-library wrapper errors as the feature public API if Application has stable error semantics.

# Retry Ownership

Choose one primary retry owner.

Possible:

```text
SERVER_STATE_LIBRARY
HTTP_CLIENT
ADAPTER
USE_CASE
NO_RETRY
```

Avoid retry stacking.

Example bad:

```text
HTTP client retries 3
+
React Query retries 3
```

which can multiply requests unexpectedly.

# Query Retry

Reads may retry according to accepted policy.

Do not retry:

- forbidden;
- invalid contract;
- cancellation;
- deterministic not-found when absence is final;

unless policy explicitly says otherwise.

# Mutation Retry

Mutations require idempotency awareness.

Do not auto-retry non-idempotent commands such as payment unless backend idempotency supports it.

# Cancellation

Query/mutation functions should honor cancellation when the library supports it.

Examples:

```text
React Query queryFn context.signal
SWR fetcher + AbortController integration
framework loader request.signal
```

Propagate:

```text
server-state
→ Use Case/repository if supported
→ adapter
→ HTTP client
```

Do not swallow cancellation into generic error state.

# Stale Response Protection

The selected server-state library should usually own key-based request lifecycle.

Do not add manual request counters unless the library/architecture genuinely needs them.

# Dependent Queries

Use dependent queries when resource B requires result A.

Example:

```text
user
→ organizationId
→ organization settings
```

Avoid executing B with invalid placeholder IDs.

Use the selected profile's enabling/conditional mechanism.

# Dependent Query Identity

The dependent key must include the resolved dependency.

Example:

```text
organizationSettings(organizationId)
```

not:

```text
organizationSettings()
```

# Dependent Query Waterfalls

Dependent queries can create latency waterfalls.

Ask whether:

- backend can aggregate;
- route loader can parallelize;
- parent data already contains required identity;
- prefetch can happen earlier.

Do not flatten true dependency just to parallelize invalid requests.

# Parallel Queries

Independent resources should load in parallel where practical.

Do not serialize unrelated queries in Effects.

# Conditional Queries

A query should be disabled/not created when required identity is absent.

Distinguish:

```text
not ready to query
```

from:

```text
query returned no data
```

Do not use `""`/`0` fake IDs to keep hooks unconditional if the library provides safe conditional semantics.

# Route Prefetch

Prefetch should use the same semantic query identity as the destination consumer.

Flow:

```text
route intent
→ prefetch semantic resource
→ destination uses same cache key
```

If prefetch uses a different key/function, duplicate requests can occur.

# Prefetch Timing

Potential triggers:

```text
link hover/focus
route transition intent
server route render
known next step
viewport proximity
```

Use accepted framework/library capability.

Do not prefetch every route/data resource without cost analysis.

# Prefetch Freshness

Prefetched data needs a freshness policy.

Avoid:

```text
prefetch
→ immediately refetch on route mount
```

unless policy intentionally wants validation.

# Route Loader Integration

Framework loaders/actions may themselves be the selected server-state strategy.

If combining loaders with a query cache:

- establish one source of truth;
- seed/hydrate the cache intentionally;
- avoid loader fetch + component query duplicate network calls.

Do not make loader and query cache independently fetch the same resource accidentally.

# SSR

For SSR, define:

```text
server fetch
cache population
serialization/dehydration
client hydration
post-hydration freshness
```

Do not create per-user cache leakage through module-level server singletons.

# Query Client Lifecycle

Server:

```text
request-scoped query/cache client
```

unless framework/library explicitly guarantees safe isolation.

Client:

```text
stable app/client instance
```

according to library conventions.

Do not create a new cache client on every render.

# Hydration

Hydrated data should not cause unnecessary loading flicker.

Ensure cache identity matches server and client.

Do not serialize:

- raw errors with unsafe causes;
- functions;
- provider SDK objects;
- server secrets.

# Application/Adapter Integration

When architecture requires repositories/Use Cases:

```text
queryFn
→ Application boundary
```

The query library should not directly import Infrastructure implementations from arbitrary components.

Composition provides accepted dependencies.

Possible patterns:

```text
hook receives Use Case
hook uses query library
queryFn calls Use Case
```

or:

```text
feature query options factory receives semantic dependency
```

Keep dependency creation at outer boundary.

# Query Options Factories

A feature-local query-options factory may improve reuse:

```text
profileQuery(userId, loadProfile)
```

when:

- prefetch and component query must share exact identity/function;
- route/server/client integration needs reuse.

Do not create a universal abstraction layer over the selected library.

# Adapter Integration Evaluation

Verify:

```text
server-state layer
→ accepted Use Case/repository
→ adapter
```

and no direct provider mapping/fetch appears in component/query config when architecture forbids it.

# Profile A Direct Adapter

For lightweight architecture, accepted direct integration may be:

```text
queryFn
→ feature Infrastructure adapter
```

Do not label it wrong solely because no Use Case exists.

# Error Boundaries

Decide what failures belong to:

```text
local query error rendering
route/framework error boundary
React Error Boundary
global session boundary
```

Operational remote failures usually belong to query/UI handling, not generic React render error boundaries.

Framework/loaders may intentionally route errors to route error boundaries.

# Error Boundary Escalation

Escalate when:

- entire route cannot function;
- auth/session boundary must take over;
- contract corruption makes local recovery impossible;
- framework convention owns loader errors.

Keep recoverable feature errors local when appropriate.

# Suspense

If selected profile uses Suspense:

- loading may move to Suspense boundary;
- errors may move to Error Boundary;
- cache still owns remote data.

Do not simultaneously maintain duplicate local `isLoading` state.

# Empty vs Error vs Not Found

The query result contract should preserve distinctions.

Example repository:

```text
findById
→ undefined = not found
```

Then query success with `undefined` can map to product not-found/empty semantics as designed.

Do not turn 404, forbidden, network failure, and empty list into one state.

# Pagination

Query identity should include page/cursor/filter semantics.

For infinite queries:

- preserve loaded pages while loading next;
- distinguish initial load from next-page fetch;
- define page invalidation;
- define mutation impact on pages.

Do not invalidate every page blindly if direct update is safe, but do not leave stale pages.

# Search

Search keys should include semantic filters/query.

Use debouncing in Presentation/hook as appropriate.

Do not put debounce timer identity in query key.

Cancellation/latest-wins should align with changing keys.

# Polling

Polling is a server-state policy.

Use only when accepted behavior requires periodic refresh.

Define:

- interval;
- visibility/background behavior;
- focus behavior;
- cancellation;
- stop condition.

Do not poll just because the library supports it.

# Focus/Reconnect Revalidation

Libraries may refetch on:

```text
window focus
network reconnect
mount
```

Use accepted defaults/policy.

Do not disable globally because one feature dislikes it.

Feature-specific deviations should be explicit.

# Cache Eviction

Cache lifetime/gc policy is Infrastructure behavior.

Do not expose it to Application unless product semantics depend on offline persistence/freshness.

# Normalized Caches

Apollo/Relay may normalize entities.

Do not additionally duplicate normalized server entities into a second ad hoc query cache.

Use the selected profile's normalization/update mechanisms.

# RTK Query Tags

Tags should model semantic invalidation relationships.

Do not use one global tag for everything.

Do not expose tags outside server-state integration.

# Apollo Field Policies

Field policies/cache IDs are Infrastructure/server-state configuration.

Keep product semantics stable above them.

# Relay Fragments

Components may consume fragment data according to Relay architecture.

Do not force generic repository DTO mapping if the project explicitly selected Relay's data architecture as the accepted profile.

Still keep provider/business rules separated according to project boundaries.

# Framework Loaders

Framework loaders/actions may fully own:

- fetch lifecycle;
- route cache;
- revalidation;
- error boundary;
- prefetch.

Do not layer React Query/SWR on top automatically.

Only combine when there is accepted value, such as cross-route client cache reuse.

# Local UI State

Server-state tools should not own:

- modal open;
- selected tab;
- unsaved input;
- hover;
- local draft interaction;
- purely visual state.

Keep local UI state local.

# Editable Drafts

When a user edits server data:

```text
server resource
→ initialize local/form/domain draft
```

The draft becomes a different owner.

Do not keep continuously syncing every keystroke back into query cache unless product semantics require it.

On save:

```text
mutation
→ authoritative result
→ reconcile/invalidate server cache
```

# Derived Data

Pure UI derivation from query data should be computed, not stored back into cache unless it is a stable semantic normalized resource.

Use library selectors where appropriate.

Do not mutate cached raw data for display formatting.

# Cache Data Shape

Cache should usually store stable Application/adapter output, not:

- JSX;
- view labels;
- localized dates;
- icons;
- component props.

Presentation derives view data.

# Query Library Types

Avoid leaking:

```text
UseQueryResult
SWRResponse
ApolloQueryResult
RTK Query endpoint types
Relay environment objects
```

into Domain/Application public contracts.

They may exist in Presentation/server-state integration layers.

# Custom Hook Integration

A custom hook may wrap server-state semantics:

```text
useProfile(...)
```

It may expose a stable feature-facing API.

Do not recreate:

```text
cache
retry scheduler
dedup map
invalidation registry
```

inside the hook.

# Thin Wrapper

A wrapper is justified when it adds:

- semantic command names;
- dependency injection;
- Application result translation;
- feature-specific derived state;
- test seam.

It is overmodeled when it simply renames every library field one-to-one.

# Duplicate Requests Audit

Check:

- same resource with different keys;
- route loader + query fetch;
- prefetch + mount query mismatch;
- nested components fetching same semantic resource;
- StrictMode/dev behavior mistaken for production duplication;
- retry mistaken for duplicate request;
- polling/focus refetch mistaken for accidental duplication.

Diagnose source before “fixing” it.

# Dev/StrictMode Requests

React development behavior may invoke code differently depending on framework/library.

Do not disable correctness mechanisms solely to hide development duplicates.

Use the library's intended cache/dedup patterns.

# Stale Invalidation Audit

After each mutation, inspect:

- detail;
- lists;
- counts;
- dashboards;
- parent resources;
- route prefetched data;
- normalized entities;
- offline copies if applicable.

Do not assume invalidating the direct resource is enough.

# Optimistic Rollback Audit

Test:

```text
snapshot
optimistic patch
mutation failure
rollback
related-cache consistency
later concurrent mutation
```

No stale rollback over a newer success.

# Dependent Query Audit

Verify:

- dependency absence does not call endpoint;
- resolved dependency enters key;
- error of parent does not produce bogus child request;
- dependency change invalidates/switches child resource;
- avoid avoidable waterfalls.

# Route Prefetch Audit

Verify:

- prefetch and destination share identity;
- prefetched data is reused;
- route does not immediately duplicate fetch unexpectedly;
- cancellation/abandonment is safe;
- cost is proportionate.

# Adapter Integration Audit

Verify:

- no raw fetch in component when architecture forbids;
- queryFn uses accepted semantic dependency;
- provider payload mapping stays adapter-owned;
- cancellation propagates;
- stable errors remain distinguishable.

# Testing Strategy

Test server-state integration behavior, not library internals.

Possible boundaries:

```text
hook/component integration
query client/cache harness
route integration
adapter fake/InMemory dependency
```

Do not assert undocumented internal cache structures.

# Test Isolation

Each test should get isolated cache/query state unless the test intentionally covers shared cache behavior.

Reset:

- cache/client;
- timers;
- subscriptions;
- request mocks;
- auth/context.

Avoid test-order dependence.

# Duplicate Request Test

Render/mount two consumers of the same semantic resource.

Assert:

```text
one accepted underlying semantic load
```

according to selected library dedup behavior.

Do not assert internal observer counts.

# Stale Invalidation Test

Seed:

```text
detail + list + aggregate
```

perform mutation, then verify affected resources update/refetch according to policy.

# Optimistic Rollback Test

Use controlled mutation.

Assert:

```text
optimistic UI/cache
→ reject mutation
→ previous semantic data restored
```

No arbitrary sleep.

# Dependent Query Test

Parent result controls child availability.

Assert child does not execute before dependency exists.

# Route Prefetch Test

Prefetch resource, navigate/render destination, assert prefetched cache is consumed according to freshness policy.

# Adapter Integration Test

Use an InMemory/fake semantic dependency or adapter mock server.

Assert server-state configuration invokes the correct architecture boundary and exposes stable results/errors.

# Library Upgrade Resilience

Tests should avoid asserting library-private state.

Prefer semantic behavior:

```text
request count
visible/loading behavior
cache reuse
mutation reconciliation
```

# Performance

Server-state integration can affect:

- request count;
- waterfalls;
- bundle size;
- cache memory;
- rerenders.

Do not optimize with complex selectors or normalization without evidence.

Fix duplicate requests and waterfalls based on observed behavior.

# Security / Privacy

Do not put secrets or sensitive user data into globally persisted query keys or devtools-visible cache metadata unnecessarily.

Be cautious with:

- auth tokens in keys;
- PII in query keys;
- persisted caches;
- SSR dehydrated state.

Query keys should identify resources without embedding secrets.

# Auth Changes

On login/logout/user switch:

- invalidate/reset user-specific cache as required;
- avoid showing previous user's cached data;
- ensure cache scope matches auth scope.

This can be a security issue, not just stale state.

# Multi-Tenant State

Tenant/org identity must be included in resource identity when it changes data.

Example:

```text
["subscriptions", organizationId, subscriptionId]
```

if subscription IDs are not globally unique or access is tenant-scoped.

Do not rely on implicit current tenant if cache can survive tenant switch.

# Persistence

Persisted query caches require explicit policy.

Consider:

- user/tenant scope;
- version;
- TTL/freshness;
- sensitive data;
- logout clearing;
- migration.

Do not enable cache persistence merely for performance.

# Error Reset

When Error Boundaries/Suspense are used, define how retry/reset re-enters query lifecycle.

Do not leave an Error Boundary permanently latched after successful retry.

# Server Events

WebSocket/SSE/subscription updates may update/invalidate query cache.

Define whether event:

```text
patches exact resource
invalidates resource
invalidates list
```

Avoid double refresh if both event handler and mutation already reconcile the same cache.

# Offline

If server-state library supports offline/network modes, use them only if selected product behavior requires it.

Offline Domain/persistence workflows may remain separate from ordinary server-state cache.

Do not assume query cache is an offline database.

# Implementation Decision Record

For each resource record:

- semantic identity;
- key/tag/record strategy;
- loader/query function owner;
- cache/freshness;
- invalidation relationships;
- retry owner;
- cancellation;
- prefetch;
- SSR/hydration;
- mutation behavior;
- optimistic behavior;
- error boundary;
- security scope.

# Final Decision

Use:

```text
FRONTEND_SERVER_STATE_INTEGRATION_READY
FRONTEND_SERVER_STATE_INTEGRATION_READY_WITH_CONDITIONS
SERVER_STATE_LIBRARY_REQUIRED
RETURN_TO_ASYNC_STATE_OR_ADAPTER_DESIGN
RESOURCE_IDENTITY_REQUIRED
INVALIDATION_POLICY_REQUIRED
OPTIMISTIC_POLICY_REQUIRED
SSR_HYDRATION_POLICY_REQUIRED
SECURITY_SCOPE_REQUIRED
BLOCKED
```

## Output

Use `assets/frontend-server-state-integration-record.md`.

## Completion Criteria

- [ ] Selected server-state profile is explicit and not changed by this skill.
- [ ] Architecture profile and accepted integration boundary are preserved.
- [ ] Query/resource identities are semantic, deterministic, and complete.
- [ ] Presentation-only state is excluded from keys.
- [ ] Cache ownership remains with selected server-state strategy.
- [ ] Remote cache is not duplicated into local state/store.
- [ ] Freshness policy derives from behavior rather than arbitrary numbers.
- [ ] Duplicate-request behavior is understood and uses profile-native deduplication.
- [ ] Invalidation relationships include detail, list, aggregates, and prefetched/normalized resources as applicable.
- [ ] Mutation result reuse versus refetch is intentional.
- [ ] Optimistic updates have one owner and explicit rollback/reconciliation semantics.
- [ ] Concurrent optimistic behavior is safe.
- [ ] Retry ownership is singular and idempotency-aware.
- [ ] Cancellation propagates through the accepted architecture.
- [ ] Dependent queries wait for real dependencies and avoid bogus requests.
- [ ] Avoidable waterfalls are considered.
- [ ] Route prefetch uses the same semantic resource identity as the destination.
- [ ] Loader/query cache duplication is avoided.
- [ ] SSR query/cache lifecycle is request-safe.
- [ ] Hydration does not leak secrets or first-user state.
- [ ] Error-boundary ownership is explicit.
- [ ] Adapter/Use Case integration preserves provider mapping and stable errors.
- [ ] Query-library types do not leak into Domain/Application contracts.
- [ ] Test caches are isolated.
- [ ] Roadmap evaluations are covered: duplicate requests, stale invalidation, optimistic rollback, dependent queries, route prefetch, adapter integration.
- [ ] No new server-state library, cache persistence layer, query abstraction framework, or architecture policy is introduced without approval.
- [ ] Final integration status is explicit.

## References

- Read `references/profile-and-architecture-preservation.md` first.
- Read `references/query-identity-cache-freshness-and-deduplication.md`.
- Read `references/invalidation-mutations-and-optimistic-updates.md`.
- Read `references/dependent-queries-prefetch-ssr-and-hydration.md`.
- Read `references/retries-errors-cancellation-and-security-scope.md`.
- Read `references/adapter-integration-testing-and-overmodeling.md`.
- Read `references/frontend-server-state-integration-audit.md` before completion.
