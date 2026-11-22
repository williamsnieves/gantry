---
name: integrating-headless-ui-primitives
description: Integrates accessible headless UI primitives such as Radix UI, Base UI, React Aria, Headless UI, or similar libraries into the project's shared UI and feature layers. Use to preserve keyboard interaction, focus management, ARIA semantics, disabled/invalid behavior, portals, dismissal, layering, and vendor state contracts while applying project tokens and variants. Decide when a vendor primitive should be wrapped in shared UI, when direct feature use is acceptable, and how to customize styling without breaking accessibility. Do not reimplement vendor behavior ad hoc, remove ARIA/focus logic, target undocumented internal DOM, mix business rules into shared primitives, or create wrappers that only rename vendor props without project-level value.
...
---

# Integrating Headless UI Primitives

## Purpose

Integrate proven accessible primitives into the frontend without weakening their behavior.

Typical providers include:

```text
Radix UI
Base UI
React Aria
Headless UI
shadcn/ui
company/vendor headless primitives
native HTML primitives
```

The core goal is:

```text
vendor accessibility/interaction contract
→ project shared UI boundary
→ project tokens/variants
→ feature usage
```

Wrappers MUST preserve accessibility and vendor behavior.

Business logic MUST NOT live in shared UI primitives.

## Governing Standard

Reusable UI primitives SHOULD live in an intentional shared UI boundary:

```text
shared/infrastructure/ui/
shared/ui/
packages/ui/
```

Feature code SHOULD consume project primitives before raw vendor primitives when centralized consistency is required.

Shared UI may wrap:

- Radix UI;
- Base UI;
- React Aria;
- shadcn/ui;
- a company design system;
- native HTML primitives.

Interactive UI MUST:

- use semantic HTML where possible;
- support keyboard interaction;
- expose an accessible name;
- preserve visible focus;
- communicate disabled and invalid states;
- avoid color-only meaning;
- maintain contrast;
- support zoom/reflow;
- respect reduced motion;
- preserve library-provided ARIA and focus management.

Modals, menus, comboboxes, tooltips, and similar complex widgets SHOULD use proven accessible primitives rather than ad hoc behavior.

## Use When

- A headless primitive must be adopted into project UI.
- A raw vendor primitive is used directly across many features.
- Project tokens/variants need to style a headless primitive.
- Keyboard/focus behavior is being accidentally overridden.
- Portals need layering/z-index ownership.
- Dialog/menu/combobox/tooltip/tabs behavior needs safe customization.
- Vendor accessibility behavior is being “simplified.”
- A feature needs to decide direct vendor usage vs shared wrapper.
- A wrapper needs a stable project-facing API.
- A primitive needs integration with CSS Modules or Tailwind.

## Do Not Use When

- The task is to select a styling strategy.
- The task is general component variant design.
- The task is generic accessibility review unrelated to a primitive.
- The component is a simple native element that does not need a headless library.
- The project primitive already fully satisfies the feature requirement.
- The proposed wrapper only renames vendor props and adds no project value.
- The proposed component contains business rules or feature-specific data orchestration.

## Inputs

- Selected headless/vendor primitive.
- Project shared UI boundary.
- Styling profile.
- Design-token source.
- Variant strategy.
- Accessibility target.
- Portal/layering strategy.
- Focus-management requirements.
- Keyboard interaction requirements.
- Error/disabled/invalid semantics.
- Server/client runtime.
- Existing wrapper conventions.
- Test strategy.
- Repository-local `AGENTS.md`.

## Outputs

- Primitive integration decision.
- Direct-vendor vs project-wrapper decision.
- Stable project-facing API.
- Accessibility preservation checklist.
- Keyboard/focus behavior contract.
- Portal/layering design.
- Token/variant mapping.
- Styling-boundary decision.
- Vendor override audit.
- Primitive test matrix.
- Headless primitive integration record.

## Core Workflow

```text
identify primitive behavior
→ inspect vendor accessibility contract
→ decide wrapper/direct use
→ define project API
→ preserve keyboard/focus/ARIA behavior
→ apply project tokens/variants
→ define portal/layering behavior
→ isolate vendor-specific details
→ test with real interaction semantics
```

## Readiness Gate

Use one:

```text
READY_TO_INTEGRATE_HEADLESS_PRIMITIVE
READY_WITH_CONDITIONS
PROJECT_PRIMITIVE_ALREADY_EXISTS
WRAPPER_DECISION_REQUIRED
ACCESSIBILITY_CONTRACT_REQUIRED
PORTAL_POLICY_REQUIRED
STYLING_BOUNDARY_REQUIRED
VENDOR_API_REQUIRED
BLOCKED
```

# Wrapper Decision

Use:

```text
PROJECT_WRAPPER_JUSTIFIED
DIRECT_VENDOR_USE_ACCEPTED
PROJECT_PRIMITIVE_ALREADY_EXISTS
WRAPPER_IS_CEREMONIAL
SHARED_UI_BOUNDARY_REQUIRED
```

A project wrapper is justified when it provides one or more:

- project token/variant contract;
- standardized accessibility baseline;
- consistent portal/layering behavior;
- consistent sizing/spacing;
- stable API across vendor changes;
- company design-system semantics;
- controlled vendor import boundary;
- shared testing/evidence;
- migration seam.

A wrapper is ceremonial when it only does:

```tsx
export const Dialog = VendorDialog
```

or renames props one-to-one with no project semantics.

# Vendor Import Boundary

If project policy centralizes primitives, prefer:

```text
feature
→ project UI primitive
→ vendor primitive
```

rather than:

```text
feature A → Radix Dialog
feature B → Headless UI Dialog
feature C → custom modal
```

Do not mix competing primitive implementations without a documented boundary.

# Shared UI Ownership

Shared UI owns:

- stable primitive API;
- project variants;
- token mapping;
- accessibility-preserving defaults;
- portal/layering conventions;
- visual states;
- vendor adaptation.

Shared UI does NOT own:

- payment logic;
- promotion eligibility;
- feature-specific async orchestration;
- repository calls;
- feature-specific business validation.

# Feature-Specific Components

A feature may compose a shared primitive:

```text
shared Dialog
→ DeleteAccountDialog
→ feature hook / Use Case
```

The shared Dialog should not know what deleting an account means.

# Direct Vendor Use

Direct vendor use may be acceptable when:

- project policy allows it;
- usage is isolated;
- no shared project contract is needed;
- wrapper adds no value;
- migration consistency is not a concern.

Document the exception.

Do not create a wrapper merely to satisfy architectural symmetry.

# Native HTML First

For simple controls, prefer native HTML when it already provides correct behavior.

Examples:

```text
button
input
select (when native select UX is acceptable)
details/summary
dialog when project/browser policy accepts it
```

Do not use a headless library for every simple interaction.

# Dialog

Dialog integration must preserve:

- semantic dialog role/element;
- accessible name;
- focus entry;
- focus trap/containment when appropriate;
- Escape dismissal when allowed;
- focus restoration;
- background interaction prevention;
- portal behavior;
- scroll lock if vendor owns it;
- inert/aria-hidden behavior if vendor owns it.

Do not remove focus management because it conflicts with visual layout.

# Dialog Naming

Every modal dialog needs an accessible name.

Preferred project API may require:

```text
title
aria-label
aria-labelledby
```

depending on primitive.

Do not visually hide/remove title semantics without an equivalent accessible name.

# Dialog Description

Use description when useful.

Do not add meaningless descriptions solely to silence library warnings.

# Dialog Dismissal

Define:

```text
ESCAPE_ALLOWED
OUTSIDE_POINTER_ALLOWED
EXPLICIT_ACTION_ONLY
```

according to product behavior.

Use vendor-supported APIs to control dismissal.

Do not intercept global keyboard events manually if the primitive already handles Escape.

# Dialog Focus Restoration

On close, focus should normally return to the trigger or another intentional logical target.

Do not always focus `body` or top of page.

If trigger disappears after action, define a valid fallback.

# Dialog Scroll Lock

Preserve vendor/project scroll-lock behavior.

Do not add a second body-lock implementation unless policy requires it.

Double scroll lock can create layout bugs.

# Select / Combobox

Distinguish:

```text
native select
custom select
autocomplete combobox
searchable listbox
```

They have different interaction models.

Do not call every popup option control a “select” and implement arbitrary keyboard behavior.

# Combobox Behavior

A combobox may require:

- input semantics;
- popup listbox;
- active descendant/focus management;
- arrow navigation;
- Escape;
- Enter selection;
- Home/End where expected;
- typeahead/search;
- disabled options;
- empty state.

Use vendor behavior rather than rebuilding.

# Select Behavior

Custom select should preserve:

- trigger accessible name;
- open/close keyboard;
- option navigation;
- selected state;
- disabled state;
- focus restoration;
- correct popup role semantics.

Do not replace vendor roles with generic `div`.

# Controlled vs Uncontrolled

Use the primitive's supported controlled/uncontrolled APIs.

Controlled state is justified when feature logic needs ownership.

Uncontrolled may be simpler for purely local behavior.

Do not mirror vendor internal state into another local state unless needed.

# Value Semantics

Project wrapper may map vendor string values to stable component value types.

Avoid leaking vendor event objects into feature APIs.

Good:

```text
onValueChange(value)
```

Weak:

```text
onVendorSelect(event, internalItem)
```

unless vendor semantics are intentionally public.

# Tooltip

Tooltip integration must preserve:

- trigger semantics;
- hover/focus behavior;
- dismissal;
- delay policy;
- Escape when relevant;
- non-essential nature.

Tooltips must not contain critical information inaccessible elsewhere.

Do not put interactive controls inside a tooltip unless the primitive explicitly supports an interactive popover instead.

# Tooltip on Touch

Hover-only behavior is insufficient for touch.

Use project/vendor behavior consistent with accessibility strategy.

If content is essential, do not rely solely on tooltip discovery.

# Tooltip Trigger Wrapping

Avoid wrappers that break button semantics or pointer/focus behavior.

Use vendor `asChild`/slot/trigger APIs correctly when provided.

Do not create extra `<span>` wrappers without checking semantics.

# Menu

Menu integration should preserve:

- menu/menuitem semantics;
- arrow-key navigation;
- Home/End where supported;
- Escape dismissal;
- typeahead;
- disabled items;
- focus placement/restoration;
- submenu behavior when applicable.

Do not use menu primitives for ordinary navigation lists when links/list semantics are more appropriate.

# Menu vs Popover

Use menu when choices are command-like.

Use popover/dialog/listbox when content semantics differ.

Do not select a primitive based only on visual appearance.

# Menu Items

Command items should expose semantic actions.

Navigation items may be links.

Do not put arbitrary form layouts inside menuitem roles.

# Tabs

Tabs must preserve:

- tablist;
- tab;
- tabpanel;
- selected state;
- keyboard navigation;
- focus behavior;
- relationships via IDs/ARIA;
- activation mode.

Do not manually hide panels in a way that breaks vendor associations.

# Tabs Activation

Activation may be:

```text
automatic
manual
```

depending on primitive/project behavior.

Preserve vendor semantics unless product requirement explicitly differs.

# Tabs URL State

Feature code may synchronize selected tab with URL.

Do not move routing logic into the shared Tabs primitive.

Shared Tabs should remain UI-only.

# Keyboard Contract

Do not override keydown behavior without understanding the vendor's keyboard contract.

Common keys:

```text
Tab
Shift+Tab
Escape
Enter
Space
Arrow keys
Home
End
PageUp/PageDown
```

depending on widget.

If feature adds a shortcut, ensure it does not conflict with primitive navigation.

# Focus Management

Treat focus as functional behavior.

Preserve:

- initial focus;
- active item;
- focus trap/containment;
- return focus;
- focus-visible styles;
- roving tabindex/aria-activedescendant as vendor-defined.

Do not “simplify” by moving focus to arbitrary wrappers.

# ARIA Preservation

Do not delete vendor-generated:

```text
role
aria-expanded
aria-controls
aria-selected
aria-activedescendant
aria-labelledby
aria-describedby
aria-disabled
```

unless replacing them with an equivalent correct semantic contract.

Do not add duplicate/conflicting ARIA.

# Vendor Accessibility Override

Any override to vendor accessibility behavior requires explicit review.

Classify:

```text
ACCESSIBILITY_PRESERVING_CONFIGURATION
ACCESSIBILITY_NEUTRAL_OVERRIDE
ACCESSIBILITY_RISK_REQUIRES_REVIEW
ACCESSIBILITY_REGRESSION
```

Examples of risky override:

- disabling focus trap;
- removing aria-labelledby;
- suppressing Escape without product reason;
- making disabled item focusable/clickable inconsistently;
- overriding role;
- hiding title from accessibility tree;
- forcing focus to body on close.

# Vendor Warnings

Do not silence accessibility warnings by removing semantics.

Understand what contract the vendor expects.

If warning is incompatible with product behavior, document the alternative accessible implementation.

# Styling

Headless primitives should use the selected project styling profile.

Possible:

```text
CSS Modules
Tailwind
company design system
hybrid with explicit boundary
```

Do not introduce a second styling system just for the primitive.

# Token Mapping

Apply project semantic tokens to:

- surfaces;
- text;
- borders;
- focus ring;
- shadows;
- radius;
- motion;
- layering;
- spacing.

Avoid raw vendor defaults if project primitives require design-system consistency.

# Variant Mapping

Project wrapper may define variants:

```text
size
tone
density
placement
```

when stable and reusable.

Do not expose every vendor prop as a project variant.

Keep the project API smaller than or equal to the meaningful supported surface.

# Data Attributes

Headless libraries often expose stable state attributes:

```text
data-state
data-disabled
data-highlighted
data-side
data-orientation
```

Use documented public attributes for styling.

Do not target internal DOM indexes/classes.

# CSS Modules Integration

CSS Modules may style vendor slots via:

- className;
- slot class APIs;
- documented data attributes;
- isolated `:global` only when unavoidable.

Do not use deep selectors against vendor DOM.

# Tailwind Integration

Tailwind may use:

```text
data-[state=open]:
aria-selected:
data-[disabled]:
```

when public attributes are stable.

Do not use unbounded dynamic classes from vendor runtime values.

# `asChild` / Slot APIs

Some libraries support `asChild` or slot composition.

Use it only when child semantics remain correct.

Do not render:

```text
button semantics
→ div child
```

through `asChild` unless the resulting element still fulfills required behavior.

# Ref Forwarding

Primitive wrappers may need refs.

Follow vendor/project React-version conventions.

Do not add ref forwarding ceremony when not required.

When ref is part of project public API, preserve its semantic target.

# Event Composition

Vendor primitives may attach event handlers.

When project wrapper adds handlers, compose rather than accidentally replace vendor behavior.

Check whether vendor utility/API handles event composition.

Do not call `preventDefault()` casually; it may disable dismissal/focus logic.

# `preventDefault`

Use only when product behavior intentionally overrides default/vendor action.

Document why.

Examples:

- prevent outside dismissal for destructive confirmation;
- keep menu open after multi-select action if primitive supports it.

Do not use it to work around unrelated state bugs.

# Disabled State

Preserve both behavior and semantics.

A disabled option/item/control should not remain actionable through keyboard/pointer.

Use vendor-supported disabled prop/state.

Do not style something gray while leaving it operational.

# Invalid State

Use:

```text
aria-invalid
error association
describedby
```

according to project form/accessibility strategy.

Do not invent invalid semantics inside a generic primitive unless the primitive contract owns them.

# Portal

Portals move overlay content outside normal DOM hierarchy.

Define project portal ownership.

Possible:

```text
document.body
app overlay root
shadow root boundary
custom container
```

Use vendor-supported portal container APIs.

Do not manually append DOM nodes outside React unless project architecture requires it.

# Portal Layering

Portals require explicit layering semantics.

Use project z-index/layer tokens:

```text
dropdown
popover
tooltip
modal
toast
```

or project equivalent.

Do not scatter:

```text
z-[9999]
z-index: 2147483647
```

to win stacking conflicts.

# Layering Model

Define semantic layers.

Example:

```text
base content
sticky/navigation
dropdown/popover
modal backdrop
modal content
tooltip
toast/system overlay
```

Exact ordering is project-specific.

Do not invent a new scale inside one component.

# Stacking Context

Portal content can still interact with:

- transforms;
- isolation;
- iframe boundaries;
- shadow DOM;
- nested portals.

Diagnose actual stacking context before increasing z-index.

# Nested Overlays

Examples:

```text
dialog → combobox
dialog → tooltip
popover → menu
```

Ensure:

- correct portal container;
- focus containment remains valid;
- Escape closes the intended layer;
- outside-click does not close parent incorrectly;
- z-index ordering is correct.

Do not globally stop propagation to “fix” nested overlays.

# Escape Ordering

Nested overlays should close topmost relevant layer first according to vendor/project behavior.

Do not install competing document-level Escape handlers.

# Outside Pointer Interaction

Use primitive-supported dismissal callbacks/config.

Avoid global click listeners.

For nested overlays, verify parent/child outside-interaction semantics.

# Body Scroll / Inert

Dialog vendors may manage:

- scroll lock;
- inert;
- aria-hidden.

Do not add competing implementations.

If vendor behavior is disabled, accessibility impact requires review.

# SSR

Some primitives are client-only because they rely on DOM/portals.

In Next.js/RSC-style environments, keep client boundaries explicit.

Do not import DOM-dependent primitive modules into server-only components if library/runtime does not support it.

# Hydration

Avoid server/client markup mismatches caused by:

- random IDs outside stable mechanism;
- client-only portal assumptions;
- conditional primitive tree differences;
- uncontrolled defaults that differ server/client.

Use vendor SSR guidance/project patterns.

# ID Stability

Many accessible primitives generate IDs.

Preserve vendor ID management.

Do not manually generate random IDs during render to “fix” ARIA links.

# Controlled Open State

When open state is feature-owned, ensure state transitions reflect vendor callbacks.

Do not create:

```text
vendor open state
+
duplicate local derived open state
```

# Business Rules

Shared primitives must remain business-agnostic.

Bad:

```text
PromotionDialog
inside packages/ui
```

if it knows campaign/business rules.

Better:

```text
packages/ui/Dialog
feature/PromotionDialog
```

The feature component composes shared primitive with business content.

# Feature Policy vs Primitive API

Feature-specific rules such as:

```text
cannot close while payment processing
```

belong in feature composition.

They may configure shared Dialog behavior through a generic prop such as:

```text
dismissible={false}
```

if that prop is broadly valid.

Do not encode payment-specific props in shared Dialog.

# Project API Design

A project wrapper should simplify and stabilize common usage.

Good project API may expose:

```text
Dialog
DialogTrigger
DialogContent
DialogTitle
DialogDescription
```

or a higher-level:

```text
Modal
```

depending on project conventions.

Do not hide essential composition flexibility if many use cases need it.

# High-Level vs Low-Level Wrapper

Choose:

```text
LOW_LEVEL_PROJECT_PRIMITIVE
HIGH_LEVEL_PROJECT_COMPONENT
BOTH
```

only if project semantics require it.

Example:

```text
Dialog primitives
+
ConfirmDialog
```

can coexist.

Do not make one giant `Modal` with dozens of unrelated boolean props.

# Prop Surface Restraint

Expose only meaningful stable props.

Avoid blindly re-exporting entire vendor prop types through public project API if vendor lock-in/migration is a concern.

But do not wrap every vendor prop into new names solely to hide the vendor.

Balance migration value and maintenance cost.

# Vendor Types

Vendor types may remain inside shared UI.

Features should prefer project-facing types when centralized boundary is required.

Do not leak vendor-specific event/context types into Domain/Application.

# Version Upgrades

Project wrappers can reduce upgrade impact.

When vendor API changes:

```text
update wrapper
→ preserve project API when sensible
```

Do not preserve broken legacy semantics forever if vendor/accessibility contract improved and project behavior should change.

# Vendor Defaults

Prefer vendor accessible defaults.

Override only when product/project behavior requires it.

Do not disable features because they seem visually unnecessary without checking keyboard/accessibility impact.

# Tooltip Delay

A shared tooltip wrapper may standardize delay.

Do not choose arbitrary timing if project primitive already defines it.

# Menu Placement

Placement/side/align may be project API if stable.

Avoid feature code depending on vendor collision-strategy internals unless needed.

# Collision Detection

Use vendor collision/positioning system.

Do not reimplement popper/floating calculations manually.

# Scrollable Popups

Combobox/select/menu content must remain keyboard usable when scrollable.

Ensure active option visibility behavior is preserved.

Do not hide scrollbars in ways that impede usability without project policy.

# Virtualized Lists

If huge combobox/menu lists require virtualization, verify compatibility with:

- active descendant;
- keyboard focus;
- item registration;
- scroll-to-active.

Do not add virtualization blindly; it can break accessibility contracts.

# Dialog Evaluation

Must verify:

- accessible name;
- keyboard opening/closing;
- focus containment;
- focus restoration;
- backdrop/outside behavior;
- portal;
- layer token;
- nested overlay behavior.

# Select / Combobox Evaluation

Must verify:

- correct widget choice;
- trigger/input name;
- arrow keyboard behavior;
- option semantics;
- selected/disabled state;
- popup focus;
- empty state;
- portal/layer behavior.

# Tooltip Evaluation

Must verify:

- focus + hover discoverability;
- non-critical content;
- dismissal;
- trigger semantics;
- no interactive content masquerading as tooltip.

# Menu Evaluation

Must verify:

- command vs navigation semantics;
- arrow navigation;
- Escape;
- typeahead where expected;
- disabled items;
- focus restoration;
- nested submenu behavior if used.

# Tabs Evaluation

Must verify:

- tablist/tab/tabpanel;
- selected state;
- keyboard;
- focus;
- activation mode;
- URL sync remains outside shared primitive.

# Vendor Accessibility Override Evaluation

Given any override, record:

```text
what vendor behavior changes
why
accessibility impact
evidence
fallback
```

Reject regressions.

# Portal Layering Evaluation

Verify:

- semantic layer token;
- correct portal container;
- nested overlays;
- stacking contexts;
- Escape ordering;
- outside-interaction semantics;
- no arbitrary z-index escalation.

# Testing Strategy

Test user-observable primitive behavior.

Prefer:

- keyboard interaction;
- focus assertions;
- accessible roles/names;
- open/close behavior;
- disabled behavior;
- selection;
- portal rendering;
- nested overlay interactions.

Do not assert vendor-private DOM structure.

# Real Browser Evidence

Some behavior benefits from real-browser tests:

- focus trapping;
- portal layering;
- collision/positioning;
- scroll lock;
- touch interactions;
- nested overlays.

jsdom may not prove layout/positioning.

Use Playwright/E2E/component-browser tests according to project strategy.

# Accessibility Queries

Use role/name-based queries.

Examples:

```text
getByRole("dialog", { name: ... })
getByRole("combobox", { name: ... })
getByRole("menu")
getByRole("tab", { selected: true })
```

Do not select by vendor class names.

# Focus Tests

Test:

```text
open
→ intended focus

Tab/Shift+Tab
→ contained/expected sequence

close
→ logical return focus
```

where appropriate.

Do not test internal focus-manager implementation details.

# Portal Tests

Portal content may render outside the local container.

Use the document/root scope expected by test library.

Do not force portals inline solely to make tests easier unless project test strategy explicitly does so and separate integration tests cover real behavior.

# Visual Evidence

Use visual regression for:

- tokens/theme;
- overlay layering;
- responsive popup width;
- nested modal/popover composition;
- high-risk design-system primitive changes.

Do not use screenshots as a substitute for keyboard/accessibility tests.

# Overmodeling Audit

Flag:

- wrapper per every vendor primitive with no project value;
- prop-by-prop vendor renaming;
- giant “UIAdapter” abstraction;
- business-specific shared primitive;
- duplicated focus/keyboard logic on top of vendor;
- custom portal system when vendor/project portal works;
- custom position engine;
- multiple competing primitive libraries in same role.

Use:

```text
PROPORTIONATE_PRIMITIVE_INTEGRATION
UNDERWRAPPED_VENDOR_USAGE
CEREMONIAL_WRAPPER
ACCESSIBILITY_REGRESSION
PORTAL_LAYERING_RISK
PRIMITIVE_LIBRARY_MISMATCH
```

# Under-Wrapping Signals

A shared wrapper may be missing when:

- features import raw vendor primitives inconsistently;
- each feature chooses different default focus/dismissal behavior;
- z-index values diverge;
- tokens/variants are repeated;
- vendor imports are intended to be centralized by policy.

# Final Decision

Use:

```text
HEADLESS_PRIMITIVE_INTEGRATION_READY
HEADLESS_PRIMITIVE_INTEGRATION_READY_WITH_CONDITIONS
PROJECT_PRIMITIVE_ALREADY_EXISTS
DIRECT_VENDOR_USE_ACCEPTED
WRAPPER_REQUIRED
ACCESSIBILITY_REVIEW_REQUIRED
PORTAL_POLICY_REQUIRED
STYLING_BOUNDARY_REQUIRED
BLOCKED
```

## Output

Use `assets/headless-ui-primitive-integration-record.md`.

## Completion Criteria

- [ ] Primitive/vendor choice is already accepted for the scope.
- [ ] Direct-vendor vs project-wrapper decision is explicit.
- [ ] Wrapper adds real project value or is omitted.
- [ ] Shared UI remains business-agnostic.
- [ ] Feature code consumes project primitives when centralized consistency is required.
- [ ] Native HTML is preferred where it already solves the problem.
- [ ] Vendor keyboard interaction is preserved.
- [ ] Vendor focus management is preserved.
- [ ] Vendor ARIA relationships are preserved.
- [ ] Accessible names/descriptions remain correct.
- [ ] Disabled/invalid semantics remain functional, not merely visual.
- [ ] Dialog focus entry/trap/restoration/dismissal behavior is explicit.
- [ ] Select/Combobox uses the correct interaction pattern.
- [ ] Tooltip content is non-critical and trigger behavior remains accessible.
- [ ] Menu semantics match command/navigation behavior.
- [ ] Tabs preserve tablist/tab/tabpanel relationships and keyboard model.
- [ ] Vendor accessibility overrides are explicitly reviewed and non-regressive.
- [ ] Project styling profile/tokens/variants are applied without targeting vendor internals.
- [ ] Public data attributes/slots are used instead of deep DOM selectors.
- [ ] Portal container and semantic layering are explicit.
- [ ] Arbitrary z-index escalation is avoided.
- [ ] Nested overlays preserve focus, Escape, outside interaction, and ordering.
- [ ] Server/client/SSR boundaries are safe for DOM-dependent primitives.
- [ ] Tests use roles/names/keyboard/focus rather than vendor-private DOM.
- [ ] Real-browser evidence is used for focus/positioning/layering where appropriate.
- [ ] Roadmap evaluations are covered: Dialog, Select/Combobox, Tooltip, Menu, Tabs, vendor accessibility override, portal layering.
- [ ] No new primitive library, portal system, positioning engine, or wrapper framework is introduced without approval.
- [ ] Final primitive integration status is explicit.
