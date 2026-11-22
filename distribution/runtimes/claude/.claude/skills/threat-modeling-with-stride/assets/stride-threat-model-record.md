# STRIDE Threat Model Record

## Context

- System/feature:
- Repository/application:
- Architecture reference:
- Environment(s):
- Scope:
- Excluded scope:
- Critical journey(s):
- Existing security policy:
- Applicable `AGENTS.md`:
- Owner/date/version:

## Assets

| Asset | Sensitivity | Integrity need | Availability need | Owner |
|---|---|---|---|---|
| | | | | |

## Actors / Roles

| Actor | Trust level | Capabilities | Authentication |
|---|---|---|---|
| | | | |

## Entry Points

| Entry point | External/internal | Auth required | Privileged |
|---|---|---|---|
| | | | |

## Trust Boundaries

| Boundary | From | To | Trust change |
|---|---|---|---|
| | | | |

## Data Flows

| Flow | Source | Destination | Data | Protection / validation |
|---|---|---|---|---|
| | | | | |

## Data Stores

| Store | Data | Access | Integrity/confidentiality | Retention |
|---|---|---|---|---|
| | | | | |

## Privileges

| Capability | Allowed actor(s) | Enforcement point |
|---|---|---|
| | | |

## Security Assumptions

| Assumption | Owner | Enforced where | Verification |
|---|---|---|---|
| | | | |

## Threat Inventory

### THREAT-001 — [Title]

- STRIDE category/categories:
- Plausibility: PLAUSIBLE / CONDITIONAL / THEORETICAL_LOW_RELEVANCE / NOT_APPLICABLE
- Asset:
- Actor:
- Entry point:
- Trust boundary:
- Preconditions:
- Attack path:
- Impact:
- Existing controls:
- Control status: IMPLEMENTED_VERIFIED / IMPLEMENTED_NOT_VERIFIED / PLANNED / PARTIAL / MISSING / NOT_APPLICABLE
- Severity: CRITICAL / HIGH / MEDIUM / LOW / ADVISORY
- Mitigation:
- Owner:
- Verification:
- Residual risk:
- Lifecycle: OPEN / MITIGATION_PLANNED / PARTIALLY_MITIGATED / MITIGATED_PENDING_VERIFICATION / VERIFIED / ACCEPTED_RISK / NOT_APPLICABLE

## STRIDE Coverage

### Spoofing
- Identity boundaries:
- Threats:
- Mitigations:

### Tampering
- Commands/data/artifacts:
- Threats:
- Mitigations:

### Repudiation
- Privileged/security actions:
- Audit evidence:
- Threats:

### Information Disclosure
- Sensitive data:
- Cross-tenant paths:
- Logs/analytics:
- Threats:

### Denial of Service
- Public/expensive paths:
- Resource limits:
- Provider dependency:
- Algorithmic DoS:
- Need `analyzing-algorithmic-complexity`:

### Elevation of Privilege
- Roles/capabilities:
- Resource ownership:
- Service/CI IAM:
- Admin/support:
- Threats:

## Authentication Flow

```text

```

- Identity source:
- Token/session:
- Replay:
- Redirect/callback:
- Refresh/logout:

## Authorization / Tenant Boundary

```text

```

- Identity source:
- Tenant source:
- Resource ownership:
- Policy enforcement:
- Client-controlled identifiers:
- Cross-tenant negative case:
- Least privilege:

## Third-Party Integrations

| Provider | Data sent | Auth/scopes | Webhook | Availability dependency |
|---|---|---|---|---|
| | | | | |

## Webhooks

- Applicable:
- Sender authentication/signature:
- Replay/idempotency:
- Flood controls:
- Audit correlation:

## File Upload / Download

- Applicable:
- Type/size:
- Validation:
- Storage ACL:
- Processing/parser:
- Malicious content:
- Download authorization:
- Resource limits:

## Browser / Frontend Boundary

- XSS/DOM injection surface:
- Token/session storage:
- Redirects:
- postMessage/iframe:
- third-party scripts:
- CSP:
- client-only authorization assumptions:

## Infrastructure / IAM

- Public ingress:
- Service identities:
- Cloud IAM:
- Secrets:
- Storage exposure:
- Egress:
- Admin pathways:
- Backups:

## CI/CD / Supply Chain

- CI identity:
- Fork/PR trust:
- Deploy credentials:
- Artifact integrity:
- Registry/dependencies:
- Secret exposure:
- Provenance/signing:

## DoS / Resource Exhaustion

| Surface | Attacker-controlled input | Resource | Limit | Mitigation |
|---|---|---|---|---|
| | | | | |

## Mitigation Plan

| Threat | Mitigation | Owner | Status | Verification |
|---|---|---|---|---|
| | | | | |

## Security Requirements

```text

```

## Verification Matrix

| Requirement / threat | Test/evidence boundary | Expected evidence |
|---|---|---|
| | | |

## Residual Risk

| Threat | Residual status | Rationale | Owner |
|---|---|---|---|
| | ACCEPTED / TRANSFERRED / REDUCED / UNRESOLVED / UNKNOWN | | |

## OWASP / CWE / ASVS Follow-Up

- OWASP/CWE application review required:
- ASVS control verification required:
- Next security skill:

## Over/Under-Threating Audit

- STRIDE forced mechanically:
- Duplicate root-cause threats:
- Implausible threats:
- Trust boundaries missing:
- Tenant boundary missing:
- Privileged operations missing:
- Third-party paths missing:
- DoS limits missing:
- Decision: PROPORTIONATE_THREAT_MODEL / OVERMODELED_THREATS / THREAT_MODEL_TOO_GENERIC / THREAT_MODEL_INCOMPLETE

## Final Decision

- Decision:
- Critical threats:
- Required mitigations:
- Required architecture clarification:
- Required verification:
- Required handoff:
