---
name: validating-backend-architecture
description: Validates backend modular hexagonal architecture through evidence-oriented static inspection and executable checks. Use when a backend change, module, or repository must be audited for inward dependency direction, module ownership, public contracts, concrete-adapter leakage, controller/repository coupling, Use Case chaining, DTO/Domain separation, composition-root isolation, test-boundary violations, or architecture drift. Prefer repository-native import graph, path, AST, lint, and architecture tests. Do not rewrite code automatically, invent architecture rules, report personal style as architecture, or mark unavailable checks as passing.
...
---

# Validating Backend Architecture

## Purpose

Validate that backend code preserves the definitive modular hexagonal architecture.

The expected dependency direction is:

```text
Infrastructure → Application → Domain
```

Mandatory inward rules:

```text
Domain MUST NOT import Application or Infrastructure
Application MUST NOT import Infrastructure
Infrastructure MAY import Application and Domain
```

This skill verifies structure and dependency boundaries. It does not replace behavioral tests, code review, or implementation skills.

## Use When

- A backend vertical slice is implemented.
- A pull request changes module or layer boundaries.
- New ports, adapters, DTOs, controllers, Use Cases, or composition wiring are introduced.
- A concrete adapter may be leaking inward.
- A controller may be calling a repository or provider directly.
- A Use Case may call another Use Case.
- Domain objects may be leaking through Application or HTTP boundaries.
- Cross-module imports may bypass public contracts.
- Tests may depend on the wrong layer or environment.
- A brownfield change needs an architecture-drift report.
- Static architecture checks must be added or repaired.

## Do Not Use When

- The task is to design the target architecture from scratch.
- The task is to implement or refactor the violation.
- The task is only behavioral validation.
- The repository standard does not support a claimed rule.
- The finding is merely a personal style preference.
- The requested check cannot be executed and would be reported as passed.
- The task is to review security, performance, or code quality comprehensively.

## Inputs

- Definitive backend engineering standard.
- Repository-local `AGENTS.md`.
- Changed files, diff, module topology, or target scope.
- Existing import graph, lint, architecture-test, and AST tooling.
- TypeScript path aliases and package boundaries.
- Existing public module entry points.
- Current validation commands.
- Accepted exceptions and decision register.
- Generated-code and test-folder policies.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Read the definitive backend architecture rules.
3. Identify the validation scope:
   - changed files;
   - one capability;
   - one package;
   - full repository.
4. Discover repository topology and path aliases.
5. Identify Domain, Application, Infrastructure, delivery, and composition locations.
6. Inspect existing architecture tests and lint rules.
7. Read accepted deviations or migration records.
8. Identify generated files and exclude them only when policy allows.
9. Confirm commands that can actually run.
10. Do not invent a missing rule or exception.

## Outputs

- Architecture scope map.
- Executed and unavailable checks.
- Findings with evidence.
- Severity and rule classification.
- Dependency-path explanation.
- Accepted-exception handling.
- Suggested owning skill for remediation.
- Backend architecture validation report.
- Optional repository-native architecture test plan.

## Core Validation Areas

1. dependency direction;
2. module ownership;
3. public-contract usage;
4. repository and external-service ports;
5. concrete adapter isolation;
6. controller thinness;
7. Use Case isolation;
8. DTO and Domain boundaries;
9. composition-root isolation;
10. test-boundary correctness;
11. generated-code handling;
12. circular dependencies;
13. accepted deviations and migration seams.

## Workflow

1. **Confirm scope and rules:** Determine files, modules, layers, and applicable standard.
2. **Map architecture:** Classify source paths by capability and layer.
3. **Discover tooling:** Import graph, lint, AST, dependency tests, typecheck.
4. **Run existing checks first:** Preserve repository-native evidence.
5. **Inspect dependency direction:** Direct and transitive imports.
6. **Inspect cross-module imports:** Public contracts and ownership.
7. **Inspect ports and adapters:** Inward abstractions versus concrete implementations.
8. **Inspect controllers:** Use Case-only delivery dependency and transport concerns.
9. **Inspect Use Cases:** No concrete adapters, controllers, or Use Case chaining.
10. **Inspect DTO/Domain boundaries:** Primitive Application DTOs and no mutable Entity leakage.
11. **Inspect composition:** Concrete selection centralized and isolated.
12. **Inspect tests:** Correct doubles and boundary level.
13. **Detect cycles:** Module and factory cycles.
14. **Classify findings:** Mandatory violation, default deviation, policy issue, accepted exception, or inconclusive.
15. **Record unavailable checks:** Never convert them to pass.
16. **Produce report:** Include evidence, impact, and remediation routing.

