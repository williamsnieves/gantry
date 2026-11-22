---
name: reviewing-application-security
description: Reviews implemented application code and configuration for concrete security weaknesses across frontend, backend, APIs, integrations, jobs, and shared libraries. Use OWASP Top 10:2025 to classify broad application-security risk and MITRE CWE, prioritizing the current CWE Top 25:2025 when applicable, to identify concrete weakness/root-cause categories. Base findings on evidence and exploitability, not checklist matching; consolidate duplicate symptoms into root-cause findings; connect architecture threats from STRIDE when available; and hand verifiable control requirements to verifying-security-controls. Do not treat OWASP Top 10 as exhaustive, do not invent CWE mappings without a concrete weakness, do not use CWE/SANS rank as severity, and do not claim a control is effective without verification evidence.
...
---

# Reviewing Application Security

## Purpose

Review implemented application behavior for concrete security weaknesses.

Core workflow:

```text
implemented surface
→ attack surface
→ evidence
→ exploit path
→ concrete weakness
→ CWE mapping
→ OWASP risk classification
→ severity
→ remediation
→ verification
```

This skill is implementation-oriented.

It asks:

```text
What concrete security weakness exists in this implementation?
```

Architecture threat discovery belongs to:

```text
threat-modeling-with-stride
```

Control compliance/evidence belongs to:

```text
verifying-security-controls
```

## Security Knowledge Model

Use the standards for different purposes:

```text
STRIDE
→ threat discovery

OWASP Top 10:2025
→ broad application-risk classification

MITRE CWE
→ concrete weakness/root-cause classification

CWE Top 25:2025
→ prioritization awareness for common/high-impact weaknesses

OWASP ASVS 5.0.0
→ downstream verifiable control requirements
```

Do not flatten them into one checklist.

## Current Canonical Sources

At the time this skill was authored:

```text
OWASP Top 10:2025
CWE Top 25:2025
OWASP ASVS 5.0.0
```

SANS Top 25 material is complementary guidance around CWE, not a separate canonical weakness taxonomy.

When standards are updated, refresh reference metadata before changing mappings.

## OWASP Top 10:2025

Use these broad categories:

```text
A01 Broken Access Control
A02 Security Misconfiguration
A03 Software Supply Chain Failures
A04 Cryptographic Failures
A05 Injection
A06 Insecure Design
A07 Authentication Failures
A08 Software or Data Integrity Failures
A09 Security Logging and Alerting Failures
A10 Mishandling of Exceptional Conditions
```

A finding may map to more than one category, but select the primary risk category when possible.

## CWE Top 25:2025 Awareness

The current Top 25 includes high-priority weaknesses such as:

```text
CWE-79  Cross-site Scripting
CWE-89  SQL Injection
CWE-352 CSRF
CWE-862 Missing Authorization
CWE-787 Out-of-bounds Write
CWE-22  Path Traversal
CWE-416 Use After Free
CWE-125 Out-of-bounds Read
CWE-78  OS Command Injection
CWE-94  Code Injection
CWE-120 Classic Buffer Overflow
CWE-434 Dangerous File Upload
CWE-476 NULL Pointer Dereference
CWE-121 Stack-based Buffer Overflow
CWE-502 Deserialization of Untrusted Data
CWE-122 Heap-based Buffer Overflow
CWE-863 Incorrect Authorization
CWE-20  Improper Input Validation
CWE-284 Improper Access Control
CWE-200 Exposure of Sensitive Information
CWE-306 Missing Authentication for Critical Function
CWE-918 SSRF
CWE-77  Command Injection
CWE-639 Authorization Bypass Through User-Controlled Key
CWE-770 Allocation of Resources Without Limits or Throttling
```

Do not limit review to these 25.

A relevant CWE outside the Top 25 is still valid.

## Use When

- Reviewing implemented frontend security.
- Reviewing backend/API security.
- Reviewing authentication or authorization implementation.
- Reviewing multi-tenant access.
- Reviewing input/output handling.
- Reviewing injection/XSS risks.
- Reviewing uploads/downloads.
- Reviewing redirects/URL handling.
- Reviewing SSRF/external fetch behavior.
- Reviewing secrets/configuration.
- Reviewing cryptographic usage.
- Reviewing third-party scripts/dependencies.
- Reviewing webhooks/integrity.
- Reviewing deserialization/parsing.
- Reviewing exception/error handling.
- Reviewing logging/audit behavior.
- Reviewing resource exhaustion.
- Reviewing supply-chain/configuration risks.
- Turning STRIDE threats into implementation findings.

## Do Not Use When

- The system is still only architecture/design with no implementation.
- The task is solely ASVS control verification.
- The task is generic dependency-CVE scanning.
- The task is infrastructure-only configuration with no application boundary.
- The task is penetration testing against a live target without authorization.
- The user wants only theoretical OWASP education.
- There is no code/config/evidence to inspect.

## Inputs

- Code/configuration.
- Feature/application scope.
- Data-flow or architecture context.
- Threat model, if available.
- Authentication/authorization model.
- Runtime validation model.
- Error/result model.
- Secrets/configuration model.
- Upload/download behavior.
- Third-party integrations.
- Deployment/browser boundary.
- Existing security tests.
- Existing scanners/SAST/DAST findings.
- Applicable `AGENTS.md`.

## Outputs

- Security-review scope.
- Attack-surface inventory.
- Evidence-backed finding inventory.
- Exploit/precondition description.
- CWE mapping.
- OWASP Top 10 classification.
- Severity/priority.
- Remediation.
- Verification plan.
- Residual risk.
- Application-security review record.

# Evidence Gate

A confirmed finding requires:

```text
code/config evidence
+
plausible exploit or abuse path
+
security impact
```

Use statuses:

```text
CONFIRMED
LIKELY_REQUIRES_VALIDATION
DEFENSE_IN_DEPTH
FALSE_POSITIVE
NOT_APPLICABLE
```

Do not convert scanner output directly into confirmed findings.

# Finding Structure

Every material finding should contain:

```text
ID
title
status
severity
affected surface
preconditions
attack path
evidence
impact
primary CWE
related CWE(s)
primary OWASP category
related OWASP category/categories
STRIDE relation if available
root cause
remediation
verification
residual risk
owner
```

# Finding IDs

Use stable IDs:

```text
SEC-001
SEC-002
```

Do not encode severity or taxonomy into ID.

# Root Cause over Symptoms

Consolidate related symptoms where the root weakness is shared.

Example:

```text
GET /orgs/{org}/subscription/{id}
PATCH /orgs/{org}/subscription/{id}
DELETE /orgs/{org}/subscription/{id}
```

all trust user-controlled resource identifiers without ownership checks.

Prefer:

```text
SEC-004 Missing resource ownership authorization across subscription operations
```

rather than three duplicate findings, unless remediation/impact differs materially.

# CWE Mapping Rule

Map only when the concrete weakness supports it.

Examples:

```text
missing authorization
→ CWE-862

incorrect authorization
→ CWE-863

authorization bypass through user-controlled key
→ CWE-639

XSS
→ CWE-79

SQL injection
→ CWE-89

OS command injection
→ CWE-78

path traversal
→ CWE-22

dangerous file upload
→ CWE-434

SSRF
→ CWE-918

deserialization of untrusted data
→ CWE-502

sensitive information exposure
→ CWE-200

missing authentication
→ CWE-306

resource allocation without limits
→ CWE-770
```

Do not choose a CWE merely because its name resembles the symptom.

# Primary vs Related CWE

Select the most precise root cause as primary.

Related CWE may describe enabling/secondary weaknesses.

Example:

```text
tenant ID from URL accepted without ownership check

primary:
CWE-639 Authorization Bypass Through User-Controlled Key

related:
CWE-862 Missing Authorization
```

depending on implementation.

Do not create a long CWE list for appearance.

# CWE Rank Is Not Severity

A Top 25 rank measures ecosystem prevalence/impact methodology, not the severity of this specific finding.

Never write:

```text
CWE #4 → Critical
```

Severity depends on exploitability and impact in the actual system.

# OWASP Mapping Rule

OWASP category is a broad risk grouping.

Examples:

```text
missing ownership check
→ A01 Broken Access Control

unsafe default/public storage
→ A02 Security Misconfiguration

malicious/untrusted dependency pipeline
→ A03 Software Supply Chain Failures

weak secret/key/crypto handling
→ A04 Cryptographic Failures

XSS/SQL/command injection
→ A05 Injection

security control absent by design
→ A06 Insecure Design

weak/missing auth/session control
→ A07 Authentication Failures

unsigned/untrusted artifact/data update
→ A08 Software or Data Integrity Failures

missing security logging/alerting
→ A09 Security Logging and Alerting Failures

fail-open exception handling
→ A10 Mishandling of Exceptional Conditions
```

Do not force every issue into exactly one category if multiple are materially relevant.

# Severity

Use:

```text
CRITICAL
HIGH
MEDIUM
LOW
ADVISORY
```

Consider:

```text
confidentiality impact
integrity impact
availability impact
privilege gained
cross-tenant scope
authentication required
attacker control
exploit complexity
user interaction
blast radius
persistence
detectability
existing controls
```

# Critical Examples

Potential Critical/High:

- unauthenticated RCE;
- cross-tenant admin capability;
- production secret exposure;
- SQL/OS command injection with meaningful reach;
- arbitrary file write/read;
- account takeover;
- supply-chain compromise path.

Do not automatically use Critical for every injection primitive.

# Authentication Review

Inspect:

```text
credential handling
session creation
session storage
token validation
refresh
logout/revocation
password reset
MFA/recovery
OAuth/OIDC callback
state/nonce/PKCE where applicable
issuer/audience
session fixation
replay
```

Frontend-specific implementation details belong to frontend security composition; backend/session authority must remain trusted-server enforced.

# Authorization Review

Inspect:

```text
operation permission
resource ownership
tenant membership
role/capability
admin/support pathways
impersonation
batch operations
indirect object references
query filters
cache key isolation
background jobs
```

Never accept:

```text
hidden button
disabled action
frontend route guard
```

as authoritative authorization.

# Broken Access Control

High-priority patterns:

```text
IDOR/BOLA
cross-tenant access
missing ownership check
role-only check without resource scope
client-controlled org/account ID
privileged endpoint without capability check
insecure default ACL
CORS confusion where it creates real access exposure
```

# XSS

Inspect:

```text
dangerouslySetInnerHTML
innerHTML
document.write
HTML parser/renderers
markdown/HTML rendering
URL attributes
DOM sinks
third-party widget HTML
stored user content
```

Determine:

```text
source
trust level
sanitization
sink
context
CSP
```

Do not flag every `dangerouslySetInnerHTML` if data is constant/trusted and usage is demonstrably safe, but require strong justification.

# Injection

Review:

```text
SQL
NoSQL/query language
OS command
code/eval
template
LDAP
XPath
header
log injection
GraphQL/query construction
```

Prefer parameterized APIs and structured commands.

Do not rely on blacklist escaping.

# SSRF

Inspect backend/server-side fetches where user input can affect:

```text
scheme
host
port
path
redirect
DNS resolution
internal/private address
metadata endpoint
```

Mitigation may need allowlists/network policy/redirect controls.

Frontend browser fetch is generally constrained differently; do not misclassify ordinary browser navigation as SSRF.

# Path Traversal

Inspect:

```text
filesystem path
archive extraction
upload key
download path
template/file include
```

Canonicalize/validate against intended root and avoid direct user path composition.

# File Upload

Review:

```text
size limits
type/content validation
extension
storage location
public ACL
name/key generation
processing/parser
malware/content risk
SVG/HTML handling
download Content-Disposition
authorization
resource exhaustion
```

CWE-434 may apply for dangerous/unrestricted upload.

CWE-770 may apply for unbounded resource use.

# Deserialization / Parsing

Inspect:

```text
untrusted serialized objects
YAML/XML
template AST
binary formats
archive
JWT-like custom parsing
```

Use safe data-only formats and runtime schemas where appropriate.

Avoid unsafe object instantiation/evaluation from untrusted data.

# CSRF

Review when browser authentication is automatically attached:

```text
cookies
ambient credentials
state-changing requests
```

Controls may include:

```text
SameSite
CSRF token
origin verification
custom request constraints
```

depending on architecture.

Do not require CSRF tokens mechanically for bearer-token APIs that cannot receive ambient auth from a third-party origin; evaluate actual browser credential model.

# CORS

CORS is a browser policy, not authentication.

Review:

```text
allowed origins
credentials
wildcards
preflight
exposed headers
```

Only report when configuration creates a real unauthorized data/action path.

# Redirects

Review:

```text
returnTo
redirect_uri
next
callback
location
```

Avoid open redirects and unsafe scheme/host acceptance.

For OAuth/OIDC, exact provider/application redirect URI policy matters.

# Secrets

Review:

```text
client bundle
environment variables
source
logs
build artifacts
CI
error telemetry
browser storage
```

Anything shipped to browser is not secret.

Use server-only secret storage and least privilege.

# Cryptography

Review:

```text
homegrown crypto
weak/deprecated algorithm
hard-coded key
nonce/IV reuse
bad randomness
incorrect encoding/signature validation
key lifetime/storage
TLS assumptions
```

Do not recommend custom crypto.

Use platform-reviewed primitives.

# Password Handling

Server side:

```text
approved adaptive password hashing
unique salts
rate limiting
reset/recovery
```

Do not store plaintext/reversible passwords.

Do not invent password complexity requirements beyond accepted product/security policy.

# Sensitive Data Exposure

Review:

```text
API overfetching
logs
analytics
error messages
browser storage
URLs/query params
referrer
source maps
public buckets
caches
backups
third-party scripts
```

Data minimization is a primary mitigation.

# Error Handling

OWASP 2025 includes Mishandling of Exceptional Conditions.

Inspect:

```text
fail open
swallowed auth/validation error
privileged default
partial state
sensitive stack/error body
retry storm
unsafe fallback
```

Example:

```text
role lookup fails
→ default role = admin
```

is a serious security flaw.

# Logging / Alerting

Review security-relevant events:

```text
auth failures
privilege changes
impersonation
authorization denial
signature failures
secret/key actions
critical admin changes
fraud/abuse signals
```

Do not log:

```text
passwords
full tokens
secret headers
sensitive request bodies
```

# Software Supply Chain

Review application-level supply chain:

```text
dependency source
lockfile integrity
install scripts
unmaintained package
typosquatting risk
third-party runtime scripts
build plugin
artifact provenance
package updates
```

Detailed dependency CVE scanning may be handled by dedicated tooling.

Do not equate “dependency exists” with vulnerability.

# Third-Party Scripts

Browser scripts can access page data and DOM.

Review:

```text
necessity
origin
integrity/version pinning
CSP
consent
data exposure
loading scope
change control
```

# Software/Data Integrity

Review:

```text
unsigned webhook
unverified update
untrusted artifact
plugin data
client-controlled signed state
tampered serialized state
```

Use signatures/MACs/verified provenance where architecture requires integrity.

# Security Misconfiguration

Review:

```text
debug mode
verbose errors
public storage
permissive CORS
default credentials
unnecessary admin interface
insecure cookie flags
unsafe headers
unrestricted source maps
environment confusion
```

Do not create generic “missing header” findings without explaining real impact.

# Insecure Design

Use A06 when the architecture/feature fundamentally lacks a necessary security design property.

Examples:

```text
no authorization concept for resource ownership
no rate/size limit for expensive public operation
no replay model for financial webhook
no tenant-isolation model
```

Do not use Insecure Design as a catch-all for coding bugs.

# Exceptional Conditions

Review fail-safe behavior:

```text
dependency unavailable
parser fails
auth service times out
role cannot be loaded
transaction partially succeeds
storage unavailable
refresh fails
```

Security-sensitive failures generally should not grant additional privilege.

# Race Conditions

CWE may apply where concurrent operations break security/business guarantees.

Examples:

```text
double redemption
TOCTOU file check/use
parallel entitlement change
quota bypass
```

Test with controlled concurrency where material.

# Resource Exhaustion

Review:

```text
unbounded upload
unbounded page size
expensive regex
large graph/query
decompression
queue flood
retry storm
memory allocation
```

CWE-770 may apply.

Invoke:

```text
analyzing-algorithmic-complexity
```

when computational growth matters.

# Frontend Composition

A frontend-specific security review should use this skill for taxonomy/root-cause and add browser concerns such as:

```text
DOM XSS
token/storage
redirect
file/browser handling
third-party scripts
client env secrets
postMessage/iframe
```

Do not duplicate the entire OWASP/CWE taxonomy inside the frontend skill.

# Backend Composition

Backend review should add:

```text
authorization
injection
SSRF
deserialization
filesystem
webhooks
database/query
secrets
jobs
resource limits
```

while using this skill for taxonomy/root-cause.

# Infrastructure Composition

Application-security findings may hand off to infra when remediation requires:

```text
IAM
network policy
secret manager
storage ACL
WAF/rate limiting
CI/CD
artifact provenance
```

# STRIDE Handoff

If a threat model exists, connect:

```text
THREAT-003
→ SEC-007 concrete implementation weakness
```

Do not assume every threat has become a vulnerability.

Threat:

```text
possible
```

Finding:

```text
evidence of weak implementation
```

# Scanner Findings

Sources may include:

```text
SAST
DAST
dependency scanner
secret scanner
lint/security plugin
browser scanner
cloud scanner
```

Classify:

```text
VALIDATED_FINDING
FALSE_POSITIVE
NEEDS_MANUAL_VALIDATION
INFORMATIONAL
```

Never forward scanner severity blindly.

# Dynamic Testing

Where authorized and safe, verification can include:

```text
negative authorization requests
malicious payload fixture
redirect abuse case
oversized upload
replayed webhook
CSRF test
SSRF allowlist rejection
```

Do not conduct destructive testing against production without explicit authorization.

# Proof of Concept

Use the minimum safe evidence needed to prove impact.

Avoid weaponized exploit development when code/config reasoning and controlled tests are enough.

# Secure Remediation

Prefer root-cause fixes:

```text
server-side authorization
parameterized queries
contextual encoding/sanitization
allowlisted destinations
bounded resources
safe parser
server-only secrets
integrity verification
fail-closed behavior
```

over fragile detection/blacklists.

# Defense in Depth

After root cause:

```text
CSP
WAF
monitoring
rate limits
alerts
```

may add depth.

Do not present compensating controls as equivalent to removing the root weakness.

# Verification

Every material remediation needs a verification plan.

Examples:

```text
unit/domain test
application/use-case negative test
adapter/integration test
browser security test
E2E critical security flow
SAST rule
DAST
configuration inspection
penetration test
```

# ASVS Handoff

Once remediation/control requirements are known:

```text
verifying-security-controls
```

can map applicable ASVS 5.0.0 requirements and evidence.

This skill should not claim ASVS conformance itself.

# Severity vs Priority

Severity describes security impact.

Priority may additionally consider:

```text
exploit exposure
active abuse
ease of remediation
critical release path
compliance
dependency
```

Record both if project uses them.

# Residual Risk

Use:

```text
RESOLVED
REDUCED
ACCEPTED
UNRESOLVED
UNKNOWN
```

Accepted risk needs owner/rationale.

# Review Scope Completeness

Review relevant attack surfaces:

```text
auth
authorization
input/output
storage
network/integrations
files
secrets
crypto
third-party/supply chain
error handling
logging
availability
```

Do not claim full security review if only one surface was inspected.

# Review Status

Use:

```text
APPLICATION_SECURITY_REVIEW_PASS
APPLICATION_SECURITY_REVIEW_PASS_WITH_ADVISORIES
APPLICATION_SECURITY_REVIEW_REQUIRES_FIXES
APPLICATION_SECURITY_REVIEW_BLOCKED
APPLICATION_SECURITY_REVIEW_INCOMPLETE
```

# Over-Classification Audit

Flag:

- every finding mapped to many OWASP categories;
- CWE selected from title similarity;
- Top 25 rank treated as severity;
- scanner result accepted automatically;
- one root weakness split into many duplicates;
- vague “insecure design” used as catch-all.

# Under-Classification Audit

Flag:

- concrete weakness with no CWE when a precise one exists;
- authorization bypass called only “validation issue”;
- XSS called only “unsafe HTML”;
- secret exposure without information-disclosure classification;
- resource exhaustion without availability analysis.

# Final Decision

Use:

```text
APPLICATION_SECURITY_REVIEW_READY
APPLICATION_SECURITY_REVIEW_READY_WITH_CONDITIONS
SECURITY_FINDINGS_REQUIRE_REMEDIATION
THREAT_MODEL_REQUIRED
CONTROL_VERIFICATION_REQUIRED
SECURITY_SCOPE_REQUIRED
SECURITY_EVIDENCE_REQUIRED
BLOCKED
```

## Output

Use `assets/application-security-review-record.md`.

## Completion Criteria

- [ ] Review scope is explicit.
- [ ] Attack surface is inventoried.
- [ ] Findings are evidence-backed.
- [ ] Scanner output is manually validated before confirmation.
- [ ] Exploit path/preconditions are described.
- [ ] Root cause is identified.
- [ ] Precise CWE is selected when supported.
- [ ] CWE Top 25 rank is not used as finding severity.
- [ ] Relevant CWE outside Top 25 is allowed.
- [ ] Primary OWASP Top 10:2025 category is assigned where applicable.
- [ ] OWASP category is not used as a substitute for concrete weakness.
- [ ] Duplicate symptoms are consolidated by root cause.
- [ ] STRIDE threats are linked when available without assuming threat=vulnerability.
- [ ] Authentication implementation is reviewed where applicable.
- [ ] Authorization/resource ownership/multitenancy is reviewed.
- [ ] Injection/XSS/SSRF/path/file/deserialization risks are reviewed where applicable.
- [ ] CSRF/CORS/redirect behavior is analyzed according to actual browser/auth model.
- [ ] Secrets and browser-delivered configuration are reviewed.
- [ ] Cryptographic implementation is reviewed where relevant.
- [ ] Supply-chain and third-party runtime exposure is considered.
- [ ] Error handling is checked for fail-open/sensitive disclosure behavior.
- [ ] Security logging avoids both missing accountability and secret logging.
- [ ] Resource-exhaustion risks are reviewed.
- [ ] Algorithmic resource risks hand off to `analyzing-algorithmic-complexity`.
- [ ] Severity reflects actual exploitability/impact.
- [ ] Remediation fixes root cause before compensating controls.
- [ ] Verification plan exists for every material finding.
- [ ] ASVS conformance is not claimed here.
- [ ] Residual risk and owner are explicit.
- [ ] Final review status is explicit.
