# Headless UI Primitive Integration Record

## Context

- Change/component:
- Repository/application:
- Vendor primitive:
- Project shared UI boundary:
- Styling profile:
- Token source:
- Variant strategy:
- Accessibility target:
- Portal/layer strategy:
- Framework/runtime:
- Existing wrapper:
- Applicable `AGENTS.md`:
- Integrated by/date:

## Readiness

- Primitive/vendor accepted:
- Wrapper policy known:
- Accessibility contract known:
- Styling boundary known:
- Portal policy known:
- SSR/client boundary known:
- Initial decision:
- Conditions/blockers:

## Integration Decision

- Decision: PROJECT_WRAPPER_JUSTIFIED / DIRECT_VENDOR_USE_ACCEPTED / PROJECT_PRIMITIVE_ALREADY_EXISTS / WRAPPER_IS_CEREMONIAL / SHARED_UI_BOUNDARY_REQUIRED
- Why:
- Project value:
- Migration value:
- Token/variant value:
- Accessibility consistency:
- Portal consistency:
- Wrapper ceremony risk:

## Ownership

| Concern | Owner |
|---|---|
| keyboard/focus base behavior | vendor/project primitive |
| project tokens/variants | shared UI |
| feature business behavior | feature |
| provider data | Infrastructure/Application |
| routing | feature/Presentation |
| portal layer policy | project UI/design system |

## Public Project API

```text

```

- Stable project props:
- Vendor props intentionally exposed:
- Vendor props intentionally hidden:
- Vendor event types leaked:
- Business-specific props excluded:

## Accessibility Contract

- Accessible role:
- Accessible name:
- Description:
- Keyboard model:
- Focus entry:
- Focus movement:
- Focus restoration:
- Disabled semantics:
- Invalid semantics:
- Visible focus:
- Reduced motion:
- Zoom/reflow:

## Vendor ARIA Preservation

| Attribute/relationship | Vendor provides | Override | Safe |
|---|---|---|---|
| role | | | |
| aria-expanded | | | |
| aria-controls | | | |
| aria-selected | | | |
| aria-activedescendant | | | |
| aria-labelledby | | | |
| aria-describedby | | | |
| aria-disabled | | | |

- Duplicate/conflicting ARIA:

## Dialog

- Applicable:
- Role/element:
- Name source:
- Description:
- Initial focus:
- Focus containment:
- Escape: ESCAPE_ALLOWED / EXPLICIT_ACTION_ONLY / custom
- Outside pointer: allowed / blocked / conditional
- Focus restoration:
- Trigger fallback:
- Scroll lock:
- Inert/aria-hidden:
- Portal:
- Nested overlay behavior:

## Select / Combobox

- Applicable:
- Widget type: native select / custom select / combobox / searchable listbox
- Trigger/input accessible name:
- Popup role:
- Option role/state:
- Arrow navigation:
- Enter/Space:
- Escape:
- Home/End:
- Typeahead/search:
- Disabled options:
- Empty state:
- Controlled/uncontrolled:
- Value mapping:
- Portal/layer:

## Tooltip

- Applicable:
- Trigger:
- Focus behavior:
- Hover behavior:
- Touch consideration:
- Dismissal:
- Escape:
- Content critical:
- Interactive content:
- Popover alternative needed:

## Menu

- Applicable:
- Command vs navigation:
- Menu/menuitem semantics:
- Arrow navigation:
- Home/End:
- Escape:
- Typeahead:
- Disabled items:
- Links:
- Submenus:
- Focus restoration:

## Tabs

- Applicable:
- tablist:
- tab:
- tabpanel:
- selected state:
- keyboard:
- activation: automatic / manual
- focus:
- IDs/relationships:
- URL state owner:

## Vendor Accessibility Override

- Override present:
- Vendor behavior changed:
- Why:
- Classification: ACCESSIBILITY_PRESERVING_CONFIGURATION / ACCESSIBILITY_NEUTRAL_OVERRIDE / ACCESSIBILITY_RISK_REQUIRES_REVIEW / ACCESSIBILITY_REGRESSION
- Evidence:
- Alternative:
- Final decision:

## Styling

- Project styling profile:
- Tokens:
- Variants:
- Vendor defaults replaced:
- Public data attributes/slots:
- Deep selectors:
- Vendor internals targeted:
- New styling system introduced:

## Theme / State Mapping

| Vendor state | Public attribute/API | Project token/variant |
|---|---|---|
| open | | |
| closed | | |
| highlighted | | |
| selected | | |
| disabled | | |
| invalid | | |
| side/orientation | | |

## Portal

- Portal root/container:
- Vendor portal API:
- Custom portal system introduced:
- Server/client implications:
- Shadow/iframe boundary:

## Portal Layering

| Layer | Semantic token | Relative order |
|---|---|---|
| dropdown/popover | | |
| modal backdrop | | |
| modal content | | |
| tooltip | | |
| toast/system overlay | | |

- Arbitrary z-index:
- Stacking context issue:
- Root cause diagnosed:

## Nested Overlays

- Scenarios:
- Topmost Escape behavior:
- Parent/child outside interaction:
- Focus containment:
- Portal container compatibility:
- z-index ordering:
- Global event propagation hacks avoided:

## SSR / Client Boundary

- DOM-dependent:
- Server-safe import:
- Client boundary:
- Stable IDs:
- Hydration:
- Portal hydration:
- Nonserializable values:
- Request/user state:

## Feature Composition

- Shared primitive:
- Feature wrapper/component:
- Business logic location:
- Routing location:
- Async/server-state owner:
- Shared primitive remains business-agnostic:

## Roadmap Evaluation Cases

### Dialog
- Decision:
- Evidence:

### Select / Combobox
- Decision:
- Evidence:

### Tooltip
- Decision:
- Evidence:

### Menu
- Decision:
- Evidence:

### Tabs
- Decision:
- Evidence:

### Vendor Accessibility Override
- Decision:
- Evidence:

### Portal Layering
- Decision:
- Evidence:

## Testing

| Behavior | Test boundary |
|---|---|
| role/name | component |
| keyboard | component/browser |
| focus entry/restoration | browser/component |
| disabled/selection | component |
| portal render | component/browser |
| nested overlay Escape | browser |
| layering/positioning | visual/browser |
| theme/variants | visual/component |

- Vendor-private DOM assertions avoided:
- Role/name queries:
- Real-browser evidence:
- Visual regression:
- No new test framework introduced:

## Overmodeling Audit

- Wrapper with no project value:
- Prop-by-prop vendor renaming:
- Giant UIAdapter:
- Business-specific shared primitive:
- Duplicate focus/keyboard logic:
- Custom portal system:
- Custom position engine:
- Competing primitive libraries:
- Decision: PROPORTIONATE_PRIMITIVE_INTEGRATION / UNDERWRAPPED_VENDOR_USAGE / CEREMONIAL_WRAPPER / ACCESSIBILITY_REGRESSION / PORTAL_LAYERING_RISK / PRIMITIVE_LIBRARY_MISMATCH

## Final Decision

- Decision:
- Conditions:
- Blocking issue:
- Next skill:
- Required follow-up:
