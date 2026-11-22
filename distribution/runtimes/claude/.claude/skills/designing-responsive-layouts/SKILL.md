---
name: designing-responsive-layouts
description: Designs frontend responsive layouts by choosing Flexbox, Grid, container queries, and viewport queries intentionally. Use when layouts must support small screens, reflow, zoom, translation expansion, overflow prevention, responsive dashboards, toolbars, cards, mobile tables, and container-dependent components. Preserve essential actions, use logical properties where internationalization matters, justify fixed dimensions, and select breakpoints from behavior rather than device folklore. Do not default to Flexbox for every layout, use arbitrary breakpoints without evidence, hide overflow to mask structural defects, or solve component-context responsiveness with viewport queries when container queries are the better fit.
---

# Designing Responsive Layouts

## Purpose

Design responsive layouts that remain usable across supported widths, zoom levels, translations, and content growth.

The primary decision is:

```text
What layout problem are we solving?
```

Then select:

```text
Flexbox
Grid
Container Query
Viewport Query
Normal Flow
```

Do not start with:

```text
mobile / tablet / desktop
```

or:

```text
always use Flexbox
```

The standard explicitly rejects “always use Flexbox.”

## Governing Standard

Use the layout primitive that matches the problem:

- Flexbox: one-dimensional distribution and alignment.
- Grid: two-dimensional tracks and structured layouts.
- Container queries: component-context responsiveness.
- Viewport queries: page-level responsiveness.

Layouts MUST:

- avoid unintended overflow;
- support content wrapping;
- support supported viewport sizes;
- preserve essential actions;
- tolerate translation expansion;
- support zoom and text scaling;
- use logical properties where internationalization matters.

Fixed dimensions require justification.

Accessibility requires support for zoom and reflow.

## Use When

- A dashboard needs responsive columns.
- A toolbar must preserve actions on narrow widths.
- A card changes layout based on its container.
- A data table needs a mobile strategy.
- Translated CTA text breaks a layout.
- Horizontal overflow appears at narrow width or zoom.
- Breakpoints are arbitrary or duplicated.
- Layout behavior depends on component width rather than viewport.
- Fixed widths/heights clip content.
- Flex/Grid selection is unclear.
- A page needs reflow under 200%/400% zoom.
- Logical properties matter for RTL/i18n.

## Do Not Use When

- The task is to implement Tailwind utilities only.
- The task is to implement CSS Modules only.
- The task is to manage global breakpoint tokens.
- The task is general accessibility review.
- The layout is static and has no responsive/content-growth concern.
- A shared design-system layout primitive already fully solves the problem.
- The task is visual polish with no structural layout decision.

## Inputs

- Layout purpose.
- Supported viewport/container sizes.
- Content hierarchy.
- Essential actions.
- Localization/translation requirements.
- Zoom/text-scaling target.
- Existing breakpoint/token source.
- Styling profile.
- Existing layout primitives.
- Browser support.
- Accessibility target.
- Existing screenshots/design references.
- Test/visual-regression strategy.
- Repository-local `AGENTS.md`.

## Outputs

- Layout primitive decision.
- Container-vs-viewport responsiveness decision.
- Breakpoint/threshold rationale.
- Track/flow strategy.
- Wrapping and overflow policy.
- Essential-action preservation strategy.
- Translation/zoom/reflow policy.
- Fixed-dimension audit.
- Logical-property/i18n decision.
- Mobile-table strategy.
- Responsive-layout test matrix.
- Responsive-layout design record.

## Core Workflow

```text
identify layout semantics
→ identify content growth and priority
→ choose layout primitive
→ choose container vs viewport responsiveness
→ derive thresholds from failure points
→ define wrapping/reflow
→ preserve essential actions
→ audit fixed dimensions/overflow
→ verify zoom/translations
→ define browser/visual evidence
```

## Readiness Gate

Use one:

```text
READY_TO_DESIGN_RESPONSIVE_LAYOUT
READY_WITH_CONDITIONS
RESPONSIVE_LAYOUT_NOT_REQUIRED
LAYOUT_SEMANTICS_REQUIRED
BREAKPOINT_SOURCE_REQUIRED
CONTAINER_QUERY_SUPPORT_REQUIRED
CONTENT_PRIORITY_REQUIRED
MOBILE_TABLE_POLICY_REQUIRED
BLOCKED
```

A valid outcome may be:

```text
RESPONSIVE_LAYOUT_NOT_REQUIRED
```

# Layout Primitive Selection

Use:

```text
NORMAL_FLOW
FLEXBOX
GRID
CONTAINER_QUERY
VIEWPORT_QUERY
HYBRID_LAYOUT
```

## Normal Flow

Use normal document flow when block/inline flow already solves the problem.

Do not introduce Flex/Grid unnecessarily.

Examples:

- stacked article content;
- simple label + paragraph sections;
- vertical text content.

## Flexbox

Use for one-dimensional distribution and alignment.

Examples:

```text
toolbar row
button group
header actions
icon + text
vertical stack with aligned controls
```

Flexbox is good when one axis is primary.

Do not use it for structured two-dimensional track alignment when Grid is clearer.

## Grid

Use for two-dimensional tracks and structured layouts.

Examples:

```text
dashboard cards
form label/control alignment
main + sidebar layouts
data summary matrices
card collections with track alignment
```

Grid is preferable when rows and columns matter together.

Do not simulate Grid with nested flex rows when track relationships are central.

## Container Queries

Use when the component should adapt to the space its parent gives it.

Examples:

```text
card in sidebar vs main content
widget embedded in different shells
reusable dashboard tile
shared component in split panes
```

The component's layout threshold should follow its local container.

Do not bind reusable component behavior to viewport width when its actual available width can differ substantially.

## Viewport Queries

Use for page-level responsiveness.

Examples:

```text
site navigation
overall page shell
global sidebar collapse
page-wide major layout shift
```

Viewport queries are appropriate when the whole viewport is the relevant context.

# Container vs Viewport Decision

Ask:

```text
Would this component need a different layout
at the same viewport width
when placed in a narrower/wider parent?
```

If yes:

```text
CONTAINER_QUERY
```

is likely better.

If no and the layout follows page width:

```text
VIEWPORT_QUERY
```

may be appropriate.

# Hybrid Layouts

A page can combine:

```text
viewport query for page shell
+
container query for reusable cards/widgets
```

This is often appropriate.

Do not force one responsive mechanism globally.

# Breakpoints

Breakpoints should come from layout/content failure points.

Prefer:

```text
when actions no longer fit
when columns become too narrow
when readable line lengths fail
when card content starts wrapping badly
when table no longer preserves useful scanning
```

Avoid device folklore:

```text
768 = tablet
1024 = desktop
```

unless project breakpoints intentionally encode those thresholds.

# Existing Breakpoint Tokens

Use project breakpoints/tokens when they fit the actual failure points.

If no existing threshold fits:

```text
record breakpoint/token need
```

or use a component-local container threshold if project policy allows it.

Do not invent a new global breakpoint in a feature silently.

# Breakpoint Minimalism

Use as few thresholds as necessary.

Avoid:

```text
sm md lg xl 2xl
```

all being used just because the framework exposes them.

Every layout transition should have a reason.

# Content-Driven Thresholds

Measure or inspect where the layout stops working.

Example:

```text
toolbar:
buttons + title + actions stop fitting at ~42rem
→ wrap/overflow strategy starts there
```

Do not choose 768px simply because it is common.

# Reflow

Responsive layout should reflow rather than shrink unusably.

Possible strategies:

```text
stack
wrap
move secondary actions
collapse detail
switch columns
enable horizontal region scroll
change information presentation
```

Choose based on content semantics.

Do not solve reflow by scaling entire UI smaller.

# Zoom and Text Scaling

Test with browser zoom/text scaling.

Layout should tolerate:

- larger text;
- wider labels;
- taller controls;
- changed wrapping;
- reduced effective viewport.

Avoid fixed heights and rigid rows that assume one line.

# 200% / 400% Zoom

Accessibility target may require meaningful reflow under substantial zoom.

Do not assume “responsive at 320px” automatically proves zoom support.

Real browser evidence is useful.

# Translation Expansion

Translated text may be significantly longer.

Design for:

- CTA expansion;
- button labels;
- headings;
- form labels;
- status text;
- navigation items.

Do not encode width from the English string.

# Translated CTA

A CTA must preserve:

- complete readable label;
- hit target;
- neighboring essential actions;
- priority.

Possible strategies:

```text
allow wrapping
increase container flexibility
stack actions
make secondary action move
use full-width button at narrow widths
```

Avoid truncating critical CTA text.

# Essential Actions

Essential actions must remain available.

Do not hide the primary action solely to make the layout fit.

Classify actions:

```text
PRIMARY_ESSENTIAL
SECONDARY_ESSENTIAL
OPTIONAL
OVERFLOW_CANDIDATE
```

Then design narrowing behavior intentionally.

# Toolbar Design

Toolbars are commonly one-dimensional and often Flexbox-based.

Need to decide:

```text
wrap
overflow menu
scroll
collapse labels
stack
split primary/secondary actions
```

Do not let buttons shrink below usable/readable sizes.

## Toolbar Action Priority

Example:

```text
Save → PRIMARY_ESSENTIAL
Cancel → SECONDARY_ESSENTIAL
Export → OVERFLOW_CANDIDATE
More filters → OVERFLOW_CANDIDATE
```

At narrow width, lower-priority actions may move into overflow.

Do not move essential actions unpredictably.

# Toolbar Wrap

Wrapping can be appropriate when multiple rows remain understandable.

Ensure:

- order remains logical;
- tab order remains logical;
- grouped actions remain associated;
- row gaps are sufficient.

Do not rely on DOM order changes through CSS that create confusing keyboard/visual order differences.

# Visual vs DOM Order

Avoid CSS reordering that substantially diverges from DOM/tab order.

Use DOM order aligned with reading/interaction priority.

`order` can be used sparingly for cosmetic changes, but accessibility impact must be reviewed.

# Dashboard Grid

Dashboard cards often suit Grid.

Potential strategy:

```text
repeat(auto-fit, minmax(...))
```

or explicit tracks according to product needs.

Do not choose auto-fit blindly if card order/track widths have stronger requirements.

## Dashboard Card Minimum Width

A minimum width should be based on:

- readable content;
- control fit;
- chart legibility;
- action fit.

Do not pick arbitrary card widths solely from a screenshot.

# Unequal Card Content

Grid rows should not force fixed card heights if content varies.

Use natural height unless visual alignment genuinely requires equal-height behavior.

Avoid clipping translated/zoomed content to maintain perfect grid symmetry.

# Card Layout

Cards may use:

```text
Grid
Flexbox
normal flow
container query
```

depending on internal content.

Reusable cards often benefit from container queries.

Example:

```text
narrow:
content stacked
actions full width

wide:
content + actions side-by-side
```

# Card Fixed Height

Fixed heights are suspect for text-rich cards.

Use:

```text
min-height
auto height
content-driven sizing
```

unless the card contains fixed-ratio media or a verified equal-height requirement.

# Mobile Table

A table needs a semantic mobile strategy.

Options:

```text
horizontal scroll
priority-column hiding
responsive card/list transformation
stacked definition layout
condensed table
separate mobile representation
```

No one strategy is universally correct.

# Horizontal Scroll Table

Use when tabular comparison relationships matter.

Requirements:

- horizontal scroll is discoverable;
- table semantics remain;
- sticky key column/header may help;
- essential columns remain identifiable;
- no page-level horizontal overflow.

Do not wrap every cell into unreadable multi-line blocks if comparison is primary.

# Priority Columns

Hiding columns may be appropriate if non-essential.

Document:

```text
which columns can hide
why
where hidden information remains accessible
```

Do not hide critical information.

# Table-to-Cards

Transform to cards/list when row-oriented reading is more important than cross-column comparison.

Ensure labels remain visible:

```text
Status: Active
Plan: Pro
Renewal: 12 Sep
```

Do not show values without headers after transformation.

# Separate Mobile Representation

A separate component may be justified if semantics/layout differ substantially.

Avoid duplicate business/data logic.

Both representations should consume the same Application/view data.

# Overflow

Distinguish:

```text
INTENTIONAL_LOCAL_SCROLL
UNINTENDED_COMPONENT_OVERFLOW
UNINTENDED_PAGE_OVERFLOW
TEXT_OVERFLOW
MEDIA_OVERFLOW
```

Do not fix all overflow with `overflow: hidden`.

# Overflow Regression

When overflow appears:

1. identify the overflowing element;
2. inspect min-content sizing;
3. inspect fixed widths;
4. inspect non-wrapping text;
5. inspect flex/grid min-width;
6. inspect absolute positioning;
7. inspect transforms;
8. inspect long URLs/IDs;
9. inspect intrinsic media width.

Fix the structural cause.

# `min-width: 0`

In Flex/Grid children, intrinsic min-content sizing often causes overflow.

`min-width: 0` may be the correct fix.

Use intentionally.

Do not add it everywhere without understanding the constraint.

# Grid `minmax(0, 1fr)`

For flexible grid tracks containing long content, prefer:

```text
minmax(0, 1fr)
```

when default min-content behavior causes overflow.

Do not use `1fr` blindly when content may refuse to shrink.

# Long Unbroken Content

Plan for:

- URLs;
- IDs;
- email;
- generated codes;
- file names.

Use:

```text
overflow-wrap:anywhere
word-break
truncate with accessible full value when allowed
scroll
```

according to semantics.

Do not truncate critical content without access to full value.

# Media Overflow

Images/video/canvas should respect container bounds.

Typical:

```text
max-inline-size: 100%
height: auto
```

according to content.

Charts/canvas may need dedicated responsive sizing logic.

# Absolute Positioning

Absolute positioning can create overflow/reflow failures.

Use for true overlays/decoration.

Do not use it for core page layout when normal flow/Grid/Flexbox can solve the structure.

# Fixed Positioning

Fixed/sticky UI must consider:

- mobile viewport;
- safe areas;
- zoom;
- on-screen keyboard;
- content obstruction.

Do not let sticky toolbars cover essential content.

# Safe Areas

For mobile/fullscreen contexts, consider safe-area insets when relevant.

Use project tokens/utilities if available.

Do not add global safe-area behavior from one feature without policy.

# Logical Properties

Use logical properties where internationalization matters.

Prefer concepts like:

```text
inline-start
inline-end
block-start
block-end
```

over physical left/right when direction should mirror.

# RTL

Responsive design must remain valid in RTL if supported.

Check:

- action order;
- icon placement;
- margins/padding;
- sticky columns;
- scroll affordance;
- chevrons/directional icons.

Do not assume LTR.

# Writing Modes

Most projects target horizontal writing modes.

Do not overengineer vertical writing-mode support without requirement.

Logical properties still improve RTL resilience.

# Width Constraints

Use:

```text
max-width
min-width
clamp
minmax
fit-content
max-content
```

intentionally.

Do not set `width: 100%` on every element without considering intrinsic/layout behavior.

# `clamp()`

Useful for fluid values:

```text
font size
spacing
container width
```

when project strategy supports fluid design.

Do not use clamp for every dimension.

# Fluid vs Breakpoint

Choose:

```text
fluid interpolation
```

when gradual scaling makes sense.

Choose:

```text
breakpoint state change
```

when layout structure changes discretely.

# Content Width

Readable text may need a max line length.

Do not stretch body text across ultra-wide dashboards just because space exists.

# Main + Sidebar

Grid often suits:

```text
main minmax(0, 1fr)
sidebar fixed/minmax
```

At narrow widths:

```text
stack
collapse
drawer
```

according to product semantics.

# Sidebar Width

Avoid rigid sidebar width if content can expand substantially.

Use min/max constraints.

# Forms

Responsive forms should preserve:

- label/control association;
- readable inputs;
- error messages;
- actions;
- keyboard order.

Grid may align labels/controls on wider layouts and stack on narrow layouts.

Do not put labels in fixed-width columns that clip translations.

# Form Action Row

Primary and secondary actions should wrap/stack appropriately.

Avoid right-aligned action rows that push primary action offscreen.

# Navigation

Navigation responsive behavior is page-level and often viewport-driven.

Potential:

```text
horizontal nav
→ menu/drawer
```

Need keyboard/focus behavior from accessible primitives.

Do not solve nav collapse purely with CSS if interaction model changes.

# Content Priority

Responsive changes should preserve information priority.

Classify regions:

```text
ESSENTIAL
IMPORTANT
SUPPORTING
OPTIONAL
```

Use priority to decide stacking/hiding/overflow.

Do not hide based only on visual convenience.

# Hidden Content

If content is hidden at a breakpoint, verify:

- it is truly optional;
- equivalent access exists if needed;
- hidden state does not trap focus;
- DOM remains semantically correct.

Do not visually hide focusable content while leaving it focusable.

# Scroll Regions

Local scroll regions may be appropriate.

Ensure:

- keyboard access;
- visible scroll affordance;
- focus visibility;
- nested scroll is not excessive;
- page itself does not unintentionally scroll horizontally.

# Sticky Headers/Columns

Useful for long tables.

Need to verify:

- stacking/layering;
- zoom;
- RTL;
- horizontal scroll;
- screen reader semantics unaffected.

Do not freeze so many columns that little content remains visible.

# Container Naming

Container queries may use named containers if project convention supports it.

Keep names semantic:

```text
card
sidebar
dashboard-panel
```

Avoid implementation names:

```text
container1
wrapper2
```

# Container Query Thresholds

Thresholds should come from component content failure points.

Example:

```text
Card actions fit beside content above 34rem
→ container threshold around that behavior
```

Do not copy global viewport breakpoints into container queries automatically.

# Container Units

Units like `cqw` may be useful if browser support/project policy allows.

Do not introduce advanced units without clear value and compatibility.

# Layout Tokens

Breakpoints/gaps/max widths may have tokens.

Use approved token source.

This skill can identify:

```text
BREAKPOINT_TOKEN_GAP
LAYOUT_TOKEN_GAP
```

but should not redesign token taxonomy.

# Fixed Dimension Audit

Classify each fixed dimension:

```text
JUSTIFIED_FIXED_SIZE
CONTENT_RISK
MEDIA_RATIO
CONTROL_SIZE
DECORATIVE
REMOVE_OR_RELAX
```

Examples justified:

- icon;
- avatar;
- touch target;
- media frame;
- graph canvas with responsive wrapper.

Text-rich card height is usually risky.

# Min/Max Constraints

Often prefer:

```text
min-height
max-width
minmax
clamp
```

over exact fixed width/height.

# Aspect Ratio

Use aspect-ratio for media/card media regions where ratio matters.

Do not use fixed height + width when aspect-ratio expresses intent better.

# Breakpoint Naming

If project uses:

```text
sm/md/lg
```

map them to actual tokens.

Do not describe behavior as “tablet” if the breakpoint really means “toolbar has room.”

# Testing Strategy

Responsive layout needs real rendering evidence.

Use:

```text
browser/component test
visual regression
E2E for critical responsive journey
manual exploratory at boundaries
```

according to project strategy.

jsdom cannot prove layout/reflow.

# Boundary Width Testing

Test:

```text
just below threshold
at threshold
just above threshold
```

for important layout transitions.

Do not only test common device presets.

# Content Stress Testing

Use:

- longest supported translation;
- long user names;
- long IDs;
- empty content;
- dense content;
- large text;
- 200%/400% zoom;
- narrow containers.

Do not rely only on ideal mock text.

# Overflow Test

Verify:

```text
document scrollWidth <= viewport width
```

where page-level horizontal overflow should not exist.

For intentional local table scroll, scope the assertion to page vs local region.

# Dashboard Grid Evaluation

Must determine:

- Grid vs Flex;
- minimum card width;
- auto-fit vs explicit tracks;
- narrow stacking;
- variable card heights;
- content/translation stress;
- local card container responsiveness.

# Toolbar Evaluation

Must determine:

- action priority;
- wrap/overflow/stack strategy;
- primary action preservation;
- DOM/tab order;
- translation expansion;
- zoom behavior.

# Card Evaluation

Must determine:

- local container vs viewport responsiveness;
- fixed height risk;
- content wrapping;
- action placement;
- long labels;
- image/media behavior.

# Mobile Table Evaluation

Must choose among:

```text
horizontal scroll
priority columns
table-to-cards
separate mobile representation
```

based on whether comparison or row reading is primary.

# Translated CTA Evaluation

Must verify:

- complete label;
- wrap/stack;
- no clipping;
- action priority;
- no reliance on English width;
- zoom.

# Overflow Regression Evaluation

Must identify root cause rather than hide overflow.

Common fixes may include:

```text
min-width: 0
minmax(0, 1fr)
wrapping
relaxed fixed width
media constraints
logical layout correction
```

# Accessibility

Responsive layout is accessibility behavior.

Must preserve:

- zoom/reflow;
- keyboard order;
- focus visibility;
- readable text;
- essential actions;
- no hidden focusable content;
- sufficient control sizes;
- meaningful reading order.

# DOM Order

Visual layout changes must not create a reading order that conflicts with DOM order.

Use source order aligned with semantic priority.

# Touch Targets

At narrow layouts, do not shrink controls below usable touch targets simply to fit more actions.

Project accessibility baseline may recommend 44×44 CSS px as a strong default.

# Reduced Motion

Responsive transitions/animations should respect reduced motion if used.

Do not animate major layout shifts unnecessarily.

# Performance

Avoid layout strategies that require high-frequency JS measurement when CSS Grid/Flex/container queries can solve the problem.

Prefer CSS-native responsiveness.

Use JS measurement only when behavior cannot be expressed reliably in CSS.

# ResizeObserver

May be justified for true runtime measurement.

Do not use ResizeObserver to recreate container queries where browser/project support already exists.

# JS Breakpoint Hooks

Avoid:

```text
useWindowWidth
useMediaQuery
```

for styling-only responsive layout when CSS can handle it.

Use JS breakpoints only when component behavior/rendered data must truly change in JavaScript.

# CSS vs JS Responsibility

Prefer CSS for:

- layout;
- wrapping;
- visibility when purely presentational;
- track changes.

Use JS for:

- behavior changes;
- expensive data changes;
- component mounting decisions with semantic/performance reasons.

Do not duplicate the same breakpoint logic independently in CSS and JS without a shared policy.

# Server Rendering

CSS-responsive layouts work before hydration.

Avoid JS-only viewport branching that causes SSR/hydration mismatch unless framework strategy supports it.

# Overmodeling Audit

Flag:

- device-specific layout variants with no content rationale;
- many arbitrary breakpoints;
- JS ResizeObserver replacing CSS container queries;
- nested wrappers only to force layout;
- separate mobile component duplicating logic when CSS reflow suffices;
- universal layout abstraction for one feature.

Use:

```text
PROPORTIONATE_RESPONSIVE_LAYOUT
UNDERMODELED_RESPONSIVENESS
OVERMODELED_RESPONSIVENESS
OVERFLOW_RISK
BREAKPOINT_TOKEN_GAP
RESPONSIVE_LAYOUT_NOT_REQUIRED
```

# Under-Modeled Signals

Flag:

- fixed height clipping translations;
- primary action disappears;
- table creates page overflow;
- card depends on viewport despite narrow container;
- toolbar actions shrink unreadably;
- breakpoint copied without rationale;
- zoom causes overlap;
- RTL breaks spacing/order.

# Final Decision

Use:

```text
RESPONSIVE_LAYOUT_READY
RESPONSIVE_LAYOUT_READY_WITH_CONDITIONS
RESPONSIVE_LAYOUT_NOT_REQUIRED
BREAKPOINT_TOKEN_CHANGE_REQUIRED
MOBILE_TABLE_STRATEGY_REQUIRED
CONTENT_PRIORITY_REQUIRED
ACCESSIBILITY_REVIEW_REQUIRED
REAL_BROWSER_EVIDENCE_REQUIRED
BLOCKED
```

## Output

Use `assets/responsive-layout-design-record.md`.

## Completion Criteria

- [ ] Layout semantics are explicit.
- [ ] Flexbox/Grid/normal flow is chosen based on dimensional needs.
- [ ] Container vs viewport responsiveness is explicitly decided.
- [ ] Breakpoints/thresholds come from content/layout failure points.
- [ ] Existing breakpoint/layout tokens are reused where appropriate.
- [ ] New global breakpoint needs are escalated rather than silently invented.
- [ ] The layout uses the minimum necessary thresholds.
- [ ] Content wraps/reflows instead of shrinking unusably.
- [ ] Essential actions remain available.
- [ ] Toolbar action priority is explicit where relevant.
- [ ] Dashboard tracks/card minimums are content-driven.
- [ ] Reusable cards use container-context responsiveness when appropriate.
- [ ] Mobile table strategy preserves the relevant data-reading model.
- [ ] Translated CTA/text expansion is supported.
- [ ] Zoom and text scaling are supported.
- [ ] Fixed dimensions are justified or relaxed.
- [ ] `min-width: 0`, `minmax(0, 1fr)`, wrapping, and overflow fixes are used intentionally.
- [ ] Unintended page overflow is eliminated structurally rather than hidden.
- [ ] Local intentional scroll regions are explicit.
- [ ] Logical properties are used where internationalization/RTL matters.
- [ ] Visual reordering does not create DOM/keyboard order conflicts.
- [ ] Hidden responsive content is non-essential or equivalently accessible.
- [ ] Touch targets remain usable.
- [ ] CSS-native responsiveness is preferred over JS measurement where possible.
- [ ] SSR/hydration is not broken by styling-only viewport logic.
- [ ] Real-browser/visual evidence covers layout transitions and stress cases.
- [ ] Tests use boundary widths, translations, zoom, and overflow stress where relevant.
- [ ] Roadmap evaluations are covered: dashboard grid, toolbar, card, mobile table, translated CTA, overflow regression.
- [ ] No speculative layout framework or breakpoint system is introduced.
- [ ] Final responsive-layout decision is explicit.

## References

- Read `references/layout-primitive-and-container-vs-viewport.md` first.
- Read `references/breakpoints-content-priority-and-reflow.md`.
- Read `references/dashboard-toolbar-card-and-table-patterns.md`.
- Read `references/translation-zoom-rtl-and-fixed-dimension-audit.md`.
- Read `references/overflow-root-causes-and-structural-fixes.md`.
- Read `references/testing-browser-evidence-and-overmodeling.md`.
- Read `references/responsive-layout-design-audit.md` before completion.
