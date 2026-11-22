# Accessible Form Design Record

## Context

- Form/journey:
- Repository/application:
- Accessibility target:
- Existing form library:
- Shared form primitives:
- Application/Domain validation:
- Backend validation:
- Server error contract:
- Localization:
- Routing/multi-step:
- Applicable `AGENTS.md`:
- Designed by/date:

## Readiness

- Form purpose known:
- Field inventory known:
- Validation ownership known:
- Server error contract known:
- Async validation known:
- Dynamic fields known:
- Multi-step behavior known:
- Initial decision:
- Conditions/blockers:

## Field Inventory

| Field | Type | Label | Required | Description | Validation owner |
|---|---|---|---|---|---|
| | | | | | |

## Labels

- Programmatic labels:
- Visible labels:
- Placeholder-only labels:
- Icon-only controls:
- Label wording:

## Descriptions / Help

| Field | Help text | Association |
|---|---|---|
| | | |

- Help retained when error appears:
- Format guidance:

## Required / Optional

- Convention:
- Native `required`:
- `aria-required`:
- Asterisk explanation:
- Optional labels:

### Required Field Roadmap Case

- Field:
- Visible required state:
- Programmatic required state:
- Validation timing:
- Error:
- Failed-submit behavior:

## Groups

| Group | Semantic structure | Group label/legend |
|---|---|---|
| | | |

- Radio groups:
- Checkbox groups:
- Date range:
- Repeating groups:

## Input Semantics

| Field | type | autocomplete | inputmode | Why |
|---|---|---|---|---|
| | | | | |

## Validation Ownership Matrix

| Rule | Ownership | Authority |
|---|---|---|
| | UI_SHAPE_VALIDATION / UI_INTERACTION_VALIDATION / DOMAIN_VALIDATION / BACKEND_AUTHORITATIVE_VALIDATION / SHARED_SEMANTICS_BACKEND_AUTHORITATIVE / UNKNOWN_REQUIRES_DECISION | |

- Complex business rule duplicated client-side:
- Client validation treated as security:

## Validation Timing

| Field/rule | Trigger | Why |
|---|---|---|
| | ON_SUBMIT / ON_BLUR / ON_CHANGE_AFTER_INTERACTION / ON_CHANGE_IMMEDIATE / ASYNC_AFTER_STABLE_INPUT | |

- Premature errors avoided:
- Touched/dirty implementation leakage avoided:

## Field Error Contract

| Field | Error message | `aria-invalid` | Association |
|---|---|---|---|
| | | | |

- Color-only error avoided:
- Error copy actionable:
- Localized:
- Stable IDs:

## Failed Submit

- Values preserved:
- Errors rendered:
- Error summary:
- Focus target:
- First invalid field:
- Announcement:
- Duplicate submit prevented:

## Error Summary

- Required:
- Why:
- Heading:
- Summary focus:
- Links to fields:
- Small-form overkill avoided:

## Submission State

```text

```

- Idle:
- Submitting:
- Validation failure:
- Server failure:
- Success:
- Duplicate activation policy:
- Submit control disabled:
- Entire form disabled:
- Accessible loading label/busy state:

## Server Errors

| Server result | UI classification | Field/form mapping | Focus/status |
|---|---|---|---|
| | FIELD_SERVER_ERROR / FORM_SERVER_ERROR / AUTHORIZATION_ERROR / CONFLICT / NETWORK_ERROR / UNKNOWN_ERROR | | |

### Server Error Roadmap Case

- Scenario:
- User input preserved:
- Raw provider message excluded:
- Field mapping:
- Form-level message:
- Recovery:
- Verification:

## Async Validation

- Applicable:
- Field:
- Trigger:
- Input precondition:
- Debounce/stability:
- Loading status:
- Latest-wins/cancellation:
- Negative result:
- Network failure:
- Final server authority:
- Announcement:

### Async Validation Roadmap Case

- Scenario:
- Race condition:
- Expected:
- Verification:

## Dynamic Fields

- Applicable:
- Add control:
- Remove control:
- Group naming:
- Stable item identity:
- Unique IDs:
- Focus after add:
- Focus after remove:
- Announcement:
- Hidden-field value policy:
- Hidden-field validation policy:
- Reordering:

### Dynamic Fields Roadmap Case

- Scenario:
- Expected:
- Verification:

## Dates / Date Range

- Input strategy: native / text + parser / accessible date-picker / segmented
- Locale/format:
- Format help:
- Parsing:
- Calendar primitive:
- Keyboard behavior owner:

### Date Range

- Group label:
- Start label:
- End label:
- Ordering rule:
- Ordering owner:
- Business constraints:
- Error association:
- Group vs field error:
- Verification:

## Multi-Step Form

- Applicable:
- Step count:
- Step titles:
- Progress communication:
- Current-step semantics:
- Next:
- Back:
- Save/exit:
- Current-step validation:
- Final validation:
- Values preserved:
- Focus after step change:
- Cross-step server error:
- Browser history:
- Draft persistence:

### Multi-Step Roadmap Case

- Scenario:
- Failed Next:
- Failed final submit:
- Cross-step field error:
- Verification:

## Focus Plan

| Event | Focus target |
|---|---|
| initial form | |
| failed submit | |
| server field error | |
| server form error | |
| dynamic add | |
| dynamic remove | |
| next step | |
| back step | |
| cross-step error | |
| success | |

## Status / Announcement Plan

| Event | Mechanism | Politeness |
|---|---|---|
| async validation | | |
| submit pending | | |
| validation failure | | |
| server failure | | |
| success | | |

- No announcement spam:
- No redundant focus + live-region duplication:

## Localization / Reflow

- Long labels:
- Long errors:
- Date/number locale:
- Zoom:
- Fixed label widths avoided:
- RTL:

## Privacy / Security

- Sensitive values in errors:
- Raw provider errors:
- Validation analytics:
- PII logging:
- Client validation authority:

## Test Matrix

| Roadmap case | Test boundary | Expected |
|---|---|---|
| required field | component/form integration | |
| async validation | controlled async hook/component | |
| server error | component + Application fake | |
| dynamic fields | component/browser | |
| date range | component + primitive contract | |
| multi-step form | component/browser/E2E | |

- Accessible queries:
- Arbitrary sleeps avoided:
- Browser evidence:
- Screen-reader evidence:
- No raw provider error mocking at wrong layer:

## Over/Under-Modeling Audit

- Error summary for trivial form:
- Live region per keystroke:
- Entire form disabled during submit:
- New validation framework:
- Giant shared FormField abstraction:
- Business rules duplicated:
- Placeholder-only label:
- Red-border-only error:
- Hidden invalid fields:
- Cross-step focus failure:
- Decision: PROPORTIONATE_ACCESSIBLE_FORM / UNDERMODELED_ACCESSIBILITY / OVERMODELED_FORM_FLOW / VALIDATION_OWNERSHIP_RISK / FORM_CONTRACT_NOT_REQUIRED

## Final Decision

- Decision:
- Conditions:
- Blocking issue:
- Next skill:
- Required follow-up:
