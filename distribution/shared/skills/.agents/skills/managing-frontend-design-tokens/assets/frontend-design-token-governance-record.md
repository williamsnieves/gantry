# Frontend Design Token Governance Record

## Context

- Change/design decision:
- Repository/application:
- Token source of truth:
- Styling profile(s):
- Theme strategy:
- Shared UI/design-system:
- Accessibility target:
- Vendor design system:
- Existing consumers:
- Published package/versioning:
- Applicable `AGENTS.md`:
- Managed by/date:

## Readiness

- Existing taxonomy known:
- Semantic meaning known:
- Theme policy known:
- Ownership known:
- Accessibility evidence available:
- Migration policy known:
- Initial decision:
- Conditions/blockers:

## Proposed Decision

- Decision: SEMANTIC_TOKEN_JUSTIFIED / BASE_SCALE_TOKEN_JUSTIFIED / COMPONENT_TOKEN_JUSTIFIED / LOCAL_VALUE_PREFERRED / EXISTING_TOKEN_REUSE / TOKEN_NOT_REQUIRED / TOKEN_OWNERSHIP_REQUIRES_DECISION
- Why:
- Repeated:
- Theme-sensitive:
- Central evolution value:
- Accessibility impact:
- Existing token checked:

## Token Hierarchy

| Level | Token/value | Owner | Purpose |
|---|---|---|---|
| raw/reference | | | |
| palette/base | | | |
| semantic | | | |
| component | | | |
| local/runtime | | | |

## Naming

- Repository naming grammar:
- Proposed token:
- Semantic meaning:
- Feature/ticket name avoided:
- Palette shade avoided in semantic API:
- Alias required:

## Ownership

- Owner: GLOBAL_DESIGN_SYSTEM / SHARED_UI_COMPONENT / FEATURE_LOCAL / VENDOR_ADAPTER / THEME
- Change authority:
- Consumers:
- Public package API:

## Existing Token Reuse

| Existing token | Meaning | Fit | Decision |
|---|---|---|---|
| | | exact / partial / wrong | |

- Duplicate synonym avoided:

## Palette / Base Mapping

| Semantic/component token | Palette/base token | Raw value |
|---|---|---|
| | | |

- Features depend directly on palette:
- Why allowed if any:

## Theme Mapping

| Token | Light | Dark | High contrast/other |
|---|---|---|---|
| | | | |

- Semantic meaning stable:
- Feature-specific dark pair avoided:
- Theme completeness:
- Root/theme ownership:
- Local component override:

## Danger / Status Semantics

| Context | Semantic token | Foreground/background pair |
|---|---|---|
| action danger | | |
| danger text | | |
| danger surface | | |
| danger border | | |
| warning | | |
| success | | |

- One generic danger red avoided:
- Color-only meaning avoided:

## Accessibility / Contrast

| Pair | Target | Evidence/result |
|---|---|---|
| text.primary / surface.default | | |
| text.danger / surface.default | | |
| action.danger fg/bg | | |
| focus ring / adjacent surface | | |

- Visible focus:
- Disabled:
- High contrast:
- Reduced motion:
- Control size:

## Spacing Scale

- Existing scale:

```text

```

| Proposed spacing | Repeats | Existing scale match | Decision |
|---|---|---|---|
| | | | |

- New scale step justified:
- Local one-off preferred:
- Semantic spacing alias:

## Size / Typography / Radius / Border / Shadow / Motion / Layer

| Category | Existing token | Proposed need | Decision |
|---|---|---|---|
| size | | | |
| typography | | | |
| radius | | | |
| border | | | |
| shadow | | | |
| motion | | | |
| z-index/layer | | | |
| breakpoint | | | |

## Vendor Token Mapping

- Vendor:
- Strategy: PROJECT_SEMANTIC_WRAPS_VENDOR / VENDOR_THEME_CONSUMES_PROJECT_TOKENS / DIRECT_VENDOR_TOKEN_ACCEPTED / HYBRID_WITH_EXPLICIT_BOUNDARY
- Direction:
- Semantic roles mapped:

| Vendor token | Project semantic/component token | Reason |
|---|---|---|
| | | |

- Unused vendor tokens mirrored:
- Vendor lock-in reduced:
- Theme parity:
- Contrast preserved:

## Multiple Styling Systems

- CSS Modules:
- Tailwind:
- Shared UI:
- CSS variables:
- Generated artifacts:
- One semantic source:
- Competing token sources:

## One-Off Local Value

- Value:
- Usage:
- Repeated:
- Semantic meaning:
- Theme dependence:
- Global evolution value:
- Would another team know when to use token:
- Decision: LOCAL_VALUE_PREFERRED / TOKEN_CANDIDATE

## Hardcoded Value Audit

| Hardcoded value | Classification | Action |
|---|---|---|
| | EXISTING_TOKEN_AVAILABLE / NEW_SEMANTIC_TOKEN_CANDIDATE / BASE_SCALE_CANDIDATE / LOCAL_ONE_OFF / RUNTIME_VALUE / LEGACY_DEBT | |

## Deprecation

- Deprecated token:
- Reason:
- Replacement:
- Semantic equivalence:
- Since:
- Removal target:
- New usage prevention:
- Theme mappings:
- Alias retained:

## Migration Inventory

| Consumer | Current token | Replacement | Mechanical vs semantic | Visual review |
|---|---|---|---|---|
| | | | | |

- Mass string replacement safe:
- Context-specific replacements required:

## Versioning

- Package:
- Change classification: PATCH_VALUE_CHANGE / MINOR_ADDITIVE_TOKEN / DEPRECATION / BREAKING_REMOVAL / SEMANTIC_BREAKING_CHANGE
- Release impact:
- Consumer communication:

## Alias Graph

```text

```

- Alias depth:
- Cycles:
- Dangling refs:
- Permanent synonym:
- Migration-only alias:

## Token Tooling

- Source:
- Generator:
- CSS output:
- TS output:
- Tailwind output:
- Docs:
- Generated files edited directly:
- New tooling introduced:

## Roadmap Evaluation Cases

### Dark Mode
- Decision:
- Evidence:

### Danger Color
- Decision:
- Evidence:

### Spacing Scale
- Decision:
- Evidence:

### Vendor Token Mapping
- Decision:
- Evidence:

### Deprecated Token
- Decision:
- Evidence:

### Local One-Off Value
- Decision:
- Evidence:

## Test / Evidence Matrix

| Case | Expected |
|---|---|
| token source resolves | |
| light theme | |
| dark theme | |
| alias resolution | |
| no cycles | |
| deprecated usage | |
| vendor mapping | |
| contrast pairs | |
| representative shared primitive visual | |

- Visual regression:
- Component explorer:
- No raw-token trivial test explosion:

## Over/Under-Modeling Audit

- Token per pixel:
- Feature/ticket token names:
- One-off optical token:
- Duplicate synonyms:
- Component-token layer with no value:
- Deep alias chains:
- Full vendor token mirror:
- Multiple source of truth:
- Repeated hardcoded semantic values:
- Dark values duplicated in features:
- Deprecated token without plan:
- Decision: PROPORTIONATE_TOKEN_SYSTEM / TOKEN_PROLIFERATION / TOKEN_GAP / SEMANTIC_DRIFT

## Final Decision

- Decision:
- Conditions:
- Blocking issue:
- Next skill:
- Required follow-up:
