---
name: validating-frontend-architecture
description: Validates a frontend repository or change against its selected architecture profile and accepted boundaries. Use to inspect dependency direction, cross-feature internal imports, public surfaces, shared-folder misuse, circular dependencies, package boundaries, server/client separation, composition placement, and automated architecture enforcement. Produce evidence-backed pass/fail findings and remediation targets using the repository's existing tooling such as ESLint boundaries, dependency-cruiser, Nx module-boundary rules, Madge, TypeScript project references, package exports, or architecture tests. Do not redesign the whole architecture, invent new folder layers, enforce Profile B/C rules on Profile A, introduce new tooling without approval, or mix subjective style review with boundary validation.
...
---

# Validating Frontend Architecture

## Purpose

Validate whether the implemented frontend structure respects the architecture profile and boundary rules already accepted for the repository.

This skill answers:

```text
Does the current code respect the architecture we said we are using?
```

It does not answer:

```text
What architecture should we choose from scratch?
```

Primary validation areas:

- dependency direction;
- feature ownership;
- cross-feature imports;
- public surfaces;
- `shared` usage;
- composition boundaries;
- server/client separation;
- package/module boundaries;
- cycles;
- automated enforcement;
- architecture-related Definition of Done.

## Roadmap Purpose

This skill must:

- inspect dependency direction;
- detect cross-feature internal imports;
- verify public surfaces;
- detect shared-folder misuse;
- verify the selected architecture profile.

Potential automation may include repository-approved use of:

```text
ESLint boundaries
dependency-cruiser
Nx enforce-module-boundaries
Madge
TypeScript project references
package exports
architecture tests
CI checks
```

The exact tool is repository-specific.

Do not install or introduce a new tool unless that decision has already been accepted.

## Use When

- A frontend change is approaching completion.
- Architecture boundaries need objective validation before merge.
- A feature has accumulated cross-feature imports.
- Components or hooks may import concrete adapters.
- Application may import Infrastructure.
- A shared folder may have become a dumping ground.
- A package exposes internal files accidentally.
- Circular dependencies are suspected.
- Server-only code may leak into client bundles.
- A migration must prove architecture improvement.
- CI boundary rules exist and need interpretation.
- A codebase needs a repeatable architecture validation report.

## Do Not Use When

- The architecture profile has not been selected.
- The task is to design the architecture itself.
- The task is a subjective code-quality review.
- The task is performance or security review.
- The task is only component/hook testing.
- The task is to create a new module-boundary tool from scratch.
- The user asks for universal folder rules independent of repository context.

## Inputs

- Selected architecture profile.
- Definitive frontend engineering standard.
- Repository-local `AGENTS.md`.
- Frontend vertical-slice plan.
- Feature/package ownership decisions.
- Public API/package export policy.
- Composition-root decision.
- Server/client boundary policy.
- Shared-code policy.
- Existing lint/build/architecture tooling.
- Current repository tree and import graph.
- Relevant CI commands.
- Previous architecture findings or migration plan.

## Outputs

- Architecture validation status.
- Dependency-direction matrix.
- Feature-boundary findings.
- Public-surface findings.
- Shared-code findings.
- Composition and runtime-boundary findings.
- Circular-dependency findings.
- Automation evidence.
- Severity-ranked violations.
- Remediation targets.
- Frontend architecture validation record.

## Readiness Gate

Use one:

```text
READY_TO_VALIDATE_FRONTEND_ARCHITECTURE
READY_WITH_CONDITIONS
ARCHITECTURE_PROFILE_REQUIRED
PUBLIC_SURFACE_POLICY_REQUIRED
OWNERSHIP_DECISION_REQUIRED
TOOLING_EVIDENCE_REQUIRED
SERVER_CLIENT_BOUNDARY_REQUIRED
BLOCKED
```

Stop when there is no accepted architecture profile to validate against.

## Validation Philosophy

Validate the repository against its selected profile.

Do not validate every frontend as if it were Profile B or C.

Use:

```text
Profile A
→ lightweight boundaries

Profile B
→ modular Domain/Application/Infrastructure boundaries

Profile C
→ package/public-contract boundaries in addition to modular rules
```

A simple feature is not invalid because it lacks Domain/Application folders when Profile A is accepted.

Conversely, a Profile B/C codebase is not valid merely because code compiles.

## Profile A Validation

Typical Profile A:

```text
feature/
├── components/
├── hooks/
├── api/
└── tests/
```

Validate:

- feature-local ownership;
- components/hooks do not bypass approved API abstraction;
- cross-feature internals are not imported casually;
- shared code is justified;
- composition remains clear;
- no unnecessary ceremonial layers;
- client/server boundaries are respected;
- public package surfaces are respected where packages exist.

Do not require Domain or Application layers.

## Profile B Validation

Typical Profile B:

```text
feature/
├── domain/
├── application/
├── infrastructure/
└── tests/
```

Validate:

```text
Infrastructure
→ Application
→ Domain
```

Rules:

- Domain MUST NOT import Application.
- Domain MUST NOT import Infrastructure.
- Application MUST NOT import Infrastructure.
- Components/hooks MUST NOT import concrete repository or HTTP adapters.
- Infrastructure may import Application and Domain according to accepted contracts.
- composition selects concrete implementations at an outer boundary.

## Profile C Validation

Profile C adds package-scale concerns.

Validate:

- package public exports;
- no deep imports into package internals;
- app-specific Infrastructure stays outside reusable package contracts;
- package dependencies remain directional;
- server/client entry points are separated where required;
- shared types are stable contracts rather than leaked implementation;
- build/project references do not create hidden cycles.

## Dependency Direction

Build a matrix of:

```text
from
→ to
```

For each import classify:

```text
ALLOWED
FORBIDDEN
CONDITIONALLY_ALLOWED
PROFILE_DEPENDENT
UNKNOWN_REQUIRES_DECISION
```

Example for Profile B:

| From | Domain | Application | Infrastructure |
|---|---|---|---|
| Domain | allowed | forbidden | forbidden |
| Application | allowed | allowed | forbidden |
| Infrastructure | allowed | allowed | allowed |

This is a conceptual matrix; repository-local exceptions may narrow it further.

Do not infer that same-layer imports are always good. Feature ownership still applies.

## Import Graph

Inspect:

- static imports;
- dynamic imports when architecture-relevant;
- package aliases;
- barrel exports;
- generated imports if checked into source;
- test-only imports separately;
- server/client entry points.

Distinguish:

```text
production import graph
test import graph
build/tooling graph
```

Do not flag test-only architecture helpers as production leakage without evidence.

## Cross-Feature Imports

Feature code SHOULD NOT import another feature's internals directly.

Bad:

```text
orders/components/OrderCard
→ imports
billing/internal/useBillingState
```

Preferred collaboration uses:

- public feature API;
- Application port;
- shared Domain contract;
- event;
- routing boundary;
- documented package export.

Classify cross-feature import:

```text
PUBLIC_SURFACE_IMPORT
INTENTIONAL_SHARED_CONTRACT
INTERNAL_BOUNDARY_BYPASS
TEMPORARY_MIGRATION_EXCEPTION
UNKNOWN
```

## Public Surfaces

Large modules SHOULD expose deliberate public surfaces.

Examples:

```text
feature/index.ts
feature/public.ts
package exports
```

Validate:

- only stable contracts are exported;
- internal files are not reachable through supported imports accidentally;
- public surface does not re-export everything mechanically;
- public surface does not create hidden cycles;
- package exports align with intended consumers.

Do not require a barrel file for every tiny feature.

## Barrel Exports

Barrels are not inherently good or bad.

Validate whether a barrel:

- exposes intentional stable contracts;
- hides ownership;
- causes cycles;
- re-exports internals;
- makes tree/build boundaries ambiguous.

Use:

```text
INTENTIONAL_PUBLIC_SURFACE
LOCAL_CONVENIENCE_BARREL
OVERBROAD_BARREL
CYCLE_RISK_BARREL
```

Do not ban all `index.ts` files.

## Shared Code

Move code to `shared` only when it is:

- genuinely used by multiple capabilities;
- semantically stable;
- not owned by one feature;
- safe to evolve centrally.

Validate each shared artifact for:

- real consumers;
- semantic neutrality/stability;
- owner;
- change blast radius;
- product-language fit;
- dependency direction.

Classify:

```text
JUSTIFIED_SHARED
FEATURE_OWNED_MISPLACED_IN_SHARED
SPECULATIVE_SHARED
GENERIC_HELPER_DUMP
SHARED_CONTRACT_WITH_OWNER
```

`shared` MUST NOT become a dumping ground.

## Shared UI

Shared UI should contain reusable presentation primitives or stable application UI contracts, not business-specific behavior disguised as generic visuals.

Validate:

- consumer count;
- stable semantics;
- accessibility ownership;
- styling/token ownership;
- no feature-specific business rule;
- vendor primitive policy;
- package ownership.

A generic appearance is not evidence of shared ownership.

## Feature Ownership

Every source file should have a recognizable owner:

```text
feature
shared contract
application shell
design system
package
infrastructure boundary
```

Flag:

```text
UNCLEAR_OWNER
CROSS_CAPABILITY_COUPLING
MISPLACED_SHARED_CODE
OUTER_LAYER_LEAK
```

Architecture validation should improve discoverability, not enforce folders mechanically.

## Folder Structure

Folder structure is evidence, not the architecture by itself.

Validate:

- code location matches responsibility;
- folders correspond to actual contents;
- no empty ceremonial layers;
- naming uses product language;
- no generic dumping folders such as `Utils`, `Helpers`, `Common`, or `Misc` unless genuinely meaningful.

Do not fail a codebase solely because folder names differ from the reference tree if boundaries are preserved.

## Components and Hooks

Validate:

- no concrete repository imports;
- no concrete HTTP adapter imports;
- no global Factory lookup unless this file is explicitly the accepted composition boundary;
- no cross-feature internal import;
- server-only imports excluded from client files;
- public dependencies used through accepted boundaries.

Potential violation:

```text
usePromotion.ts
→ imports HttpPromotionRepository
```

Expected remediation:

```text
composition boundary injects semantic dependency
```

## Application Layer

Where an Application layer exists, validate:

- no Infrastructure imports;
- Use Cases depend on ports/contracts;
- DTOs do not expose provider payloads;
- no React imports unless the repository explicitly defines an outer application UI boundary differently;
- no browser/vendor implementation dependency.

Do not apply this validation when Profile A intentionally has no Application layer.

## Domain Layer

Where Domain exists, validate:

- no React;
- no browser API;
- no HTTP;
- no storage SDK;
- no Application import;
- no Infrastructure import;
- no UI/design-system dependency;
- no provider payload type.

Domain should remain portable and deterministic.

## Infrastructure Layer

Validate that Infrastructure:

- implements inward ports;
- may depend on Application/Domain as accepted;
- owns HTTP/storage/provider types;
- owns composition/factory where project structure places it;
- does not become the owner of business policy;
- does not leak technical types inward.

Architecture validation detects direction and ownership; semantic business-rule review may require `reviewing-frontend-architecture`.

## Composition Boundary

Validate:

- concrete implementations selected at an outer boundary;
- components/hooks do not instantiate adapters directly;
- Domain/Application do not import composition;
- server/client composition is separated where needed;
- no global Service Locator;
- dependency lifecycle matches accepted scope.

Potential violations:

```text
component → new HttpClient()
hook → getDependencies()
Domain → Factory
```

## Service Locator Detection

Flag patterns such as:

```text
getDependencies()
resolve(token)
container.get(name)
services.repository
globalDependencies.*
```

when feature code can request arbitrary dependencies.

A DI container may be accepted at the composition root.

Do not flag typed container registration itself if the accepted policy allows it and resolution remains at the boundary.

## Server / Client Boundary

Validate when relevant:

- server-only modules do not enter client import graph;
- browser-only APIs do not enter server graph unsafely;
- secrets remain server-only;
- non-serializable dependencies are not passed across server/client boundary;
- request-scoped state is not cached globally;
- client/server package entry points are explicit.

Classify:

```text
SERVER_ONLY_LEAK_TO_CLIENT
CLIENT_ONLY_LEAK_TO_SERVER
NON_SERIALIZABLE_BOUNDARY_LEAK
SAFE_SPLIT_ENTRYPOINT
RUNTIME_BOUNDARY_UNKNOWN
```

## Package Boundaries

For monorepos/packages validate:

- import follows declared package dependency;
- no deep imports into another package's internal source;
- package exports match supported surface;
- dependency graph has no prohibited reverse edges;
- build references match logical dependencies;
- cyclic package dependency is absent;
- environment-specific entry points are safe.

Examples:

Bad:

```text
@company/orders/src/internal/foo
```

Preferred:

```text
@company/orders
@company/orders/server
@company/orders/client
```

when those exports are intentionally supported.

## Circular Dependencies

Detect:

- file cycles;
- feature cycles;
- package cycles;
- barrel-created cycles;
- composition cycles.

Classify:

```text
DIRECT_FILE_CYCLE
FEATURE_CYCLE
PACKAGE_CYCLE
BARREL_CYCLE
TYPE_ONLY_CYCLE
FALSE_POSITIVE_OR_TOOL_LIMITATION
```

Type-only cycles may still be architectural signals but should not be reported as runtime cycles without evidence.

## Dynamic Imports

Dynamic import can be valid for:

- code splitting;
- client-only integration;
- optional feature loading.

It must not be used merely to bypass architecture enforcement.

Validate semantic ownership even when the static rule is avoided through `import()`.

## Type-Only Imports

Type imports can still expose unstable internal contracts across boundaries.

Validate them against public-surface ownership.

Do not assume `import type` is architecture-safe by definition.

## Generated Code

Generated clients/types may require exceptions.

Validate:

- generated location;
- who may import generated types;
- whether generated provider types leak into Domain/Application;
- regeneration ownership;
- public-wrapper policy.

Do not edit generated code merely to satisfy structure.

## Test Imports

Tests may require access to internal seams.

Classify separately:

```text
PRODUCTION_BOUNDARY
TEST_ONLY_BOUNDARY
ARCHITECTURE_TEST_HELPER
```

A test importing a feature internal file is not automatically a production violation.

However, cross-package test imports can still create brittle coupling and should be evaluated.

## Tooling Discovery

Use existing repository tooling first.

Look for:

- ESLint rules/config;
- dependency-cruiser config;
- Nx tags and module-boundary rules;
- Madge scripts;
- TS project references;
- package exports;
- custom architecture tests;
- CI workflows.

Do not assume a tool exists.

Do not invent commands.

## ESLint Boundary Validation

When existing ESLint rules enforce imports, record:

- rule names;
- scope;
- ignored paths;
- severity;
- violations;
- gaps between policy and rule.

Do not treat a green ESLint run as complete architecture proof if important boundaries are not encoded.

## dependency-cruiser

When present, inspect:

- forbidden rules;
- allowed rules;
- cycle detection;
- orphan policy if relevant;
- path aliases;
- generated/test exclusions;
- output.

Map each rule back to the accepted architecture policy.

## Nx Module Boundaries

When Nx is present, inspect:

- project tags;
- dependency constraints;
- enforce-module-boundaries rules;
- implicit dependencies;
- buildable/publishable constraints;
- project graph.

Verify tags represent actual architectural ownership.

Do not introduce Nx merely for architecture validation.

## Madge or Cycle Tools

When used, scope results correctly.

Cycle output should be classified by:

- production versus test;
- runtime versus type-only;
- feature/package ownership;
- barrel involvement.

Do not report tool output without interpretation.

## TypeScript Project References

When present, validate:

- references follow intended package dependency direction;
- no reverse reference;
- no hidden path alias bypass;
- declarations/public types stay within intended package surface.

A successful TypeScript build does not guarantee architectural validity if path aliases bypass package exports.

## Package Exports

Validate `exports`/public entry points against supported consumption.

Check:

- internal paths not exported unintentionally;
- server/client surfaces explicit;
- test-only entry points not exposed to production consumers;
- package root not re-exporting private implementation;
- types align with public runtime exports.

## Architecture Tests

Custom architecture tests are valuable when they encode rules repeatedly relied upon.

Validate:

- they reflect current profile;
- false positives are understood;
- legitimate framework patterns are allowed;
- critical rules are represented;
- tests are included in CI.

Do not make architecture tests stricter than the accepted standard.

## CI Validation

Architecture rules that matter repeatedly SHOULD be automated in CI.

Record:

```text
LOCAL_ONLY
PR_BLOCKING
MAIN_BRANCH
NIGHTLY
NOT_AUTOMATED
```

Potential evidence:

- lint;
- typecheck;
- dependency graph;
- architecture tests;
- package build.

Do not invent a new gate without accepted CI policy.

## Automation Gap Analysis

For every important architecture rule classify:

```text
AUTOMATED_AND_BLOCKING
AUTOMATED_NON_BLOCKING
PARTIALLY_AUTOMATED
MANUAL_ONLY
NOT_ENFORCED
```

High-value repeated rules should not rely solely on memory.

Potential candidates:

- layer direction;
- cross-feature internals;
- package deep imports;
- cycles;
- client/server import restrictions.

## False Positives and Exceptions

Architecture tooling must match the selected project profile and framework.

Record exceptions with:

- rule;
- path;
- reason;
- owner;
- duration;
- removal trigger;
- validation.

Use:

```text
VALID_EXCEPTION
TEMPORARY_MIGRATION_EXCEPTION
TOOL_FALSE_POSITIVE
UNJUSTIFIED_EXCEPTION
POLICY_REQUIRES_UPDATE
```

Do not disable a whole rule because one path is exceptional.

## Violation Severity

Use:

```text
BLOCKER
HIGH
MEDIUM
LOW
ADVISORY
```

Suggested interpretation:

### BLOCKER

- Domain/Application reverse dependency that undermines architecture;
- server secret/client boundary leak;
- package cycle blocking independent evolution;
- Service Locator introduced across the feature;
- critical public-boundary bypass creating cross-capability coupling.

### HIGH

- components/hooks importing concrete adapters;
- cross-feature internal imports;
- unbounded shared-folder misuse with broad impact;
- production cycle across capabilities.

### MEDIUM

- overbroad public barrel;
- undocumented migration exception;
- architecture rule not automated despite repeated violations.

### LOW

- misplaced file with preserved dependencies;
- naming/ownership ambiguity with small blast radius.

Do not inflate severity for folder aesthetics.

## Evidence Requirements

Every finding should include:

- file/module/package;
- actual dependency/import;
- violated accepted rule;
- profile relevance;
- tool/manual evidence;
- consequence;
- smallest remediation target.

Avoid vague findings such as:

```text
architecture could be cleaner
```

Prefer:

```text
HIGH:
src/promotions/hooks/usePromotion.ts
imports src/promotions/infrastructure/adapters/HttpPromotionRepository.ts

Violation:
Components/hooks must not import concrete repository adapters.

Remediation:
inject the accepted semantic dependency from the feature composition boundary.
```

## Remediation Principles

Prefer the smallest architecture correction.

Examples:

```text
internal cross-feature import
→ export stable contract or move shared contract to justified shared owner

component imports adapter
→ inject semantic dependency from composition

Application imports Infrastructure
→ introduce/restore inward port

shared helper owned by one feature
→ move back to feature

deep package import
→ expose intentional public export or keep private and redesign consumer

cycle caused by barrel
→ replace broad barrel with direct intentional exports
```

Do not respond to one violation with a repository-wide rewrite.

## Architecture Definition of Done

Validate applicable architecture DoD:

- change belongs to recognizable business capability;
- dependency direction remains inward;
- no feature internal boundary is bypassed;
- selected architecture profile is respected;
- shared abstractions are justified.

Also inspect related boundary-sensitive concerns:

- public imports;
- composition;
- server/client;
- package exports;
- cycles.

Do not turn UI/data/test DoD into architecture findings unless they affect boundaries.

## Validation Versus Review

This skill is objective validation against accepted architecture.

It asks:

```text
Does the code violate a known boundary?
```

The later `reviewing-frontend-architecture` skill asks broader questions such as:

```text
Is the architecture still the right design?
Are ownership and abstractions healthy?
Should boundaries evolve?
```

Do not duplicate that broader review here.

## Validation Status

Use:

```text
ARCHITECTURE_VALID
ARCHITECTURE_VALID_WITH_ADVISORIES
ARCHITECTURE_INVALID
ARCHITECTURE_VALIDATION_BLOCKED
ARCHITECTURE_PROFILE_MISMATCH
AUTOMATION_GAPS_REMAIN
```

## Output

Use `assets/frontend-architecture-validation-record.md`.

## Completion Criteria

- [ ] Selected architecture profile is explicit.
- [ ] Validation rules are profile-aware.
- [ ] Production dependency direction is inspected.
- [ ] Domain/Application/Infrastructure rules are checked where those layers exist.
- [ ] Components/hooks do not import concrete adapters.
- [ ] Cross-feature imports use intentional public boundaries.
- [ ] Public surfaces and package exports are deliberate.
- [ ] Shared code has real consumers, stable semantics, and an owner.
- [ ] `shared` dumping-ground patterns are identified.
- [ ] Composition remains at an outer boundary.
- [ ] Service Locator patterns are detected.
- [ ] Server/client import separation is validated where applicable.
- [ ] Package deep imports and cycles are checked.
- [ ] File/feature/package cycles are classified accurately.
- [ ] Type-only, test-only, generated, and dynamic imports are interpreted correctly.
- [ ] Existing architecture tooling is discovered rather than assumed.
- [ ] Tooling results are mapped back to accepted architecture rules.
- [ ] Important repeated rules have automation-gap status.
- [ ] Exceptions are scoped and justified.
- [ ] Findings include evidence, severity, consequence, and smallest remediation.
- [ ] Folder aesthetics are not confused with architecture violations.
- [ ] No new architecture profile, tool, or repository-wide redesign is introduced.
- [ ] Final validation status is explicit.
