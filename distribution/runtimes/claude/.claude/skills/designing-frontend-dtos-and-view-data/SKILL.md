---
name: designing-frontend-dtos-and-view-data
description: Designs frontend Application DTOs, explicit Application results, component props, and UI view data while preserving boundaries between transport responses, Domain models, Application contracts, and Presentation. Use to map provider-specific payloads into stable serializable frontend data, decide where date/number/text formatting belongs, design nested dashboard/application results, prevent React/provider leakage, and determine when discriminated results are preferable to nullable bags or technical errors. Do not put ReactNode, JSX, icons, colors, CSS classes, callbacks, browser objects, raw provider DTOs, snake_case transport contracts, or concrete SDK types into Application DTOs.
---

# Designing Frontend DTOs and View Data

## Purpose

Design stable frontend data boundaries between:

```text
Transport/provider data
→ Domain
→ Application DTO/result
→ Presentation view data/component props
```

The goal is to prevent accidental coupling between:

- provider contracts;
- business semantics;
- application orchestration;
- UI rendering.

A DTO is a boundary contract, not a convenient dumping bag.

## Governing Standard

Application DTOs SHOULD:

- contain serializable data;
- use stable application language;
- avoid provider-specific types;
- avoid React-specific types;
- avoid browser implementation details;
- preserve semantic distinctions needed by callers.

Transport responses, Domain models, Application DTOs, and component props are different concerns even when their current shapes look similar.

## Use When

- A Use Case needs a stable output contract.
- An HTTP/provider response uses transport-specific naming or shape.
- Domain models should not be exposed directly to Presentation.
- A dashboard aggregates multiple sources.
- Date/number/text formatting ownership is unclear.
- Presentation needs derived view data.
- A result has several meaningful semantic outcomes.
- A package/public boundary needs stable serializable data.
- Provider SDK objects currently leak into components.
- ReactNode/icons/colors are appearing inside Application types.

## Do Not Use When

- The task is to design the Use Case itself.
- The task is HTTP mapping implementation.
- The task is Domain modeling.
- The data is purely local component state.
- The question is only CSS or visual styling.
- The operation can return `void` and no DTO/result is needed.
- The proposal adds DTO layers with no boundary or semantic value.

## Inputs

- Accepted behavior.
- Architecture profile.
- Domain model, when present.
- Use Case design.
- Provider/transport contracts.
- Component/view requirements.
- Localization/formatting policy.
- Package/public API requirements.
- Serialization requirements.
- Server/client boundary requirements.
- Existing naming conventions.
- Repository-local `AGENTS.md`.

## Outputs

- Boundary classification.
- Transport-to-Application mapping decision.
- Application DTO design.
- Explicit Application result design when needed.
- View-data/component-props decision.
- Formatting ownership.
- Nullability/optional-field semantics.
- Date/number/enum serialization semantics.
- Package/server-client safety decision.
- DTO/view-data test matrix.
- Frontend DTO and view-data design record.

## Core Workflow

```text
accepted behavior
→ identify source data and owner
→ classify boundary
→ choose stable Application semantics
→ define DTO/result only if valuable
→ define Presentation view data separately
→ assign formatting
→ define mapping and tests
```

## Readiness Gate

Use one:

```text
READY_TO_DESIGN_FRONTEND_DATA_BOUNDARIES
READY_WITH_CONDITIONS
NO_APPLICATION_DTO_REQUIRED
TRANSPORT_CONTRACT_REQUIRED
DOMAIN_BOUNDARY_REQUIRED
VIEW_REQUIREMENTS_REQUIRED
FORMAT_POLICY_REQUIRED
RESULT_SEMANTICS_REQUIRED
BLOCKED
```

A valid outcome may be:

```text
NO_APPLICATION_DTO_REQUIRED
```

Do not manufacture mapping layers without real boundary value.

# Boundary Model

Use these categories:

```text
TRANSPORT_RESPONSE
PROVIDER_SDK_TYPE
DOMAIN_MODEL
APPLICATION_REQUEST_DTO
APPLICATION_DTO
APPLICATION_RESULT
VIEW_DATA
COMPONENT_PROPS
LOCAL_UI_STATE
```

Every important data structure should have one primary owner.

## Transport Response

Transport response is Infrastructure-owned.

Examples:

```text
snake_case JSON
HTTP pagination envelope
GraphQL generated type
provider SDK response
generated OpenAPI DTO
```

Transport data may include:

- provider naming;
- nullable compatibility fields;
- version metadata;
- raw timestamps;
- technical status;
- nested provider-specific structures.

Do not expose it inward merely because TypeScript knows its type.

## Provider SDK Types

Concrete SDK objects stay in Infrastructure.

Examples:

```text
Stripe.PaymentIntent
Firebase.User
MapboxFeature
ContentfulEntry
AxiosResponse
```

Map them into stable inward semantics.

Do not use provider types as Application DTOs or component props across architectural boundaries.

## Domain Models

Domain models express business meaning and invariants.

They are not automatically view models.

Presentation MAY receive Domain values directly only when the accepted architecture deliberately allows it and no inappropriate behavior/implementation leaks.

Otherwise map into Application DTO or view data.

Do not flatten Domain merely because UI prefers a different shape if that mapping destroys important semantics.

## Application DTO

An Application DTO is a stable boundary contract for application consumers.

It SHOULD:

- be serializable;
- use camelCase or repository-standard application naming;
- contain primitives or stable nested application structures;
- avoid JSX/ReactNode;
- avoid icon components;
- avoid CSS classes/colors;
- avoid browser handles;
- avoid provider SDK types;
- avoid raw HTTP details;
- avoid localized presentation strings unless Application explicitly owns them.

## Application DTO Value

Create an Application DTO when it provides one or more:

- provider decoupling;
- Domain encapsulation;
- stable package boundary;
- aggregation across sources;
- semantic renaming;
- nullability normalization;
- result stability;
- server/client serialization safety.

Do not create one simply because “every Use Case must return a DTO.”

## Application DTO Example

Transport:

```text
{
  subscription_id: "sub-1",
  campaign_code: "SUMMER",
  starts_at: "2026-08-07T10:00:00Z",
  status_code: "ACTIVE"
}
```

Application:

```text
PromotionDTO {
  subscriptionId: string
  campaignCode: string
  startsAt: string
  status: PromotionStatus
}
```

Presentation may later format `startsAt`.

## Shape Coincidence

If transport and Application shapes currently match, decide whether an explicit mapping still protects a real boundary.

Use:

```text
EXPLICIT_MAPPING_REQUIRED
STRUCTURAL_REUSE_ACCEPTED
NO_SEPARATE_DTO_REQUIRED
```

Do not map fields one-to-one purely for ceremony.

But do not reuse provider-generated types merely because the field names happen to match today if provider independence matters.

# Application Results

Use an explicit Application result when callers need to distinguish meaningful outcomes.

Example:

```text
ApplyPromotionResult =
  | { type: "applied"; promotion: PromotionDTO }
  | { type: "invalid" }
  | { type: "expired" }
  | { type: "forbidden" }
  | { type: "unavailable" }
```

This is better than:

```text
{
  success?: boolean
  promotion?: ...
  error?: string
}
```

when several invalid combinations are possible.

## Result Versus DTO

Use:

```text
DTO
→ describes stable data

RESULT
→ describes outcome/state of an application intention
```

Do not overload one DTO with both data and workflow status if a discriminated result is clearer.

## Result Versus Exception

Expected recoverable outcomes may be explicit results.

Exceptional/unexpected failures may use the repository's stable error convention.

Do not force all failures into unions if the project consistently uses typed errors.

Do not collapse semantic outcomes to generic exceptions if callers need differentiated behavior.

# View Data

View data is Presentation-owned derived data shaped for rendering.

Examples:

```text
formattedDate
formattedPrice
statusLabel
progressText
ariaDescription
displayRows
chartSeries
```

View data may legitimately include presentation semantics that Application DTOs should not.

However, keep view data framework-neutral when practical.

Do not automatically put ReactNode, components, icons, or CSS classes into generic view-data objects.

## View Data Versus Component Props

View data represents rendering-ready values.

Component props define a component API and may additionally include:

- callbacks;
- child content;
- ReactNode when component composition genuinely requires it;
- accessibility relationships;
- presentation variants.

Do not push component API concerns into Application DTOs.

## Component Props

Component props MAY contain React-specific types because they are Presentation-owned.

Examples:

```text
children: ReactNode
icon?: ReactNode
onApply(): void
variant: "success" | "warning"
```

This is valid in component props.

It is invalid in Application DTOs.

The boundary, not the type itself, determines correctness.

# Formatting Ownership

Decide formatting based on semantics.

Use:

```text
DOMAIN
APPLICATION
PRESENTATION
INFRASTRUCTURE
```

## Presentation Formatting

Usually Presentation-owned:

- localized date/time;
- currency display;
- percentage text;
- label translation;
- truncation;
- title casing;
- UI-specific status copy;
- icon selection;
- color/variant selection.

Example:

```text
startsAt: "2026-08-07T10:00:00Z"
→ Presentation
→ "7 Aug, 12:00"
```

## Application Formatting

Application may own formatting only when it is semantic and presentation-independent.

Examples might include:

- stable human-readable export format;
- domain-defined code normalization intended for all consumers;
- application-level summary text explicitly treated as contract.

Use restraint.

Do not localize ordinary UI copy in Application by default.

## Domain Formatting

Domain should not perform locale-specific display formatting.

It may define semantic serialization or canonical representation.

Example:

```text
CampaignCode.toString()
```

is not the same as UI formatting.

## Infrastructure Formatting

Infrastructure handles provider serialization:

- query strings;
- headers;
- snake_case;
- wire dates;
- enum codes.

Do not leak wire formatting inward.

# Dates and Time

Application DTOs should use a stable date representation.

Possible choices:

```text
ISO-8601 string
epoch milliseconds
repository-approved date primitive
```

Choose consistently.

Do not return locale-formatted strings from Application by default.

Record:

- instant versus local date;
- timezone meaning;
- nullable semantics;
- parsing owner;
- display owner.

## Date Objects

`Date` may be acceptable inside one client-only boundary depending on repository policy.

For server/client/package serialization, strings or other serialization-safe forms are usually safer.

Do not introduce Temporal/polyfills or date libraries unless already approved.

# Numbers, Money, Percentages

Preserve semantics.

Transport:

```text
price_cents: 1099
```

Application may return:

```text
amountMinor: 1099
currency: "EUR"
```

or a serialized Domain Money representation.

Presentation decides:

```text
€10.99
```

Do not send a localized string inward when calculations or other consumers need numeric semantics.

## Precision

Record:

- unit;
- precision;
- rounding owner;
- nullable/unknown semantics.

Do not convert money into floating-point major units casually if exactness matters.

# Enums and Discriminated Unions

Provider enum:

```text
"A" | "E" | "X"
```

should map to stable application semantics such as:

```text
"active" | "expired" | "cancelled"
```

when provider codes are not meaningful inward.

Unknown enum behavior must be explicit:

```text
reject contract
map to unknown
preserve future-compatible value
```

Do not silently cast.

# Null, Undefined, Missing, Empty

Distinguish semantics:

```text
missing
null
undefined
empty string
empty list
not loaded
not found
not applicable
```

Do not normalize everything to `undefined` automatically.

Example:

```text
avatarUrl?: string
```

means absence.

```text
avatarUrl: string | null
```

may mean explicitly no avatar.

Follow repository conventions and actual product semantics.

# Optional Fields

Optional should mean something.

Record:

- absent because not requested;
- absent because not applicable;
- absent because provider omitted;
- absent for backward compatibility.

Avoid optionalizing every field to make mapping easier.

Weak:

```text
DashboardDTO {
  user?: UserDTO
  stats?: StatsDTO
  items?: ItemDTO[]
  error?: string
}
```

This admits too many invalid states.

# Nested Dashboard Results

A dashboard may combine several independent sources.

Do not automatically create one giant nullable DTO.

Options:

```text
DashboardDTO
```

when data is atomically required,

or:

```text
DashboardResult {
  profile: SectionResult<ProfileDTO>
  stats: SectionResult<StatsDTO>
  activity: SectionResult<ActivityDTO>
}
```

when sections load/fail independently.

Choose based on accepted behavior.

## Partial Data

If partial success is meaningful, model it explicitly.

Example:

```text
DashboardResult {
  summary: SummaryDTO
  recommendations:
    | { type: "available"; items: RecommendationDTO[] }
    | { type: "unavailable" }
}
```

Do not hide partial failure inside missing fields.

# React Leakage

Application DTOs MUST NOT contain:

```text
ReactNode
ReactElement
JSX.Element
ComponentType
RefObject
CSSProperties
SyntheticEvent
Dispatch
SetStateAction
```

Those belong to Presentation.

If such a type appears, ask whether the structure is actually component props/view data rather than an Application DTO.

# UI Styling Leakage

Application DTOs MUST NOT decide:

```text
color: "red"
icon: WarningIcon
className: "error"
variant: "destructive"
```

when these are UI styling decisions.

Prefer semantic data:

```text
severity: "error"
status: "expired"
```

Presentation maps semantics to visual treatment.

## Semantic Presentation Hints

Some application semantics may legitimately influence presentation.

Example:

```text
priority: "critical"
```

if it is a product semantic, not a design-system variant.

Do not confuse semantic severity with visual token names.

# Accessible View Data

Accessibility text tied to rendering may belong to Presentation view data.

Examples:

```text
ariaLabel
ariaDescription
formattedStatusAnnouncement
```

Do not push them into Application unless they are stable content semantics shared across non-React consumers.

The generic accessibility contract determines behavior; view data prepares content.

# Localization

Application DTOs should usually carry:

```text
semantic code/data
```

Presentation resolves:

```text
translation key
localized string
pluralization
date/number formatting
```

Whether translation keys belong in Application depends on project policy.

Prefer semantic status over direct UI copy:

```text
status: "expired"
```

instead of:

```text
statusLabel: "Promotion expired"
```

unless Application explicitly owns content.

# View Model Functions

A view-data mapper may transform:

```text
Application DTO
→ rendering-ready view data
```

It should be:

- deterministic;
- presentation-owned;
- testable;
- free of transport concerns.

Example:

```text
toPromotionCardViewData(dto, locale)
```

may produce formatted date, labels, and semantic display state.

Do not place such mappers in Domain.

# Component Props Mapping

Props may be created from view data plus callbacks.

Example:

```text
PromotionCardViewData
+
{
  onApply
}
→ PromotionCardProps
```

Do not contaminate reusable view data with closures unless the object is explicitly a component-props contract.

# View Data Reuse

A view-data type may be shared by multiple components only when rendering semantics are genuinely shared.

Do not create global `ViewModel` layers speculatively.

Feature-local view data is often preferable.

# Server Components and Serialization

When Application DTOs cross server/client boundaries:

- keep them serializable;
- avoid class instances unless framework/project policy supports serialization;
- avoid functions;
- avoid browser handles;
- avoid provider SDK objects;
- avoid non-serializable caches.

Domain models may need explicit serialization before crossing.

Do not rely on accidental framework serialization behavior.

# Package Boundaries

Public package DTOs should be:

- stable;
- serializable;
- semantically named;
- provider-independent;
- framework-independent unless the package is explicitly a React UI package.

A React component package may expose React props.

An Application package should not.

# Request DTOs Versus Response DTOs

Request DTOs express input intent.

Application DTOs express output data.

Do not reuse one transport-style type bidirectionally when input/output semantics differ.

Example:

```text
UpdateProfileRequest
ProfileDTO
```

rather than:

```text
ProfilePayload
```

for everything.

# Generic API Types

Avoid inward types such as:

```text
ApiResponse<T>
ApiData<T>
BackendItem
ServerModel
```

unless they truly represent Infrastructure contracts.

Application types should use product language.

# Pagination

Provider pagination may use:

```text
page
per_page
next_cursor
```

Application may expose:

```text
PaginatedResult<T> {
  items: T[]
  nextCursor?: string
}
```

only if pagination semantics are stable and reused.

Do not create a universal pagination type when APIs have materially different semantics.

# Errors in DTOs

Do not embed technical errors casually:

```text
DashboardDTO {
  data: ...
  axiosError?: AxiosError
}
```

Use explicit application results/errors.

View data may include rendering-safe error semantics.

Do not pass stack traces to components.

# Booleans

Avoid ambiguous flags:

```text
isActive
isAvailable
isValid
```

when semantic state is richer.

Prefer discriminated state when invalid combinations would otherwise exist.

Example:

```text
status: "active" | "expired" | "scheduled"
```

rather than three booleans.

# Derived Fields

Application DTOs may include derived fields when:

- derivation is stable application semantics;
- multiple consumers need the same result;
- exposing raw source would leak Domain/Infrastructure complexity.

Presentation-derived fields belong in view data.

Ask:

```text
Would this field mean the same thing in a CLI or another UI?
```

If yes, Application may own it.

If it is about how this screen displays, Presentation likely owns it.

# Duplication

It is acceptable for DTO and Domain shapes to have some duplication when they protect different boundaries.

Do not eliminate boundary types solely for DRY.

Also do not introduce mapping layers solely for theoretical decoupling with no meaningful boundary.

Use:

```text
BOUNDARY_DUPLICATION_JUSTIFIED
STRUCTURAL_REUSE_SAFE
MAPPING_CEREMONY
LEAKING_BOUNDARY
```

# Naming

Use names that reveal owner:

```text
ProfileDTO
ApplyPromotionResult
PromotionCardViewData
PromotionCardProps
PromotionApiResponse
```

Avoid ambiguous:

```text
ProfileData
PromotionModel
ResultData
ItemType
```

when several layers have similar shapes.

# DTO Mutability

Prefer immutable/read-only DTO contracts where repository conventions support it.

Do not rely on mutation of shared Application DTOs as UI state.

Presentation may copy/derive local editable state when needed.

# Mapping Ownership

Typical ownership:

```text
Transport → Application/Domain
Infrastructure adapter

Domain → Application DTO
Use Case/Application mapper

Application DTO → View data
Presentation mapper

View data → Component props
Presentation/composition
```

Do not create one giant universal mapper spanning all layers.

# Mapping Errors

Mapping must define:

- missing required field;
- invalid enum;
- invalid date;
- unsupported provider variant;
- partial response.

Runtime validation may be required for external data; that belongs to the external-data validation skill/Infrastructure boundary.

Do not trust a TypeScript interface as runtime validation.

# DTO Tests

Test DTO/mapping contracts at the boundary that owns them.

Possible evidence:

- adapter tests for provider mapping;
- Application tests for result mapping;
- pure view-data mapper tests for formatting;
- component tests for rendered props.

Do not duplicate the same field mapping at every level.

# View Data Tests

View-data mapper tests may cover:

- date/number formatting;
- status-to-label mapping;
- empty/partial data;
- localization;
- accessible description strings;
- deterministic sorting/grouping for display.

Keep them pure where possible.

Do not use React render tests just to test a pure formatting mapper.

# Snapshot Restraint

Do not snapshot entire DTOs or view models by default.

Prefer explicit semantic assertions.

Snapshots may be acceptable for stable structured export contracts according to project policy.

# Overmodeling Audit

Flag:

- DTO identical to provider type with no boundary value;
- DTO identical to Domain with no encapsulation/package value;
- view-data layer with no actual formatting/derivation;
- component props reused as Application DTO;
- universal `BaseDTO`;
- generic mapper framework;
- `ApiResponse<T>` leaked throughout Application.

Use:

```text
PROPORTIONATE_BOUNDARY
MAPPING_CEREMONY
UNDERMODELED_BOUNDARY
LEAKING_BOUNDARY
NO_APPLICATION_DTO_REQUIRED
```

# Example — snake_case API

Transport:

```text
{
  user_id: "u1",
  display_name: "Ana",
  created_at: "2026-08-07T10:00:00Z"
}
```

Application:

```text
UserDTO {
  id: "u1"
  displayName: "Ana"
  createdAt: "2026-08-07T10:00:00Z"
}
```

Presentation:

```text
UserCardViewData {
  name: "Ana"
  createdLabel: "7 Aug 2026"
}
```

No transport casing leaks inward.

# Example — Date Formatting

Application:

```text
startsAt: ISO string
```

Presentation:

```text
startsAtLabel: localized string
```

Do not return localized dates from Use Cases merely because the first consumer is React.

# Example — ReactNode Leak

Reject:

```text
AlertDTO {
  title: string
  icon: ReactNode
}
```

Prefer Application:

```text
AlertDTO {
  type: "warning"
  title: string
}
```

Presentation maps `warning` to icon and style.

# Example — Nested Dashboard

Avoid:

```text
DashboardDTO {
  profile?: ...
  recommendations?: ...
  stats?: ...
  error?: string
}
```

if sections fail independently.

Prefer explicit section results or a stable partial-success structure.

# Example — Discriminated Result

Good:

```text
ApplyPromotionResult =
  | { type: "applied"; promotion: PromotionDTO }
  | { type: "invalid" }
  | { type: "expired" }
  | { type: "forbidden" }
```

This prevents contradictory booleans and nullable fields.

# Final Decision

Use:

```text
FRONTEND_DATA_BOUNDARIES_READY
FRONTEND_DATA_BOUNDARIES_READY_WITH_CONDITIONS
NO_APPLICATION_DTO_REQUIRED
RETURN_TO_USE_CASE_OR_DOMAIN_DESIGN
TRANSPORT_MAPPING_REQUIRED
VIEW_DATA_REQUIRED
RESULT_CONTRACT_REQUIRED
FORMAT_POLICY_REQUIRED
BLOCKED
```

## Output

Use `assets/frontend-dto-view-data-design-record.md`.

## Completion Criteria

- [ ] Transport, Domain, Application, view-data, and component-props boundaries are explicit.
- [ ] Application DTOs exist only when they provide real boundary value.
- [ ] Transport/provider naming and types remain in Infrastructure.
- [ ] Application DTOs are serializable and framework-independent.
- [ ] ReactNode/JSX/icons/colors/CSS/callbacks are excluded from Application DTOs.
- [ ] Provider SDK objects and HTTP responses are excluded.
- [ ] Domain models are not exposed accidentally as view models.
- [ ] Explicit Application results are used when callers need distinguishable outcomes.
- [ ] Invalid nullable/boolean state bags are avoided.
- [ ] UI-specific formatting has an explicit owner.
- [ ] Localized dates/numbers/text remain in Presentation by default.
- [ ] Date/timezone/precision semantics are explicit.
- [ ] Null/undefined/missing/empty meanings are explicit.
- [ ] Provider enums map to stable application semantics where necessary.
- [ ] Nested/partial dashboard results model independent failure honestly.
- [ ] Server/client/package boundaries remain serializable.
- [ ] View data remains Presentation-owned.
- [ ] Component props may use React types only because they are Presentation-owned.
- [ ] Mapping ownership is explicit by layer.
- [ ] Tests target the boundary that owns each transformation.
- [ ] Boundary duplication versus mapping ceremony is consciously decided.
- [ ] No generic DTO/mapper framework, library, or project policy is invented.
- [ ] Final data-boundary decision is explicit.

## References

- Read `references/data-boundary-classification-and-dto-value.md` first.
- Read `references/application-results-nullability-and-partial-data.md`.
- Read `references/view-data-formatting-localization-and-component-props.md`.
- Read `references/provider-domain-and-serialization-boundaries.md`.
- Read `references/mapping-ownership-testing-and-overmodeling.md`.
- Read `references/frontend-dto-view-data-design-audit.md` before completion.
