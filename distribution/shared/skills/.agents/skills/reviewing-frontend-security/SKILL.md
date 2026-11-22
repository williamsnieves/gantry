---
name: reviewing-frontend-security
description: Reviews implemented frontend/browser code for security risks specific to the client trust boundary. Use for XSS and unsafe HTML sinks, token/session storage, browser-visible secrets and environment variables, redirect/navigation handling, file upload and browser file processing, third-party scripts, browser storage, postMessage/iframe boundaries, URL/referrer leakage, CSP-related risks, and client-side authorization assumptions. Treat all frontend data and shipped configuration as observable by the user, and distinguish UX permission checks from authoritative server-side security. Reuse reviewing-application-security for OWASP/CWE classification, threat-modeling-with-stride for architectural threat discovery, and verifying-security-controls for ASVS/control evidence. Do not duplicate generic application-security taxonomies, claim frontend route guards are authorization, or flag dangerous-looking APIs without tracing source, sink, sanitization, context, and exploitability.
...
---

# Reviewing Frontend Security

## Purpose

Review security risks created by the browser/client trust boundary.

Core model:

```text
browser-delivered code/config/data
→ assume user can observe or modify it
→ inspect sources, sinks, storage, navigation, files, third parties, permissions
→ prove exploit path
→ remediate at the correct trust boundary
```

The governing frontend rule is:

```text
all client-side data is observable by the user
```

Therefore:

```text
frontend secrecy
≠
security boundary
```

and:

```text
frontend permission UX
≠
server authorization
```

## Composition with Cross-Cutting Security Skills

This skill specializes frontend/browser concerns.

Use:

```text
threat-modeling-with-stride
→ architecture threats and trust boundaries

reviewing-application-security
→ OWASP Top 10:2025 + precise CWE classification

verifying-security-controls
→ ASVS/project-control evidence

analyzing-algorithmic-complexity
→ algorithmic DoS when browser/client computation is security relevant
```

Do not duplicate their complete rules here.

## Roadmap Purpose

- inspect XSS;
- inspect token storage;
- inspect sensitive data exposure;
- inspect unsafe HTML;
- inspect dependency risks;
- inspect authorization assumptions;
- distinguish UX permission checks from server security.

## Roadmap Evaluations

This skill MUST cover:

```text
dangerouslySetInnerHTML
localStorage token
secret environment variable
redirect handling
file upload
third-party script
```

## Use When

- Reviewing a React/Vue/Svelte/Angular/browser frontend.
- Reviewing an SPA or SSR/CSR client boundary.
- Reviewing `dangerouslySetInnerHTML` or equivalent HTML sink.
- Reviewing markdown/rich-text rendering.
- Reviewing token/session persistence.
- Reviewing browser storage.
- Reviewing environment variables exposed to client build.
- Reviewing open redirects or callback/return URLs.
- Reviewing file selection/upload/preview.
- Reviewing third-party runtime scripts.
- Reviewing analytics/tag manager code from a security perspective.
- Reviewing `postMessage`, iframes, popups, or cross-window communication.
- Reviewing URL/query/hash leakage.
- Reviewing frontend permission/role guards.
- Reviewing CSP or browser security mechanisms.
- Reviewing frontend dependency/runtime-supply-chain exposure.

## Do Not Use When

- The task is purely backend authorization/injection/SSRF.
- The system is still only architecture/design.
- The task is ASVS verification only.
- The task is privacy/analytics policy rather than security.
- The task is dependency CVE scanning only.
- The task is generic threat modeling.
- The task is only accessibility/performance.

## Inputs

- Frontend code/config.
- Framework/version.
- Rendering model.
- Auth/session model.
- Browser storage model.
- HTML/markdown/rich-text rendering.
- Redirect/navigation logic.
- File handling.
- Third-party scripts/SDKs.
- Environment/build variables.
- CSP/security headers where visible/available.
- Backend authorization contract.
- Threat model if available.
- Application-security findings if available.
- Existing browser/security tests.
- Applicable `AGENTS.md`.

## Outputs

- Frontend security scope.
- Browser attack-surface inventory.
- Evidence-backed findings.
- Trust-boundary classification.
- Required server-side handoffs.
- OWASP/CWE handoff.
- Control-verification handoff.
- Remediation and negative-test plan.
- Frontend-security review record.

# Browser Trust Model

Assume the user can:

- inspect JS bundles;
- inspect source maps if served;
- change browser storage;
- modify DOM;
- replay requests;
- change URL/query/hash;
- call APIs directly;
- alter client state;
- bypass hidden/disabled UI;
- run browser extensions;
- inspect network traffic visible to their browser.

Therefore never protect authority through client obscurity.

# Secrets

The frontend standard says:

```text
Never store secrets in frontend bundles.
```

Anything compiled/shipped to the browser is not secret.

Examples:

```text
VITE_*
NEXT_PUBLIC_*
PUBLIC_*
client config JSON
inline script config
window.__ENV__
```

can be visible by design.

Review the build/runtime convention rather than the variable name alone.

# Roadmap Evaluation — Secret Environment Variable

Find:

```text
API secrets
webhook secrets
private signing keys
provider private keys
database credentials
service credentials
internal bearer tokens
```

referenced by client code.

Classify as real exposure when the value is shipped or retrievable by browser users.

Do not flag public identifiers such as:

```text
public analytics site ID
public OAuth client ID
public map project identifier
```

merely because they are in client config.

Determine whether the value is intended to be public.

# Browser-Visible Configuration

For every sensitive-looking value ask:

```text
Is it secret by security model?
Is it included in browser-delivered code/config?
Can a normal user retrieve it?
What privilege does possession grant?
```

If possession grants privileged backend/provider access, it must remain server-side.

# Token / Session Storage

Roadmap evaluation:

```text
localStorage token
```

Review:

```text
localStorage
sessionStorage
IndexedDB
memory
cookies
service worker storage
URL/hash/query
```

# Token Threat Model

Browser-accessible tokens are exposed to successful XSS.

Persistent storage can increase exposure duration.

But security design depends on:

```text
token type
scope
lifetime
rotation
refresh model
XSS threat
backend architecture
cookie model
CSRF model
```

Do not prescribe one universal storage mechanism without context.

# localStorage Token

A long-lived bearer token in localStorage is typically high risk because:

```text
successful same-origin script execution
→ token read
→ token exfiltration
→ replay outside browser
```

Evaluate:

- token lifetime;
- refresh token presence;
- scope;
- rotation;
- logout invalidation;
- CSP;
- XSS surface;
- same-origin third-party scripts.

Prefer an architecture that reduces browser-readable high-value credentials where feasible.

# Cookie Sessions

HttpOnly cookies reduce JS access but introduce/retain browser ambient credential semantics.

Review:

```text
HttpOnly
Secure
SameSite
domain/path
expiry
CSRF controls
session fixation
logout/revocation
```

Do not say “cookies are secure” without evaluating configuration.

# In-Memory Tokens

Memory can reduce persistence but does not eliminate XSS access while token exists.

Do not present it as complete XSS mitigation.

# URL Tokens

Avoid credentials in:

```text
query
path
fragment
```

unless protocol explicitly requires a temporary value and leakage is controlled.

URLs may leak through:

- history;
- screenshots;
- logs;
- referrers;
- copy/paste;
- analytics.

# Token Logging

Never log:

```text
Authorization
access token
refresh token
ID token
session cookie
```

in browser console/telemetry.

# XSS Review

Trace:

```text
untrusted source
→ transformation/sanitizer
→ rendering context/sink
→ browser execution capability
```

Sources include:

- API payload;
- URL;
- storage;
- postMessage;
- user content;
- third-party content;
- markdown;
- CMS;
- localization content;
- provider errors.

# Unsafe HTML Sinks

Inspect:

```text
dangerouslySetInnerHTML
innerHTML
outerHTML
insertAdjacentHTML
document.write
DOMParser with later insertion
HTML template rendering
rich-text renderer
markdown allowing raw HTML
SVG injection
```

Framework escaping is preferred for ordinary text.

# Roadmap Evaluation — dangerouslySetInnerHTML

Do not auto-fail merely because it exists.

Determine:

```text
source trusted?
sanitizer exists?
sanitizer configuration?
sanitizer maintained?
correct output context?
dangerous URL schemes?
SVG/MathML behavior?
post-sanitization mutation?
CSP defense-in-depth?
```

A safe constant HTML fragment differs from user-authored raw HTML.

# Sanitization

Use an established sanitizer appropriate to the content/context.

Review allowlist for:

- tags;
- attributes;
- URLs;
- protocols;
- style;
- SVG/MathML;
- custom elements.

Do not build sanitizer with ad hoc regex.

# Encoding vs Sanitization

Use escaping/encoding for text/context where HTML is not required.

Use sanitization only when product truly requires controlled HTML.

Prefer:

```text
render text
```

over:

```text
sanitize arbitrary HTML
```

when possible.

# React / Framework Escaping

Normal framework interpolation:

```jsx
<div>{userInput}</div>
```

is generally escaped as text.

Do not replace it with manual HTML encoding unnecessarily.

# DOM-Based XSS

Review URL/storage/message data reaching DOM sinks without server involvement.

Examples:

```text
location.hash
location.search
localStorage
postMessage
```

→ unsafe HTML/URL/script sink.

# URL Sinks

Review:

```text
href
src
window.location
location.assign
window.open
iframe src
script src
form action
```

for unsafe protocols/destinations.

# javascript: / data: URLs

Prevent dangerous schemes in user-controlled navigations/resources according to actual element/context.

Do not use naive string-prefix filters susceptible to normalization/encoding tricks.

# CSP

CSP is defense in depth for XSS and third-party content.

Review when available:

- script-src;
- object-src;
- base-uri;
- frame-ancestors;
- nonce/hash strategy;
- unsafe-inline;
- unsafe-eval;
- allowed third parties.

Do not treat CSP as a replacement for safe rendering.

# Trusted Types

If selected by the application, Trusted Types can strengthen DOM sink controls.

Do not require it universally unless project/security policy does.

# Sensitive Data Exposure

The frontend standard says avoid exposing:

- internal stack traces;
- private identifiers unnecessarily;
- insecurely stored auth tokens;
- sensitive logs;
- provider credentials.

Review browser-visible:

```text
API responses
preloaded state
SSR hydration payload
HTML source
source maps
console logs
analytics
error trackers
local/session storage
IndexedDB
URLs
DOM attributes
```

# SSR / Hydration Payloads

Server-rendered state sent to browser is browser-visible.

Do not place server secrets or unauthorized records in serialized hydration payloads.

Authorization must happen before serialization.

# Source Maps

Source maps are not automatically a vulnerability.

Review whether they expose:

- embedded source secrets;
- internal endpoints;
- proprietary source beyond policy;
- debug data.

Secrets should never be in source regardless of source-map publication.

# Private Identifiers

An opaque ID is not authorization.

Even UUIDs can be exposed if user is legitimately sent them.

Server ownership checks remain mandatory.

# Error Messages

Do not expose:

- stack traces;
- SQL/provider internals;
- tokens;
- sensitive request data.

Use stable user-facing errors and protected server diagnostics.

# Authorization Assumptions

Roadmap purpose:

```text
distinguish UX permission checks from server security
```

Frontend checks may:

- hide unavailable actions;
- disable controls;
- tailor navigation;
- reduce user confusion.

They MUST NOT be the authoritative control for:

- reading protected data;
- mutation;
- role change;
- tenant access;
- privileged action.

# Frontend Permission Example

Valid:

```ts
if (!permissions.canManageSubscription) {
  return null
}
```

for UX.

Still required:

```text
backend verifies canManageSubscription/resource ownership
```

on every protected operation.

# Route Guards

A protected frontend route:

```text
/admin
```

is UX/navigation control.

Users can call backend endpoints directly.

Do not classify route guards as server access control.

# Client-Controlled Role

Never trust:

```text
localStorage.role
query role
hidden form field
Redux user.isAdmin
```

as authoritative privilege.

# Multi-Tenant Frontend

Review accidental disclosure in:

- cached queries;
- local persistence;
- route preload;
- stale tenant data;
- optimistic state;
- client search index.

But authoritative tenant isolation belongs to backend/server.

# Cache Keys

Server-state cache keys should include security-relevant identity/tenant dimensions where data differs.

Example risk:

```text
["subscription", id]
```

may be insufficient if same client session switches tenant contexts and identifier semantics do not guarantee isolation.

Do not use client cache correctness as a substitute for server authorization.

# Redirect Handling

Roadmap evaluation:

```text
redirect handling
```

Review:

```text
next
returnTo
redirect
callbackUrl
continue
location
```

from URL/API/storage.

# Open Redirect

Dangerous pattern:

```ts
window.location.assign(searchParams.get("next"))
```

without destination policy.

Potential impact:

- phishing;
- auth-flow abuse;
- trust-domain confusion;
- token/code leakage depending on flow.

# Safe Redirect Policy

Prefer:

```text
relative internal paths
```

or explicit allowed origins/routes.

Normalize/parse URLs structurally.

Do not rely only on:

```text
startsWith("https://trusted.com")
```

because host confusion/encoding can defeat simplistic checks.

# Protocol-Relative URLs

Consider:

```text
//evil.example
```

when only relative same-origin redirects are allowed.

# OAuth/OIDC Redirects

Do not modify provider redirect rules ad hoc.

Review exact approved redirect URI/callback handling and state/nonce/PKCE ownership where applicable.

Use `reviewing-application-security` for broad auth taxonomy.

# Reverse Tabnabbing

For links opening new tabs, follow framework/browser conventions for opener isolation where applicable.

Do not blindly add attributes when modern framework/browser behavior already handles it; inspect actual result.

# File Upload

Roadmap evaluation:

```text
file upload
```

Frontend validation is UX and early rejection.

Server must revalidate.

Review frontend:

- accepted extensions/types;
- size checks;
- preview;
- object URLs;
- parsing;
- EXIF/metadata;
- filename display;
- drag/drop;
- SVG/HTML preview;
- archive handling;
- upload endpoint;
- progress/retry;
- error messages.

# File Input Trust

Browser-provided:

```text
file.name
file.type
extension
```

are not authoritative security validation.

Server/storage pipeline must enforce accepted content policy.

# Client File Preview

High-risk previews:

```text
raw SVG
HTML
PDF viewer plugins
rich document
```

may introduce active content/sandbox issues.

Use safe rendering/sandboxing strategy.

# Object URLs

If using:

```text
URL.createObjectURL
```

revoke when no longer needed to avoid resource retention.

This is usually performance/resource hygiene, but can matter for sensitive file lifetime.

# File Names

Do not insert filenames into unsafe HTML.

Render as text.

Do not derive trusted storage path directly from client filename.

# Oversized Files

Frontend size check improves UX but server must enforce request/object/parser limits.

DoS/security authority remains server-side/infrastructure.

# Upload Progress

Avoid logging file content or secret upload URLs.

# Third-Party Script

Roadmap evaluation:

```text
third-party script
```

A runtime script executes with page privileges unless isolated.

Review:

```text
why needed
who controls origin
version/change policy
data it can read
DOM access
cookies/browser storage
network calls
consent
CSP
SRI where applicable
sandbox/iframe isolation
failure behavior
supply-chain ownership
```

# Dynamic Script Injection

Pattern:

```ts
const script = document.createElement("script")
script.src = providerUrl
document.head.appendChild(script)
```

requires destination/source governance.

Never allow arbitrary user-controlled script URL.

# Script Trust

A third-party script can often access:

- DOM;
- JS-readable tokens;
- localStorage;
- page content;
- forms;
- user identifiers.

This increases the importance of minimizing browser-readable secrets/tokens.

# Tag Managers

Tag managers can become code-execution control planes.

Review:

- publisher permissions;
- approval/change control;
- consent;
- script allowlists;
- environments;
- audit.

Privacy-specific behavior goes to `reviewing-frontend-privacy-and-analytics`.

# Subresource Integrity

SRI may help for static third-party resources where deployment model supports stable hashes.

Do not require SRI for dynamically versioned provider SDKs where incompatible; use CSP/version governance/isolated integration instead.

# Third-Party Iframes

Iframe isolation can reduce privileges.

Review:

```text
sandbox
allow
origin
postMessage
frame-ancestors
credential behavior
```

# postMessage

Review:

```text
targetOrigin
event.origin
event.source
message schema
privileged action
```

Avoid:

```ts
window.postMessage(data, "*")
```

for sensitive flows unless broadcasting to any origin is intentionally harmless.

Receiver must verify origin and message shape before privileged actions.

# Dependency Risks

Roadmap purpose includes dependency risks.

This frontend skill reviews runtime/browser impact:

- malicious or compromised package;
- large third-party script privilege;
- unsafe package API;
- abandoned package handling sensitive HTML;
- package executing install/build code;
- direct CDN script.

Use generic application-security/supply-chain review for taxonomy.

Do not duplicate dependency-CVE tooling here.

# Package Typosquatting

Use lockfiles/trusted registries/review process and supply-chain tooling.

Do not infer compromise solely from package age.

# Browser Extensions

Do not design security assuming browser extensions are trusted.

But ordinary malicious extensions are usually outside application threat boundaries unless product policy includes them.

# Clickjacking

Where sensitive actions are embedded, frame protection may be relevant:

```text
CSP frame-ancestors
X-Frame-Options legacy support if required
```

This is often deployment/header evidence, so hand to control verification.

# Iframes

Review whether app or sensitive pages may be embedded by untrusted origins.

# CSRF

Frontend security review should understand actual auth model.

If cookies provide ambient auth for state-changing requests, CSRF controls matter.

Do not treat adding an `Authorization` header from JS as a generic solution if it creates worse token exposure.

Use application-security review for detailed classification.

# CORS

CORS does not protect backend authorization.

A server can be called outside browser constraints.

Review frontend assumptions but server security owns authorization.

# Cookies

Frontend JS cannot inspect HttpOnly cookies, which is desirable for session secrecy.

Do not attempt to read them through client code.

# Browser Storage

Treat stored data as user-controlled on read.

For integrity-sensitive client preferences/state:

```text
parse
runtime validate
use safe defaults
```

Do not trust localStorage DTO shape because your own code wrote it previously.

# IndexedDB

Same trust principle:

```text
browser-local state
≠
trusted server truth
```

Sensitive cached server data should follow product privacy/security policy and logout/tenant-switch cleanup requirements.

# Logout

Review whether logout clears:

- sensitive browser caches;
- client state;
- storage owned by app;
- query caches;
- worker state.

But server-side session/token revocation remains server concern.

# Shared Device

Persistent sensitive browser data can remain after logout.

Assess according to product/user environment.

# Clipboard

Avoid silently copying secrets.

If copying sensitive values is a real feature, provide explicit user intent and minimize retention/exposure.

# Downloads

For downloads:

- backend authorization;
- content type;
- safe filename;
- Content-Disposition;
- signed URL scope/expiry where used.

Frontend cannot make an unauthorized resource safe by hiding link.

# URL / Referrer Leakage

Do not put secrets/sensitive identifiers unnecessarily in URL.

Review navigation to third-party origins if current URL may contain sensitive query/path data.

Referrer policy is a defense mechanism; verify deployment/browser behavior via control verification.

# Browser History

Sensitive query/path values may persist in history.

Prefer server/session state or non-sensitive opaque navigation state when appropriate.

# Service Workers

Service workers are highly privileged within scope.

Review:

- registration origin/scope;
- cached sensitive responses;
- update behavior;
- offline auth assumptions;
- message validation.

Do not cache authenticated sensitive data indiscriminately.

# PWA Offline State

Offline copies may outlive session.

Review tenant/user logout cleanup and data sensitivity.

# Web Workers

Workers do not provide a security boundary against same-origin application code.

Do not place secrets there expecting secrecy.

# WebAssembly

WASM is not inherently safer for secrets or untrusted code.

Treat browser-shipped data/credentials as observable.

# Client Encryption

Encrypting data in browser does not hide it from a user who also receives the key.

Use cryptography according to a real threat model.

Do not implement “frontend encryption” as secret obfuscation.

# Environment Separation

Ensure frontend cannot accidentally point production users to:

- staging auth;
- test payment;
- internal endpoints;
- privileged debug APIs.

Misconfiguration classification goes to application-security review.

# Debug Features

Remove/guard:

- dev consoles exposing secrets;
- admin debug panels backed only by frontend flag;
- raw provider payload viewers;
- stack traces.

A build-time feature flag is observable, not authorization.

# Feature Flags

Frontend feature flags control UX rollout, not security.

Backend must enforce capabilities independently.

# Source of Permission Data

Permission data returned by server may guide UI.

Still, malicious users can alter it locally.

Do not let client permission state alter backend authority.

# Error Telemetry

Security-review concern:

- tokens/secrets;
- headers;
- raw request bodies;
- DOM snapshots with sensitive data.

Privacy/retention goes to privacy skill.

# Console Logging

Production console logs may expose identifiers/tokens/debug context.

Use structured safe logging or remove sensitive debug logs.

# Analytics SDKs

From security perspective, third-party SDK is runtime code/data boundary.

From privacy perspective, consent/PII/event policy belongs to `reviewing-frontend-privacy-and-analytics`.

# CSP Nonce

If application uses nonces/hashes, verify that client behavior does not undermine them with broad `unsafe-inline`/`unsafe-eval`.

Configuration evidence should be gathered through control verification.

# Security Headers

Potential:

```text
Content-Security-Policy
frame-ancestors
Referrer-Policy
Permissions-Policy
Strict-Transport-Security
X-Content-Type-Options
```

Not every header is frontend code responsibility.

Avoid generic “missing header” findings without risk context.

# Dependency on Backend Security

For every frontend security check distinguish:

```text
UX/browser defense
```

from:

```text
authoritative backend control
```

Examples:

```text
frontend file size check
→ UX

backend file size/content/parser limit
→ security authority
```

```text
frontend route guard
→ UX

backend authorization
→ security authority
```

# Finding Format

For each finding record:

```text
ID
surface
browser source
sink/storage/action
attacker control
preconditions
exploit path
impact
frontend mitigation
required backend/infra mitigation
application-security classification handoff
verification evidence
```

# Statuses

Use:

```text
CONFIRMED
LIKELY_REQUIRES_VALIDATION
DEFENSE_IN_DEPTH
FALSE_POSITIVE
NOT_APPLICABLE
```

# Severity

Do not invent a frontend-only severity scheme.

Use `reviewing-application-security` severity logic when a real vulnerability is confirmed.

# Roadmap Evaluation — dangerouslySetInnerHTML

Pass review only if:

- source/trust known;
- sanitizer or constant-trust proof exists where needed;
- context is appropriate;
- no post-sanitization unsafe mutation;
- tests/verification exist for attacker content when applicable.

# Roadmap Evaluation — localStorage token

Pass review only if:

- token type/lifetime/scope understood;
- storage choice justified by architecture;
- XSS/third-party exposure considered;
- long-lived high-value bearer credentials are not persisted without explicit accepted risk/control model.

# Roadmap Evaluation — secret environment variable

Pass review only if:

- client-exposed values are intended public identifiers/config;
- true secrets remain server-side;
- bundle/runtime config evidence confirms no secret shipping.

# Roadmap Evaluation — redirect handling

Pass review only if:

- untrusted destination inputs use internal-relative or explicit allowlist policy;
- structural URL parsing/normalization is used;
- dangerous external/scheme cases have negative tests.

# Roadmap Evaluation — file upload

Pass review only if:

- frontend validation is treated as UX;
- preview is safe;
- filename rendered safely;
- no active-content preview issue;
- server-side type/size/content/storage/auth resource controls are confirmed or handed off.

# Roadmap Evaluation — third-party script

Pass review only if:

- script origin/purpose/privilege are known;
- user data/credentials accessible to it are understood;
- load/change/isolation/CSP strategy is explicit;
- arbitrary/user-controlled script injection is impossible;
- privacy policy is handed off where relevant.

# Application Security Handoff

When confirmed:

```text
frontend source/sink weakness
→ reviewing-application-security
→ OWASP/CWE/severity/root cause
```

Examples:

```text
DOM XSS
→ likely CWE-79 / OWASP Injection classification as supported

browser secret exposure
→ sensitive information exposure classification

open redirect
→ precise CWE if applicable

frontend-only authorization relied upon
→ Broken Access Control root cause in server/application design
```

Do not guess mappings locally if precise review is needed.

# STRIDE Handoff

Use threat modeling when frontend changes introduce:

- new cross-origin flow;
- new iframe;
- new provider;
- new auth flow;
- new trust boundary;
- privileged browser capability.

# ASVS / Control Handoff

Use `verifying-security-controls` for evidence such as:

- CSP/header config;
- session cookie settings;
- authorization negative tests;
- secret absence in client bundle;
- redirect rejection;
- upload limits;
- webhook/provider controls.

# Security Testing

Potential browser-level tests:

```text
malicious HTML fixture
dangerous URL rejection
external redirect rejection
wrong-tenant UI data-cache isolation
logout cache cleanup
file preview malicious SVG rejection
postMessage wrong-origin rejection
```

Keep tests at lowest useful boundary.

# Browser E2E Security Test

Use E2E when browser integration is itself the control:

- CSP behavior;
- redirect navigation;
- cookie/session behavior;
- iframe/postMessage;
- file preview.

Do not move all security testing to E2E.

# Static Analysis

Lint/SAST may identify:

- unsafe HTML sinks;
- eval;
- insecure URL handling;
- secret references;
- risky dependency usage.

Validate manually.

# False Positive Example

```jsx
<div dangerouslySetInnerHTML={{ __html: STATIC_BUILD_GENERATED_TRUSTED_HTML }} />
```

may be acceptable if input cannot be attacker-controlled and trust is demonstrated.

Do not suppress blindly; document source provenance.

# True Positive Example

```jsx
<div dangerouslySetInnerHTML={{ __html: searchParams.get("bio") ?? "" }} />
```

is a strong XSS candidate.

# Redirect Example

Bad:

```ts
window.location.href = new URLSearchParams(location.search).get("next")!
```

Better pattern:

```text
parse
→ require same-origin/internal relative route
→ navigate
```

# Token Example

Bad:

```ts
localStorage.setItem("refreshToken", token)
```

for a long-lived high-value bearer token without an explicitly accepted architecture.

Mitigation may require backend/session redesign rather than a frontend-only patch.

# Secret Example

Bad:

```ts
const webhookSecret = import.meta.env.VITE_PROVIDER_WEBHOOK_SECRET
```

if used by browser bundle.

A webhook secret belongs to trusted server boundary.

# Upload Example

Bad:

```text
accept=".svg"
→ render uploaded SVG directly into same-origin DOM
```

without safe isolation/content policy.

# Third-Party Example

Bad:

```ts
loadScript(searchParams.get("sdk"))
```

because an attacker controls executable origin.

# Authorization Example

Bad:

```ts
if (user.isAdmin) {
  fetch(`/admin/delete/${id}`, { method: "DELETE" })
}
```

when backend endpoint does not enforce authorization.

Fix must be backend authoritative.

# Over-Review Audit

Flag:

- every environment variable called secret;
- every `dangerouslySetInnerHTML` called XSS;
- every localStorage value called critical;
- every dependency called supply-chain vulnerability;
- generic security-header checklist without threat context;
- server findings duplicated wholesale.

Use:

```text
PROPORTIONATE_FRONTEND_SECURITY_REVIEW
OVERCLASSIFIED_FRONTEND_RISK
FRONTEND_SECURITY_REVIEW_TOO_GENERIC
```

# Under-Review Audit

Flag:

- route guard treated as auth;
- refresh token in localStorage ignored;
- client secret shipped;
- untrusted redirect;
- raw user HTML;
- unsafe third-party script;
- active file preview;
- sensitive hydration payload;
- postMessage wildcard on privileged flow.

# Final Decision

Use:

```text
FRONTEND_SECURITY_ACCEPTABLE
FRONTEND_SECURITY_ACCEPTABLE_WITH_CONDITIONS
FRONTEND_SECURITY_REMEDIATION_REQUIRED
APPLICATION_SECURITY_CLASSIFICATION_REQUIRED
SERVER_AUTHORIZATION_REMEDIATION_REQUIRED
SECURITY_CONTROL_VERIFICATION_REQUIRED
THREAT_MODEL_UPDATE_REQUIRED
FRONTEND_SECURITY_EVIDENCE_REQUIRED
BLOCKED
```

## Output

Use `assets/frontend-security-review-record.md`.

## Completion Criteria

- [ ] Frontend/browser scope is explicit.
- [ ] Client data/config is treated as user-observable/modifiable.
- [ ] UX permission checks are distinguished from authoritative server authorization.
- [ ] `dangerouslySetInnerHTML` and other HTML sinks are traced from source to sink.
- [ ] XSS findings require attacker control + unsafe rendering context.
- [ ] Established sanitizer configuration/context is inspected before confirming XSS.
- [ ] Client-side secrets/environment variables are differentiated from intentionally public config.
- [ ] No true secret is shipped in browser bundle/runtime config.
- [ ] Token/session storage is reviewed with type/lifetime/scope/XSS/CSRF model.
- [ ] Long-lived high-value bearer tokens in localStorage receive explicit risk analysis.
- [ ] Tokens/secrets are absent from browser logs/telemetry.
- [ ] Sensitive SSR/hydration/browser-storage data is reviewed.
- [ ] Redirect inputs use safe structural destination policy.
- [ ] Dangerous schemes/external redirect cases are tested where applicable.
- [ ] File upload frontend checks are treated as UX, not authoritative validation.
- [ ] File preview/active-content risks are reviewed.
- [ ] Server upload/content/size/storage/auth controls are verified or handed off.
- [ ] Third-party runtime scripts are reviewed for origin, privilege, data access, change control, CSP/isolation.
- [ ] Arbitrary user-controlled script URLs are prohibited.
- [ ] postMessage/iframe boundaries are reviewed where applicable.
- [ ] Browser storage data is treated as untrusted input on read.
- [ ] Tenant/user cache cleanup/isolation is reviewed where applicable.
- [ ] CSP/security headers are treated as defense/config controls rather than root XSS fixes.
- [ ] Scanner/lint findings are validated before confirmation.
- [ ] OWASP/CWE classification is delegated to `reviewing-application-security`.
- [ ] ASVS/control evidence is delegated to `verifying-security-controls`.
- [ ] New trust boundaries invoke `threat-modeling-with-stride` when needed.
- [ ] Findings identify required backend/infra remediation when frontend cannot provide authority.
- [ ] Roadmap evaluations are covered: dangerouslySetInnerHTML, localStorage token, secret environment variable, redirect handling, file upload, third-party script.
- [ ] Final frontend-security status is explicit.
