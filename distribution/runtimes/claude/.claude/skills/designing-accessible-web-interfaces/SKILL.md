---
name: designing-accessible-web-interfaces
description: Designs accessible web interfaces independently of framework using WCAG 2.2 and the Perceivable, Operable, Understandable, and Robust principles. Use before implementing or changing pages, components, forms, navigation, dialogs, menus, comboboxes, dynamic status, authentication, drag interactions, media, or other web UI. Define semantic HTML, accessible names and relationships, keyboard and pointer behavior, focus management, status communication, contrast, reflow, motion, target size, timing, error prevention, assistive-technology compatibility, conformance target, and verification evidence. Add React, Vue, Angular, Web Components, or native-web adaptations only after the framework-neutral contract is defined. Do not claim WCAG conformance from automated scans alone, replace native semantics with unnecessary ARIA, invent legal requirements, assume every AAA criterion, implement code, or accept inaccessible custom widgets without an equivalent accessible path.
---

# Designing Accessible Web Interfaces

## Purpose

Design the accessibility contract for one web interface before implementation.

The contract is framework-independent and defines:

```text
content and information
→ semantic structure
→ interaction model
→ visual and non-visual presentation
→ state and status communication
→ assistive-technology compatibility
→ verification evidence
```

The primary standard is WCAG 2.2, organized under:

```text
Perceivable
Operable
Understandable
Robust
```

## Default Target

Use:

```text
WCAG 2.2 Level AA
```

as the default engineering baseline unless an explicit organizational, contractual, product, or legal requirement selects another target.

Level AA includes all applicable Level A and Level AA success criteria.

Do not:

- claim formal conformance from a design record;
- claim conformance because axe or another scanner reports no violations;
- invent jurisdiction-specific legal obligations;
- assume every Level AAA criterion;
- treat advisory techniques as mandatory success criteria.

## Use When

- Designing a new page, component, view, or interaction.
- Changing semantics, layout, navigation, focus, status, or error behavior.
- Designing forms, authentication, validation, and recovery.
- Designing dialogs, menus, tabs, listboxes, comboboxes, trees, grids, tooltips, carousels, or date pickers.
- Adding drag-and-drop, gestures, timing, motion, auto-updating content, media, charts, or canvas.
- Wrapping native, design-system, or headless primitives.
- Defining responsive, zoom, contrast, target-size, or reduced-motion behavior.
- Writing accessibility acceptance criteria and verification evidence.
- Creating a reusable accessibility contract for several frameworks.

## Do Not Use When

- The task is to audit an already implemented interface.
- The task is to write framework code or CSS.
- Product behavior is too incomplete to determine semantics.
- The request is legal advice about accessibility obligations.
- The task is native mobile without a web surface.
- The request is only to run an automated scanner.
- The task is backend-only.

## Inputs

- Accepted behavior and content.
- User journeys and states.
- Target conformance level.
- Organizational accessibility policy.
- Supported browsers and assistive technologies.
- Content, media, language, and localization requirements.
- Design-system or primitive contracts.
- Responsive and theme requirements.
- Framework and rendering model, when selected.
- Existing exceptions.
- Test and review tooling.
- Applicable `AGENTS.md`.

## Outputs

- Scope and conformance target.
- User-impact inventory.
- WCAG 2.2 applicability matrix.
- Semantic structure.
- Accessible-name and relationship design.
- Keyboard and pointer interaction model.
- Focus-management contract.
- Status and error communication.
- Visual, responsive, zoom, motion, and target-size requirements.
- Complex-widget and primitive decision.
- Framework adaptation notes.
- Verification matrix.
- Exceptions and residual risks.
- Accessible web-interface design record.

## Workflow

```text
accepted behavior
→ identify users, journeys, content, and states
→ map applicable WCAG criteria
→ choose native semantics and relationships
→ define keyboard, pointer, focus, and status behavior
→ define visual and responsive accessibility
→ select proven primitives for complex widgets
→ add framework adaptation
→ define automated and manual evidence
```

## Readiness Gate

Use one:

```text
READY_TO_DESIGN_ACCESSIBLE_INTERFACE
READY_WITH_CONDITIONS
CONTENT_OR_BEHAVIOR_REQUIRED
CONFORMANCE_TARGET_REQUIRED
INTERACTION_PATTERN_REQUIRED
DESIGN_SYSTEM_ACCESSIBILITY_DECISION_REQUIRED
MEDIA_ALTERNATIVE_REQUIRED
LEGAL_OR_POLICY_CLARIFICATION_REQUIRED
BLOCKED
```

Stop when an essential interaction has no keyboard or equivalent path, critical content alternatives are undefined, or the accepted design conflicts with the target without an approved decision.

## WCAG Applicability Matrix

For every relevant criterion record:

- number and name;
- level;
- applicability;
- user impact;
- design decision;
- implementation owner;
- automated evidence;
- manual evidence;
- assistive-technology evidence.

Use:

```text
APPLICABLE
NOT_APPLICABLE
APPLICABLE_WITH_CONDITIONS
REQUIRES_CONTENT_DECISION
REQUIRES_PRODUCT_DECISION
REQUIRES_TECHNICAL_VALIDATION
```

Tooling limitations do not make a criterion non-applicable.

# Principle 1 — Perceivable

## Text Alternatives

Define alternatives for:

- informative images;
- functional icons;
- decorative content;
- complex graphics and charts;
- CAPTCHA;
- canvas or custom graphics.

Functional icons use an action-based name.

Bad:

```text
Magnifying glass
```

Preferred:

```text
Search
```

Decorative content must be ignored by assistive technology.

## Time-Based Media

When media exists, determine applicable:

- captions;
- audio description;
- transcript;
- media alternative;
- live captions;
- controls;
- autoplay behavior.

Do not invent media requirements when no media exists.

## Adaptable Structure

Define:

- document language;
- page title;
- headings;
- landmarks;
- lists;
- tables;
- form labels and groups;
- programmatic relationships;
- meaningful DOM and reading order;
- instructions independent of color, shape, sound, or visual position.

Visual order and programmatic order should align.

## Distinguishable Content

Define:

- text contrast;
- non-text contrast;
- color-independent meaning;
- text resize;
- reflow;
- text spacing;
- hover/focus content;
- themes;
- forced colors or high contrast where supported.

Do not communicate error, success, selection, or required state through color alone.

## Reflow and Zoom

At supported viewport and zoom conditions:

- essential content remains reachable;
- content does not overlap or clip;
- focus is not obscured;
- controls remain usable;
- unintended horizontal scrolling is avoided, except for content that genuinely requires two-dimensional layout.

Account for long translations, tables, editors, charts, sticky regions, and large text.

## Hover or Focus Content

Tooltip, popover, and supplemental content must be appropriately:

- dismissible;
- hoverable;
- persistent;
- keyboard accessible;
- available on touch or through an equivalent path.

Essential information cannot exist only on hover.

# Principle 2 — Operable

## Keyboard

Every applicable function needs a keyboard-operable path.

Define:

- tab order;
- activation keys;
- composite-widget arrow keys;
- Escape behavior;
- Enter/Space behavior;
- no keyboard trap;
- pointer and gesture alternatives.

Adding `tabindex="0"` to a `div` does not create a button.

## Native Interaction First

Prefer:

- `button` for actions;
- `a` for navigation;
- native form controls;
- semantic lists and tables;
- native disclosure patterns where suitable.

ARIA does not add missing keyboard behavior.

## Focus

Define:

- initial focus;
- logical focus order;
- visible focus;
- focus after validation;
- focus after deletion or navigation;
- focus containment for modal contexts;
- focus restoration;
- focus not obscured by sticky or overlay UI;
- no unexpected focus loss.

Avoid positive tabindex.

## Timing and Auto-Updating Content

When applicable define:

- warning and extension;
- pause, stop, or hide;
- preservation of input;
- auto-rotation control;
- update frequency;
- recovery.

## Motion and Flashing

Define:

- flash safety;
- reduced-motion behavior;
- pause/stop controls;
- non-motion alternatives;
- essential versus decorative motion.

## Navigation

Define:

- bypass/skip mechanisms;
- meaningful page titles;
- logical headings and labels;
- link purpose;
- consistent navigation;
- consistent identification;
- consistent help.

## Input Modalities

Define accessible alternatives and behavior for:

- multipoint or path gestures;
- dragging;
- motion actuation;
- pointer cancellation;
- label in name;
- target size;
- concurrent input methods.

Drag-only interaction is unacceptable when an equivalent non-drag path can be provided.

# Principle 3 — Understandable

## Readable and Predictable

Define:

- document and passage language;
- clear terminology;
- predictable focus behavior;
- predictable input behavior;
- consistent navigation;
- consistent components;
- consistent help.

Focus or input should not trigger unexpected context changes without warning.

## Labels and Instructions

Controls need:

- visible labels when appropriate;
- accessible names;
- descriptions;
- required state;
- format instructions;
- input purpose/autocomplete where applicable.

Placeholder text is not a replacement for a label.

## Errors

Errors must:

- identify the field or operation;
- use text, not color alone;
- be programmatically associated;
- remain available until resolved;
- preserve valid user data;
- provide suggestions when appropriate;
- support an error summary for complex forms;
- avoid exposing raw technical details.

Separate:

```text
input-shape validation
business-rule rejection
system failure
```

## Error Prevention

For consequential actions, assess:

- review;
- confirmation;
- reversibility;
- correction;
- undo;
- data verification.

Do not add confirmation mechanically to every minor action.

## Accessible Authentication

Define:

- password-manager support;
- paste support;
- MFA code behavior;
- accessible alternatives to puzzles;
- timeout and recovery;
- understandable errors.

Do not block password paste without a strong accepted reason.

# Principle 4 — Robust

## Semantic HTML

Define correct:

- element;
- accessible name;
- role;
- value;
- state;
- property;
- description;
- relationship;
- group;
- status semantics.

Avoid conflicting roles on native controls.

## Name, Role, Value

Every custom control must expose and maintain:

- name;
- role;
- current value/state;
- state changes;
- available actions;
- keyboard and focus behavior.

When this recreates extensive native behavior, reconsider the custom control.

## Status Messages

Important changes that do not move focus must be programmatically available.

Examples:

- loading;
- save success;
- validation result;
- search result count;
- cart update;
- upload progress;
- unavailable/retry state.

Choose semantics deliberately:

```text
status
alert
progressbar
log
timer
```

Do not make every message assertive.

## ARIA

Follow:

```text
native semantics first
ARIA only when needed
valid role/state/property combinations
no redundant or conflicting ARIA
```

ARIA cannot repair an incoherent interaction model.

## Dynamic Content

Define:

- whether focus remains or moves;
- what is announced;
- loading and busy states;
- retained data;
- stale and partial content;
- insertion and removal;
- modal and overlay behavior;
- virtualized content.

Avoid excessive announcements.

# Complex Widgets

Decision order:

```text
native element
→ existing accessible design-system component
→ proven headless primitive
→ custom widget with complete specification
```

## Dialog

Define:

- label and description;
- initial focus;
- focus containment;
- close method;
- Escape behavior when appropriate;
- background inertness;
- focus restoration;
- destructive-action behavior;
- scrolling.

## Menu

Use menu semantics for application-style commands, not normal navigation by default.

Define trigger, expanded state, arrow navigation, Home/End, Escape, typeahead, disabled items, and focus return.

## Combobox

Define editable/select-only mode, label, popup relationship, expanded state, active option, keyboard behavior, filtering, no-results/loading, selection, and Escape.

## Tabs

Define tablist, tab, and tabpanel relationships; arrow behavior; automatic or manual activation; focus order; selected state; and lazy content.

## Tooltip and Popover

A tooltip supplements rather than replaces an essential visible label.

Interactive content normally needs popover or dialog behavior, not tooltip semantics.

## Tables and Grids

Use native tables for tabular data.

Add grid semantics only for a truly interactive grid with a complete keyboard model.

## Drag and Drop

Define:

- non-drag alternative;
- selection;
- destination;
- status announcement;
- cancellation;
- undo;
- focus preservation;
- pointer/touch behavior.

## Charts, Canvas, and SVG

Define:

- text alternative;
- summary or data table;
- non-color distinctions;
- keyboard interaction when interactive;
- contrast;
- zoom;
- detailed description when needed.

# Visual and Responsive Accessibility

Define:

- rendered contrast;
- visible focus;
- non-color meaning;
- light/dark themes;
- forced colors;
- text resizing;
- text spacing;
- zoom/reflow;
- reduced motion;
- touch target behavior;
- localization expansion;
- bidirectional layouts where relevant.

Token names are not proof that rendered combinations pass.

# Framework-Neutral First

The core contract must not depend on React hooks, Vue directives, Angular templates, or one testing library.

Define semantics and behavior first, then adapt.

## React Adaptation

Consider:

- portals and focus restoration;
- conditional rendering and announcement timing;
- refs for focus;
- Effects only for genuine synchronization;
- server/client boundaries;
- hydration;
- stable IDs;
- Strict Mode;
- wrapper components;
- React Testing Library semantics.

## Vue Adaptation

Consider templates, teleports, focus after updates, generated IDs, composables, directives, and wrappers.

## Angular Adaptation

Consider templates, CDK accessibility primitives, overlays, focus management, live announcer, forms, and change-detection timing.

## Web Components Adaptation

Consider shadow DOM, label relationships, form-associated custom elements, focus delegation, `ElementInternals`, slots, and support across the accepted AT matrix.

## Server-Rendered HTML Adaptation

Consider valid initial semantics, progressive enhancement, hydration consistency, enhanced-navigation focus, and server-side error summaries.

# Design-System and Primitive Integration

For every reused primitive verify:

- semantics;
- name;
- keyboard behavior;
- focus behavior;
- state attributes;
- status communication;
- disabled behavior;
- contrast and themes;
- wrapper preservation;
- version-specific behavior.

Vendor documentation alone is insufficient.

# Acceptance Criteria

Write observable criteria.

Good:

```text
When the dialog opens, focus moves to the defined initial target,
focus remains within the dialog,
Escape closes it when cancellation is allowed,
and focus returns to the trigger.
```

Weak:

```text
The dialog is accessible.
```

# Verification

Use a combination of:

```text
static analysis
automated accessibility checks
semantic DOM assertions
keyboard testing
focus testing
contrast review
responsive and zoom review
screen-reader or other AT review
content review
manual interaction review
```

## Automated Testing Limits

Automated tools cannot reliably prove:

- meaningful alternative text;
- logical reading order;
- correct focus strategy;
- complete keyboard interaction;
- understandable errors;
- appropriate announcements;
- usability with assistive technologies;
- full WCAG conformance.

Never state:

```text
axe passed, therefore WCAG AA compliant
```

## Assistive-Technology Matrix

Select representative browser, platform, AT, and user journeys according to organizational support policy.

One combination cannot prove universal compatibility.

## Conformance Claims

This skill prepares design and evidence but does not certify.

A formal claim requires a defined scope, applicable criteria, complete processes, supported technologies, non-interference assessment, and retained evidence.

# Exceptions

Every exception must include:

- criterion or requirement;
- exact scope;
- user impact;
- reason;
- equivalent path;
- owner;
- remediation plan and date;
- approval;
- validation.

Use:

```text
NO_EXCEPTION
TEMPORARY_APPROVED_EXCEPTION
KNOWN_LIMITATION_WITH_EQUIVALENT_PATH
VENDOR_BLOCKER
CONTENT_BLOCKER
EXCEPTION_REQUIRES_APPROVAL
UNACCEPTABLE_BARRIER
```

A deadline or vendor limitation does not make a barrier accessible.

# Final Decision

Use:

```text
ACCESSIBLE_INTERFACE_DESIGN_READY
ACCESSIBLE_INTERFACE_DESIGN_READY_WITH_CONDITIONS
RETURN_TO_PRODUCT_OR_CONTENT_DESIGN
COMPLEX_WIDGET_PRIMITIVE_REQUIRED
ACCESSIBILITY_EXCEPTION_REQUIRES_APPROVAL
CONFORMANCE_TARGET_REQUIRED
BLOCKED
```

## Output

Use `assets/accessible-web-interface-design-record.md`.

## Completion Criteria

- [ ] Scope, journeys, users, and target are explicit.
- [ ] Applicable WCAG 2.2 criteria are mapped.
- [ ] Perceivable requirements cover alternatives, structure, contrast, color, reflow, spacing, and hover/focus content.
- [ ] Operable requirements cover keyboard, focus, traps, timing, motion, navigation, dragging alternatives, and target size.
- [ ] Understandable requirements cover language, predictability, labels, errors, prevention, redundant entry, and authentication.
- [ ] Robust requirements cover semantic HTML, names, roles, values, states, and status messages.
- [ ] Native semantics were considered before ARIA or custom widgets.
- [ ] Complex widgets use an accepted interaction model or proven primitive.
- [ ] Dynamic status and focus behavior are explicit.
- [ ] Visual, responsive, zoom, motion, forced-color, and theme behavior are explicit.
- [ ] Framework-neutral behavior precedes framework adaptation.
- [ ] Wrappers preserve accessibility behavior.
- [ ] Acceptance criteria are observable.
- [ ] Verification combines automated and manual evidence.
- [ ] Automated tests are not presented as proof of conformance.
- [ ] Exceptions include user impact, equivalent path, owner, and remediation.
- [ ] No legal requirement, implementation code, or unsupported conformance claim was invented.

## References

- Read `references/wcag-22-principles-and-conformance.md` first.
- Read `references/perceivable-content-and-visual-design.md`.
- Read `references/operable-keyboard-focus-input-and-motion.md`.
- Read `references/understandable-content-forms-errors-and-authentication.md`.
- Read `references/robust-semantics-aria-status-and-dynamic-content.md`.
- Read `references/complex-widgets-and-interaction-patterns.md`.
- Read `references/framework-adaptation-and-design-system-integration.md`.
- Read `references/accessibility-verification-and-conformance-evidence.md`.
- Read `references/accessible-web-interface-design-audit.md` before completion.
