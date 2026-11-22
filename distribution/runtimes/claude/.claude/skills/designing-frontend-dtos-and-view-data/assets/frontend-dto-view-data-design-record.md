# Frontend DTO and View Data Design Record

## Context

- Change/capability:
- Repository/application:
- Architecture profile:
- Accepted behavior:
- Use Case:
- Domain model:
- Provider/transport source:
- Presentation consumers:
- Server/client boundary:
- Package boundary:
- Localization policy:
- Applicable `AGENTS.md`:
- Designed by/date:

## Readiness

- Transport contract known:
- Domain boundary known:
- Application consumer known:
- View requirements known:
- Formatting policy known:
- Initial decision:
- Conditions/blockers:

## Boundary Inventory

| Structure | Classification | Owner | Consumers |
|---|---|---|---|
| | TRANSPORT_RESPONSE/PROVIDER_SDK_TYPE/DOMAIN_MODEL/APPLICATION_REQUEST_DTO/APPLICATION_DTO/APPLICATION_RESULT/VIEW_DATA/COMPONENT_PROPS/LOCAL_UI_STATE | | |

## Boundary Value Decision

- Application DTO required:
- Why:
- Provider decoupling:
- Domain encapsulation:
- Package stability:
- Aggregation:
- Semantic renaming:
- Nullability normalization:
- Serialization:
- Decision: PROPORTIONATE_BOUNDARY / MAPPING_CEREMONY / UNDERMODELED_BOUNDARY / LEAKING_BOUNDARY / NO_APPLICATION_DTO_REQUIRED

## Transport Source

```text

```

- Provider naming/casing:
- Nullable compatibility fields:
- Provider enums:
- Raw timestamps:
- SDK objects:
- Technical metadata:
- Must remain Infrastructure-owned:

## Application DTO

```text

```

| Field | Type | Meaning | Required/optional | Source |
|---|---|---|---|---|
| | | | | |

- Serializable:
- Camel/application naming:
- Provider types excluded:
- React types excluded:
- Browser types excluded:
- Localized strings excluded:
- UI style/icon fields excluded:

## Application Result

- Required:
- Why distinguish outcomes:

```text

```

| Variant | Semantic meaning | Data |
|---|---|---|
| | | |

- Generic success/error bag rejected:
- Exception convention:
- Recoverable outcomes explicit:

## Domain Boundary

- Domain types exposed directly:
- Why safe/unsafe:
- Domain-to-DTO mapping:
- Domain behavior hidden:
- Serialization:
- Value Objects serialized as:

## Nullability and Optionality

| Field/state | Representation | Meaning |
|---|---|---|
| | null / undefined / absent / empty / discriminated state | |

- Not loaded:
- Not found:
- Not applicable:
- Partial data:
- Provider omitted:
- Compatibility field:

## Dates / Time

- Representation:
- Instant/local date/date-time:
- Timezone semantics:
- Parsing owner:
- Display formatting owner:
- Server/client serialization:
- Locale-formatted strings excluded from Application:

## Numbers / Money / Percentage

| Value | Unit | Precision | Rounding owner | Application representation |
|---|---|---|---|---|
| | | | | |

- Localized formatting owner:

## Enums / Semantic Codes

| Provider value | Application semantic | Unknown behavior |
|---|---|---|
| | | |

- Silent casts excluded:

## Nested / Partial Results

- Atomic result:
- Independent sections:
- Partial success:
- Section result model:

```text

```

- Giant nullable DTO avoided:

## View Data

```text

```

| Field | Source | Presentation transformation |
|---|---|---|
| | | |

- Localized dates:
- Localized numbers/currency:
- Status labels:
- Accessible descriptions:
- Chart/display structures:
- Sorting/grouping:
- Framework-neutral where practical:

## Component Props

```text

```

- ReactNode allowed because Presentation-owned:
- Callbacks:
- Variants:
- Accessibility props:
- View data reused:
- Application DTO not contaminated:

## Styling / Semantic Presentation

- Application semantic status:
- Presentation visual variant:
- Icon mapping:
- Color/token mapping:
- CSS class mapping:
- Semantic severity versus visual treatment:

## Localization

- Translation owner:
- Semantic code:
- Translation key policy:
- Localized text:
- Pluralization:
- Date/number locale:
- Bidirectional considerations:

## Server / Client / Package Safety

- Serializable across boundary:
- Functions excluded:
- Class instances excluded or serialized:
- SDK objects excluded:
- Browser handles excluded:
- Public package type stable:
- React-specific package exception:

## Mapping Ownership

| Mapping | Owner | Function/module |
|---|---|---|
| Transport → Domain/Application | Infrastructure | |
| Domain → Application DTO | Application | |
| Application DTO → View Data | Presentation | |
| View Data → Component Props | Presentation/composition | |

- Universal mapper avoided:

## Test Matrix

| Transformation | Test boundary | Cases |
|---|---|---|
| Provider mapping | adapter | |
| Application result mapping | Use Case/Application | |
| View formatting | pure Presentation mapper | |
| Props/rendering | component | |

- Duplicate field mapping tests avoided:
- Snapshot restraint:

## Overmodeling Audit

- Provider-identical DTO with no value:
- Domain-identical DTO with no value:
- Empty view-data layer:
- Props reused as Application DTO:
- BaseDTO:
- Generic mapper framework:
- Generic ApiResponse leak:
- Mapping ceremony:

## Final Decision

- Decision:
- Conditions:
- Blocking issue:
- Next skill:
- Required follow-up:
