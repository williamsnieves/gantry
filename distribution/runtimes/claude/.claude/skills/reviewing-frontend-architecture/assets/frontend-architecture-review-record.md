# Frontend Architecture Review Record

## Context

- Change/PR:
- Scope:
- Repository/application:
- Selected architecture profile:
- Accepted behavior/spec:
- Architecture validation record:
- Styling profile:
- Accessibility design:
- Test strategy:
- Performance evidence:
- Security/privacy context:
- Applicable `AGENTS.md`:
- Reviewed by/date:

## Readiness

- Profile known:
- Accepted behavior known:
- Validation evidence available:
- Accessibility evidence:
- Performance evidence:
- Security context:
- Initial status:
- Conditions/blockers:

## Review Summary

- Final status:
- Blocking findings:
- High findings:
- Medium findings:
- Low findings:
- Advisories:
- Accepted deviations:
- Residual risks:

## Findings

| ID | Severity | Classification | Location | Rule evidence | Impact | Minimal remediation |
|---|---|---|---|---|---|---|
| | BLOCKER/HIGH/MEDIUM/LOW/ADVISORY | MANDATORY_INVARIANT/DEFAULT_CONVENTION/PROJECT_POLICY/ACCEPTED_DEVIATION/SUGGESTION | | | | |

## Architecture Profile Fit

- Selected profile still proportionate:
- Under-structured signals:
- Over-structured signals:
- Profile change required:
- Reason/evidence:

## Capability and Ownership

- Recognizable business capability:
- Feature ownership:
- Cross-feature collaboration:
- Public surfaces:
- Shared ownership:
- Unclear ownership:

## Domain

- Applicable:
- Business invariants:
- Framework/browser independence:
- Over-modeling:
- DTO/provider leakage:
- Findings:

## Application

- Applicable:
- User-intention Use Cases:
- Orchestration:
- Ports:
- DTO boundaries:
- Ceremony/forwarding-only concerns:
- Findings:

## Infrastructure

- Mapping:
- Error translation:
- Cancellation/races:
- Provider leakage:
- Business-rule leakage:
- Retry policy:
- Findings:

## Presentation

- Component responsibility:
- Hook responsibility:
- Business-rule leakage:
- Direct data access:
- God component/hook:
- Rendering states:
- Typed props/public API:
- Findings:

## State and Async

- Valid state model:
- Contradictory booleans:
- Derived state duplication:
- Server/local state duplication:
- Race behavior:
- Cancellation:
- Duplicate commands:
- Optimistic behavior:
- Findings:

## Effects

| Effect/use | External system | Necessary | Dependencies/cleanup | Finding |
|---|---|---|---|---|
| | | | | |

- Derivation-in-Effect:
- Event-via-Effect:
- Dependency suppression:
- Cleanup:
- Stale closure:

## Composition

- Outer boundary:
- Concrete dependency selection:
- Shared lifecycle:
- User/request scope:
- Service Locator:
- Server/client roots:
- Test overrides:
- Findings:

## UI and Styling

- Styling profile respected:
- Tokens:
- Variants:
- Global CSS:
- Runtime inline values:
- `!important` exceptions:
- Shared UI ownership:
- Vendor primitive policy:
- Findings:

## Accessibility

- Target:
- Semantic HTML:
- Accessible names:
- Keyboard:
- Focus:
- Disabled/invalid:
- Color-independent meaning:
- Contrast:
- Zoom/reflow:
- Reduced motion:
- Complex widgets:
- Status messages:
- Automated/manual evidence:
- Findings:

## Errors and Recovery

| Condition | User-facing behavior | Recovery | Finding |
|---|---|---|---|
| Validation | | | |
| Authorization | | | |
| Not found | | | |
| Network | | | |
| Server | | | |
| Cancellation | | | |
| Semantic rejection | | | |

## Testing

- Domain:
- Use Case:
- Adapter:
- Hook:
- Component:
- Accessibility:
- Visual:
- E2E:
- Duplication:
- Test doubles:
- Flakiness:
- Regression:
- Findings:

## Performance

| Concern | Evidence | User impact | Classification |
|---|---|---|---|
| | | | |

- Core Web Vitals:
- Bundle:
- Route loading:
- Render frequency:
- Network waterfall:
- Long tasks:
- Memory:
- Duplicate requests:
- Third-party cost:
- Speculative findings downgraded appropriately:

## Security and Privacy

- Secrets in bundle:
- Untrusted HTML:
- Token storage:
- Stack traces:
- Client-only authorization assumption:
- Analytics/consent:
- PII/logging:
- Third-party scripts:
- Findings:

## Maintainability and Abstractions

- Naming/product language:
- Catch-all helpers:
- DRY:
- YAGNI:
- SOLID used proportionately:
- Shared abstractions:
- Comment quality:
- Findings:

## Brownfield / Migration Context

- Legacy constraints:
- Incremental improvement:
- Target direction:
- Temporary mixed boundaries:
- Exit trigger:
- Out-of-scope legacy intentionally untouched:

## Accepted Deviations

| Deviation | Classification | Reason | Owner | Expiry/removal trigger |
|---|---|---|---|---|
| | ACCEPTED_PERMANENT_DEVIATION/ACCEPTED_TEMPORARY_DEVIATION/MIGRATION_DEVIATION/THIRD_PARTY_DEVIATION/DEVIATION_REQUIRES_APPROVAL/UNJUSTIFIED_DEVIATION | | | |

## Definition of Done

| Area | Requirement | Applicable | Status | Evidence |
|---|---|---|---|---|
| Architecture | recognizable capability | | | |
| Architecture | inward dependency direction | | | |
| Architecture | no feature-boundary bypass | | | |
| Architecture | profile respected | | | |
| Architecture | shared abstractions justified | | | |
| Behavior | accepted states | | | |
| Behavior | race/cancellation | | | |
| UI | semantics/keyboard/focus | | | |
| UI | responsive/theme | | | |
| Data | mapping/validation/errors | | | |
| Testing | relevant tests | | | |
| Quality | lint/type/tests/build | | | |
| Quality | performance | | | |
| Quality | security/privacy | | | |
| Quality | docs/rules updated | | | |

## Suggestions

| Suggestion | Benefit | Optional |
|---|---|---|
| | | yes |

## Final Decision

- Status:
- Required changes:
- Advisories:
- Accepted deviations:
- Residual risks:
- Next skill:
