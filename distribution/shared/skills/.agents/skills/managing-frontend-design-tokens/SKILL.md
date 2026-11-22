---
name: managing-frontend-design-tokens
description: Portable engineering capability `managing-frontend-design-tokens`. Use
  when the harness or a specialist agent explicitly requires this named capability.
---
# Managing Frontend Design Tokens

## Purpose

Create, reuse, govern, and evolve design tokens so repeated visual decisions have stable semantic meaning.

The core hierarchy is:

```text
raw/palette/base values
→ semantic tokens
→ component tokens/variants
→ feature/component implementation
```

Themes remap semantic tokens rather than forcing features to encode light/dark colors directly.

The purpose is not to turn every visual value into a global token.

The purpose is to centralize decisions that are:

- repeated;
- semantic;
- theme-sensitive;
- system-owned;
- expected to evolve together.

## Governing Standard

Repeated visual decisions SHOULD use semantic tokens.

Token categories include:

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

Prefer semantic names such as:

```text
color.text.primary
color.surface.elevated
color.action.danger
space.4
radius.medium
```

Hardcoded colors SHOULD be avoided when a semantic token exists.

Global styles SHOULD be limited to approved global concerns including tokens and themes.

## Use When

- Several components repeat the same visual decision.
- Dark/light themes need a stable semantic mapping.
- Danger/warning/success semantics need central colors.
- Spacing or size values are inconsistent across the app.
- A vendor design system needs token mapping.
- A token must be renamed/deprecated.
- A token's meaning has drifted.
- A feature wants to introduce a new root variable.
- A one-off value may not deserve global token status.
- Shared primitives need stable theme/token APIs.
- CSS Modules/Tailwind implementation reports a missing global token.

## Do Not Use When

- The task is to implement CSS Modules classes.
- The task is to implement Tailwind utilities.
- The task is to design component variant semantics only.
- The value is truly runtime/dynamic.
- The value is a one-off local geometry with no reusable semantic meaning.
- The project already has an appropriate semantic token.
- The proposed change would create a token solely to avoid writing one local CSS value.
- The task is to choose the styling framework.

## Inputs

- Existing token taxonomy.
- Palette/base values.
- Semantic tokens.
- Theme definitions.
- Component/shared UI tokens.
- Styling profile.
- Repeated usage evidence.
- Accessibility/contrast target.
- Vendor design-system tokens.
- Existing consumers.
- Deprecation/version policy.
- Naming conventions.
- Build/tooling constraints.
- Repository-local `AGENTS.md`.

## Outputs

- Token justification decision.
- Token category and ownership.
- Base/palette vs semantic separation.
- Theme mapping.
- Component/vendor mapping.
- Spacing/size scale decision.
- Deprecation/migration plan.
- Alias policy.
- Local one-off decision.
- Accessibility/contrast evidence.
- Design-token governance record.

## Core Workflow

```text
identify repeated visual decision
→ determine semantic meaning
→ decide local vs global ownership
→ place in token hierarchy
→ define theme mappings
→ define consumers/component mappings
→ check accessibility
→ define migration/deprecation
→ test themes and downstream usage
```

## Readiness Gate

Use one:

```text
READY_TO_MANAGE_FRONTEND_DESIGN_TOKENS
READY_WITH_CONDITIONS
TOKEN_NOT_REQUIRED
TOKEN_OWNERSHIP_REQUIRED
SEMANTIC_MEANING_REQUIRED
THEME_POLICY_REQUIRED
ACCESSIBILITY_EVIDENCE_REQUIRED
MIGRATION_POLICY_REQUIRED
BLOCKED
```

A valid result may be:

```text
TOKEN_NOT_REQUIRED
```

# Token Hierarchy

Use the following conceptual levels.

```text
LEVEL 0 — raw/reference value
LEVEL 1 — palette/base token
LEVEL 2 — semantic token
LEVEL 3 — component token
LEVEL 4 — local component/runtime value
```

Not every project implements every level explicitly.

## Raw / Reference Value

Example:

```text
#D92D20
4px
0.2s
```

A raw value is not a semantic API.

Do not consume raw values widely from product features when a semantic token exists.

# Palette / Base Tokens

Palette/base tokens describe a reusable scale or raw family.

Examples:

```text
color.red.600
color.neutral.50
space.4
radius.3
font.size.2
shadow.2
```

These are still mostly value-oriented.

Features should prefer semantic tokens when product meaning matters.

# Semantic Tokens

Semantic tokens describe meaning or UI role.

Examples:

```text
color.text.primary
color.text.muted
color.surface.default
color.surface.elevated
color.surface.warning
color.border.subtle
color.action.primary
color.action.danger
color.focus.ring
```

Semantic tokens are the preferred interface for repeated product UI decisions.

# Component Tokens

Component tokens narrow semantic decisions to one reusable component system.

Examples:

```text
button.primary.background
button.primary.foreground
dialog.backdrop.background
card.elevated.shadow
```

Component tokens are useful when:

- shared primitive has multiple coordinated values;
- variants must evolve centrally;
- vendor integration needs a stable mapping.

Do not create component tokens for every feature-local component automatically.

# Local Values

A local value is valid when it is:

- one-off;
- structural;
- mathematical;
- intrinsic;
- runtime;
- not semantically reused.

Examples:

```text
grid-template-columns: minmax(0,1fr) auto
chart marker width
one-off illustration offset
runtime progress %
```

Do not globalize local geometry merely to achieve 100% token coverage.

# Token Justification

Classify:

```text
SEMANTIC_TOKEN_JUSTIFIED
BASE_SCALE_TOKEN_JUSTIFIED
COMPONENT_TOKEN_JUSTIFIED
LOCAL_VALUE_PREFERRED
EXISTING_TOKEN_REUSE
TOKEN_NOT_REQUIRED
TOKEN_OWNERSHIP_REQUIRES_DECISION
```

# Token Creation Heuristics

A global semantic token is strongly justified when:

- meaning recurs across several components/features;
- it changes across themes;
- design wants centralized evolution;
- accessibility depends on coordinated mapping;
- a shared primitive depends on it;
- multiple styling systems need one semantic source.

It is weakly justified when:

- only one component uses it;
- meaning is unclear;
- value is visual coincidence;
- no theme/evolution need exists.

# Palette vs Semantic Meaning

Do not name product meaning after palette shade.

Weak:

```text
color.red.600
```

used directly for every danger action.

Preferred:

```text
color.action.danger
→ color.red.600 in light theme
→ another accessible mapping in dark/high-contrast theme
```

The palette can change while semantics remain stable.

# Semantic Stability

Changing:

```text
color.action.danger
```

from one red value to another is allowed if the meaning remains danger.

Changing it to represent warning is a semantic breaking change.

Do not silently repurpose token meaning.

# Danger Color

Danger is a semantic concept.

Possible uses:

```text
destructive action
critical error
danger text
danger surface
danger border
```

Do not assume one danger color token can serve every context.

A design system may need role-specific tokens:

```text
color.action.danger.background
color.action.danger.foreground
color.text.danger
color.surface.danger
color.border.danger
```

Avoid a single generic:

```text
--danger-red
```

if contexts need different contrast relationships.

# Success / Warning / Info

Apply the same principle:

```text
semantic role
→ context-specific token
→ palette mapping
```

Do not make status meaning color-only.

Content/icon/state semantics remain necessary.

# Dark Mode

Dark mode should remap semantic tokens.

Preferred:

```text
light theme
color.surface.default → neutral.0
color.text.primary → neutral.950

dark theme
color.surface.default → neutral.950
color.text.primary → neutral.50
```

Feature components continue to consume:

```text
color.surface.default
color.text.primary
```

Do not force every feature to define:

```text
light value
+
dark value
```

when semantic theme tokens already exist.

# Theme Layers

Possible themes:

```text
light
dark
high contrast
brand variants
tenant themes
```

Use only themes the product supports.

Do not create speculative theme dimensions.

# Theme Override Ownership

Themes belong to global/design-system ownership.

Feature modules should not mutate root theme variables.

A feature may override a semantic/component token locally only when the component API explicitly permits contextual variation.

# Theme Fallbacks

Token fallback behavior should be explicit.

Avoid masking missing theme mappings with arbitrary hardcoded fallback values in every component.

Tests should detect incomplete token definitions.

# Theme Completeness

For each semantic token used across themes, verify that required theme variants resolve.

Do not let one theme silently inherit an inaccessible default when semantics differ.

# Contrast

Color tokens affecting text, controls, focus, and status must meet the project's accessibility target.

Record contrast evidence for key pairs.

Do not approve a new danger/background mapping based solely on visual preference.

# Focus Tokens

Focus indication should use semantic tokens.

Example:

```text
color.focus.ring
size.focus.ring
offset.focus.ring
```

depending on system.

Do not let component variants erase visible focus.

# Spacing Scale

A spacing scale provides reusable rhythm.

Example conceptual scale:

```text
space.1
space.2
space.3
space.4
space.6
space.8
```

Exact values are project-specific.

The scale should be coherent and intentionally bounded.

Do not add a new global spacing token for every pixel value encountered.

# Spacing Scale Evaluation

Ask:

```text
Does this spacing repeat?
Does it belong to the project rhythm?
Does another existing value already express the intended density?
```

If yes, reuse scale.

If one specific geometry needs 13px and has no repeated semantic meaning, local value may be preferable.

# Spacing Aliases

Some systems define semantic spacing aliases:

```text
space.control.inline
space.card.padding
space.section.gap
```

Use only when central design ownership benefits.

Do not alias the entire numeric scale into dozens of equivalent names without semantic value.

# Size Tokens

Use size tokens for stable repeated dimensions:

```text
control.height.sm
avatar.md
icon.sm
sidebar.width
```

when centrally owned.

Do not turn every width into a global size token.

# Typography Tokens

Typography tokens may include:

```text
font.family
font.size
font.weight
line.height
letter.spacing
text.style.body
text.style.heading
```

Prefer semantic text styles where project design-system ownership warrants it.

Do not duplicate typography values across features.

# Radius Tokens

Use stable radius scale/semantic values.

Do not add:

```text
radius.13
```

just because one screenshot shows 13px.

# Border Tokens

Possible:

```text
border.width.default
color.border.subtle
color.border.strong
```

Keep width/style/color concerns distinct if system benefits.

# Shadow / Elevation Tokens

Use shared elevation tokens for repeated surfaces.

Avoid component-specific box-shadow copies across features.

Do not create dozens of near-identical elevation tokens.

# Motion Tokens

Motion tokens may encode:

```text
duration.fast
duration.normal
easing.standard
```

Respect reduced-motion strategy.

Do not make motion essential to understanding.

# Z-Index / Layer Tokens

Prefer semantic layer tokens:

```text
layer.base
layer.sticky
layer.dropdown
layer.modal
layer.tooltip
layer.toast
```

rather than numeric escalation.

Do not use:

```text
z-index: 99999
```

as a token strategy.

# Breakpoint Tokens

Breakpoint tokens may represent page-level responsive thresholds.

Component container-query thresholds may remain component-local if they are content-driven.

Do not globalize every container threshold.

# Token Naming

Names should be:

- semantic;
- stable;
- composable;
- implementation-independent;
- not tied to one feature unless component-scoped.

Avoid:

```text
blue500ForButtons
homepageCardGray
newRed
tempSpacing
```

# Naming Grammar

Use repository conventions.

Possible grammar:

```text
category.role.state
component.variant.property
scale.step
```

Examples:

```text
color.text.primary
color.action.danger.background
button.primary.background
space.4
```

Do not redesign naming grammar if the repository already has one.

# Token Ownership

Classify ownership:

```text
GLOBAL_DESIGN_SYSTEM
SHARED_UI_COMPONENT
FEATURE_LOCAL
VENDOR_ADAPTER
THEME
```

Ownership determines who may change meaning.

# Vendor Token Mapping

External design systems may provide vendor tokens.

Example:

```text
Radix colors
Material tokens
Fluent tokens
company vendor package
```

Prefer a mapping layer:

```text
vendor token
→ project semantic token
```

or:

```text
project semantic token
→ vendor theme input
```

depending on direction.

Do not make feature code depend directly on vendor palette names if project semantics should be stable.

# Vendor Mapping Strategies

Use one:

```text
PROJECT_SEMANTIC_WRAPS_VENDOR
VENDOR_THEME_CONSUMES_PROJECT_TOKENS
DIRECT_VENDOR_TOKEN_ACCEPTED
HYBRID_WITH_EXPLICIT_BOUNDARY
```

Record why.

# Vendor Lock-In

A mapping layer can reduce coupling.

But do not map every vendor token one-to-one if the project only uses a small subset.

Map semantic roles actually needed.

# Vendor Accessibility

If vendor tokens have accessible state pairs, preserve or improve them.

Do not remap vendor foreground/background pairs independently without contrast validation.

# Multiple Styling Systems

If Tailwind and CSS Modules both consume tokens, semantic tokens should remain framework-neutral.

Examples:

```text
CSS custom properties
design token build artifacts
shared theme package
```

Do not maintain separate semantic meanings per styling framework.

# Token Source of Truth

Choose one authoritative token source.

Possible:

```text
JSON/token source
TypeScript object
CSS custom properties
design token package
Style Dictionary/Tokens Studio output
framework theme config
```

Follow project architecture.

Do not create a second competing source of truth from one feature.

# Generated Outputs

If source tokens generate:

```text
CSS variables
Tailwind theme
TS types
platform artifacts
```

edit the source, not generated files.

Record generated consumers.

# Token Type Safety

If project generates token typings/autocomplete, use it.

Do not introduce codegen solely for one token change.

# Hardcoded Value Audit

Classify each hardcoded value:

```text
EXISTING_TOKEN_AVAILABLE
NEW_SEMANTIC_TOKEN_CANDIDATE
BASE_SCALE_CANDIDATE
LOCAL_ONE_OFF
RUNTIME_VALUE
LEGACY_DEBT
```

Do not replace every hardcoded value mechanically.

# One-Off Local Value

A local one-off should remain local when:

- meaning is not reusable;
- it is geometry-specific;
- no theme mapping is needed;
- no shared design decision exists.

Example:

```text
transform: translateY(-1px)
```

for optical alignment may remain local.

Do not create:

```text
offset.optical.minus1
```

unless this is a recurring system decision.

# Local One-Off Evaluation

Ask:

```text
Would another team know when to use this token?
Would changing it globally make semantic sense?
```

If not, keep local.

# Token Proliferation

Warning signs:

```text
hundreds of near-identical color tokens
one token per component pixel
many aliases to same raw value
temporary names becoming permanent
tokens named after feature tickets
```

Use:

```text
PROPORTIONATE_TOKEN_SYSTEM
TOKEN_PROLIFERATION
TOKEN_GAP
SEMANTIC_DRIFT
```

# Aliases

Aliases are valid for:

- migration;
- semantic layering;
- component token → semantic token mapping.

Avoid permanent alias chains:

```text
A → B → C → D → raw value
```

unless tooling/system clearly benefits.

Keep dependency depth understandable.

# Deprecated Tokens

A token may be deprecated because:

- name is wrong;
- semantic meaning changed;
- duplicate exists;
- system moved to new hierarchy;
- component token replaced by semantic token.

Do not delete immediately if consumers exist.

# Deprecation Flow

Preferred:

```text
introduce replacement
→ mark old token deprecated
→ document replacement
→ migrate consumers
→ prevent new usage
→ remove after accepted window
```

Do not silently point deprecated token to a semantically different replacement if behavior would change unexpectedly.

# Deprecation Metadata

If tooling supports it, record:

```text
deprecated: true
replacement
since
removal target
reason
```

Otherwise document in token registry/migration notes.

# New Usage Prevention

Possible:

```text
lint rule
type deprecation
docs warning
code review gate
```

Use existing project tooling.

Do not build a new lint plugin for one token unless project policy justifies it.

# Token Migration

Migration should distinguish:

```text
mechanical alias-compatible change
semantic visual change
theme-sensitive change
breaking component contract
```

Visual review may be necessary.

# Deprecated Token Evaluation

Given:

```text
color.red.error
```

replaced by:

```text
color.text.danger
```

check whether all usages are actually text-danger semantics.

Some consumers may need:

```text
color.border.danger
color.surface.danger
```

Do not mass-replace by string similarity.

# Token Versioning

For published design-system packages, token changes may be API changes.

Classify:

```text
PATCH_VALUE_CHANGE
MINOR_ADDITIVE_TOKEN
DEPRECATION
BREAKING_REMOVAL
SEMANTIC_BREAKING_CHANGE
```

Follow repository/package version policy.

# Value Change Risk

Changing a semantic token's raw value may affect many components.

Assess:

- contrast;
- visual regression;
- brand;
- screenshots;
- vendor mappings;
- dark theme;
- high contrast;
- print/document output.

Do not treat token-value edits as trivial local changes.

# Themes and Deprecated Tokens

When deprecating a token, migrate theme mappings consistently.

Do not leave old token defined only in light theme.

# Component Token Mapping

A component token may map:

```text
button.danger.background
→ color.action.danger.background
```

This allows component-level evolution.

Use when component system warrants it.

Do not add component token layer if semantic tokens already serve the primitive cleanly.

# Design-System Primitive Mapping

Shared primitives should consume semantic/component tokens rather than palette values.

Feature consumers should use primitive variants rather than token names where possible.

Example:

```text
feature
→ Button variant=danger
→ button token
→ semantic token
→ palette
```

# Theme Overrides in Components

Allow component-local token override only when:

- component API supports contextual theming;
- override is semantic;
- accessibility remains valid.

Do not mutate global token definitions.

# Dark Mode Evaluation

Must verify:

- semantic tokens are theme-stable;
- light/dark mappings exist;
- features do not encode repeated raw dark pairs;
- contrast is valid;
- component tokens inherit correctly.

# Danger Color Evaluation

Must verify:

- danger semantics;
- context-specific surface/text/action roles;
- contrast;
- not color-only;
- feature code does not consume raw red shade unnecessarily.

# Spacing Scale Evaluation

Must verify:

- repeated spacing aligns to scale;
- no unnecessary new scale step;
- local one-off geometry remains local;
- component semantic spacing aliases are justified.

# Vendor Token Mapping Evaluation

Must verify:

- direction of mapping;
- semantic roles;
- vendor lock-in boundary;
- contrast/theme consistency;
- unused vendor tokens are not mirrored speculatively.

# Deprecated Token Evaluation

Must verify:

- replacement semantics;
- migration inventory;
- new usage prevention;
- theme consistency;
- removal timing.

# Local One-Off Value Evaluation

Must verify:

- no repeated semantic meaning;
- no theme dependency;
- no global evolution need;
- token would not improve communication.

Then accept:

```text
LOCAL_VALUE_PREFERRED
```

# Accessibility

Token governance affects accessibility.

Review tokens for:

- contrast;
- visible focus;
- disabled states;
- error/warning/success distinguishability;
- reduced motion;
- touch/control size;
- high contrast where supported.

Do not certify accessibility from token values alone; component behavior also matters.

# Contrast Pair Testing

Test semantic foreground/background pairs rather than isolated colors.

Examples:

```text
text.primary on surface.default
text.danger on surface.default
action.danger.foreground on action.danger.background
focus.ring against adjacent surfaces
```

# Color Scheme

If browser `color-scheme` is used, align it with theme behavior.

Do not set it from individual components.

# Forced Colors

If project supports forced-colors/high contrast, token use should not block system adjustments unnecessarily.

Review shared primitives.

# Runtime Brand/Theming

If product supports tenant branding, define a constrained theme contract.

Do not let arbitrary tenant values replace accessibility-critical tokens without validation/fallback.

# User Customization

User-selected colors may be runtime values rather than fixed design tokens.

Map/validate carefully.

Do not globalize every user choice into static token taxonomy.

# Tooling

Possible token tooling:

```text
Style Dictionary
Tokens Studio
Theo
custom build pipeline
CSS variables
TypeScript generation
Tailwind theme integration
```

Use existing tooling.

Do not introduce tooling merely to manage one token.

# Documentation

Shared/global tokens should document:

- semantic purpose;
- allowed contexts;
- theme mappings;
- deprecation;
- component consumers where useful.

Do not require exhaustive prose for obvious scale tokens.

# Token Discoverability

Developers should be able to answer:

```text
Which token should I use for danger text?
```

If names are ambiguous, improve taxonomy/documentation.

Do not solve ambiguity by adding duplicate synonyms.

# Audit Usage

Search for:

- raw hardcoded colors;
- repeated spacing;
- deprecated token usage;
- direct vendor tokens;
- theme-specific hardcodes;
- semantic tokens used in wrong contexts.

Do not mass-fix unrelated usage outside accepted scope unless requested.

# Testing Strategy

Token tests may include:

- generated token existence;
- theme completeness;
- alias resolution;
- no cycles;
- deprecation metadata;
- semantic contrast pairs;
- vendor mapping;
- representative visual regression.

Do not unit-test every raw constant trivially.

# Theme Snapshot

Visual regression should cover representative shared primitives/pages in supported themes.

Do not rely solely on snapshotting token JSON.

# Token Graph Integrity

If tokens alias each other, verify:

- no cycles;
- valid references;
- all required themes resolve;
- no dangling deprecated alias.

# Consumer Tests

Shared primitive visual tests are often better evidence than isolated token tests for value changes.

Example:

```text
Button danger
Dialog
Alert
Focus ring
```

# Dark Mode Test

Verify semantic token behavior under light/dark theme.

Do not assert that a particular feature includes `dark:` classes if token-driven theme is used.

# Deprecated Token Test

If tooling can detect deprecation, verify no new usage in changed code.

Do not block legacy migration incrementally unless project policy says immediate removal.

# Migration Evidence

For high-impact token change, record:

- before/after visual;
- affected components;
- themes;
- contrast;
- package/version impact.

# Governance Decision Matrix

For a proposed token ask:

```text
1. Is the decision repeated?
2. Does it have stable semantic meaning?
3. Does it need theme remapping?
4. Is central evolution desirable?
5. Is a suitable token already available?
6. Is it component-specific or global?
7. Does accessibility depend on coordinated use?
8. Would another developer know when to use it?
9. Is it actually one-off geometry/runtime?
10. What migration impact exists?
```

# Overmodeling Audit

Flag:

- token per pixel;
- feature-ticket token names;
- token created for one-off transform;
- palette token duplicated as semantic synonym;
- component token layer with no value;
- alias chains;
- vendor token mirror of entire external system;
- multiple token sources of truth.

# Under-Modeling Signals

Flag:

- repeated hardcoded danger colors;
- light/dark values duplicated in components;
- spacing drift;
- shared primitives using palette shades directly;
- arbitrary z-index escalation;
- direct vendor tokens everywhere;
- deprecated tokens with no migration plan.

# Final Decision

Use:

```text
FRONTEND_DESIGN_TOKENS_READY
FRONTEND_DESIGN_TOKENS_READY_WITH_CONDITIONS
TOKEN_NOT_REQUIRED
EXISTING_TOKEN_REUSE
NEW_SEMANTIC_TOKEN_REQUIRED
NEW_COMPONENT_TOKEN_REQUIRED
TOKEN_DEPRECATION_REQUIRED
TOKEN_MIGRATION_REQUIRED
ACCESSIBILITY_REVIEW_REQUIRED
BLOCKED
```

## Output

Use `assets/frontend-design-token-governance-record.md`.

## Completion Criteria

- [ ] Token source of truth is explicit.
- [ ] Proposed token has a justified semantic/system role.
- [ ] Existing token reuse is checked first.
- [ ] Palette/base and semantic tokens are distinguished.
- [ ] Features consume semantic tokens where product meaning matters.
- [ ] Theme mappings preserve semantic meaning.
- [ ] Dark mode is implemented through semantic remapping rather than repeated raw light/dark values where possible.
- [ ] Danger/warning/success roles are context-specific enough for contrast/accessibility.
- [ ] Spacing/size scales remain coherent and bounded.
- [ ] One-off local values are allowed when tokenization adds no semantic value.
- [ ] Global token creation is not used merely to eliminate local CSS literals.
- [ ] Shared/component token ownership is explicit.
- [ ] Vendor token mapping has a documented direction and boundary.
- [ ] Direct vendor token leakage is avoided where project semantics should remain stable.
- [ ] Theme/contrast evidence exists for accessibility-sensitive tokens.
- [ ] Token aliases are intentional and shallow.
- [ ] Deprecated tokens have replacement, migration, new-usage prevention, and removal strategy.
- [ ] Semantic token meaning is not silently repurposed.
- [ ] Published token changes respect package/versioning policy.
- [ ] Multiple styling systems consume one semantic source where architecture requires it.
- [ ] Generated artifacts are updated from source rather than hand-edited.
- [ ] Token graph has no cycles/dangling references.
- [ ] High-impact changes have representative visual evidence.
- [ ] Roadmap evaluations are covered: dark mode, danger color, spacing scale, vendor token mapping, deprecated token, local one-off value.
- [ ] No new token toolchain/framework is introduced without approval.
- [ ] Final token-governance decision is explicit.

## References

- Read `references/token-hierarchy-and-semantic-meaning.md` first.
- Read `references/themes-dark-mode-contrast-and-accessibility.md`.
- Read `references/spacing-size-typography-radius-shadow-and-layer-scales.md`.
- Read `references/vendor-token-mapping-and-shared-ui-boundaries.md`.
- Read `references/deprecation-migration-versioning-and-aliases.md`.
- Read `references/local-values-token-proliferation-and-governance.md`.
- Read `references/testing-tooling-and-token-graph-integrity.md`.
- Read `references/frontend-design-token-governance-audit.md` before completion.
