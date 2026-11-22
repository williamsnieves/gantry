---
name: threat-modeling-with-stride
description: Performs architecture-level threat modeling using STRIDE before or during system design. Use when a frontend, backend, API, identity flow, infrastructure boundary, storage layer, asynchronous workflow, third-party integration, or full-stack feature needs systematic threat discovery. Identify assets, actors, entry points, trust boundaries, data flows, privileges, and abuse paths; then analyze Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, and Elevation of Privilege threats and derive concrete mitigations, residual risk, verification evidence, and ownership. Do not use STRIDE as a flat checklist detached from actual data flows, invent threats without a plausible path, or treat mitigations as implemented until evidence exists.
---

# Threat Modeling with STRIDE

## Purpose

Discover plausible security threats from architecture and data-flow design.

```text
system scope
→ assets
→ actors
→ entry points
→ data flows
→ trust boundaries
→ privileges
→ STRIDE threat discovery
→ attack paths
→ mitigations
→ residual risk
→ verification plan
```

This skill is design-oriented. It asks:

```text
How could this architecture be abused or crossed incorrectly?
```

Implementation-level weakness review belongs to `reviewing-application-security`; control verification belongs to `verifying-security-controls`.

## Use When

- Designing a security-relevant frontend, backend, API, identity, storage, provider, or infrastructure flow.
- Reviewing authentication/session architecture.
- Designing authorization or multi-tenant boundaries.
- Introducing a public API, webhook, file flow, queue, or privileged operation.
- Adding sensitive/business-critical data storage.
- Integrating a third-party provider.
- Reviewing CI/CD, IAM, secrets, deployment, or network boundaries.
- Preparing security requirements before implementation.
- Reconstructing attack paths after an incident.

## Do Not Use When

- The task is only code-level vulnerability scanning.
- The task is verifying implemented controls against ASVS.
- The task is dependency vulnerability scanning.
- The user only wants OWASP/CWE classification of an implemented finding.
- The scope/data flow is unknown and cannot be reconstructed.

## Inputs

- System/feature scope.
- Architecture/data-flow description.
- Actors and roles.
- Assets and data classification.
- Entry points.
- Trust boundaries.
- Authentication/session model.
- Authorization/resource ownership model.
- Storage/persistence.
- External providers/webhooks.
- Infrastructure/network/IAM/deployment.
- Existing controls and security assumptions.
- Logging/audit model.
- Availability/resource requirements.
- Applicable `AGENTS.md`.

## Outputs

- Threat-model scope.
- Asset/actor/entry-point inventories.
- Trust-boundary and data-flow map.
- Privilege inventory.
- STRIDE threat inventory.
- Attack paths and preconditions.
- Severity/prioritization.
- Concrete mitigations.
- Security requirements.
- Verification plan.
- Residual risk and ownership.
- STRIDE threat-model record.

## STRIDE Categories

```text
S — Spoofing
T — Tampering
R — Repudiation
I — Information Disclosure
D — Denial of Service
E — Elevation of Privilege
```

Do not mechanically force all six categories onto every component. Record a threat only when there is a plausible path.

## Core Model

Analyze:

```text
actor
→ entry point
→ trust boundary
→ data/process/store
→ privileged effect
```

Threats emerge from how these pieces interact.

## Readiness Gate

Use one:

```text
READY_TO_MODEL_THREATS
READY_WITH_CONDITIONS
THREAT_MODEL_NOT_REQUIRED
ARCHITECTURE_DETAIL_REQUIRED
TRUST_BOUNDARY_REQUIRED
AUTHORIZATION_MODEL_REQUIRED
THIRD_PARTY_SECURITY_DECISION_REQUIRED
ALGORITHMIC_DOS_ANALYSIS_REQUIRED
BLOCKED
```

## Scope

Define exactly:

- feature/system;
- environments;
- included components;
- excluded components;
- actors/roles;
- external dependencies;
- critical journeys;
- sensitive/business-critical assets.

Do not imply the whole platform was reviewed if only one feature was modeled.

## Assets

Assets may include:

```text
identity
session
credentials
tokens
personal data
payment data
business records
entitlements
configuration
secrets
audit history
source/build artifacts
deployment credentials
availability
tenant boundaries
command integrity
```

For each asset record owner, sensitivity, integrity need, availability need, where it is stored/transmitted, and who may access it.

## Actors and Privileges

Possible actors:

```text
anonymous user
authenticated user
tenant admin
system admin
support operator
backend service
service account
third-party provider
CI/CD identity
automation
attacker
```

Do not conflate authenticated with authorized.

Record meaningful capabilities:

```text
read
write
delete
approve
refund
impersonate
configure
deploy
rotate secret
grant role
cross-tenant access
```

## Entry Points

Examples:

```text
web route
API endpoint
GraphQL operation
webhook
queue consumer
file upload
admin console
CLI
scheduled job
OAuth callback
browser storage
cloud control plane
```

## Trust Boundaries

A trust boundary exists where assumptions or authority change.

Examples:

```text
browser ↔ backend
public internet ↔ edge
service ↔ service
tenant ↔ tenant
application ↔ provider
CI ↔ cloud
application ↔ database
developer machine ↔ production
```

Every relevant boundary-crossing flow must be explicit.

## Data Flows

For each flow record:

```text
source
destination
data
protocol/channel
authentication
authorization
validation
integrity
confidentiality
logging
failure behavior
```

## Security Assumptions

Record assumptions such as:

```text
TLS terminates at trusted edge
backend verifies issuer/audience
resource tenant is derived from verified identity
webhook signatures are validated
service account is least privilege
```

For each assumption ask:

```text
Who guarantees it?
Where is it enforced?
How is it verified?
What happens if it is false?
```

An unverified assumption is a risk, not a verified control.

# STRIDE Analysis

## Spoofing

Question:

```text
Can an attacker pretend to be another actor or system?
```

Analyze where relevant:

- stolen/replayed session;
- forged identity claims;
- weak API authentication;
- webhook sender spoofing;
- service identity spoofing;
- OAuth callback abuse;
- impersonation;
- credential misuse.

Potential mitigations include strong authentication, signature verification, anti-replay controls, verified issuer/audience, short-lived credentials, and scoped service identity.

Do not reduce Spoofing to “use MFA” generically.

## Tampering

Question:

```text
Can data, commands, artifacts, or configuration be altered without authorization?
```

Analyze:

- request/body/tenant/resource manipulation;
- modified client state;
- unsigned provider events;
- file/content tampering;
- queue/event modification;
- cache poisoning;
- artifact/IaC/config mutation.

Prefer trusted-boundary authorization, runtime validation, integrity controls, artifact provenance, least privilege, and transactional checks as appropriate.

## Repudiation

Question:

```text
Can an actor deny a security-relevant action?
```

Focus on privileged or consequential actions:

- role/permission changes;
- deletion;
- payment/refund;
- impersonation;
- security settings;
- secret rotation;
- deployment.

Security audit evidence should capture the actor, action, target/resource, time, and correlation context without logging secrets unnecessarily.

## Information Disclosure

Question:

```text
Can sensitive information reach an unauthorized actor?
```

Analyze:

- cross-tenant reads;
- excessive API responses;
- browser-delivered secrets;
- logs/analytics;
- source maps;
- error messages;
- caches;
- pre-signed URLs;
- backups;
- third-party scripts/providers;
- browser storage.

Mitigations may include authorization, data minimization, response projection, secret segregation, redaction, cache controls, scoped URLs, and browser/security-policy controls.

## Denial of Service

Question:

```text
Can input, traffic, dependency failure, or retry behavior exhaust a resource or availability target?
```

Analyze:

- unbounded upload;
- expensive parser/search/filter;
- regex backtracking;
- graph expansion;
- queue flood;
- retry storm;
- cache stampede;
- memory/resource leak;
- provider exhaustion;
- browser-main-thread abuse where in scope.

Potential mitigations include rate limits, quotas, size limits, timeouts, circuit breakers, backpressure, pagination, resource budgets, bounded parsing, caching, and load shedding.

If computational growth itself is important, invoke `analyzing-algorithmic-complexity`.

## Elevation of Privilege

Question:

```text
Can an actor gain a capability they should not have?
```

Analyze:

- missing role/capability checks;
- tenant/resource ownership bypass;
- client-controlled role/tenant;
- insecure support impersonation;
- overprivileged service/CI identity;
- workflow escalation;
- admin actions reachable by ordinary users.

Prefer server-side authorization, least privilege, capability/resource checks, scoped IAM, separation of duties when policy requires it, and short-lived credentials.

# Threat-to-Element Guidance

Useful guidance, not a rigid matrix:

```text
External Entity
→ Spoofing, Repudiation

Process
→ all STRIDE categories may apply

Data Flow
→ Tampering, Information Disclosure, DoS

Data Store
→ Tampering, Repudiation, Information Disclosure, DoS

Trust Boundary
→ review all relevant categories crossing it
```

# Threat Statement Format

Write:

```text
[Actor] can [action] against [asset/component]
through [entry point/data flow]
because [missing/weak trust assumption/control],
causing [impact].
```

Example:

```text
An authenticated tenant user can alter orgId in the request
and update another tenant's subscription because authorization
checks only the user role, not tenant/resource ownership,
causing cross-tenant tampering and privilege escalation.
```

# Plausibility and Preconditions

Use:

```text
PLAUSIBLE
CONDITIONAL
THEORETICAL_LOW_RELEVANCE
NOT_APPLICABLE
```

Record preconditions such as authentication, network access, tenant membership, knowledge of an identifier, provider compromise, or admin privilege.

Avoid fantasy threats disconnected from the architecture.

# Existing Controls

Record controls such as:

```text
authentication
authorization
runtime validation
signature verification
encryption
rate limiting
CSP
WAF
IAM
security audit logging
secret management
network policy
```

Use control status:

```text
IMPLEMENTED_VERIFIED
IMPLEMENTED_NOT_VERIFIED
PLANNED
PARTIAL
MISSING
NOT_APPLICABLE
```

A backlog item is not a verified mitigation.

# Multi-Tenant Systems

Always examine:

```text
tenant identifier source
resource ownership
shared cache keying
shared storage
search/index filtering
exports
logs/analytics
background jobs
support/admin access
```

Do not accept UUID unpredictability as an authorization mechanism.

# Authentication Flow

Trace:

```text
credential/IdP
→ callback
→ session/token
→ browser/cookie/storage
→ backend verification
→ refresh
→ logout
```

Analyze spoofing, replay, redirect/callback abuse, token disclosure, fixation, refresh, and logout invalidation where relevant.

# Authorization Flow

Trace:

```text
actor
→ verified identity
→ role/capability
→ tenant/resource
→ operation
→ policy decision
```

Ask:

```text
Where is authorization enforced?
What determines resource ownership?
Can the client alter that input?
```

Critical authorization MUST be enforced at a trusted server/service boundary.

# Webhooks

Trace:

```text
provider
→ public webhook
→ sender/signature verification
→ replay/idempotency
→ business handler
```

Analyze Spoofing, Tampering, Repudiation, replay/duplicate processing, and DoS/flooding.

IP allowlists may be defense in depth but are not automatically sufficient sender authentication.

# File Upload / Download

Trace:

```text
browser
→ upload endpoint
→ validation
→ object storage
→ processing
→ display/download
```

Review:

- size limits;
- content type vs actual content;
- path/key manipulation;
- ACL/public exposure;
- malicious content;
- parser exploit;
- stored XSS/content serving;
- metadata disclosure;
- decompression/resource bombs;
- download authorization.

# Third-Party Providers

For each provider record:

```text
data sent
data received
credentials/scopes
callbacks/webhooks
retention
availability dependency
permissions
incident boundary
```

Do not treat the provider as automatically trusted.

# Browser / Frontend Boundary

Review architecture-level exposure to:

- XSS/DOM injection surfaces;
- token/session storage;
- redirects;
- third-party scripts;
- CSP;
- `postMessage`/iframe boundaries;
- URL/referrer disclosure;
- client-only authorization assumptions.

Detailed implementation review belongs to `reviewing-frontend-security`.

# Infrastructure and IAM

Review:

- public/private network boundaries;
- ingress/egress;
- service identities;
- cloud IAM;
- object/storage exposure;
- secrets;
- admin/bastion pathways;
- backup access;
- control-plane permissions.

# CI/CD and Supply Chain

Assets include:

```text
source
build artifacts
registry credentials
signing credentials
cloud deploy credentials
secrets
package registry
```

Threats include malicious build steps, dependency/artifact tampering, secret exfiltration, overprivileged runners, untrusted fork access, and deploy identity abuse.

# Secrets

Model:

```text
origin
storage
who can read
injection point
logging
scope
rotation
expiry
```

A secret compiled or delivered into browser JavaScript is no longer secret from the browser user.

# Availability and Algorithmic DoS

Define what resource can be exhausted and what input controls the cost.

Examples:

```text
regex
parser
graph traversal
search
sorting
compression
file processing
```

When attacker-controlled input creates non-linear growth, hand off to `analyzing-algorithmic-complexity` and the relevant security-review skill.

# Threat Chaining

Record important chains:

```text
Spoofing
→ compromised service identity
→ Tampering
→ altered artifact/config
→ Elevation of Privilege
```

Prioritize root leverage rather than duplicating every stage as disconnected findings.

# Mitigations

A good mitigation is:

- rooted in the attack path;
- enforceable at the correct trust boundary;
- owned;
- testable;
- proportional;
- explicit about failure behavior.

Weak:

```text
sanitize input
be careful
add security
```

# Security Requirements

Convert material mitigations into testable requirements.

Example:

```text
The backend MUST verify that the target subscription belongs to an organization
the authenticated actor is authorized to administer before applying the update.
```

Do not invent legal/compliance requirements.

# Verification Plan

Choose the lowest reliable boundary:

```text
unit/domain test
application test
adapter/integration test
security negative test
E2E
manual architecture/code review
configuration/IAM evidence
security audit-log verification
penetration test
```

Do not use E2E for every security property.

# Residual Risk

Use:

```text
ACCEPTED
TRANSFERRED
REDUCED
UNRESOLVED
UNKNOWN
```

Accepted risk needs an owner and rationale.

# Threat Lifecycle

Use:

```text
OPEN
MITIGATION_PLANNED
PARTIALLY_MITIGATED
MITIGATED_PENDING_VERIFICATION
VERIFIED
ACCEPTED_RISK
NOT_APPLICABLE
```

# Relationship to OWASP, CWE, and ASVS

```text
STRIDE
→ discover architecture threats

OWASP Top 10
→ classify broad application-risk categories

CWE
→ classify concrete implementation weaknesses/root causes

ASVS
→ verify security requirements/controls
```

Do not force CWE IDs during architecture-only threat discovery when no concrete weakness has been established.

Recommended pipeline:

```text
threat-modeling-with-stride
→ security requirements / mitigations

implementation

reviewing-application-security
→ concrete OWASP/CWE findings

verifying-security-controls
→ ASVS/control evidence
```

# Threat Inventory Structure

Each material threat should include:

```text
ID
STRIDE category/categories
asset
actor
entry point
trust boundary
preconditions
attack path
impact
existing controls
control status
severity
mitigation
owner
verification
residual risk
```

Use stable IDs such as:

```text
THREAT-001
THREAT-002
```

# Severity

Use:

```text
CRITICAL
HIGH
MEDIUM
LOW
ADVISORY
```

Consider impact, exposure, exploitability/plausibility, privilege gained, cross-tenant blast radius, data sensitivity, availability impact, reversibility, and existing verified controls.

Do not assign severity solely from STRIDE category.

# Duplicate Threats

Different STRIDE labels may describe one root attack path.

Prefer one finding with multiple applicable STRIDE categories when root cause and mitigation are shared.

# Attack Surface Reduction

Prefer removing unnecessary exposure where feasible:

```text
remove public endpoint
remove unused provider scope
remove browser-delivered secret
eliminate privileged client capability
reduce IAM permissions
```

rather than piling compensating controls onto unnecessary surface area.

# Fail Securely

Security-control failure should default to safe behavior for critical operations:

```text
deny
rollback
avoid partial privileged mutation
avoid secret disclosure
```

Do not default to permissive behavior when a control cannot evaluate safely.

# Over-Threating Audit

Flag:

- forcing every STRIDE category onto every component;
- implausible attacker powers;
- generic “could be hacked” statements;
- duplicate threats with one root cause;
- mitigations unrelated to a flow;
- dozens of low-value theoretical items hiding critical threats.

Use:

```text
PROPORTIONATE_THREAT_MODEL
OVERMODELED_THREATS
THREAT_MODEL_TOO_GENERIC
THREAT_MODEL_INCOMPLETE
```

# Under-Threating Audit

Flag:

- missing trust boundaries;
- missing tenant/resource ownership;
- missing privileged operations;
- missing provider/webhook/file flows;
- missing availability/resource limits;
- missing secrets/IAM/CI boundaries;
- trusting frontend controls as security enforcement.

# Final Decision

Use:

```text
THREAT_MODEL_READY
THREAT_MODEL_READY_WITH_CONDITIONS
SECURITY_REQUIREMENTS_REQUIRED
ARCHITECTURE_DETAIL_REQUIRED
TRUST_BOUNDARY_REQUIRED
AUTHORIZATION_MODEL_REQUIRED
THIRD_PARTY_SECURITY_DECISION_REQUIRED
ALGORITHMIC_DOS_ANALYSIS_REQUIRED
THREAT_MODEL_REVIEW_REQUIRED
BLOCKED
```

## Output

Use `assets/stride-threat-model-record.md`.

## Completion Criteria

- [ ] Scope is explicit.
- [ ] Assets are inventoried and prioritized.
- [ ] Actors/roles are explicit.
- [ ] Entry points are identified.
- [ ] Trust boundaries are identified.
- [ ] Data flows are explicit.
- [ ] Privileges/capabilities are explicit.
- [ ] Critical assumptions are documented and verifiable.
- [ ] STRIDE is applied to actual flows/elements, not as a flat checklist.
- [ ] Spoofing is assessed where identity crosses boundaries.
- [ ] Tampering is assessed where commands/data cross boundaries.
- [ ] Repudiation is assessed for material privileged actions.
- [ ] Information disclosure is assessed for sensitive data/stores/logs.
- [ ] DoS is assessed for public/resource-expensive paths.
- [ ] Elevation of privilege is assessed for roles/IAM/resource ownership.
- [ ] Multi-tenant boundaries are reviewed where applicable.
- [ ] Authentication/session flows are reviewed where applicable.
- [ ] Authorization/resource ownership is enforced at trusted boundaries.
- [ ] Third-party integrations are reviewed.
- [ ] Webhook/file/browser boundaries are reviewed when present.
- [ ] Infrastructure/IAM/CI/secrets are reviewed when in scope.
- [ ] Algorithmic DoS is handed to `analyzing-algorithmic-complexity` when relevant.
- [ ] Threats include plausible attack paths and preconditions.
- [ ] Existing controls and verification status are distinguished.
- [ ] Planned controls are not marked verified.
- [ ] Mitigations are concrete, owned, and testable.
- [ ] Client-side controls are not treated as authoritative authorization.
- [ ] Severity is evidence/path based rather than category based.
- [ ] Duplicate root-cause threats are consolidated.
- [ ] Residual risk and owners are explicit.
- [ ] Verification exists for every material mitigation.
- [ ] Final threat-model status is explicit.

## References

- Read `references/stride-categories-and-threat-statements.md` first.
- Read `references/assets-actors-trust-boundaries-and-data-flows.md`.
- Read `references/authentication-authorization-multitenancy-and-privilege.md`.
- Read `references/webhooks-files-third-parties-and-browser-boundaries.md`.
- Read `references/infrastructure-iam-cicd-secrets-and-supply-chain.md`.
- Read `references/dos-resource-exhaustion-and-algorithmic-complexity.md`.
- Read `references/mitigations-residual-risk-and-verification.md`.
- Read `references/stride-threat-model-audit.md` before completion.
