# Backend Code Review Report

## Context

- Change/PR:
- Specification:
- Repository/service:
- Review scope:
- Changed modules/layers:
- Governing standard:
- Repository-local rules:
- Accepted decisions/exceptions:
- Reviewer/date:

## Change Understanding

- Trigger:
- Accepted behavior:
- Actor/tenant:
- Inputs:
- Domain decision:
- State changes:
- External side effects:
- Public output:
- Migration/compatibility:
- Out of scope:

## Scope Classification

| Area/file | Classification | Reviewed | Notes |
|---|---|---|---|
| | IN_CHANGED_SCOPE/DIRECTLY_AFFECTED/PRE_EXISTING_ADJACENT/UNRELATED | | |

## Validation Evidence

| Command/check | Executed | Result | Scope/limitation |
|---|---|---|---|
| | | PASSED/FAILED/BLOCKED/UNAVAILABLE/NOT_APPLICABLE/INCONCLUSIVE | |

## Correctness Review

- Happy path:
- Failure paths:
- Boundary values:
- State preservation after rejection:
- Absence/null behavior:
- Error propagation:
- Output mapping:
- Duplicate/retry behavior:
- Findings:

## Architecture Review

- Domain boundaries:
- Application boundaries:
- Repository ports/adapters:
- External ports/adapters:
- Controller thinness:
- Use Case chaining:
- DTO/Entity leakage:
- Composition:
- Cycles/transitive dependencies:
- Findings:

## Security and Privacy

- Authentication:
- Authorization:
- Tenant isolation:
- Input validation:
- Secret handling:
- PII/data minimization:
- Logging/redaction:
- Public error safety:
- Test-only overrides:
- Findings:

## Persistence, Transactions, and Migration

- Authoritative constraints:
- Transaction owner:
- Concurrency/versioning:
- Partial failure:
- Data mapping/reconstitution:
- Unknown/legacy data:
- Migration order:
- Backfill/rollback:
- Mixed-version deployment:
- Findings:

## External Integrations

- Provider-neutral boundary:
- Request/response mapping:
- Failure translation:
- Timeout:
- Retry:
- Rate limit:
- Idempotency:
- Ambiguous outcome:
- Reconciliation:
- Credentials/account:
- Findings:

## HTTP Contract

- Route/method:
- Request validation:
- Trusted context:
- Status/body/headers:
- Error mapping:
- Internal detail leakage:
- Idempotency contract:
- Findings:

## Testing Review

- Domain tests:
- Use Case tests:
- Repository integration:
- External adapter evidence:
- HTTP E2E:
- Determinism:
- Test isolation/cleanup:
- Missing cases:
- False-confidence risks:
- Findings:

## Operability and Maintainability

- Startup/config:
- Readiness/shutdown:
- Observability:
- Resource lifecycle:
- Hidden global state:
- Duplicated rules/mappings:
- Complexity and ownership:
- Temporary seams/debt:
- Findings:

## Findings

### BE-REV-001 — <title>

- Severity:
- Category:
- Confidence:
- Status:
- Scope:
- Rule/accepted behavior:
- Evidence:
- Failure scenario:
- Impact:
- Remediation direction:
- Validation after remediation:

## Questions and Decisions Required

| Question | Why it matters | Owner | Blocking |
|---|---|---|---|
| | | | |

## Positive Evidence

- 

## Findings Summary

| Severity | Count |
|---|---|
| Critical | |
| High | |
| Medium | |
| Low | |

- New:
- Worsened:
- Pre-existing blocking:
- Pre-existing non-blocking:
- Accepted temporary:
- Fixed:

## Final Decision

- Decision:
- Blocking findings:
- Conditions:
- Missing evidence:
- Residual risks:
- Recommended next skill:
