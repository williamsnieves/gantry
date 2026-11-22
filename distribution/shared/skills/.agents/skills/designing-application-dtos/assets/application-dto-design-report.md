# Application DTO Design Report

## Context

- Change ID:
- Vertical slice:
- Use Case:
- Accepted consumers:
- Existing DTOs/contracts:
- Applicable policies:
- Public/shared contract:
- Error/result convention:

## DTO Suitability

- Request DTO required:
- Response DTO required:
- `void` considered:
- Direct primitive considered:
- Decision rationale:

## Request DTO

- Name:
- Responsibility:

| Field | Primitive/plain type | Required/optional/nullable | Domain mapping |
|---|---|---|---|
| | | | |

## Response DTO

- Name:
- Responsibility:

| Field | Primitive/plain type | Source | Transformation |
|---|---|---|---|
| | | | |

## Shape Decisions

- Flat versus nested:
- Selected fields:
- Flattened fields:
- Derived presentation-neutral fields:
- Explicit exclusions:

## Field Semantics

### Identifiers

-

### Enums

-

### Dates and Time

-

### Money and Precision

-

### Optionality and Nullability

-

### Collections and Pagination

-

## Input Mapping

1.
2.
3.

### Invalid Input Semantics

| Input problem | Application/Domain meaning |
|---|---|
| | |

## Output Mapping

1.
2.
3.

### Mapping Location

- Use Case:
- Application mapper:
- DTO factory:
- Rationale:

## Validation Ownership

| Concern | Delivery | Application | Domain |
|---|---|---|---|
| | | | |

## Boundary Audit

- Entity leakage:
- Value Object leakage:
- ORM/database leakage:
- Provider leakage:
- HTTP/framework leakage:
- Automatic/universal mapping:
- Sensitive/internal fields:

## Compatibility

- Consumers:
- Added/removed/renamed fields:
- Enum compatibility:
- Optionality changes:
- Versioning/deprecation:
- Coordination required:

## Test Plan

| Test | Boundary | Expected evidence |
|---|---|---|
| | | |

## Follow-up Skills

1.
2.

## Readiness

- Decision:
- Conditions:
- Open decisions:
- Risks:
- Recommended next action:
