---
name: implementing-tailwind-ui
description: Implements frontend UI using the project's already-selected Tailwind conventions. Use to compose readable utility classes, consume semantic theme tokens, define explicit component variants, integrate project primitives, handle responsive/container behavior and dark/theme modes, resolve class conflicts, and decide when repeated class strings justify extraction into a component/variant abstraction. Avoid arbitrary values when an approved token exists, long duplicated class strings, conflicting utilities, undocumented theme overrides, utility strings that hide component semantics, and new class-merge/variant tooling without approval.
...
---

# Implementing Tailwind UI

## Purpose

Implement UI using Tailwind when the project has already selected Tailwind as the styling strategy for the scope.

The core flow is:

```text
component semantics
→ explicit variants / project primitive
→ Tailwind utilities
→ project theme tokens
```

Tailwind is an implementation strategy, not an architecture layer.

This skill preserves:

- semantic component APIs;
- project design tokens;
- project primitive ownership;
- accessibility;
- responsive behavior;
- readable class composition.

It avoids:

- arbitrary-value sprawl;
- duplicated class strings;
- class conflicts;
- ad hoc dark-mode overrides;
- “utility soup” that hides component intent;
- abstracting every utility into custom CSS.

## Governing Standard

Each project MUST document:

- primary styling strategy;
- design-token source;
- component primitive library;
- theming strategy;
- responsive strategy;
- accessibility baseline;
- allowed exceptions.

No universal rule prohibits Tailwind or requires it.

Repeated visual decisions SHOULD use semantic tokens.

Component variants MUST be explicit and valid.

Use a variant system appropriate to the selected stack.

Layouts MUST choose Flexbox, Grid, container queries, or viewport queries based on the problem.

Inline styles remain acceptable for genuine runtime values.

## Use When

- Tailwind is the accepted project styling profile.
- A component needs utility-first implementation.
- Long class lists are becoming unreadable.
- The same button/card utility set is repeated.
- Responsive variants need clearer behavior.
- Arbitrary values may duplicate project tokens.
- Dark/theme-mode classes need alignment with project policy.
- Tailwind class conflicts produce unexpected styling.
- Project primitives need feature-specific Tailwind composition.
- A feature needs to decide between local class extraction and shared component/variant abstraction.

## Do Not Use When

- The selected profile is CSS Modules-only.
- The selected profile is CSS-in-JS-only.
- The task is to choose the styling strategy.
- The task is to design the global token taxonomy.
- The task is to integrate headless primitives generally.
- The task is pure component-variant design independent of Tailwind.
- The component should simply consume an existing project primitive with no feature-specific Tailwind need.
- The proposed solution introduces CVA/tailwind-merge/clsx plugins without checking repository policy.

## Inputs

- Selected Tailwind profile/version.
- Existing Tailwind configuration/theme.
- Design-token source.
- Dark/theme-mode strategy.
- Responsive strategy.
- Project primitive/component library.
- Existing class-composition utility.
- Existing class-conflict/merge utility.
- Component variant contract.
- Accessibility requirements.
- Runtime dynamic-value requirements.
- Test/visual-regression strategy.
- Repository-local `AGENTS.md`.

## Outputs

- Tailwind UI implementation.
- Semantic utility composition.
- Long-class-list decision.
- Repeated-class extraction decision.
- Responsive variant design.
- Arbitrary-value/token decision.
- Dark/theme-mode implementation.
- Class-conflict resolution.
- Project primitive integration.
- Tailwind implementation record.

## Core Workflow

```text
confirm Tailwind profile
→ inspect theme/tokens/primitives
→ identify component semantics and variants
→ compose readable utilities
→ replace arbitrary values with tokens where possible
→ define responsive/theme behavior
→ resolve conflicts deterministically
→ extract repetition only when it has semantic value
→ verify accessibility and visual evidence
```

## Readiness Gate

Use one:

```text
READY_TO_IMPLEMENT_TAILWIND_UI
READY_WITH_CONDITIONS
TAILWIND_PROFILE_REQUIRED
THEME_TOKEN_SOURCE_REQUIRED
VARIANT_CONTRACT_REQUIRED
RESPONSIVE_POLICY_REQUIRED
DARK_MODE_POLICY_REQUIRED
CLASS_MERGE_POLICY_REQUIRED
BLOCKED
```

Do not assume Tailwind version, dark-mode strategy, or merge utility.

# Tailwind Profile Confirmation

Record:

```text
Tailwind version
theme source
config style
dark-mode strategy
class composition utility
class conflict strategy
primitive library
```

Examples of project-specific tooling may include:

```text
clsx
classnames
cva
tailwind-merge
twMerge
custom recipe utility
shadcn/ui conventions
```

Use only what the repository already accepts.

Do not add a tool merely because it is common in Tailwind projects.

# Tailwind Version

Respect the repository's installed Tailwind major/minor and conventions.

Do not write config or syntax from another major version blindly.

If theme tokens come from CSS variables, use the project-approved pattern.

If theme tokens come from Tailwind config/theme namespaces, use that pattern.

# Semantic Component First

Start with the component contract:

```text
variant
size
state
layout
responsive behavior
```

Then map semantics to utilities.

Do not let the raw class string become the component API.

Good:

```tsx
<Button variant="danger" size="sm" />
```

Weak:

```tsx
<Button className="bg-red-600 text-white px-3 py-1 ..." />
```

when the project already owns a semantic Button variant.

# Project Primitives First

Feature code SHOULD consume project primitives before raw vendor primitives when centralized consistency is required.

If a shared `Button` already handles:

- focus;
- disabled state;
- variant;
- size;
- theme;
- accessibility;

do not recreate it with utilities in every feature.

Feature Tailwind should adapt:

- layout;
- local width;
- spacing around primitive;
- feature-specific composition.

# Utility Classes

Use utilities directly when they remain readable and local.

Tailwind utility classes are not inherently “messy.”

Do not extract every list into a named class.

The question is:

```text
Does the utility list still reveal intent?
```

# Long Class List Evaluation

A long class list is a smell only when it harms:

- readability;
- variant reasoning;
- reuse;
- conflict detection;
- maintenance.

Possible remedies:

```text
format across lines
group by concern
extract semantic subcomponent
use existing variant utility
use shared primitive
use local class constant
```

Do not default to `@apply`.

## Long Class List Example

A class list with:

```text
layout
spacing
typography
color
border
interaction
responsive
dark mode
```

may still be valid if it is one cohesive element.

But if it repeats across several elements/components, extract the semantic abstraction.

# Formatting Long Class Lists

Use repository formatting conventions.

Possible:

```tsx
className={cn(
  "grid min-w-0 gap-4 rounded-lg border",
  "bg-surface text-foreground",
  "md:grid-cols-[1fr_auto]",
  selected && "ring-2 ring-focus"
)}
```

Avoid manual comments for every utility unless genuinely clarifying.

# Class Grouping

Conceptual grouping can aid review:

```text
layout
spacing
typography
surface
interaction
responsive
state
```

Do not rely on class order for semantic documentation when a merge tool reorders/conflict-resolves differently.

# Repeated Button Classes

If the same classes appear repeatedly, first ask:

```text
Is this actually the same semantic component?
```

If yes, prefer the project `Button` or a shared/feature component variant.

Do not create:

```text
const buttonClasses = "..."
```

in many files when the repetition represents a real component API.

# Repeated Classes Without Component Semantics

Some repeated utility sets are layout patterns, not components.

Possible solutions:

- local wrapper component;
- project utility/recipe if one exists;
- Tailwind component layer if project policy uses it;
- duplication if extraction would obscure context.

DRY is not absolute.

Do not create global abstractions for two coincidental utility strings.

# `@apply`

Use `@apply` only if the project's Tailwind strategy explicitly uses it.

It can be appropriate for:

- third-party markup boundaries;
- generated/non-React markup;
- project-specific CSS layers.

It should not be the default response to long class lists.

Avoid recreating semantic component CSS through huge `@apply` blocks when utilities/components are clearer.

# Variants

Component variants MUST be explicit and valid.

Example:

```text
variant = primary | secondary | danger
size = sm | md | lg
```

Avoid contradictory boolean props:

```text
primary
secondary
danger
```

that can all be true.

Map accepted variants to utilities with the project's variant strategy.

# Variant Strategy

Possible accepted strategies:

```text
plain conditionals
clsx/classnames
CVA
recipe utility
shared primitive variants
Tailwind plugin/component API
```

Do not introduce CVA merely because a component has variants.

If CVA is already project standard, use it.

# Variant Mapping

Keep mappings semantic.

Example:

```ts
const variants = {
  warning: "bg-warning-surface text-warning-foreground",
  success: "bg-success-surface text-success-foreground",
}
```

Better yet, use existing primitive tokens/variants when available.

Do not name variants by raw color if product semantics are stable:

```text
red
green
blue
```

unless the component API truly is a color palette.

# Compound Variants

Use compound variants only when combinations have genuinely distinct styling.

Do not create a combinatorial matrix for every possible state.

If state can be represented by ordinary utilities:

```text
disabled:opacity-50
```

keep it simple.

# Class Conflict

Tailwind class conflicts occur when multiple utilities target the same CSS property.

Example:

```text
px-2 px-4
text-sm text-lg
bg-red-500 bg-blue-500
```

Resolve intentionally.

Do not depend on source-string intuition when generated CSS order differs.

# Merge Utility

If the project uses `tailwind-merge`, `twMerge`, or an equivalent, use it at the approved abstraction boundary.

Typical:

```ts
cn = (...inputs) => twMerge(clsx(inputs))
```

when already established.

Do not introduce `tailwind-merge` automatically.

# Class Conflict Sources

Common sources:

- base + variant;
- shared primitive + caller `className`;
- responsive utility + default;
- dark mode + base;
- conditional classes;
- duplicate string fragments;
- third-party primitive classes.

Audit where precedence should be intentional.

# Caller `className`

If a component accepts `className`, decide whether callers may override internal utilities.

Possible policies:

```text
CALLER_MAY_OVERRIDE
CALLER_ADDS_LAYOUT_ONLY
CALLER_CLASSNAME_NOT_SUPPORTED
MERGED_WITH_PROJECT_POLICY
```

Do not pretend caller precedence is safe without considering conflicting utilities.

# Invariants vs Overrides

Some classes represent component invariants:

- focus treatment;
- minimum hit area;
- required display behavior;
- accessibility state.

Do not let arbitrary caller class merging silently remove critical behavior unless the component API explicitly permits it.

Prefer semantic props/slots for invariant-sensitive styling.

# Arbitrary Values

Tailwind arbitrary values are legitimate for truly exceptional/local values:

```text
w-[37px]
grid-cols-[minmax(0,1fr)_auto]
[--progress:37%]
```

They are not automatically violations.

The rule is:

```text
If an approved semantic token/utility exists, use it.
If no stable token exists and the value is genuinely local/runtime/structural, arbitrary value may be appropriate.
```

# Arbitrary Token Evaluation

Bad when project has token:

```text
bg-[#fff2f0]
```

and the theme defines:

```text
bg-warning-surface
```

Use the token.

If no warning token exists and several components need it, record a design-token need.

Do not normalize a missing design token by scattering arbitrary hex values.

# Arbitrary Structural Values

May be valid:

```text
grid-cols-[minmax(0,1fr)_auto]
```

because it is layout structure, not a design token.

May also be valid:

```text
max-w-[68ch]
```

if project lacks a semantic content-width token and the value is intentional.

Do not turn every bracket syntax into a blocker.

# Runtime Values

For runtime dynamic values, prefer:

```text
inline style
CSS custom property
style prop consumed by Tailwind arbitrary custom-property syntax
```

Example:

```tsx
<div
  style={{ "--progress": `${progress}%` } as React.CSSProperties}
  className="w-[var(--progress)]"
/>
```

or direct inline width if simpler.

Do not pre-generate utility classes for continuous runtime values.

# Theme Tokens

Tailwind utilities should map to project theme tokens.

Examples may be:

```text
bg-surface
text-foreground
border-subtle
text-danger
ring-focus
```

depending on project naming.

Do not hardcode palette utilities such as:

```text
bg-red-500
text-slate-900
```

when semantic aliases exist.

Raw palette utilities may be acceptable for genuinely decorative/non-semantic visuals if project policy allows them.

# Tailwind Palette vs Semantic Tokens

Distinguish:

```text
palette token
semantic token
```

Product UI should prefer semantic tokens for repeated meaning.

Example:

```text
danger
warning
success
surface
foreground
muted
```

rather than direct palette shade choices.

# Dark Mode

Follow the project's selected dark/theme mode strategy.

Possible:

```text
class-based `dark:`
media-based
data-theme selectors
CSS-variable semantic theme
framework/provider controlled
```

Do not invent another dark-mode mechanism in one feature.

# Dark Mode with Semantic Tokens

If semantic CSS variables already change by theme:

```text
bg-surface
text-foreground
```

may require no explicit `dark:` classes.

Avoid duplicate:

```text
bg-white dark:bg-slate-900
```

when theme tokens already express the semantic surface.

# Dark Mode Evaluation

Ask:

```text
Does the component need an explicit dark variant,
or should its semantic tokens change globally?
```

Prefer token-driven theme behavior.

Use `dark:` only where the project's convention or genuinely theme-specific component behavior requires it.

# Theme-Specific Structure

Occasionally a theme changes more than color.

Examples:

- image asset;
- shadow/elevation;
- blend mode.

Explicit dark/theme variant may be justified.

Document it.

# Responsive Variants

Tailwind responsive utilities should express accepted behavior.

Example:

```text
grid grid-cols-1 gap-4
md:grid-cols-[1fr_auto]
```

only if the breakpoint reflects page/viewport behavior.

For reusable component-context responsiveness, consider project container-query support.

Do not use `md:` simply because it is familiar.

# Responsive Variant Evaluation

Determine:

```text
viewport-driven
or
container-driven
```

Then use:

- responsive prefix;
- container query utility/plugin if project supports it;
- component primitive API.

Do not invent new breakpoint values via arbitrary syntax when an approved breakpoint exists.

# Breakpoint Tokens

Use project-configured breakpoints.

Avoid:

```text
min-[742px]:
```

when an existing semantic/project breakpoint matches the intended behavior.

Arbitrary breakpoint may be justified for a component-specific threshold if project policy permits and container query/token does not fit.

Record why.

# Layout

Use Tailwind utilities for the layout primitive that matches the problem:

```text
flex
grid
container query
block/flow
```

The earlier “always use Flexbox” rule is rejected.

Do not force one-dimensional Flexbox onto a two-dimensional layout.

# Overflow and Wrapping

Useful patterns include:

```text
min-w-0
flex-wrap
break-words
overflow-wrap
grid-cols-[minmax(0,1fr)_auto]
```

according to problem.

Do not hide content with `overflow-hidden` to mask layout defects unless truncation/clipping is intentional.

# Fixed Heights

Avoid fixed heights for text-rich cards when content may expand.

Use:

```text
min-h
auto height
flex/grid layout
```

when appropriate.

Fixed sizes are valid for icons, avatars, controls, known media, and intentional geometry.

# Logical Properties

Use Tailwind logical utilities if the project/version supports them and direction matters.

Examples may include:

```text
ms-*
me-*
ps-*
pe-*
```

depending on Tailwind version.

Do not assume syntax unsupported by the installed version.

# Typography

Prefer theme typography utilities.

Do not scatter arbitrary:

```text
text-[15px]
leading-[22px]
font-[550]
```

when theme values exist.

Arbitrary typography may be acceptable for a documented product requirement absent a token.

# Spacing

Prefer configured spacing scale.

Arbitrary:

```text
p-[13px]
gap-[11px]
```

should be questioned when standard spacing values/tokens exist.

Do not force a nearby token if the design intentionally requires an exact non-token geometry.

# Radius / Shadow / Border

Prefer theme utilities.

Avoid arbitrary shadows/radii when semantic component tokens exist.

Do not use `rounded-full` as a universal pill token when the component semantic shape differs.

# Focus

Interactive UI must preserve visible focus.

Use project focus-ring utilities/primitive behavior.

Avoid:

```text
focus:outline-none
```

unless replaced with:

```text
focus-visible:ring-...
```

or approved equivalent.

Do not remove vendor/native focus behavior without replacement.

# Disabled and Invalid

Use semantic/native states:

```text
disabled:
aria-disabled:
aria-invalid:
data-[state=...]:
```

according to primitive/API.

Do not style disabled purely by a custom `.disabled` class while semantics remain interactive.

# Data Attributes

Headless/project primitives may expose stable attributes.

Tailwind can target them:

```text
data-[state=open]:
aria-expanded:
aria-invalid:
```

when supported.

Use documented public attributes.

Do not target undocumented vendor DOM internals.

# Reduced Motion

Use project-approved motion utilities and reduced-motion variants.

Example:

```text
motion-safe:
motion-reduce:
```

when supported by project/version.

Do not make essential information depend on animation.

# High Contrast / Forced Colors

Follow project accessibility strategy.

Avoid utilities that remove system-provided contrast behavior without replacement.

# Class Duplication

Repeated classes can mean:

```text
same semantic component
same variant
same local layout pattern
coincidental styling
```

Extract only when semantics justify it.

Do not use raw string deduplication as the only criterion.

# Local Constants

A local class constant can improve readability for a one-file repeated fragment:

```ts
const actionLayout = "flex items-center gap-2";
```

Use sparingly.

If the string represents a true component variant, a component/variant abstraction is clearer.

# Shared Components

Promote to shared only when:

- multiple features genuinely share semantics;
- API is stable;
- ownership is clear;
- accessibility/theme behavior should evolve centrally.

Do not move a feature-specific Tailwind component to shared because class strings look generic.

# Feature Components

Feature-local components are a strong reuse mechanism for repeated class structures inside one capability.

Prefer them over global Tailwind utility abstractions when semantics are feature-specific.

# Tailwind Component Layer

If the project uses `@layer components`, follow existing conventions.

Do not create component-layer CSS merely to move utilities out of JSX.

The abstraction should have semantic value.

# Tailwind Utility Layer

Custom utilities belong to project-level styling ownership.

Do not invent a utility class from one feature.

# Arbitrary Properties

Tailwind arbitrary properties:

```text
[mask-image:...]
[contain:layout]
```

may be valid for unsupported CSS.

Use only when:

- real CSS feature is required;
- no built-in utility/project abstraction exists;
- browser support is accepted.

Keep them readable.

# CSS Variables

Tailwind works well with CSS custom properties.

Use project semantic variables.

For runtime values, set component-scoped variables inline and consume them through Tailwind if clear.

Do not define global theme variables in feature JSX/style.

# Primitive Integration

When using shadcn/company UI:

- preserve primitive API;
- compose feature layout around it;
- use provided variants;
- use public `className`/slot APIs;
- keep accessibility behavior intact.

Do not fork primitive class strings into feature code unless intentional customization requires it.

# Headless Primitive Integration

This skill can style already-selected headless primitives.

The broader integration/behavior contract belongs to `integrating-headless-ui-primitives`.

Do not redesign focus management/portal behavior here.

# Class Conflict with Primitives

When a caller passes:

```text
className
```

to a shared primitive, ensure merge policy is consistent.

Example conflict:

```text
primitive: px-4
caller: px-2
```

If project merge utility says caller overrides, verify that is intentional.

Do not use conflict merging to override accessibility invariants accidentally.

# Responsive Component API

Sometimes a component prop is clearer than many consumer-specific responsive classes.

Example:

```text
orientation="horizontal"
```

when orientation is semantic and owned by component.

Do not encode every product state exclusively through utility strings passed by callers.

# Class String Generation

Do not concatenate unbounded external/user values into Tailwind class names:

```ts
`bg-${color}-500`
```

Tailwind build scanning may not generate them, and untrusted values are unsafe/unpredictable.

Use explicit mappings.

# Dynamic Class Maps

Good:

```ts
const statusClass = {
  warning: "bg-warning-surface",
  success: "bg-success-surface",
}
```

Avoid runtime arbitrary utility construction from provider strings.

# Content Scanning

If classes are dynamically generated, ensure build-time scanning supports them.

Prefer explicit mappings/safelists according to project policy.

Do not add broad safelists that bloat CSS for one feature.

# Safelist

Safelist should be exceptional.

Use for:

- CMS-driven known bounded values;
- generated content with approved classes.

Do not safelist entire color/spacing matrices.

# Bundle / CSS Size

Tailwind generally generates used utilities, but arbitrary safelists/plugins can expand CSS.

Do not add giant safelists or plugins casually.

# Styling Conflicts

When two class sources conflict, classify:

```text
BASE_VS_VARIANT
VARIANT_VS_STATE
PRIMITIVE_VS_CALLER
RESPONSIVE_OVERRIDE
THEME_OVERRIDE
DUPLICATE_FRAGMENT
```

Then resolve at the semantic source.

Do not just append another utility until it “wins”.

# CSS Specificity

Tailwind utilities usually have low uniform specificity.

Problems often come from:

- external CSS;
- important modifier;
- CSS Modules/global styles;
- vendor components;
- inline styles.

Do not use Tailwind `!` important modifier routinely.

# Important Modifier

Use:

```text
!p-4
```

or global important settings only for documented exceptions.

Do not turn it into normal conflict resolution.

# Hybrid Styling Boundaries

If project explicitly mixes Tailwind with CSS Modules/design system, document ownership.

Example:

```text
design system primitives
→ semantic component styling

Tailwind
→ feature layout/composition

CSS Module
→ specialized animation/third-party boundary
```

Do not mix systems ad hoc in one element without reason.

# Dark-Mode Duplication

Avoid repeating long dark-mode class pairs when semantic tokens solve them globally.

If many components contain:

```text
bg-white text-black dark:bg-black dark:text-white
```

and project has theme tokens, migrate to semantic theme utilities within scope.

Do not redesign the entire theme from one feature task.

# Token Gap

If Tailwind config lacks a needed semantic token:

```text
record token need
→ managing-frontend-design-tokens
```

Do not encode the new system token as an arbitrary hex in every feature.

# Testing

Test semantics and user behavior, not Tailwind implementation detail.

Avoid assertions on entire class strings.

Possible targeted assertions:

- selected variant maps to expected public style contract;
- caller class conflict resolved if that is API behavior;
- runtime custom property emitted;
- dark/responsive class presence only when class behavior itself is under test.

Prefer visual/browser evidence for actual layout/theme rendering.

# Long Class List Test

Do not write tests simply because a class list is long.

Refactor readability, then test component behavior.

# Variant Test

Test variant rendering/semantics at component level.

If visual distinction is important, add visual regression.

Do not snapshot huge class strings as the primary contract.

# Responsive Test

Use real-browser/visual regression for layout.

jsdom cannot prove responsive CSS behavior.

# Dark Mode Test

Use component explorer/visual/browser test if project has one.

Verify theme token behavior rather than asserting every `dark:` class when semantic CSS variables drive theme.

# Class Conflict Test

If `className` override is a documented API, test one representative conflict.

Do not test the internals of `tailwind-merge`.

# Accessibility

Tailwind implementation must preserve:

- semantic HTML;
- visible focus;
- contrast;
- disabled/invalid semantics;
- reflow/zoom;
- reduced motion;
- non-color-only meaning;
- hit targets.

Styling utilities do not prove accessibility.

# Long Class List Evaluation

Given a long class string:

1. determine whether it is one cohesive element;
2. identify repeated semantic fragments;
3. check project primitives/variants;
4. format/group if local;
5. extract only when semantics/reuse justify.

Do not reflexively move utilities into CSS.

# Repeated Button Classes Evaluation

Given repeated button utility strings:

```text
project Button exists
→ use its variant API

no shared Button, repeated same feature meaning
→ feature Button/variant may be justified

coincidental styling
→ duplication may be acceptable
```

# Responsive Variant Evaluation

Given:

```text
md:flex-row
```

ask whether component behavior is:

```text
viewport breakpoint
or
container width
```

Use selected responsive strategy.

# Arbitrary Token Evaluation

Given:

```text
bg-[#fff2f0]
```

check theme/token source.

If semantic token exists, use it.

If missing and globally meaningful, record token gap.

If truly local/decorative one-off, arbitrary value may be accepted.

# Dark Mode Evaluation

Given:

```text
bg-white dark:bg-slate-950
```

check whether semantic theme token utilities already exist.

Prefer:

```text
bg-surface
```

when theme system owns the switch.

# Class Conflict Evaluation

Given:

```text
base: px-4
variant: px-2
caller: px-6
```

define intended precedence, then use the project's merge/composition policy.

Do not depend on accidental class concatenation.

# Overmodeling Audit

Flag:

- CVA introduced for one two-state component;
- tailwind-merge added solely to silence one conflict;
- every class list extracted into constants;
- `@apply` recreating a component library;
- global Tailwind utility abstraction for one feature;
- giant safelist;
- custom plugin for one CSS property;
- duplicate design-system primitive.

Use:

```text
PROPORTIONATE_TAILWIND_UI
UNDERMODELED_VARIANTS
OVERMODELED_TAILWIND_UI
TOKEN_GAP
STYLING_PROFILE_MISMATCH
```

# Under-Modeled Signals

Flag:

- duplicated semantic button classes across features;
- arbitrary palette values everywhere;
- raw vendor primitive classes copied into features;
- uncontrolled caller class conflicts;
- dynamic class construction from runtime strings;
- repeated dark-mode pairs despite semantic theme tokens.

# Final Decision

Use:

```text
TAILWIND_UI_COMPLETE
TAILWIND_UI_COMPLETE_WITH_CONDITIONS
STYLING_PROFILE_MISMATCH
TOKEN_CHANGE_REQUIRED
VARIANT_DESIGN_REQUIRED
RESPONSIVE_DESIGN_REQUIRED
CLASS_MERGE_POLICY_REQUIRED
ACCESSIBILITY_REVIEW_REQUIRED
BLOCKED
```

## Output

Use `assets/tailwind-ui-implementation-record.md`.

## Completion Criteria

- [ ] Tailwind is the accepted styling profile for the scope.
- [ ] Installed Tailwind version/conventions are respected.
- [ ] Project theme/token source is used.
- [ ] Project primitives are consumed before duplicating semantic controls.
- [ ] Utility classes remain readable and local.
- [ ] Long class lists are formatted/extracted only when value is clear.
- [ ] Repeated utility strings are evaluated by semantic reuse, not DRY alone.
- [ ] Existing class composition/variant utilities are reused.
- [ ] No new CVA/classnames/tailwind-merge/plugin/tool is introduced without approval.
- [ ] Component variants are explicit and valid.
- [ ] Contradictory boolean variants are avoided.
- [ ] Arbitrary values are not used when approved semantic tokens exist.
- [ ] Missing globally meaningful tokens are recorded for token ownership.
- [ ] Legitimate local/structural/runtime arbitrary values remain allowed.
- [ ] Dark/theme mode follows project policy.
- [ ] Semantic theme utilities are preferred over repeated raw light/dark palette pairs when available.
- [ ] Responsive utilities match viewport/container behavior.
- [ ] Approved breakpoints are reused.
- [ ] Layout supports wrapping, translations, zoom, reflow, and essential actions.
- [ ] Class conflicts have intentional precedence.
- [ ] Caller `className` override policy is explicit where applicable.
- [ ] Important utilities are exceptional.
- [ ] Dynamic class generation from arbitrary runtime/provider strings is avoided.
- [ ] Safelists/plugins remain bounded and justified.
- [ ] Focus, disabled, invalid, reduced-motion, contrast, and accessibility behavior are preserved.
- [ ] Tests avoid huge class-string snapshots and library-internal merge assertions.
- [ ] Real-browser/visual evidence is used for responsive/theme rendering when needed.
- [ ] Roadmap evaluations are covered: long class list, repeated button classes, responsive variant, arbitrary token, dark mode, class conflict.
- [ ] No speculative Tailwind abstraction framework is introduced.
- [ ] Final Tailwind implementation status is explicit.
