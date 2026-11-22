---
name: reviewing-frontend-architecture
description: Reviews a frontend change against the definitive frontend engineering standard after objective architecture validation. Use to identify mandatory architectural violations, state-management risks, accessibility gaps, styling inconsistencies, test-strategy weaknesses, performance concerns, security/privacy issues, and accepted deviations. Separate MUST/MUST NOT violations from SHOULD-level suggestions, cite rule evidence, explain user/engineering impact, and recommend the smallest remediation. Do not treat preferences as blockers, re-run architecture validation as the primary task, invent new project policies, force a heavier architecture profile, or recommend repository-wide rewrites for local issues.
...
---

# Reviewing Frontend Architecture

## Purpose

Review a frontend change holistically against the definitive frontend engineering standard.

This skill answers:

```text
Is this frontend change architecturally healthy,
correctly layered,
appropriately stateful,
accessible,
testable,
performant,
secure,
and maintainable?
```

It is broader than `validating-frontend-architecture`.

Validation asks:

```text
Does code violate known boundaries?
```

This review asks:

```text
Are the chosen boundaries, ownership, state, UI behavior,
tests, performance, and safety healthy for this change?
```

The review must separate:

- mandatory violations;
- default-convention concerns;
- project-policy mismatches;
- accepted deviations;
- suggestions and optional improvements.

## Use When

- A frontend change is ready for architecture review.
- Objective boundary validation already exists or is straightforward.
- A PR needs severity-ranked architectural feedback.
- A change mixes UI, hooks, effects, adapters, composition, styling, and tests.
- A refactor may improve or worsen ownership.
- A feature appears overengineered or under-structured.
- Accessibility, performance, security, or testing concerns need architectural interpretation.
- A reviewer must distinguish blockers from suggestions.
- An accepted deviation needs explicit documentation.

## Do Not Use When

- The architecture profile is not selected.
- The task is only to validate imports and cycles.
- The task is only code style or formatting.
- The task is pure implementation.
- The task is backend-only.
- The task is to select a new framework, state library, or styling system.
- The review would be based only on personal preference.
- The request is a generic code review unrelated to the frontend standard.

## Inputs

- Definitive frontend engineering standard.
- Selected architecture profile.
- Frontend architecture validation record when available.
- Accepted specification and user stories.
- Vertical-slice plan.
- Component/hook/effect design records.
- Adapter and composition decisions.
- Styling profile.
- Accessibility design.
- Test-strategy record and test evidence.
- Current implementation/change set.
- Performance evidence when applicable.
- Security/privacy context.
- Repository-local `AGENTS.md`.
- Accepted deviations and decision register.

## Outputs

- Review status.
- Findings by severity.
- Rule classification and evidence.
- User/engineering impact.
- Minimal remediation.
- Suggestions separated from violations.
- Accepted deviations.
- Residual risks.
- Frontend architecture review record.

## Governing Rule Classification

Every finding must be classified as:

```text
MANDATORY_INVARIANT
DEFAULT_CONVENTION
PROJECT_POLICY
ACCEPTED_DEVIATION
SUGGESTION
NO_ISSUE
```

Map to standard language:

```text
MUST / MUST NOT
→ mandatory invariant

SHOULD / SHOULD NOT / PREFERRED / DEFAULT
→ default convention

documented repository choice
→ project policy
```

Never promote a SHOULD-level preference to blocker severity without concrete additional risk.

## Severity

Use:

```text
BLOCKER
HIGH
MEDIUM
LOW
ADVISORY
```

### BLOCKER

Use when the change:

- violates a critical mandatory invariant;
- exposes server secrets to clients;
- breaks essential accessibility with no equivalent path;
- creates unsafe stale/race behavior causing incorrect user state;
- introduces an architectural direction violation that invalidates the selected profile;
- creates a serious security/privacy defect;
- makes the accepted behavior fundamentally incorrect.

### HIGH

Use when the change:

- imports concrete adapters into hooks/components;
- embeds substantial business rules in presentation;
- bypasses feature ownership;
- introduces unsafe global mutable user/request state;
- uses inaccessible custom interaction for an important task;
- has missing critical error/recovery behavior;
- has a test gap likely to allow high-impact regression.

### MEDIUM

Use for:

- overcomplicated state;
- unjustified abstraction/shared ownership;
- styling-policy mismatch;
- weak error semantics;
- duplicated tests;
- performance concern with plausible user impact but insufficient evidence for blocker;
- incomplete automation of repeated architecture rules.

### LOW

Use for:

- localized maintainability issue;
- naming/ownership ambiguity;
- small convention deviation;
- narrow test readability concern.

### ADVISORY

Use for optional improvement with no current correctness or policy violation.

Severity must follow impact, not reviewer taste.

## Review Workflow

```text
accepted behavior and profile
→ inspect architecture-validation evidence
→ inspect ownership and dependency choices
→ inspect state/effects/data boundaries
→ inspect composition
→ inspect UI/accessibility/styling
→ inspect testing
→ inspect performance
→ inspect security/privacy
→ classify findings
→ separate violations from suggestions
→ recommend minimal remediation
```

## Readiness Gate

Use one:

```text
READY_TO_REVIEW_FRONTEND_ARCHITECTURE
READY_WITH_CONDITIONS
ARCHITECTURE_PROFILE_REQUIRED
ACCEPTED_BEHAVIOR_REQUIRED
VALIDATION_EVIDENCE_REQUIRED
ACCESSIBILITY_EVIDENCE_REQUIRED
PERFORMANCE_EVIDENCE_REQUIRED
SECURITY_CONTEXT_REQUIRED
BLOCKED
```

Do not invent missing requirements.

## Review Scope

Review only what the change can reasonably affect.

Possible scope:

```text
FEATURE
VERTICAL_SLICE
ROUTE
PACKAGE
APPLICATION
MIGRATION
PR_CHANGESET
```

Avoid expanding a feature PR into an application-wide redesign unless the change exposes a systemic blocker.

## Architecture Profile Fit

Review whether the selected profile is still proportionate.

### Under-structured

Potential signals:

- business rules in components;
- repeated provider mapping in UI;
- many components directly coordinating remote calls;
- cross-feature coupling;
- no clear owner for complex workflow.

### Over-structured

Potential signals:

- ceremonial Domain layer for UI-only behavior;
- one-file Use Cases with no orchestration value;
- ports with one permanent trivial implementation and no boundary value;
- shared abstractions with one consumer;
- wrapper components/hooks with no semantic value.

Do not escalate architecture solely because a larger profile looks “cleaner.”

Recommend profile change only when the current profile materially harms correctness, ownership, reuse, or changeability.

## Capability Ownership

Review whether the change belongs to a recognizable business capability.

Ask:

- Can a developer find it by product concept?
- Are files owned by one capability?
- Does `shared` hide feature ownership?
- Are cross-feature interactions intentional?
- Is public surface stable and narrow?

Do not require identical folder names across repositories.

## Dependency Direction

Use architecture validation evidence.

Review consequences, not just the import.

Examples:

```text
hook → concrete HTTP adapter
```

Concern:

- presentation now selects Infrastructure;
- testability and replaceability degrade;
- composition boundary is bypassed.

Minimal remediation:

- inject the semantic dependency from composition.

Do not repeat every validation finding verbatim when there is no additional review insight.

## Domain

Where Domain exists, review:

- business invariants are actually domain-relevant;
- entities/value objects are not DTO wrappers;
- Domain is framework/browser-independent;
- transformations are cohesive;
- no presentation concern leaked inward.

Also detect over-modeling:

- Value Object with no invariant;
- Domain Service that merely forwards data;
- business concept invented only to satisfy architecture ceremony.

Not every feature needs Domain.

## Application

Where Application exists, review:

- Use Cases represent user intentions;
- orchestration belongs here;
- DTOs are stable boundaries;
- external-service ports are meaningful;
- no React/CSS/concrete Infrastructure leaks in;
- Use Cases do not duplicate Domain rules.

Detect anemic ceremony:

```text
UseCase.execute()
→ repository.get()
→ returns unchanged response
```

This may still be valid when it protects a boundary, but should not be assumed valuable automatically.

## Infrastructure

Review:

- transport/storage mapping is explicit;
- provider details remain outward;
- errors remain distinguishable;
- cancellation/race support is appropriate;
- adapters do not own business rules;
- composition/lifecycle is safe.

Flag:

- provider payload passed directly to UI;
- every error mapped to `undefined`;
- singleton adapter capturing user token;
- retry policy invented locally.

## Presentation

Review components and hooks for responsibility.

Components should answer:

```text
What should the user see?
How can the user interact?
```

Hooks should answer:

```text
How does this UI behavior work?
```

Review for:

- business-rule leakage;
- direct repositories/fetch;
- god components;
- god hooks;
- duplicated state;
- hidden side effects;
- invalid state combinations;
- overly generic catch-all props.

Do not use line count as a hard violation.

## State Model

Review whether state represents valid UI states.

Look for:

- contradictory booleans;
- duplicated derived state;
- server data copied unnecessarily into local state;
- stale closures;
- race-prone transitions;
- state split that breaks atomic updates;
- reducer ceremony for independent fields;
- one giant object for unrelated state.

Prefer the simplest state model that preserves valid transitions.

Do not impose one `useState`, one object, or `useReducer` universally.

## Server State Versus Local State

Review ownership.

Server state belongs to the approved server-state strategy when applicable.

Local component/hook state should represent:

- input;
- selection;
- ephemeral interaction;
- local workflow state.

Flag:

- recreating caching/dedup/retry in custom hooks;
- duplicating server data in local state without need;
- stale manual synchronization between cache and local state.

Do not require a server-state library where simple fetch/load behavior is already accepted.

## Effects

Review Effects for necessity.

Effects are appropriate for synchronization with external systems.

Flag:

- render derivation moved into Effect;
- user action indirectly triggered through Effect;
- suppressed dependency warnings;
- missing cleanup;
- stale closure;
- duplicated external initialization;
- Effect used as general orchestration engine.

Also flag unnecessary “no Effect ever” refactors that make synchronization less explicit.

## Async Races and Cancellation

Review:

- obsolete requests;
- latest-wins behavior;
- duplicate submissions;
- unmount cleanup;
- route/resource identity changes;
- optimistic concurrency;
- cancellation semantics.

User-visible stale data or wrong-result overwrites are correctness concerns, not optional polish.

## Components

Review:

- responsibility;
- typed props;
- rendering branches;
- semantic HTML;
- presentation/container separation where useful;
- over-fragmentation;
- hidden dependency composition;
- catch-all props.

Do not split a coherent component merely to reduce line count.

## Custom Hooks

Review:

- reusable behavior;
- public API stability;
- named commands;
- dependency injection;
- correct state granularity;
- no second Application layer;
- no concrete adapters/global Factory;
- race/cancellation handling.

A hook that simply renames one library field may be unnecessary ceremony.

## Composition

Review:

- dependencies created at outer boundary;
- safe shared lifecycle;
- per-user/request state not global;
- no Service Locator leakage;
- server/client roots separated when needed;
- test overrides possible.

Flag:

```text
first-user token captured in module singleton
global query cache shared across SSR users
component constructs HttpClient
hook calls getDependencies()
```

## Routing

Routes are outer composition boundaries.

Review:

- route-level data/composition ownership;
- URL state versus local state;
- route error handling;
- server/client hydration;
- nested route ownership;
- navigation semantics.

Avoid moving feature logic into routing solely because the framework makes it convenient.

## Styling Architecture

Review against the selected styling profile.

Check:

- primary strategy respected;
- competing systems have explicit boundary;
- token source remains authoritative;
- variants are explicit;
- global styles remain bounded;
- hardcoded values do not bypass available semantic tokens;
- inline runtime values are genuine exceptions;
- `!important` is scoped and documented.

Do not ban Tailwind, CSS Modules, inline styles, or `!important` universally.

## Shared UI and Design System

Review:

- project primitives before raw vendor imports when required;
- wrappers preserve accessibility/vendor behavior;
- shared UI remains presentation-focused;
- no business rules inside primitives;
- feature-specific components are not promoted based only on generic appearance.

Shared UI ownership requires stable semantics and real consumers.

## Accessibility

Accessibility is functional correctness.

Review:

- semantic HTML;
- accessible names;
- keyboard path;
- visible focus;
- disabled/invalid semantics;
- color-independent meaning;
- contrast;
- zoom/reflow;
- reduced motion;
- complex-widget primitive choice;
- status messages;
- focus behavior.

Use the accepted accessibility target.

Do not claim compliance from automated checks alone.

A critical inaccessible path may be BLOCKER or HIGH depending on task impact and equivalent alternatives.

## Error Handling

Review whether UI distinguishes:

- validation;
- authorization;
- not found;
- network;
- server;
- cancellation;
- semantic business rejection.

Flag:

- raw technical errors;
- all failures shown as generic “Something went wrong” when recovery differs;
- user input lost unnecessarily;
- retry shown for non-retryable error;
- forbidden shown as empty data.

## Testing Strategy

Review whether tests match behavior and boundaries.

Look for:

- Domain rules at Domain level;
- Use Cases through InMemory ports;
- adapters through realistic boundaries;
- hook behavior through public state/commands;
- component tests through user semantics;
- visual tests for visual risk;
- small E2E critical journey set;
- accessibility evidence beyond automation.

Flag:

- all-E2E;
- every branch duplicated at every layer;
- private implementation assertions;
- mocks replacing meaningful boundaries;
- flaky retries masking instability.

## Test Quality

Review:

- test names describe behavior;
- async waits are observable;
- data is isolated;
- caches/providers reset;
- global mutable state absent;
- selectors are semantic;
- regressions target the smallest reliable boundary.

Do not treat coverage percentage as proof of quality.

## React Compiler and Manual Memoization

Before recommending:

```text
useMemo
useCallback
React.memo
```

determine whether React Compiler is enabled for the affected code.

Use:

```text
REACT_COMPILER_ENABLED
REACT_COMPILER_PARTIAL
REACT_COMPILER_DISABLED
REACT_COMPILER_STATUS_UNKNOWN
```

### When React Compiler Is Enabled

React Compiler performs automatic build-time optimization and handles memoization for React components and hooks.

For new code:

- prefer compiler-managed memoization;
- do not recommend `useMemo`, `useCallback`, or `React.memo` as routine hygiene;
- require a concrete semantic-identity requirement or measured performance need before recommending manual memoization;
- prefer simpler code when the compiler already provides equivalent optimization.

Manual memoization may still be appropriate as an escape hatch when precise memoization control is required.

A representative case is when a memoized value or callback must remain stable because it is an Effect dependency and semantic identity matters.

Do not recommend manual memoization merely because:

```text
a function is recreated on render
an object literal is recreated
a child component exists
a callback is passed as a prop
```

Those facts alone are not sufficient when React Compiler is active.

### When React Compiler Is Disabled

Manual memoization is still not the default recommendation.

Require evidence such as:

- measured expensive calculation;
- measured avoidable render cost;
- meaningful child-render prevention;
- stable identity required by an external integration;
- semantic Effect dependency stability;
- accepted performance target currently missed.

Prefer profiling before adding complexity.

### Partial or Incremental Compiler Adoption

React Compiler can be adopted incrementally.

Do not assume the entire repository has one compiler state.

Determine whether the affected component/hook is inside the compiled scope.

For mixed repositories:

```text
compiled code
→ compiler-first review policy

non-compiled code
→ evidence-based manual memoization policy
```

Do not extrapolate from package-level configuration without checking affected code scope.

### Existing Manual Memoization

When compiler adoption occurs in existing code:

- do not remove `useMemo`, `useCallback`, or `React.memo` mechanically;
- recognize that removing existing memoization can change compiler output;
- require tests and/or profiling before simplification;
- preserve behavior and integration identity;
- remove memoization only when the change is demonstrated safe and simpler.

Do not create cleanup churn merely because the compiler is enabled.

### Compiler Scope

React Compiler focuses primarily on:

- avoiding cascading re-renders;
- memoizing expensive calculations used inside React components and hooks.

It does not imply that every expensive function everywhere in the application is globally memoized.

For expensive reusable computation outside React components/hooks:

- profile first;
- consider an appropriate non-React caching/memoization strategy only when evidence justifies it.

### Compiler Is Not a Correctness Tool

Never use React Compiler, `useMemo`, `useCallback`, or `React.memo` to repair:

- stale state;
- incorrect Effect dependencies;
- race conditions;
- invalid state transitions;
- broken ownership;
- side-effect ordering.

Fix correctness at its actual boundary.

### Review Decision

Use:

```text
NO_MANUAL_MEMOIZATION_NEEDED
MANUAL_MEMOIZATION_SEMANTICALLY_REQUIRED
MANUAL_MEMOIZATION_PERFORMANCE_JUSTIFIED
EXISTING_MEMOIZATION_PRESERVE
EXISTING_MEMOIZATION_REMOVAL_REQUIRES_EVIDENCE
REACT_COMPILER_SCOPE_UNKNOWN
PERFORMANCE_EVIDENCE_REQUIRED
```

A review finding about memoization must record:

- React Compiler status;
- affected compilation scope;
- semantic identity requirement, if any;
- performance evidence, if any;
- whether memoization already exists;
- risk of adding/removing it;
- smallest justified action.

## Performance

Performance review MUST be evidence-driven.

Ask for evidence when claiming a performance issue.

Review:

- Core Web Vitals where relevant;
- route loading;
- bundle growth;
- network waterfall;
- rendering frequency;
- long tasks;
- memory;
- interaction latency;
- duplicate requests;
- large collections;
- third-party dependency cost.

Prefer architectural fixes:

```text
reduce work
improve data boundaries
split route/feature
remove dependency
virtualize
cache at correct layer
avoid duplicate requests
```

Do not recommend `useMemo`/`useCallback` everywhere without evidence.

Before any manual memoization recommendation, check React Compiler status for the affected code. When Compiler is enabled, prefer compiler-managed memoization for new code and require semantic identity constraints or measured performance evidence for manual memoization. When Compiler is disabled, manual memoization still requires evidence. Existing memoization should not be removed mechanically during Compiler adoption.

Classify speculative performance concerns as ADVISORY or `EVIDENCE_REQUIRED`.

## Bundle and Dependency Review

Review new dependencies when they materially affect:

- bundle size;
- runtime initialization;
- SSR/client boundary;
- duplication;
- security;
- accessibility;
- maintenance.

A large library is not automatically wrong.

Require evidence and available repository constraints.

## Security

Review frontend security/privacy assumptions.

Mandatory concerns:

- no secrets in client bundle;
- no provider credentials;
- safe untrusted HTML rendering;
- no sensitive token storage against accepted policy;
- no private stack traces;
- frontend authorization not treated as server authorization;
- analytics follows consent/privacy requirements.

Do not provide false confidence from UI-only authorization checks.

## Privacy

Review:

- telemetry payloads;
- identifiers;
- PII;
- browser storage;
- logs;
- third-party scripts;
- consent.

Use accepted organizational policy.

Do not invent compliance requirements not present in the context.

## Naming and Maintainability

Review names when they affect discoverability and responsibility.

Prefer product language.

Flag vague catch-all concepts such as:

```text
Helper
Utils
Manager
Common
Misc
```

when they hide ownership.

Do not create naming findings for harmless stylistic preference.

## Comments

Comments should explain why, constraints, or trade-offs.

Flag:

- commented-out code;
- stale TODOs with no owner/trigger;
- comments narrating obvious code only when they create noise.

This is normally LOW or ADVISORY.

## Shared Abstraction Review

Before approving a shared abstraction, ask:

- How many real consumers?
- Are semantics stable?
- Is ownership clear?
- Is central evolution safe?
- Is the abstraction business-neutral or a stable contract?

Flag speculative generalization.

YAGNI applies to architecture.

## SOLID Interpretation

Use SOLID as reasoning, not ceremony.

### SRP

A component/hook/module should have one coherent reason to change.

### OCP

Stable variation boundaries may use explicit strategies/ports when real variation exists.

### LSP

Alternative implementations of a port must preserve semantic behavior.

### ISP

Prefer narrow interfaces over dependency bags.

### DIP

Inner policy should not depend on concrete outer implementation.

Do not manufacture interfaces merely to “be SOLID.”

## DRY

Review duplication semantically.

Do not deduplicate two blocks merely because they look similar.

Extract when:

- semantics are the same;
- changes should occur together;
- ownership is stable.

Duplicated appearance with different business meaning may correctly remain separate.

## YAGNI

Flag:

- unused abstractions;
- speculative extension points;
- generic plugin systems for one use case;
- shared components with one consumer and no stable contract;
- premature package extraction.

Architecture should support known change pressure, not imagined universality.

## POLA

Prefer least-surprising APIs and behavior.

Examples:

- `retry()` retries;
- `cancel()` does not surface as generic failure;
- disabled action behaves consistently;
- hook command names match product intention;
- public exports are stable.

## Brownfield Context

Review changes relative to the existing repository.

A local improvement may be good even if the entire repository is not ideal.

Prefer:

```text
leave code better
without widening scope unnecessarily
```

Accepted legacy exceptions should not be re-litigated in every PR unless the change touches them materially.

## Migration Review

For migration changes, review:

- target direction;
- change-local value;
- compatibility period;
- mixed-state boundaries;
- rollback;
- test safety;
- exit trigger.

Do not require full migration before accepting an incremental improvement.

## Accepted Deviations

A deviation is valid when:

- explicit;
- higher-priority requirement justifies it;
- scope is clear;
- impact is understood;
- owner exists;
- expiration/removal trigger is recorded when temporary.

Use:

```text
ACCEPTED_PERMANENT_DEVIATION
ACCEPTED_TEMPORARY_DEVIATION
MIGRATION_DEVIATION
THIRD_PARTY_DEVIATION
DEVIATION_REQUIRES_APPROVAL
UNJUSTIFIED_DEVIATION
```

Do not report an accepted deviation as a violation unless its conditions are no longer true.

## Findings Format

Every finding should include:

```text
severity
classification
rule evidence
location
problem
impact
minimal remediation
```

Example:

```text
HIGH — MANDATORY_INVARIANT

Rule:
Components and hooks MUST NOT import concrete repository adapters.

Evidence:
usePromotion.ts imports HttpPromotionRepository.

Impact:
Presentation chooses Infrastructure directly and bypasses composition.

Minimal remediation:
Inject the accepted semantic dependency from the feature composition boundary.
```

## Suggestion Format

Suggestions MUST be clearly separated.

Example:

```text
ADVISORY — SUGGESTION

Consider renaming `PromotionUtils` to a product-specific name
if this module continues to own promotion-only mapping.
```

Do not place optional suggestions in the blocker list.

## Minimal Remediation

Prefer the smallest change that restores correctness.

Examples:

```text
god component
→ extract one meaningful interaction region or hook

direct adapter import
→ inject semantic dependency

derived state Effect
→ derive during render

shared feature helper
→ move back to feature

raw vendor primitive
→ use approved project wrapper

all-E2E branch matrix
→ move branch evidence to lower boundaries
```

Avoid “rewrite using clean architecture” as a finding.

## Review Status

Use:

```text
APPROVE
APPROVE_WITH_ADVISORIES
CHANGES_REQUESTED
BLOCKED_PENDING_DECISION
BLOCKED_PENDING_EVIDENCE
```

### APPROVE

No mandatory or material concerns.

### APPROVE_WITH_ADVISORIES

No blocking concern; optional improvements remain.

### CHANGES_REQUESTED

One or more findings require remediation before merge.

### BLOCKED_PENDING_DECISION

A missing project/product decision prevents safe review.

### BLOCKED_PENDING_EVIDENCE

A claim requires performance/security/accessibility evidence not currently available.

## Definition of Done Review

Check applicable categories:

### Architecture

- recognizable capability;
- inward dependency direction;
- no feature boundary bypass;
- selected profile respected;
- shared abstractions justified.

### Behavior

- accepted behavior implemented;
- loading/empty/success/error/permission states considered;
- races/cancellation safe;
- business rules in correct layer.

### UI

- semantics/names;
- keyboard;
- focus;
- responsive;
- theme;
- design-system conventions.

### Data

- explicit mapping;
- runtime validation when needed;
- intentional error translation;
- no provider leakage.

### Testing

- relevant boundary tests;
- correct doubles;
- critical regressions.

### Quality

- lint/type/tests/build;
- acceptable performance;
- security/privacy;
- documentation/rules updated when architecture changes.

Do not require non-applicable DoD items.

## Output

Use `assets/frontend-architecture-review-record.md`.

## Completion Criteria

- [ ] Review scope and selected profile are explicit.
- [ ] Architecture validation evidence is incorporated where available.
- [ ] Mandatory invariants are separated from conventions and suggestions.
- [ ] Severity follows impact rather than preference.
- [ ] Profile fit is reviewed without forcing heavier architecture.
- [ ] Domain/Application/Infrastructure/Presentation responsibilities are reviewed where applicable.
- [ ] State, Effects, races, and cancellation are reviewed.
- [ ] Composition and lifecycle are reviewed.
- [ ] Styling and shared UI are reviewed against selected project policy.
- [ ] Accessibility is treated as functional correctness.
- [ ] Error semantics and recovery are reviewed.
- [ ] Tests are reviewed against boundary strategy.
- [ ] Performance findings are evidence-driven.
- [ ] React Compiler status is checked before recommending manual memoization.
- [ ] Compiler-enabled code does not receive routine `useMemo`/`useCallback`/`React.memo` recommendations.
- [ ] Existing manual memoization is not removed mechanically during Compiler adoption.
- [ ] Security/privacy mandatory rules are reviewed.
- [ ] Shared abstractions and YAGNI are considered.
- [ ] Brownfield and migration context are respected.
- [ ] Accepted deviations are not misreported.
- [ ] Every finding contains evidence, impact, and minimal remediation.
- [ ] Suggestions are not mixed into blocker findings.
- [ ] Definition of Done is reviewed only where applicable.
- [ ] No new project policy, framework, library, or repository-wide redesign is invented.
- [ ] Final review status is explicit.

## References

- Read `references/react-compiler-and-manual-memoization-review.md` for modern React performance guidance.
