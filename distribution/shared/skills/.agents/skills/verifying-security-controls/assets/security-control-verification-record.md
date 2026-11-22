# Security Control Verification Record

## Context

- Application/feature:
- Scope type: FEATURE / SERVICE / APPLICATION / PLATFORM / REPOSITORY / DEPLOYMENT / FULL_STACK_FLOW
- Repository/system:
- Environment:
- Threat model:
- Security review:
- Applicable `AGENTS.md`:
- Verifier/date:

## Control Baseline

- Standard:
- Version:
- Approved source/location:
- Exact source available:
- Verification level/profile:
- Tailoring:
- Organization-specific additions:
- Baseline owner:

## Scope

- Included:
- Excluded:
- Environments:
- Actors/roles:
- Data:
- Integrations:
- Claim boundary:

## Control Inventory

| Control ID | Requirement | Applicable | Status | Evidence quality |
|---|---|---|---|---|
| | | YES / NO / UNKNOWN | PASS / FAIL / NOT_APPLICABLE / NOT_VERIFIED | STRONG / MODERATE / WEAK / MISSING |

## Control Verification

### CONTROL-[ID]

- Baseline:
- Version:
- Exact requirement:
- Source reference:
- Scope:
- Applicability: YES / NO / UNKNOWN
- N/A rationale:
- Implementation:
- Evidence:
- Evidence type:
- Environment:
- Commit/version:
- Evidence date:
- Evidence quality: STRONG / MODERATE / WEAK / MISSING
- Verification confidence: HIGH / MEDIUM / LOW
- Status: PASS / FAIL / NOT_APPLICABLE / NOT_VERIFIED
- Related threat(s):
- Related finding(s):
- Owner:
- Required remediation:
- Compensating control:
- Residual risk:
- Notes:

## Evidence Matrix

| Control | Code/config | Automated test | Runtime/config | Provider/infra | Manual |
|---|---|---|---|---|---|
| | | | | | |

## Authentication

- Applicable controls:
- Identity provider evidence:
- Session/token validation:
- Negative missing/invalid auth:
- Recovery/MFA:
- Refresh/logout:
- Result:

## Authorization / Multitenancy

- Applicable controls:
- Server-side policy:
- Positive allowed case:
- Wrong-role denial:
- Wrong-tenant denial:
- Wrong-resource denial:
- Query/cache isolation:
- Admin/support:
- Result:

## Validation / Encoding / Injection

- Runtime validation:
- Structured/parameterized APIs:
- XSS sinks:
- Sanitizer:
- malicious fixture:
- CSRF:
- CORS:
- redirects:
- SSRF:
- Result:

## Secrets / Cryptography

- Server-only secrets:
- Client bundle check:
- Source:
- Logs:
- CI:
- secret manager:
- key scope/rotation:
- approved crypto:
- signature:
- TLS:
- Result:

## Files / Resources

- Upload:
- size:
- type/content:
- path/key:
- storage ACL:
- parser:
- download auth:
- archive/decompression:
- quota:
- Result:

## Webhooks / Integrity

- Signature:
- negative signature:
- replay:
- idempotency:
- timestamp:
- flood protection:
- event ownership:
- Result:

## Logging / Exceptional Conditions

- Security audit:
- actor/action/resource:
- secret/PII redaction:
- authorization failure logging:
- privileged changes:
- safe failure:
- fail-open test:
- partial state:
- alerting:
- Result:

## Resource Limits / DoS

- request size:
- upload size:
- page/query size:
- rate limit:
- timeout:
- queue/backpressure:
- memory:
- regex/parser:
- complexity handoff:
- Result:

## Infrastructure / Deployment Evidence

- IAM:
- network:
- egress:
- storage ACL:
- TLS:
- WAF/rate limit:
- secret manager:
- CI/CD:
- artifact integrity:
- monitoring:
- Evidence links:

## Third-Party Evidence

| Provider/control | Evidence | Freshness | Status |
|---|---|---|---|
| | | | |

## Threat / Finding Traceability

| Threat/Finding | Control(s) | Verification |
|---|---|---|
| | | |

## Failures / Evidence Gaps

| Control | Gap | Status | Required action |
|---|---|---|---|
| | | | |

## Compensating Controls

| Original control | Reason | Alternative | Evidence | Approval | Residual risk |
|---|---|---|---|---|---|
| | | | | | |

## Risk Acceptance

| Failed control | Risk treatment | Owner | Expiry/review | Verification status |
|---|---|---|---|---|
| | ACCEPTED / REDUCED / TRANSFERRED / UNRESOLVED | | | FAIL / NOT_VERIFIED |

## Evidence Freshness

- Commit/build:
- Environment:
- Deployment version:
- Provider/config version:
- Review date:
- Drift-sensitive controls:
- Reverification trigger:

## Coverage Summary

- Applicable:
- PASS:
- FAIL:
- NOT_VERIFIED:
- NOT_APPLICABLE:
- Unknown applicability:
- Coverage percentage requested:
- If shown, labeled verification coverage rather than security score:

## Conformance Claim Boundary

- Feature-level:
- Application-level:
- Full selected profile verified:
- Exceptions:
- Claim supported:
- Unsupported wording avoided:
- External certification implied:

## Final Decision

- Decision:
- Required remediation:
- Required evidence:
- Accepted exceptions:
- Residual risk:
- Reverification required:
- Precise claim:
