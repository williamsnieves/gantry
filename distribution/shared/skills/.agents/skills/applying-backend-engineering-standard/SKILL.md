---
name: applying-backend-engineering-standard
description: Portable engineering capability `applying-backend-engineering-standard`.
  Use when the harness or a specialist agent explicitly requires this named capability.
---
# Applying the Backend Engineering Standard

## Purpose

Prepare backend work by converting a ready change and repository context into a precise, minimal, evidence-based set of applicable engineering rules.

This skill prevents two failure modes:

- loading or enforcing the entire backend standard when most sections do not apply;
- beginning implementation before repository policies, affected layers, boundaries, and validation obligations are understood.

## Use When

- Starting implementation planning for a backend change.
- A change affects Domain, Application, Infrastructure, HTTP, persistence, providers, composition, contracts, or backend tests.
- A repository needs the applicable backend rules identified before coding.
- A brownfield change must distinguish target standards from existing exceptions.
- Another backend skill requires a scoped rule set and validation plan.
- The user asks which backend rules apply to a change or code area.

## Do Not Use When

- The request is to implement the backend change.
- The request is only to validate, audit, or review completed code.
- The change is frontend-only.
- The accepted behavior or scope is still materially unresolved.
- The repository context is unavailable and cannot be inspected.
- The user expects this skill to choose unapproved frameworks, databases, DI containers, or architectural policies.

## Inputs

- Accepted specification or OpenSpec change.
- Repository structure.
- Root and nearest nested `AGENTS.md`.
- `FULLSTACK-ENGINEERING-STANDARD.md`.
- `BACKEND-ENGINEERING-STANDARD.md`.
- Backend and full-stack decision registers.
- Backend project policies and ADRs.
- Relevant existing code, tests, packages, and commands.
- Brownfield exception registry when applicable.

## Required Context

1. Read the root and nearest applicable `AGENTS.md`.
2. Resolve the exact change and backend scope.
3. Inspect repository structure and backend workspace boundaries.
4. Locate applicable standards, decision registers, ADRs, and project policies.
5. Discover repository-native build, type-check, lint, test, migration, generation, and run commands.
6. Inspect representative existing code in each affected module or layer.
7. Identify current architecture rather than assuming idealized structure.
8. Distinguish mandatory invariants, defaults, project policies, and existing exceptions.
9. Do not read every backend reference automatically; load only those triggered by the classification.

## Outputs

- Backend Rule Applicability Report.
- Affected modules, capabilities, layers, and boundaries.
- Active mandatory invariants.
- Selected defaults and project policies.
- Existing exceptions and deviations.
- Required follow-up decisions.
- Recommended implementation-skill sequence.
- Required validation and review gates.
- Stop/continue decision.

## Workflow

1. **Resolve the change:** Confirm accepted behavior, exclusions, risk, and backend ownership.
2. **Discover repository instructions:** Read `AGENTS.md`, standards, ADRs, and policies in precedence order.
3. **Map backend topology:** Identify workspaces, packages, modules, capabilities, layers, public surfaces, and composition roots.
4. **Classify the change:** Type, lifecycle, risk, affected layers, boundaries, contracts, data, and operations.
5. **Select standard sections:** Activate only relevant shared and backend rules.
6. **Resolve policy choices:** Read existing decisions; never invent missing ones.
7. **Detect conflicts:** Compare specification, standards, policies, local conventions, and existing implementation.
8. **Classify deviations:** Accepted exception, brownfield debt, required decision, or implementation violation.
9. **Select implementation skills:** Recommend focused backend skills in dependency order.
10. **Build validation plan:** Map selected rules and risks to checks and gates.
11. **Decide readiness:** Ready, ready with explicit conditions, return to specification, or blocked.
12. **Report:** Use the backend rule applicability report.

## Change Classification

Classify at minimum:

### Change Type

```text
FEATURE
BUG_FIX
REFACTOR
CONTRACT_CHANGE
DATA_MIGRATION
SECURITY
RELIABILITY
PERFORMANCE
TEST_ONLY
TOOLING_BUILD
DOCUMENTATION
```

### Lifecycle

```text
GREENFIELD
BROWNFIELD_EXTENSION
BROWNFIELD_REFACTOR
MIGRATION
DEPRECATION
REMOVAL
```

### Risk

```text
LOW
MEDIUM
HIGH
CRITICAL
```

### Affected Backend Areas

```text
DOMAIN_ENTITY
DOMAIN_VALUE_OBJECT
DOMAIN_SERVICE
DOMAIN_REPOSITORY_PORT
APPLICATION_USE_CASE
APPLICATION_DTO
APPLICATION_EXTERNAL_PORT
REPOSITORY_ADAPTER
EXTERNAL_SERVICE_ADAPTER
HTTP_CONTROLLER
COMPOSITION_ROOT
DATABASE_SCHEMA
MIGRATION
EVENT_OR_PUBLIC_CONTRACT
BACKGROUND_JOB
CACHE
OBSERVABILITY
TEST_INFRASTRUCTURE
```

## Rule Categories

### Mandatory Invariant

Must apply whenever its trigger exists.

Examples:

- Domain does not depend on Application or Infrastructure.
- Application does not import concrete Infrastructure adapters.
- Controllers do not call repositories directly.
- Provider SDK types remain in Infrastructure.
- Changed real boundaries require realistic validation.
- Generated output is not edited instead of its source.

A mandatory invariant may be blocked only by an explicit accepted exception.

### Default

Applies unless an accepted project policy selects another valid approach.

Examples may include:

- one intention per Use Case;
- manual composition root;
- Application DTO or `void` output;
- InMemory repositories for Use Case tests;
- explicit mapping at boundaries.

### Project Policy

Must be discovered from repository context.

Examples:

- generic versus typed IDs;
- Result versus exception error model;
- DTO naming;
- ORM and migration tooling;
- DI strategy;
- transaction ownership;
- event schema/versioning;
- test location.

Never silently choose a project policy.

### Existing Exception

A known departure from the target standard.

Record:

- scope;
- affected rule;
- rationale;
- risk;
- containment;
- migration trigger;
- owner.

Do not propagate an exception into new code without explicit need.

## Layer and Boundary Detection

### Domain Trigger

Activate Domain rules when the change introduces or modifies:

- business identity;
- invariants;
- lifecycle/state transitions;
- value semantics;
- pure cross-entity behavior;
- domain-oriented repository needs.

### Application Trigger

Activate Application rules when the change introduces or modifies:

- user/system intention;
- orchestration;
- ports;
- request/response DTOs;
- transaction or external collaboration boundaries.

### Infrastructure Trigger

Activate Infrastructure rules when the change touches:

- database;
- provider/SDK;
- HTTP transport;
- messaging;
- filesystem;
- clock/randomness;
- cache;
- external configuration;
- concrete composition.

### Contract Trigger

Activate contract rules when the change affects:

- routes;
- request/response schemas;
- events;
- public packages;
- database representations shared across versions;
- generated clients;
- error/status semantics.

## Architecture Profile

Determine the current and target profile proportionally.

Possible classifications:

```text
SIMPLE_SERVICE
MODULAR_BACKEND
HEXAGONAL_CAPABILITY
PACKAGE_OR_PLATFORM
LEGACY_TRANSITION
```

Do not force full hexagonal decomposition when a simple service has no meaningful domain or external boundary complexity.

Do not use simplicity as justification for leaking infrastructure into business behavior.

## Conflict Resolution

Apply instruction precedence from `AGENTS.md`.

Classify conflicts as:

```text
NO_CONFLICT
LOCAL_CONVENTION_WITHIN_STANDARD
PROJECT_POLICY_REQUIRED
ACCEPTED_EXCEPTION
TARGET_STANDARD_VIOLATION
SPECIFICATION_CONFLICT
UNRESOLVED_ARCHITECTURE_DECISION
```

### Stop Conditions

Stop and return to specification or decision-making when:

- accepted behavior is ambiguous;
- public contract ownership is unclear;
- a persistence or migration strategy is unresolved;
- authorization ownership is unresolved;
- a mandatory rule conflicts with an unrecorded local convention;
- two modules claim the same capability;
- a framework or dependency choice is material and unapproved.

## Recommended Skill Routing

Select only relevant next skills.

Examples:

```text
Domain identity/invariants
→ modeling-domain-entities
→ modeling-domain-value-objects

Cross-domain pure behavior
→ designing-domain-services

Persistence need
→ designing-domain-repositories
→ implementing-repository-adapters

Application intention
→ designing-application-use-cases
→ designing-application-dtos

External collaboration
→ designing-external-service-ports
→ implementing-external-service-adapters

HTTP boundary
→ implementing-http-controllers

Construction/lifecycle
→ wiring-backend-composition

Implementation sequence
→ planning-backend-vertical-slices
→ implementing-backend-inside-out
```

Do not route to skills that are not triggered.

## Validation Plan

Map applicable rules to concrete evidence.

### Domain

- pure unit tests;
- invariant and invalid-state tests;
- no prohibited imports.

### Application

- Use Case tests;
- port interaction checks;
- DTO/result assertions;
- no concrete adapter dependencies.

### Repository/Provider Adapters

- realistic integration;
- mapping;
- failure semantics;
- configuration;
- cleanup and lifecycle.

### HTTP

- route, request, response, status, error, auth/authz;
- protocol integration or E2E where required.

### Composition

- wiring/startup smoke tests;
- configuration validation;
- lifecycle ownership.

### Cross-Cutting Risk

- security/privacy;
- reliability/idempotency;
- migration/data safety;
- performance;
- observability;
- compatibility.

## Readiness Decision

Use one:

```text
READY_FOR_BACKEND_PLANNING
READY_WITH_CONDITIONS
RETURN_TO_SPECIFICATION
DECISION_REQUIRED
BLOCKED
NOT_A_BACKEND_CHANGE
```

## Output

Use `assets/backend-rule-applicability-report.md`.

## Completion Criteria

- [ ] Exact change and backend scope resolved.
- [ ] Instruction precedence and repository policies inspected.
- [ ] Backend topology and affected capabilities mapped.
- [ ] Change type, lifecycle, risk, layers, and boundaries classified.
- [ ] Only applicable standard sections selected.
- [ ] Mandatory invariants, defaults, policies, and exceptions separated.
- [ ] Conflicts and missing decisions identified.
- [ ] Focused backend skills selected in dependency order.
- [ ] Validation and review obligations mapped.
- [ ] Readiness decision justified.
- [ ] No implementation or unapproved policy decision performed.

## References

- Read `references/intake-and-repository-discovery.md` first.
- Read `references/backend-change-classification.md` to classify triggers.
- Read `references/rule-selection-and-precedence.md` to select rules.
- Read `references/backend-topology-and-boundaries.md` to map architecture.
- Read `references/deviations-and-brownfield.md` for legacy repositories.
- Read `references/skill-routing.md` to select next backend skills.
- Read `references/backend-validation-planning.md` before reporting readiness.
