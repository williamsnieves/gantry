---
name: verifying-security-controls
description: Verifies implemented application-security controls against an accepted control baseline, with OWASP ASVS 5.0.0 as the default application-security verification standard when selected by the project. Use after threat modeling or security review to determine which controls are applicable, gather implementation and test/configuration/runtime evidence, classify each requirement as PASS, FAIL, NOT_APPLICABLE, or NOT_VERIFIED, track compensating controls and residual risk, and prevent unsupported conformance claims. Require exact requirement identifiers and wording from the project's approved ASVS source/version before claiming coverage. Do not invent requirement IDs, treat planned controls as implemented, infer PASS from code intent alone, or claim application-wide ASVS conformance from a partial feature review.
---

# Verifying Security Controls

## Purpose

Verify that required security controls actually exist and work.

Core workflow:

```text
accepted security baseline
→ scope
→ applicability
→ exact control requirement
→ implementation evidence
→ behavioral/config/runtime evidence
→ PASS / FAIL / NOT_APPLICABLE / NOT_VERIFIED
→ remediation / residual risk
→ verification report
```

This skill answers:

```text
Is the required security control actually implemented and evidenced?
```

It does not primarily discover threats or vulnerabilities.

Use:

```text
threat-modeling-with-stride
```

for architecture threat discovery.

Use:

```text
reviewing-application-security
```

for implementation weakness discovery and OWASP/CWE classification.

## Default Verification Baseline

When the project has selected OWASP ASVS:

```text
OWASP ASVS 5.0.0
```

is the default baseline for this skill.

However:

- exact requirement identifiers;
- exact requirement text;
- verification level/profile;
- organizational tailoring;

MUST come from the approved project copy/source of ASVS.

Do not invent ASVS requirement IDs from memory.

If the exact ASVS source is unavailable, use:

```text
CONTROL_BASELINE_SOURCE_REQUIRED
```

and continue only with project-defined security requirements that are actually available.

## Knowledge Model

```text
STRIDE
→ what could go wrong

OWASP Top 10
→ broad risk classification

CWE
→ concrete weakness/root cause

ASVS / project control baseline
→ what must be verified

evidence
→ whether control is actually satisfied
```

## Use When

- Verifying remediation after a security review.
- Verifying security requirements before release.
- Assessing a feature against ASVS.
- Building a security quality gate.
- Producing evidence for a security sign-off.
- Verifying authentication/session controls.
- Verifying authorization controls.
- Verifying validation/encoding controls.
- Verifying secrets/crypto controls.
- Verifying logging/audit controls.
- Verifying file/upload controls.
- Verifying API/webhook/integrity controls.
- Verifying configuration/deployment controls.
- Verifying selected controls for frontend/backend/full-stack.
- Re-checking controls after architectural change.

## Do Not Use When

- No accepted control baseline exists.
- Exact ASVS requirements are unavailable and the task requires ASVS-specific IDs.
- The task is still threat discovery.
- The task is to find code vulnerabilities generally.
- The task is generic penetration testing.
- The task is dependency vulnerability scanning.
- The user asks for a conformance certificate.
- Only one narrow feature was reviewed but the requested claim is application-wide.

## Inputs

- Approved control baseline.
- Baseline version.
- Exact requirement IDs/text.
- Verification level/profile if applicable.
- Feature/application scope.
- Threat model.
- Security findings.
- Architecture.
- Code/configuration.
- Tests.
- Runtime/deployment evidence.
- IAM/secrets/config evidence.
- Logs/audit evidence.
- CI/CD evidence where applicable.
- Existing exceptions/risk acceptances.
- Applicable `AGENTS.md`.

## Outputs

- Verification scope.
- Baseline/version.
- Applicability matrix.
- Control-by-control evidence.
- PASS/FAIL/N/A/NOT_VERIFIED statuses.
- Evidence gaps.
- Remediation requirements.
- Compensating-control decisions.
- Residual-risk record.
- Conformance-claim boundary.
- Security-control verification record.

# Verification Statuses

Use exactly:

```text
PASS
FAIL
NOT_APPLICABLE
NOT_VERIFIED
```

Optional operational states may supplement but not replace them:

```text
REMEDIATION_IN_PROGRESS
EVIDENCE_PENDING
RISK_ACCEPTED
```

# PASS

Use `PASS` only when:

```text
requirement is applicable
+
implementation exists
+
evidence demonstrates required behavior
```

Evidence may be:

```text
code/config inspection
+
automated test
+
runtime/deployment evidence
```

depending on the control.

Intent is insufficient.

# FAIL

Use `FAIL` when:

- requirement is applicable;
- implementation is absent; or
- implementation contradicts requirement; or
- evidence proves unsafe behavior.

A failed control cannot be turned into PASS because another unrelated control exists.

# NOT_APPLICABLE

Use only when the control truly does not apply to the scoped system.

Record:

```text
reason
scope assumption
approver/owner if project requires
```

Weak reason:

```text
we do not want to implement it
```

is not N/A.

# NOT_VERIFIED

Use when:

- implementation may exist but evidence is insufficient;
- environment cannot be tested;
- configuration cannot be inspected;
- exact requirement interpretation is unresolved;
- third-party control evidence is missing.

`NOT_VERIFIED` is not PASS.

# Evidence Hierarchy

Prefer direct evidence.

Possible hierarchy:

```text
1. deterministic automated security behavior test
2. integration/runtime/configuration evidence
3. code/config inspection
4. platform/provider documented evidence
5. manual demonstration
6. statement/intent only
```

The exact best evidence depends on the requirement.

Do not demand an automated test for every control if configuration/runtime inspection is the correct proof.

# Evidence Triangulation

For high-impact controls, combine multiple evidence types.

Example authorization control:

```text
server-side policy/code
+
negative integration test
+
positive allowed case
```

Example secrets control:

```text
server-only configuration
+
bundle inspection
+
secret scanner / CI policy
```

# Exact Requirement Source

Record:

```text
baseline
version
requirement ID
exact approved wording/location
```

Do not paraphrase into a stronger or weaker requirement before verifying.

Interpretation notes may be added separately.

# Applicability First

Before testing, determine:

```text
Does this requirement apply to this scope?
```

Examples:

- password controls do not apply if app delegates authentication and stores no passwords;
- file-upload controls do not apply if feature has no upload;
- browser-specific control may not apply to backend-only service;
- API control may apply even if no browser exists.

Do not mark irrelevant requirements FAIL merely because they are absent.

# Scope Types

Use:

```text
FEATURE
SERVICE
APPLICATION
PLATFORM
REPOSITORY
DEPLOYMENT
FULL_STACK_FLOW
```

# Conformance Boundary

A feature-level review can claim only:

```text
scoped controls verified for this feature
```

It cannot claim:

```text
application is ASVS compliant
```

unless the full required scope/profile has actually been assessed.

# Verification Profile / Level

If project selects an ASVS verification level/profile, record it exactly.

Do not infer a level merely from application type.

If no level/profile is accepted:

```text
PROFILE_DECISION_REQUIRED
```

# Tailoring

Organizations may add/remove/tailor controls.

Record:

```text
baseline requirement
tailoring decision
reason
owner
```

Do not silently omit controls.

# Threat-to-Control Traceability

Link:

```text
THREAT-001
→ security requirement
→ ASVS/project control
→ evidence
```

This demonstrates that important threat mitigations are covered.

# Finding-to-Control Traceability

Link:

```text
SEC-004
→ remediation
→ control requirement
→ verification evidence
```

A finding marked fixed should have control evidence when appropriate.

# Control Categories

The actual ASVS source determines exact categories/IDs.

Common verification domains may include:

```text
architecture/design
authentication
session management
access control
validation/sanitization/encoding
cryptography
error handling/logging
data protection
communications
malicious code/supply chain
business logic
files/resources
API/web services
configuration
```

Do not substitute this conceptual list for the exact ASVS document structure.

# Authentication Controls

Evidence may include:

```text
identity-provider configuration
token/session validation
negative auth tests
credential handling
recovery flow
MFA configuration
lockout/rate controls where required
```

Do not require password-storage evidence if passwords are fully delegated and out of scope.

# Authorization Controls

High-value evidence:

```text
server-side enforcement point
positive allowed test
negative wrong-role test
negative wrong-tenant/resource test
batch/query isolation
admin/support pathway tests
```

Client-side hiding is not sufficient.

# Multi-Tenant Controls

Verify:

```text
tenant membership
resource ownership
query filtering
cache isolation
search/index isolation
background job isolation
export isolation
support/admin access
```

according to baseline requirements and threat model.

# Input Validation

Verify at trust boundaries.

Evidence:

```text
runtime schema
allowlist/structured parser
invalid-input tests
boundary tests
```

Do not claim validation because TypeScript types exist at runtime.

# Output Encoding / XSS

Verify context-appropriate controls:

```text
framework escaping
sanitizer configuration
safe sink
negative malicious fixture
CSP defense-in-depth
```

`dangerouslySetInnerHTML` with a sanitizer requires evidence of sanitizer policy/context.

# Injection Controls

Evidence:

```text
parameterized queries
structured command APIs
no dynamic code evaluation
negative injection tests where risk warrants
```

Do not rely only on blacklist validation.

# CSRF

Verify against the real authentication model.

Evidence may include:

```text
SameSite
CSRF token
origin checks
request constraints
```

depending on requirement.

Do not require a token mechanically if the selected requirement/control model is satisfied differently.

# CORS

Verify exact:

```text
allowed origins
credentials
methods
headers
preflight behavior
```

in deployment/configuration evidence.

CORS is not authentication.

# Redirect Controls

Verify:

```text
allowed destination policy
scheme/host/path restrictions
OAuth redirect URI exactness
negative external-host cases
```

# SSRF Controls

Verify server-side outbound destination restrictions:

```text
allowlist
scheme restrictions
DNS/private address behavior
redirect behavior
network egress controls
```

when applicable.

# File Controls

Verify:

```text
size
type/content
filename/key
storage ACL
processing
download authorization
malicious content
archive/decompression
quota
```

# Resource Limits

Verify:

```text
request size
page size
upload size
query complexity
rate limits
timeouts
queue limits
memory/resource caps
```

For computational growth, compose with:

```text
analyzing-algorithmic-complexity
```

# Cryptography

Evidence may include:

```text
approved library
algorithm/mode
key source/storage
rotation
randomness
nonce/IV handling
signature validation
TLS configuration
```

Do not approve custom crypto based on unit tests alone.

# Secrets

Verify:

```text
server-only location
least privilege
rotation
no browser bundle
no source
no logs
no CI artifact exposure
```

Potential evidence:

```text
bundle grep
secret scanner
deployment config
IAM
CI policy
```

# Data Protection

Verify:

```text
data minimization
authorization
storage
transmission
logging
retention
cache
backup
analytics
```

according to accepted requirements.

# Logging / Audit

Verify security events include enough evidence for accountability:

```text
actor
action
resource
time
result
correlation
```

without storing:

```text
password
full token
secret
sensitive payload
```

# Alerting

If requirement includes detection/alerting, evidence may include:

```text
rule/config
test event
alert receipt
routing/ownership
```

A log line alone may not satisfy alerting.

# Exceptional Conditions

Verify safe failures.

Negative cases:

```text
auth service unavailable
authorization lookup fails
signature verification errors
storage failure
parser exception
```

Expected:

```text
no privilege increase
no sensitive disclosure
consistent rollback/failure
```

# Webhook Integrity

Verify:

```text
signature
timestamp/anti-replay if applicable
idempotency
event ownership
ordering semantics if required
flood protection
negative signature test
replay test
```

# Supply Chain / Integrity

Depending on control baseline:

```text
dependency lock
trusted registries
build isolation
artifact provenance
signing
CI permissions
update verification
third-party script governance
```

# Third-Party Controls

When a provider owns a control:

```text
provider evidence
contract/documentation
configuration export
attestation if available
```

may support verification.

Do not mark PASS only because provider marketing says it is secure.

# Infrastructure Controls

Some application requirements rely on infrastructure:

```text
TLS
secret manager
IAM
network egress
storage ACL
WAF/rate limiting
logging
artifact integrity
```

Record ownership:

```text
APP
BACKEND
FRONTEND
PLATFORM
INFRA
SECURITY
THIRD_PARTY
```

# Configuration Evidence

Capture reproducible evidence:

```text
IaC
config file
cloud policy export
deployment manifest
CI configuration
header scan
runtime endpoint behavior
```

Avoid screenshots alone when machine-readable/config evidence exists.

# Runtime Evidence

Runtime verification is valuable for:

```text
headers
cookies
TLS
CORS
redirects
authz
rate limits
error behavior
security logging
```

Use safe, authorized environments.

# Test Evidence

Prefer negative tests for security controls.

Examples:

```text
wrong tenant denied
missing auth denied
invalid signature denied
malicious HTML neutralized
external redirect rejected
oversized file rejected
```

Positive-only tests do not prove enforcement boundaries sufficiently.

# Control Independence

One control may mitigate several threats.

Several controls may be needed for one threat.

Do not force 1:1 mapping.

# Compensating Controls

Use only when:

- baseline/project permits;
- primary control cannot be implemented;
- alternative reduces equivalent risk;
- limitation is documented;
- owner accepts residual risk;
- evidence exists.

Status remains based on the accepted tailored requirement.

Do not silently replace failed control with unrelated defense-in-depth.

# Compensating Control Record

Record:

```text
original requirement
reason primary cannot be met
alternative control
equivalence argument
evidence
residual risk
owner/approval
```

# Exceptions / Risk Acceptance

A failed control can be risk-accepted operationally.

That does NOT make it PASS.

Represent:

```text
verification status = FAIL
risk treatment = ACCEPTED
```

unless the baseline itself has been formally tailored.

# Planned Control

Backlog/task/design:

```text
PLANNED
```

is evidence of intent only.

Verification:

```text
FAIL
```

if applicable and absent, or:

```text
NOT_VERIFIED
```

if implementation status is unknown.

Never PASS.

# Code Review Evidence

Code inspection can establish:

```text
control exists in source
```

but may not prove:

```text
deployed configuration
runtime behavior
all routes use it
integration works
```

Choose proportional additional evidence.

# Automated Tests

Automated tests provide repeatability.

But tests can themselves be wrong.

Review:

```text
test boundary
negative case
fixture realism
actual production code path
```

# Penetration Testing Evidence

A pentest can strengthen verification.

A pentest finding-free result does not automatically prove every ASVS requirement.

Map evidence precisely.

# Scanner Evidence

SAST/DAST/SCA/secret scanner may support a control.

Do not make scanner pass/fail the entire verification baseline.

# Manual Verification

Manual review is acceptable where automation is impractical.

Record:

```text
steps
environment
evidence
reviewer/date
```

# Evidence Freshness

Evidence can become stale after:

```text
architecture change
auth change
provider change
dependency change
deployment/config change
control refactor
```

Record:

```text
commit/version
environment
date
```

# Regression Verification

After remediation:

```text
old exploit/negative case
→ fails safely
```

Add durable automated regression when practical.

# Control Drift

Configuration controls can drift independently of code.

Examples:

```text
CORS
cookie flags
bucket ACL
IAM
TLS
WAF
CI permissions
```

Use recurring/config policy checks where project supports them.

# Environment Differences

A control may pass in staging and fail in production configuration.

Record environment evidence separately.

Do not extrapolate blindly.

# Evidence Quality

Use:

```text
STRONG
MODERATE
WEAK
MISSING
```

based on directness/reproducibility/freshness.

# Verification Confidence

Use:

```text
HIGH
MEDIUM
LOW
```

Do not turn low confidence into PASS if requirement cannot actually be demonstrated.

# Requirement Result Record

For every control:

```text
baseline/version
control ID
requirement
scope
applicable?
implementation
evidence
status
confidence
owner
finding/threat links
remediation
residual risk
```

# Coverage Metrics

Useful:

```text
applicable controls
PASS count
FAIL count
NOT_VERIFIED count
NOT_APPLICABLE count
```

Do not report a misleading “90% secure” percentage.

If percentage is requested, label it:

```text
verification coverage
```

not security level.

# Conformance Claims

Allowed wording for partial scope:

```text
The listed controls were verified for Feature X
against the selected ASVS 5.0.0 requirements.
```

Avoid:

```text
ASVS compliant
ASVS certified
secure
fully compliant
```

unless the organization has a complete approved assessment basis.

# Full Application Claim

Before broad claim require:

```text
complete in-scope control set
exact baseline/profile
all applicability decisions
evidence
exceptions
review ownership
required organizational approval
```

This skill alone does not issue external certification.

# Verification Gate

Possible decisions:

```text
SECURITY_CONTROLS_VERIFIED
SECURITY_CONTROLS_VERIFIED_WITH_EXCEPTIONS
SECURITY_CONTROLS_REQUIRE_REMEDIATION
SECURITY_CONTROLS_NOT_VERIFIED
CONTROL_BASELINE_SOURCE_REQUIRED
PROFILE_DECISION_REQUIRED
EVIDENCE_REQUIRED
SCOPE_INCOMPLETE
BLOCKED
```

# Relationship to Frontend Security

Future flow:

```text
reviewing-frontend-security
→ identifies browser/frontend risk
→ reviewing-application-security taxonomy
→ verifying-security-controls evidence
```

Frontend controls may require:

```text
CSP
safe DOM handling
no browser secrets
redirect policy
upload handling
third-party script controls
cookie/session settings
```

# Relationship to Backend Security

Backend controls may require:

```text
authn
authz
tenant ownership
validation
injection prevention
SSRF
webhook integrity
file safety
rate/resource limits
logging
```

# Relationship to Infrastructure

Infrastructure can own evidence for:

```text
IAM
secret storage
TLS
network
WAF
storage ACL
CI/CD
artifact integrity
monitoring
```

The application verification record should link it rather than duplicate implementation.

# Relationship to Security Agent

Future Security Agent can orchestrate:

```text
threat-modeling-with-stride
→ reviewing-application-security
→ verifying-security-controls
→ frontend/backend/infra specialization
→ validator-agent
```

# Verification Workflow

1. load exact approved baseline/version;
2. define scope/profile;
3. select applicable requirements;
4. link threats/findings/security requirements;
5. inspect implementation;
6. collect direct evidence;
7. run negative/positive verification where needed;
8. assign PASS/FAIL/N/A/NOT_VERIFIED;
9. record gaps/remediation;
10. record compensating controls/exceptions;
11. assess residual risk;
12. state precise claim boundary.

# Over-Verification Audit

Flag:

- testing every control through E2E;
- duplicate evidence collection across layers;
- requiring pentest for trivial config control;
- screenshots when config can be inspected directly;
- repeated manual steps where deterministic automation exists.

# Under-Verification Audit

Flag:

- PASS from code comment;
- PASS from backlog item;
- PASS from unit test that bypasses production path;
- authz control without negative test;
- secret control without bundle/deployment evidence;
- runtime config inferred from source only;
- third-party control with no evidence;
- N/A without rationale.

# Final Decision

Use:

```text
SECURITY_CONTROL_VERIFICATION_READY
SECURITY_CONTROL_VERIFICATION_READY_WITH_CONDITIONS
SECURITY_CONTROLS_REQUIRE_REMEDIATION
SECURITY_CONTROL_EVIDENCE_REQUIRED
CONTROL_BASELINE_SOURCE_REQUIRED
PROFILE_DECISION_REQUIRED
SECURITY_SCOPE_REQUIRED
SECURITY_CONFORMANCE_CLAIM_NOT_SUPPORTED
BLOCKED
```

## Output

Use `assets/security-control-verification-record.md`.

## Completion Criteria

- [ ] Exact control baseline and version are recorded.
- [ ] Exact ASVS requirement IDs/text come from the approved source rather than memory.
- [ ] Verification scope is explicit.
- [ ] Selected level/profile/tailoring is explicit when applicable.
- [ ] Applicability is decided before verification.
- [ ] NOT_APPLICABLE includes rationale.
- [ ] PASS requires implemented control plus evidence.
- [ ] Planned/backlog control is never marked PASS.
- [ ] NOT_VERIFIED is distinct from PASS.
- [ ] FAIL is not converted to PASS by risk acceptance.
- [ ] Threats/findings are traced to relevant controls where available.
- [ ] Evidence type matches the control.
- [ ] High-impact controls use strong/direct evidence.
- [ ] Authorization controls include negative cases where applicable.
- [ ] Multi-tenant/resource-ownership controls are verified server-side.
- [ ] Runtime input validation is evidenced at trust boundaries.
- [ ] XSS/injection controls use context/structured API evidence.
- [ ] CSRF/CORS are verified according to actual auth/browser model.
- [ ] SSRF/file/redirect controls are verified where applicable.
- [ ] Secrets are checked across source, client bundle, logs, CI, and deployment where relevant.
- [ ] Cryptographic controls use approved primitives/config evidence.
- [ ] Logging/audit controls prove accountability without secret leakage.
- [ ] Exceptional conditions fail safely.
- [ ] Resource limits are verified.
- [ ] Algorithmic resource controls hand off to `analyzing-algorithmic-complexity` where needed.
- [ ] Webhook integrity/replay/idempotency controls are tested when applicable.
- [ ] Infrastructure-owned controls link to reproducible evidence.
- [ ] Third-party-owned controls have evidence, not assumptions.
- [ ] Compensating controls are explicitly justified and approved where used.
- [ ] Evidence freshness/environment/commit is recorded.
- [ ] Remediations have regression verification where practical.
- [ ] Verification coverage is not presented as “percent secure.”
- [ ] Partial feature review does not claim application-wide ASVS conformance.
- [ ] Final verification status and claim boundary are explicit.

## References

- Read `references/asvs-baseline-scope-profile-and-applicability.md` first.
- Read `references/evidence-quality-pass-fail-na-and-not-verified.md`.
- Read `references/authentication-authorization-validation-and-browser-controls.md`.
- Read `references/secrets-crypto-files-webhooks-resource-limits-and-logging.md`.
- Read `references/configuration-infrastructure-third-party-and-supply-chain-evidence.md`.
- Read `references/compensating-controls-risk-acceptance-and-residual-risk.md`.
- Read `references/conformance-claims-coverage-metrics-and-evidence-freshness.md`.
- Read `references/security-control-verification-audit.md` before completion.
