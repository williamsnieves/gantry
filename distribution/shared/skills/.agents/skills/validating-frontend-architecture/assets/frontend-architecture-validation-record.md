# Frontend Architecture Validation Record

## Context

- Change/repository:
- Scope:
- Selected architecture profile:
- Repository/application:
- Feature/package ownership:
- Public-surface policy:
- Composition policy:
- Server/client policy:
- Existing architecture tooling:
- Applicable `AGENTS.md`:
- Validated by/date:

## Readiness

- Profile explicit:
- Ownership explicit:
- Public surfaces defined:
- Shared-code policy defined:
- Server/client policy defined:
- Tooling discoverable:
- Initial status:
- Conditions/blockers:

## Validation Scope

| Area | In scope | Evidence source |
|---|---|---|
| Dependency direction | | |
| Cross-feature imports | | |
| Public surfaces | | |
| Shared code | | |
| Components/hooks | | |
| Composition | | |
| Server/client | | |
| Package boundaries | | |
| Cycles | | |
| Automation | | |

## Profile Rules

### Selected Profile

- Profile:
- Expected structure:
- Mandatory boundaries:
- Rules intentionally not applicable:
- Repository-local refinements:

## Dependency Direction Matrix

| From | To | Expected | Actual evidence | Status |
|---|---|---|---|---|
| | | ALLOWED/FORBIDDEN/CONDITIONAL | | PASS/FAIL/UNKNOWN |

## Layer Findings

| File/module | From layer | Imported target | Rule | Status |
|---|---|---|---|---|
| | | | | |

- Domain violations:
- Application violations:
- Infrastructure ownership issues:
- Profile-A non-applicable layer rules:

## Components and Hooks

| Source | Imported dependency | Classification | Result |
|---|---|---|---|
| | | concrete adapter / semantic dependency / public surface / global factory | |

- Concrete repository imports:
- HTTP adapter imports:
- Global Factory/Service Locator:
- Server-only imports:

## Cross-Feature Boundaries

| Importing feature | Imported feature/path | Boundary type | Status |
|---|---|---|---|
| | | PUBLIC_SURFACE_IMPORT / INTENTIONAL_SHARED_CONTRACT / INTERNAL_BOUNDARY_BYPASS / TEMPORARY_MIGRATION_EXCEPTION | |

## Public Surfaces

| Feature/package | Supported surface | Internal exposure | Barrel/cycle risk | Status |
|---|---|---|---|---|
| | | | | |

- Overbroad barrels:
- Deep imports:
- Package exports:
- Type-only public leakage:

## Shared Code

| Shared artifact | Consumers | Semantic owner | Classification | Status |
|---|---|---|---|---|
| | | | JUSTIFIED_SHARED/FEATURE_OWNED_MISPLACED_IN_SHARED/SPECULATIVE_SHARED/GENERIC_HELPER_DUMP/SHARED_CONTRACT_WITH_OWNER | |

- Shared dumping-ground patterns:
- Feature code misplaced in shared:
- Speculative abstractions:

## Composition

- Composition root location:
- Concrete implementation selection:
- Component/hook direct construction:
- Domain/Application composition imports:
- Service Locator patterns:
- Dependency lifecycle violations:

## Server / Client Boundary

| Source | Runtime | Imported target | Classification | Status |
|---|---|---|---|---|
| | SERVER/CLIENT/ISOMORPHIC | | SERVER_ONLY_LEAK_TO_CLIENT/CLIENT_ONLY_LEAK_TO_SERVER/NON_SERIALIZABLE_BOUNDARY_LEAK/SAFE_SPLIT_ENTRYPOINT | |

- Secret leakage:
- Browser API server leakage:
- Request/global state:
- Serializable boundary:

## Package Boundaries

| Consumer | Dependency | Import path | Public/deep | Direction status |
|---|---|---|---|---|
| | | | | |

- Reverse package dependencies:
- TS reference mismatch:
- App-specific implementation leakage:
- Server/client entry points:

## Circular Dependencies

| Cycle | Type | Production impact | Cause | Status |
|---|---|---|---|---|
| | DIRECT_FILE_CYCLE/FEATURE_CYCLE/PACKAGE_CYCLE/BARREL_CYCLE/TYPE_ONLY_CYCLE/FALSE_POSITIVE_OR_TOOL_LIMITATION | | | |

## Special Import Classification

### Test-Only

- Findings:
- Production impact:

### Type-Only

- Findings:
- Contract leakage:

### Dynamic Imports

- Findings:
- Code-splitting versus boundary bypass:

### Generated Code

- Findings:
- Provider-type leakage:
- Accepted exception:

## Existing Automation

| Tool/check | Rule/scope | CI stage | Result | Coverage gap |
|---|---|---|---|---|
| ESLint | | | | |
| dependency-cruiser | | | | |
| Nx boundaries | | | | |
| Madge/cycle tool | | | | |
| TS project references | | | | |
| package exports | | | | |
| architecture tests | | | | |

## Automation Gap Matrix

| Architecture rule | Enforcement | Risk if manual | Recommendation |
|---|---|---|---|
| | AUTOMATED_AND_BLOCKING/AUTOMATED_NON_BLOCKING/PARTIALLY_AUTOMATED/MANUAL_ONLY/NOT_ENFORCED | | |

## Findings

| ID | Severity | Evidence | Violated rule | Consequence | Smallest remediation |
|---|---|---|---|---|---|
| | BLOCKER/HIGH/MEDIUM/LOW/ADVISORY | | | | |

## Exceptions

| Rule/path | Classification | Reason | Owner | Removal trigger |
|---|---|---|---|---|
| | VALID_EXCEPTION/TEMPORARY_MIGRATION_EXCEPTION/TOOL_FALSE_POSITIVE/UNJUSTIFIED_EXCEPTION/POLICY_REQUIRES_UPDATE | | | |

## Architecture Definition of Done

| Requirement | Status | Evidence |
|---|---|---|
| Recognizable business capability | | |
| Dependency direction inward | | |
| No internal feature boundary bypass | | |
| Selected profile respected | | |
| Shared abstractions justified | | |

## Residual Risks

| Risk/gap | Impact | Owner | Blocking |
|---|---|---|---|
| | | | |

## Final Decision

- Status:
- Blocking findings:
- Non-blocking advisories:
- Automation gaps:
- Required remediation:
- Next skill:
