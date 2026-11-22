# CSS Modules UI Implementation Record

## Context

- Change/component:
- Repository/application:
- Selected styling profile:
- CSS Modules convention:
- Token source:
- Theme strategy:
- Responsive strategy:
- Primitive/design-system library:
- Accessibility baseline:
- Existing style utilities:
- Applicable `AGENTS.md`:
- Implemented by/date:

## Readiness

- CSS Modules selected:
- Token source known:
- Theme policy known:
- Responsive policy known:
- Variant contract known:
- Global style boundary known:
- Initial decision:
- Conditions/blockers:

## Styling Ownership

- Component-owned styles:
- Global-owned styles:
- Shared primitive-owned styles:
- Token/theme-owned decisions:
- Third-party boundary:
- Decision: PROPORTIONATE_CSS_MODULES / UNDER_SCOPED_STYLING / OVERMODELED_CSS_MODULES / GLOBAL_STYLE_MISPLACED / STYLING_PROFILE_MISMATCH

## Module Structure

- File:
- Imported by:
- Root class:
- Semantic classes:

```text

```

- Generic utility-like class names avoided:
- Unused classes:

## Global Boundary

| Style concern | Owner | Reason |
|---|---|---|
| reset/normalize | global | |
| tokens | global/design system | |
| themes | global/design system | |
| base typography | global | |
| document behavior | global | |
| feature style | module | |
| third-party override | documented boundary | |

- `:global` usages:
- Each global escape justified:
- Feature-specific globals removed:

## Design Tokens

| Visual decision | Token | Local hardcoded value needed |
|---|---|---|
| color | | |
| spacing | | |
| typography | | |
| radius | | |
| border | | |
| shadow | | |
| motion | | |
| z-index | | |
| size | | |

- Repeated hardcoded values removed:
- Missing semantic token:
- Global token change required:
- Local component custom properties:

## Theme

- Semantic variables consumed:
- Light/dark behavior:
- High-contrast/forced colors:
- Feature global theme selectors:
- `:root` mutation:
- Theme-specific structural exception:

## Variants

- Component variant contract:

```text

```

| Variant/state | CSS class/data selector | Token changes |
|---|---|---|
| | | |

- Contradictory boolean styles avoided:
- Existing `cx`/classnames utility:
- CSS `composes` used:
- Composition chain shallow:
- New variant library introduced:

## Runtime Values

| Runtime value | Source | Technique | Why runtime |
|---|---|---|---|
| | | CSS variable / inline style | |

- CSS custom-property names:
- Generated class explosion avoided:
- Untrusted CSS values constrained:

## Responsive Layout

- Layout primitive: Flexbox / Grid / Container Query / Viewport Query
- Why:
- Breakpoint/token:
- Component vs page responsiveness:
- Wrapping:
- Overflow:
- Translation expansion:
- Zoom/text scaling:
- Essential actions preserved:
- Logical properties:
- Fixed dimensions:
- Fixed-dimension justification:

## Selectors

| Selector | Classification | Action |
|---|---|---|
| | LOCAL_STRUCTURE_ACCEPTABLE / DEEP_SELECTOR_SMELL / VENDOR_BOUNDARY_SELECTOR / GLOBAL_LEAKAGE / SPECIFICITY_ESCALATION | |

- IDs used:
- `nth-child` semantics:
- Vendor internal DOM targeted:
- Stable slot/data-state API used:
- Descendant depth:

## Specificity / Cascade

- One-class baseline:
- Chained selectors:
- `!important`:
- `!important` justification:
- Cascade layer policy:
- Import-order dependency:

## Accessibility Styling

- `:focus-visible`:
- Outline removed:
- Visible replacement:
- Disabled state:
- Invalid state:
- Color-only meaning avoided:
- Contrast token:
- Reduced motion:
- Forced colors/high contrast:
- Touch target:
- Text clipping avoided:

## Shared Primitive Integration

- Project primitive used:
- Feature adaptation only:
- Primitive implementation duplicated:
- Supported class/slot/data API:
- Unsupported vendor internals avoided:

## External className / Style API

- `className` supported:
- Precedence:
- `style` supported:
- Public CSS variable API:
- Internal variables kept private:

## Roadmap Evaluation Cases

### Component Module

- Styles scoped:
- Tokens used:
- Selectors shallow:
- Global leakage:

### Global Token Need

- Repeated/global visual decision:
- Existing token:
- Missing token escalation:
- Feature-local duplicate avoided:

### Dynamic Runtime Value

- Value:
- CSS variable/inline style:
- Build-time class alternative rejected:

### Variant Composition

- Base:
- Variant:
- Size/state:
- Composition utility:
- Invalid combinations avoided:

### Deep Selector Smell

- Selector:
- Why brittle:
- Replacement:
- Vendor-boundary exception if any:

## Testing / Evidence

- Component semantic tests:
- CSS class hash assertions avoided:
- Runtime CSS variable test:
- Visual regression:
- Responsive browser evidence:
- Theme evidence:
- Accessibility evidence:
- Component explorer/story:
- No new testing tool introduced:

## Overmodeling Audit

- Zero-value module:
- Local token framework:
- generic styles/utils module:
- one-class module proliferation:
- design-system primitive duplicated:
- variant library for one component:
- new Sass/PostCSS plugin:
- global utility invented:

## Final Decision

- Decision:
- Conditions:
- Blocking issue:
- Next skill:
- Required follow-up:
