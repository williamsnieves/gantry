---
name: classifying-frontend-architecture-profile
description: Selects the lightest frontend architecture profile that preserves the required boundaries for a feature, application, or package. Use when deciding between Profile A (simple feature/application), Profile B (modular frontend), and Profile C (large product/monorepo), especially when Domain/Application layers, ports, public package contracts, capability ownership, offline behavior, or independent evolution are uncertain. Base the decision on accepted behavior, repository reality, consumers, state complexity, authority, testability, and scaling triggers. Do not implement code, force hexagonal layers, treat folder count as architecture, create speculative packages or shared abstractions, or leave complex client-owned behavior in a flat feature without justification.
...
---

# Classifying Frontend Architecture Profile

## Purpose

Choose the lightest frontend architecture profile that preserves the boundaries required by the accepted behavior and the repository.

Profiles:

```text
Profile A — Small feature or small application
Profile B — Modular frontend
Profile C — Large product or monorepo
```

The classification must prevent:

```text
overengineering
and
under-structuring
```

The output is a profile decision, rationale, required boundaries, deferred complexity, and scaling triggers.

This skill does not implement or reorganize code.

## Use When

- The current frontend profile is unclear or mixed.
- A feature may or may not justify Domain and Application layers.
- A flat feature is gaining business, offline, optimistic, or workflow complexity.
- A monorepo capability may need a public package contract.
- A proposed shared package may be speculative.
- A legacy technical-folder structure needs a change-local profile decision.
- Several applications consume or may consume one capability.
- `applying-frontend-engineering-standard` returned `FRONTEND_PROFILE_CLASSIFICATION_REQUIRED`.

## Do Not Use When

- The selected profile is already accepted and the task is implementation.
- The task is only to plan vertical slices.
- The task is to redesign the complete repository.
- The only argument is preferred folder naming.
- The user requests code generation.
- The accepted behavior and ownership cannot be determined.
- The task is backend-only.

## Inputs

- Accepted change or capability behavior.
- Frontend standard application record.
- Repository and workspace structure.
- Current feature/module organization.
- Existing `AGENTS.md` and architecture decisions.
- Runtime/rendering model.
- State and server-state strategy.
- Data and browser dependencies.
- Existing consumers and ownership.
- Test and deployment boundaries.
- Product evolution and compatibility constraints.

## Outputs

- Selected profile.
- Confidence and evidence.
- Architecture rationale.
- Required capability, folder, and dependency boundaries.
- Domain/Application justification or rejection.
- Shared/public boundary decision.
- Current-to-target delta.
- Deferred complexity.
- Scaling triggers.
- Migration conditions when the current structure differs.
- Frontend architecture profile record.

## Governing Rule

Projects MUST select the lightest profile that preserves required boundaries.

```text
Complexity MUST be earned.
```

The goal is not the fewest files.

The goal is the smallest architecture that:

- keeps ownership clear;
- preserves correctness;
- supports required testing;
- isolates meaningful dependencies;
- allows accepted evolution;
- avoids speculative abstraction.

## Profile Definitions

## Profile A — Small Feature or Small Application

Typical shape:

```text
feature/
├── components/
├── hooks/
├── api/
└── tests/
```

Use when:

- business logic is limited;
- Domain modeling adds little value;
- behavior mostly coordinates UI and server state;
- the feature has one application owner;
- external dependencies are already hidden by approved shared infrastructure;
- the feature is unlikely to evolve independently;
- offline and complex optimistic workflows are absent;
- feature-level tests can prove behavior clearly.

Profile A may still use:

- typed data mapping;
- custom hooks;
- feature-local components;
- accessible UI;
- approved server-state abstractions;
- feature-local adapters when small and clear.

Profile A does not mean unstructured code.

## Profile B — Modular Frontend

Typical shape:

```text
feature/
├── domain/
├── application/
├── infrastructure/
└── tests/
```

Use when:

- meaningful client-owned business rules exist;
- deterministic behavior must remain React-independent;
- external browser or remote capabilities require ports;
- offline or optimistic transitions have real policy;
- a rich editor/workflow has independent lifecycle;
- several UI entry points share one application behavior;
- testability and independent capability evolution matter;
- transport/provider types must be isolated from inner logic.

Profile B does not require every folder for every behavior.

Create only the layers justified by the selected capability.

## Profile C — Large Product or Monorepo

Typical shape:

```text
apps/
packages/
features/
shared/
```

Use when:

- multiple applications consume a capability;
- ownership boundaries are explicit;
- public package contracts are required;
- independent delivery, versioning, or release matters;
- platform teams own shared UI/data/runtime capabilities;
- package dependency direction must be enforced;
- consumers have different adapters or composition roots.

Profile C is not justified solely because a repository uses workspaces.

A monorepo may still contain Profile A and B features inside applications.

## Classification Workflow

1. **Confirm scope and accepted behavior.**
2. **Map the current repository and feature profile.**
3. **Identify capability ownership.**
4. **Assess behavior and state complexity.**
5. **Assess local versus server authority.**
6. **Assess external dependency boundaries.**
7. **Assess consumers, reuse, and public contracts.**
8. **Assess testability, rendering, and deployment boundaries.**
9. **Challenge overengineering and under-structuring.**
10. **Select the lightest valid profile.**
11. **Define required boundaries and explicitly excluded complexity.**
12. **Define scaling triggers and migration conditions.**

## Readiness Gate

Use one:

```text
READY_TO_CLASSIFY_FRONTEND_PROFILE
READY_WITH_CONDITIONS
BEHAVIOR_SCOPE_REQUIRED
OWNERSHIP_DECISION_REQUIRED
CONSUMER_EVIDENCE_REQUIRED
AUTHORITY_DECISION_REQUIRED
PRODUCT_EVOLUTION_DECISION_REQUIRED
BLOCKED
```

Stop when:

- behavior is too vague;
- ownership is disputed;
- local versus server authority is unknown;
- a proposed shared package has no confirmed consumers;
- offline/optimistic requirements are unresolved;
- the classification would depend on invented future scale.

## Scope

Classify one of:

```text
FEATURE
CAPABILITY
APPLICATION
PACKAGE
WORKSPACE
```

A feature-level decision should not redesign the workspace.

A package-level decision must identify actual consumers and public contracts.

## Evidence

Use evidence in this order:

1. accepted behavior;
2. repository-local architecture decisions;
3. current consumers and ownership;
4. client-owned state transitions and rules;
5. data/browser dependencies;
6. test and release boundaries;
7. current folder structure;
8. anticipated future needs with explicit commitment.

Current folders are evidence, not the final answer.

A legacy flat structure may still require Profile B for the selected change.

## Behavior Complexity

Assess:

- number of user intentions;
- state transitions;
- invariants;
- long-lived client state;
- undo/redo;
- optimistic updates;
- offline behavior;
- conflict resolution;
- collaboration;
- retry/reconciliation;
- derived calculations;
- independent evolution.

Use:

```text
LOW
MODERATE
HIGH
```

Do not equate UI visual complexity with Domain complexity.

A visually complex dashboard may remain Profile A if it only displays server-owned data.

A simple-looking offline workflow may require Profile B.

## Local Versus Server Authority

Classify behavior:

```text
SERVER_AUTHORITATIVE
CLIENT_AUTHORITATIVE
SHARED_OR_RECONCILED_AUTHORITY
PRESENTATIONAL_ONLY
UNKNOWN
```

### Server-Authoritative

The server owns the business truth.

Frontend may validate for UX, but should avoid duplicating authoritative business rules.

Usually favors Profile A unless other boundaries justify Profile B.

### Client-Authoritative

The client owns meaningful deterministic state or behavior.

Examples:

- rich editor;
- offline draft lifecycle;
- local simulation;
- undo/redo;
- client-only workflow.

Often supports Profile B.

### Shared or Reconciled Authority

The client performs optimistic/offline behavior and later reconciles with the server.

Usually supports Profile B and explicit ports, failure semantics, and state transitions.

## Domain Layer Justification

A frontend Domain layer is justified when it protects:

- client-owned invariants;
- meaningful state transitions;
- deterministic offline behavior;
- reusable pure rules;
- rich workflow/editor state;
- reconciliation logic with business meaning.

It is not justified merely for:

- API response interfaces;
- date formatting;
- field-required checks already owned by forms;
- one-off filtering/sorting for display;
- backend business validation copied for convenience;
- naming consistency.

Use one:

```text
FRONTEND_DOMAIN_REQUIRED
FRONTEND_DOMAIN_NOT_JUSTIFIED
FRONTEND_DOMAIN_TENTATIVE
DOMAIN_AUTHORITY_DECISION_REQUIRED
```

## Application Layer Justification

A frontend Application layer is justified when it coordinates a user intention independently of React.

Examples:

- load, merge, and reconcile data from several ports;
- submit a workflow with cancellation and stable failures;
- orchestrate offline persistence and synchronization;
- coordinate browser capabilities;
- provide the same intention to several UI entry points.

It is not justified for a hook that only wraps one SWR query or forwards one API call.

Use one:

```text
FRONTEND_APPLICATION_REQUIRED
FRONTEND_APPLICATION_NOT_JUSTIFIED
FRONTEND_APPLICATION_TENTATIVE
```

## Port and Adapter Justification

A port is justified when it protects inner behavior from an outer dependency such as:

- remote repository;
- browser storage;
- clipboard;
- files;
- notifications;
- analytics;
- geolocation;
- clock;
- feature flags;
- collaboration transport.

Do not create ports that mirror:

- generic fetch;
- Axios;
- SDK methods;
- browser APIs without semantic meaning;
- one helper with no inner policy.

One implementation may still justify a port when the boundary is meaningful.

## Profile A Indicators

Strong indicators:

- one route/screen;
- limited state;
- server-authoritative data;
- approved HTTP/server-state abstractions already exist;
- no meaningful client invariants;
- no offline or reconciliation;
- one application consumer;
- feature-local UI and tests are sufficient;
- no independent package/release need.

Risks that may still require separation inside Profile A:

- effects;
- accessibility;
- mapping;
- testability;
- component size.

Do not promote to Profile B solely because a custom hook exists.

## Profile B Indicators

Strong indicators:

- client-owned lifecycle;
- rich editor/workflow;
- offline drafts;
- optimistic transitions with rollback;
- conflict resolution;
- several UI surfaces share one intention;
- browser capabilities need semantic ports;
- provider/API mapping must be isolated;
- pure rules need direct tests;
- capability evolves independently inside one application.

Do not require Profile B simply because the backend uses DDD.

## Profile C Indicators

Strong indicators:

- two or more actual applications consume the capability;
- package contract has an owner;
- consumers require different Infrastructure/composition;
- independent release/versioning matters;
- workspace boundaries are enforced;
- platform/design-system packages have explicit governance;
- breaking-change management is required.

Weak indicators that are insufficient alone:

- repository uses pnpm workspaces;
- code might be reused someday;
- one component looks generic;
- team prefers packages;
- file count is large.

## Consumer Evidence

Classify reuse:

```text
ONE_REAL_CONSUMER
MULTIPLE_REAL_CONSUMERS
PLANNED_COMMITTED_CONSUMERS
SPECULATIVE_REUSE
PLATFORM_BOUNDARY
```

Profile C or shared-package extraction normally requires:

```text
MULTIPLE_REAL_CONSUMERS
or
PLATFORM_BOUNDARY
```

A committed second consumer may justify preparatory boundaries, but not necessarily immediate package extraction.

## Ownership

For each proposed profile record:

- capability owner;
- application owner;
- package owner;
- public API owner;
- design-system/platform owner;
- migration owner.

Shared code without a clear owner is a risk.

Do not classify something as `shared` merely because no team wants ownership.

## Public Boundaries

Profile C public contracts may include:

- package exports;
- component APIs;
- Application DTOs;
- Domain types;
- adapter ports;
- design tokens;
- extension points.

The public API should be smaller than the package internals.

Do not expose implementation files through deep imports.

Profile A and B may also use feature entry points without becoming packages.

## Rendering Model

Assess:

- client rendering;
- SSR;
- SSG;
- React Server Components;
- hydration;
- streaming;
- client-only widgets.

Rendering model may justify separation of:

- server-executed code;
- browser adapters;
- serialized data;
- client composition.

Rendering complexity alone does not automatically require Profile B or C.

## State Boundary

Assess:

- server state;
- local UI state;
- form state;
- URL state;
- browser persistence;
- shared client state;
- optimistic state;
- offline state.

Do not choose Profile B because several `useState` calls exist.

Choose based on ownership, lifecycle, invariants, and coordination.

## Testing Implications

### Profile A

Typical:

- component tests;
- hook tests when needed;
- adapter/data mapping tests;
- accessibility checks;
- critical E2E.

### Profile B

Typical:

- Domain tests;
- Application Use Case tests;
- adapter tests;
- hook/component tests;
- accessibility;
- architecture validation;
- critical E2E.

### Profile C

Additionally:

- package contract tests;
- consumer integration;
- dependency-boundary checks;
- version/compatibility validation;
- independent build/release checks.

Testing needs may reveal under-structuring.

If pure business behavior can only be tested through broad component/E2E tests, Profile A may be insufficient.

## Deployment and Release

Profile C is strengthened by:

- independent publishing;
- independent versioning;
- separate application deployment;
- compatibility windows;
- package consumer matrices.

A shared repository build alone is not independent delivery.

## Mixed Profiles

A repository may legitimately contain:

```text
Profile A features
inside a Profile C monorepo

Profile B capabilities
inside one application

shared UI packages
with feature-local Profile A usage
```

Use:

```text
MIXED_PROFILE_ACCEPTED
```

when boundaries are explicit.

Do not force one global profile onto every feature.

## Legacy Flat Structure

A legacy root may contain:

```text
components/
hooks/
services/
utils/
```

Classify the selected behavior independently.

Possible result:

```text
current: flat/technical
target for selected capability: Profile A or B
migration: change-local screaming boundary
```

Do not reorganize unrelated files.

## Overengineering Checks

Challenge:

- Domain layer with no business behavior;
- Use Case wrapping one API call;
- port mirroring `fetch`;
- generic repository for one endpoint;
- package with one speculative consumer;
- shared component used once;
- abstract factory with one stable choice;
- duplicated DTO hierarchy without boundary value;
- architecture created only to match backend folders.

Every abstraction must protect an actual boundary.

## Under-Structuring Checks

Challenge:

- offline lifecycle inside one large hook;
- business rules duplicated across components;
- several UI entry points reimplement one intention;
- provider/browser details spread through components;
- impossible pure testing without rendering;
- shared state with unclear owner;
- direct deep imports across applications/packages;
- local component folder acting as an undocumented platform package.

## Profile Scoring

A score may assist reasoning but must not replace judgment.

Consider dimensions:

| Dimension | A | B | C |
|---|---|---|---|
| Business/client rules | low | moderate/high | varies |
| Consumers | one | one app, several surfaces | several apps/packages |
| Authority | server/presentational | client/shared | any |
| Offline/reconciliation | absent | meaningful | shared/platform scale |
| Public contracts | feature-local | capability-local | package-level |
| Independent release | no | usually no | often yes |
| Ports/adapters | minimal | meaningful | per app/package |
| Test boundaries | UI-focused | layered | layered + consumer contracts |

Do not publish a numeric score as certainty when evidence is incomplete.

## Selected Profile

Use exactly:

```text
PROFILE_A_SELECTED
PROFILE_B_SELECTED
PROFILE_C_SELECTED
MIXED_PROFILE_SELECTED
PROFILE_DECISION_BLOCKED
```

Include confidence:

```text
HIGH
MEDIUM
LOW
```

## Required Structure

Specify only required boundaries.

Example Profile A:

```text
subscriptions/
├── components/
├── hooks/
├── api/
└── tests/
```

Example Profile B:

```text
editor/
├── domain/
├── application/
├── infrastructure/
│   ├── adapters/
│   └── ui/
└── tests/
```

Example Profile C:

```text
apps/admin
apps/customer
packages/promotion-capability
packages/ui
```

Do not create empty folders in the decision.

## Deferred Complexity

Explicitly state what is not justified now:

- Domain layer;
- Application layer;
- package extraction;
- generic port;
- shared state;
- design-system promotion;
- offline support;
- independent versioning.

This protects against speculative growth.

## Scaling Triggers

Define observable triggers for reconsidering the profile.

Examples:

- second real application consumer;
- second UI surface sharing one intention;
- offline lifecycle introduced;
- optimistic reconciliation becomes complex;
- duplicated business rule appears;
- package needs independent versioning;
- provider/browser dependency spreads to several callers;
- component tests become unable to prove pure behavior;
- capability gets a dedicated owner.

Avoid “when the project grows.”

## Migration Decision

When current and selected profiles differ, use:

```text
NO_MIGRATION_REQUIRED
CHANGE_LOCAL_MIGRATION
INCREMENTAL_CAPABILITY_MIGRATION
PACKAGE_EXTRACTION_REQUIRED
MIGRATION_DECISION_REQUIRED
```

Migration should preserve behavior and avoid unrelated reorganization.

Route implementation planning to:

```text
planning-frontend-vertical-slices
```

## Conflicts and Deviations

Record:

- existing architecture conflicts;
- local overrides;
- temporary mixed profile;
- package/deep-import debt;
- shared ownership exceptions.

A deviation needs scope, reason, risk, owner, and exit condition when temporary.

## Final Decision

Use one:

```text
FRONTEND_PROFILE_CLASSIFIED
FRONTEND_PROFILE_CLASSIFIED_WITH_CONDITIONS
MORE_EVIDENCE_REQUIRED
OWNERSHIP_DECISION_REQUIRED
PRODUCT_EVOLUTION_DECISION_REQUIRED
BLOCKED
```

## Output

Use `assets/frontend-architecture-profile-record.md`.

## Completion Criteria

- [ ] Scope and accepted behavior are explicit.
- [ ] Repository and current feature structure were inspected.
- [ ] Capability and ownership are identified.
- [ ] Behavior complexity is distinguished from visual complexity.
- [ ] Local, server, shared, or presentational authority is classified.
- [ ] Domain and Application layers are justified or rejected explicitly.
- [ ] Ports and adapters are tied to meaningful boundaries.
- [ ] Consumer and public-contract evidence is explicit.
- [ ] Rendering, state, testing, deployment, and release implications were considered.
- [ ] Both overengineering and under-structuring were challenged.
- [ ] The lightest valid profile was selected.
- [ ] Required structure contains no ceremonial empty layers.
- [ ] Deferred complexity and scaling triggers are concrete.
- [ ] Migration conditions are change-local and proportionate.
- [ ] No implementation or broad repository redesign was produced.
