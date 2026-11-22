---
name: implementing-css-modules-ui
description: Implements frontend UI using the project's selected CSS Modules profile. Use to create scoped component styles, consume semantic design tokens, compose variants, support responsive and theme behavior, keep specificity low, handle genuine runtime values with CSS variables or inline styles, and identify when a concern belongs in global tokens/themes rather than a component module. Avoid global leakage, brittle deep selectors, repeated hardcoded visual decisions, `!important` escalation, framework/library internals styling, and CSS Modules abstractions that duplicate the project's variant/design-system strategy.
---

# Implementing CSS Modules UI

## Purpose

Implement UI using CSS Modules when the project has selected CSS Modules as its primary or explicitly scoped styling strategy.

The core boundary is:

```text
component semantics
→ scoped CSS Module classes
→ semantic tokens / theme
```

Feature styles SHOULD remain scoped.

Global CSS SHOULD remain limited to:

- reset/normalization;
- design tokens;
- themes;
- base typography;
- document-level behavior;
- approved utilities;
- third-party boundaries.

CSS Modules are not a reason to:

- hide global design decisions inside feature files;
- use deep selectors against implementation details;
- recreate a design-token system per component;
- build a custom CSS framework.

## Governing Standard

The project MUST already define:

- primary styling strategy;
- design-token source;
- component primitive library;
- theming strategy;
- responsive strategy;
- accessibility baseline;
- allowed exceptions.

This skill MUST NOT introduce CSS Modules into a project whose selected styling profile is something else unless an accepted exception explicitly allows it.

Repeated visual decisions SHOULD use semantic tokens.

Feature styles SHOULD be scoped.

Avoid brittle selectors and specificity escalation.

Inline styles are acceptable for genuine runtime values.

`!important` SHOULD be exceptional and documented.

Hardcoded colors SHOULD be avoided when a semantic token exists.

CSS Modules composition may be used as one project-approved reuse mechanism.

## Use When

- CSS Modules is the selected styling profile.
- A component needs scoped styles.
- Feature styles are leaking globally.
- Repeated style decisions should consume tokens.
- Variants need explicit class composition.
- Theme behavior needs token-driven adaptation.
- Responsive component styles are required.
- Runtime values such as measured width/position/progress need CSS variables or inline style.
- Deep selectors or specificity escalation need correction.
- A developer is unsure whether a style belongs in a module or global token/theme layer.

## Do Not Use When

- The selected profile is Tailwind-only.
- The selected profile is CSS-in-JS-only.
- The task is to select a styling strategy.
- The task is to design component variants independent of implementation.
- The task is to create/manage the design-token system itself.
- The task is headless primitive integration.
- The task is general accessibility design.
- The proposed CSS Module would only wrap a design-system primitive with no feature-specific styling need.
- A global reset/theme/token change is needed but the component module is not the correct owner.

## Inputs

- Selected styling profile.
- Existing CSS Modules conventions.
- Design-token source.
- Theme strategy.
- Responsive strategy.
- Component/feature design.
- Component variant contract.
- Shared primitives/design-system APIs.
- Existing global CSS boundaries.
- Runtime dynamic-value requirements.
- Accessibility requirements.
- Browser support.
- Existing lint/style rules.
- Test/visual-regression strategy.
- Repository-local `AGENTS.md`.

## Outputs

- CSS Module file/component style implementation.
- Scoped class design.
- Token-consumption decisions.
- Global-vs-module ownership decision.
- Variant class composition.
- Responsive rules.
- Theme behavior.
- Runtime CSS variable/inline-style decision.
- Selector/specificity audit.
- CSS Modules implementation record.

## Core Workflow

```text
confirm CSS Modules profile
→ inspect tokens/theme/primitives
→ identify component-owned styles
→ identify global/token concerns
→ define scoped classes
→ compose explicit variants
→ implement responsive/theme behavior
→ isolate runtime values
→ audit selectors/specificity/leakage
```

## Readiness Gate

Use one:

```text
READY_TO_IMPLEMENT_CSS_MODULES_UI
READY_WITH_CONDITIONS
CSS_MODULES_PROFILE_REQUIRED
TOKEN_SOURCE_REQUIRED
THEME_POLICY_REQUIRED
RESPONSIVE_POLICY_REQUIRED
VARIANT_CONTRACT_REQUIRED
GLOBAL_STYLE_DECISION_REQUIRED
BLOCKED
```

Do not invent a new token/theme system inside a component task.

# Scope

A component module owns styles specific to that component/feature.

Example:

```text
PromotionCard.module.css
```

may own:

- card layout;
- local spacing;
- component-specific responsive behavior;
- component-specific state styling;
- feature-specific visual arrangement.

It should not own:

- global page reset;
- root design-token definitions;
- global theme variables;
- body typography baseline;
- unrelated utilities;
- global third-party normalization.

# CSS Module Naming

Use repository conventions.

Possible file names:

```text
PromotionCard.module.css
PromotionCard.module.scss
styles.module.css
```

Do not rename the whole repository convention.

Class names should describe component structure/semantics:

```css
.root {}
.header {}
.actions {}
.errorMessage {}
.compact {}
```

Avoid generated-looking utility names unless the project deliberately uses that convention:

```css
.mt12 {}
.redText {}
.flexRowCenter {}
```

when semantic layout/component names are clearer.

# Root Class

A clear module root is often useful:

```css
.root {}
```

or a component name:

```css
.card {}
```

It is not mandatory.

Do not force `.root` in every module if repository conventions differ.

# Scoped Styles

CSS Modules should prevent accidental global leakage.

Prefer:

```css
.root {}
.title {}
.actions {}
```

Avoid:

```css
button {}
h2 {}
a {}
```

when those selectors style all descendants unintentionally and component semantics would be safer.

Element selectors inside a clearly scoped root may be acceptable when structure is controlled and semantic.

Do not treat all element selectors as forbidden.

# Global Selectors

Use `:global(...)` only for an intentional boundary such as:

- third-party library markup;
- legacy integration;
- unavoidable external generated class;
- documented global contract.

Do not use `:global` to bypass CSS Modules because local styling is inconvenient.

Record every nontrivial global escape.

# Global Style Ownership

When a component needs a visual value shared broadly, ask:

```text
Is this a component style
or a system/token/theme decision?
```

Examples that often belong globally:

- semantic color token;
- spacing scale;
- global typography token;
- radius token;
- shadow token;
- motion duration/easing token;
- z-index layer token;
- breakpoint/container token;
- theme variable.

Do not define a duplicate “global” value in one feature module.

# Global Token Need Evaluation

If several components need:

```css
color: #b42318;
```

do not copy the hex value.

Prefer the selected token:

```css
color: var(--color-text-danger);
```

If no semantic token exists and the design decision is genuinely global, escalate to token/design-system ownership rather than inventing feature-specific copies.

Do not automatically create a new token from one isolated visual value.

# Semantic Tokens

Prefer:

```text
--color-text-primary
--color-surface-elevated
--color-action-danger
--space-4
--radius-medium
--shadow-elevated
--motion-fast
--z-modal
```

or the project's token naming convention.

Do not hardcode:

```text
#fff
#111827
12px
9999px
0 2px 10px rgba(...)
```

when a semantic token already exists.

Hardcoded values may be legitimate for:

- one-off geometry;
- mathematical alignment;
- intrinsic icon dimensions;
- runtime-calculated values;
- accepted local exception.

Record why when non-obvious.

# Token Fallbacks

Use CSS variable fallbacks only when the project has a compatibility reason.

Avoid:

```css
color: var(--color-text-primary, #111);
```

everywhere if token availability is guaranteed.

Fallbacks can hide missing theme/token configuration.

# Component Tokens

A component may define local custom properties when they are truly component-scoped.

Example:

```css
.root {
  --card-inline-padding: var(--space-4);
}
```

This can improve internal consistency.

Do not create a parallel token taxonomy inside every module.

# Theme Behavior

Prefer theme-driven variables from the project.

Example:

```css
.root {
  background: var(--color-surface-elevated);
  color: var(--color-text-primary);
}
```

Then dark/light/high-contrast themes update tokens centrally.

Avoid:

```css
:global(.dark) .root { ... }
```

if semantic theme tokens already solve it.

Use explicit theme selectors only when the component genuinely has theme-specific structural behavior not expressible through tokens.

# Theme Leakage

Do not define global theme selectors in a feature module.

If theme variables must be defined at document/app scope, move them to approved theme ownership.

# Component Theme Overrides

Local override may be valid:

```css
.danger {
  --button-background: var(--color-action-danger);
}
```

when the project primitive supports component-scoped custom properties.

Do not mutate global `:root` variables from a component module.

# Variants

Variants should reflect the accepted component contract.

Example:

```ts
variant: "primary" | "secondary" | "danger"
size: "small" | "medium" | "large"
```

CSS Module:

```css
.root {}
.primary {}
.secondary {}
.danger {}
.small {}
.medium {}
.large {}
```

Compose classes explicitly.

Do not infer variants from arbitrary boolean combinations.

# Variant Composition

Typical composition:

```ts
className={cx(
  styles.root,
  styles[variant],
  styles[size],
  loading && styles.loading,
  className
)}
```

or repository-approved equivalent.

Do not introduce a new classnames/cva library if the repository has an existing strategy.

For small cases, simple template strings/arrays may be enough.

# Composition in CSS

CSS Modules may support:

```css
.primary {
  composes: base;
}
```

depending on tooling.

Use CSS composition when it improves clarity and is supported by repository conventions.

Do not create deep composition inheritance chains.

Prefer explicit common class + variant class when easier to reason about.

# Variant Specificity

Prefer:

```css
.root {}
.danger {}
.disabled {}
```

with predictable class application.

Avoid:

```css
.root.danger.disabled:not(.loading) > div > span {}
```

when semantics can be represented by simpler classes/tokens/structure.

# State Selectors

Pseudo-classes are appropriate:

```css
.button:hover {}
.button:focus-visible {}
.button:disabled {}
.input:invalid {}
```

when they reflect native component states.

Do not replicate native disabled/focus semantics through unrelated wrapper classes unnecessarily.

# Data Attributes

Data attributes can be useful for explicit component state:

```css
.root[data-state="open"] {}
.root[data-invalid="true"] {}
```

especially when integrating primitives/design systems.

Use the project primitive's stable public attributes.

Do not target undocumented internal attributes from vendor implementations.

# ARIA Selectors

Selectors such as:

```css
.root[aria-expanded="true"] {}
```

can be legitimate when the ARIA state is already correct and stable.

Do not add ARIA only to create a styling hook.

Semantics come first.

# Runtime Dynamic Values

Inline styles or CSS custom properties are appropriate for genuine runtime values.

Examples:

```text
progress percentage
measured popover coordinate
dynamic grid column width
user-selected color when product permits
drag transform
chart segment size
```

Preferred:

```tsx
<div
  className={styles.progress}
  style={{ "--progress": `${progress}%` } as React.CSSProperties}
/>
```

CSS:

```css
.progress {
  width: var(--progress);
}
```

or direct inline style when simpler.

Do not generate dozens of runtime class names for continuous values.

# Dynamic Runtime Value Evaluation

Ask:

```text
Is the value known at build/design time?
```

If yes, prefer class/token.

If no and it changes continuously or comes from measurement/data, inline style/custom property is appropriate.

Do not flag all inline styles as architectural violations.

The standard explicitly permits inline styles for genuine runtime values.

# Runtime CSS Variable Naming

Use component-semantic names:

```text
--progress
--x
--item-size
--column-count
```

Avoid generic global-looking token names:

```text
--space-4
--color-primary
```

for runtime component variables unless they actually override an approved token intentionally.

# Inline Style Security

Do not pass untrusted strings into arbitrary CSS properties.

For user/provider values:

- constrain allowed properties;
- validate value shape;
- avoid unsafe `url(...)`/HTML-like injection contexts.

CSS values do not become safe merely because React uses a style object.

# Responsive Layout

Use the primitive that matches the problem:

```text
Flexbox
Grid
Container Queries
Viewport Media Queries
```

CSS Modules are implementation scope, not layout strategy.

Do not default to Flexbox for every layout.

# Component Context Responsiveness

Prefer container queries when behavior depends on component/container width and project/browser support allows it.

Example:

```css
.root {
  container-type: inline-size;
}

@container (min-width: 32rem) {
  .content {
    grid-template-columns: 1fr auto;
  }
}
```

Do not use viewport breakpoints for a reusable component if its layout actually depends on local container size and the project supports container queries.

# Viewport Responsiveness

Use media queries for page-level viewport behavior.

Prefer project breakpoint tokens/custom media when available.

Do not invent new breakpoints casually.

# Responsive Requirements

Layouts MUST:

- avoid unintended overflow;
- support wrapping;
- preserve essential actions;
- tolerate translation expansion;
- support zoom/text scaling;
- use logical properties where internationalization matters.

Test long content and narrow widths.

# Logical Properties

Prefer when direction/i18n matters:

```css
margin-inline-start
padding-inline
inset-inline-end
border-inline-start
```

instead of left/right-specific properties.

Do not force logical properties for mathematical left/right concepts where physical direction is intentional.

# Fixed Dimensions

Fixed dimensions require justification.

Acceptable examples:

- icon size;
- avatar size;
- control hit area;
- known media aspect box;
- canvas/chart requirement.

Avoid fixed card heights that clip translated or zoomed text.

# Overflow

Use:

```text
min-width: 0
overflow-wrap
flex-wrap
grid minmax(0, 1fr)
```

where needed.

Do not hide layout defects with:

```css
overflow: hidden;
```

unless clipping is intentional behavior.

# Typography

Use typography tokens/primitives.

Avoid copying font family/size/line-height/weight values across modules when tokens/classes exist.

Text must support zoom and content expansion.

Do not fix line heights/heights in ways that clip text.

# Spacing

Use semantic/scale tokens for repeated spacing.

One-off exact values may be valid when geometrically required.

Do not create meaningless wrapper elements solely to apply spacing if layout primitives/gap solve it.

# Gap

Prefer `gap` for spacing between flex/grid children when appropriate.

Avoid nth-child margin hacks.

# Borders / Radius / Shadow

Consume tokens where available.

Avoid feature-specific shadow/radius copies if they are design-system decisions.

Do not create visual elevation through arbitrary box shadows when a shared elevation token exists.

# Motion

Use motion tokens when available.

Respect `prefers-reduced-motion`.

Example:

```css
@media (prefers-reduced-motion: reduce) {
  .animated {
    transition: none;
  }
}
```

or project-approved reduced-motion strategy.

Do not disable all motion globally from a feature module.

# Focus Styles

Do not remove focus outlines without a visible replacement.

Use shared focus token/ring convention when available.

Avoid:

```css
outline: none;
```

unless a clear accessible focus treatment replaces it.

# Color-Only Meaning

Styles must not make status understandable only by color.

Pair color with semantic text/icon/state as required by accessibility design.

CSS implementation should preserve the accepted component semantics.

# Forced Colors / High Contrast

If project accessibility baseline requires it, ensure component styles do not break forced-colors/high-contrast behavior.

Do not override system colors unnecessarily.

# Selectors

Prefer shallow selectors.

Good:

```css
.root {}
.header {}
.title {}
.actions {}
```

Potentially acceptable:

```css
.root > svg {}
```

when structure is controlled and icon semantics are stable.

Smell:

```css
.root > div:nth-child(2) > div > span {}
```

# Deep Selector Smell

Classify:

```text
LOCAL_STRUCTURE_ACCEPTABLE
DEEP_SELECTOR_SMELL
VENDOR_BOUNDARY_SELECTOR
GLOBAL_LEAKAGE
SPECIFICITY_ESCALATION
```

A selector is suspect when it depends on:

- many ancestor/child levels;
- DOM order;
- `nth-child` for semantics;
- vendor internal markup;
- broad descendant tags;
- escalating specificity to beat previous CSS.

Fix by:

- adding semantic local class;
- using stable primitive slot API;
- wrapping through project UI;
- using tokens/variant API;
- moving third-party override to documented boundary.

# Vendor Primitive Styling

Prefer the vendor/project primitive's public API:

- className;
- slot class;
- data-state;
- CSS variables;
- variant props;
- documented selectors.

Do not target minified/internal DOM structure.

If a third-party boundary requires a deep/global selector, isolate and document it.

# Specificity

Keep specificity low and predictable.

Prefer one class.

Use state pseudo-classes/data attributes.

Avoid IDs for component styling.

Avoid chaining classes purely to win cascade.

# `!important`

`!important` is exceptional.

Valid cases may include:

- hostile third-party CSS boundary;
- unavoidable legacy override;
- approved utility contract.

Document why and keep scope narrow.

Do not use it as routine conflict resolution.

# CSS Cascade Layers

If the project already uses `@layer`, follow its architecture.

Do not introduce cascade layers from one component module without project-level policy.

# Global Leakage

A CSS Module can still leak globally through:

```text
:global
global element selectors in global files
global custom-property mutation
third-party overrides
```

Audit escapes.

Do not assume `.module.css` means every declaration is automatically harmless.

# Global Token Need

If a new semantic token is required:

```text
component implementation
→ record token need
→ token/design-system owner
```

Do not define a root-level token in a feature module.

A temporary local fallback may be acceptable only with explicit accepted deviation.

# Global Utility Need

If many modules repeat the exact non-semantic utility, consider the project's approved utility mechanism.

Do not create global utility classes from one feature without evidence.

# CSS Modules Composition Reuse

Use `composes` or shared local classes when it expresses real styling reuse.

Avoid large inheritance-like class graphs.

Shared primitives/design-system APIs are often better for cross-feature visual reuse.

# Feature-Specific Styling

Keep feature visual behavior in the owning feature.

Do not move a feature class to `shared/styles` merely because another component might use it someday.

# Shared Primitive Styling

Project shared UI primitives own stable cross-feature component styling.

Feature modules may adapt/layout primitives but should not duplicate the entire shared primitive implementation.

# External `className`

A component may accept `className` when composition requires outer layout/style adaptation.

Define whether it is supported by component API.

Do not automatically expose `className` on every shared component if project policy prefers variants/slots.

# className Ordering

When external `className` is supported, define precedence intentionally.

Example:

```ts
cx(styles.root, styles[variant], className)
```

allows caller classes later in cascade depending on bundling/specificity.

Do not depend on accidental import order for critical invariants.

# Style Prop

Avoid generic `style` escape hatches on shared primitives unless project API allows them.

For product runtime values, explicit CSS custom-property props may be safer.

Do not ban `style` universally.

# CSS Variable API

A shared component may expose documented custom properties:

```text
--progress
--dialog-max-width
--avatar-size
```

when this is an intentional styling API.

Do not make every internal custom property public.

# Media Queries

Keep component-responsive queries close to component module.

Global layout breakpoints may remain at page/layout level.

Do not duplicate the same page-level breakpoint logic across many feature modules if project primitives exist.

# Container Queries

Use stable containment boundaries.

Be mindful that containment can affect layout/size/position behavior.

Do not add `container-type` everywhere without need.

# Theme Media Queries

For system preference themes such as `prefers-color-scheme`, follow project theming strategy.

If theme is application-controlled, don't mix independent system media-query overrides inside feature modules unless policy says so.

# Reduced Motion

A component with transitions/animation should respect the project's reduced-motion baseline.

Do not create animation essential to understanding.

# Print Styles

If the product supports printing/document rendering, component print behavior may belong in module.

Do not create print rules without requirement.

# CSS Module Imports

Typical:

```ts
import styles from "./PromotionCard.module.css";
```

Use repository/tooling conventions.

Do not add type generators/plugins if build already supports modules.

# Type Safety

Some repositories generate typed CSS Module class names.

Use existing tooling if present.

Do not introduce CSS Module type-generation infrastructure as part of ordinary UI work.

# Sass/PostCSS

If `.module.scss` or PostCSS is selected, follow existing toolchain.

Do not add Sass because nesting is convenient.

Native CSS nesting may already be available depending on project support.

# Nesting

Keep nesting shallow.

Example:

```css
.root {
  &:hover {}
}
```

can be fine.

Avoid deeply nested Sass-style structures that recreate global CSS specificity problems.

# CSS Imports

Avoid feature modules importing global theme files merely to establish side effects unless project convention requires it.

Global stylesheet entrypoints should be explicit.

# Dead Styles

Remove unused classes as part of local change when safe.

Do not perform broad stylesheet cleanup without scope/evidence.

# CSS Module Testing

Component tests generally should not assert hashed CSS Module class names.

Test behavior/accessibility.

Use visual regression for pixel-sensitive styling.

Unit tests may assert explicit semantic class selection only when variant styling contract itself is under test and repository conventions support it.

# Visual Regression

Consider for:

- shared primitives;
- complex responsive layouts;
- theme variants;
- high-risk pixel-sensitive features.

Do not replace semantic/accessibility tests with screenshots.

# Storybook / Component Explorer

If the project already has a component explorer, use it for variant/theme/responsive evidence.

Do not introduce Storybook solely for this skill.

# Runtime Value Test

For runtime CSS variables, test semantic style output only if behavior depends on it.

Example:

```text
progress=70
→ --progress: 70%
```

Do not assert internal generated class hashes.

# Theme Test

Prefer visual/component-level evidence that semantic tokens produce correct theme behavior.

Do not duplicate the whole global theme token test in each component.

# Responsive Test

Use real-browser/visual testing for layout/reflow where jsdom cannot provide reliable evidence.

Do not rely solely on unit snapshots for CSS layout.

# Accessibility Test

CSS Modules implementation must not break:

- focus visibility;
- contrast;
- reflow;
- zoom;
- keyboard targets;
- reduced motion.

Automated checks do not prove full conformance.

# Component Module Evaluation

Given a component, verify:

```text
feature styles scoped
classes semantic
tokens reused
selectors shallow
responsive behavior local
global escape absent/unnecessary
```

# Global Token Need Evaluation

Given a repeated visual decision with no token:

```text
global semantic decision
→ report token need
```

Do not silently define token in component.

# Dynamic Runtime Value Evaluation

Given:

```text
progress = 37
```

prefer:

```text
CSS custom property / inline style
```

rather than 100 generated classes.

# Variant Composition Evaluation

Given explicit component variants:

```text
variant
size
disabled/loading
```

compose valid classes without contradictory boolean styling.

Do not create highly specific selectors for every compound combination when the variant model can express it cleanly.

# Deep Selector Smell Evaluation

Given:

```css
.root > div > div:nth-child(2) span {}
```

flag `DEEP_SELECTOR_SMELL`.

Prefer a semantic class/slot/stable public primitive API.

# Overmodeling Audit

Flag:

- module for a component with zero custom styling;
- local token framework;
- generic `styles/utils.module.css`;
- dozens of tiny one-class modules with no ownership value;
- CSS abstraction replicating design-system primitives;
- variant library added for one component;
- new Sass/PostCSS plugin without need.

Use:

```text
PROPORTIONATE_CSS_MODULES
UNDER_SCOPED_STYLING
OVERMODELED_CSS_MODULES
GLOBAL_STYLE_MISPLACED
STYLING_PROFILE_MISMATCH
```

# Under-Scoped Styling

Flag:

- feature class in global stylesheet;
- generic global element styling for one feature;
- feature-specific theme variable on `:root`;
- broad selector affecting sibling features;
- undocumented third-party override.

# Final Decision

Use:

```text
CSS_MODULES_UI_COMPLETE
CSS_MODULES_UI_COMPLETE_WITH_CONDITIONS
STYLING_PROFILE_MISMATCH
GLOBAL_TOKEN_CHANGE_REQUIRED
THEME_CHANGE_REQUIRED
VARIANT_DESIGN_REQUIRED
RESPONSIVE_DESIGN_REQUIRED
ACCESSIBILITY_REVIEW_REQUIRED
BLOCKED
```

## Output

Use `assets/css-modules-ui-implementation-record.md`.

## Completion Criteria

- [ ] CSS Modules is the selected/accepted styling profile for the scope.
- [ ] Feature styles are scoped.
- [ ] Global styles are limited to accepted global concerns.
- [ ] Class names describe component semantics rather than ad hoc utilities where appropriate.
- [ ] Semantic design tokens are reused for repeated visual decisions.
- [ ] New global token needs are escalated to token/design-system ownership.
- [ ] Theme behavior consumes the accepted token/theme strategy.
- [ ] Component modules do not mutate global root theme variables.
- [ ] Variant classes reflect the accepted component variant contract.
- [ ] Class composition uses existing project utilities/conventions.
- [ ] No new classnames/variant/Sass/PostCSS tooling is introduced without approval.
- [ ] Dynamic runtime values use CSS variables/inline styles when genuinely runtime.
- [ ] Inline styles are not rejected mechanically.
- [ ] Responsive layout uses Flex/Grid/container/viewport queries according to the problem.
- [ ] Layout tolerates wrapping, translations, zoom, text scaling, and supported viewports.
- [ ] Logical properties are used where i18n direction matters.
- [ ] Fixed dimensions are justified.
- [ ] Selectors remain shallow and stable.
- [ ] Deep selectors/vendor internals are avoided or isolated as documented boundary exceptions.
- [ ] Specificity escalation and routine `!important` are avoided.
- [ ] Focus/reduced-motion/accessibility styling is preserved.
- [ ] CSS Module hashes/internal classes are not over-tested.
- [ ] Visual/browser tests are used when layout/theme behavior requires real rendering evidence.
- [ ] Roadmap evaluations are covered: component module, global token need, dynamic runtime value, variant composition, deep selector smell.
- [ ] No speculative global utility/token/style framework is introduced.
- [ ] Final CSS Modules implementation status is explicit.

## References

- Read `references/css-modules-scope-and-global-boundaries.md` first.
- Read `references/tokens-themes-and-global-style-ownership.md`.
- Read `references/variants-composition-and-runtime-values.md`.
- Read `references/responsive-layout-selectors-and-specificity.md`.
- Read `references/accessibility-testing-and-visual-evidence.md`.
- Read `references/css-modules-overmodeling-and-migration-smells.md`.
- Read `references/css-modules-ui-audit.md` before completion.
