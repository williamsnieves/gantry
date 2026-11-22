# React Feature Refactoring Record

## Context

- Feature:
- Repository:
- Selected architecture profile:
- Framework/version:
- React Compiler status:
- Server-state strategy:
- HTTP/repository strategy:
- Accessibility primitives/design system:
- Applicable `AGENTS.md`:
- Refactor owner/date:

## Behavior Preservation

- User-visible behavior:
- Route behavior:
- Network/business outcome:
- Loading/error/retry:
- Accessibility behavior:
- Existing tests:
- Characterization gaps:
- Characterization added:

## Responsibility Inventory

| Current module | Responsibility | Current owner | Target owner |
|---|---|---|---|
| | rendering / interaction / React state / server state / Application / Domain / mapping / HTTP / navigation / analytics / effect / accessibility / styling | | |

## Refactor Decisions

| Problem | Decision | Reason | Behavior risk |
|---|---|---|---|
| | KEEP_COHESIVE / SPLIT_COMPONENT / SPLIT_HOOK / MOVE_TO_APPLICATION / MOVE_TO_INFRASTRUCTURE / MOVE_TO_FEATURE / REDUCE_SHARED_ABSTRACTION / REMOVE_DUPLICATE_ASYNC_STATE / REPLACE_WITH_ACCESSIBLE_PRIMITIVE | | |

## Oversized Component

- Component:
- Lines:
- Independent responsibilities:
- Business rules:
- Infrastructure access:
- Async workflows:
- Semantic regions:
- Accessibility patterns:
- Proposed split:
- Keep cohesive areas:
- Props/events:
- Validation:

## God Hook

- Hook:
- Claimed responsibility:
- Actual responsibilities:
- Resources fetched:
- Local states:
- Application behavior:
- Navigation:
- Analytics:
- Concrete dependencies:
- Return API size:
- Raw setters:
- Split/keep decision:
- Race/cancellation semantics:
- Target hook/API:

## Direct Fetch / Data Boundary

- Direct fetch/vendor usage:
- Current location:
- Existing approved HTTP client:
- Repository/adapter:
- Server-state library:
- Fetch-on-mount Effect:
- Target boundary:
- DTO/runtime validation:
- Error taxonomy:
- Cancellation:
- Result:

## Shared Abstraction Overreach

- Shared module:
- Current consumers:
- Business semantics:
- Feature imports:
- Feature flags/variant explosion:
- Neutral core:
- Feature wrapper:
- Re-own to feature:
- Duplication accepted:
- Result:

## Async State Ownership

- Remote concern:
- Primary owner:
- Server-state library:
- Local mirrored data:
- Local mirrored loading:
- Local mirrored error:
- Legit local draft:
- Semantic derived state:
- Impossible combinations:
- Target representation:
- Optimistic owner:
- Hydration:
- Result:

## Effects

| Effect | External synchronization? | Replacement/owner |
|---|---|---|
| | | render derivation / event handler / server-state / custom hook / keep |

- Exhaustive-deps issues:
- Cleanup:
- Stale closure/race:
- Removed derivation Effects:

## Inaccessible Custom Widget

- Widget:
- Current semantics:
- Native alternative:
- Existing design-system primitive:
- Headless primitive:
- Custom still necessary:
- Accessible name:
- Role:
- Keyboard:
- Focus:
- Escape/dismiss:
- Status/errors:
- Mobile/pointer:
- Tests:
- Manual/browser verification:
- Result:

## Mapping / View Data

- API DTO leaked to UI:
- Mapper location:
- View-data contract:
- Formatting ownership:
- Business interpretation removed from UI:

## Public / Internal Contracts

- Public component props preserved:
- Feature public API:
- Internal signatures changed:
- Route/query/storage/event contracts:
- Compatibility needed:

## Incremental Sequence

### Step 1
- Change:
- Tests:
- Validation:
- Rollback:

### Step 2
- Change:
- Tests:
- Validation:
- Rollback:

### Step 3
- Change:
- Tests:
- Validation:
- Rollback:

## Validation

- Lint:
- Typecheck:
- Unit:
- Component:
- Hook:
- Adapter:
- Build:
- Critical E2E:
- Accessibility:
- Architecture:
- Performance:
- Security/privacy:
- Result:

## Obsolete Code

- Duplicate async state removed:
- Old Effect removed:
- Old shared abstraction removed:
- Old service method removed:
- Compatibility alias removed:
- Dead code handoff:

## Over/Under-Refactoring Audit

- Split by line count:
- Tiny wrapper components:
- Cohesive hook fragmented:
- Premature generic abstraction:
- Manual memoization added:
- Unrelated behavior change:
- Direct fetch remains:
- Duplicated async state remains:
- Inaccessible widget remains:
- Decision: PROPORTIONATE_REFACTOR / OVER_REFACTORED / PREMATURE_ABSTRACTION / BEHAVIOR_CHANGE_MIXED_IN

## Final Decision

- Decision:
- Required characterization:
- Required component refactor:
- Required hook refactor:
- Required infrastructure boundary:
- Required async ownership fix:
- Required shared reownership:
- Required accessibility refactor:
- Required architecture validation:
- Residual risk:
