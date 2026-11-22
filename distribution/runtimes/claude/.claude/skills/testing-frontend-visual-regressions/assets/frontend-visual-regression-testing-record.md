# Frontend Visual Regression Testing Record

## Context

- Surface:
- Repository/application:
- Visual risk:
- Existing visual environment:
- Styling profile:
- Theme system:
- Responsive strategy:
- Browser/runtime:
- Existing baseline:
- Applicable `AGENTS.md`:
- Designed/tested by/date:

## Readiness

- Visual regression justified:
- Infrastructure exists:
- Fixture can be stabilized:
- Fonts/assets stable:
- Baseline policy known:
- Initial decision:
- Conditions/blockers:

## Scope Decision

- Classification: DESIGN_SYSTEM_PRIMITIVE / RESPONSIVE_LAYOUT / THEME_VARIANT / CHART / DOCUMENT_RENDERING / PIXEL_SENSITIVE_UI / VISUAL_REGRESSION_NOT_REQUIRED
- Why visual evidence is needed:
- Why semantic tests are insufficient:
- Smallest valuable surface:
- Component vs page:
- Blast radius:

## Existing Test Infrastructure

- Tool: Playwright screenshots / Storybook test runner / Chromatic / Percy / custom image diff
- Reused:
- New tool introduced:
- Baseline storage:
- Diff artifacts:
- Local focused workflow:
- CI workflow:

## Fixture

- Fixture/story/route:
- Data source:
- Network:
- IDs:
- Dates/time:
- Locale:
- Timezone:
- Permissions:
- Feature flags:
- Long-content stress:
- Production/PII data excluded:

## Stabilization

| Source of nondeterminism | Strategy |
|---|---|
| fonts | |
| images | |
| animations | |
| caret | |
| scroll | |
| random values | |
| current time | |
| async network | |
| chart animation | |
| external CDN | |

- Arbitrary sleeps:
- Readiness condition:

## Viewport / Container Matrix

| Case | Viewport | Container | Why |
|---|---|---|---|
| narrow | | | |
| transition | | | |
| wide | | | |

- Device-preset inflation avoided:
- Container query behavior covered:
- Threshold -1/at/+1 required:

## Theme Matrix

| Surface/state | Light | Dark | Other supported |
|---|---|---|---|
| | | | |

- OS preference dependency avoided:
- Theme set deterministically:

## State Matrix

| State | Screenshot required | Why |
|---|---|---|
| default | | |
| focus-visible | | |
| disabled | | |
| loading | | |
| invalid | | |
| selected | | |
| open | | |
| error | | |

- Cartesian explosion avoided:

## Design-System Primitive

- Applicable:
- Primitive:
- Variants:
- Sizes:
- Focus:
- Disabled/loading/invalid:
- Theme coverage:
- Representative matrix:

## Responsive Layout

- Applicable:
- Narrow:
- Transition:
- Wide:
- Translation stress:
- Overflow risk:
- Sticky/fixed UI:
- Browser behavior test paired:

## Chart

- Applicable:
- Data fixed:
- Dimensions fixed:
- Labels:
- Locale:
- Theme:
- Animation disabled/stabilized:
- Canvas/SVG:
- Tolerance justification:

## Document Rendering

- Applicable:
- Page size:
- Fonts:
- Pagination:
- Margins:
- Scale:
- Content:
- Screen vs print media:
- Historical risk:

## Pixel-Sensitive UI

- Applicable:
- Contract:
- Failure impact:
- Targeted surface:
- Why image diff is appropriate:

## Baseline

- Expected image owner:
- Created/updated by:
- Reviewed by:
- Environment:
- Browser/version:
- Viewport:
- Theme:
- Baseline automatically trusted:
- Approval evidence:

## Diff Policy

- Threshold:
- maxDiffPixels:
- maxDiffPixelRatio:
- Why:
- Masks:
- Mask justification:
- Masked regression risk:
- Strict comparison possible:

## Triage

| Diff | Classification | Root cause | Action |
|---|---|---|---|
| | INTENTIONAL_CHANGE / ACCIDENTAL_REGRESSION / FLAKY_RENDER / ENVIRONMENT_DRIFT / FIXTURE_DRIFT / BASELINE_OUTDATED / NEEDS_PRODUCT_REVIEW | | |

## Intentional Change Workflow

- Product/design intent:
- Collateral diffs reviewed:
- Approval:
- Baseline update:
- Affected matrix rerun:

## Accidental Regression Workflow

- Reproduced:
- Root cause:
- Code/token/layout fix:
- Baseline unchanged:
- Rerun result:

## Failure Diagnostics

- Expected image retained:
- Actual image retained:
- Diff image retained:
- Viewport/theme/state metadata:
- Browser/runtime metadata:
- CI artifact location:

## Privacy / Security

- Customer data:
- Production screenshot:
- Email/name/PII:
- Tokens/secrets:
- Sensitive URL/query:
- Artifact access policy:

## Flake Audit

- Font:
- Browser version:
- OS:
- DPR:
- Animation:
- Network:
- Time:
- Locale:
- Scroll:
- Image loading:
- Chart rendering:
- Retry dependency:

## Test Layering

- Semantic/component tests:
- Accessibility tests:
- Browser responsive tests:
- Visual test unique risk:
- E2E duplication:
- Visual-only business assertions avoided:

## Roadmap Responsibilities

### Scope Selection
- Decision:
- Evidence:

### Stable Fixtures / Viewports
- Decision:
- Evidence:

### Themes / Responsive States
- Decision:
- Evidence:

### Intentional vs Accidental Triage
- Decision:
- Evidence:

## Standard Priority Surfaces

| Surface | Applicable | Covered |
|---|---|---|
| design-system primitives | | |
| complex responsive layout | | |
| theme variants | | |
| charts | | |
| document rendering | | |
| high-risk pixel-sensitive UI | | |

## Execution Evidence

- Focused command:
- Result:
- CI visual job:
- Result:
- Baseline update command/process:
- Diff artifacts:
- Duration:
- Flakiness:

## Over/Under-Testing Audit

- Every component snapshotted:
- Cartesian state matrix:
- Full page for local risk:
- Live/random data:
- Unnecessary masks:
- Excessive threshold:
- Critical pixel risk missing:
- Decision: PROPORTIONATE_VISUAL_COVERAGE / OVERTESTED_VISUAL_MATRIX / UNDERTESTED_PIXEL_RISK / VISUAL_REGRESSION_NOT_REQUIRED

## Final Decision

- Decision:
- Conditions:
- Blocking issue:
- Next skill:
- Required follow-up:
