# Frontend Privacy and Analytics Review Record

## Context

- Application/feature:
- Repository:
- Analytics providers:
- Error/telemetry providers:
- Consent manager:
- Accepted privacy/consent policy:
- Event catalog:
- Retention policy/evidence:
- Applicable `AGENTS.md`:
- Reviewer/date:

## Scope

- Included:
- Excluded:
- Routes/features:
- User/account types:
- Environments:
- Policy gaps:
- Blockers:

## Event Inventory

| Event | Trigger | Purpose | Provider | Consent | Identifier | Payload |
|---|---|---|---|---|---|---|
| | | | | | | |

## Findings

### PRIV-001 — [Title]

- Status: CONFIRMED / LIKELY_REQUIRES_VALIDATION / POLICY_DECISION_REQUIRED / EVIDENCE_REQUIRED / NOT_APPLICABLE
- Priority: BLOCKING / HIGH / MEDIUM / LOW / ADVISORY
- Surface:
- Data collected:
- Purpose:
- Policy/consent requirement:
- Actual behavior:
- Provider:
- Impact:
- Remediation:
- Verification:
- Owner:

## Roadmap Evaluation — Page Tracking

- Event name:
- Trigger:
- Initial page:
- SPA route changes:
- Duplicate events:
- URL/path:
- Query/hash:
- Sensitive URL data:
- Semantic page name:
- Consent gate:
- User ID:
- Provider boundary:
- Result:

## Roadmap Evaluation — Form Field Capture

- Forms:
- Raw values captured:
- Sensitive fields:
- Free text:
- Password/payment fields:
- Autocapture:
- Session replay:
- Masking:
- Approved metadata:
- Consent:
- Result:

## Roadmap Evaluation — Consent Withdrawal

- Consent source:
- Initial unknown state:
- SDK initialization:
- Withdraw UI:
- Application state updated:
- Provider opt-out/disable:
- Replay stopped:
- Queued events:
- Provider cookies/IDs:
- Re-grant behavior:
- Result:

## Roadmap Evaluation — User Identifier

- Identifier:
- Purpose:
- Raw email/username:
- Internal ID:
- Analytics-specific ID:
- Hashed:
- Hash treated as anonymization:
- Tenant/org ID:
- Anonymous→known merge:
- Logout reset:
- Account switch:
- Tenant switch:
- Result:

## Roadmap Evaluation — Debug Logging

- console logs:
- event payload dumps:
- provider debug mode:
- error breadcrumbs:
- raw URLs:
- form values:
- tokens/secrets:
- production behavior:
- Result:

## Roadmap Evaluation — Third-Party SDK

| Provider | Purpose | Auto-collection | Storage/cookies | Consent gate | Disable/withdraw | Retention owner |
|---|---|---|---|---|---|---|
| | | | | | | |

- Direct SDK calls outside adapter:
- Provider-specific code in Infrastructure:
- Runtime initialization order:
- Consent bypass:
- Data contract:
- Result:

## Data Minimization

| Event | Current field | Necessary | Remove/transform |
|---|---|---|---|
| | | | |

- Raw domain objects:
- Full API responses:
- Full URL:
- Form state:
- Free text:
- Customer-readable names:

## PII / Sensitive Classification

| Field | Classification | Purpose | Approved |
|---|---|---|---|
| | KNOWN_SENSITIVE / POTENTIALLY_IDENTIFYING / NON_SENSITIVE_BY_POLICY / CLASSIFICATION_REQUIRED | | |

## Provider Boundary

```text
Presentation/Application
→ analytics event contract
→ analytics adapter
→ provider SDK
```

- Application-owned event contract:
- Consent gate location:
- Payload policy location:
- Direct provider imports:
- Provider mapping:
- Failure isolation:

## Retention

- Requirement:
- Provider setting:
- Evidence:
- Owner:
- Unknown:
- Required follow-up:

## Environment Separation

- Development:
- Staging:
- Production:
- Test/synthetic users:
- Production data pollution:
- Provider projects separated:

## Error / Diagnostic Telemetry

- User context:
- URL:
- breadcrumbs:
- request metadata:
- DOM/screenshot:
- scrubbing:
- consent/policy:
- retention:
- provider:

## Testing

| Behavior | Boundary | Evidence |
|---|---|---|
| consent denied | | |
| consent unknown | | |
| withdrawal | | |
| payload minimization | | |
| page URL sanitization | | |
| user reset | | |
| provider initialization | | |

## Security Handoff

- XSS/script/token/security issues:
- `reviewing-frontend-security` required:
- Secret/provider security finding:

## Over/Under-Review Audit

- legal requirement invented:
- retention invented:
- all IDs forbidden:
- raw URL tracking:
- raw form capture:
- consent bypass:
- withdrawal incomplete:
- provider autocapture:
- raw debug payload:
- Decision: PROPORTIONATE_PRIVACY_ANALYTICS_REVIEW / OVERCLASSIFIED_PRIVACY_RISK / POLICY_REQUIRED

## Final Decision

- Decision:
- Blocking findings:
- Required policy decision:
- Required frontend remediation:
- Required provider change:
- Required retention evidence:
- Security handoff:
- Residual uncertainty:
