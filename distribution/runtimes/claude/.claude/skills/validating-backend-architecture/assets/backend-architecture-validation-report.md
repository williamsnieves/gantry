# Backend Architecture Validation Report

## Context

- Change ID:
- Repository/service:
- Validation scope:
- Changed files/modules:
- Governing standard:
- Repository-local rules:
- Accepted decision register:
- Validation date:
- Validator/tooling:

## Scope Classification

- Changed-files only:
- Capability/module:
- Package/service:
- Full repository:
- Generated paths excluded:
- Test paths included:
- Baseline used:
- Scope limitations:

## Architecture Map

| Capability/module | Domain path | Application path | Infrastructure path | Composition/delivery path |
|---|---|---|---|---|
| | | | | |

## Applicable Rules

| Rule | Classification | Source | Applicable |
|---|---|---|---|
| Infrastructure → Application → Domain | MANDATORY_INVARIANT | | |
| Domain must not import outward | MANDATORY_INVARIANT | | |
| Application must not import Infrastructure | MANDATORY_INVARIANT | | |
| Use Case must not call another Use Case | MANDATORY_INVARIANT | | |
| Controllers call Use Cases, not repositories/providers | MANDATORY_INVARIANT | | |
| Use Cases return DTOs or void | MANDATORY_INVARIANT | | |
| Concrete selection only in composition | PROJECT_POLICY | | |
| No runtime DI container/Service Locator | PROJECT_POLICY | | |

## Tooling Discovery

| Tool/check | Available | Command | Scope | Limitation |
|---|---|---|---|---|
| Typecheck | | | | |
| Lint/restricted imports | | | | |
| Import graph | | | | |
| Cycle detection | | | | |
| AST checks | | | | |
| Architecture tests | | | | |

## Executed Checks

| Check | Command | Result | Evidence summary |
|---|---|---|---|
| | | PASSED/FAILED/BLOCKED/UNAVAILABLE/INCONCLUSIVE | |

## Dependency Direction

### Domain

- Application imports found:
- Infrastructure imports found:
- Framework/ORM/SDK imports:
- Composition/config imports:
- Result:

### Application

- Concrete adapter imports:
- HTTP/framework imports:
- ORM/SDK imports:
- Composition/environment imports:
- Result:

### Infrastructure

- Inward implementation:
- Technical type leakage:
- Result:

## Module Boundaries

- Cross-module imports:
- Public contracts used:
- Deep private imports:
- Cross-module Use Case imports:
- Concrete implementation coupling:
- Result:

## Ports and Adapters

### Repositories

- Port location:
- Domain-oriented signatures:
- Persistence type leakage:
- Concrete adapter leakage inward:
- InMemory policy:
- Result:

### External Services

- Port location:
- Provider-neutral contract:
- SDK/provider type leakage:
- Credentials leakage:
- Adapter selection location:
- Result:

## Controllers

- Use Case dependency:
- Repository/provider dependencies:
- Domain construction/mutation:
- Business rules:
- Transaction management:
- Use Case chaining:
- Technical error parsing:
- Result:

## Use Cases

- Single intention:
- Other Use Case imports/calls:
- Concrete adapter imports:
- Controller/framework imports:
- DTO/void return:
- Entity leakage:
- Environment/factory access:
- Result:

## DTO, Domain, and Errors

- Primitive Request DTOs:
- Primitive Response DTOs:
- Entity/Value Object leakage:
- ORM/provider/framework types:
- HTTP status in Domain/Application errors:
- Explicit mapping:
- Result:

## Composition

- Concrete selection centralized:
- `get*` shared caching:
- `create*` transient Use Cases:
- Domain/Application imports composition:
- Runtime container/Service Locator:
- Scattered environment reads:
- Controller wiring:
- Result:

## Testing Boundaries

- Domain tests pure:
- Use Case tests use InMemory/port doubles:
- Repository tests use real persistence:
- External adapter evidence level:
- HTTP E2E uses real HTTP:
- Wrong-boundary tests:
- Result:

## Cycles and Transitive Leaks

| Cycle/leak | Type | Path | Impact |
|---|---|---|---|
| | LAYER/MODULE/COMPOSITION/TEST | | |

## Findings

### BA-ARCH-001 — <title>

- Severity:
- Classification:
- Rule:
- Evidence:
- Dependency path:
- Impact:
- Scope:
- Status: NEW/PRE_EXISTING/WORSENED/FIXED/ACCEPTED_TEMPORARY
- Accepted exception:
- Confidence:
- Recommended remediation skill:

## Accepted Exceptions

| Exception | Rule | Scope | Owner | Expiry/removal condition | Status |
|---|---|---|---|---|---|
| | | | | | |

## Unavailable or Inconclusive Checks

| Check | Reason | Risk | Required future evidence |
|---|---|---|---|
| | | | |

## Summary

- Critical findings:
- High findings:
- Medium findings:
- Low findings:
- New violations:
- Pre-existing violations:
- Worsened violations:
- Fixed violations:
- Accepted temporary deviations:

## Final Decision

- Decision:
- Conditions:
- Blocking findings:
- Residual uncertainty:
- Required remediation:
- Recommended next validation:
