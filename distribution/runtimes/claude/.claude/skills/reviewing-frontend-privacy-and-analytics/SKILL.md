---
name: reviewing-frontend-privacy-and-analytics
description: Reviews frontend analytics, telemetry, consent handling, PII exposure, retention assumptions, event naming, debug logging, and third-party analytics/provider boundaries. Use when page tracking, form analytics, user identifiers, consent withdrawal, telemetry SDKs, session replay, error reporting, or client-side debug events may collect or transmit user data. Ensure analytics follows application privacy/consent policy and cannot bypass it through direct SDK calls. Keep provider access behind application/infrastructure boundaries and prefer data minimization. Do not invent legal requirements, infer consent policy, classify every identifier as forbidden PII, or duplicate general security findings handled by reviewing-frontend-security.
---

# Reviewing Frontend Privacy and Analytics

## Purpose

Review whether frontend analytics and telemetry follow the application's accepted privacy, consent, minimization, and provider-boundary policy.

Core workflow:

```text
analytics/telemetry surface
→ identify data collected
→ identify purpose/event owner
→ identify consent/policy gate
→ identify provider boundary
→ minimize payload
→ verify withdrawal/disable behavior
→ inspect retention/debug leakage
→ produce remediation + evidence plan
```

This skill answers:

```text
Does frontend telemetry collect and transmit only what the application policy allows,
through controlled boundaries, with the correct consent state?
```

It does not determine law or regulation by itself.

## Governing Standard

The frontend engineering standard requires:

```text
Analytics and telemetry MUST follow privacy and consent requirements.
```

Analytics adapters belong to frontend Infrastructure.

Presentation/Application code should not bypass approved analytics abstractions by calling provider SDKs directly when project architecture defines a provider boundary.

## Roadmap Purpose

- inspect telemetry;
- inspect consent;
- inspect PII;
- inspect retention;
- inspect event naming;
- inspect provider boundaries;
- ensure analytics does not bypass application policy.

## Roadmap Evaluations

This skill MUST cover:

```text
page tracking
form field capture
consent withdrawal
user identifier
debug logging
third-party SDK
```

## Use When

- Adding or reviewing page analytics.
- Adding event tracking.
- Adding form analytics.
- Adding session replay or heatmaps.
- Adding product analytics.
- Adding error/telemetry SDKs that include user context.
- Reviewing analytics user IDs.
- Reviewing consent gating.
- Reviewing consent withdrawal.
- Reviewing third-party analytics SDKs.
- Reviewing debug telemetry/logging.
- Reviewing analytics adapter architecture.
- Reviewing retention/config assumptions visible to frontend ownership.

## Do Not Use When

- The task is purely XSS/token/security review.
- The task is legal advice.
- The task is backend data-governance review only.
- The task is general product metrics design with no privacy/telemetry implications.
- The project has no analytics/telemetry surface.
- Exact consent/retention policy is unknown and the review would require inventing one.

## Inputs

- Accepted privacy/consent policy.
- Analytics requirements.
- Event catalog if available.
- Analytics adapter/port.
- Provider SDK configuration.
- Consent-state source.
- User/session identity model.
- Event payloads.
- Error/debug logging.
- Form analytics.
- Session replay configuration.
- Retention settings/contract if available.
- Third-party SDK data contracts.
- Applicable `AGENTS.md`.

## Outputs

- Analytics/telemetry inventory.
- Event/data inventory.
- Consent-gating assessment.
- PII/sensitive-field assessment.
- User-identifier assessment.
- Provider-boundary assessment.
- Retention evidence/gaps.
- Debug logging assessment.
- Withdrawal behavior assessment.
- Remediation and verification plan.
- Frontend privacy/analytics review record.

# Policy Gate

Before judging a telemetry event, identify the accepted application policy.

Record:

```text
what may be collected
for what purpose
under which consent state
for which user/account type
with which provider
for how long if defined
```

If this is unknown:

```text
PRIVACY_POLICY_REQUIRED
```

Do not invent consent requirements from general knowledge.

# Data Inventory

For each event record:

```text
event name
trigger
purpose
payload
user/session identifiers
page/route
provider
consent requirement
retention if known
```

# Data Minimization

Prefer:

```text
minimum data needed for the declared purpose
```

Avoid sending raw domain objects or complete form state when one semantic flag/count is sufficient.

Bad:

```ts
analytics.track("checkout_failed", formState)
```

Better:

```ts
analytics.track("checkout_failed", {
  reasonCode,
  step,
})
```

when accepted policy permits those fields.

# Event Naming

Event names SHOULD be:

- stable;
- product/domain-oriented;
- documented;
- purpose-specific.

Prefer:

```text
subscription_upgrade_started
subscription_upgrade_succeeded
```

over:

```text
button_clicked_17
event2
```

Do not encode personal data into event names.

# Event Payload Schema

Define allowed fields explicitly.

Avoid:

```text
spread entire API response
spread user object
spread form values
```

Use a typed event contract where project architecture supports it.

# Analytics Adapter Boundary

Frontend Infrastructure owns analytics adapters.

Preferred:

```text
Presentation/Application
→ analytics port / approved event API
→ Infrastructure analytics adapter
→ provider SDK
```

Avoid:

```text
component
→ window.gtag(...)
```

or:

```text
hook
→ mixpanel.track(...)
```

when that bypasses application consent/payload policy.

# Provider-Agnostic Event Contract

Prefer application-owned event semantics.

Provider-specific details belong in adapter:

```text
product event
→ provider mapping
```

This supports:

- policy enforcement;
- provider replacement;
- payload review;
- tests;
- consent gating.

# Consent Gate

Consent-sensitive events must not be emitted before the accepted consent state permits them.

Check:

```text
initial unknown state
granted
denied
withdrawn
changed
```

Unknown should not be silently treated as granted unless project policy explicitly says so.

# Consent Source of Truth

Use one accepted source:

```text
consent manager
cookie preference state
application privacy service
```

Do not let each SDK maintain its own uncontrolled interpretation when application policy requires centralized consent.

# Consent Race

Review startup order:

```text
app starts
→ SDK loads
→ page event fires
→ consent state resolves
```

A common defect is sending an initial page event before consent resolves.

Use deterministic gating.

# Roadmap Evaluation — Page Tracking

Review:

- when page view fires;
- route identity;
- URL/query data;
- user identifier;
- consent state;
- duplicate SPA route events;
- provider adapter path.

Do not send full query strings blindly if they may contain sensitive data.

# SPA Page Tracking

In client routing:

```text
route change
→ normalized page identifier
→ consent/policy gate
→ analytics adapter
```

Avoid duplicate initial page + router event without intention.

# URL Sanitization

Prefer semantic route/page names or sanitized path.

Review query/hash for:

- email;
- tokens;
- search terms;
- IDs;
- invite codes;
- callback data.

Do not automatically send `location.href`.

# Roadmap Evaluation — Form Field Capture

Default principle:

```text
do not capture raw form values unless explicitly required and approved
```

High-risk examples:

```text
name
email
phone
address
password
payment data
free-text message
health/financial/sensitive notes
```

Prefer interaction metadata:

```text
field_name
validation_state
step
completion
```

where policy allows.

# Password / Credential Fields

Never send password or authentication secret values to analytics/telemetry.

# Payment Fields

Do not send card/security-code/bank credential values.

Provider payment telemetry should use provider-safe identifiers/status codes according to accepted policy.

# Free Text

Free text is difficult to constrain and can contain unexpected sensitive data.

Avoid capturing raw free-text content unless explicitly required and reviewed.

# Automatic Form Capture

Review SDK features such as:

```text
autocapture
session replay
DOM capture
form analytics
```

Default provider settings may collect more than intended.

Disable or mask according to application policy.

# Session Replay

Review:

- enabled routes;
- masking;
- text/input capture;
- screenshots;
- identifiers;
- consent;
- provider;
- retention.

Do not assume “mask all inputs” is enough if page text or DOM attributes can contain sensitive information.

# Roadmap Evaluation — Consent Withdrawal

Withdrawal should take effect for future collection according to accepted policy.

Review:

```text
stop event transmission
disable/opt-out provider
clear provider identifiers where required by project policy
stop replay
prevent queued event flush if policy requires
update application consent state
```

Do not assume changing a UI toggle automatically stops already initialized SDKs.

# Provider Opt-Out

Some SDKs maintain cookies/local IDs after application consent changes.

The analytics adapter should implement the provider-specific withdrawal mechanism when required.

# Consent Re-Grant

If consent is later granted:

- initialize/start only accepted providers;
- avoid duplicate identities/events;
- restore policy-consistent state.

# Roadmap Evaluation — User Identifier

Classify identifiers by purpose and policy.

Examples:

```text
internal stable user ID
tenant ID
anonymous analytics ID
session ID
email
username
device/provider ID
```

A stable internal ID can still be personal data depending on project policy/context.

Do not assume hashing makes an identifier anonymous.

# Hashed Identifiers

Hashing an email/ID usually produces a persistent pseudonymous identifier, not automatic anonymization.

Do not use hashing as permission to collect data that policy forbids.

# Prefer Purpose-Built IDs

Prefer:

```text
analytics-specific pseudonymous ID
```

when product policy supports it, instead of raw email/username.

# Tenant / Organization IDs

Review whether provider needs organization identity.

Avoid sending customer-readable names when an internal scoped identifier is sufficient.

# Identity Reset

On logout/account switch/tenant switch, review whether analytics identity should:

```text
reset
change
associate
```

according to provider and application policy.

Prevent previous-user identity from leaking into next session on shared devices.

# Anonymous to Authenticated Merge

Provider identity merge can connect pre-login activity with a known user.

This should be intentional and consistent with application policy.

# Roadmap Evaluation — Debug Logging

Review:

```text
console.log
debug telemetry
provider debug mode
network event inspector
error tracking breadcrumbs
raw payload logs
```

Avoid sensitive payloads.

Debug mode must not silently expand collection in production.

# Production Debug Logs

Remove or gate development analytics dumps that expose:

- user objects;
- tokens;
- form data;
- provider payloads;
- consent state with sensitive metadata.

# Error Reporting

Error trackers can collect:

- URLs;
- breadcrumbs;
- DOM/context;
- request metadata;
- user identity;
- stack traces.

Review data-scrubbing and consent/policy requirements separately from security.

# Roadmap Evaluation — Third-Party SDK

Review each SDK:

```text
purpose
provider
data sent
automatic collection
cookies/storage
user identifiers
consent gate
retention setting/contract
subprocessors if project policy tracks them
runtime permissions
disable/withdraw mechanism
```

Do not add provider SDK directly in random components.

# SDK Initialization

Preferred:

```text
application bootstrap/composition
→ consent/policy state
→ analytics adapter/provider initialization
```

not:

```text
import SDK
→ SDK auto-starts on module load
```

if consent/policy gating is required.

# SDK Autocapture

Disable default automatic collection that exceeds accepted event policy.

Explicit event allowlists are easier to review.

# Provider Boundary

Provider-specific APIs stay in Infrastructure.

Application/presentation should depend on application-owned event semantics.

# Provider Failure

Analytics must generally not break core product flow.

If provider fails:

```text
business operation continues
```

unless analytics is explicitly a business requirement.

Do not let telemetry exceptions crash the UI.

# Analytics Blocking UX

Avoid awaiting non-critical analytics before navigation/critical actions unless policy/product explicitly requires delivery.

Use provider-safe asynchronous handling.

# Retention

Frontend may not own retention, but review must record:

```text
provider retention configured?
owner?
evidence?
unknown?
```

If retention is required by policy but no evidence exists:

```text
RETENTION_EVIDENCE_REQUIRED
```

Do not invent a number of days.

# Retention Boundary

Retention may be enforced in:

- provider settings;
- backend pipeline;
- warehouse;
- event proxy;
- analytics platform.

Link to owner rather than duplicating configuration.

# Data Deletion / Identity Erasure

If application policy includes deletion/erasure workflows, verify analytics ownership/handoff.

Do not invent legal deletion obligations when policy is absent.

# Environment Separation

Ensure:

```text
development
staging
production
```

analytics are separated where project policy requires.

Avoid polluting production analytics from local/dev environments.

# Test Users / Synthetic Traffic

If policy supports it, tag or exclude test traffic.

Do not include real customer identifiers in development telemetry.

# Analytics and Authorization

Analytics must not bypass access policy.

Example:

```text
component cannot read full customer profile
but analytics SDK receives it anyway
```

is a policy boundary violation.

Telemetry gets only data the application is allowed to expose for the declared purpose.

# Analytics and Security

Security concerns such as:

- arbitrary script injection;
- token theft;
- XSS;
- exposed secrets;

belong to `reviewing-frontend-security`.

Privacy concerns such as:

- consent;
- form capture;
- user ID;
- retention;
- event payload minimization;

belong here.

A third-party SDK can require both reviews.

# PII / Sensitive Data Classification

Use the project's terminology/classification.

If no classification exists, do not invent legal categories.

Record:

```text
KNOWN_SENSITIVE
POTENTIALLY_IDENTIFYING
NON_SENSITIVE_BY_POLICY
CLASSIFICATION_REQUIRED
```

# No Raw Domain Objects

Avoid:

```ts
analytics.track("user_loaded", user)
```

Prefer explicit projection:

```ts
analytics.track("subscription_loaded", {
  status,
  planType,
})
```

if policy permits.

# Event Review Checklist

For each event:

```text
purpose clear?
name stable?
trigger correct?
payload minimized?
identifier necessary?
consent gate correct?
provider correct?
retention known?
debug-safe?
testable?
```

# Event Catalog

Maintain an event catalog when project scale justifies it.

Useful fields:

```text
event
owner
purpose
trigger
payload schema
consent category
provider
identifier policy
retention owner
```

# Event Versioning

For breaking analytics schema changes, use project convention:

- event version field;
- renamed event;
- migration window.

Do not create arbitrary versioning if analytics platform already owns schema evolution.

# Provider Mapping

Example:

```text
application event:
subscription_upgrade_succeeded

provider A:
track("Subscription Upgraded", ...)

provider B:
event("subscription_upgrade_succeeded", ...)
```

Application code should not know provider naming quirks.

# Duplicate Analytics

SPA/component lifecycle can emit duplicate events.

Review:

- Strict Mode dev behavior;
- mount/remount;
- retry;
- route transition;
- provider auto page tracking + manual tracking.

Confirm production behavior before reporting.

# Idempotency / Deduplication

Analytics dedupe may use:

```text
event ID
interaction ID
route transition ID
```

only if provider/product semantics need it.

Do not overengineer for low-value telemetry.

# Server vs Client Analytics

Some events may be more trustworthy server-side:

```text
payment succeeded
subscription activated
entitlement granted
```

because frontend can close/reload or be manipulated.

Use frontend analytics for user interaction; use authoritative server event for business outcome where architecture supports it.

Avoid double-counting the same business event from both sides without reconciliation.

# Business-Critical Analytics

If analytics drives billing, entitlement, fraud, or legal process, it is no longer “best-effort telemetry.”

Escalate architecture/security/reliability review.

# Consent Categories

Use exact project categories.

Examples could include:

```text
necessary
analytics
personalization
marketing
```

but do not invent them if not defined.

# Necessary Telemetry

Do not label product analytics “necessary” merely to bypass consent.

Use project policy.

# Consent Persistence

Review where consent state is persisted and how it is restored before SDK initialization.

Browser storage state should be runtime-validated if read by application logic.

# Consent Withdrawal Race

Test:

```text
event scheduled
→ user withdraws
→ event flush happens
```

according to provider/application policy.

# Multi-Tab

If consent state can change in another tab, determine whether synchronization is required by project behavior.

Do not invent cross-tab requirements without policy.

# Route Analytics Example

Bad:

```ts
analytics.track("page_view", {
  url: window.location.href,
  user: currentUser,
})
```

Better:

```ts
analytics.track("page_view", {
  page: "subscription_details",
})
```

plus only explicitly approved dimensions.

# Form Example

Bad:

```ts
analytics.track("form_change", {
  values: form.getValues(),
})
```

Better:

```ts
analytics.track("form_validation_failed", {
  field: "postal_code",
  reason: "invalid_format",
})
```

if accepted policy permits.

# User Identifier Example

Bad:

```text
userId = email
```

just because provider needs a string.

Prefer approved stable analytics identifier.

# Withdrawal Example

Bad:

```text
setConsent(false)
```

only updates React state while SDK continues recording.

Need provider opt-out/disable implementation where required.

# Debug Example

Bad:

```ts
console.log("analytics event", eventPayload)
```

when payload can contain user identifiers/form data.

# Third-Party Example

Bad:

```ts
import "provider-sdk/auto"
```

when module initialization starts tracking before consent state resolves.

# Testing Strategy

Prefer lower-level tests around analytics adapter/policy.

Examples:

```text
consent denied → provider.track not called
consent unknown → provider not initialized
consent withdrawn → provider optOut called
event projection removes email
logout → provider reset
page tracking strips query
```

# Provider Adapter Tests

Stub/mock provider boundary, not policy code.

The application analytics service/policy should be real under test.

# Browser Integration Tests

Use browser/E2E selectively for:

- consent manager integration;
- SDK cookie/storage behavior;
- route tracking;
- withdrawal;
- session replay masking.

Do not test every event E2E.

# Audit Trail

For privacy-sensitive analytics changes record:

```text
event added/changed
payload fields
policy decision
consent category
provider
owner
review evidence
```

# Findings

Use:

```text
PRIV-001
PRIV-002
```

Each finding should include:

```text
surface
data collected
purpose
policy/consent requirement
actual behavior
provider
impact
remediation
verification
owner
```

# Status

Use:

```text
CONFIRMED
LIKELY_REQUIRES_VALIDATION
POLICY_DECISION_REQUIRED
EVIDENCE_REQUIRED
NOT_APPLICABLE
```

# Severity / Priority

Do not invent legal severity.

Use review priority:

```text
BLOCKING
HIGH
MEDIUM
LOW
ADVISORY
```

based on:

- sensitive data;
- collection without required consent;
- broad provider exposure;
- inability to withdraw;
- uncontrolled auto-capture;
- production leakage;
- event volume/blast radius.

# Roadmap Evaluation — Page Tracking

Pass when:

- page event has stable semantic identity;
- payload excludes unnecessary URL/query data;
- consent gate is correct;
- duplicates are controlled;
- provider boundary is respected.

# Roadmap Evaluation — Form Field Capture

Pass when:

- raw sensitive values are not captured by default;
- automatic form/session-replay capture is reviewed;
- only approved/minimized metadata is emitted.

# Roadmap Evaluation — Consent Withdrawal

Pass when:

- application state changes;
- provider collection stops as required;
- replay/queue behavior is handled according to policy;
- identity reset/cleanup happens where required.

# Roadmap Evaluation — User Identifier

Pass when:

- identifier purpose is explicit;
- raw email/username is avoided unless approved;
- hashing is not misrepresented as anonymization;
- logout/account switch behavior is correct.

# Roadmap Evaluation — Debug Logging

Pass when:

- debug logs/telemetry exclude sensitive payloads;
- production debug mode does not broaden collection;
- error-reporting context is scrubbed.

# Roadmap Evaluation — Third-Party SDK

Pass when:

- provider purpose/data/auto-collection is known;
- SDK is gated by application policy;
- initialization does not bypass consent;
- retention/disable ownership is known;
- provider-specific behavior is isolated in Infrastructure.

# Over-Review Audit

Flag:

- every identifier called forbidden;
- legal conclusions without policy;
- retention period invented;
- every analytics event blocked;
- security findings duplicated;
- provider SDK banned solely because third-party.

Use:

```text
PROPORTIONATE_PRIVACY_ANALYTICS_REVIEW
OVERCLASSIFIED_PRIVACY_RISK
POLICY_REQUIRED
```

# Under-Review Audit

Flag:

- full URL page tracking;
- raw form values;
- session replay without review;
- consent denied but SDK initialized;
- withdrawal only updates UI state;
- raw email as provider identity without policy;
- production analytics payload console logging;
- provider autocapture bypassing adapter/policy.

# Final Decision

Use:

```text
FRONTEND_PRIVACY_ANALYTICS_ACCEPTABLE
FRONTEND_PRIVACY_ANALYTICS_ACCEPTABLE_WITH_CONDITIONS
FRONTEND_PRIVACY_ANALYTICS_REMEDIATION_REQUIRED
PRIVACY_POLICY_REQUIRED
CONSENT_IMPLEMENTATION_REQUIRED
DATA_MINIMIZATION_REQUIRED
PROVIDER_BOUNDARY_REQUIRED
RETENTION_EVIDENCE_REQUIRED
PRIVACY_ANALYTICS_EVIDENCE_REQUIRED
BLOCKED
```

## Output

Use `assets/frontend-privacy-analytics-review-record.md`.

## Completion Criteria

- [ ] Review scope and accepted policy are explicit.
- [ ] Analytics/telemetry events are inventoried.
- [ ] Event purpose is explicit.
- [ ] Event naming is stable and product/domain-oriented.
- [ ] Payload schemas are explicit and minimized.
- [ ] Raw domain objects are not forwarded blindly.
- [ ] PII/sensitive classification uses project policy/terminology.
- [ ] Unknown classification is reported instead of invented.
- [ ] Page tracking does not blindly send full URL/query/hash.
- [ ] SPA duplicate page tracking is inspected.
- [ ] Form analytics does not capture raw sensitive values by default.
- [ ] Autocapture/session replay configuration is reviewed.
- [ ] Consent-sensitive providers/events are gated before initialization/emission.
- [ ] Unknown consent is not silently treated as granted unless policy says so.
- [ ] Consent withdrawal stops provider collection as required.
- [ ] Provider opt-out/reset behavior is implemented where policy requires.
- [ ] User identifiers are purpose-specific and minimized.
- [ ] Hashing is not misrepresented as anonymization.
- [ ] Logout/account/tenant switch identity behavior is reviewed.
- [ ] Debug logging excludes sensitive event payloads.
- [ ] Error telemetry data scrubbing is reviewed.
- [ ] Third-party SDK auto-collection is understood.
- [ ] Provider-specific code is isolated in Infrastructure/analytics adapters.
- [ ] Analytics cannot bypass application consent/payload policy via direct SDK calls.
- [ ] Retention ownership/evidence is recorded where required.
- [ ] Development/staging traffic does not contaminate production where policy requires separation.
- [ ] Security issues are handed to `reviewing-frontend-security` rather than duplicated.
- [ ] Tests cover consent denial/withdrawal and payload minimization at the lowest useful boundary.
- [ ] Roadmap evaluations are covered: page tracking, form field capture, consent withdrawal, user identifier, debug logging, third-party SDK.
- [ ] Final privacy/analytics status is explicit.

## References

- Read `references/analytics-policy-data-minimization-and-event-contracts.md` first.
- Read `references/consent-gating-initialization-and-withdrawal.md`.
- Read `references/page-tracking-urls-and-spa-routing.md`.
- Read `references/forms-session-replay-and-autocapture.md`.
- Read `references/user-identifiers-identity-reset-and-pseudonymization.md`.
- Read `references/debug-logging-error-telemetry-and-sensitive-context.md`.
- Read `references/third-party-sdks-provider-boundaries-and-retention.md`.
- Read `references/frontend-privacy-analytics-review-audit.md` before completion.
