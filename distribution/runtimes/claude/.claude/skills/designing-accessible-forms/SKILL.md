---
name: designing-accessible-forms
description: Designs accessible web form contracts before implementation. Use when a form needs explicit labels, descriptions, required/optional semantics, field groups, validation timing, accessible error association, error summaries, async validation, server-error handling, dynamic fields, date ranges, multi-step flows, and duplicate-submission prevention. Keep UI shape/interaction validation separate from Domain/backend business invariants, preserve keyboard and screen-reader behavior, and define focus/status behavior for failures and submission. Do not rely on placeholders as labels, communicate errors only by color, duplicate authoritative business rules across client and server, or move focus/announce status without a deliberate interaction contract.
---

# Designing Accessible Forms

## Purpose

Design the accessibility and interaction contract of a web form before implementation.

The core flow is:

```text
form intent
→ field semantics
→ labels/descriptions/groups
→ validation ownership
→ error communication
→ submission state
→ focus/status behavior
→ verification plan
```

The skill must distinguish:

```text
UI shape + interaction validation
```

from:

```text
Domain/backend business invariants
```

The frontend validates enough to create a good user experience, but the backend remains authoritative for server-enforced business rules.

## Governing Standard

Forms MUST validate shape and interaction requirements at the UI boundary.

Business invariants MUST remain authoritative in Domain or backend systems.

Do not duplicate complex business rules inconsistently across controller, hook, component, and server.

Validation errors MUST be associated with fields accessibly.

Submission state MUST prevent accidental duplicate actions where required.

Interactive UI MUST:

- use semantic HTML where possible;
- support keyboard interaction;
- expose an accessible name;
- preserve visible focus;
- communicate disabled and invalid states;
- avoid color-only meaning;
- maintain contrast;
- support zoom and reflow;
- respect reduced-motion preferences.

## Use When

- Designing a new form before implementation.
- Adding fields to an existing form.
- Designing validation timing and error behavior.
- Designing an async-validated field.
- Designing server-error mapping.
- Designing dynamic/repeating fields.
- Designing date or date-range input.
- Designing a multi-step/wizard form.
- Defining error summary/focus behavior.
- Defining required/optional semantics.
- Defining submission/loading behavior.
- Deciding native form APIs vs approved form library interaction contracts.

## Do Not Use When

- The form is already implemented and needs an audit.
- The task is a general accessibility review.
- The task is to choose React Hook Form/Formik/Zod/etc.
- The task is Domain/backend business-rule design.
- The task is server-side validation implementation.
- The task is CSS/Tailwind styling.
- The task is generic component variant design.
- No form/control interaction exists.

## Inputs

- Form purpose.
- Accepted user journey.
- Field inventory.
- Data ownership.
- Application/Domain/backend validation contracts.
- Server error semantics.
- Required/optional rules.
- Dynamic-field behavior.
- Submission behavior.
- Accessibility target.
- Routing/multi-step requirements.
- Existing form library, if selected.
- Existing shared form primitives.
- Localization requirements.
- Test strategy.
- Repository-local `AGENTS.md`.

## Outputs

- Form accessibility contract.
- Field-label/description contract.
- Required/optional semantics.
- Grouping contract.
- Validation ownership matrix.
- Validation timing.
- Field-error association.
- Error-summary behavior.
- Async-validation behavior.
- Server-error mapping.
- Submission-state behavior.
- Dynamic-field behavior.
- Date/date-range behavior.
- Multi-step behavior.
- Focus/status announcement plan.
- Form verification matrix.
- Accessible-form design record.

## Core Workflow

```text
identify form intent
→ inventory fields and groups
→ define labels/descriptions
→ classify validation ownership
→ define timing and errors
→ define focus/status behavior
→ define submission state
→ handle async/server/dynamic/date/multi-step cases
→ define verification
```

## Readiness Gate

Use one:

```text
READY_TO_DESIGN_ACCESSIBLE_FORM
READY_WITH_CONDITIONS
FORM_CONTRACT_NOT_REQUIRED
FIELD_SEMANTICS_REQUIRED
VALIDATION_OWNERSHIP_REQUIRED
SERVER_ERROR_CONTRACT_REQUIRED
MULTI_STEP_POLICY_REQUIRED
DYNAMIC_FIELD_POLICY_REQUIRED
BLOCKED
```

# Field Inventory

Record every interactive field.

For each field define:

```text
name
label
type
required/optional
description/help
validation owner
validation timing
error semantics
autocomplete
input mode
format expectations
```

Do not begin with JSX/component names.

Begin with the user's task.

# Labels

Every field requires a meaningful programmatic accessible name.

Preferred patterns:

```text
<label for="email">Email address</label>
<input id="email" ... />
```

or equivalent framework-safe association.

Do not use placeholder text as the only label.

Do not use visually adjacent text without programmatic association.

# Visible Labels

Visible labels are preferred for standard form controls.

Use `aria-label` only when a visible label is genuinely inappropriate and the control remains understandable.

Do not hide labels solely for visual minimalism.

# Label Wording

Labels should describe the requested value.

Good:

```text
Email address
Start date
Number of seats
```

Weak:

```text
Input
Value
Data
```

Do not encode error instructions in the label itself unless they are part of stable field meaning.

# Descriptions / Help Text

Use descriptions for:

- format guidance;
- constraints;
- consequences;
- examples;
- privacy/context where useful.

Associate help text programmatically using the project's approved mechanism, commonly:

```text
aria-describedby
```

Do not overload the label with long instructions.

# Description vs Error

Help text and error text are different.

A field may need both.

When both are present, the accessible description should include both in a stable logical order.

Do not make error rendering remove important help text unless the product intentionally replaces it.

# Required / Optional Semantics

Required state must be understandable visually and programmatically.

Preferred:

```text
native required
```

where correct for the form behavior, plus visible convention.

If all fields are required except a few, clearly mark optional fields.

If most are optional, clearly mark required fields.

Do not rely on an asterisk with no explanation.

# `required` vs `aria-required`

Use native `required` when native form validation semantics are appropriate.

Use `aria-required` for custom/non-native controls when needed.

Do not set conflicting required semantics.

# Required Field Evaluation

Roadmap case:

```text
required field
```

Must define:

- visible indication;
- programmatic indication;
- validation timing;
- error message;
- focus/summary behavior after submit.

# Field Groups

Use semantic grouping for related controls.

Examples:

```text
fieldset + legend
radiogroup
group
```

according to native/custom control semantics.

Use groups for:

- radio choices;
- checkbox sets;
- date range;
- address subsections;
- related dynamic items.

Do not visually group controls without conveying group meaning when relationships matter.

# Radio Groups

Use native radio inputs when possible.

The group needs a clear question/legend.

Each option needs its own label.

Do not implement radios as unrelated buttons unless a proven primitive preserves expected semantics.

# Checkbox Groups

If multiple checkboxes answer one question, group them semantically.

Do not assume each checkbox label communicates the parent question.

# Input Types

Prefer semantic native types when they improve input and browser behavior:

```text
email
tel
url
number
date
search
password
```

But use them only when their browser behavior fits product requirements.

Do not use `type=number` for values like IDs, postal codes, or credit-card numbers merely because they contain digits.

# Autocomplete

Use appropriate autocomplete tokens for common personal/contact fields when relevant.

Do not disable autocomplete globally without a product/security requirement.

Password-manager compatibility should be considered for authentication forms.

# Input Mode

Use `inputmode` when it improves virtual-keyboard input without changing the semantic data type.

Example:

```text
one-time code
numeric identifier
decimal input
```

Do not use it as validation.

# Shape Validation

UI shape validation may include:

- required;
- parseable number/date;
- min/max length;
- basic email shape;
- format;
- client-safe file type/size;
- date ordering if it is interaction-level and not business-specific.

The goal is immediate usable feedback.

# Business Validation

Business invariants belong in Domain/backend.

Examples:

```text
promotion eligibility
credit availability
subscription renewal policy
inventory
authorization
pricing
account state
```

The frontend may provide preview guidance, but must not become authoritative.

# Validation Ownership Matrix

Classify each rule:

```text
UI_SHAPE_VALIDATION
UI_INTERACTION_VALIDATION
DOMAIN_VALIDATION
BACKEND_AUTHORITATIVE_VALIDATION
SHARED_SEMANTICS_BACKEND_AUTHORITATIVE
UNKNOWN_REQUIRES_DECISION
```

Do not implement the same complex business rule independently in five places.

# Client Validation Is Not Security

Client validation improves UX.

It does not replace server validation or authorization.

Do not treat disabled controls or hidden fields as security boundaries.

# Validation Timing

Possible timing:

```text
ON_SUBMIT
ON_BLUR
ON_CHANGE_AFTER_INTERACTION
ON_CHANGE_IMMEDIATE
ASYNC_AFTER_STABLE_INPUT
```

Choose per field/problem.

Avoid aggressive validation that announces errors while the user is still typing.

# Validation Timing Heuristics

Use `ON_SUBMIT` as a safe baseline for many forms.

Use blur/change when early feedback has clear value.

Examples:

- password requirements may update as user types;
- username availability may validate after debounce;
- required empty field usually need not error before interaction.

# Touched / Dirty

Libraries may track:

```text
touched
dirty
visited
```

These are implementation concepts.

The design contract should express observable timing:

```text
show error after field blur
```

rather than requiring one library's state shape.

# Error Message Content

An error message should explain:

```text
what is wrong
how to fix it
```

Good:

```text
Enter an email address in the form name@example.com.
```

Weak:

```text
Invalid.
```

Avoid exposing provider/backend technical messages directly.

# Error Localization

User-facing validation/server errors should be localizable where product requires it.

Do not use raw exception strings as UI copy.

# Error Association

Field errors MUST be programmatically associated with the field.

Typical pattern:

```text
aria-invalid="true"
aria-describedby="email-help email-error"
```

plus visible error text.

Do not communicate invalid state only through red border/color.

# `aria-errormessage`

May be used when supported by project/browser/AT policy.

Follow project conventions.

Do not introduce inconsistent error-association patterns across shared fields without reason.

# Error ID Stability

Error/help IDs should remain stable enough for ARIA relationships.

Use React/framework stable ID mechanisms.

Do not generate random IDs on every render.

# Error Placement

Place field error close to the field visually.

Programmatic association remains the authoritative relationship.

Do not rely only on visual proximity.

# Focus on Error

Do not move focus to every field error as it appears.

This is disruptive.

Focus movement is usually most appropriate after failed submission, especially to:

```text
error summary
first invalid field
step heading
```

depending on form design.

# Failed Submit Behavior

After failed submit:

1. prevent submission;
2. render all actionable validation errors according to policy;
3. make the failure clear;
4. move focus deliberately if required;
5. preserve user-entered data.

Do not reset the form.

# Error Summary

Use an error summary when the form is long, complex, multi-section, or has multiple errors that may be offscreen.

A summary should:

- have a clear heading;
- identify that submission failed;
- list errors;
- link/focus to fields where feasible;
- receive focus after failed submission if that improves recovery.

Do not use a global summary for a trivial two-field form if inline errors are sufficient.

# Error Summary Links

Summary items should use field labels/meaningful text.

Example:

```text
Email address: Enter a valid email address.
```

Do not say:

```text
Error 3.
```

# Screen Reader Announcements

Errors/status should be announced proportionately.

Do not make every keystroke trigger an assertive live region.

Use:

```text
focus to summary
status region
polite live region
field description update
```

according to urgency.

# `aria-live`

Use sparingly.

Possible:

```text
polite
assertive
```

Assertive should be reserved for truly urgent interruptions.

Form validation is often better handled via focus and described errors than continuous assertive announcements.

# Submission State

Define:

```text
idle
submitting
success
validation failure
server failure
```

according to form behavior.

Do not create contradictory booleans.

Use the accepted frontend async-state model where complexity warrants it.

# Duplicate Submission Prevention

When duplicate submission would be harmful:

```text
submitting
→ prevent repeated activation
```

Possible:

- disable submit;
- make mutation idempotent;
- show loading state;
- ignore duplicate command.

Do not rely only on button styling.

# Loading Button

If submit button enters loading:

- preserve accessible name;
- expose busy state appropriately;
- keep visible focus;
- prevent accidental duplicate action if required;
- avoid layout shift where practical.

Do not replace label with an unlabeled spinner.

# Disabled During Submission

Do not disable the entire form automatically.

Disabling everything can:

- remove controls from focus;
- make status harder to understand;
- prevent copying data;
- create confusing AT behavior.

Disable only what needs protection.

# Readonly vs Disabled

Use correctly.

```text
readonly
→ value remains perceivable/focusable/submittable depending on control

disabled
→ interaction unavailable; often excluded from submission
```

Do not use disabled when readonly semantics are intended.

# Server Errors

Server errors must be translated into stable user-facing semantics.

Classify:

```text
FIELD_SERVER_ERROR
FORM_SERVER_ERROR
AUTHORIZATION_ERROR
CONFLICT
NETWORK_ERROR
UNKNOWN_ERROR
```

Do not expose provider stack traces/messages.

# Field Server Error

If backend returns a field-specific error and stable mapping exists:

```text
field name/domain key
→ UI field
→ associated field error
```

Preserve the user's input.

Do not discard all values.

# Form-Level Server Error

Use form-level error for failures not attributable to one field.

Examples:

- network unavailable;
- server failure;
- submission conflict;
- policy failure spanning fields.

Ensure it is discoverable after submit.

# Server Business Error

Example:

```text
"This promotion is no longer available."
```

This may be a business/application result, not a shape-validation error.

Keep ownership clear.

Do not duplicate the eligibility algorithm client-side just to predict the message.

# Server Error Focus

After a failed server response:

- field error → focus/summary behavior according to field validation policy;
- form-level error → ensure status/summary is discoverable;
- auth/session error → escalate to session boundary as architecture defines.

Do not always focus the submit button again.

# Async Validation

Async validation may be appropriate for:

- username availability;
- invite code existence;
- unique slug;
- server-backed address lookup.

It must not become the only final server validation.

# Async Validation Trigger

Prefer:

```text
after stable valid-enough input
```

rather than every keystroke.

Possible:

- debounce;
- on blur;
- explicit check.

Do not send requests for clearly incomplete input.

# Async Validation State

Model:

```text
idle
checking
available/valid
unavailable/invalid
network failure
cancelled/obsolete
```

only to the extent UI behavior needs distinction.

Do not show stale result for old input.

# Async Race Safety

If value changes during validation:

```text
result for old value
MUST NOT
overwrite new value state
```

Use cancellation/latest-wins according to server-state/hook strategy.

Do not expose request counters as UI semantics.

# Async Validation Messaging

While checking, announce status only if helpful.

Example:

```text
Checking username availability…
```

Do not create noisy announcements on rapid input.

Final availability/error should be understandable visually and programmatically.

# Async Validation Failure

Network failure is not the same as:

```text
username unavailable
```

Distinguish:

```text
VALIDATION_NEGATIVE
VALIDATION_UNAVAILABLE
```

Do not block form permanently because availability check network failed unless business policy requires server confirmation.

# Async Validation Evaluation

Roadmap case:

```text
async validation
```

Must define:

- trigger;
- debounce/stability;
- loading/status behavior;
- cancellation/latest-wins;
- negative result;
- network failure;
- final server authority.

# Dynamic Fields

Dynamic fields include:

- add/remove repeating rows;
- conditional sections;
- dependent fields;
- generated participants/items;
- feature-controlled subforms.

Accessibility requires focus and naming discipline.

# Adding Dynamic Fields

When user adds a new field/group:

- give it a stable meaningful label;
- ensure unique IDs/names;
- consider moving focus to the new group/first field;
- announce addition if it is not otherwise obvious.

Do not always force focus if the added content is merely supplemental.

# Removing Dynamic Fields

After removal:

- move focus to a logical surviving control if the removed element had focus;
- update indexes/names carefully;
- preserve remaining entered values;
- avoid screen-reader confusion from silent structural change.

# Repeating Group Labels

Use meaningful group legends/headings.

Weak:

```text
Item 1
Item 2
```

can be acceptable only if context is clear.

Better when semantic:

```text
Traveler 1
Traveler 2
```

with stable accessible group structure.

# Dynamic Indexes

If items can reorder, do not use array index as the only semantic identity if it causes state/error association to drift.

Stable item IDs are preferred.

# Conditional Fields

When a field is hidden:

- remove it from keyboard/accessibility tree if not active;
- decide whether its value remains or clears;
- decide whether hidden field errors still block submit.

Do not keep an invisible invalid field preventing progress with no way to fix it.

# Dependent Fields

Example:

```text
country
→ state/province options
```

When parent changes:

- update child options;
- preserve/clear child value intentionally;
- communicate required re-selection if needed;
- avoid stale validation.

# Dynamic Fields Evaluation

Roadmap case:

```text
dynamic fields
```

Must define:

- add/remove control names;
- focus after add/remove;
- group semantics;
- stable identity;
- hidden-field validation policy;
- announcement if needed.

# Date Inputs

Choose input strategy according to product/browser/localization needs:

```text
native date input
text input with parsing
accessible date-picker primitive
segmented date fields
```

Do not build a custom calendar grid ad hoc unless a proven primitive is unavailable and the interaction contract is fully designed.

# Date Labels and Format

If using text date input, communicate expected format.

Example:

```text
Date of birth
Format: DD/MM/YYYY
```

Do not use placeholder-only format guidance.

# Date Parsing

Shape validation may verify parseability.

Calendar/business invariants remain separate.

Example:

```text
valid calendar date
→ UI shape validation

booking must be 48h in advance
→ business/server rule
```

# Date Range

A range has two related fields:

```text
Start date
End date
```

Group them with a meaningful range label where useful.

Do not use labels only:

```text
From
To
```

without sufficient context.

# Date Range Ordering

`end >= start` may be interaction/domain-dependent.

Classify ownership.

If it is universal range structure for the form, UI can validate early.

If business rules add:

```text
maximum 30 days
cannot include holidays
```

keep them authoritative where appropriate.

# Date Range Error

Attach the error to:

- the relevant field;
- the group;
- or both;

based on what the user needs to fix.

Do not duplicate identical error announcement excessively.

# Calendar Widget

If a custom date picker exists, verify:

- keyboard navigation;
- selected/current date semantics;
- month/year controls;
- focus;
- escape/dismissal;
- manual text alternative where project requires it.

Prefer project/headless accessible primitive.

# Date Range Evaluation

Roadmap case:

```text
date range
```

Must define:

- labels/group;
- format;
- parsing;
- ordering;
- business-rule ownership;
- error association;
- date-picker accessibility if used.

# Multi-Step Forms

A multi-step form adds:

```text
progress
navigation
step validation
state persistence
focus
error recovery
```

Do not implement it as disconnected pages with ambiguous progress.

# Step Semantics

Each step should have:

- meaningful step title;
- current step;
- progress indication;
- consistent navigation.

Possible visible text:

```text
Step 2 of 4: Billing details
```

Do not rely solely on progress bar color.

# Multi-Step Navigation

Define:

```text
Next
Back
Save and exit
Submit
```

according to journey.

Back should preserve entered values unless accepted behavior says otherwise.

# Step Validation

Choose:

```text
validate current step on Next
validate all at final submit
hybrid
```

