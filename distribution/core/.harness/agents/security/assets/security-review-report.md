# Security Review Report

## Gate Decision

- Decision: SECURITY_APPROVED / SECURITY_APPROVED_WITH_CONDITIONS / SECURITY_CHANGES_REQUIRED / SECURITY_BLOCKED_PENDING_DECISION / SECURITY_BLOCKED_PENDING_EVIDENCE / SECURITY_REVIEW_NOT_REQUIRED
- Review version:
- Reviewer:
- Date:
- Target change / PR:
- Scope: ARCHITECTURE / BACKEND / FRONTEND / FULL_STACK / INFRASTRUCTURE / MIXED
- Re-review required: yes/no

## Authoritative Basis

- Applicable `AGENTS.md`:
- Requirement / OpenSpec:
- Architecture package:
- DFD / trust boundaries:
- STRIDE record:
- Security policies:
- Privacy/consent policy:
- Accepted control baseline:
- Approved ASVS source/version:
- Risk-acceptance authority:
- Validator evidence:
- Code Review findings:
- Architecture Review findings:
- QA findings:

## Security Scope

### Assets
-

### Actors / Roles
-

### Entry Points
-

### Trust Boundaries
-

### Privileged Operations
-

### Sensitive Data
-

### External Providers
-

### Secrets / Credentials
-

## Threat Model Status

- STRIDE required: yes/no
- Status: THREAT_MODEL_READY / THREAT_MODEL_READY_WITH_CONDITIONS / THREAT_MODEL_NOT_REQUIRED / THREAT_MODEL_REVIEW_REQUIRED / BLOCKED
- New/changed trust boundaries:
- New/changed attack paths:
- Threats requiring implementation verification:

## Attack Surface Inventory

| Surface | Actor/source | Trust boundary | Sensitive/privileged effect | Existing control | Evidence |
|---|---|---|---|---|---|
| | | | | | |

## Security Findings

### SEC-001 — [Title]

- Severity: CRITICAL / HIGH / MEDIUM / LOW
- Confidence: HIGH / MEDIUM / LOW
- Category: AUTHORIZATION / TENANT_ISOLATION / AUTHENTICATION_SESSION / INJECTION / XSS / SSRF / FILE_PATH / DESERIALIZATION / CRYPTOGRAPHY / SECRETS / SECURITY_CONFIGURATION / EXCEPTION_HANDLING / LOGGING_AUDIT / INTEGRITY_SUPPLY_CHAIN / WEBHOOK_INTEGRITY / RESOURCE_EXHAUSTION / FRONTEND_TRUST / PRIVACY_ANALYTICS / CONTROL_VERIFICATION / DEPENDENCY_VULNERABILITY
- Asset/security property:
- Actor/precondition:
- Entry point / trust boundary:
- Location/evidence:
- Abuse/exploit path:
- Concrete weakness:
- CWE:
- OWASP Top 10:2025:
- Impact:
- Existing mitigation/control:
- Why insufficient:
- Smallest remediation/control direction:
- Verification required:
- Residual risk:
- Blocking: yes/no
- Related Code Review finding:
- Handoff / owner:

## Frontend Security

- Applicable: yes/no
- Unsafe HTML/XSS:
- Token/session storage:
- Browser-visible secrets:
- Redirect/navigation:
- Browser storage:
- Files:
- Third-party scripts:
- postMessage/iframe:
- URL/referrer leakage:
- Client-side authorization assumption:
- CSP/browser controls:
- Findings:

## Privacy / Analytics

- Applicable: yes/no
- Accepted policy available: yes/no
- Collection/purpose:
- Consent gate:
- User identifiers:
- Sensitive fields:
- Analytics provider:
- Session replay:
- Debug/error logging:
- Retention evidence:
- Consent withdrawal:
- Findings/gaps:

## Security Control Verification

| Control | Baseline/source | Applicable? | Implementation evidence | Behavioral/config/runtime evidence | Status | Residual risk |
|---|---|---|---|---|---|---|
| | | | | | PASS / FAIL / NOT_APPLICABLE / NOT_VERIFIED | |

## Compensating Controls

| Primary gap | Compensating control | Evidence | Authority | Residual risk | Status |
|---|---|---|---|---|---|
| | | | | | |

## Risk Acceptance Ledger

| Risk | Severity | Control gap | Authority | Scope/expiry | Residual risk | Valid? |
|---|---|---|---|---|---|---|
| | | | | | | |

## Dependency / Supply Chain Assessment

- Scanner/SBOM evidence:
- Reachable vulnerabilities:
- Build-time only findings:
- Runtime findings:
- CI/action integrity:
- Third-party runtime scripts:
- Required remediation:

## Security Questions / Missing Evidence

| ID | Decision/evidence needed | Why needed | Blocking? | Route |
|---|---|---|---|---|
| | | | | Product / Architecture / Infrastructure / Validator / Governance |

## Handoffs

| Finding / need | Recipient | Expected output | Blocking | Re-entry condition |
|---|---|---|---|---|
| | Implementation / Validator / Code Review / Architecture Review / QA / Performance / Infrastructure / Detail Analyst / Reviewer / Product / Governance | | yes/no | |

## Residual Security Risk

- Open threats:
- Failed controls:
- Not-verified controls:
- Accepted risks:
- Evidence limitations:
- Deferred controls:
- Third-party dependencies:

## Security Summary

- Critical findings:
- High findings:
- Medium findings:
- Low findings:
- Blocking decisions:
- Blocking evidence:
- Control PASS:
- Control FAIL:
- Control NOT_VERIFIED:
- Risk accepted:
- Why final decision is justified:

## Exact Next Action

-