## Readiness Gate

Use one:

```text
READY_TO_VALIDATE_ARCHITECTURE
READY_WITH_CONDITIONS
SCOPE_REQUIRED
ARCHITECTURE_RULES_REQUIRED
TOOLING_REQUIRED
ACCEPTED_EXCEPTION_DECISION_REQUIRED
BLOCKED
```

Stop when:

- scope cannot be determined;
- repository topology is unknown;
- the governing standard is unavailable;
- a finding conflicts with an accepted exception that cannot be resolved;
- generated code is indistinguishable from maintained source;
- the command would alter code or state unexpectedly.

## Rule Classification

Classify every evaluated rule as:

```text
MANDATORY_INVARIANT
DEFAULT
PROJECT_POLICY
ACCEPTED_EXCEPTION
NOT_APPLICABLE
INCONCLUSIVE
```

A finding against a mandatory invariant is normally more severe than a default deviation.

Do not report a default as mandatory without repository evidence.

## Result Classification

Each check must be:

```text
PASSED
FAILED
BLOCKED
SKIPPED_NOT_APPLICABLE
UNAVAILABLE
INCONCLUSIVE
```

`BLOCKED`, `UNAVAILABLE`, and `INCONCLUSIVE` are not passes.

## Dependency Direction

Expected:

```text
Infrastructure → Application → Domain
```

Validate direct and transitive imports.

### Domain

Domain may contain:

- Entities;
- Value Objects;
- Domain Services;
- Domain errors;
- repository ports;
- Domain-facing contracts.

Domain must not import:

- Application Use Cases;
- Request/Response DTOs;
- controllers;
- Infrastructure adapters;
- ORM/database;
- provider SDKs;
- framework modules;
- composition factories;
- environment/configuration readers.

### Application

Application may depend on Domain.

Application may contain:

- Use Cases;
- Request/Response DTOs;
- external-service ports;
- Application errors/results.

Application must not import:

- concrete repository adapters;
- concrete provider adapters;
- ORM/database clients;
- HTTP controllers/framework request objects;
- composition factories;
- SDK types;
- environment readers.

### Infrastructure

Infrastructure may depend inward on Application and Domain.

Infrastructure contains:

- repository adapters;
- external-service adapters;
- HTTP controllers;
- composition;
- configuration;
- technical telemetry.

Infrastructure must not reverse ownership by exporting technical types through inward contracts.

## Direct Versus Transitive Violations

A direct violation:

```text
Application Use Case
→ Prisma repository adapter
```

A transitive violation:

```text
Application
→ shared helper
→ Infrastructure config
```

Import-graph validation should inspect both when tooling allows.

Do not dismiss a transitive leak because the immediate import path looks neutral.

## Module Boundaries

Capabilities should be modular and business-oriented.

Validate:

- source ownership by capability;
- intentional shared contracts;
- no arbitrary deep import into another module;
- no cross-module access to concrete adapters;
- no cross-module Use Case imports;
- no bypass of public entry points where policy requires them.

Good:

```text
orders → customers/public-domain-contract
```

Risky:

```text
orders → customers/infrastructure/prisma/CustomerRecord
orders → customers/application/CreateCustomerUseCase
```

## Public Contracts

Cross-module imports should use explicit stable contracts.

Potential public contracts:

- intentionally shared Domain types;
- repository or external-service ports;
- Domain-facing events;
- stable read contracts;
- public module index according to repository policy.

Do not force barrel files when the repository does not require them.

Validate the actual public-contract convention.

## Deep Imports

A deep import is not automatically a violation.

It becomes a finding when it:

- bypasses an explicit public API;
- imports a private implementation;
- crosses ownership boundaries;
- creates adapter or internal-helper coupling;
- violates package exports.

Classify based on repository policy and architecture effect.

## Repository Ports and Adapters

Validate:

```text
Domain repository port
← implemented by Infrastructure adapter
```

Repository ports should:

- use Domain language;
- accept and return Domain objects;
- avoid DTOs and persistence records;
- expose operations required by Use Cases;
- have InMemory implementation according to current policy.

Concrete adapters should remain Infrastructure-only.

Findings include:

- ORM model returned from port;
- Application imports `Prisma...Repository`;
- controller calls repository directly;
- adapter interface defined by database CRUD terminology;
- InMemory repository located in unrelated global test utilities when policy requires colocation.

## External-Service Ports and Adapters

Validate:

```text
Application external-service port
← implemented by Infrastructure adapter
```

Findings include:

- SDK interface reused as Application port;
- SDK request/response imported into Application;
- provider error code used in Use Case;
- credentials in Request DTO;
- provider adapter selected outside composition;
- generic API client used as an Application capability.

## Controller Boundaries

Controllers are transport adapters.

A controller should:

- parse and validate transport shape;
- extract trusted context;
- build an Application Request DTO;
- invoke one Use Case intention;
- map result/errors to HTTP.

Detect:

- repository imports;
- concrete adapter or SDK imports;
- Domain Entity construction/mutation;
- business rules;
- transaction management;
- Use Case chaining;
- raw technical error mapping;
- Application DTO duplication.

A framework decorator or request schema is allowed inside delivery/Infrastructure.

## Controller-to-Repository Coupling

Mandatory finding pattern:

```text
Controller
→ Repository port or implementation
```

The preferred boundary is:

```text
Controller
→ Use Case
```

A controller must not bypass Application even when the repository port is abstract.

## Use Case Boundaries

A Use Case represents one intention.

Detect:

- import of another Use Case;
- direct concrete adapter import;
- controller/framework import;
- ORM/SDK import;
- response Entity leakage;
- transport status codes;
- environment reads;
- broad class with many CRUD intentions;
- direct static composition lookup.

A Use Case may depend on:

- Domain types;
- repository ports;
- external-service ports;
- pure Domain Services;
- Application DTOs/results.

## Use Case Chaining

Mandatory rule:

```text
A Use Case MUST NOT call another Use Case
```

When a workflow spans intentions, expected alternatives include:

- dedicated higher-level Use Case;
- Domain Service;
- domain/integration event;
- shared lower-level Domain capability.

Detect direct imports and runtime resolution through factories/containers.

## DTO Boundaries

Application DTOs must be transport-neutral primitive data.

Detect DTO fields containing:

- Entity;
- Value Object without explicit primitive mapping;
- ORM model;
- provider response;
- framework request/response;
- database enum;
- SDK enum;
- mutable Domain collection.

Use Cases must map Domain objects to Response DTOs explicitly.

Infrastructure should not reimplement business mapping already owned by Application.

## Entity Leakage

Detect:

```text
Use Case return type → Entity
Controller response → Entity
Application DTO field → Entity
```

The accepted boundary is:

```text
Use Case → Response DTO or void
```

A Domain Entity inside a repository port is valid.

Do not classify every Entity crossing an internal Domain boundary as leakage.

## Value Object Leakage

A Value Object may be valid inside Domain/Application internals.

At public Application DTO and HTTP boundaries it should normally map to primitives.

Classify according to accepted contract.

Do not report internal Use Case construction of Value Objects as a violation.

## Error Boundaries

Domain/Application errors must not know HTTP status codes.

Detect:

- `statusCode` in Domain error;
- framework exception imported in Application;
- SQLSTATE/provider code used as semantic Application error;
- raw technical error returned through controller;
- controller parsing provider or ORM errors directly.

One stable protocol-neutral error model should be used according to project policy.

## Composition Root

Concrete dependency wiring belongs to Infrastructure.

Validate:

- adapter selection centralized;
- Domain/Application do not import factory/composition;
- no runtime Service Locator;
- no DI container when current policy forbids it;
- shared `get*` dependencies are cached;
- transient `create*` Use Cases are fresh;
- environment reads remain near composition/config;
- controllers receive Use Cases.

Findings include:

```text
Use Case → getRepository()
Domain Service → container.resolve()
Controller → new PrismaClient()
Application → process.env
```

## Runtime DI and Service Locator

Current standard states no dependency-injection container.

Detect:

- token registries;
- `container.resolve`;
- decorators for automatic runtime injection;
- global mutable dependency maps;
- arbitrary `getService(name)`.

A narrow explicit typed test-composition builder is not automatically a Service Locator.

## Circular Dependencies

Detect cycles across:

- modules;
- layers;
- composition factories;
- controllers and composition;
- shared helpers.

Classify cycle impact:

```text
LAYER_CYCLE
MODULE_CYCLE
COMPOSITION_CYCLE
TEST_ONLY_CYCLE
GENERATED_CYCLE
```

A cycle that crosses Domain/Application/Infrastructure is high risk.

Do not rely only on runtime success; cycles can cause partial initialization and hidden coupling.

## Testing Boundaries

Validate test strategy architecture where in scope.

### Domain tests

Must not import Infrastructure, Application, database, HTTP, SDK, or mocks.

### Use Case tests

Should use:

- real Domain;
- InMemory repositories;
- explicit external-port doubles.

Detect repository mocks replacing accepted InMemory implementations.

### Repository adapter tests

Should use isolated real persistence.

Mocks are not proof of database behavior.

### External adapter tests

Should use strongest safe sandbox/emulator/contract evidence.

### HTTP E2E

Should issue real HTTP requests and avoid direct controller calls.

Do not require every changed file to have every test layer; assess applicability.

## Test Import Violations

Test files may import Infrastructure when Infrastructure is the subject.

Do not apply production dependency direction mechanically to all tests.

Instead validate the intended test boundary.

Example:

```text
repository adapter integration test
→ may import adapter and database harness
```

But it should not cause production inward imports.

## Generated Code

Identify generated paths from repository configuration.

Generated code may legitimately contain patterns that violate maintained-source style or dependency rules.

Rules:

- do not hand-edit generated files;
- validate source schemas/generators;
- exclude only documented generated paths;
- do not use generated status to hide maintained wrappers or adapters;
- report generated output drift separately.

## Architecture Automation

Prefer repository-native tooling.

Potential checks:

- TypeScript ESLint restricted imports;
- package `exports`;
- dependency-cruiser;
- madge;
- Nx module-boundary rules;
- ArchUnitTS or equivalent;
- custom TypeScript AST checks;
- `tsc --noEmit`;
- path-based scripts;
- package graph checks.

Do not add a new tool when existing tooling can express the rule adequately.

## Import Graph Analysis

An import-graph check should:

- resolve aliases;
- distinguish type-only imports where relevant;
- follow re-exports;
- exclude generated/test fixtures deliberately;
- report shortest violating path;
- detect cycles;
- support changed-file or full-repository scope.

Record tool limitations.

## Path-Based Checks

Useful for stable topology:

```text
domain/** must not import application/** or infrastructure/**
application/** must not import infrastructure/**
controllers/** must not import repositories/adapters/**
```

Path checks are fast but may miss:

- re-export leaks;
- alias indirection;
- runtime Service Locator calls;
- semantically wrong types.

Combine them with AST or code inspection for critical rules.

## AST Checks

Potential AST rules:

- Use Case class imports another Use Case;
- controller constructor accepts repository;
- Use Case return type references Entity;
- Application DTO references Domain/Infrastructure class;
- Domain error references HTTP;
- `process.env` appears outside config/composition;
- `container.resolve` appears in maintained source;
- controller constructs ORM/SDK clients.

AST checks must avoid fragile naming-only assumptions when possible.

## Naming Heuristics

Names such as `Controller`, `Repository`, `UseCase`, or `DTO` help discovery but are not proof.

Validate imports, constructors, return types, and file ownership.

Do not report findings solely because a filename differs from a preferred convention.

## Manual Inspection

Automation does not replace focused inspection.

Manually inspect:

- adapter selection;
- DTO mapping;
- error translation;
- transaction ownership;
- public-contract intent;
- suspicious shared helpers;
- accepted exceptions;
- tests that fake the wrong boundary.

Record whether a finding is automated or manual.

## Changed-Scope Versus Full-Scope Validation

### Changed Scope

Useful for fast PR feedback.

Validate:

- changed files;
- their inward and outward dependency edges;
- affected modules;
- newly introduced cycles.

### Full Scope

Required when:

- architecture tooling changes;
- aliases/package exports change;
- shared module changes;
- composition changes broadly;
- brownfield baseline is being established.

Do not claim repository-wide compliance from changed-file-only checks.

## Baselines and Brownfield Repositories

A brownfield repository may have known violations.

Use a baseline that distinguishes:

```text
PRE_EXISTING
NEW
WORSENED
FIXED
ACCEPTED_TEMPORARY
```

Do not require unrelated cleanup.

Do not allow the change to introduce or worsen violations without explicit decision.

Baseline files must not become an unreviewed suppression list.

## Accepted Exceptions

An exception must include:

- violated rule;
- scope;
- rationale;
- owner;
- risk;
- expiry or removal condition;
- validation suppression mechanism;
- decision reference.

Do not silently suppress.

Expired or broadened exceptions are findings.

## Severity

Suggested severity:

### Critical

- Domain imports Infrastructure with runtime side effects;
- production Service Locator enables arbitrary dependency lookup;
- controller exposes credentials or raw technical errors;
- public boundary leaks mutable Entity with correctness/security risk.

### High

- Application imports concrete adapter;
- controller calls repository/provider directly;
- Use Case chaining;
- DTO exposes ORM/provider object;
- cross-module concrete implementation coupling;
- composition imported inward.

### Medium

- public-contract bypass;
- new cycle without immediate runtime failure;
- missing architecture test for a high-risk new boundary;
- shared helper creates transitive dependency leak;
- test strategy validates wrong boundary.

### Low

- local default deviation with low coupling risk;
- architecture test maintainability issue;
- documented but near-expiry temporary exception.

Severity must reflect impact, not preference.

## Finding Format

Each finding should include:

- ID;
- title;
- severity;
- classification;
- rule;
- evidence;
- dependency path;
- impact;
- scope;
- existing/new status;
- accepted exception;
- recommended remediation skill;
- confidence.

Example:

```text
BA-ARCH-003
High — Application imports concrete campaign adapter

Rule:
Application MUST NOT import Infrastructure.

Evidence:
promotion/application/ApplyPromotionUseCase.ts
→ promotion/infrastructure/AcmeCampaignProvider.ts

Impact:
Use Case is provider-coupled and cannot be tested or replaced through the port.

Route:
designing-external-service-ports
implementing-external-service-adapters
wiring-backend-composition
```

## False Positives

Before reporting, check:

- alias resolution;
- type-only import;
- generated file;
- test-only subject;
- public-contract policy;
- accepted exception;
- re-export source;
- file misclassification;
- conditional compilation;
- dead code.

Do not suppress a real violation merely because the import is type-only if the type itself leaks an Infrastructure contract inward.

## Evidence Quality

Prefer:

1. executable architecture test;
2. import graph/path;
3. AST evidence;
4. type declaration;
5. direct code inspection;
6. naming heuristic.

A finding may combine several.

Do not cite line numbers or commands that were not inspected/executed.

## Remediation Routing

Route findings to focused skills:

```text
wrong Entity/VO boundary
→ modeling-domain-entities / modeling-domain-value-objects

wrong Domain Service ownership
→ designing-domain-services

repository port/adapter leakage
→ designing-domain-repositories / implementing-repository-adapters

Use Case boundary
→ designing-application-use-cases

DTO leakage
→ designing-application-dtos

provider port/adapter leakage
→ designing-external-service-ports / implementing-external-service-adapters

thick controller
→ implementing-http-controllers

composition leak
→ wiring-backend-composition

test-boundary issue
→ focused backend testing skill

brownfield migration
→ adapting-backend-rules-to-existing-code
```

The validation skill identifies; it does not perform the remediation automatically.

## Architecture Check Design

When adding checks, prefer:

- one rule per test/check;
- clear failure messages;
- shortest dependency path;
- stable path conventions;
- minimal suppressions;
- changed-scope command plus full command;
- deterministic output;
- CI compatibility.

Do not create one giant opaque architecture script.

## Potential Scripts

Roadmap-compatible automation may include:

```text
scripts/check-backend-import-direction
scripts/check-backend-module-boundaries
scripts/check-backend-controller-dependencies
scripts/check-backend-use-case-dependencies
scripts/check-backend-dto-boundaries
scripts/check-backend-cycles
scripts/run-backend-architecture-tests
```

Use repository-native language and tooling.

Do not create scripts if existing lint/architecture tooling is sufficient.

## Commands and Evidence

Record:

- command;
- scope;
- tool/version;
- exit code;
- result classification;
- output summary;
- unavailable capability;
- generated/baseline exclusions.

Do not claim a check ran based only on package scripts existing.

## Final Decision

Use one:

```text
ARCHITECTURE_VALID
ARCHITECTURE_VALID_WITH_CONDITIONS
ARCHITECTURE_VIOLATIONS_FOUND
ARCHITECTURE_BASELINE_REQUIRED
ACCEPTED_EXCEPTION_DECISION_REQUIRED
ARCHITECTURE_TOOLING_BLOCKED
INCONCLUSIVE
```

## Output

Use `assets/backend-architecture-validation-report.md`.

## Completion Criteria

- [ ] Governing backend rules and repository topology confirmed.
- [ ] Validation scope is explicit.
- [ ] Existing repository-native checks were discovered and run where available.
- [ ] Domain, Application, and Infrastructure dependency directions were inspected.
- [ ] Cross-module public-contract usage was inspected.
- [ ] Repository and external-service adapter leakage was inspected.
- [ ] Controllers were checked for repository/provider/business coupling.
- [ ] Use Cases were checked for concrete adapters, framework imports, and chaining.
- [ ] DTO and Domain boundaries were checked.
- [ ] Composition-root isolation and Service Locator prohibition were checked.
- [ ] Relevant test boundaries were checked.
- [ ] Cycles and transitive leaks were considered.
- [ ] Generated files and accepted exceptions were handled explicitly.
- [ ] Findings include evidence, severity, impact, and remediation routing.
- [ ] Blocked, unavailable, skipped, and inconclusive checks are not marked passed.
- [ ] No personal-style preference or unsupported rule was reported as architecture.
- [ ] Final decision reflects executed evidence and residual uncertainty.
