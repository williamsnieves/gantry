# Frontend User Journey Testing Record

## Context

- Journey:
- Product/domain:
- Repository/application:
- Test strategy decision:
- E2E framework:
- Environment:
- Browser support:
- Backend/test API:
- Auth system:
- External providers:
- CI tier:
- Applicable `AGENTS.md`:
- Designed/tested by/date:

## E2E Justification

- Decision: E2E_REQUIRED / ROUTE_INTEGRATION_SUFFICIENT / LOWER_BOUNDARY_SUFFICIENT / MANUAL_PRODUCTION_CHECK_ONLY / NOT_IN_SCOPE
- Business impact:
- User frequency:
- Integration breadth:
- Production incident history:
- Browser/deployment risk:
- Unique E2E evidence:
- Why lower levels are insufficient:

## Lower-Level Coverage Audit

| Behavior | Existing boundary | Already proved |
|---|---|---|
| | Domain / Use Case / Adapter / Hook / Component / Visual | |

- Duplicated branches excluded:
- Regression root boundary:

## Journey Scope

- Starting state:
- Entry route:
- Critical actions:
- Routes crossed:
- Browser capability:
- Backend boundaries:
- External provider:
- Success outcome:
- Critical failure/recovery:
- Explicitly out of scope:

## Environment Contract

- Environment: local / ephemeral preview / integration / staging / controlled sandbox / production synthetic
- Deployment readiness probe:
- Backend health:
- Migrations:
- Required flags/config:
- Base path/origin:
- Environment-specific risk:
- Production mutation prohibited:

## Test Data Isolation

- Namespace strategy:
- Per-test/per-worker:
- User:
- Tenant/org:
- Subscription/order/resource:
- Unique ID strategy:
- Shared mutable record:
- Parallel collision risk:

## Seed / Setup

| Precondition | Setup strategy | Why not UI |
|---|---|---|
| | test API / fixture / DB factory / sandbox / UI | |

- Setup itself part of journey:
- Deterministic:
- Production-only API exposed:
- Business logic duplicated in test helper:

## Cleanup

- Cleanup method:
- Idempotent:
- Handles aborted CI:
- TTL/fallback:
- Sandbox resources:
- Storage/session:
- Cleanup failure diagnostics:

## Authentication

- Login is journey risk:
- Real login UI:
- Storage state:
- Test session endpoint:
- IdP sandbox:
- MFA/SSO mechanism:
- Test-only identity:
- Credentials handling:
- State file protected:

## Feature Flags / Roles / Time

- Feature flags:
- Role/permissions:
- Locale:
- Timezone:
- Clock/date:
- Experiment targeting:
- Deterministic:

## Critical Success Flow

```text

```

### User Actions

| Step | Action | Locator strategy |
|---|---|---|
| | | role / label / text / approved test id |

### Assertions

| Step | Observable assertion | Unique integration risk |
|---|---|---|
| | | |

- Private state assertions:
- CSS/DOM structure assertions:
- Durable result verified:
- Reload/navigation verification:

## Critical Failure / Recovery

- Failure:
- Injection/setup method:
- User-visible state:
- State preserved:
- Recovery action:
- Final outcome:
- Why this failure deserves E2E:
- Other error branches kept lower:

## External Provider / Revenue Safety

- Applicable:
- Provider:
- Test/sandbox mode:
- Production credentials:
- Real charges/mutations:
- Synthetic data:
- Resource lifecycle:
- Provider outage classification:
- Separate CI tier:

## Browser Matrix

| Browser/viewport | Journey | Why |
|---|---|---|
| | | |

- Every journey x every browser avoided:
- Mobile unique interaction:
- Browser-specific risk:

## Resilience

- Semantic locators:
- Test IDs:
- Auto-wait:
- Arbitrary sleeps:
- Exact network-order coupling:
- `networkidle` dependence:
- Stable readiness condition:
- Page objects/helpers:
- Helpers remain product-language oriented:

## Diagnostics

- Trace:
- Screenshot:
- Video:
- Console errors:
- Page errors:
- Failed requests:
- Environment metadata:
- Test data/run id:
- Secrets/PII redacted:
- Artifact retention:

## CI Placement

- Tier: PR_SMOKE / PR_CRITICAL / MERGE_GATE / RELEASE_GATE / NIGHTLY / SCHEDULED_PROVIDER / PRODUCTION_SYNTHETIC
- Parallel:
- Sharded:
- Serial:
- Retry policy:
- Timeout policy:
- Expected runtime:
- Block release:
- Policy basis:

## Flake Management

- Current retry dependence:
- Classification: PRODUCT_REGRESSION / TEST_DEFECT / ENVIRONMENT_OUTAGE / PROVIDER_OUTAGE / DATA_COLLISION / TIMING_FLAKE / BROWSER_FLAKE / UNKNOWN
- Owner:
- Quarantined:
- Issue:
- Expiry/review:
- Permanent skip avoided:

## Privacy / Security

- Synthetic test identity:
- PII:
- Payment data:
- Tokens:
- Screenshots/traces:
- Test APIs protected:
- Production resources:
- Analytics/test-user exclusion:

## Regression Placement

- Incident/bug:
- Lowest defective boundary:
- Lower-level regression:
- E2E regression justified:
- Unique cross-boundary risk:

## Execution Evidence

- Focused command:
- Result:
- CI job:
- Result:
- Environment:
- Browser:
- Duration:
- Retry count:
- Failure artifacts:

## Over/Under-E2E Audit

- Every validation branch:
- Every provider error:
- Every component state:
- Every theme:
- Every locale:
- UI-only setup ceremony:
- Browser matrix explosion:
- Missing critical journey:
- Missing data isolation:
- Missing diagnostics:
- Decision: PROPORTIONATE_E2E_COVERAGE / ALL_E2E_STRATEGY / DUPLICATED_LOWER_LEVEL_COVERAGE / E2E_MATRIX_EXPLOSION

## Final Decision

- Decision:
- Conditions:
- Blocking issue:
- Next skill:
- Required follow-up:
