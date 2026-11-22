---
name: testing-frontend-user-journeys
description: Portable engineering capability `testing-frontend-user-journeys`. Use
  when the harness or a specialist agent explicitly requires this named capability.
---
# Testing Frontend User Journeys

## Purpose

Implement end-to-end tests for critical user journeys that require confidence across real application boundaries.

Core principle:

```text
E2E
→ critical integration confidence

NOT
→ default place for every behavior
```

The preferred testing progression remains:

```text
Domain
→ Application Use Case
→ adapter integration
→ hook/component behavior
→ route/E2E confidence
```

E2E is the outer confidence layer, not a replacement for inner tests.

## Governing Standard

E2E tests SHOULD cover critical user journeys, not every local branch.

They MUST avoid replacing lower-level tests with a slow all-E2E strategy.

Good candidates include:

- authentication-dependent critical flow;
- revenue or entitlement path;
- route-to-route workflow;
- browser integration;
- server/client hydration;
- deployment configuration;
- real backend contract;
- one representative accessibility or retry path where browser behavior matters.

E2E should cover:

- essential success;
- one or few critical failures/recovery paths;
- integration risks not proved below.

Do not use E2E for:

- every validation branch;
- every provider error;
- pure business rules;
- every component state;
- every theme variant;
- exhaustive edge cases.

## Use When

- A critical journey spans route, browser, and backend boundaries.
- Authentication/session integration must be verified.
- Revenue, entitlement, booking, checkout, subscription, or account-critical flow needs deployment confidence.
- A route-to-route workflow can fail despite component tests passing.
- Browser-only behavior is central.
- Server/client hydration or routing configuration is risky.
- Real backend/staging contract must be proven selectively.
- A previously observed production integration defect needs outer-boundary regression coverage.
- One representative failure/recovery path is business-critical.
- The test strategy explicitly classifies the journey as `E2E_REQUIRED`.

## Do Not Use When

- A pure Domain test proves the behavior.
- A Use Case test proves orchestration.
- An adapter test proves protocol/provider mapping.
- A hook/component test proves local UI behavior.
- A visual test proves appearance.
- The only reason is “more coverage.”
- The scenario is every validation message.
- The scenario is every HTTP/provider error.
- The journey depends on production data.
- The environment cannot isolate state safely.
- The test requires brittle CSS selectors or sleeps to work.
- The flow is not critical and cheaper route/component coverage is sufficient.

## Inputs

- Accepted user journey.
- Business/integration risk.
- Test strategy decision.
- Environment/staging policy.
- Authentication strategy.
- Data seeding/reset capability.
- Backend contract.
- Browser matrix.
- Routing/deployment model.
- Feature flags.
- Test account policy.
- CI execution policy.
- Failure artifact policy.
- Existing E2E framework, usually Playwright where selected.
- Applicable `AGENTS.md`.

## Outputs

- Journey selection decision.
- Critical-path scope.
- Environment/data-isolation plan.
- Authentication/session setup.
- Deterministic seed/reset strategy.
- User-oriented locators/actions/assertions.
- Recovery-path coverage.
- Retry/timeout policy.
- Failure diagnostics.
- CI placement.
- E2E user-journey testing record.

# Journey Selection

Classify each candidate:

```text
E2E_REQUIRED
ROUTE_INTEGRATION_SUFFICIENT
LOWER_BOUNDARY_SUFFICIENT
MANUAL_PRODUCTION_CHECK_ONLY
NOT_IN_SCOPE
```

Only `E2E_REQUIRED` proceeds to this skill unless the repository explicitly asks for implementation of an already-approved journey.

# Critical Journey Ranking

Rank by:

```text
business impact
user frequency
integration breadth
production incident history
inability to prove lower
browser-specific behavior
deployment/configuration risk
```

A high-risk critical path with broad boundaries is a good E2E candidate.

A rare local input-validation branch usually is not.

# Unique E2E Evidence

Every E2E test should answer:

```text
What integration risk does this prove
that lower-level tests do not?
```

If the answer is unclear, move the test inward or remove it.

# Small E2E Set

Prefer:

```text
few high-value journeys
```

over:

```text
hundreds of branch-level E2E tests
```

A healthy suite may contain many tests for a large product, but each should have a unique integration purpose.

# Journey Shape

A typical critical journey:

```text
known isolated starting state
→ user enters application
→ authenticates or restores session
→ performs critical actions
→ crosses required routes/boundaries
→ observes business-visible outcome
→ environment state verified where appropriate
→ cleanup
```

# User Perspective

Interact as a user would.

Prefer:

```text
getByRole
getByLabel
getByText with stable product copy where appropriate
```

Avoid:

```text
[data-testid]
CSS chains
nth-child
implementation classes
```

unless no stable semantic locator exists and test-id policy explicitly supports them.

# Accessible Locators

Role/name locators improve:

- resilience;
- accessibility alignment;
- readability.

Example:

```ts
page.getByRole("button", { name: "Apply promotion" })
```

Do not couple to DOM structure.

# Test IDs

Use test IDs only when:

- semantics cannot uniquely identify the element;
- the identifier represents stable product intent;
- project policy allows it.

Do not use test IDs for every element.

# Assertions

Assert user-visible or contract-visible outcomes.

Good:

```text
confirmation visible
route changed
entitlement appears
saved record appears on reload
critical button becomes available
error recovery succeeds
```

Avoid:

```text
internal Redux value
hook invocation count
private component state
CSS class
network call count
```

unless network behavior itself is the integration risk and the framework exposes it safely.

# End State Verification

Where useful, verify durable outcome by:

- reload;
- navigating away/back;
- backend test API;
- user-visible listing;
- next route.

Do not read private DB tables from E2E unless accepted test infrastructure provides a stable test API and that check adds unique confidence.

# Environment Selection

Use the environment defined by project policy:

```text
local full stack
ephemeral preview
integration
staging
controlled sandbox
```

Do not point automated destructive journeys at production unless explicitly approved and designed as safe synthetic monitoring.

# Production Smoke

Production smoke is a separate policy.

If accepted, it should be:

- non-destructive or isolated;
- minimal;
- synthetic;
- privacy-safe;
- observable;
- rollback-aware.

Do not reuse staging mutation tests blindly in production.

# Test Data Isolation

Every mutable journey should own isolated data.

Strategies:

```text
unique user/resource namespace
test API seed
database fixture in ephemeral env
sandbox account
factory endpoint
per-worker account
transaction/reset mechanism
```

Avoid shared global records.

# Unique Data

Generate deterministic unique identifiers using:

```text
worker id
test id
run id
fixed prefix
```

Do not use uncontrolled randomness if it makes failures hard to reproduce.

# Data Seeding

Prefer fast deterministic setup through:

```text
test API
fixture
database seed command
backend factory
sandbox setup
```

rather than creating all prerequisite state through UI.

E2E should test the journey, not spend 80% of runtime creating setup through unrelated screens.

# UI Setup When Relevant

Use UI setup only if the setup itself is part of the critical journey under test.

Example:

```text
signup flow
```

should create the user through UI because signup is the journey.

A checkout test may seed an existing account/cart through test API if account creation is not the risk.

# Cleanup

Define cleanup for:

```text
users
orders
subscriptions
files
feature flags
sandbox resources
sessions
```

Prefer idempotent cleanup.

Do not depend on successful test completion to avoid permanent garbage if CI can abort.

# Cleanup Strategies

Possible:

```text
afterEach
afterAll
environment TTL
unique ephemeral environment
backend cleanup API
sandbox teardown
```

Use the safest repository-approved method.

# Test Independence

Each test should run independently.

Do not rely on:

```text
test A creates state
test B continues
test C cleans
```

unless the runner explicitly treats the sequence as one serial journey and project policy accepts the trade-off.

Default to isolated tests.

# Serial Journeys

Use serial grouping only where the journey itself must preserve a single stateful sequence and splitting would be artificial.

Serial suites reduce parallelism and increase cascading failures.

Use sparingly.

# Authentication

Authentication setup should prove only the intended risk.

Options:

```text
real login UI
storage state
test session endpoint
identity-provider sandbox
```

# Auth Journey

If login itself is critical:

```text
test real login UI
```

using safe test identity.

# Non-Auth Journey

If the critical journey starts after login:

```text
reuse authenticated storage state
```

or approved test session setup to reduce runtime/flakiness.

Do not repeat login through UI in every E2E test.

# Storage State

When framework supports it, generate authenticated state in a controlled setup project.

Protect:

- cookies;
- tokens;
- test credentials.

Do not commit sensitive state files.

# MFA / SSO

Use test identity-provider mechanisms where available.

Do not bypass security in a way production code cannot represent unless test environment explicitly supports a safe test hook.

# Feature Flags

Set flags deterministically.

Prefer:

- ephemeral-environment config;
- test API;
- seeded user targeting.

Do not rely on whatever flag state happens to be live.

# Time

Control time where product behavior depends on it.

Possible:

```text
backend fixed clock in test env
browser clock APIs
seeded dates far from boundary
```

Do not test “expires in 3 seconds” with real timing unless timer behavior itself is under test.

# Dates / Timezones

Set explicit locale/timezone when date behavior affects the journey.

Do not let CI location change expected results.

# External Providers

Avoid uncontrolled third-party dependencies in the default E2E suite.

Use:

```text
provider sandbox
emulator
stubbed lower boundary
test gateway
```

according to product risk.

# Real Provider E2E

Use real sandbox only when provider integration is itself a critical risk and lower adapter tests are insufficient.

Separate expensive/fragile provider journeys from core fast E2E.

# Network Control

E2E is generally more valuable with real application-backend traffic.

Do not intercept every API and turn the suite into a component test disguised as E2E.

Selective interception may be valid for:

- nondeterministic third parties;
- catastrophic provider failure simulation;
- one recovery path;
- privacy/safety.

Record why.

# Mocking Policy

Avoid mocking internal application layers in E2E.

If you mock:

```text
Use Case
repository
query hook
router
```

you have weakened the end-to-end boundary.

# Browser Matrix

Do not run every journey on every browser automatically.

Use risk-based browser coverage.

Possible:

```text
critical smoke
→ Chromium every PR

representative critical subset
→ Firefox/WebKit scheduled or release gate
```

according to supported browsers.

# Browser-Specific Risk

Run journey on browser where the risk exists:

```text
Safari/WebKit file input
Firefox form behavior
mobile WebKit viewport
```

Do not inflate matrix without product support.

# Responsive Journeys

E2E may cover a small number of critical mobile/desktop paths when layout changes the interaction model.

Do not repeat all component visual states across every viewport.

# Accessibility in E2E

One representative keyboard/browser accessibility path may be useful when route-level behavior matters.

Example:

```text
open checkout dialog
→ keyboard complete critical action
```

Do not replace dedicated accessibility/component tests with E2E.

# Failure / Recovery Paths

E2E should include only one or a few critical failures where integration/recovery matters.

Examples:

```text
payment rejected → user can retry
session expires → re-auth flow
network retry → operation recovers
conflict → user gets recoverable route state
```

Do not implement every backend error code E2E.

# Error Injection

Use an approved test mechanism:

```text
test backend state
sandbox scenario
fault-injection endpoint
provider sandbox behavior
selective route interception
```

Avoid test-only branches in production code.

# Retry Path

A retry E2E should prove:

```text
failure occurs
→ user sees actionable state
→ retry is available
→ second attempt succeeds
→ final state is correct
```

Do not use framework-level test retry as a substitute for product retry.

# Test Runner Retries

Runner retries may handle infrastructure flake.

They must not hide flaky journey design.

Track tests that pass only on retry.

# Timeouts

Use meaningful readiness assertions.

Prefer:

```text
expect(locator).toBeVisible()
expect(page).toHaveURL(...)
wait for semantic state
```

Avoid:

```text
waitForTimeout(2000)
```

# Auto-Wait

Use Playwright-style auto-waiting where selected.

Do not add sleeps before every click.

# Race Conditions

If app asynchronously transitions:

```text
click
→ pending
→ server response
→ route/state update
```

wait for the expected user-visible state, not implementation timing.

# Resilience

A resilient E2E test depends on:

- product semantics;
- stable user interactions;
- deterministic data;
- explicit environment state.

It does not depend on:

- DOM tree shape;
- class names;
- incidental request ordering;
- animation duration.

# Page Objects

Use page objects only when they add stable reusable behavior.

Good:

```text
CheckoutPage.completePayment(...)
```

if several journeys use the same user interaction.

Avoid giant page-object frameworks mirroring the DOM.

# Journey Objects

Prefer business/user-language helpers:

```text
signInAs(...)
createSubscriptionFixture(...)
completeCheckout(...)
```

over:

```text
clickButton1()
fillInput2()
```

# Helper Layers

Separate:

```text
test data setup
page interaction
assertion
environment control
```

without hiding the full journey.

# Readability

A reviewer should understand:

```text
Given
When
Then
```

from the test without opening ten helper files.

# Diagnostics

Preserve useful failure evidence.

Recommended:

```text
trace
screenshot
video where policy permits
console errors
network/request summary where safe
DOM snapshot if framework provides it
test annotations
seed/run identifiers
```

# Playwright Trace

If Playwright is selected, trace-on-first-retry or retain-on-failure can provide strong diagnostics.

Follow repository policy.

Do not record sensitive data unnecessarily.

# Screenshots

Capture failure screenshots automatically where useful.

Do not use screenshot assertions unless visual appearance is the contract; that belongs to visual regression.

# Video

Video can help complex failures but has storage/privacy cost.

Use project policy.

# Console Errors

Unexpected page errors should often fail or annotate the test.

Define allowlist only for known accepted noise.

Do not ignore all console errors.

# Page Errors

Capture uncaught browser errors.

A journey that visually succeeds while throwing an unhandled critical error may still be invalid.

# Network Diagnostics

Record failed requests where safe.

Do not log Authorization headers, tokens, PII payloads, or confidential provider bodies.

# Trace Privacy

Traces can capture:

- DOM;
- network;
- input values;
- screenshots.

Use synthetic data and restricted artifact access.

# CI Placement

Classify journey:

```text
PR_SMOKE
PR_CRITICAL
MERGE_GATE
RELEASE_GATE
NIGHTLY
SCHEDULED_PROVIDER
PRODUCTION_SYNTHETIC
```

Not every E2E belongs on every PR.

# Fast Critical Smoke

A small critical smoke set should be fast, deterministic, and valuable enough to block a PR if project policy says so.

# Expensive Journeys

Provider sandboxes, cross-browser suites, large data, or document flows may run:

```text
nightly
release gate
manual trigger
```

# Parallelism

Parallelize independent journeys.

Ensure data namespaces do not collide.

Do not mark suites serial merely to hide isolation problems.

# Sharding

Use runner sharding when suite size justifies it.

Do not add distributed complexity prematurely.

# Environment Readiness

Before running:

```text
deployment available
backend healthy
migrations complete
test API ready
feature flags set
```

Use a readiness probe or environment contract.

Do not let first test discover half-deployed state unpredictably.

# Deployment Configuration

E2E is useful for deployment risks such as:

- base path;
- environment variables;
- route rewrites;
- API origin;
- CSP-related browser behavior;
- asset loading;
- SSR/hydration.

Test representative critical paths.

# Hydration

A critical route may need a browser assertion that:

```text
server-rendered content
→ hydrates
→ remains interactive
```

Do not test framework internals.

# Route-to-Route Journey

Verify user-facing navigation:

```text
route A
→ action
→ route B
→ persisted outcome visible
```

Avoid asserting internal router calls.

# Back / Forward

Test browser navigation only if critical to accepted journey.

Do not include it in every routing E2E.

# Reload Persistence

Useful when product guarantees state persists across reload.

Otherwise do not add it speculatively.

# Revenue / Entitlement

Critical flows may include:

```text
subscribe
upgrade
redeem
purchase
book
renew
activate entitlement
```

Use sandbox/fake payment rails approved by project.

Never execute real charges.

# Payment E2E Safety

Use provider test mode.

Verify:

- no real card;
- no production merchant;
- deterministic sandbox scenario;
- cleanup or idempotent test order.

# Entitlement End State

Verify the user-visible entitlement or stable backend test contract after success.

Do not only check “payment request was sent.”

# Destructive Flows

Account deletion or destructive operations need isolated disposable users/resources.

Never use shared accounts.

# Email / Notification

If journey requires email, use:

```text
test inbox
email sandbox
captured message service
```

Do not use real personal email accounts.

# One-Time Codes

Use approved test mechanisms to retrieve synthetic OTP.

Do not weaken production auth logic globally for tests.

# Flake Classification

Classify failing/retried test:

```text
PRODUCT_REGRESSION
TEST_DEFECT
ENVIRONMENT_OUTAGE
PROVIDER_OUTAGE
DATA_COLLISION
TIMING_FLAKE
BROWSER_FLAKE
UNKNOWN
```

# Quarantine

Quarantine only with:

- owner;
- issue;
- reason;
- expiry/review;
- non-blocking policy.

Do not permanently skip flaky critical journeys.

# Flake Budget

Track:

```text
pass-on-retry rate
failure frequency
mean time to repair
```

where organization supports it.

Do not normalize chronic flake.

# Failure Ownership

Every critical journey should have an owning team.

Failure triage should be actionable.

# Lower-Level Duplication Audit

For each E2E scenario ask whether these already prove it:

```text
Domain
Use Case
adapter
hook
component
visual
```

E2E should add integration evidence.

# Example Duplication

Scenario:

```text
invalid promotion code
```

Lower layers:

```text
Domain → code format
Use Case → semantic rejection
component → error message/focus
```

E2E is unnecessary unless a real backend/routing integration risk exists.

# Example Critical E2E

Scenario:

```text
authenticated user applies valid promotion
→ backend updates subscription
→ route reflects new price
→ reload preserves result
```

This may justify E2E because multiple real boundaries interact.

# Regression Placement

For a production bug:

1. identify root defective boundary;
2. add low-level regression there;
3. add E2E only if the bug represented a cross-boundary failure that lower tests cannot guard.

Do not add E2E automatically for every incident.

# Test Data Factories

Factories should produce valid business fixtures through accepted test-support APIs.

Do not duplicate Domain construction logic in Playwright helper code.

# API Setup Helpers

Test setup APIs should be:

- non-production or strongly protected;
- documented;
- deterministic;
- minimal;
- unavailable to ordinary end users.

Do not add insecure hidden production endpoints solely for E2E.

# DB Access

Direct DB seeding may be acceptable in ephemeral integration environments.

Prefer stable factory/test support where possible.

Do not couple browser tests to production DB schema if a test API exists.

# Schema Drift

If direct DB seeding is used, ensure migrations and test data factories evolve together.

# Multi-Tenant

Use isolated tenant/org per worker/test where needed.

Do not share tenant state across parallel tests.

# Permissions / Roles

Seed explicit roles.

Do not rely on a globally privileged test admin for every journey if permissions are part of critical behavior.

# Test Accounts

Test accounts should be:

- synthetic;
- disposable or resettable;
- excluded from analytics where policy requires;
- safely credentialed.

# Analytics

E2E generally should not assert every analytics event.

If one compliance/business-critical analytics integration needs E2E, use a test sink.

Most analytics belongs to lower provider/integration tests.

# Privacy / Consent

Consent journeys may deserve E2E when browser storage/cookies/integration matter.

Use synthetic state and verify user-visible consent behavior.

# Accessibility Journey

A representative route-level keyboard path can prove:

```text
navigation
→ dialog
→ action
→ focus after route change
```

when cross-boundary browser behavior matters.

Dedicated accessibility review/test coverage remains required for detailed criteria.

# Mobile Journey

Use a mobile viewport when:

- navigation model changes;
- touch-only layout exposes unique critical path;
- mobile web is a supported core journey.

Do not run every desktop test again on mobile.

# Offline Journey

Only test offline E2E if offline mode is a real product contract.

Use browser context offline controls.

Do not invent offline behavior.

# Service Worker

If PWA/service-worker behavior is critical, E2E may verify:

```text
install/cache
reload offline
update
```

in a supported browser/environment.

Keep detailed cache rules below where possible.

# Downloads

Use browser download APIs and assert filename/content where journey risk requires.

Do not read arbitrary local filesystem state.

# Uploads

Use synthetic files.

Do not upload confidential documents.

# Clipboard

Use browser permissions only where clipboard behavior is critical.

# Popups / New Tabs

Assert browser behavior when product relies on it.

Do not rewrite the UI solely to simplify E2E.

# Internationalization

Critical journeys may run one non-default locale when translation/layout/routing integration is business-critical.

Do not multiply every E2E by all locales.

# Theme

Theme is generally visual/component coverage, not E2E.

Only include theme in E2E if it affects critical behavior such as persisted preference across routes/reload.

# Visual Assertions in E2E

Keep image assertions in visual-regression suites unless the journey requires one very targeted visual checkpoint.

Do not turn E2E into screenshot testing.

# Stable Text

Use stable product copy when it represents the user contract.

If copy changes frequently, role/label/test-id may be more stable.

Do not hardcode entire paragraphs unnecessarily.

# Localization Assertions

Use translated semantic labels from fixtures/i18n helpers if repository conventions support it.

# Response Waiting

Avoid coupling to exact network sequence.

Prefer UI state.

Use request/response waits only when:

- the network boundary itself is the integration risk;
- it prevents ambiguous races;
- endpoint contract is intentionally stable.

# Avoid `networkidle` Blindly

`networkidle` can be unreliable for apps with polling/websockets.

Wait for semantic readiness instead.

# Polling

Disable or control non-essential polling in test environment if it creates noise, using accepted app configuration.

Do not alter production behavior just for tests without a safe environment-specific strategy.

# WebSockets

Critical real-time flows may need E2E.

Use deterministic test server events.

Do not use arbitrary sleeps waiting for a push.

# Assertions on Errors

Error/recovery E2E should assert:

```text
user sees actionable message
input/state preserved where required
retry/recovery available
final success/failure semantics
```

Do not assert raw provider error body.

# Screenshot on Failure

Useful diagnostic artifact.

Not an assertion by itself.

# Trace Annotations

Annotate:

```text
journey id
test user/resource id
feature flags
environment
```

without secrets.

# Journey Naming

Name in product language.

Good:

```text
user upgrades an active subscription
user recovers from a declined test payment
```

Weak:

```text
test case 47
click button flow
```

# Test Structure

Prefer readable high-level structure:

```ts
test("user upgrades an active subscription", async ({ page, testData }) => {
  const account = await testData.createActiveAccount()

  await page.goto("/subscriptions")
  await signInAs(page, account.user)

  await page.getByRole("link", { name: "Manage subscription" }).click()
  await page.getByRole("button", { name: "Upgrade" }).click()

  await expect(page.getByRole("heading", { name: "Subscription upgraded" }))
    .toBeVisible()
})
```

Use repository APIs and exact route/copy conventions.

# Page/Domain Language

Helpers should use product concepts.

Avoid technical wrapper names leaking into test intent.

# E2E Contract Record

For every journey record:

```text
why E2E
starting state
environment
test data
critical path
unique integration risk
recovery path
cleanup
CI tier
diagnostics
```

# Journey Evaluation — Authentication

Verify login/session only when it is part of unique E2E risk.

Use storage state for unrelated authenticated journeys.

# Journey Evaluation — Revenue/Entitlement

Use sandbox/test mode and verify final user-visible entitlement.

No production payment.

# Journey Evaluation — Route-to-Route

Assert navigation and state persistence from user perspective.

# Journey Evaluation — Browser Integration

Cover a browser capability only if supported and critical.

# Journey Evaluation — Hydration/Deployment

Use deployed/preview environment where configuration can differ from local component tests.

# Journey Evaluation — Recovery

Cover one representative critical failure/retry path rather than every error code.

# Over-E2E Audit

Flag:

- every validation rule repeated E2E;
- every API error code;
- every component state;
- every theme;
- every locale;
- UI setup for unrelated preconditions;
- same business rule repeated across all layers;
- browser matrix explosion.

Use:

```text
PROPORTIONATE_E2E_COVERAGE
ALL_E2E_STRATEGY
DUPLICATED_LOWER_LEVEL_COVERAGE
E2E_MATRIX_EXPLOSION
```

# Under-E2E Audit

Flag:

- critical revenue journey has no deployed-browser confidence;
- authentication/session integration never tested;
- route-to-route critical workflow only has isolated component tests;
- production incident caused by deployment/hydration config has no outer regression;
- no diagnostics/data isolation.

# Final Decision

Use:

```text
FRONTEND_USER_JOURNEYS_READY
FRONTEND_USER_JOURNEYS_READY_WITH_CONDITIONS
E2E_NOT_REQUIRED
TEST_DATA_ISOLATION_REQUIRED
ENVIRONMENT_CONTRACT_REQUIRED
AUTH_TEST_STRATEGY_REQUIRED
FAILURE_DIAGNOSTICS_REQUIRED
E2E_SCOPE_REQUIRES_DECISION
BLOCKED
```

## Output

Use `assets/frontend-user-journey-testing-record.md`.

## Completion Criteria

- [ ] Every implemented journey is explicitly justified as E2E.
- [ ] Lower-level coverage was inspected first.
- [ ] E2E adds unique integration confidence.
- [ ] Suite is intentionally small relative to local behavior surface.
- [ ] Critical success path is covered.
- [ ] Only one/few critical failure/recovery paths are added.
- [ ] Environment is controlled and documented.
- [ ] Mutable data is isolated per test/worker.
- [ ] Test setup uses deterministic factories/APIs where setup itself is not the journey.
- [ ] Cleanup is reliable and idempotent.
- [ ] Tests do not depend on order.
- [ ] Authentication uses real UI only when login is the risk.
- [ ] Authenticated state is reused safely for unrelated journeys.
- [ ] Feature flags, time, locale, timezone, and roles are deterministic where relevant.
- [ ] Production credentials/resources are never used.
- [ ] Payment/provider journeys use safe sandbox/test mode.
- [ ] User interactions use stable semantic locators.
- [ ] Assertions target user-visible/stable outcomes.
- [ ] DOM structure/classes/private app state are not asserted.
- [ ] Arbitrary sleeps are absent.
- [ ] Runner retries do not hide product/test flake.
- [ ] Browser matrix is risk-based.
- [ ] E2E does not duplicate every validation/provider/component/theme branch.
- [ ] Representative accessibility/browser recovery coverage remains proportional.
- [ ] Critical failures retain trace/screenshot/video/console/network diagnostics according to policy.
- [ ] Diagnostic artifacts contain only synthetic/privacy-safe data.
- [ ] CI placement matches journey cost/risk.
- [ ] Flaky tests have owner/classification rather than permanent silent skips.
- [ ] Regression tests are added at the lowest defective boundary first.
- [ ] Final E2E status is explicit.

## References

- Read `references/selecting-critical-e2e-journeys.md` first.
- Read `references/environment-data-isolation-seeding-and-cleanup.md`.
- Read `references/authentication-sessions-flags-time-and-test-identities.md`.
- Read `references/resilient-locators-waits-assertions-and-page-objects.md`.
- Read `references/critical-failure-recovery-and-external-provider-flows.md`.
- Read `references/diagnostics-traces-ci-flake-and-quarantine.md`.
- Read `references/browser-matrix-accessibility-mobile-and-deployment-risk.md`.
- Read `references/frontend-user-journey-testing-audit.md` before completion.
