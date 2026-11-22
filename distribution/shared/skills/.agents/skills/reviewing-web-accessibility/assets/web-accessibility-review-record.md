# Web Accessibility Review Record

## Context

- Review target:
- Route/component/journey:
- Review mode:
- Accessibility target:
- Browser/runtime:
- Supported themes:
- Supported viewport ranges:
- Supported input modes:
- Supported assistive technologies:
- Existing design accessibility contract:
- Existing test coverage:
- Applicable `AGENTS.md`:
- Reviewer/date:

## Scope

### Included

```text

```

### Excluded / Not Reviewed

```text

```

- Scope limitation risk:

## Evidence Inventory

| Evidence type | Performed | Tool/environment | Notes |
|---|---|---|---|
| automated scan | | | |
| manual keyboard | | | |
| focus inspection | | | |
| semantic DOM/accessibility tree | | | |
| contrast measurement | | | |
| zoom/reflow browser | | | |
| reduced motion | | | |
| touch/target size | | | |
| screen reader | | | |
| visual/browser | | | |
| code inspection | | | |

## Automated Tool Results

| Finding | Tool status | Manual validation | Final status |
|---|---|---|---|
| | VALIDATED_VIOLATION / FALSE_POSITIVE / NEEDS_MANUAL_VALIDATION / ADVISORY / NOT_APPLICABLE | | |

- Scan-only conclusion avoided:

## Review Summary

| Severity | Count |
|---|---:|
| Critical | |
| High | |
| Medium | |
| Low | |
| Advisory | |

- Confirmed findings:
- Needs validation:
- Accepted exceptions:
- False positives:

## Finding Template

### A11Y-001 — [Title]

- Severity:
- Status: OPEN / CONFIRMED / NEEDS_VALIDATION / FIXED_PENDING_VERIFICATION / VERIFIED / ACCEPTED_EXCEPTION / FALSE_POSITIVE
- Affected surface:
- User impact:
- Affected users/input modes:
- Journey importance:
- Evidence:
- Actual behavior:
- Expected behavior:
- Reproduction:
  1.
  2.
  3.
- WCAG mapping:
- WCAG mapping confidence:
- Root cause:
- Recommended fix:
- Remediation owner:
- Verification plan:
- Regression-prevention candidate:
- Notes:

## Keyboard Review

- All interactive elements reachable:
- Logical tab order:
- Enter/Space behavior:
- Escape behavior:
- Arrow-key widgets:
- No invalid keyboard traps:
- No hidden focusable content:
- Shortcuts conflicts:

## Focus Review

- Visible focus:
- Initial focus:
- Modal containment:
- Exit behavior:
- Focus restoration:
- Route/update focus:
- Sticky/fixed obstruction:
- Portal/nested overlays:

## Focus Trap Roadmap Case

- Surface:
- Containment expected:
- Escape path expected:
- Actual:
- Finding:
- Severity:
- Verification:

## Semantic Structure

- Page title:
- Language:
- Headings:
- Landmarks:
- Lists:
- Tables:
- Button/link semantics:
- Native semantics preferred:
- Custom clickable elements:
- Invalid/conflicting ARIA:

## Labels / Accessible Names

| Control | Visible label | Programmatic name | Status |
|---|---|---|---|
| | | | |

### Missing Label Roadmap Case

- Control:
- Current name:
- Placeholder-only:
- Impact:
- Finding:
- Verification:

## Color / Contrast

- Color-only meaning:
- Text contrast:
- Icon/non-text contrast:
- Focus contrast:
- Light theme:
- Dark theme:
- Other theme:

### Color-Only Error Roadmap Case

- Error surface:
- Visual communication:
- Programmatic communication:
- Impact:
- Finding:
- Verification:

## Zoom / Reflow

| Scenario | Result |
|---|---|
| narrow viewport | |
| 200% zoom | |
| 400% zoom / accepted substantial zoom | |
| long translation | |
| large text | |

- Clipping:
- Overlap:
- Page horizontal overflow:
- Essential actions lost:
- Focus obscured:

## Motion

- Motion present:
- `prefers-reduced-motion` tested:
- Non-essential motion reduced:
- Essential alternative:

### Reduced Motion Roadmap Case

- Surface:
- Motion:
- Reduced preference behavior:
- Impact:
- Finding:
- Verification:

## Touch / Target Size

| Control | Hit area | Spacing | Criticality | Result |
|---|---:|---:|---|---|
| | | | | |

### Mobile Target Size Roadmap Case

- Surface:
- Measured hit area:
- Project target/guidance:
- Alternative access:
- Impact:
- Finding:
- Verification:

## Errors / Forms

- Labels:
- Required state:
- Field descriptions:
- Error association:
- Error summary:
- Failed-submit focus:
- Server error:
- Recovery:
- Color-only error avoided:

## Dynamic Status / Live Regions

| Status | Visual update | Programmatic exposure | Announcement quality |
|---|---|---|---|
| | | | |

### Screen-Reader Status Roadmap Case

- Status:
- Expected announcement:
- Actual:
- Live region:
- Focus move:
- Duplicate announcement:
- Finding:
- Verification:

## Complex Widgets

### Dialog

- Accessible name:
- Focus entry:
- Containment:
- Escape:
- Focus restoration:
- Background interaction:

### Menu

- Semantics:
- Arrow keys:
- Escape:
- Disabled items:
- Focus restoration:

### Combobox

- Name:
- Popup relationship:
- Option semantics:
- Active/selected state:
- Keyboard:

### Tooltip / Popover

- Passive vs interactive:
- Focus access:
- Touch:
- Critical content:

### Tabs

- tablist/tab/tabpanel:
- selected state:
- keyboard:
- focus:

## Shared Primitive Regression

- Shared primitive involved:
- Local override:
- Blast radius:
- Other consumers sampled:
- Shared fix required:
- Feature-only fix:

## Exceptions

| Issue | Owner | Rationale | Mitigation | Review/expiry |
|---|---|---|---|---|
| | | | | |

## Verification Matrix

| Finding | Automated | Component | Browser | Screen reader | Visual | Manual keyboard |
|---|---|---|---|---|---|---|
| | | | | | | |

## Regression Prevention

| Finding | Prevent with | Owner |
|---|---|---|
| | lint / component test / browser test / shared primitive test / docs | |

## Release Assessment

- Decision: ACCESSIBILITY_REVIEW_PASS / ACCESSIBILITY_REVIEW_PASS_WITH_ADVISORIES / ACCESSIBILITY_REVIEW_REQUIRES_FIXES / ACCESSIBILITY_REVIEW_BLOCKED / ACCESSIBILITY_REVIEW_INCOMPLETE
- Release-policy basis:
- Blocking findings:
- Required remediation:
- Residual risks:
- Formal WCAG certification claimed: no

## Final Notes

- Unverified areas:
- Recommended follow-up:
- Next skill:
