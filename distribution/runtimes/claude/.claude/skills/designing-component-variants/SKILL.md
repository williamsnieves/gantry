---
name: designing-component-variants
description: Designs explicit, valid frontend component variant APIs before styling implementation. Use when a shared or feature component needs semantic visual/behavioral variants, sizes, compound variants, loading/disabled states, token mapping, or a decision about whether styling belongs in a shared primitive or a feature wrapper. Prevent contradictory boolean props, combinatorial variant explosions, raw color/spacing props that bypass design tokens, and feature-specific business styling leaking into shared primitives. Keep the result implementation-agnostic so it can be realized with CSS Modules, Tailwind, CSS-in-JS, or a design-system variant mechanism.
---

# Designing Component Variants

## Purpose

Design a component variant model that is explicit, valid, and proportional.

This skill answers:

```text
Which visual and behavioral variants does this component actually support?
```

and:

```text
Which combinations are valid?
```

before deciding how CSS Modules, Tailwind, CVA, a design system, or another styling implementation will realize them.

The core flow is:

```text
component semantics
→ variant axes
→ valid combinations
→ state behavior
→ semantic token mapping
→ styling implementation
```

The variant contract should reveal component intent without exposing low-level styling details.

## Governing Standard

Repeated visual decisions SHOULD use semantic tokens.

Component variants MUST be explicit and valid.

Avoid contradictory boolean-prop combinations.

Use a variant system appropriate to the chosen stack.

This skill defines the semantic contract, not the final implementation mechanism.

## Use When

- A Button/Card/Badge/etc. needs explicit variants.
- Several boolean props can contradict one another.
- Size variants are inconsistent.
- Loading and disabled states interact ambiguously.
- Compound variants exist.
- Shared primitive styling is growing feature-specific.
- Raw color/spacing props bypass semantic design tokens.
- The team is unsure whether a new variant belongs in shared UI or only in a feature wrapper.
- Tailwind/CSS Modules implementation needs a stable variant contract first.

## Do Not Use When

- The task is to implement Tailwind utilities.
- The task is to implement CSS Modules.
- The task is to manage the global design-token taxonomy.
- The task is general accessibility design.
- The task is to integrate a headless primitive's keyboard/focus behavior.
- The component has no meaningful variant axis.
- The proposal would create variants solely to expose arbitrary styling knobs.

## Inputs

- Component purpose.
- Shared vs feature ownership.
- Existing project primitive API.
- Design-token source.
- Existing variant conventions.
- Visual states from product/design.
- Behavioral states.
- Accessibility requirements.
- Styling profile.
- Existing shared UI boundaries.
- Test strategy.
- Repository-local `AGENTS.md`.

## Outputs

- Variant-justification decision.
- Variant axes.
- Size model.
- State model.
- Compound-variant rules.
- Invalid-combination rules.
- Shared-vs-feature ownership.
- Semantic token mapping requirements.
- Implementation-neutral variant contract.
- Variant test matrix.
- Component-variant design record.

## Core Workflow

```text
identify component responsibility
→ inventory meaningful variation
→ separate semantic variants from styling knobs
→ define axes
→ define valid combinations
→ define loading/disabled behavior
→ decide shared vs feature ownership
→ map to semantic tokens
→ define tests
```

## Readiness Gate

Use one:

```text
READY_TO_DESIGN_COMPONENT_VARIANTS
READY_WITH_CONDITIONS
NO_VARIANT_MODEL_REQUIRED
COMPONENT_OWNERSHIP_REQUIRED
DESIGN_SEMANTICS_REQUIRED
TOKEN_SOURCE_REQUIRED
STATE_BEHAVIOR_REQUIRED
BLOCKED
```

A valid result may be:

```text
NO_VARIANT_MODEL_REQUIRED
```

Do not create a variant system for a component with one stable appearance.

# Variant Semantics

A variant should represent stable component meaning.

Good:

```text
primary
secondary
danger
success
warning
subtle
outline
```

when those meanings are part of the component system.

Weak:

```text
red
blue
gray
12px
left
bold
```

when they are merely low-level styling knobs.

Prefer semantic variants over visual implementation details.

# Variant Axes

Classify each axis:

```text
VISUAL_VARIANT
SIZE
DENSITY
STATE
ORIENTATION
EMPHASIS
PLACEMENT
FEATURE_MODE
```

Not every component needs every axis.

Example:

```text
Button
- variant
- size
- loading
- disabled
```

A Card may instead need:

```text
Card
- tone
- density
- elevation
```

Use only axes supported by accepted behavior.

# Boolean Prop Smell

Avoid APIs such as:

```tsx
<Button
  primary
  secondary
  danger
  small
  large
  loading
  disabled
/>
```

because contradictory combinations are possible.

Prefer:

```tsx
<Button
  variant="danger"
  size="sm"
  loading
  disabled
/>
```

where axes are mutually exclusive by construction.

# Boolean Props That Are Fine

Not all booleans are bad.

A boolean is appropriate when the semantic state itself is binary:

```text
disabled
loading
selected
fullWidth
required
```

provided it does not conflict with another boolean representing the same axis.

Bad:

```text
small + medium + large
```

Good:

```text
size="sm" | "md" | "lg"
```

# Button Variants

A shared Button should expose a small semantic set.

Example:

```text
primary
secondary
danger
ghost
link
```

Only include variants that:

- recur across product surfaces;
- have stable semantics;
- share the same interaction contract;
- belong centrally in shared UI.

Do not add:

```text
checkoutPrimary
subscriptionDanger
campaignCTA
```

to shared Button.

Those are feature semantics.

# Shared vs Feature Variant

Classify:

```text
SHARED_PRIMITIVE_VARIANT
FEATURE_WRAPPER_VARIANT
LOCAL_COMPONENT_VARIANT
NO_VARIANT_REQUIRED
```

A shared primitive variant is justified when it expresses a recurring UI-system semantic.

A feature-specific variant should remain outside shared primitive.

Example:

```text
shared Button variant="danger"
```

is fine.

But:

```text
shared Button variant="renewSubscription"
```

is feature leakage.

Use feature composition:

```tsx
<RenewSubscriptionAction>
  <Button variant="primary" />
</RenewSubscriptionAction>
```

or a feature component.

# Size Variants

Size should represent an intentional component scale.

Example:

```text
sm
md
lg
```

Each size may map coherently to:

- control height;
- horizontal padding;
- typography;
- icon size;
- gap;
- touch target.

Do not let each feature redefine what `sm` means.

# Size Semantics

For interactive controls, size must still respect accessibility and hit-target expectations.

A smaller visual variant may still preserve sufficient target size through padding/layout.

Do not use a `xs` size that makes controls unusably small merely for table density unless project accessibility policy explicitly supports an alternative pattern.

# Density vs Size

Distinguish:

```text
size
→ component scale

density
→ spacing/compactness
```

Do not overload size when the component's semantic scale remains the same but content spacing changes.

Example:

```text
Card density="compact"
```

may be better than:

```text
Card size="sm"
```

if only padding changes.

# Loading State

Loading is usually a component state, not a visual variant axis.

Define:

- whether interaction is blocked;
- whether content remains visible;
- whether spinner replaces icon/text;
- accessible busy state;
- width preservation;
- focus behavior;
- whether `disabled` is implied.

Do not implement loading as:

```text
variant="loading"
```

unless the project component system explicitly treats it as a state variant.

# Loading vs Disabled

Loading and disabled can overlap but mean different things.

```text
disabled
→ action unavailable

loading
→ action currently processing
```

A loading Button may behave disabled while preserving a distinct semantic state.

Decide:

```text
LOADING_IMPLIES_DISABLED
LOADING_ALLOWS_CANCEL
LOADING_INTERACTION_POLICY_REQUIRED
```

Do not let users accidentally trigger duplicate commands if loading should block activation.

# Disabled State

Disabled should preserve semantic/native behavior.

For native buttons:

```text
disabled
```

is usually preferable.

For non-native primitives, use the project's accessible disabled semantics.

Do not implement disabled only through opacity.

# Loading Accessible Semantics

Consider:

```text
aria-busy
accessible loading label
status text
preserve accessible name
```

according to component behavior.

Do not replace button text with an unlabeled spinner.

# Variant + State Matrix

Define state interactions explicitly.

Example:

| Variant | Loading | Disabled | Expected |
|---|---|---|---|
| primary | no | no | active |
| primary | yes | implied | pending |
| danger | no | yes | unavailable |
| danger | yes | implied | pending destructive action |

Do not leave state interaction to accidental CSS precedence.

# Compound Variants

A compound variant is justified when a combination has semantics not expressible by independent axes.

Example:

```text
variant="outline"
+
tone="danger"
```

may need:

```text
danger border
danger text
danger hover surface
```

if those mappings are truly combination-specific.

Use compound variants sparingly.

# Compound Variant Smell

If the matrix grows rapidly:

```text
5 variants × 4 sizes × 5 states × 3 densities
```

ask whether:

- axes are redundant;
- shared primitive owns too much;
- feature-specific behavior has leaked inward;
- states should be native/pseudo-state behavior instead;
- tokens can absorb the difference.

Do not encode every visual combination as a manual compound rule.

# Compound Variant Decision

Use:

```text
COMPOUND_VARIANT_JUSTIFIED
INDEPENDENT_AXES_SUFFICIENT
VARIANT_MODEL_TOO_COMPLEX
FEATURE_SPLIT_REQUIRED
```

# Default Variant

Define defaults explicitly.

Example:

```text
variant="primary"
size="md"
```

or no default if callers must choose.

Defaults should reflect project conventions.

Do not make a destructive action default.

# Optional Variant Prop

If variant prop is optional, its default must be stable.

Avoid runtime context changing defaults invisibly unless the project system explicitly supports context-driven component theming.

# Semantic Token Mapping

Variant design should identify semantic token categories.

Example:

```text
primary
→ action.primary.background
→ action.primary.foreground
→ action.primary.border
→ action.primary.hover
```

The exact token names belong to the project token system.

Do not embed:

```text
#2563eb
#ffffff
```

into the semantic variant contract.

# Token Ownership

This skill may identify:

```text
TOKEN_EXISTS
TOKEN_GAP
FEATURE_LOCAL_VALUE
```

It does not redesign the token system.

If a new global semantic token is needed, record it for `managing-frontend-design-tokens`.

# Variant Naming

Variant names should describe stable meaning, not current implementation.

Prefer:

```text
danger
subtle
elevated
compact
```

over:

```text
red
gray
shadow2
padding8
```

unless the design-system vocabulary itself is intentionally palette/scale-based.

# Behavior vs Appearance

Some props change behavior more than appearance.

Examples:

```text
dismissible
selectable
collapsible
orientation
```

Do not force them into a generic `variant` prop.

Use separate semantic props.

# Orientation

For components such as Tabs/Divider/Toolbar:

```text
orientation="horizontal" | "vertical"
```

is often clearer than a boolean:

```text
vertical
```

when both modes are first-class.

# Placement

Placement may be a stable axis for overlays/badges.

Example:

```text
placement="top" | "bottom"
```

but vendor positioning details should not leak into a generic primitive unless part of the project API.

# Feature Mode

A feature-local component may use a semantic feature mode:

```text
mode="preview" | "editable"
```

if it changes valid behavior/styling.

Do not promote such feature modes into shared primitives.

# Variant Prop Explosion

Flag APIs like:

```tsx
<Card
  compact
  elevated
  bordered
  muted
  warning
  rounded
  interactive
  selected
/>
```

Ask whether these are independent semantics or arbitrary style toggles.

A stable component API should not become a CSS property bag.

# Style Prop Escape Hatch

Do not use variant design to eliminate all styling flexibility.

Project policy may allow:

```text
className
style
slot classes
CSS variables
```

for composition/runtime needs.

But stable semantic variants should remain the main API for repeated product decisions.

# Raw Color Prop

Avoid:

```tsx
<Badge color="red" />
```

when product meaning is:

```tsx
<Badge tone="danger" />
```

A raw palette/color prop may be valid for:

- charts;
- user-customized themes;
- data visualization;
- brand swatches;
- intentionally palette-driven primitives.

Classify intentionally.

# Icon Variants

Do not create variant values solely to swap icons if icon is content.

Prefer explicit:

```text
icon
startIcon
endIcon
```

when project API supports it.

If icon changes as part of semantic state, a variant may determine the default icon, but avoid hiding content decisions in styling.

# Text Variants

Do not put copy/content into variant definitions.

Variant may alter tone/style, not business text.

# Shared Primitive Boundary

A shared primitive should remain generic enough to be reused but opinionated enough to ensure consistency.

Too generic:

```text
backgroundColor
padding
borderRadius
fontSize
shadow
```

Too specific:

```text
subscriptionUpgrade
campaignError
paymentExpired
```

Aim for project UI semantics.

# Feature-Specific Styling Leak

A common smell:

```text
shared Button gets `subscriptionRenewal` variant
```

because one feature needs a unique look.

Preferred options:

```text
existing semantic shared variant
+
feature wrapper/layout

feature-local component

new shared semantic variant only if design-system meaning truly recurs
```

# Promotion Threshold

Do not promote feature styling into shared UI based on “used twice” alone.

Ask:

- same semantics?
- same interaction contract?
- same accessibility?
- likely central ownership?
- design system recognizes it?

Reuse by coincidence is insufficient.

# Variant Implementation Independence

This skill should output a contract implementable by:

```text
CSS Modules
Tailwind
CVA
design-system recipes
CSS-in-JS
vanilla CSS
```

Do not make the semantic model depend on class names.

Example output:

```text
variant = primary | secondary | danger
size = sm | md | lg
loading = boolean
disabled = boolean
```

Then styling skill maps it.

# CSS Modules Mapping

Possible later implementation:

```text
styles.root
styles.primary
styles.sm
styles.loading
```

This skill should not prescribe exact class structure.

# Tailwind Mapping

Possible later implementation:

```text
variant map
size map
state utilities
```

This skill should not prescribe CVA or tailwind-merge unless project already requires them.

# Design-System Mapping

A company design system may already have:

```text
Button.variant
Button.size
```

Reuse it.

Do not create a parallel feature variant vocabulary unless necessary.

# Variant Aliases

Avoid aliases unless migration requires them.

Example:

```text
danger
destructive
```

should not both mean the same thing indefinitely.

Choose one canonical term.

# Deprecated Variants

When a shared variant is deprecated:

- preserve migration compatibility only if project policy requires it;
- document replacement;
- avoid using it in new code.

Do not keep adding aliases forever.

# Invalid Combinations

Make invalid combinations difficult or impossible.

Examples:

```text
iconOnly + children required
loading + href navigation semantics
size="xs" + touch-only primary action
```

If TypeScript can encode the restriction proportionately, do so.

Do not create extremely complex generic types for trivial runtime rules.

# Type-Level Constraints

Use discriminated unions when they provide real safety.

Example:

```ts
type ButtonProps =
  | { iconOnly: true; "aria-label": string; children?: never }
  | { iconOnly?: false; children: ReactNode };
```

if project API needs this guarantee.

Do not turn simple style variants into type-system puzzles.

# Runtime Guards

For constraints difficult to encode, runtime development warnings may be acceptable if project policy uses them.

Do not add validation libraries to component props.

# Variant State Priority

When styles overlap, define priority semantically.

Example:

```text
disabled
→ overrides hover/active

loading
→ overrides interactive feedback

invalid
→ may override neutral border

focus-visible
→ remains visible even on selected state
```

Do not let CSS ordering decide accidentally.

# Hover / Active / Focus

These are interaction states, not ordinary variant axes.

Map them from each semantic variant.

Example:

```text
primary normal
primary hover
primary active
primary focus
```

The variant contract should ensure all required interaction states exist.

# Disabled Hover

Disabled controls should not show misleading hover/active feedback.

Variant implementation should reflect disabled precedence.

# Focus Across Variants

Every interactive variant must maintain visible focus.

Do not create a ghost/subtle variant whose focus ring disappears against its background.

# Contrast

Each visual variant must meet the project's contrast target.

Do not approve a variant contract whose token mapping cannot meet accessibility requirements.

# Color-Only Variants

A status component may have:

```text
success
warning
danger
```

but user meaning should not rely solely on color.

The semantic component may also provide text/icon/state.

Variant design should not replace accessibility/content design.

# Loading Width Stability

For Button loading state, define whether layout width should remain stable.

Common policy:

```text
preserve label footprint
```

to avoid layout shift.

Do not force this universally if a compact icon-only pattern is intended.

# Spinner Placement

Possible:

```text
replace start icon
prepend spinner
replace content but preserve accessible label
overlay spinner
```

Choose one project convention.

Do not let each feature invent loading layout.

# Icon-Only Button

Icon-only variant/state requires accessible name.

This is not merely a styling concern.

If the shared Button supports `iconOnly`, its API must enforce or document accessible labeling.

# Link Button

If a “Button” can render as anchor/link, interaction semantics may differ.

Avoid forcing disabled/link behavior into the same variant model if it becomes confusing.

Consider separate primitive or polymorphic API according to project design system.

# Destructive Semantics

Danger/destructive variant should represent destructive or high-risk action consistently.

Do not use danger merely because red matches a design screenshot.

# Success Variant

Interactive Buttons rarely need a persistent “success” variant unless project design system defines it.

A success state may be transient result feedback instead of a normal action variant.

Do not add variants solely because a color exists in tokens.

# Badge Variants

Badges/status chips may legitimately have more tone variants than buttons.

Component purpose determines allowed axes.

Do not reuse Button variant vocabulary mechanically across all primitives.

# Card Variants

Card may have:

```text
surface
elevation
density
interactive
selected
```

but avoid arbitrary combinatorial toggles.

Sometimes separate components are clearer:

```text
Card
SelectableCard
AlertCard
```

if behavior diverges substantially.

# Variant Split Decision

Use:

```text
ONE_COMPONENT_MULTIPLE_VARIANTS
SEPARATE_COMPONENTS_PREFERRED
FEATURE_WRAPPER_PREFERRED
SHARED_PRIMITIVE_EXTENSION_JUSTIFIED
```

Split when variants differ in:

- semantics;
- DOM structure;
- accessibility contract;
- behavior;
- data requirements;

not merely in color.

# Compound Component Variant

For multi-part primitives:

```text
Dialog
Tabs
Select
```

variant design may apply across slots.

Example:

```text
density="compact"
```

affects trigger/content/item spacing consistently.

Do not expose separate unrelated padding props per slot if one semantic axis suffices.

# Slot Variants

Shared design systems may support slots.

Use stable slot semantics:

```text
root
trigger
content
icon
label
description
```

Do not expose DOM-position selectors as public variant surface.

# Loading/Disabled in Headless Primitives

When integrating vendor primitives, preserve vendor-disabled/focus semantics.

Variant design should configure appearance without overriding functional accessibility.

# Variants and Async State

Component variant state should consume semantic async state, not create it.

Example:

```text
mutation pending
→ Button loading=true
```

The Button does not own the mutation.

# Variants and Domain

Variant selection may come from product semantics:

```text
severity="danger"
```

but Domain should not depend on UI variant names.

Presentation maps Domain/Application status to component variants.

# Mapping Layer

Example:

```text
Application:
subscriptionStatus = "expired"

Presentation:
Badge tone = "danger"
```

Do not make Application DTO return:

```text
badgeVariant = "danger"
```

unless that is explicitly accepted Presentation data ownership.

# Variant Testing

Test the public component contract.

Verify:

- supported variants render;
- invalid combinations are prevented/handled;
- loading behavior;
- disabled semantics;
- representative compound variants;
- feature-only styling remains outside shared primitive.

Do not snapshot all CSS classes.

# Visual Tests

Variants are visual contracts.

Visual regression/component explorer evidence is valuable for:

- every shared variant;
- each size;
- key compound combinations;
- dark/theme variants;
- focus/disabled/loading states.

Do not generate exhaustive cartesian snapshots if most combinations are redundant.

# Pairwise/Representative Coverage

For many axes, use representative combinations rather than full cartesian product.

Prioritize:

- defaults;
- extremes;
- risky compounds;
- accessibility states;
- theme differences.

# Story Matrix

If project uses Storybook/component explorer, a variant matrix can document:

```text
variant × size
```

with selected state examples.

Do not introduce Storybook solely for this skill.

# Button Variant Evaluation

Given:

```text
primary
secondary
danger
```

verify:

- semantic meaning;
- shared ownership;
- token mapping;
- focus/hover/disabled coverage;
- no feature-specific names.

# Size Variant Evaluation

Given:

```text
sm
md
lg
```

verify:

- consistent scale;
- typography/padding/icon mapping;
- hit-target accessibility;
- no feature-local redefinition.

# Compound Variant Evaluation

Given:

```text
variant="outline"
tone="danger"
```

verify whether the combination has stable semantics and whether independent token mapping is enough.

Do not add compound logic if axes already combine correctly.

# Loading/Disabled Evaluation

Verify:

- loading meaning;
- disabled meaning;
- whether loading implies disabled;
- accessible busy/name behavior;
- duplicate command prevention;
- focus/visual state.

# Feature-Specific Styling Evaluation

Given:

```text
Button variant="subscriptionRenewal"
```

classify as feature leakage unless the design-system semantic is genuinely cross-product.

Prefer feature composition or a feature-local component.

# Overmodeling Audit

Flag:

- huge variant matrices;
- raw style props exposed as “variants”;
- CVA/recipe abstraction introduced without styling-profile need;
- shared variant added for one feature;
- duplicate variant aliases;
- variants that only differ by one arbitrary color with no semantic meaning;
- type-level generics too complex for component value.

Use:

```text
PROPORTIONATE_VARIANT_MODEL
UNDERMODELED_VARIANTS
OVERMODELED_VARIANTS
FEATURE_STYLING_LEAK
TOKEN_GAP
NO_VARIANT_MODEL_REQUIRED
```

# Under-Modeling Signals

Flag:

- mutually exclusive boolean props;
- features reimplementing the same shared semantic style;
- arbitrary color/size props everywhere;
- loading/disabled interactions inconsistent;
- caller className used to simulate undocumented variants;
- shared primitive lacks recurring semantic variant.

# Final Decision

Use:

```text
COMPONENT_VARIANT_MODEL_READY
COMPONENT_VARIANT_MODEL_READY_WITH_CONDITIONS
NO_VARIANT_MODEL_REQUIRED
FEATURE_WRAPPER_REQUIRED
SHARED_PRIMITIVE_EXTENSION_REQUIRED
TOKEN_CHANGE_REQUIRED
STATE_BEHAVIOR_REQUIRED
ACCESSIBILITY_REVIEW_REQUIRED
BLOCKED
```

## Output

Use `assets/component-variant-design-record.md`.

## Completion Criteria

- [ ] Component ownership and responsibility are explicit.
- [ ] Variant model is justified.
- [ ] Variant names express semantic meaning rather than low-level styling.
- [ ] Mutually exclusive visual states use one explicit axis instead of contradictory booleans.
- [ ] Binary behavioral states remain booleans only where appropriate.
- [ ] Size/density/orientation axes are separated where semantics differ.
- [ ] Defaults are explicit and safe.
- [ ] Loading and disabled semantics are distinct and their interaction is explicit.
- [ ] Loading preserves accessible naming/busy behavior.
- [ ] Duplicate command behavior during loading is explicit.
- [ ] Compound variants exist only where independent axes are insufficient.
- [ ] Variant matrix is proportionate and not combinatorially explosive.
- [ ] Invalid combinations are prevented proportionately.
- [ ] Shared primitive variants are cross-product/project semantics.
- [ ] Feature-specific styling remains in a feature wrapper/local component.
- [ ] Raw color/spacing/style knobs do not replace semantic variants when a stable design meaning exists.
- [ ] Semantic token mapping needs are identified without redesigning the token system.
- [ ] Missing global tokens are recorded for the design-token skill.
- [ ] Contract remains implementation-neutral across CSS Modules, Tailwind, CSS-in-JS, or design-system recipes.
- [ ] Vendor/headless accessibility behavior is not overridden by variant design.
- [ ] Focus, disabled, contrast, loading, and accessible-name requirements are preserved.
- [ ] Tests cover representative variant/size/compound/loading/disabled cases.
- [ ] Styling implementation details/class strings are not treated as the public contract.
- [ ] Roadmap evaluations are covered: Button variants, size variants, compound variants, loading/disabled state, feature-specific styling leaking into shared primitive.
- [ ] No new variant library/framework is introduced by this semantic design skill.
- [ ] Final variant decision is explicit.

## References

- Read `references/semantic-variant-axes-and-boolean-prop-smells.md` first.
- Read `references/shared-vs-feature-variant-ownership.md`.
- Read `references/size-density-loading-and-disabled-states.md`.
- Read `references/compound-variants-invalid-combinations-and-complexity.md`.
- Read `references/tokens-accessibility-and-implementation-independence.md`.
- Read `references/testing-variant-matrices-and-overmodeling.md`.
- Read `references/component-variant-design-audit.md` before completion.
