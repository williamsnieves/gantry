---
name: selecting-frontend-styling-profile
description: Identifies and documents the approved frontend styling profile for a project, application, package, capability, or feature. Use when deciding whether UI should use CSS Modules, Tailwind, CSS-in-JS, vanilla CSS, a company design system, shadcn/ui, headless primitives, or a hybrid with explicit ownership boundaries. Determine token source, primitive ownership, variant strategy, theming, responsive approach, accessibility baseline, global-style limits, runtime-value exceptions, and migration policy. Preserve repository-local conventions and choose the smallest coherent strategy. Do not implement CSS, introduce or ban a styling system universally, mix competing systems without a documented boundary, promote feature UI to shared based only on appearance, wrap accessible primitives in ways that break behavior, or invent design tokens.
---

# Selecting Frontend Styling Profile

## Purpose

Identify and document the styling strategy that applies to one project, application, package, capability, or feature.

The profile must define:

- primary styling strategy;
- component primitive ownership;
- design-token source;
- variant strategy;
- theming strategy;
- responsive strategy;
- accessibility baseline;
- global-style policy;
- runtime-value exceptions;
- migration and exception policy.

Supported strategies may include:

```text
CSS Modules
Tailwind CSS
CSS-in-JS
vanilla CSS
company design system
shadcn/ui
Radix UI
Base UI
React Aria
native HTML primitives
hybrid strategy with explicit boundaries
```

No universal rule prohibits Tailwind or requires CSS Modules.

The goal is coherence, not ideology.

## Roadmap Purpose

This skill must:

- identify the project's approved styling strategy;
- decide CSS Modules, Tailwind, design system, headless primitives, or hybrid boundaries;
- document tokens, theming, and exception policy.

Outputs:

- styling profile;
- primitive ownership;
- token source;
- variant strategy;
- responsive approach;
- accessibility baseline.

It must not:

- introduce a new styling system without approval;
- ban Tailwind or force it universally.

## Use When

- A frontend change needs a confirmed styling path.
- The repository contains more than one styling approach.
- A feature request casually assumes Tailwind, CSS Modules, or another system.
- Design-system components and feature-local styles overlap.
- Headless/vendor primitives require ownership rules.
- Tokens, themes, variants, responsive behavior, or exceptions are undocumented.
- A migration between styling systems is proposed.
- A package or monorepo needs app versus shared-UI boundaries.
- `applying-frontend-engineering-standard` found a mixed or unresolved styling profile.
- A feature should choose between shared primitives and local composition.

## Do Not Use When

- The styling profile is already accepted and only implementation remains.
- The task is to write CSS Modules or Tailwind classes.
- The task is only component behavior or accessibility design.
- A new styling library must be selected through a broader architecture decision.
- Product/design requirements are too incomplete to identify tokens, variants, or responsive behavior.
- The task is backend-only.
- The user asks for a universal “best CSS technology.”

## Inputs

- Accepted frontend change or capability.
- Frontend standard application record.
- Architecture-profile decision.
- Component and vertical-slice designs.
- Repository-local `AGENTS.md`.
- Existing CSS, Tailwind, CSS-in-JS, vanilla CSS, or design-system setup.
- Theme and token definitions.
- Component primitive libraries.
- Package/public-export structure.
- Accessibility baseline.
- Responsive and browser-support policy.
- Existing exceptions and migration decisions.
- Build, lint, visual-regression, and test tooling.

## Outputs

- Styling-profile classification.
- Primary strategy.
- Hybrid boundaries where applicable.
- Primitive ownership.
- Token source and semantic-token rules.
- Variant strategy.
- Theming strategy.
- Responsive approach.
- Accessibility baseline.
- Global-style and exception policy.
- Migration conditions.
- Styling-profile record.

## Core Workflow

```text
inspect repository and accepted UI behavior
→ identify active styling systems
→ classify ownership and consumers
→ select primary strategy
→ define explicit hybrid boundaries if required
→ define tokens, variants, themes, responsive behavior, accessibility
→ define exceptions and migration policy
→ validate coherence
```

## Readiness Gate

Use one:

```text
READY_TO_SELECT_STYLING_PROFILE
READY_WITH_CONDITIONS
REPOSITORY_STYLE_EVIDENCE_REQUIRED
DESIGN_SYSTEM_OWNERSHIP_REQUIRED
TOKEN_SOURCE_REQUIRED
THEME_POLICY_REQUIRED
RESPONSIVE_POLICY_REQUIRED
ACCESSIBILITY_BASELINE_REQUIRED
MIGRATION_DECISION_REQUIRED
BLOCKED
```

Stop when:

- current styling systems cannot be identified;
- design-system ownership is disputed;
- token sources conflict with no accepted precedence;
- the request assumes a new system without approval;
- accessibility or theming requirements materially affect the profile but remain undefined.

## Scope

Classify one of:

```text
WORKSPACE
APPLICATION
PACKAGE
CAPABILITY
FEATURE
COMPONENT_FAMILY
```

A feature-level profile must not silently redesign the workspace.

A package-level profile must define its consumers and public styling contract.

## Evidence Order

Use evidence in this order:

1. accepted product/design behavior;
2. repository-local `AGENTS.md`;
3. definitive frontend standard;
4. design-system and token documentation;
5. build and lint configuration;
6. current shared primitives;
7. current feature conventions;
8. existing code;
9. personal preference.

Existing code is evidence, not automatically policy.

## Profile Classification

Use exactly one primary classification:

```text
CSS_MODULES_PROFILE
TAILWIND_PROFILE
CSS_IN_JS_PROFILE
VANILLA_CSS_PROFILE
DESIGN_SYSTEM_PROFILE
HYBRID_PROFILE
PROFILE_DECISION_REQUIRED
```

A profile may include supporting tools without becoming hybrid.

Example:

```text
primary: CSS Modules
supporting: company design-system components
```

This is not necessarily a competing hybrid.

## CSS Modules Profile

Use when the project standardizes:

- component-scoped `.module.css` or equivalent;
- token variables or imported token definitions;
- composition or shared utility modules;
- predictable selector scoping;
- explicit responsive and theme selectors.

Define:

- module naming;
- class composition;
- global escape policy;
- selector depth;
- token access;
- runtime inline-style exceptions;
- variant composition.

Do not use deep selectors to reach through unrelated component internals.

## Tailwind Profile

Use when the project standardizes:

- utility-first composition;
- theme-backed tokens;
- approved class-merging or variant tooling;
- responsive and state variants;
- dark/theme policy;
- project primitives.

Define:

- theme token source;
- arbitrary-value policy;
- class-order/readability policy;
- repeated-class extraction policy;
- variant composition;
- design-system integration;
- class-conflict handling.

Do not ban arbitrary values universally, but require justification when a token exists.

Do not extract every short class list into a component.

## CSS-in-JS Profile

Use when the repository accepts a specific runtime or compile-time solution.

Define:

- server-rendering behavior;
- style extraction;
- theme provider;
- runtime cost;
- prop filtering;
- token access;
- variants;
- cache/provider lifecycle;
- server/client boundary.

Do not add another CSS-in-JS library.

Do not leak styling props to the DOM.

## Vanilla CSS Profile

Use when the project intentionally uses:

- global or feature-scoped CSS;
- cascade layers;
- naming conventions;
- tokens/custom properties;
- explicit ownership.

Define selector and global-boundary discipline.

Vanilla CSS does not mean unrestricted global selectors.

## Design-System Profile

Use when product UI primarily consumes a governed component and token system.

Define:

- design-system owner;
- public primitive/component APIs;
- allowed feature-local styling;
- token source;
- variant extension;
- composition versus modification;
- versioning;
- accessibility contract;
- escape-hatch policy.

Feature code should consume project primitives before raw vendor primitives when project policy requires centralized consistency.

Business logic must not live in shared UI primitives.

## Hybrid Profile

A hybrid is valid only when boundaries are explicit.

Examples:

```text
design system for shared primitives
+ CSS Modules for feature layout

Tailwind for application UI
+ CSS Modules only for third-party widget boundary

company tokens
+ headless primitives
+ feature-local Tailwind composition
```

Document:

- which layer owns each system;
- where each system may appear;
- which system wins on conflicts;
- how tokens remain consistent;
- how migration works;
- which combinations are forbidden.

Do not call an accidental mixture a strategy.

## Competing-System Check

A project should avoid mixing competing systems without a documented boundary.

Potential competition:

- Tailwind and CSS Modules both used for the same component role;
- two unrelated token sources;
- two theme providers;
- local hardcoded variants competing with design-system variants;
- raw vendor primitives and wrapped project primitives used inconsistently.

Classify:

```text
COHERENT_SUPPORTING_TOOLS
EXPLICIT_HYBRID
ACCIDENTAL_MIXTURE
MIGRATION_IN_PROGRESS
CONFLICT_REQUIRES_DECISION
```

## Primitive Ownership

Classify primitive ownership:

```text
NATIVE_HTML_FIRST
PROJECT_SHARED_UI
COMPANY_DESIGN_SYSTEM
HEADLESS_VENDOR_WRAPPED
HEADLESS_VENDOR_DIRECT_ALLOWED
FEATURE_LOCAL
PACKAGE_PUBLIC
```

Define:

- allowed import path;
- who owns accessibility;
- who owns styling;
- who owns variants;
- who owns vendor upgrades;
- who owns breaking changes.

Do not allow feature code to bypass project wrappers when repository policy centralizes vendor use.

## Native HTML

Use native HTML for semantics where it satisfies the behavior.

A styling profile must not force a custom primitive when native controls are sufficient.

Examples:

- `button`;
- `a`;
- `input`;
- `select`;
- headings;
- lists;
- tables.

ARIA and styling must preserve native behavior.

## Headless Primitives

When using Radix UI, Base UI, React Aria, or similar:

- preserve vendor accessibility behavior;
- preserve keyboard interactions;
- preserve focus management;
- preserve state attributes;
- wrap only when project consistency requires it;
- avoid hiding important vendor extension points;
- test wrapper behavior after upgrades.

Do not convert a feature-specific component into shared UI merely because it wraps a headless primitive.

## shadcn/ui

Treat shadcn-style copied components according to repository ownership.

Define:

- whether components are project-owned source;
- update policy;
- token/theme integration;
- allowed local modification;
- package versus app ownership;
- accessibility regression responsibility.

Do not assume vendor-managed upgrade behavior when code is copied into the repository.

## Token Source

Select one authoritative token source per applicable scope.

Use:

```text
COMPANY_TOKEN_PACKAGE
DESIGN_SYSTEM_TOKENS
CSS_CUSTOM_PROPERTIES
TAILWIND_THEME
CSS_IN_JS_THEME
APPLICATION_TOKEN_LAYER
TOKEN_SOURCE_DECISION_REQUIRED
```

Supporting representations may be generated from one source.

Do not maintain conflicting hardcoded token sets manually.

## Semantic Tokens

Repeated visual decisions should use semantic tokens.

Categories:

- color;
- spacing;
- typography;
- radius;
- border;
- shadow;
- motion;
- z-index;
- breakpoints;
- size.

Prefer semantic naming:

```text
color.text.primary
color.surface.elevated
color.action.danger
space.4
radius.medium
```

Avoid component-independent raw-value names as the only public contract when semantic meaning exists.

## Hardcoded Values

Hardcoded values may be acceptable when:

- the value is genuinely unique;
- no semantic token exists;
- it is a runtime measurement;
- it is a third-party integration boundary;
- an accepted exception exists.

Do not hardcode a color, spacing, radius, or shadow when an approved semantic token already exists.

## Runtime Values and Inline Styles

Inline styles are acceptable for genuine runtime values.

Examples:

- measured position;
- progress percentage;
- dynamic transform;
- user-supplied safe dimension;
- canvas/widget host sizing.

Define:

- allowed properties;
- sanitization;
- units;
- fallback;
- SSR/hydration behavior;
- whether a CSS custom property is preferable.

Do not ban inline styles universally.

Do not use inline styles as an undocumented second styling system.

## Variant Strategy

Select:

```text
EXPLICIT_COMPONENT_PROPS
DISCRIMINATED_VARIANT_PROPS
CSS_MODULE_COMPOSITION
UTILITY_VARIANT_HELPER
DESIGN_SYSTEM_VARIANTS
RECIPE_SYSTEM
DATA_ATTRIBUTE_STYLING
VARIANT_DECISION_REQUIRED
```

Variants must be explicit and valid.

Avoid contradictory boolean combinations such as:

```text
primary
secondary
danger
```

all being independently true.

Prefer:

```text
variant: "primary" | "secondary" | "danger"
```

when one choice is intended.

## State Styling

Define styling for:

- hover;
- active;
- focus-visible;
- disabled;
- `aria-disabled`;
- invalid;
- busy/pending;
- selected;
- expanded;
- loading;
- error;
- success;
- reduced motion;
- high contrast where supported.

Do not communicate meaning using color alone.

## Theming

Define:

```text
SINGLE_THEME
LIGHT_DARK
MULTI_BRAND
USER_SELECTABLE
SYSTEM_PREFERENCE
TENANT_THEME
THEME_POLICY_REQUIRED
```

Document:

- theme source;
- provider or attribute/class mechanism;
- server-rendering behavior;
- persistence;
- hydration;
- token overrides;
- component compatibility;
- contrast validation;
- theme-switch testing.

Do not introduce a second theme provider casually.

## Theme Ownership

Theme should normally be owned at:

```text
APPLICATION_ROOT
DESIGN_SYSTEM_PROVIDER
PACKAGE_CONSUMER
SERVER_DOCUMENT_BOUNDARY
```

Feature components consume theme tokens rather than choose global theme.

A tenant-specific theme requires trusted configuration and safe scoping.

## Responsive Strategy

Select based on the problem:

- Flexbox for one-dimensional distribution;
- Grid for two-dimensional tracks;
- container queries for component-context responsiveness;
- viewport queries for page-level responsiveness.

The universal rule “always use Flexbox” is rejected.

Define:

```text
VIEWPORT_BREAKPOINTS
CONTAINER_QUERIES
FLUID_LAYOUT
HYBRID_RESPONSIVE
RESPONSIVE_POLICY_REQUIRED
```

## Responsive Requirements

Layouts must:

- avoid unintended overflow;
- support content wrapping;
- support supported viewport sizes;
- preserve essential actions;
- tolerate translation expansion;
- support zoom and text scaling;
- use logical properties where internationalization matters.

Fixed dimensions require justification.

## Breakpoints

Use approved breakpoint tokens.

Do not create component-specific magic breakpoints without evidence.

A component may use container queries when its behavior depends on available container width rather than viewport size.

## Layout Primitive

Choose the primitive that matches the relationship.

Use:

- Flexbox for one axis;
- Grid for rows and columns;
- normal flow for document content;
- positioning for overlays and genuine positioned UI;
- container queries for reusable component adaptation.

Do not use absolute positioning as the default layout strategy.

## Global Styles

Global styles should be limited to:

- reset or normalization;
- tokens;
- themes;
- base typography;
- document-level behavior;
- approved utilities;
- third-party boundaries.

Classify:

```text
GLOBAL_ALLOWED
FEATURE_SCOPED_REQUIRED
THIRD_PARTY_GLOBAL_EXCEPTION
GLOBAL_EXCEPTION_REQUIRES_DECISION
```

Do not place feature-specific selectors in global CSS without an accepted reason.

## Selector Discipline

Avoid:

- brittle descendant chains;
- element selectors tied to incidental markup;
- specificity escalation;
- deep vendor-internal selectors;
- global feature selectors;
- unnecessary `!important`.

Prefer:

- scoped classes;
- explicit state/data attributes;
- project variants;
- supported primitive APIs;
- semantic selectors where stable.

## `!important`

`!important` should be exceptional.

Acceptable cases may include:

- third-party boundary override;
- forced-colors/accessibility workaround;
- browser/user-agent conflict;
- legacy compatibility with an exit condition.

Document:

- exact selector;
- reason;
- risk;
- owner;
- removal trigger.

Do not ban it universally, but do not normalize it.

## Specificity Policy

Define:

- selector depth;
- nesting limits if project policy uses them;
- cascade layers if used;
- global versus module precedence;
- third-party override location;
- variant/state precedence.

Do not solve architecture problems by adding more specificity.

## Accessibility Baseline

The project must define an accessibility target.

Recommended default:

```text
WCAG 2.2 AA
```

unless another organizational baseline is approved.

The styling profile must support:

- semantic HTML;
- keyboard interaction;
- visible focus;
- disabled and invalid states;
- contrast;
- non-color-only meaning;
- text scaling;
- zoom/reflow;
- reduced motion;
- forced colors/high contrast where applicable;
- touch target needs.

The styling system is not compliant merely because a component library claims accessibility.

## Motion

Define:

- motion tokens;
- durations/easing;
- reduced-motion behavior;
- essential versus decorative motion;
- transition ownership.

Do not remove essential state feedback under reduced motion; provide a non-motion equivalent.

## Typography

Define:

- token source;
- font families;
- scale;
- line height;
- weight;
- responsive behavior;
- localization and script support;
- fallback;
- loading strategy if relevant.

No universal “maximum two fonts” rule applies, but complexity requires product and performance justification.

## Z-Index and Overlays

Use a documented z-index scale or overlay system.

Do not invent arbitrary high z-index values per feature.

Shared dialogs, popovers, tooltips, and menus should follow primitive/design-system layering rules.

## Component Ownership

Classify styled UI as:

```text
FEATURE_LOCAL
CAPABILITY_SHARED
APPLICATION_SHARED
DESIGN_SYSTEM
PACKAGE_PUBLIC
THIRD_PARTY_BOUNDARY
```

A visually generic card remains feature-local if its semantics and behavior are feature-specific.

Promotion requires real consumers, stable semantics, ownership, accessibility contract, and change policy.

## Shared UI Boundaries

Shared UI may wrap:

- native elements;
- Radix UI;
- Base UI;
- React Aria;
- shadcn/ui;
- company design systems.

Wrappers must preserve:

- accessibility;
- vendor behavior;
- ref/slot behavior where required;
- state attributes;
- keyboard and focus contracts;
- theming;
- extension points.

Business logic must not enter shared primitives.

## Feature Extensions

Define whether feature code may:

- pass class names;
- pass style props;
- use slots;
- wrap primitives;
- create local variants;
- override tokens;
- add data attributes.

Escape hatches should be explicit and bounded.

Do not expose arbitrary styling escape hatches that undermine the profile.

## Public Package Styling

For Profile C packages define:

- whether styles ship with package;
- token peer dependency;
- theme contract;
- class-name stability;
- CSS side effects;
- consumer override policy;
- SSR ordering;
- versioning;
- tree shaking;
- style isolation.

Do not expose internal class names as a public contract unless intentionally supported.

## Exception Policy

Every exception should record:

- rule;
- exact scope;
- reason;
- owner;
- risk;
- validation;
- expiry/removal trigger when temporary.

Use:

```text
APPROVED_PERMANENT_EXCEPTION
APPROVED_TEMPORARY_EXCEPTION
MIGRATION_EXCEPTION
THIRD_PARTY_EXCEPTION
ACCESSIBILITY_EXCEPTION_REQUIRES_REVIEW
UNAPPROVED_EXCEPTION
```

Do not let “just this component” become an undocumented second strategy.

## Migration

For a migration define:

```text
CURRENT_PROFILE
TARGET_PROFILE
MIGRATION_BOUNDARY
COMPATIBILITY_PERIOD
NEW_CODE_POLICY
REMOVAL_TRIGGER
```

Prefer:

- change-local migration;
- capability-by-capability migration;
- shared-token alignment first;
- wrapper or adapter boundaries;
- visual-regression evidence.

Avoid:

- repository-wide rewrites without product value;
- mixing old and new systems inside one component without a plan;
- changing styling, component behavior, and design-system ownership simultaneously when not necessary.

## Tailwind Migration Cases

When moving toward Tailwind:

- map tokens first;
- define primitive ownership;
- define class-merge/variant policy;
- avoid arbitrary-value proliferation;
- preserve theme and accessibility;
- define whether CSS Modules remain for widget or complex-selector boundaries.

Do not convert code mechanically without visual and behavior evidence.

## CSS Modules Migration Cases

When moving toward CSS Modules:

- define token access;
- replace global feature selectors;
- establish composition and variants;
- handle runtime values;
- preserve state attributes and primitive behavior;
- define third-party boundaries.

Do not recreate a utility framework through uncontrolled global classes.

## Design-System Adoption

When adopting a design system:

- confirm governance;
- map existing tokens;
- identify primitive/component coverage;
- preserve feature-specific behavior locally;
- define extension and exception policy;
- stage migration by user-visible slices;
- validate accessibility and visual parity.

Do not assume a shared component fits merely because its visual appearance is similar.

## Validation

A profile decision should identify required evidence:

- style lint or build;
- TypeScript where variant APIs are typed;
- component tests;
- accessibility checks;
- visual regression;
- responsive checks;
- theme checks;
- reduced-motion checks;
- package build/consumer validation;
- no forbidden imports;
- bundle/runtime impact where relevant.

Do not invent repository commands.

## Styling Decisions

Use:

```text
STYLING_PROFILE_SELECTED
STYLING_PROFILE_SELECTED_WITH_CONDITIONS
EXPLICIT_HYBRID_SELECTED
DESIGN_SYSTEM_BOUNDARY_REQUIRED
TOKEN_SOURCE_DECISION_REQUIRED
THEME_POLICY_REQUIRED
RESPONSIVE_POLICY_REQUIRED
MIGRATION_PLAN_REQUIRED
RETURN_TO_FRONTEND_STANDARD
BLOCKED
```

## Output

Use `assets/frontend-styling-profile-record.md`.

## Completion Criteria

- [ ] Scope and accepted UI behavior are explicit.
- [ ] Existing styling systems and repository rules were inspected.
- [ ] One primary profile or explicit hybrid is selected.
- [ ] Competing systems have a documented boundary.
- [ ] Primitive ownership and import policy are explicit.
- [ ] Token source is authoritative and semantic-token usage is defined.
- [ ] Variant strategy prevents contradictory combinations.
- [ ] Theming ownership, persistence, SSR, and contrast are explicit.
- [ ] Responsive strategy uses Flexbox, Grid, container, or viewport queries according to the problem.
- [ ] Global styles and selector specificity are bounded.
- [ ] Inline styles and `!important` have context-aware exception policies.
- [ ] Accessibility baseline is explicit.
- [ ] Shared/design-system promotion requires real evidence.
- [ ] Headless wrappers preserve accessibility and vendor behavior.
- [ ] Feature-local versus shared ownership is clear.
- [ ] Migration and exception policies are explicit where applicable.
- [ ] Required visual, accessibility, responsive, theme, package, and build evidence is identified.
- [ ] No CSS implementation, new styling system, or universal ban was produced.

## References

- Read `references/profile-selection-and-hybrid-boundaries.md` first.
- Read `references/tokens-variants-themes-and-runtime-values.md` for visual contracts.
- Read `references/primitives-design-systems-and-headless-ownership.md` for UI ownership.
- Read `references/responsive-global-css-specificity-and-accessibility.md` for discipline.
- Read `references/migration-exceptions-and-validation.md` before finalizing.
- Read `references/frontend-styling-profile-audit.md` before completion.
