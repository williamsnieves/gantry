---
name: testing-frontend-visual-regressions
description: Designs and maintains frontend visual-regression tests for UI whose appearance is itself part of the product contract. Use to select proportional screenshot scope, stabilize deterministic fixtures and rendering conditions, define meaningful viewport/container/theme matrices, test design-system primitives, complex responsive layouts, charts, document rendering, and other pixel-sensitive UI, and triage intentional versus accidental image changes. Prefer existing Playwright screenshot, Storybook/Chromatic, Percy, or custom image-diff infrastructure. Do not snapshot every component, use visual tests to replace semantic/behavior tests, approve baselines blindly, or hide nondeterminism behind excessive pixel tolerances.
---

# Testing Frontend Visual Regressions

## Purpose

Use image-based regression evidence when visual appearance is itself a meaningful contract.

The core workflow is:

```text
identify visual risk
→ choose the smallest valuable visual surface
→ stabilize state/data/environment
→ define representative viewports/themes
→ capture baseline
→ compare
→ triage diff
→ approve intentional change or fix regression
```

Visual regression is not a replacement for semantic tests.

Use:

```text
behavior/accessibility tests
+
visual regression
```

when both interaction and appearance matter.

## Governing Standard

Visual regression tests SHOULD be considered for:

- design-system primitives;
- complex responsive layouts;
- theme variants;
- charts;
- document rendering;
- high-risk pixel-sensitive UI.

Component tests SHOULD prioritize accessible roles/names and user behavior.

Avoid DOM/class assertions unless styling is actually the behavior under test.

Responsive and theme behavior should be verified.

## Potential Environments

The roadmap explicitly allows:

```text
Playwright screenshots
Storybook test runner
Chromatic
Percy
custom image diff
```

Use the infrastructure already selected by the repository.

Do not introduce a new visual-regression platform merely because this skill is activated.

## Use When

- A design-system primitive has a stable visual contract.
- Responsive layout can regress without semantic failure.
- Theme changes can break contrast, tokens, or composition.
- Charts or document rendering are pixel-sensitive.
- Overlay/layering behavior matters visually.
- Typography/layout changes have meaningful risk.
- A previously observed visual bug needs regression coverage.
- A high-risk page/template requires screenshot protection.
- A component explorer already provides deterministic fixtures.
- A PR contains intended broad visual change requiring baseline review.

## Do Not Use When

- The behavior is primarily semantic and can be proven cheaper.
- A unit/component test already fully proves the risk.
- The screenshot would be highly nondeterministic.
- The UI changes intentionally on every run.
- The target contains live timestamps/random content without stabilization.
- The test exists only to raise screenshot coverage numbers.
- The repository has no accepted visual test environment and introducing one is out of scope.
- The expected result is text/data behavior rather than appearance.

## Inputs

- Visual-risk surface.
- Existing visual test environment.
- Accepted styling/theme system.
- Supported responsive states.
- Stable fixture strategy.
- Fonts/assets loading strategy.
- Animation/motion behavior.
- Browser/OS/runtime used by CI.
- Pixel-diff configuration.
- Existing baselines.
- Review/approval ownership.
- Accessibility/component test coverage.
- Repository-local `AGENTS.md`.

## Outputs

- Visual-test scope decision.
- Fixture stabilization plan.
- Viewport/container matrix.
- Theme matrix.
- State matrix.
- Baseline strategy.
- Diff tolerance/masking policy.
- Triage workflow.
- Intentional-change approval process.
- Visual-regression testing record.

# Readiness Gate

Use one:

```text
READY_TO_ADD_VISUAL_REGRESSION
READY_WITH_CONDITIONS
VISUAL_REGRESSION_NOT_REQUIRED
VISUAL_TEST_INFRASTRUCTURE_REQUIRED
FIXTURE_STABILIZATION_REQUIRED
BASELINE_POLICY_REQUIRED
FONT_ASSET_STABILITY_REQUIRED
BLOCKED
```

# Visual Scope Decision

Classify the target:

```text
DESIGN_SYSTEM_PRIMITIVE
RESPONSIVE_LAYOUT
THEME_VARIANT
CHART
DOCUMENT_RENDERING
PIXEL_SENSITIVE_UI
VISUAL_REGRESSION_NOT_REQUIRED
```

Do not snapshot by default.

Ask:

```text
Would a visual defect matter to users
while semantic tests could still pass?
```

If no, visual regression may add little value.

# Smallest Valuable Surface

Prefer the smallest surface that contains the visual risk.

Examples:

```text
Button stories
Dialog story
responsive Card fixture
dashboard layout
PDF/document preview page
chart component
```

Do not screenshot the entire application for a one-component spacing risk unless integration context is what matters.

# Component vs Page Screenshot

Use component-level visual tests when:

- component can be rendered deterministically;
- visual contract is local;
- shared primitive changes have broad reuse.

Use page/journey screenshot when:

- layout interaction across regions matters;
- sticky/fixed positioning matters;
- full-page responsive composition matters;
- document rendering requires the complete page.

# Design-System Primitives

Good candidates:

```text
Button
Input
Dialog
Select
Tooltip
Menu
Tabs
Card
Badge
Toast
```

but only for meaningful shared visual states.

Do not capture every prop combination.

# State Selection

Choose representative states:

```text
default
hover
focus-visible
active
disabled
loading
invalid
selected
open
empty
error
success
```

only where visual behavior is part of the contract.

Do not generate a Cartesian product automatically.

# Representative Matrix

For multiple axes, prefer:

```text
defaults
extremes
risky compounds
accessibility states
theme-sensitive states
responsive boundaries
```

over exhaustive combinations.

# Visual State Ownership

A screenshot should represent accepted product state.

Avoid relying on:

- asynchronous live APIs;
- random fixture generation;
- current date;
- user-specific production data.

Use deterministic fixture/builders.

# Stable Fixtures

A stable fixture should control:

```text
copy
numbers
dates
IDs
image assets
loading state
feature flags
permissions
locale
timezone
theme
viewport
container size
```

where those affect pixels.

# Fixture Realism

Deterministic does not mean unrealistic.

Fixtures should contain representative:

```text
long labels
empty values
dense content
large numbers
translation stress
```

when these affect visual risk.

# Long Content

Include visual stress fixtures where useful:

```text
German translation
long user name
long URL
large currency
multi-line error
```

Do not rely only on ideal English mock copy.

# Viewport Strategy

Choose viewports from accepted responsive behavior.

Good matrix:

```text
narrow
important transition boundary
wide
```

Potentially:

```text
threshold - 1
threshold
threshold + 1
```

for fragile transitions.

Do not screenshot every standard device size.

# Container Query Components

If component responsiveness depends on its container, vary container width rather than only viewport.

Example:

```text
Card in 320px container
Card in 720px container
```

at the same viewport.

Do not miss local layout regressions by testing viewport only.

# Responsive Layouts

The frontend standard specifically calls out complex responsive layouts.

Visual tests are useful for:

- grid track collapse;
- toolbar wrapping;
- card composition;
- tables;
- sticky content;
- overflow;
- translated CTA behavior.

Still pair with semantic/overflow/browser tests where required.

# Theme Matrix

For supported themes, test representative:

```text
light
dark
high contrast/brand
```

according to product support.

Do not snapshot unsupported speculative themes.

# Theme Test Selection

Not every story needs every theme.

Prioritize:

- shared primitives;
- token-heavy surfaces;
- danger/status states;
- overlays;
- charts;
- surfaces/text relationships.

# Token Changes

A broad token change can alter many snapshots.

Treat mass diffs as a signal requiring deliberate review.

Do not bulk-accept thousands of baseline changes without understanding the token impact.

# Dark Mode

Stabilize theme selection before capture.

Do not depend on host OS preference in CI unless that is explicitly what the test verifies.

Set the theme deterministically.

# Fonts

Font rendering is a major source of visual instability.

Ensure:

- intended fonts are available;
- loading completes before capture;
- fallback font does not intermittently render;
- CI/browser image is stable.

Do not screenshot during font swap.

# Web Fonts

Wait for:

```text
document.fonts.ready
```

or repository-approved equivalent when necessary.

Do not add arbitrary sleep.

# Images

Control:

- asset URLs;
- image loading;
- dimensions/aspect ratio;
- placeholders;
- external CDN variability.

Prefer local deterministic assets for screenshot fixtures.

# SVG / Icons

Ensure icon version/source is stable.

External icon fonts/CDNs may make baselines flaky.

# Animations

Animations must be stabilized.

Options:

```text
disable non-essential animations
prefers-reduced-motion
Playwright screenshot animation disabling
freeze transition state
```

Use repository-supported behavior.

Do not hide an actual reduced-motion regression if reduced motion itself is the behavior under test.

# Motion State

If animation visuals are themselves the contract, capture deterministic key states intentionally rather than arbitrary timing frames.

# Caret / Cursor

Text carets and blinking cursors can produce diff noise.

Use the visual framework's caret-hiding option or ensure focus target is intentional.

Do not mask the entire focused control if focus style is what you need to test.

# Scroll Position

Set explicit scroll position before capture.

Full-page screenshots should have deterministic content height.

Do not rely on previous test scroll state.

# Sticky / Fixed UI

Visual tests can prove:

- overlap;
- stacking;
- clipping;
- sticky positioning.

But capture at a meaningful scroll state.

# Overlays

For Dialog/Menu/Tooltip/Popover:

- open deterministically;
- wait for positioning;
- stabilize portal;
- capture relevant stacking context;
- preserve focus styling if part of contract.

Do not screenshot while entry animation is mid-flight.

# Charts

The standard explicitly calls out charts.

Stabilize:

```text
data
dimensions
labels
time range
locale
random IDs
animation
canvas/SVG rendering
```

Do not use live market/production data.

# Chart Visual Risk

Visual tests are good for:

- bars/lines disappearing;
- axis label clipping;
- legend collision;
- color/theme regressions;
- responsive chart sizing.

Behavior/data correctness should be tested separately.

# Canvas Charts

Canvas rasterization can vary by browser/runtime.

Pin the supported browser/runtime and use tolerances cautiously.

Do not set a huge diff threshold to hide unstable rendering.

# Document Rendering

The standard explicitly calls out document rendering.

Potential targets:

```text
invoice preview
certificate
print layout
template editor final preview
PDF-like canvas/page
```

Stabilize:

- page size;
- fonts;
- pagination;
- content;
- margins;
- scale;
- browser print/render environment.

# Print / Page Media

If print CSS is part of the product, capture the correct media mode using supported browser tooling.

Do not assume screen screenshot proves print layout.

# High-Risk Pixel-Sensitive UI

Examples:

```text
email/document template designer
drag/drop editor preview
barcode/QR layout
signature region
fixed-size printable artifact
data visualization
```

Use visual regression where tiny layout changes can be product defects.

# Baseline Creation

A baseline is approved expected output.

Record:

```text
who created/approved it
why the state is expected
environment
browser
viewport/theme
```

Do not treat the first screenshot as correct automatically.

# Baseline Ownership

Baseline review should be owned by the team responsible for UI/product/design behavior.

Do not allow bots to self-approve visual changes.

# Baseline Storage

Follow existing repository/platform strategy:

```text
committed images
Chromatic cloud
Percy cloud
artifact service
custom baseline store
```

Do not add parallel baseline storage.

# Intentional Visual Change

When product/design intentionally changes appearance:

```text
implementation change
→ visual diff
→ verify change matches intent
→ review collateral diffs
→ approve baseline
```

Do not “fix” a correct intentional diff back to old pixels.

# Accidental Regression

When unexpected:

```text
visual diff
→ reproduce
→ identify root cause
→ fix code/token/layout
→ rerun
→ baseline stays unchanged
```

Do not update baseline to make CI green.

# Triage Categories

Use:

```text
INTENTIONAL_CHANGE
ACCIDENTAL_REGRESSION
FLAKY_RENDER
ENVIRONMENT_DRIFT
FIXTURE_DRIFT
BASELINE_OUTDATED
NEEDS_PRODUCT_REVIEW
```

# Diff Triage Record

For each meaningful diff record:

```text
surface
expected state
what changed
classification
root cause
action
approval evidence
```

# Pixel Threshold

Prefer strict comparison when rendering is stable.

Use threshold only for known small antialiasing/render variance.

Do not start with broad tolerance.

# Threshold Types

Possible tool settings:

```text
maxDiffPixels
maxDiffPixelRatio
threshold
```

Use the smallest accepted value.

Document why.

# Threshold Anti-Pattern

Bad:

```text
allow 20% difference
```

because tests are flaky.

Fix the source of nondeterminism first.

# Masking

Mask only content that is:

- truly nondeterministic;
- irrelevant to visual contract;
- impossible/expensive to stabilize.

Examples may include a third-party timestamp or external avatar.

Do not mask the region where the regression could occur.

# Dynamic Regions

Preferred order:

```text
stabilize
→ fixture
→ freeze
→ deterministic fake
→ mask as last resort
```

# Screenshot Clipping

Component screenshot:

```text
locator.screenshot()
```

can reduce noise.

Full-page screenshot is useful when page composition is the risk.

Choose intentionally.

# Browser Pinning

Use a stable supported browser version/container in CI.

Do not compare baselines across arbitrary local browsers/OSes as if rendering is identical.

# OS Rendering

Font/antialias differences can occur across OS.

Prefer same CI image/environment used for baseline generation and comparison.

# Device Scale Factor

Pin if the visual environment depends on it.

Do not regenerate baselines from different DPR accidentally.

# Timezone / Locale

Pin them when copy/date/number formatting affects pixels.

Use explicit locale fixtures for translation tests.

# Color Scheme

Set supported theme explicitly.

Do not let CI host preference choose pixels.

# Reduced Motion

If the screenshot environment disables animations via reduced-motion, document that.

Separately test reduced-motion behavior where accessibility contract requires it.

# Network

Avoid external network dependencies for visual fixtures.

Use:

```text
local assets
MSW
fixture routes
story data
```

where appropriate.

# Loading Completion

Wait on meaningful readiness:

```text
visible expected content
network idle when reliable
font ready
chart rendered flag
document ready state
known loader disappears
```

Avoid arbitrary sleeps.

# Storybook / Component Explorer

If Storybook is already used, it is a strong fixture surface for shared primitives and state matrices.

Stories should be deterministic and represent public component states.

Do not make test-only stories that diverge from actual component usage semantics.

# Chromatic

Useful when already selected for:

- story snapshots;
- cloud baseline review;
- per-PR diff review.

Do not assume Chromatic approval equals semantic/accessibility correctness.

# Percy

Same principle: use if repository already selected it.

Keep interaction/accessibility tests separate.

# Playwright Screenshots

Useful for:

- component/page screenshots;
- responsive states;
- real browser rendering;
- overlays;
- document preview;
- page composition.

Use stable locators and readiness conditions.

# Custom Image Diff

Acceptable when repository already owns it.

Ensure it provides:

- deterministic baseline store;
- diff artifact;
- meaningful failure output;
- threshold policy;
- review workflow.

Do not build custom image infrastructure casually.

# Failure Diagnostics

On failure preserve:

```text
actual screenshot
expected baseline
diff image
viewport/theme/state metadata
test name
browser/runtime
```

The visual failure should be diagnosable without rerunning locally first.

# Artifact Retention

Follow CI artifact retention policy.

Do not upload sensitive/private user data in screenshots.

# Privacy

Visual fixtures must not contain:

```text
real customer PII
production screenshots
auth tokens
private messages
sensitive internal data
```

Use synthetic data.

# Secrets

Screenshot artifacts can leak data.

Audit:

- URL query;
- user name/email;
- tokens;
- console overlays;
- internal environment labels.

# Accessibility

Visual regression cannot prove accessibility.

It can support checks for:

- focus-visible appearance;
- contrast/theme surface regressions;
- clipping at zoom fixtures;
- reduced-motion visual state.

But pair with semantic/browser accessibility tests.

# Focus Visuals

For shared interactive primitives, capture representative `focus-visible` state if focus styling is a visual contract.

Do not rely only on screenshot; keyboard/focus behavior must be tested elsewhere.

# Contrast

Image diff does not measure WCAG contrast.

Use token/accessibility review tools separately.

# Responsive Overflow

Screenshots can expose clipping/overflow, but objective page-overflow assertions may still be needed.

Do not depend solely on human image review for invisible scrollWidth regressions.

# Test Layering

Recommended:

```text
Domain/Application
→ behavior

adapter
→ provider/storage contract

hook/component
→ state + interaction

visual
→ appearance

E2E
→ critical cross-boundary journey
```

Do not duplicate every branch visually.

# When Visual Regression Is Not Required

Use:

```text
VISUAL_REGRESSION_NOT_REQUIRED
```

when:

- UI is simple;
- semantic tests cover the meaningful risk;
- visual output changes frequently by design;
- screenshot stabilization cost exceeds product risk.

This is a valid outcome.

# Regression Bug Placement

If a bug is:

```text
wrong business value
```

put regression at Domain/Application/component boundary.

If bug is:

```text
same values but wrong spacing/overflow/theme/pagination
```

visual regression may be appropriate.

# Responsive Bug Example

Bug:

```text
CTA overlaps secondary action at 200% zoom
```

Use:

- responsive/browser accessibility test for reflow behavior;
- visual screenshot at the failing viewport if image evidence adds durable value.

Do not rely on screenshot alone for accessibility compliance.

# Theme Bug Example

Bug:

```text
danger text becomes invisible in dark theme
```

Use:

- semantic token/contrast verification;
- representative visual regression to catch future theme mapping drift.

# Visual Coverage Budget

Visual suites can be expensive.

Prioritize by:

```text
reuse/blast radius
pixel sensitivity
historical regression frequency
theme/responsive complexity
user impact
```

# Baseline Count

More baselines increase review/maintenance cost.

Avoid dozens of near-duplicate screenshots.

# Sharding / Parallelism

Use existing runner features if suite becomes large.

Do not introduce distributed infrastructure prematurely.

# Flake Diagnosis

Common causes:

```text
font loading
animations
network
random data
time
browser version
OS rendering
caret
scroll position
image loading
chart animation
async layout shift
```

Fix source first.

# Retry Policy

Retries can help distinguish infrastructure flake, but should not normalize flaky screenshots.

A test that passes only on retry needs investigation.

# Environment Drift

When many unrelated screenshots change:

check:

```text
browser version
fonts
OS image
device scale
token/build change
Storybook global decorators
CSS reset
theme provider
```

before reviewing each diff as product change.

# Fixture Drift

If fixture data changed intentionally, decide whether visual baseline should change.

Do not merge fixture changes and broad visual refactors without clear review when avoidable.

# Baseline Review Size

Large intentional redesigns can produce massive diffs.

Consider:

```text
split baseline change
document intended visual scope
review representative surfaces first
```

rather than blind bulk approval.

# Design Sign-Off

If team policy requires design approval for baseline changes, record it.

Do not invent approval gates not present in repository policy.

# CI Policy

Potential:

```text
PR visual diff
blocking on unapproved changes
non-blocking advisory
nightly document/chart suite
```

Follow accepted repository policy.

# Local Workflow

Developers should be able to:

```text
run focused visual test
inspect diff
update one approved baseline
```

Do not require regenerating the entire baseline suite for a local component change.

# Update Baselines

Baseline update should be explicit.

Example conceptual flow:

```text
review diff
→ confirm intentional
→ update approved baseline
```

Never use automatic baseline overwrite on test failure.

# Triage Workflow

1. confirm fixture/environment stability;
2. inspect actual/expected/diff;
3. classify change;
4. reproduce if unexpected;
5. fix regression or verify intent;
6. obtain required approval;
7. update baseline only for intentional change;
8. rerun affected matrix.

# Visual Regression Record

Use:

```text
VISUAL_BASELINE_STABLE
INTENTIONAL_VISUAL_CHANGE_APPROVED
ACCIDENTAL_VISUAL_REGRESSION
FLAKY_VISUAL_TEST
ENVIRONMENT_DRIFT
FIXTURE_DRIFT
VISUAL_REVIEW_REQUIRED
```

# Evaluation — Design-System Primitive

Verify shared primitive in a representative matrix:

```text
variant
size
focus
disabled/loading/invalid if visually relevant
theme
```

without exhaustive Cartesian coverage.

# Evaluation — Responsive Layout

Verify:

```text
narrow
transition
wide
```

and container widths where component-context responsiveness matters.

# Evaluation — Theme Variant

Verify supported theme mappings on representative surfaces.

# Evaluation — Chart

Verify deterministic data, dimensions, labels, theme, and animation stability.

# Evaluation — Document Rendering

Verify page size, fonts, pagination, content, scale, and margins.

# Evaluation — High-Risk Pixel-Sensitive UI

Verify the specific high-risk visual contract at the smallest meaningful surface.

# Over-Testing Audit

Flag:

- snapshot every component;
- every prop permutation captured;
- page screenshot for local icon change;
- visual test duplicating semantic unit coverage;
- giant baseline suite with low product value.

Use:

```text
PROPORTIONATE_VISUAL_COVERAGE
OVERTESTED_VISUAL_MATRIX
UNDERTESTED_PIXEL_RISK
VISUAL_REGRESSION_NOT_REQUIRED
```

# Under-Testing Audit

Flag:

- design-system primitives with no theme coverage;
- complex responsive layout only tested at desktop;
- chart screenshot uses random/live data;
- document renderer has no visual regression despite historical layout defects;
- baselines frequently accepted without triage;
- no diff artifacts retained.

# Final Decision

Use:

```text
VISUAL_REGRESSION_TESTS_READY
VISUAL_REGRESSION_TESTS_READY_WITH_CONDITIONS
VISUAL_REGRESSION_NOT_REQUIRED
VISUAL_INFRASTRUCTURE_REQUIRED
FIXTURE_STABILIZATION_REQUIRED
BASELINE_REVIEW_REQUIRED
FLAKY_VISUAL_TESTS_REQUIRE_FIX
BLOCKED
```

## Output

Use `assets/frontend-visual-regression-testing-record.md`.

## Completion Criteria

- [ ] Visual risk is explicit.
- [ ] Visual regression is justified rather than automatic.
- [ ] Existing repository visual-test infrastructure is reused.
- [ ] The smallest valuable screenshot surface is selected.
- [ ] Fixtures are deterministic and representative.
- [ ] Dates/IDs/randomness/locale/timezone are stable where relevant.
- [ ] Fonts/assets are loaded deterministically before capture.
- [ ] Animations/caret/scroll are stabilized appropriately.
- [ ] Viewports come from meaningful responsive states, not device coverage inflation.
- [ ] Container width is varied where container queries own responsiveness.
- [ ] Supported themes are covered proportionately.
- [ ] Representative visual states are selected without Cartesian explosion.
- [ ] Design-system primitive coverage is proportionate.
- [ ] Complex responsive layouts are covered where visual risk exists.
- [ ] Charts use deterministic data/dimensions/animation state.
- [ ] Document rendering uses stable page/font/pagination conditions.
- [ ] Pixel-sensitive UI has targeted visual protection.
- [ ] Baselines are reviewed rather than auto-trusted.
- [ ] Intentional and accidental changes have separate workflows.
- [ ] Baselines are updated only after intentional visual change is verified.
- [ ] Diff thresholds/masks are minimal and documented.
- [ ] Nondeterminism is fixed before tolerance is increased.
- [ ] CI preserves actual/expected/diff artifacts.
- [ ] Screenshots contain no production/customer-sensitive data.
- [ ] Visual tests do not replace semantic/accessibility/component tests.
- [ ] Visual coverage does not duplicate every higher/lower-level branch.
- [ ] Roadmap responsibilities are covered: scope selection, stable fixtures/viewports, themes/responsive states, intentional-vs-accidental triage.
- [ ] Standard priority surfaces are addressed where applicable: design-system primitives, responsive layouts, themes, charts, document rendering, pixel-sensitive UI.
- [ ] Final visual-testing status is explicit.

## References

- Read `references/selecting-visual-regression-scope.md` first.
- Read `references/stabilizing-fixtures-fonts-assets-animation-and-environment.md`.
- Read `references/viewports-container-queries-themes-and-state-matrices.md`.
- Read `references/charts-documents-and-pixel-sensitive-ui.md`.
- Read `references/baselines-diff-thresholds-and-triage.md`.
- Read `references/playwright-storybook-chromatic-percy-and-tool-selection.md`.
- Read `references/privacy-ci-artifacts-flake-and-maintenance.md`.
- Read `references/frontend-visual-regression-testing-audit.md` before completion.