Do not block progress on hidden future-step fields.

# Cross-Step Errors

At final submit, a server error may point to a field in another step.

Define:

```text
navigate to affected step
→ render error
→ focus summary/field
```

Do not show “error in step 1” while leaving user stranded on step 4.

# Multi-Step Focus

On step transition, place focus deliberately:

```text
step heading
first invalid field
error summary
```

depending on transition.

Do not leave focus on a removed Next button.

# Browser History

If steps map to routes/URLs, define Back/Forward behavior.

Do not make browser Back unexpectedly discard form data unless accepted.

# Progress Announcement

Progress should be perceivable visually and programmatically.

Do not announce every minor internal state change.

# Draft Persistence

If multi-step draft persists:

- ownership is separate from accessibility;
- loaded draft should restore labels/errors/state coherently;
- stale persisted errors should usually not reappear blindly.

# Multi-Step Evaluation

Roadmap case:

```text
multi-step form
```

Must define:

- progress semantics;
- step titles;
- current-step validation;
- final validation;
- Back behavior;
- focus after transitions;
- cross-step server-error routing;
- duplicate submission;
- persistence behavior if relevant.

# Form Libraries

The project may use:

```text
native form APIs
React Hook Form
Formik
framework actions
Zod
Valibot
Yup
custom typed validation
```

Use the selected stack.

This skill must not select a new form library.

The accessible contract should remain stable across libraries.

# Schema Validation

Schema libraries can validate shape.

Do not make the schema the sole source of accessible error behavior.

Need a mapping:

```text
validation issue
→ field/form error semantics
→ localized message
→ ARIA relationship
```

# Runtime Schema vs Domain Rule

Example:

```text
email: valid email shape
→ schema/UI validation

customer may change billing email only once per month
→ business/server rule
```

Do not encode the latter merely because the schema library can.

# Server Actions / Framework Forms

Framework actions can own submission transport.

Still design:

- labels;
- errors;
- pending state;
- focus;
- status;
- duplicate prevention.

Do not let framework convenience remove accessible error association.

# Native Validation UI

Browser-native validation may be acceptable if project UX/localization/accessibility policy accepts it.

If custom validation is used, consider `novalidate` only when the custom experience fully replaces native behavior intentionally.

Do not disable native validation and then provide no equivalent.

# Form Reset

Define reset semantics.

Do not reset automatically after server failure.

After success, reset only when user journey expects a fresh form.

# Unsaved Changes

If form warns on navigation:

- warning should be accessible;
- modal/dialog follows accessible primitive behavior;
- do not trap users from leaving permanently.

# File Inputs

If present, define:

- visible label;
- accepted file types;
- size guidance;
- selected file status;
- upload progress;
- file-specific/server errors;
- remove/retry controls.

Do not rely on file extension text alone if validation is authoritative elsewhere.

# Password Fields

If present, define:

- visible label;
- show/hide password control with accessible name/state;
- requirements;
- caps-lock handling if implemented;
- password manager compatibility.

Do not prevent paste without strong reason.

# Confirmation Fields

Avoid asking users to retype data unnecessarily.

If confirmation is required, label it explicitly.

# Address Forms

Use semantic labels/autocomplete.

Do not assume one country format globally.

Dynamic address fields need the same focus/hidden validation policies.

# Localization

Forms must tolerate translated labels/errors/help.

Avoid fixed field-label widths that clip.

Date/number formats should follow product locale strategy.

Do not place semantic meaning only in punctuation/symbols that may translate poorly.

# RTL

If supported, form layout and error indicators should respect direction.

Programmatic label associations are direction-independent.

# Error Copy Ownership

User-facing form error copy is Presentation/content policy.

Application/Domain should return stable semantic errors, not localized UI strings, unless architecture explicitly defines otherwise.

# Analytics

Form analytics should not capture sensitive field values.

Do not log full validation payloads or PII.

Accessibility review does not justify expanding telemetry.

# Privacy

Help/error content should avoid exposing sensitive server details.

File/password/payment-related failures need careful wording.

# Testing Strategy

Test behavior at the lowest reliable boundary.

Component/form integration tests should prioritize:

- roles;
- labels;
- described errors;
- keyboard behavior;
- submission state;
- async validation transitions;
- dynamic fields;
- error summary;
- multi-step navigation.

# Accessible Queries

Prefer:

```text
getByRole
getByLabelText
getByText for error/status where appropriate
```

Do not locate fields by implementation class or placeholder when a label exists.

# Required Field Test

Verify:

- accessible label;
- required semantics;
- failed submit;
- associated error;
- error recovery.

# Async Validation Test

Use controlled async resolution.

Verify:

```text
value A check starts
→ value changes to B
→ A result cannot override B
```

No arbitrary sleeps.

# Server Error Test

Verify field and form-level mappings separately.

Do not mock raw provider errors at the component if Application already translates them.

# Dynamic Field Test

Verify add/remove focus and stable labels.

Do not assert array indexes as the primary behavior.

# Date Range Test

Verify labels, parsing/order errors, and group association.

Calendar keyboard behavior belongs to the primitive integration test if a shared picker already owns it.

# Multi-Step Test

Verify:

- step title/progress;
- Next/Back;
- step validation;
- focus after transition;
- data persistence;
- cross-step error recovery;
- final submit state.

# Browser / Screen Reader Evidence

Use real-browser evidence for:

- native browser form behavior;
- focus transitions;
- date-picker/popover behavior;
- sticky/fixed error summary;
- multi-step focus;
- mobile virtual keyboard/target size where relevant.

Use screen-reader checks for dynamic error/status behavior when DOM semantics alone are insufficient.

# Visual Error Styling

Error styling must preserve contrast and not rely on color only.

This skill designs the semantic requirement; styling skills implement it.

# Error Icon

An error icon can reinforce meaning.

Do not use icon-only error communication.

Decorative error icons should be hidden from AT if error text already conveys the message.

# Success State

Submission success may:

- navigate;
- show confirmation;
- update in place;
- reset.

Ensure success is perceivable programmatically where needed.

Do not steal focus unnecessarily for minor success.

# Status Region

A status region may be appropriate for:

```text
Saving…
Saved
Upload complete
```

Use proportionately.

Do not announce both button text and live region redundantly.

# Preventing Double Submit

Prefer semantic command-state ownership.

Example:

```text
submit pending
→ one command in flight
```

Do not rely only on debounce.

Server idempotency may still be required for high-risk commands.

# High-Risk Forms

Payments/account deletion/security-sensitive forms may require additional confirmation/authorization.

Accessibility contract still applies.

Do not place security logic in shared form primitives.

# Shared Form Primitives

Shared UI may own:

```text
Field
Label
Description
ErrorMessage
Fieldset
FormErrorSummary
SubmitButton
```

when these abstractions are stable and reused.

Do not create a giant `FormField` abstraction that cannot represent real control differences.

# Primitive API

A shared Field abstraction should make correct associations easy.

Example conceptual API:

```text
Field
├── Label
├── Control
├── Description
└── ErrorMessage
```

Do not force every control through identical DOM if semantics differ.

# Headless Form Primitives

If a design system/headless library provides form primitives, preserve its ARIA/focus behavior.

Do not override accessibility contracts to fit one styling implementation.

# Error Summary Shared Primitive

May be shared if multiple forms need the same accessible behavior.

Feature code supplies semantic errors and field targets.

Shared UI should not know business error rules.

# Dynamic Form Builder

If product has schema-driven forms, this skill still applies.

Generated controls need:

- stable labels;
- IDs;
- descriptions;
- validation mapping;
- grouping;
- focus;
- dynamic errors.

Do not assume generated schema automatically produces accessible forms.

# Overmodeling Audit

Flag:

- error summary for a one-field form without value;
- live region for every keystroke;
- all fields disabled during submit;
- custom validation framework added without need;
- shared form abstraction hiding control semantics;
- client duplication of complex server business rules;
- multi-step architecture for a trivial short form.

Use:

```text
PROPORTIONATE_ACCESSIBLE_FORM
UNDERMODELED_ACCESSIBILITY
OVERMODELED_FORM_FLOW
VALIDATION_OWNERSHIP_RISK
FORM_CONTRACT_NOT_REQUIRED
```

# Under-Modeled Signals

Flag:

- placeholder-only label;
- visual-only required asterisk;
- red-border-only error;
- errors not associated;
- server error disappears;
- async result race;
- hidden dynamic field blocks submit;
- date range has ambiguous From/To labels;
- multi-step focus remains on removed controls;
- duplicate submit possible.

# Final Decision

Use:

```text
ACCESSIBLE_FORM_DESIGN_READY
ACCESSIBLE_FORM_DESIGN_READY_WITH_CONDITIONS
FORM_CONTRACT_NOT_REQUIRED
VALIDATION_OWNERSHIP_REQUIRED
SERVER_ERROR_MAPPING_REQUIRED
ASYNC_VALIDATION_POLICY_REQUIRED
DYNAMIC_FIELD_POLICY_REQUIRED
MULTI_STEP_POLICY_REQUIRED
ACCESSIBILITY_REVIEW_REQUIRED
BLOCKED
```

## Output

Use `assets/accessible-form-design-record.md`.

## Completion Criteria

- [ ] Form purpose and field inventory are explicit.
- [ ] Every field has a meaningful programmatic label.
- [ ] Placeholder-only labeling is rejected.
- [ ] Help/descriptions are associated programmatically where needed.
- [ ] Required/optional semantics are visible and programmatic.
- [ ] Related controls are grouped semantically.
- [ ] Input type/autocomplete/inputmode are intentional.
- [ ] Validation ownership separates UI shape/interaction from Domain/backend invariants.
- [ ] Client validation is not treated as security/authority.
- [ ] Validation timing is explicit and not excessively disruptive.
- [ ] Error messages explain what happened and how to recover.
- [ ] Field errors are associated accessibly.
- [ ] Invalid state is not communicated only by color.
- [ ] Failed submission preserves entered values.
- [ ] Error-summary need is decided proportionately.
- [ ] Focus behavior after failed submit is explicit.
- [ ] Announcements/live regions are used proportionately.
- [ ] Submission state prevents harmful duplicate actions.
- [ ] Loading preserves accessible naming and focus.
- [ ] Server field/form errors map to stable user-facing semantics.
- [ ] Async validation defines trigger, race safety, negative vs network failure, and final server authority.
- [ ] Dynamic fields define add/remove focus, labels, stable identity, hidden-field validation, and announcement behavior.
- [ ] Date/date-range inputs define labels, format, parsing, ordering ownership, and error association.
- [ ] Multi-step forms define progress, step validation, Back/Next, focus, cross-step errors, and final submission.
- [ ] Form-library implementation remains replaceable; the accessibility contract is library-independent.
- [ ] Localization/zoom/reflow considerations are explicit.
- [ ] Sensitive data is not leaked through errors/analytics.
- [ ] Tests use accessible queries and controlled async behavior.
- [ ] Roadmap evaluations are covered: required field, async validation, server error, dynamic fields, date range, multi-step form.
- [ ] No new form/validation framework is introduced without approval.
- [ ] Final form-design decision is explicit.

## References

- Read `references/labels-descriptions-required-and-groups.md` first.
- Read `references/validation-ownership-timing-and-error-association.md`.
- Read `references/submission-error-summary-server-errors-and-status.md`.
- Read `references/async-validation-and-race-safety.md`.
- Read `references/dynamic-fields-dates-and-date-ranges.md`.
- Read `references/multi-step-forms-focus-progress-and-cross-step-errors.md`.
- Read `references/testing-localization-privacy-and-overmodeling.md`.
- Read `references/accessible-form-design-audit.md` before completion.
