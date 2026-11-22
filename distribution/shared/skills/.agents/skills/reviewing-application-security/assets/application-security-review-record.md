# Application Security Review Record

## Context

- Application/feature:
- Frontend/backend/full-stack:
- Repository:
- Environment:
- Architecture reference:
- Threat model:
- Authentication:
- Authorization/multitenancy:
- External integrations:
- Security tooling:
- Applicable `AGENTS.md`:
- Reviewer/date:

## Scope

- Included:
- Excluded:
- Claim scope: focused / feature / application / full review
- Evidence available:
- Blockers:

## Attack Surface

| Surface | Entry point | Trust boundary | Sensitive asset |
|---|---|---|---|
| | | | |

## Finding Inventory

| ID | Severity | Status | Title | Primary CWE | OWASP |
|---|---|---|---|---|---|
| | | | | | |

## Finding

### SEC-001 — [Title]

- Status: CONFIRMED / LIKELY_REQUIRES_VALIDATION / DEFENSE_IN_DEPTH / FALSE_POSITIVE / NOT_APPLICABLE
- Severity: CRITICAL / HIGH / MEDIUM / LOW / ADVISORY
- Affected surface:
- Preconditions:
- Attack path:
- Evidence:
- Impact:
- Root cause:
- Primary CWE:
- Related CWE(s):
- CWE Top 25 2025:
- Primary OWASP Top 10:2025:
- Related OWASP category/categories:
- Related STRIDE threat:
- Existing controls:
- Remediation:
- Verification:
- Owner:
- Residual risk: RESOLVED / REDUCED / ACCEPTED / UNRESOLVED / UNKNOWN

## OWASP Top 10:2025 Coverage

| Category | Applicable | Findings / evidence |
|---|---|---|
| A01 Broken Access Control | | |
| A02 Security Misconfiguration | | |
| A03 Software Supply Chain Failures | | |
| A04 Cryptographic Failures | | |
| A05 Injection | | |
| A06 Insecure Design | | |
| A07 Authentication Failures | | |
| A08 Software or Data Integrity Failures | | |
| A09 Security Logging and Alerting Failures | | |
| A10 Mishandling of Exceptional Conditions | | |

## CWE Mapping Audit

- Precise root-cause CWE used:
- Top 25 rank incorrectly treated as severity:
- CWE selected by title only:
- Relevant non-Top-25 CWE allowed:
- Duplicate CWE mappings consolidated:

## Access Control / Multitenancy

- Resource ownership:
- Tenant identifier source:
- Role/capability:
- Server-side enforcement:
- Batch/query filtering:
- Cache tenant isolation:
- Admin/support impersonation:
- Negative authorization tests:

## Authentication / Session

- Token/session validation:
- Storage:
- Refresh:
- Logout/revocation:
- OAuth/OIDC:
- Recovery/MFA:
- Replay/fixation:
- Missing-auth critical paths:

## Injection / XSS

- User-controlled sources:
- SQL/query construction:
- OS command:
- code/eval/template:
- HTML/DOM sinks:
- sanitization/encoding:
- CSP defense-in-depth:

## SSRF / URLs / Redirects

- Server-side outbound fetch:
- Host/scheme control:
- private/internal addresses:
- redirect following:
- open redirect:
- OAuth redirect URI:

## Files / Parsing / Deserialization

- Upload:
- size/type/content:
- storage ACL:
- parser:
- path/key:
- archive:
- untrusted deserialization:
- download authorization:

## CSRF / CORS

- Authentication model:
- Ambient credentials:
- CSRF control:
- SameSite:
- Origin:
- CORS origins:
- credentials:
- Real exploit path:

## Secrets / Crypto

- Browser-delivered secrets:
- source/config:
- logs:
- CI/build:
- key storage:
- algorithm:
- randomness:
- nonce/IV:
- signature validation:

## Supply Chain / Integrity

- dependencies:
- lockfile/provenance:
- install scripts:
- runtime third-party scripts:
- webhook signatures:
- artifact/update integrity:

## Exceptional Conditions

- fail-open:
- privileged defaults:
- swallowed errors:
- partial state:
- sensitive error output:
- unsafe fallback:

## Logging / Alerting

- auth failures:
- authorization denials:
- privilege changes:
- impersonation:
- signature/integrity failures:
- secrets/PII excluded:
- alerting:

## Availability / Resource Exhaustion

- rate/size limits:
- upload limits:
- page/query limits:
- parser/regex:
- retries:
- queue:
- memory:
- algorithmic handoff required:

## Scanner / Tool Findings

| Tool finding | Classification | Reason |
|---|---|---|
| | VALIDATED_FINDING / FALSE_POSITIVE / NEEDS_MANUAL_VALIDATION / INFORMATIONAL | |

## Severity / Priority

- Severity method:
- Exploitability:
- Blast radius:
- Authentication required:
- Cross-tenant:
- Active abuse:
- Priority:

## Remediation Plan

| Finding | Root-cause fix | Defense-in-depth | Owner |
|---|---|---|---|
| | | | |

## Verification Matrix

| Finding | Boundary | Negative/positive evidence |
|---|---|---|
| | | |

## ASVS Follow-Up

- Control verification required:
- Candidate control areas:
- Do not claim conformance here:
- Next skill: `verifying-security-controls`

## Residual Risk

| Finding | Status | Rationale | Owner |
|---|---|---|---|
| | | | |

## Final Decision

- Review status:
- Critical/high findings:
- Required remediation:
- Required threat-model update:
- Required control verification:
- Remaining uncertainty:
