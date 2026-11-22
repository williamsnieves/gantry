---
name: migrating-to-frontend-vertical-slices
description: Portable engineering capability `migrating-to-frontend-vertical-slices`.
  Use when the harness or a specialist agent explicitly requires this named capability.
---
# Migrating to Frontend Vertical Slices

## Purpose

Move an existing frontend toward business-oriented vertical slices incrementally and safely.

The target principle is:

```text
source tree
→ communicates product capabilities
→ capability owns its frontend behavior
→ dependencies cross boundaries intentionally
```

Preferred shape when complexity justifies it:

```text
src/
├── orders/
├── subscriptions/
├── billing/
├── authentication/
└── shared/
```

rather than a root dominated by:

```text
components/
hooks/
services/
utils/
models/
```

The migration must preserve behavior and avoid a repository-wide rewrite.

## Roadmap Purpose

This skill MUST:

- move a flat or technical-layer-first codebase toward business slices incrementally;
- preserve behavior;
- define public feature boundaries;
- avoid a large rewrite.

## Roadmap Evaluations

This skill MUST cover:

```text
global components folder
services folder
shared hook ownership
circular dependencies
monorepo package extraction
```

## Governing Architecture Rules

### Screaming Architecture

The top-level tree SHOULD communicate product capabilities.

### Vertical Slicing

A capability MAY own:

```text
domain
application
infrastructure
components
hooks
styling
tests
```

only when those boundaries add value.

Do not create every layer mechanically.

### Dependency Direction

For modular/hexagonal profiles:

```text
UI / Infrastructure
→ Application
→ Domain
```

Dependencies point inward.

### Cross-Feature Imports

Feature code SHOULD NOT import another feature's internal files.

Cross-feature collaboration SHOULD use:

```text
intentional public API
application port
shared domain contract
event/routing boundary
documented package export
```

### Shared Code

Move code to `shared` only when it is:

- genuinely used by multiple capabilities;
- semantically stable;
- not owned by one feature;
- safe to evolve centrally.

`shared` MUST NOT become a dumping ground.

# Use When

- Root structure is dominated by `components`, `hooks`, `services`, `utils`, or `models`.
- Feature ownership is unclear.
- Components/hooks/services for one capability are scattered globally.
- Shared hooks actually belong to one feature.
- Cross-feature internal imports exist.
- Circular dependencies block clean ownership.
- A capability should expose a deliberate public surface.
- A monorepo package may eventually be extracted.
- A brownfield codebase needs incremental adoption of the frontend standard.
- A feature change is a safe opportunity to improve local architecture.

## Do Not Use When

- The codebase is greenfield.
- The architecture profile is not selected.
- The request is only to plan one new vertical slice.
- The task is a local component/hook refactor with no ownership migration.
- Behavior is unknown and no characterization evidence exists.
- The user wants a full rewrite.
- Package extraction is proposed only for aesthetics.
- The target feature boundary is still ambiguous.

## Inputs

- Definitive frontend engineering standard.
- Selected architecture profile.
- Current repository tree.
- Import/dependency graph.
- Feature/capability map.
- Existing public APIs/package exports.
- Current tests and runtime behavior.
- Accepted routes/API/browser contracts.
- Current styling/design-system conventions.
- Monorepo/workspace conventions.
- Existing architecture validation findings.
- Repository-local `AGENTS.md`.
- Migration constraints and release cadence.

## Outputs

- Current-state architecture map.
- Target capability map.
- Migration seam inventory.
- Public-surface design.
- Shared-code ownership decisions.
- Circular-dependency resolution plan.
- Incremental migration sequence.
- Characterization/safety-net plan.
- Compatibility/deprecation plan.
- Package-extraction readiness decision.
- Debt ledger.
- Vertical-slice migration record.

# Core Workflow

```text
understand current behavior
→ map current ownership/imports
→ identify one capability seam
→ define target slice + public surface
→ protect behavior
→ move one dependency cluster
→ redirect consumers
→ validate architecture + behavior
→ remove obsolete compatibility layer
→ repeat
```

# Migration Unit

Prefer:

```text
one capability
one route
one workflow
one cohesive dependency cluster
```

Do not migrate:

```text
all components
all hooks
all services
```

as horizontal batches unless repository constraints make that unavoidable.

# Current-State Mapping

Inventory:

```text
routes/screens
global components
global hooks
services
API clients
state
models/types
styles
tests
feature flags
cross-feature imports
shared utilities
```

Then assign:

```text
likely capability owner
truly shared
unknown
```

Do not move unknown ownership prematurely.

# Behavior Preservation

Before moving a behavior, identify:

```text
user-visible behavior
public route
API contract
browser/storage contract
state semantics
accessibility behavior
tests
```

Use characterization tests when existing tests do not protect current behavior.

# Characterization Evidence

Possible:

```text
component integration test
hook test
route/browser test
adapter test
E2E critical journey
snapshot only when visual contract is relevant
```

Do not rely solely on file-path equivalence.

# Migration Seam

A good seam has:

- clear business meaning;
- manageable dependency set;
- stable callers;
- testable behavior;
- limited cross-feature coupling.

Examples:

```text
subscription management route
billing invoice table
authentication recovery flow
order detail workflow
```

# Target Slice

Choose the lightest structure that fits selected profile.

### Profile A

```text
subscription/
├── components/
├── hooks/
├── api/
└── tests/
```

### Profile B/C

Potentially:

```text
subscription/
├── domain/
├── application/
├── infrastructure/
├── components/
├── hooks/
└── tests/
```

Do not create Domain/Application folders when behavior does not justify them.

# Public Feature Boundary

Large modules SHOULD expose a deliberate public surface.

Potential:

```text
subscription/index.ts
subscription/public.ts
package exports
```

Expose only stable contracts.

Avoid broad barrel exports that leak internals or hide cycles.

# Public Surface Design

Classify exports:

```text
PUBLIC_STABLE
PUBLIC_TRANSITIONAL
INTERNAL
DEPRECATED
```

Examples of stable public exports:

```text
route entry
feature container
application command/query contract
shared domain type when intentionally shared
navigation helper
```

Avoid exporting:

```text
private component internals
implementation hooks
concrete adapters
internal mappers
test fixtures
```

unless repository contract explicitly requires it.

# Cross-Feature Collaboration

When Feature A needs Feature B, ask:

```text
Does A need B's implementation
or only a stable capability contract?
```

Prefer:

```text
A
→ B public surface
```

not:

```text
A
→ B/internal/hooks/useWhatever
```

# Global Components Folder

Roadmap evaluation:

```text
global components folder
```

Classify every component by semantic ownership.

Possible decisions:

```text
MOVE_TO_FEATURE
KEEP_SHARED_UI
KEEP_APP_SHELL
KEEP_ROUTE_COMPOSITION
DELETE_DEAD
OWNERSHIP_REQUIRED
```

# Feature-Owned Components

Move when:

- terminology is capability-specific;
- business state/permissions are embedded;
- only one capability uses it;
- changes are driven by one capability.

Example:

```text
components/SubscriptionUpgradeCard.tsx
→ subscriptions/components/SubscriptionUpgradeCard.tsx
```

# Shared UI Components

Keep shared only when:

- behavior is generic;
- no business rule;
- multiple capabilities use it;
- API is semantically stable.

Examples:

```text
Button
Dialog
Stack
VisuallyHidden
DataTable primitive
```

A component that “looks generic” but knows `subscriptionStatus` is not shared UI.

# App Shell

Some global UI genuinely belongs to application shell:

```text
AppLayout
RouterBoundary
GlobalNavigation
ErrorBoundary
```

Do not force shell concerns into a business feature.

# Global Hooks Folder

Roadmap evaluation:

```text
shared hook ownership
```

For each hook determine:

```text
feature behavior?
browser primitive?
server-state binding?
shared infrastructure?
generic UI utility?
```

# Feature Hook

Example:

```text
hooks/useSubscriptionUpgrade
```

belongs to `subscriptions` if it encodes:

- subscription state;
- upgrade orchestration;
- feature-specific permissions;
- feature-specific query keys.

# Shared Hook

Examples may include:

```text
useMediaQuery
useReducedMotion
useEventListener
```

if implemented generically and truly reused.

Do not move hooks to shared because two files import them temporarily.

# Hook Publicity

A feature hook may remain internal even if several components in the feature use it.

Cross-feature consumers should generally use a stable feature API instead of importing the hook directly.

# Services Folder

Roadmap evaluation:

```text
services folder
```

"Service" is often ambiguous.

Classify each service:

```text
HTTP/provider adapter
Application Use Case
server-state gateway
Domain service
browser adapter
composition/configuration
miscellaneous god service
```

Then move according to responsibility.

# Service Example

Before:

```text
services/subscriptionService.ts
```

containing:

```text
fetch
mapping
business validation
toast
navigation
```

This is mixed responsibility.

Migration may split into:

```text
subscriptions/application/
subscriptions/infrastructure/
subscriptions/components/hooks/
```

only as justified.

# No Mechanical Service Renaming

Do not rename:

```text
service
→ repository
```

without changing the actual boundary.

A forwarding wrapper adds no architectural value.

# Utils Folder

Global `utils` often mixes ownership.

Classify:

```text
business utility
feature mapper
formatting primitive
browser utility
generic algorithm
test helper
```

Move business-specific functions to owning feature.

Keep truly generic utilities shared.

# Models / Types Folder

Types should follow ownership.

Examples:

```text
Subscription
SubscriptionViewData
SubscriptionApiResponse
```

usually belong near `subscriptions`.

Do not centralize all types merely for import convenience.

# State Ownership

Migrate state with capability ownership.

Do not leave:

```text
global store slice
```

in a technical folder while all consumers moved to feature if feature owns it.

But do not migrate global cross-capability state into one feature incorrectly.

# Server State

Query keys, query functions, mappers, and hooks should follow feature/data ownership.

Avoid cross-feature direct access to another feature's query internals.

Use public feature boundary or shared server-state contract when intentional.

# Styling

Move feature-specific styles with feature.

Keep:

- global tokens;
- design-system primitives;
- app shell themes;

in accepted shared locations.

Do not duplicate tokens/styles during migration.

# Tests

Tests SHOULD move with ownership when repository convention supports colocated/feature tests.

Do not break test discoverability/config.

Preserve:

```text
behavior
fixtures
test IDs/contracts
CI
```

# Circular Dependencies

Roadmap evaluation:

```text
circular dependencies
```

Do not solve a cycle by:

```text
moving both modules to shared
```

automatically.

Find root cause:

```text
mutual feature internals
ambiguous ownership
barrel cycle
composition leak
shared contract hidden inside feature
runtime registration
```

# Cycle Resolution

Potential fixes:

```text
define one-way ownership
extract narrow neutral contract
move orchestration up to composition/root
invert dependency via port/callback
use event/routing boundary
replace broad barrel with direct public export
```

# Cycle Example

Bad:

```text
subscriptions
→ billing/internal/useInvoice

billing
→ subscriptions/internal/useSubscription
```

Potential:

```text
billing/public.ts
subscriptions/public.ts

route/container
→ composes both
```

or shared stable contract if truly neutral.

# Dependency Direction

After each migration step verify:

```text
feature internals do not leak
Application does not import Infrastructure
components/hooks do not import concrete adapters when selected profile forbids it
shared does not import feature
```

# Shared Dependency Rule

Prefer:

```text
feature → shared
```

Avoid:

```text
shared → feature
```

because it reverses ownership and often creates cycles.

# Compatibility Seam

During migration, temporary compatibility may be needed.

Examples:

```text
old import path re-export
facade
adapter
deprecated public alias
route redirect
```

Every seam needs:

```text
reason
owner
exit condition
removal date/milestone
```

# Transitional Re-export

Example:

```ts
// old/components/SubscriptionCard.ts
export { SubscriptionCard } from "@/subscriptions/public"
```

Can reduce PR blast radius.

But it is temporary debt.

Do not leave permanent alias forests.

# Deprecation

Mark transitional exports according to repo convention:

```text
deprecated comment
migration issue
codemod/grep list
```

Avoid breaking all consumers in one commit if incremental redirection is safer.

# Import Rewrite

Update consumers gradually.

After each batch:

```text
typecheck
lint
tests
architecture validation
```

Do not mass-rewrite imports without behavior validation.

# Monorepo Package Extraction

Roadmap evaluation:

```text
monorepo package extraction
```

Package extraction is not the first migration step.

First prove the capability has:

- stable ownership;
- stable public surface;
- inward dependency direction;
- limited app-shell coupling;
- limited cross-feature internals;
- clear runtime/config dependencies;
- independent testability.

# Package Extraction Readiness

Use:

```text
PACKAGE_EXTRACTION_READY
PACKAGE_EXTRACTION_READY_WITH_CONDITIONS
KEEP_AS_APP_FEATURE
BOUNDARY_NOT_STABLE
PUBLIC_API_NOT_STABLE
CYCLE_BLOCKS_EXTRACTION
RUNTIME_COUPLING_BLOCKS_EXTRACTION
```

# Do Not Extract for Folder Aesthetics

Bad reason:

```text
folder is large
```

Better reasons:

```text
multiple apps consume capability
independent release/versioning is valuable
package boundary improves ownership/enforcement
```

# Package Public API

Before extraction, define package exports explicitly.

Avoid:

```text
exports: "./src/*"
```

that exposes internals.

Prefer stable package entry points.

# Package Dependencies

Check:

```text
React/framework peer deps
design-system dependency
routing
server-state
environment config
assets
CSS
browser APIs
internal aliases
```

A feature that imports app singleton/config everywhere may not be package-ready.

# Monorepo Circularity

Package extraction can reveal:

```text
package A ↔ package B
```

Do not resolve by creating `shared-everything`.

Find capability ownership or introduce a narrow contract package only when semantically stable.

# Composition Root

Cross-feature wiring often belongs higher:

```text
route
page
app composition
dependency composition
```

Move orchestration upward rather than making features import each other's implementations.

# Route Ownership

A route may compose several capabilities.

Do not assign every route dependency to one feature if the route is genuinely application composition.

# Feature Entry Point

Potential:

```text
subscriptions/public.ts
```

could expose:

```text
SubscriptionRoute
SubscriptionSummary
subscriptionNavigation
```

while keeping:

```text
adapters
mappers
internal hooks
```

private.

# Incremental Migration Sequence

Recommended:

```text
1. map
2. protect behavior
3. select one capability
4. define public surface
5. move feature-owned leaf modules
6. redirect imports
7. move state/data ownership
8. resolve cycles
9. validate
10. remove obsolete compatibility
11. repeat
```

# Leaf-First Moves

Move modules with few dependencies first.

This reveals boundary issues before moving central orchestration.

Do not start with the most connected god service unless migration seam requires it.

# Vertical Behavior First

Prefer migrating one behavior end-to-end:

```text
subscription list
→ query
→ mapper
→ hook
→ component
→ test
```

instead of:

```text
move all hooks first
```

This produces usable architecture after each step.

# Strangler Pattern

A practical brownfield approach:

```text
legacy technical structure
├── untouched behavior
└── compatibility seam
        ↓
new feature slice
```

New/changed behavior flows through the new slice while legacy shrinks incrementally.

# New Code Rule

During migration:

```text
new code
→ target architecture
```

unless compatibility constraint requires otherwise.

Do not add new feature-specific modules to known legacy global folders merely because migration is incomplete.

# No Worsened Drift

A migration change should not:

- add new cross-feature internal imports;
- add new feature-specific shared code;
- add new cycles;
- broaden public barrels;
- deepen service god objects.

# Existing Debt

Distinguish:

```text
PRE_EXISTING_DEBT
CHANGE_LOCAL_REQUIRED
NEW_DEBT
ACCEPTED_TEMPORARY_DEVIATION
```

Do not block a local migration on unrelated repository-wide debt.

# Mandatory Fixes

Do not postpone:

- broken security boundaries;
- tenant isolation issues;
- data-loss behavior;
- build/runtime breakage;

as optional migration debt.

# Architecture Profile Preservation

Do not force Profile C on Profile A.

Migration target should match the selected profile.

A simple feature may remain:

```text
feature/
├── components/
├── hooks/
├── api/
└── tests/
```

# Ceremonial Layers

Do not create empty:

```text
domain/
application/
infrastructure/
```

folders merely to match diagrams.

Every layer must represent a real responsibility.

# Shared UI Boundary

Reusable UI primitives may live in accepted shared UI locations.

Business logic MUST NOT live in shared UI primitives.

# Shared Abstraction Promotion

Before moving a module to shared, require:

```text
at least multiple genuine consumers
semantic stability
neutral ownership
central evolution is beneficial
```

Do not promote on speculation.

# Duplication During Migration

Temporary duplication may be safer than premature abstraction when two capabilities are still diverging.

Record and revisit.

Do not immediately centralize every repeated 5-line function.

# Public API Stability

During migration, preserve:

- route contracts;
- package exports consumed externally;
- import aliases promised to other packages;
- event names;
- storage keys;
- query params;
- component contracts used outside scope.

Change only with explicit migration plan.

# Import Aliases

Update path aliases carefully.

Avoid making aliases so broad that they hide feature-internal imports.

# Barrel Files

Broad barrels can hide:

- cycles;
- internal leakage;
- accidental bundle inclusion.

Use narrow intentional public surfaces.

# Tree Shaking

Package/public-surface changes can affect bundling.

If performance-sensitive, hand off to:

```text
reviewing-frontend-performance
```

# Security / Privacy

Moving modules must not accidentally:

- expose server-only code to client;
- expose secrets;
- bypass analytics policy;
- move auth logic to client.

Use security/privacy review if relevant.

# Accessibility

Migration should preserve semantics/focus/keyboard behavior.

Moving component ownership is not justification for UI rewrite.

# Behavior-Preserving Rule

Default:

```text
architecture changes
→ no user-visible behavior change
```

unless migration is bundled with an explicitly accepted feature change.

Separate structural and behavioral diffs where possible.

# Change Size

Prefer PRs that reviewers can reason about.

Potential sequence:

```text
PR 1: establish public surface + tests
PR 2: move feature components/hooks
PR 3: move services/adapters/state
PR 4: redirect consumers + remove aliases
```

Adapt to repository size.

# Migration Branch Strategy

Do not maintain long-lived huge migration branches if small mergeable steps are possible.

# Validation After Each Step

Run repository-approved:

```text
lint
typecheck
tests
build
architecture validation
critical E2E if affected
```

The Validator Agent later verifies execution, but this skill defines what evidence is needed.

# Architecture Validation

Use:

```text
validating-frontend-architecture
```

to verify:

- dependency direction;
- feature boundary;
- public surface;
- shared misuse;
- cycles;
- package boundaries.

# Architecture Review

After meaningful migration:

```text
reviewing-frontend-architecture
```

can assess broader health.

# Refactor Handoff

If the feature internals themselves remain mixed after ownership migration, use:

```text
refactoring-react-features
```

Do not overload this migration skill with every internal React refactor.

# Migration Finding Structure

Record:

```text
current path
current owner
target owner
reason
dependencies
public/private status
compatibility need
test protection
migration step
exit condition
```

# Ownership Decision

Use:

```text
FEATURE_OWNED
SHARED_UI
SHARED_INFRASTRUCTURE
APP_SHELL
COMPOSITION_ROOT
CROSS_FEATURE_CONTRACT
PACKAGE_PUBLIC
OWNERSHIP_UNRESOLVED
```

# Migration Status

Use:

```text
MIGRATION_READY
MIGRATION_READY_WITH_CONDITIONS
BEHAVIOR_CHARACTERIZATION_REQUIRED
FEATURE_OWNERSHIP_REQUIRED
PUBLIC_SURFACE_REQUIRED
CIRCULAR_DEPENDENCY_REQUIRES_RESOLUTION
PACKAGE_EXTRACTION_NOT_READY
MIGRATION_IN_PROGRESS
MIGRATION_COMPLETE_FOR_SCOPE
BLOCKED
```

# Roadmap Evaluation — Global Components Folder

Passing result:

- each moved component has explicit capability/shared/app-shell owner;
- business components move to features;
- generic primitives remain shared;
- no blind folder rename.

# Roadmap Evaluation — Services Folder

Passing result:

- services are classified by actual responsibility;
- mixed services are decomposed only where value exists;
- concrete HTTP/provider work moves to infrastructure;
- application behavior moves inward when profile justifies;
- no `services/`→`repositories/` mechanical rename.

# Roadmap Evaluation — Shared Hook Ownership

Passing result:

- hook semantics determine owner;
- feature-specific hooks move to feature;
- generic browser/UI hooks remain shared;
- cross-feature consumers use stable public contracts.

# Roadmap Evaluation — Circular Dependencies

Passing result:

- root ownership/dependency problem is identified;
- cycle is broken through direction, composition, port, event, or narrow neutral contract;
- `shared` is not used as a cycle trash bin.

# Roadmap Evaluation — Monorepo Package Extraction

Passing result:

- capability/public API is already stable;
- dependencies are directional;
- app-runtime coupling is understood;
- extraction has a business/engineering reason;
- package exports do not leak internals.

# Over-Migration Audit

Flag:

- big-bang folder rewrite;
- all technical folders moved at once;
- every repeated module promoted to shared;
- package extraction before public API;
- empty ceremonial layers;
- architecture rewrite combined with unrelated UI redesign.

Use:

```text
INCREMENTAL_VERTICAL_SLICE_MIGRATION
BIG_BANG_MIGRATION
PREMATURE_SHARED_ABSTRACTION
PREMATURE_PACKAGE_EXTRACTION
CEREMONIAL_ARCHITECTURE
```

# Under-Migration Audit

Flag:

- files moved but imports still bypass boundaries;
- public barrels expose internals;
- legacy aliases never removed;
- shared still imports features;
- cycles remain hidden;
- new code continues entering legacy folders.

# Final Decision

Use:

```text
FRONTEND_VERTICAL_SLICE_MIGRATION_READY
FRONTEND_VERTICAL_SLICE_MIGRATION_READY_WITH_CONDITIONS
FRONTEND_VERTICAL_SLICE_MIGRATION_REQUIRES_CHARACTERIZATION
FRONTEND_VERTICAL_SLICE_MIGRATION_REQUIRES_OWNERSHIP_DECISION
FRONTEND_VERTICAL_SLICE_MIGRATION_REQUIRES_CYCLE_RESOLUTION
MONOREPO_PACKAGE_EXTRACTION_NOT_READY
FRONTEND_VERTICAL_SLICE_MIGRATION_COMPLETE_FOR_SCOPE
BLOCKED
```

## Output

Use `assets/frontend-vertical-slice-migration-record.md`.

## Completion Criteria

- [ ] Selected architecture profile is known.
- [ ] Current technical-layer structure is mapped.
- [ ] Capability ownership is mapped.
- [ ] User-visible behavior/contracts are protected.
- [ ] Characterization evidence exists where behavior was previously unprotected.
- [ ] Migration operates on one capability/cohesive seam at a time.
- [ ] Target slice uses the lightest justified structure.
- [ ] Public feature surface is deliberate and narrow.
- [ ] Cross-feature consumers stop importing internals.
- [ ] Global components are classified by feature/shared/app-shell ownership.
- [ ] Feature-specific components move with their capability.
- [ ] Shared UI remains business-logic free.
- [ ] Services are classified by real responsibility rather than name.
- [ ] Mixed services are decomposed only as needed.
- [ ] Feature-specific hooks have feature ownership.
- [ ] Shared hooks are genuinely generic/stable.
- [ ] Global utils/types are re-owned where business-specific.
- [ ] State/server-state ownership moves with capability when appropriate.
- [ ] Dependency direction matches selected profile.
- [ ] Shared does not import feature internals.
- [ ] Circular dependencies are resolved at the root cause.
- [ ] Shared is not used as a cycle dumping ground.
- [ ] Compatibility seams are temporary and have exit conditions.
- [ ] New code follows target architecture during migration.
- [ ] No new/worsened architectural drift is introduced.
- [ ] Package extraction is deferred until public boundary is stable.
- [ ] Package exports are deliberate if extraction is approved.
- [ ] App/runtime coupling is understood before package extraction.
- [ ] Styling/tests/accessibility behavior are preserved.
- [ ] Each migration step runs focused validation.
- [ ] `validating-frontend-architecture` is used after structural movement.
- [ ] `refactoring-react-features` is handed off when internal responsibilities still need cleanup.
- [ ] Final migration status is explicit.

## References

- Read `references/current-state-capability-and-ownership-mapping.md` first.
- Read `references/public-feature-surfaces-cross-feature-contracts-and-barrels.md`.
- Read `references/global-components-hooks-services-utils-and-types.md`.
- Read `references/circular-dependencies-composition-and-shared-boundaries.md`.
- Read `references/incremental-migration-characterization-and-compatibility-seams.md`.
- Read `references/monorepo-package-extraction-readiness.md`.
- Read `references/validation-debt-ledger-and-migration-completion.md`.
- Read `references/frontend-vertical-slice-migration-audit.md` before completion.
