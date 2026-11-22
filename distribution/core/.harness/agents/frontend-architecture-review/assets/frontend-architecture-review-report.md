# Frontend Architecture Review Report

## Gate Decision

- Status: APPROVE / APPROVE_WITH_ADVISORIES / CHANGES_REQUESTED / BLOCKED_PENDING_DECISION / BLOCKED_PENDING_EVIDENCE
- Readiness: READY_TO_REVIEW_FRONTEND_ARCHITECTURE / READY_WITH_CONDITIONS / ARCHITECTURE_PROFILE_REQUIRED / ACCEPTED_BEHAVIOR_REQUIRED / VALIDATION_EVIDENCE_REQUIRED / ACCESSIBILITY_EVIDENCE_REQUIRED / PERFORMANCE_EVIDENCE_REQUIRED / SECURITY_CONTEXT_REQUIRED / BLOCKED
- Review version:
- Reviewer:
- Date:
- Target change / PR:
- Scope: FEATURE / VERTICAL_SLICE / ROUTE / PACKAGE / APPLICATION / MIGRATION / PR_CHANGESET
- Selected profile:
- Re-review required: yes/no

## Authoritative Basis

- Applicable `AGENTS.md`:
- Accepted requirement / OpenSpec:
- Frontend engineering standard:
- Decision register / project policy:
- Accepted deviations:
- Architecture validation record:
- Frontend Code Review:
- Known unresolved product/architecture decisions:

## Architecture Profile Fit

- Selected profile:
- Why it fits:
- Change remains within profile:
- Heavier profile introduced accidentally:
- Profile decision required:

## Rule Classification Summary

| Rule / concern | Classification | Evidence | Result |
|---|---|---|---|
| | MANDATORY_INVARIANT / DEFAULT_CONVENTION / PROJECT_POLICY / ACCEPTED_DEVIATION / SUGGESTION / NO_ISSUE | | |

## Feature / Ownership Map

```text
feature / route
→ presentation
→ hook/application behavior
→ semantic port
→ infrastructure adapter
→ external API
```

- Feature owner:
- Shared ownership:
- Cross-feature dependencies:
- Composition boundary:

## Dependency / Boundary Review

| Boundary | Expected direction | Observed direction | Result |
|---|---|---|---|
| Presentation → Application | | | |
| Application → Domain/Ports | | | |
| Infrastructure → inward contracts | | | |
| Feature → shared/public contracts | | | |

## State / Effects / Server State

### State Ownership
- Local UI:
- Remote/server state:
- Feature/application state:
- Global/cross-route state:
- Persistent preference:
- Ownership concerns:

### Effects
- Synchronization responsibilities:
- Hidden business logic:
- Derived-state effects:
- Lifecycle/cleanup:
- Architectural concern:

### Server State
- Ownership:
- Cache/invalidation:
- Mutation/retry/rollback:
- UI-state leakage:

## Composition / Lifecycle

- Dependency selection location:
- Adapter construction:
- Provider/context ownership:
- Singleton/request/feature lifecycle:
- Test replacement points:
- Concerns:

## UI / Styling / Shared Abstractions

- Selected styling profile:
- Design-system primitive usage:
- Tokens/variants:
- Shared abstraction justification:
- Cross-profile mixing:
- Concerns:

## Accessibility Architecture

- Semantic primitive ownership:
- Keyboard:
- Focus:
- Form/error semantics:
- Modal/menu/dialog behavior:
- Evidence:
- Concerns:

## Error Semantics

```text
transport error
→ application/infrastructure meaning
→ presentation state
→ recovery
```

- Provider leakage:
- User-facing semantics:
- Recovery ownership:

## Test Strategy

| Responsibility | Expected evidence | Actual evidence | Result |
|---|---|---|---|
| Pure/domain/application logic | | | |
| Adapter | | | |
| Hook | | | |
| Component | | | |
| E2E/user journey | | | |

- Over-mocking:
- E2E overreach:
- Duplicate evidence:
- Missing architectural test boundary:

## Performance

- React Compiler enabled:
- Manual memoization concern:
- Render architecture:
- Request architecture:
- Bundle/loading architecture:
- Evidence required:
- Finding/advisory:

## Security / Privacy

### Security
- Client secrets:
- Authorization boundary:
- Unsafe rendering/navigation:
- External-data validation:
- Concerns:

### Privacy / Analytics
- Sensitive data storage:
- Analytics:
- URLs/logging:
- Consent/policy:
- Concerns:

## Brownfield / Migration / Deviations

| Deviation / seam | Type | Scope | Owner | Exit/removal trigger | Valid? |
|---|---|---|---|---|---|
| | ACCEPTED_PERMANENT_DEVIATION / ACCEPTED_TEMPORARY_DEVIATION / MIGRATION_DEVIATION / THIRD_PARTY_DEVIATION / DEVIATION_REQUIRES_APPROVAL / UNJUSTIFIED_DEVIATION | | | | |

## Architecture Findings

### FAR-001 — [Title]

- Severity: BLOCKER / HIGH / MEDIUM / LOW / ADVISORY
- Classification: MANDATORY_INVARIANT / DEFAULT_CONVENTION / PROJECT_POLICY / ACCEPTED_DEVIATION / SUGGESTION / NO_ISSUE
- Category: PROFILE_FIT / OWNERSHIP / DEPENDENCY_DIRECTION / DOMAIN_APPLICATION / INFRASTRUCTURE_BOUNDARY / COMPOSITION / STATE_OWNERSHIP / EFFECTS / SERVER_STATE / UI_STYLING / SHARED_UI / ACCESSIBILITY / ERROR_SEMANTICS / TEST_STRATEGY / PERFORMANCE / SECURITY / PRIVACY / ABSTRACTION / MIGRATION / ARCHITECTURAL_DRIFT / DEVIATION
- Confidence: HIGH / MEDIUM / LOW
- Rule evidence:
- Location / scope:
- Problem:
- Architectural / user impact:
- Failure / evolution scenario:
- Minimal remediation:
- Related Frontend Code Review finding:
- Blocking: yes/no
- Handoff / owner:

## Advisories

### ADV-001 — [Suggestion]

- Classification: SUGGESTION
- Evidence:
- Potential benefit:
- Why non-blocking:

## Decision / Evidence Questions

| ID | Question/evidence | Why needed | Blocking? | Route |
|---|---|---|---|---|
| | | | | Product / Design / Architecture / Accessibility / Performance / Security |

## Validation Evidence

| Evidence | Status | Source | Architecture implication |
|---|---|---|---|
| Frontend architecture validation | PASSED / FAILED / BLOCKED / UNAVAILABLE / INCONCLUSIVE | | |
| Frontend Code Review | | | |
| Accessibility | | | |
| Performance | | | |
| Security/privacy | | | |
| Tests | | | |

## Residual Architecture Risk

- Accepted trade-offs:
- Pre-existing debt not worsened:
- Conditional risks:
- Evidence gaps:
- Future trigger for heavier profile:

## Handoffs

| Finding/question | Recipient | Expected output | Blocking | Re-entry condition |
|---|---|---|---|---|
| | Implementation / Frontend Code Review / Validator / QA / Accessibility / Security / Performance / Detail Analyst / Reviewer / Product / Architecture Owner | | yes/no | |

## Architecture Review Summary

- Blockers:
- High:
- Medium:
- Low:
- Advisories:
- Blocking decisions:
- Blocking evidence:
- Accepted deviations:
- Why final status is justified:

## Exact Next Action

-
