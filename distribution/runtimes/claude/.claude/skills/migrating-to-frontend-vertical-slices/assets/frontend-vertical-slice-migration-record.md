# Frontend Vertical Slice Migration Record

## Context

- Repository/application:
- Selected architecture profile:
- Current structure:
- Target structure:
- Migration scope:
- Capability:
- Critical behavior:
- Monorepo:
- Applicable `AGENTS.md`:
- Owner/date:

## Current-State Map

| Current path | Responsibility | Current owner | Consumers | Problems |
|---|---|---|---|---|
| | | | | |

## Capability Map

| Capability | Routes/workflows | Owned UI | Owned data/state | Status |
|---|---|---|---|---|
| | | | | |

## Behavior / Contract Protection

- User-visible behavior:
- Route contract:
- API/browser contract:
- Storage/query contract:
- Accessibility behavior:
- Existing tests:
- Characterization needed:
- Characterization added:
- Critical E2E affected:

## Target Slice

```text

```

- Profile justified:
- Ceremonial layers avoided:
- Domain needed:
- Application needed:
- Infrastructure needed:
- Components/hooks:
- Tests:

## Ownership Decisions

| Module | Decision | Target owner | Reason |
|---|---|---|---|
| | FEATURE_OWNED / SHARED_UI / SHARED_INFRASTRUCTURE / APP_SHELL / COMPOSITION_ROOT / CROSS_FEATURE_CONTRACT / PACKAGE_PUBLIC / OWNERSHIP_UNRESOLVED | | |

## Public Feature Surface

- Entry file:
- Stable exports:
- Transitional exports:
- Internal modules:
- Broad barrels removed:
- Cross-feature consumers:
- Package exports:

## Global Components Folder

| Component | Business-specific | Consumers | Decision |
|---|---|---|---|
| | | | |

## Services Folder

| Service | Actual responsibility | Mixed concerns | Target |
|---|---|---|---|
| | | | |

## Shared Hook Ownership

| Hook | Semantics | Consumers | Target owner | Public? |
|---|---|---|---|---|
| | | | | |

## Utils / Types / Models

| Module | Semantic owner | Target |
|---|---|---|
| | | |

## State / Server State

- Global store:
- Feature-owned state:
- Query keys:
- Query hooks:
- Cache tenant/identity dimensions:
- Adapters:
- Mappers:
- Ownership change:

## Dependency Graph

### Before

```text

```

### After

```text

```

- Feature internal imports:
- Shared→feature imports:
- Application→Infrastructure:
- Component/hook→concrete adapter:
- App-shell/composition responsibility:

## Circular Dependencies

| Cycle | Root cause | Resolution | Status |
|---|---|---|---|
| | | | |

- Shared dumping-ground avoided:
- Port/event/composition used:
- Barrel cycle:
- Validation evidence:

## Compatibility Seams

| Seam | Reason | Consumers | Exit condition | Owner |
|---|---|---|---|---|
| | | | | |

- Deprecated aliases:
- Re-exports:
- Removal milestone:

## Migration Sequence

### Step 1
- Move:
- Redirect:
- Protect:
- Validate:
- Rollback:
- Exit criteria:

### Step 2
- Move:
- Redirect:
- Protect:
- Validate:
- Rollback:
- Exit criteria:

### Step 3
- Move:
- Redirect:
- Protect:
- Validate:
- Rollback:
- Exit criteria:

## Monorepo Package Extraction

- Candidate:
- Why extract:
- Multiple consumers:
- Public API stable:
- Internal leakage:
- App-shell coupling:
- Router dependency:
- Server-state dependency:
- Environment/config:
- CSS/assets:
- Circular package dependencies:
- Independent tests:
- Decision: PACKAGE_EXTRACTION_READY / PACKAGE_EXTRACTION_READY_WITH_CONDITIONS / KEEP_AS_APP_FEATURE / BOUNDARY_NOT_STABLE / PUBLIC_API_NOT_STABLE / CYCLE_BLOCKS_EXTRACTION / RUNTIME_COUPLING_BLOCKS_EXTRACTION

## Validation

- Lint:
- Typecheck:
- Unit/integration:
- Build:
- Architecture validation:
- Critical E2E:
- Accessibility:
- Performance:
- Security/privacy:
- Result:

## Debt Ledger

| Debt | Classification | Owner | Exit condition |
|---|---|---|---|
| | PRE_EXISTING_DEBT / CHANGE_LOCAL_REQUIRED / NEW_DEBT / ACCEPTED_TEMPORARY_DEVIATION | | |

## Over/Under-Migration Audit

- Big-bang rewrite:
- All technical folders moved horizontally:
- Shared abstraction premature:
- Package extraction premature:
- Ceremonial layers:
- Files moved without boundary repair:
- Legacy aliases without exit:
- New code still entering legacy folders:
- Decision: INCREMENTAL_VERTICAL_SLICE_MIGRATION / BIG_BANG_MIGRATION / PREMATURE_SHARED_ABSTRACTION / PREMATURE_PACKAGE_EXTRACTION / CEREMONIAL_ARCHITECTURE

## Final Decision

- Decision:
- Ready capability:
- Required ownership decision:
- Required characterization:
- Required cycle resolution:
- Required compatibility seam:
- Package extraction:
- Required validation:
- Next skill:
