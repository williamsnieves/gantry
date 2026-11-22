# Frontend Domain Modeling Record

## Context

- Change/capability:
- Repository/application:
- Architecture profile:
- Accepted behavior:
- Backend/domain authority:
- Offline/local behavior:
- Optimistic behavior:
- Persistence:
- Existing frontend Domain:
- Applicable `AGENTS.md`:
- Modeled by/date:

## Readiness

- Product behavior complete:
- Authority boundary known:
- Offline policy:
- Persistence ownership:
- Initial decision:
- Conditions/blockers:

## Domain Justification

| Signal | Present | Evidence |
|---|---|---|
| Rich local behavior | | |
| Offline operation | | |
| Client-side decision support | | |
| Deterministic product rules | | |
| Shared semantic validation | | |
| Stateful local product model | | |
| Meaningful invariant protection | | |

- Decision: PROPORTIONATE_DOMAIN / UNDERMODELED_DOMAIN / OVERMODELED_DOMAIN / NO_DOMAIN_REQUIRED
- Why Domain is or is not justified:
- Smallest useful Domain boundary:

## Authority Matrix

| Rule/behavior | Authority | Frontend purpose | Drift risk |
|---|---|---|---|
| | FRONTEND_AUTHORITATIVE/BACKEND_AUTHORITATIVE/SHARED_SEMANTICS_BACKEND_AUTHORITATIVE/FRONTEND_PREVIEW_ONLY/LOCAL_ONLY_RULE/UNKNOWN_REQUIRES_DECISION | | |

## Concept Inventory

| Concept | Type | Why Domain | Owner |
|---|---|---|---|
| | ENTITY/VALUE_OBJECT/DOMAIN_SERVICE/DOMAIN_ERROR/REPOSITORY_PORT | | |

## Entities

### Entity

- Name:
- Identity:
- Lifecycle:
- Invariants:
- Valid transitions:
- Invalid transitions:
- Intent-revealing operations:
- Mutation model:
- Public mutation prevented:
- Serialization:
- Persistence owner:

## Value Objects

| Value Object | Primitive/value | Validation | Equality | Operations | Serialization |
|---|---|---|---|---|---|
| | | | value | | |

## Domain Services

| Service/function | Inputs | Output | Why no natural entity/VO owner | Purity |
|---|---|---|---|---|
| | | | | |

## Domain Errors

| Error | Semantic meaning | Trigger | Technical detail excluded |
|---|---|---|---|
| | | | |

## Presentation Logic Excluded

| Logic | Correct owner | Reason |
|---|---|---|
| | Presentation/Application/Infrastructure | |

## Backend Rules Not Duplicated

| Server rule | Frontend behavior | Authority preserved |
|---|---|---|
| | | |

## Offline / Local Model

- Applicable:
- Local identity:
- Lifecycle:
- Validation:
- Conflict behavior:
- Sync boundary:
- Storage implementation excluded:

## Rich Editor Model

- Applicable:
- Product-semantic state:
- Browser/editor-library mechanics excluded:
- Commands:
- Invariants:

## Optimistic Behavior

- Classification: DOMAIN_OPTIMISTIC_RULE / SERVER_STATE_OPTIMISTIC_BEHAVIOR / PRESENTATION_OPTIMISTIC_STATE / NOT_APPLICABLE
- Owner:
- Transitions:
- Rollback/reconciliation:
- Concurrency:
- Duplicate ownership excluded:

## Repository Port Decision

- Decision: DOMAIN_REPOSITORY_PORT_JUSTIFIED / APPLICATION_PORT_PREFERRED / NO_PORT_REQUIRED / PORT_OWNERSHIP_REQUIRES_DECISION
- Port name:
- Domain language:
- Persistence semantics:
- Why meaningful without HTTP:
- Concrete implementation explicitly excluded:

## Serialization

| Domain concept | Serialized form | Mapper owner |
|---|---|---|
| | primitive/transport-safe structure | Application/Infrastructure |

- Provider casing excluded:
- Framework types excluded:

## Dates / Numeric Semantics

- Date/time meaning:
- Timezone:
- Inclusive/exclusive ranges:
- Units:
- Precision:
- Rounding:
- Allowed range:

## Shared Domain Decision

- Shared concept:
- Real consumers:
- Semantic stability:
- Owner:
- Central evolution justified:
- Speculative shared abstraction excluded:

## Domain Test Matrix

| Concept/rule | Valid case | Boundary/invalid case | Environment |
|---|---|---|---|
| | | | plain test runtime |

- React excluded:
- HTTP excluded:
- Browser excluded:
- Storage excluded:
- Domain mocks excluded:
- Property-based testing justified:

## Over/Under Modeling Audit

- Passive API bags:
- Empty Value Objects:
- Forwarding Domain Services:
- Endpoint-shaped repositories:
- Provider types:
- Speculative abstractions:
- Repeated local invariants currently outside Domain:

## Final Decision

- Decision:
- Conditions:
- Blocking issue:
- Next skill:
- Required follow-up:
