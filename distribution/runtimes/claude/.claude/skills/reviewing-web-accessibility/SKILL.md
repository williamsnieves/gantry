---
name: reviewing-web-accessibility
description: Performs a structured, framework-agnostic accessibility review of an implemented web interface. Use when a page, component, flow, form, dialog, menu, dashboard, or responsive layout already exists and needs evidence-based review against the accepted accessibility target, typically WCAG 2.2 AA. Inspect keyboard navigation, focus management, semantic structure, accessible names, contrast, zoom/reflow, motion, target size, status/error communication, and assistive-technology behavior; then produce severity-ranked findings with user impact, reproduction, recommended fix, and verification plan. Do not claim conformance from automated scans alone, treat tooling warnings as violations without validation, or redesign the entire product when a bounded remediation is sufficient.
---

# Reviewing Web Accessibility

## Purpose

Review an implemented web interface for accessibility defects and risks.

This skill is evidence-driven.

The core workflow is:

```text
implemented interface
→ accepted accessibility target
→ automated + manual + browser/AT evidence
→ validated findings
→ severity + user impact
→ remediation
→ verification plan
```

This skill does not design the original accessibility contract. That belongs to:

```text
designing-accessible-web-interfaces
```

This skill asks:

```text
What is actually broken or risky in the implementation?
```

## Default Review Target

Use the project's accepted accessibility target.

If none is explicitly documented, use:

```text
WCAG 2.2 Level AA
```

as the engineering baseline, consistent with the frontend standard.

Do not:

- invent legal obligations;
- claim formal WCAG conformance from this review alone;
- treat an automated scanner as sufficient evidence;
- assume every Level AAA criterion;
- report speculative violations without reproduction/evidence.

## Use When

- Reviewing an implemented page or component.
- Auditing a route before release.
- Investigating keyboard/focus regressions.
- Reviewing responsive accessibility at zoom/reflow.
- Checking dialogs, menus, comboboxes, tabs, tooltips, or custom widgets.
- Reviewing forms and error communication.
- Reviewing touch/mobile target size.
- Reviewing reduced-motion behavior.
- Reviewing screen-reader status communication.
- Reviewing an implementation after accessibility fixes.
- Producing a remediation backlog.

## Do Not Use When

- The interface has not been designed yet.
- The task is to define accessibility requirements before implementation.
- The task is only to run axe/Lighthouse.
- The task is purely visual styling with no accessibility review.
- The task is native mobile without a web surface.
- The task is legal advice.
- The review target/scope cannot be determined.

## Inputs

- Implemented interface.
- Accepted behavior.
- Accessibility target.
- Existing design accessibility contract, if available.
- Browser/runtime.
- Supported input modes.
- Supported assistive technologies.
- Responsive/theme requirements.
- Existing test coverage.
- Automated accessibility tooling.
- Known exceptions.
- Repository-local `AGENTS.md`.

## Outputs

- Review scope.
- Evidence inventory.
- Severity-ranked violation inventory.
- User impact for every validated finding.
- Reproduction steps.
- WCAG mapping where supportable.
- Recommended remediation.
- Verification plan.
- Residual risk/exception inventory.
- Web accessibility review record.

# Review Philosophy

A finding should be traceable:

```text
observed behavior
→ affected user capability
→ reproducible barrier
→ applicable requirement
→ bounded remediation
→ verification evidence
```

Avoid vague findings such as:

```text
Accessibility could be improved.
```

Prefer:

```text
Keyboard focus moves behind the open modal.
```

with exact reproduction and expected behavior.

# Evidence Types

Use a combination of:

```text
AUTOMATED
KEYBOARD_MANUAL
POINTER_TOUCH
FOCUS_INSPECTION
SEMANTIC_DOM
CONTRAST_MEASUREMENT
ZOOM_REFLOW_BROWSER
REDUCED_MOTION
SCREEN_READER
VISUAL_BROWSER
CODE_INSPECTION
```

The absence of one evidence type does not automatically block the whole review.

However, do not claim a behavior is verified when the required evidence was not performed.

# Automated Tooling

Automated tools may include project-approved:

```text
axe
Lighthouse
Accessibility Insights
eslint/jsx-a11y
browser accessibility tree inspection
framework/design-system checks
```

Use existing project tooling.

Do not introduce a new scanner unless necessary and approved.

Automated tooling is useful for:

- missing names;
- invalid ARIA;
- some contrast issues;
- duplicate IDs;
- some landmark/heading issues;
- form labeling;
- structural rule violations.

It cannot reliably prove:

- logical focus order;
- correct dialog restoration;
- usable screen-reader announcements;
- keyboard interaction quality;
- meaningful error recovery;
- responsive reflow quality;
- target-size appropriateness in context;
- motion experience;
- overall WCAG conformance.

# Automated Result Validation

Classify scanner output:

```text
VALIDATED_VIOLATION
FALSE_POSITIVE
NEEDS_MANUAL_VALIDATION
ADVISORY
NOT_APPLICABLE
```

Do not copy tool output blindly into the final report.

# Manual Keyboard Review

Review the full intended keyboard path.

Typical keys:

```text
Tab
Shift+Tab
Enter
Space
Escape
Arrow keys
Home
End
```

according to widget semantics.

Check:

- all interactive elements reachable;
- no keyboard trap;
- logical order;
- visible focus;
- correct activation;
- no hidden focusable content;
- widget-specific keyboard behavior;
- focus restoration after transient UI.

# Keyboard Trap

Distinguish:

```text
INTENTIONAL_MODAL_CONTAINMENT
```

from:

```text
INVALID_KEYBOARD_TRAP
```

A modal dialog may intentionally contain focus while open.

A trap is invalid when the user cannot leave a component or progress using expected keyboard interaction.

# Focus Review

Review:

- initial focus;
- focus order;
- focus visibility;
- focus restoration;
- focus after validation;
- focus after route/content update;
- focus obscured by sticky/fixed UI;
- focus inside portals/overlays.

Do not judge focus only by CSS outline presence.

# Focus Trap Evaluation

Roadmap case:

```text
focus trap
```

Review both failure directions:

```text
focus escapes a modal that should contain it
```

and:

```text
focus is trapped in a widget with no expected exit
```

Report exact observed barrier.

# Semantic Structure

Inspect:

- page title;
- language;
- headings;
- landmarks;
- lists;
- tables;
- buttons vs links;
- form labels;
- group relationships;
- descriptions;
- state/value semantics;
- native element usage;
- ARIA validity.

Prefer native semantics where possible.

Do not report “missing role” when native HTML already provides the role.

# Accessible Names

Every interactive control needs an accessible name.

Check:

- visible label;
- `aria-label`;
- `aria-labelledby`;
- native label;
- icon-only buttons;
- inputs;
- comboboxes;
- dialogs;
- links.

Do not accept names that describe appearance rather than action.

Example:

```text
Magnifying glass
```

is weaker than:

```text
Search
```

# Missing Label Evaluation

Roadmap case:

```text
missing label
```

Review:

- input has programmatic label;
- visible text is actually associated;
- placeholder is not the sole label;
- group/fieldset labeling exists when needed;
- errors/descriptions do not replace labels.

# Color-Only Information

Review whether meaning is communicated only by color.

Examples:

- red border for invalid;
- green dot for online;
- chart series with color only;
- selected state only by background color.

Need additional:

- text;
- icon with accessible meaning;
- shape;
- label;
- pattern;
- programmatic state.

# Color-Only Error Evaluation

Roadmap case:

```text
color-only error
```

Example defect:

```text
input border becomes red
but no error text/state is announced.
```

Review both visual and programmatic communication.

# Contrast

Measure applicable foreground/background contrast.

Review:

- text;
- icons conveying meaning;
- form boundaries/states where applicable;
- focus indicators;
- disabled behavior under project policy;
- theme variants.

Use the project's approved measurement approach.

Do not estimate contrast by eye when a measurable pair is available.

# Theme Review

Review every supported theme relevant to the change:

```text
light
dark
high contrast
brand/tenant
```

Do not assume light-theme contrast proves dark-theme accessibility.

# Zoom and Reflow

Review at supported zoom/text scale.

Check:

- no content loss;
- no overlap;
- no clipped labels;
- no essential action loss;
- no unintended two-dimensional page scrolling;
- focus remains visible;
- sticky UI does not obscure content.

For WCAG-oriented review, substantial zoom/reflow evidence is especially important.

# Responsive Boundary Evidence

Test meaningful failure points, not just device presets.

Use:

```text
narrow viewport
zoomed effective viewport
long translation
large text
```

# Motion

Review:

- animation;
- auto-scrolling;
- parallax;
- transitions;
- flashing;
- motion triggered by interaction;
- motion under `prefers-reduced-motion`.

Do not assume a global reduced-motion stylesheet covers every animation.

# Reduced Motion Evaluation

Roadmap case:

```text
reduced motion
```

Verify:

```text
prefers-reduced-motion: reduce
```

actually removes/reduces non-essential motion.

If motion is essential to understanding, provide an accessible alternative.

# Timing

When applicable review:

- session timeout;
- disappearing status;
- auto-advance;
- toast duration;
- time-limited tasks.

Do not add timing findings when the interface has no timed behavior.

# Touch and Pointer

Review:

- pointer activation;
- target size;
- spacing between targets;
- hover-only disclosure;
- drag-only operations;
- touch accessibility.

Keyboard support does not replace touch usability.

# Mobile Target Size

Roadmap case:

```text
mobile target size
```

The frontend standard recommends:

```text
44×44 CSS pixels
```

as a strong default for touch interfaces.

Treat this as project engineering guidance, not an invented universal WCAG threshold.

Review:

- actual target;
- spacing;
- criticality;
- alternative access;
- dense UI exceptions.

Do not report based only on visual icon size if the interactive hit area is larger.

# Screen Reader Review

When screen-reader evidence is required, review:

- names;
- roles;
- states;
- values;
- reading order;
- dynamic announcements;
- form errors;
- dialog names;
- menu/combobox semantics;
- status updates.

Use supported project/browser/AT combinations when documented.

Do not generalize one screen reader's exact phrasing as the universal expected output.

# Dynamic Status

Dynamic updates may require:

```text
role=status
aria-live
aria-atomic
focus movement
```

depending on urgency/interaction.

Do not announce every update.

Announcements should be:

- meaningful;
- concise;
- non-duplicative;
- correctly timed.

# Screen-Reader Status Evaluation

Roadmap case:

```text
screen-reader status
```

Example:

```text
"Saved successfully"
```

appears visually but is never exposed to assistive technology.

Review whether:

- live region exists if needed;
- update is inserted correctly;
- announcement is not duplicated;
- focus does not move unnecessarily.

# Forms and Errors

Review:

- labels;
- required state;
- descriptions;
- validation timing;
- field error association;
- error summary;
- server errors;
- focus after failed submit;
- error recovery;
- success/status communication.

Business rule correctness is not the accessibility review's job.

# Error Communication

An error should be perceivable without relying on:

```text
color
position alone
icon alone
```

and programmatically connected where appropriate.

Review whether the user can understand:

```text
what happened
where
how to fix it
```

# Disabled Controls

Review both semantics and behavior.

A visually disabled control that remains clickable is a defect.

Check:

- native `disabled` or correct ARIA pattern;
- keyboard/pointer behavior;
- explanation if user needs to understand why action is unavailable.

# Hidden Content

Responsive/conditional hidden content should not remain unexpectedly focusable.

Check:

- `display:none` / hidden semantics;
- inert background;
- offscreen content;
- collapsed navigation;
- dialogs;
- tabs.

# Complex Widgets

Prefer proven native/design-system/headless behavior.

Review:

- Dialog;
- Menu;
- Combobox/Listbox;
- Tabs;
- Tooltip/Popover;
- Tree/Grid where applicable.

Do not re-audit vendor internals if the project wrapper preserves the contract and the specific usage shows no regression.

# Dialog Review

Check:

- accessible name;
- role/modal state;
- initial focus;
- containment;
- Escape/dismissal policy;
- focus restoration;
- background interaction;
- scroll lock effects;
- nested overlays.

# Menu Review

Check:

- menu semantics appropriate;
- keyboard navigation;
- disabled items;
- Escape;
- focus placement/restoration;
- link vs command semantics.

# Combobox Review

Check:

- accessible input/trigger name;
- popup relationship;
- option semantics;
- active/selected state;
- keyboard;
- no inaccessible custom autocomplete behavior.

# Tooltip Review

Check:

- content is non-critical;
- focus access;
- hover behavior;
- touch alternative where relevant;
- no interactive controls that should be a popover.

# Tabs Review

Check:

- tablist/tab/tabpanel roles/relationships;
- selected state;
- keyboard navigation;
- focus;
- hidden panel behavior.

# Heading and Landmark Review

Check:

- meaningful heading structure;
- one understandable page structure;
- landmarks available where useful;
- duplicate landmark labels when multiple same-type regions exist.

Do not enforce a simplistic “only one h1” rule if the project's document model legitimately differs.

# Tables

Review:

- actual tabular data uses table semantics;
- headers associated;
- captions/labels where useful;
- responsive transformation preserves labels and relationships.

Do not demand table markup for layout-only grids.

# Images and Icons

Review:

- informative alternative text;
- decorative hiding;
- functional icon accessible name;
- complex graphic alternative.

Do not duplicate visible adjacent text in alt unnecessarily.

# Links

Review:

- purpose understandable from context;
- keyboard activation;
- focus;
- visited/visual distinction per project design when relevant;
- no fake button semantics.

# Buttons

Review:

- correct button semantics;
- accessible name;
- disabled state;
- loading state;
- duplicate-submission risk when loading;
- focus visibility.

# Custom Clickable Elements

Flag:

```text
<div onClick>
<span onClick>
```

when they substitute for native interactive semantics without keyboard/focus/role behavior.

Preferred remediation is usually native HTML.

# Mobile Navigation

Review:

- disclosure control name/state;
- focus movement;
- hidden menu focusability;
- close behavior;
- touch targets;
- keyboard use;
- escape when applicable.

# Sticky / Fixed Content

Check whether focused content is obscured by:

- sticky header;
- cookie banner;
- bottom bar;
- floating CTA.

This can create a focus visibility/access problem even if focus style itself is correct.

# Focus Obscured

Record:

```text
focused element
→ obscured by fixed UI
→ user cannot identify current focus / operate content
```

Provide exact viewport/zoom reproduction.

# Target Size Evidence

Measure the interactive hit box, not just the icon.

Record:

```text
width
height
spacing
context
```

# Voice / Speech Input

Where scope requires it, accessible names should generally align with visible labels to support voice control.

Do not create a speech-input finding without evidence/project support requirements.

# Cognitive Understandability

Review obvious barriers:

- unclear labels;
- inconsistent navigation;
- ambiguous errors;
- unexpected context changes.

Do not turn a focused engineering review into speculative UX psychology.

# Severity Model

Use:

```text
CRITICAL
HIGH
MEDIUM
LOW
ADVISORY
```

## Critical

Use when a major/core journey is effectively impossible for a user group and no practical workaround exists.

Examples may include:

- checkout impossible by keyboard;
- authentication impossible with supported assistive technology;
- app unusable due to persistent keyboard trap.

Use sparingly.

## High

Use for substantial barriers in important workflows.

Examples:

- modal focus escapes and background becomes operable;
- required field has no accessible label;
- critical error is not programmatically communicated;
- major content unavailable at zoom.

## Medium

Use for meaningful but bounded barriers with workaround or lower workflow impact.

Examples:

- non-primary icon button name ambiguous;
- secondary target undersized;
- status announcement missing but visual state remains clear to some users.

## Low

Use for smaller accessibility quality defects with limited barrier impact.

## Advisory

Use for recommended improvement without a validated violation/barrier under the accepted target.

Do not inflate severity based on code ugliness.

# Severity Factors

Consider:

```text
user impact
journey importance
frequency
affected user groups
workaround
persistence
scope
risk of task failure
```

# Finding Structure

Every finding should include:

```text
ID
title
severity
status
affected surface
user impact
evidence
reproduction
expected behavior
actual behavior
WCAG mapping (when supportable)
recommended fix
verification plan
```

# Finding Status

Use:

```text
OPEN
CONFIRMED
NEEDS_VALIDATION
FIXED_PENDING_VERIFICATION
VERIFIED
ACCEPTED_EXCEPTION
FALSE_POSITIVE
```

# WCAG Mapping

Map to WCAG criteria only when the evidence supports the mapping.

Do not add criteria simply because they are related topically.

A finding can still be valid engineering feedback if exact criterion mapping is uncertain.

Mark:

```text
WCAG_MAPPING_REQUIRES_CONFIRMATION
```

when needed.

# User Impact

Describe impact from the user's perspective.

Weak:

```text
aria-label missing
```

Better:

```text
Screen-reader users encounter an unnamed button and cannot determine what action it performs.
```

# Reproduction

Reproduction should be executable.

Example:

```text
1. Open /settings.
2. Navigate to "Delete account".
3. Activate the dialog using keyboard.
4. Press Tab repeatedly.
5. Focus moves to the page behind the modal.
```

Avoid “sometimes inaccessible.”

# Recommended Fix

Recommend the smallest reliable fix.

Prefer:

```text
restore the existing Dialog primitive focus containment
```

over:

```text
rewrite the modal system
```

unless architecture truly requires broader change.

# Verification Plan

Every finding needs a plan.

Possible:

```text
automated rule
component keyboard test
browser focus test
contrast measurement
zoom/reflow test
screen-reader check
visual regression
manual keyboard retest
```

Use the lowest reliable boundary plus manual/browser evidence where required.

# Remediation Ownership

Classify likely owner:

```text
SHARED_UI
FEATURE
STYLING
ROUTING
FORM
DESIGN_TOKENS
CONTENT
DESIGN
PLATFORM
```

Do not move all accessibility fixes into shared UI automatically.

# Shared Primitive Regression

If a shared primitive causes the defect, assess blast radius.

Review other consumers or require a targeted regression plan.

# Feature-Level Regression

If only one feature overrides otherwise-correct shared behavior, remediate locally.

Do not change every consumer unnecessarily.

# Accessibility Exception

If product accepts an exception, record:

- rationale;
- owner;
- scope;
- target criterion/impact;
- mitigation;
- expiry/review date if project policy uses one.

Do not silently omit known issues.

# False Positive

Record false positives where useful so tooling configuration can improve.

Do not suppress globally from one local false positive without understanding scope.

# Review Scope

Define exact scope:

```text
route
component
journey
breakpoints
themes
input modes
AT combinations
```

Do not imply the entire application was reviewed if only one route was inspected.

# Sampling

For large apps, sample representative:

- shared primitives;
- templates;
- critical journeys;
- themes;
- responsive states.

Document what was not reviewed.

# Review Modes

Possible:

```text
PRE_RELEASE_REVIEW
REGRESSION_REVIEW
COMPONENT_REVIEW
CRITICAL_JOURNEY_REVIEW
DESIGN_SYSTEM_REVIEW
REMEDIATION_VERIFICATION
```

# Pre-Release Review

Prioritize:

- blockers/high severity;
- critical journey;
- new interactions;
- shared primitive changes;
- regressions.

# Remediation Verification

A fix is not complete because code changed.

Re-run the reproduction and required evidence.

Use:

```text
FIXED_PENDING_VERIFICATION
→ VERIFIED
```

only after evidence.

# Regression Prevention

For validated defects, decide whether to add:

- automated a11y rule;
- component test;
- browser test;
- visual test;
- shared primitive contract test.

Do not automate only for the sake of automation.

# Focus Trap Evaluation

Roadmap evaluation.

A passing review should determine:

```text
Is focus contained where required?
Can the user escape where expected?
Does focus return logically?
```

# Color-Only Error Evaluation

Roadmap evaluation.

A passing review should verify:

```text
error has visible non-color communication
+
programmatic error state/relationship where needed
```

# Missing Label Evaluation

Roadmap evaluation.

A passing review should verify:

```text
control has meaningful programmatic accessible name
```

not placeholder-only naming.

# Reduced Motion Evaluation

Roadmap evaluation.

A passing review should verify:

```text
non-essential animation is reduced/removed when user requests reduced motion
```

# Mobile Target Size Evaluation

Roadmap evaluation.

A passing review should verify actual hit area and contextual spacing against the accepted target/project guidance.

# Screen-Reader Status Evaluation

Roadmap evaluation.

A passing review should verify meaningful dynamic status becomes available to assistive technology without disruptive focus movement or duplicated announcements.

# Test Strategy Integration

Accessibility review is not the same as accessibility test implementation.

However findings should identify the correct verification boundary.

Possible next skills:

```text
testing-react-components
testing-frontend-user-journeys
reviewing-web-accessibility
designing-accessible-forms
```

# Automated Coverage

Good automated coverage candidates:

- labels/names;
- roles;
- invalid ARIA;
- some contrast;
- duplicate IDs;
- static landmark issues.

# Browser Coverage

Good browser coverage candidates:

- focus containment;
- restoration;
- target size;
- zoom/reflow;
- sticky obstruction;
- portal layering;
- reduced motion;
- keyboard sequences.

# Screen Reader Coverage

Use where semantic/dynamic status behavior cannot be proven sufficiently from DOM/accessibility tree inspection alone.

Do not require a screen reader for every static heading finding.

# Review Report Summary

Summarize:

```text
critical
high
medium
low
advisory
```

and distinguish:

```text
validated findings
unverified risks
accepted exceptions
```

# Release Recommendation

Use one:

```text
ACCESSIBILITY_REVIEW_PASS
ACCESSIBILITY_REVIEW_PASS_WITH_ADVISORIES
ACCESSIBILITY_REVIEW_REQUIRES_FIXES
ACCESSIBILITY_REVIEW_BLOCKED
ACCESSIBILITY_REVIEW_INCOMPLETE
```

A pass does not claim formal WCAG conformance.

# Blocking Rule

Recommend blocking release when accepted project policy requires it and a critical/high barrier affects a critical journey with no acceptable workaround.

Do not invent a release policy if the project has none.

# Over-Reporting Audit

Flag:

- tool warning copied without validation;
- duplicate findings for same root cause;
- severity inflated by code smell;
- speculative screen-reader issue with no evidence;
- every hardcoded pixel reported as accessibility defect;
- all focus styling deviations called blockers.

# Under-Reporting Audit

Flag:

- “axe passed” used as conclusion;
- keyboard path not tested;
- no zoom/reflow evidence;
- no screen-reader/dynamic-status review where required;
- theme contrast ignored;
- shared primitive regression scope ignored.

# Final Decision

Use:

```text
ACCESSIBILITY_REVIEW_PASS
ACCESSIBILITY_REVIEW_PASS_WITH_ADVISORIES
ACCESSIBILITY_REVIEW_REQUIRES_FIXES
ACCESSIBILITY_REVIEW_BLOCKED
ACCESSIBILITY_REVIEW_INCOMPLETE
```

## Output

Use `assets/web-accessibility-review-record.md`.

## Completion Criteria

- [ ] Review scope and target are explicit.
- [ ] Review does not claim formal conformance from scans alone.
- [ ] Automated findings are manually validated where required.
- [ ] Keyboard navigation is reviewed.
- [ ] Focus order, visibility, containment, restoration, and obstruction are reviewed where applicable.
- [ ] Semantic structure and native element use are reviewed.
- [ ] Accessible names/labels are reviewed.
- [ ] Color-only information is reviewed.
- [ ] Contrast is measured where applicable.
- [ ] Zoom/reflow and content expansion are reviewed.
- [ ] Reduced-motion behavior is reviewed where motion exists.
- [ ] Touch/mobile target size is reviewed where relevant.
- [ ] Dynamic status/error communication is reviewed.
- [ ] Complex widget behavior is reviewed against proven primitive semantics.
- [ ] Hidden responsive content is not unexpectedly focusable.
- [ ] Findings describe user impact rather than only code symptoms.
- [ ] Every confirmed finding has reproducible steps.
- [ ] WCAG mapping is included only when supportable.
- [ ] Severity is based on barrier impact, journey importance, frequency, and workaround.
- [ ] Every finding has a bounded recommended fix.
- [ ] Every finding has a verification plan.
- [ ] Exceptions and unreviewed scope are explicit.
- [ ] Regression-prevention opportunity is recorded for material defects.
- [ ] Roadmap evaluations are covered: focus trap, color-only error, missing label, reduced motion, mobile target size, screen-reader status.
- [ ] Final review decision is explicit.
- [ ] A pass is not described as formal WCAG certification.

## References

- Read `references/review-scope-evidence-and-severity.md` first.
- Read `references/keyboard-focus-semantics-and-labels.md`.
- Read `references/contrast-zoom-reflow-motion-and-target-size.md`.
- Read `references/errors-live-regions-and-screen-reader-status.md`.
- Read `references/complex-widgets-and-shared-primitive-regressions.md`.
- Read `references/automated-tools-manual-review-and-false-positives.md`.
- Read `references/remediation-verification-and-regression-prevention.md`.
- Read `references/web-accessibility-review-audit.md` before completion.
