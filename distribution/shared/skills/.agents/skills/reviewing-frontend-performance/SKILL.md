---
name: reviewing-frontend-performance
description: Performs an evidence-driven frontend performance review. Use when a page, route, component, chart, list, or interaction is slow, heavy, janky, memory-hungry, or suspected of unnecessary work. Inspect Core Web Vitals, route loading, bundle size, rendering frequency, network waterfalls, duplicate requests, memory, long tasks, interaction latency, large collections, and expensive transformations. Recommend architectural fixes before micro-optimization; account for React Compiler or equivalent optimizers before adding manual memoization. Delegate true scaling/data-structure questions to analyzing-algorithmic-complexity, and do not diagnose performance from code smell alone without runtime/build/network evidence.
...
---

# Reviewing Frontend Performance

## Purpose

Investigate frontend performance using evidence and identify the smallest high-leverage fix.

Core workflow:

```text
user-visible symptom
→ reproduce
→ establish measurement
→ isolate bottleneck category
→ identify root cause
→ prefer architectural fix
→ invoke algorithmic complexity analysis when relevant
→ verify before/after
```

This skill answers:

```text
Why is this frontend experience slow or heavy?
```

It does not answer only:

```text
What is the Big O of this loop?
```

Use `analyzing-algorithmic-complexity` when scaling or data-structure complexity is a material part of the bottleneck.

## Governing Standard

Performance work MUST be evidence-driven.

Measure as applicable:

- Core Web Vitals;
- bundle size;
- route loading;
- rendering frequency;
- network waterfalls;
- memory;
- interaction latency;
- long tasks.

Prefer architectural fixes:

- reduce work;
- improve data boundaries;
- split routes or features;
- remove unnecessary dependencies;
- virtualize large collections;
- cache at the correct layer;
- avoid duplicated requests.

Do not add memoization everywhere as a substitute for measurement.

Large third-party libraries SHOULD be reviewed before adoption.

## Roadmap Evaluations

This skill MUST cover:

```text
unnecessary rerenders
large dependency
duplicated request
unvirtualized list
route bundle
expensive chart
```

## Use When

- UI feels slow or janky.
- Interaction latency is high.
- A route loads too much JavaScript.
- A component rerenders more than expected.
- Network requests duplicate or waterfall.
- A large list freezes or drops frames.
- A chart takes too long to preprocess/render.
- Memory grows unexpectedly.
- Core Web Vitals regress.
- A dependency materially increases route/bundle cost.
- A performance regression appears after a change.
- A route/page is fast locally but slow in deployed conditions.
- A code review identifies a plausible performance risk that needs evidence.

## Do Not Use When

- The task is purely Big O analysis.
- The issue is primarily backend/DB latency with no meaningful frontend work.
- The issue is only visual correctness.
- The task is testing correctness rather than performance.
- The problem is security/privacy/accessibility.
- The user only wants a theoretical optimization with no performance requirement.
- There is no measurable symptom and no accepted risk requiring preventive analysis.

## Inputs

- User-visible symptom.
- Reproduction route/interaction.
- Target browser/device class.
- Production or representative performance evidence.
- Core Web Vitals if relevant.
- React Profiler/browser Performance trace.
- Bundle/build analysis.
- Network trace.
- Memory evidence.
- Route/module graph.
- Data sizes.
- Existing server-state/cache strategy.
- React Compiler/equivalent optimizer status.
- Existing performance budgets.
- Applicable `AGENTS.md`.

## Outputs

- Review scope.
- Performance symptom.
- Evidence inventory.
- Bottleneck classification.
- Root-cause findings.
- Severity/impact.
- Recommended architectural fix.
- Algorithmic-complexity handoff when needed.
- Before/after verification plan.
- Frontend performance review record.

# Readiness Gate

Use:

```text
READY_TO_REVIEW_FRONTEND_PERFORMANCE
READY_WITH_CONDITIONS
PERFORMANCE_REVIEW_NOT_REQUIRED
REPRODUCTION_REQUIRED
MEASUREMENT_REQUIRED
PRODUCTION_EVIDENCE_REQUIRED
BUNDLE_ANALYSIS_REQUIRED
NETWORK_EVIDENCE_REQUIRED
ALGORITHMIC_ANALYSIS_REQUIRED
BLOCKED
```

# Evidence First

Do not conclude:

```text
useMemo missing → performance bug
large component → performance bug
many functions → performance bug
Context → performance bug
```

without evidence.

Begin with:

```text
what is slow
where
under what input/device/network
how often
what measurement proves it
```

# Evidence Types

Possible:

```text
CORE_WEB_VITALS
BROWSER_PERFORMANCE_TRACE
REACT_PROFILER
BUNDLE_ANALYZER
BUILD_MANIFEST
NETWORK_WATERFALL
RUM
LIGHTHOUSE_LAB
MEMORY_PROFILE
LONG_TASK_TRACE
CPU_PROFILE
CUSTOM_USER_TIMING
CONTROLLED_BENCHMARK
```

Prefer real-user/representative evidence for production prioritization.

# Lab vs Field

Lab data is useful for reproducibility.

Field/RUM data is useful for:

- real devices;
- real networks;
- p75 distribution;
- production prioritization.

Do not assume a fast developer laptop represents users.

# Core Web Vitals

Review when route/page experience is relevant:

```text
LCP
INP
CLS
```

Use accepted project thresholds/budgets.

Do not optimize one metric blindly if the actual user problem is elsewhere.

# LCP

Investigate:

- server response;
- render-blocking resources;
- route bundle;
- hero/image loading;
- font loading;
- client-side data dependency;
- hydration;
- waterfall.

Do not conclude “image optimization” before identifying the actual LCP element and phase.

# INP / Interaction Latency

Investigate:

```text
input delay
processing duration
presentation delay
long tasks
render work
synchronous JS
expensive data transformation
layout/paint
```

A slow click may have multiple phases.

# CLS

Investigate:

- missing size reservation;
- fonts;
- injected banners;
- lazy-loaded content;
- route transitions;
- image dimensions;
- dynamic UI.

Do not fix layout shifts with arbitrary fixed heights that break responsive behavior.

# Long Tasks

Identify tasks that block the main thread.

Possible causes:

- huge JS initialization;
- expensive transform;
- large render;
- third-party script;
- synchronous parser;
- chart computation;
- JSON processing.

Break work only when it preserves UX and adds value.

# Route Loading

Measure:

```text
navigation start
bundle fetch
module evaluation
data fetch
render/hydration
```

Do not treat route loading as bundle size alone.

# Performance Bottleneck Classification

Use one or more:

```text
RENDERING
BUNDLE
NETWORK
DATA_FETCHING
MAIN_THREAD_CPU
ALGORITHMIC
MEMORY
LAYOUT_PAINT
IMAGE_FONT_ASSET
THIRD_PARTY
HYDRATION
SERVER_DEPENDENCY
UNKNOWN
```

# Root-Cause Principle

A symptom may be caused by several layers.

Example:

```text
slow dashboard
→ route bundle 1.8 MB
→ chart library 700 KB
→ duplicate API calls
→ 50k rows rendered
```

Prioritize by measured contribution.

# Finding Structure

Each finding should contain:

```text
ID
symptom
evidence
affected users
root cause
category
severity
recommended fix
expected impact
verification
```

# Severity

Use:

```text
CRITICAL
HIGH
MEDIUM
LOW
ADVISORY
```

based on:

```text
user impact
frequency
critical journey
affected population
measured latency/budget regression
resource cost
workaround
```

Do not rank based on code style.

# Unnecessary Rerenders

Roadmap case:

```text
unnecessary rerenders
```

Use React Profiler or equivalent evidence.

Inspect:

- render count;
- render duration;
- commit duration;
- parent propagation;
- context updates;
- unstable props where semantically relevant;
- expensive child work;
- large tree blast radius.

Do not label every rerender unnecessary.

# Rerender Is Not Automatically Bad

Rendering can be cheap.

Ask:

```text
Did rerender cause measurable interaction/render cost?
```

If no, do not optimize mechanically.

# React Compiler

If React Compiler or equivalent optimization is enabled:

```text
trust compiler-generated memoization first
```

unless:

- semantic identity is required;
- integration requires stable reference;
- profiler shows remaining issue;
- code is outside compiler optimization;
- compiler cannot safely optimize the path.

Do not add redundant `useMemo`, `useCallback`, or `React.memo` everywhere.

# Compiler Status

Record:

```text
REACT_COMPILER_ENABLED
REACT_COMPILER_PARTIAL
REACT_COMPILER_DISABLED
REACT_COMPILER_STATUS_UNKNOWN
```

Performance recommendations should respect this.

# Manual Memoization

Use only for:

```text
semantic identity
measured performance
integration requirement
```

Validate before/after.

Memoization has cost:

- dependency management;
- memory;
- cache invalidation;
- readability;
- stale-value risk.

# Context Rerenders

Broad Context can cause unrelated rerenders.

Investigate with profiler.

Potential fixes:

- split context by ownership;
- move volatile state down;
- external store/selectors if already selected;
- stable provider values when semantically required.

Do not ban Context globally.

# State Ownership

Performance often improves when state is owned near the consumers that need it.

Do not move local state globally merely for reuse.

# Derived State

Avoid storing duplicated derived state that triggers synchronization/render work.

Compute when cheap; memoize only when measured.

# Expensive Render Calculation

If render performs:

```text
large filter
sort
group
graph traversal
heavy formatting
```

measure the cost.

If the transformation scales materially, invoke:

```text
analyzing-algorithmic-complexity
```

Do not assume `useMemo` is the correct first fix.

# Component Splitting

Split only when it:

- reduces render blast radius;
- enables route/lazy boundaries;
- isolates expensive subscriptions;
- improves ownership.

Do not split into tiny components solely to “make React faster.”

# Server Components / SSR

If framework uses server components/SSR:

inspect:

- server/client boundary;
- hydration cost;
- duplicate fetching;
- unnecessary client components;
- serialized payload;
- route streaming.

Do not prescribe one rendering mode universally.

# Hydration

Symptoms:

- long hydration task;
- delayed interactivity;
- mismatch/re-render;
- too much client JS.

Potential fixes:

- reduce client boundary;
- defer non-critical hydration;
- route/component splitting;
- remove unnecessary client dependency.

Follow selected framework capabilities.

# Large Dependency

Roadmap case:

```text
large dependency
```

Measure:

- parsed/minified/gzip/brotli size;
- route contribution;
- tree-shaking;
- transitive dependencies;
- evaluation cost;
- duplicate versions.

Do not reject a library only because package install size is large.

# Dependency Value

Compare:

```text
bundle/runtime cost
vs
capability value
maintainability
correctness
accessibility
security
```

A larger proven library may be preferable to unsafe custom code.

# Large Dependency Findings

Possible:

```text
ROUTE_CRITICAL_DEPENDENCY
LAZY_LOAD_CANDIDATE
TREE_SHAKING_FAILURE
DUPLICATE_PACKAGE_VERSION
HEAVY_TRANSITIVE_DEPENDENCY
ALTERNATIVE_REQUIRED
ACCEPTABLE_COST
```

# Dynamic Import

Use when:

- capability is not needed at initial route;
- code-splitting boundary is stable;
- loading state is acceptable.

Do not dynamically import tiny code everywhere.

# Route Bundle

Roadmap case:

```text
route bundle
```

Measure route-specific:

- entry chunk;
- shared chunks;
- lazy chunks;
- CSS;
- third-party modules;
- module evaluation cost.

Do not evaluate only total app bundle.

# Bundle Budget

Use project-defined budgets where available.

If absent, establish comparison against:

- previous baseline;
- neighboring routes;
- user/device constraints.

Do not invent arbitrary universal KB limits.

# Bundle Regression

Record:

```text
before
after
delta
largest contributors
route impact
```

# Tree Shaking

Check:

- ESM import style;
- barrel side effects;
- package sideEffects metadata;
- namespace imports;
- dual-package issues.

Do not rewrite imports without bundle evidence.

# Duplicate Dependency Version

Bundle analyzers may reveal multiple versions.

Fix only when dedupe is safe.

Do not force dependency resolution that violates package compatibility.

# Polyfills

Large polyfills may affect legacy browser support.

Do not remove them without checking supported browser policy.

# Third-Party Scripts

Measure:

- transfer;
- parse/evaluation;
- long tasks;
- network contention;
- privacy/security implications.

Potential:

```text
defer
lazy load
consent-gate
server-side proxy/alternative
remove
```

Coordinate with privacy/security review where appropriate.

# Duplicated Request

Roadmap case:

```text
duplicated request
```

Use network trace/server-state tooling.

Identify why:

- same resource requested by multiple components;
- key mismatch;
- hook-local fetching duplication;
- remount;
- Strict Mode dev-only behavior;
- SSR + client refetch;
- prefetch + fetch mismatch;
- cache disabled/incorrect;
- retry mistaken for duplication.

# Dev vs Production

React Strict Mode can expose duplicate development effects.

Do not report production duplicate request based only on dev behavior without confirming production semantics.

# Server-State Strategy

If project uses:

```text
SWR
React Query
Apollo
Relay
RTK Query
framework loaders
```

use its deduplication/cache model.

Do not add a second ad hoc request cache.

# Request Key

Duplicated request may come from semantically different cache keys.

Normalize:

```text
resource identity
params
tenant
locale
permissions
```

only when requests truly represent the same server state.

# Cache Correct Layer

Cache at the owner:

```text
HTTP cache
server-state library
Application repository
browser/storage
server
CDN
```

Do not cache everywhere.

# Waterfall

Inspect sequential requests that could overlap.

Example:

```text
request A
→ await
→ request B
```

when B does not depend on A.

Potential:

```text
parallelize
prefetch
server aggregate
route loader
```

Do not parallelize when dependency ordering is real.

# Waterfall vs Dependency

Document whether request B requires result A.

Do not “optimize” a valid sequential dependency into incorrect concurrency.

# Overfetching

Large payloads can cause:

- network delay;
- parse cost;
- memory;
- rendering work.

Prefer narrower contracts when ownership permits.

Do not move backend projection logic into UI if API contract can improve.

# Request Cancellation

Stale requests can consume bandwidth/CPU and cause UI race.

Review if high-frequency interactions trigger them.

Coordinate with server-state/hook behavior.

# Prefetch

Use for high-probability next navigation when it improves UX.

Do not prefetch large routes/data indiscriminately on slow networks.

# Unvirtualized List

Roadmap case:

```text
unvirtualized list
```

Measure:

```text
item count
DOM node count
render/commit duration
scroll FPS
memory
interaction latency
```

Do not virtualize a list of 20 items.

# Virtualization Decision

Good candidate:

```text
hundreds/thousands of expensive rows
```

with measured render/scroll cost.

Possible solutions:

```text
virtualization/windowing
pagination
incremental rendering
server pagination
grouping/collapse
```

Choose based on product behavior.

# Virtualization Trade-Offs

Review:

- accessibility;
- keyboard navigation;
- browser find;
- scroll restoration;
- variable row height;
- sticky headers;
- print/export;
- testing.

Do not introduce virtualization without considering these.

# Large Collections + Algorithmic Handoff

If list preparation itself is expensive:

```text
filter/sort/group/match 100k items
```

invoke:

```text
analyzing-algorithmic-complexity
```

Then combine:

```text
data algorithm cost
+
React render cost
+
DOM/layout cost
```

# Pagination

Pagination can reduce both network and DOM cost.

But it changes UX.

Do not use as a performance fix without product acceptance.

# Infinite Scroll

Review:

- retained DOM;
- retained data;
- memory growth;
- navigation restore;
- accessibility.

Infinite scroll without windowing can still grow unbounded.

# Memory

Measure when:

- long-lived page slows over time;
- navigation retains objects;
- large charts/lists;
- subscriptions/listeners remain;
- caches grow.

Use heap snapshots/profiling where possible.

# Memory Leak Signals

Potential:

- detached DOM;
- retained event listeners;
- timers;
- observers;
- WebSocket subscriptions;
- unbounded caches;
- Blob/Object URLs;
- chart instances;
- workers.

Do not call normal cache retention a leak without evidence.

# Cache Size

Caching improves latency but consumes memory.

Review:

```text
lifetime
eviction
key cardinality
max size
```

# Expensive Chart

Roadmap case:

```text
expensive chart
```

Separate phases:

```text
data fetch
data transform
chart library load
chart initialization
layout/measure
draw/render
interaction
resize
```

Do not blame chart library before tracing phases.

# Chart Data Transform

For:

```text
sort
group
bucket
aggregate
join
downsample
```

use `analyzing-algorithmic-complexity` when scale matters.

# Chart Rendering

Potential fixes:

- reduce visible points;
- downsample;
- canvas/WebGL for appropriate scale;
- defer offscreen chart;
- lazy-load chart library;
- avoid full redraw;
- reduce animation;
- virtualize dashboard panels;
- split work.

Follow library capabilities.

# Chart Library Cost

Large chart libraries may create both:

```text
bundle cost
runtime render cost
```

Evaluate separately.

# Chart Resize

Repeated resize/layout observers can cause expensive redraw.

Throttle/debounce only when measured and UX-safe.

# Offscreen Content

Do not render expensive offscreen tabs/panels unnecessarily if product permits lazy mounting.

But preserve state/semantics when unmounting would harm UX.

# CSS / Layout Performance

Inspect when trace shows:

```text
style recalculation
layout
paint
composite
```

Potential causes:

- layout thrashing;
- read/write interleaving;
- huge DOM;
- expensive selectors rarely;
- large paint areas;
- shadows/filters;
- sticky complexity.

Do not micro-optimize CSS without trace evidence.

# Layout Thrashing

Pattern:

```text
read layout
→ write DOM/style
→ read
→ write
```

in a loop.

Batch reads/writes where necessary.

# Animation

Prefer compositor-friendly transforms/opacity when appropriate.

Do not change animation semantics solely for performance if accessibility/design constraints differ.

Respect reduced motion.

# Images

Review:

- dimensions;
- format;
- responsive sizes;
- lazy loading;
- priority;
- decode;
- CDN.

Only if images are a measured bottleneck.

# Fonts

Review:

- font files/weights;
- preload;
- fallback;
- render blocking;
- layout shift.

Do not remove typography requirements without product/design decision.

# Web Workers

Useful for CPU-heavy independent work that blocks main thread.

Use when:

- workload is substantial;
- serialization cost acceptable;
- code can run off-main-thread;
- architecture supports worker lifecycle.

Do not use worker for tiny computation.

# Chunking Work

Breaking a long task across frames can improve responsiveness.

But total work remains.

Reduce unnecessary work first.

# Idle Work

Non-critical precomputation may use idle scheduling where supported.

Do not schedule essential action response as idle.

# Algorithmic Complexity Handoff

Invoke when the issue involves:

```text
large input growth
repeated scans
nested transformations
sorting/searching
grouping
graph/tree processing
memory growth
repeated copying
```

Expected return:

```text
current time/space complexity
real input bounds
candidate algorithm/data structure
new time/space complexity
trade-offs
benchmark/profile recommendation
```

Then decide frontend-specific fix.

# Example Handoff — List

```text
50k rows
→ React render slow
→ data transform also O(n×m)
```

Need both:

```text
analyzing-algorithmic-complexity
→ reduce O(n×m) matching

reviewing-frontend-performance
→ virtualize DOM/render
```

Neither alone solves the full problem.

# Example Handoff — Chart

```text
100k points
→ O(n log n) sort
→ chart renders all 100k SVG nodes
```

Possible:

- avoid repeated sort/index;
- downsample;
- canvas;
- defer;
- reduce visible series.

Analyze algorithm + rendering separately.

# Core Web Vitals and Algorithms

An expensive algorithm can cause INP/long tasks.

Do not translate Big O directly into CWV impact.

Verify with performance trace.

# Performance Budgets

Use existing budgets:

```text
LCP/INP/CLS
route bundle
JS execution
interaction
memory
```

If none exist, report baseline/regression evidence instead of inventing arbitrary hard gates.

# Before / After

Every material fix should record:

```text
metric
before
after
environment
dataset
device/network
```

# Verification Environment

Use representative:

```text
production build
supported browser
mid/low-tier device or throttling where policy uses it
representative network
representative dataset
```

Do not verify only in development mode.

# Production Build

React/framework dev mode can distort:

- Strict Mode;
- warnings;
- source maps;
- non-minified code;
- extra checks.

Use production build for final performance conclusions.

# Statistical Noise

For lab measurements, run multiple times where variance is material.

Use median/p75-like summary according to tooling.

Do not celebrate a one-run 5 ms improvement.

# Regression Attribution

Compare same:

- build mode;
- browser;
- hardware/throttling;
- data;
- network;
- route state.

Otherwise attribution is weak.

# RUM Verification

For significant production fixes, monitor after release if RUM exists.

Do not claim field improvement only from local lab evidence.

# Finding Confidence

Use:

```text
CONFIRMED
LIKELY
NEEDS_MEASUREMENT
NOT_REPRODUCED
DEV_ONLY
```

# Architectural Fix Priority

Prefer:

1. remove unnecessary work;
2. move work to correct layer;
3. reduce data transferred/processed;
4. deduplicate/cancel/cache correctly;
5. split/lazy-load;
6. virtualize/page;
7. improve algorithm/data structure;
8. only then targeted memoization/micro-optimization.

This ordering is guidance, not an absolute rule.

# Micro-Optimization

Examples:

- memoizing tiny function;
- replacing one loop form;
- manual inline caching;
- shaving a trivial allocation.

Do not prioritize while a 700 KB unused dependency or 50 duplicate requests remain.

# Dependency vs Custom Implementation

Do not remove a proven accessible/design-system dependency merely for bytes without evaluating replacement risk.

Performance is one quality dimension.

# Performance vs Accessibility

A performance fix must preserve:

- keyboard behavior;
- focus;
- semantic DOM;
- screen-reader status;
- zoom/reflow.

Virtualization/lazy mounting require accessibility consideration.

# Performance vs Correctness

Do not introduce stale data, wrong ordering, race conditions, or missing updates to improve speed.

# Performance vs Maintainability

A highly complex optimization requires measured value.

Prefer simpler solution if within budget.

# React DevTools Profiler

Use to inspect:

- component render duration;
- commit;
- why rendered where tooling supports;
- interaction.

Do not infer root cause solely from component count.

# Browser Performance Panel

Useful for:

- long tasks;
- scripting;
- rendering;
- layout;
- paint;
- network;
- screenshots;
- main-thread flame chart.

# Bundle Analyzer

Use framework/build-approved tooling.

Do not add a permanent analyzer dependency if one-off build stats already exist and policy discourages it.

# Network Waterfall

Inspect:

- request start;
- dependency;
- DNS/TLS only when relevant;
- blocking;
- response time;
- transfer;
- duplicated resource;
- priority.

# Memory Tools

Use:

- heap snapshots;
- allocation timeline;
- performance.measureUserAgentSpecificMemory where supported/policy permits;
- framework/library diagnostics.

# Custom Instrumentation

Use User Timing:

```text
performance.mark
performance.measure
```

only when existing profiler cannot isolate an important app phase.

Remove debug-only marks if repository policy requires.

# Review Report

Summarize:

```text
symptom
primary bottleneck
secondary bottlenecks
evidence
highest-leverage fix
expected impact
verification
remaining risks
```

# Roadmap Evaluation — Unnecessary Rerenders

Passing review:

- profiler evidence exists;
- rerender is proven expensive/unnecessary;
- React Compiler status considered;
- fix targets state/context/data boundary before blanket memoization.

# Roadmap Evaluation — Large Dependency

Passing review:

- route contribution measured;
- tree-shaking/transitive/duplication inspected;
- lazy-load/remove/alternative recommendation is proportional.

# Roadmap Evaluation — Duplicated Request

Passing review:

- production/representative duplication confirmed;
- source identified;
- server-state/key/cache/SSR ownership corrected;
- dev Strict Mode false positive excluded.

# Roadmap Evaluation — Unvirtualized List

Passing review:

- dataset and DOM/render cost measured;
- virtualization/pagination decision considers UX/accessibility;
- algorithmic preprocessing handed off when scale complexity matters.

# Roadmap Evaluation — Route Bundle

Passing review:

- route-specific chunks and contributors measured;
- initial vs lazy cost separated;
- before/after bundle evidence planned.

# Roadmap Evaluation — Expensive Chart

Passing review:

- fetch/transform/library-load/render phases separated;
- algorithmic complexity invoked where data transform scales;
- point count/render technology/lazy loading/downsampling considered from evidence.

# Over-Optimization Audit

Flag:

- blanket `useMemo`/`useCallback`;
- `React.memo` everywhere;
- virtualization for tiny lists;
- dynamic import for tiny modules;
- caching at several layers;
- worker for trivial CPU;
- microbenchmark before user symptom;
- dependency removal without value/risk analysis.

Use:

```text
EVIDENCE_DRIVEN_PERFORMANCE_REVIEW
PREMATURE_OPTIMIZATION
PERFORMANCE_FIX_OVERCOMPLEX
PERFORMANCE_REVIEW_NOT_REQUIRED
```

# Under-Optimization Audit

Flag:

- 50k DOM rows;
- 1 MB+ route regression with no analysis;
- repeated production requests;
- long main-thread tasks;
- expensive chart redraw;
- large transform each render;
- unbounded cache/memory;
- architectural issue “fixed” only with memoization.

# Final Decision

Use:

```text
FRONTEND_PERFORMANCE_ACCEPTABLE
FRONTEND_PERFORMANCE_ACCEPTABLE_WITH_CONDITIONS
FRONTEND_PERFORMANCE_OPTIMIZATION_REQUIRED
ALGORITHMIC_ANALYSIS_REQUIRED
BUNDLE_OPTIMIZATION_REQUIRED
NETWORK_OPTIMIZATION_REQUIRED
RENDERING_OPTIMIZATION_REQUIRED
MEMORY_OPTIMIZATION_REQUIRED
PRODUCTION_MEASUREMENT_REQUIRED
PERFORMANCE_REVIEW_INCOMPLETE
BLOCKED
```

## Output

Use `assets/frontend-performance-review-record.md`.

## Completion Criteria

- [ ] User-visible symptom and scope are explicit.
- [ ] Review is evidence-driven rather than code-smell-driven.
- [ ] Production build/representative environment is used for final conclusions.
- [ ] Relevant Core Web Vitals are measured when page experience is the concern.
- [ ] Rendering frequency/duration is measured when rerenders are suspected.
- [ ] React Compiler/equivalent optimizer status is considered.
- [ ] Manual memoization is not recommended mechanically.
- [ ] Route bundle/chunk contributors are measured when bundle cost is suspected.
- [ ] Large dependency cost is compared against capability value.
- [ ] Network waterfall is inspected when request latency/duplication matters.
- [ ] Dev Strict Mode duplication is distinguished from production duplication.
- [ ] Server-state/cache ownership is respected.
- [ ] Large-list item count, DOM cost, render cost, and accessibility trade-offs are considered.
- [ ] Expensive chart phases are separated into fetch/transform/load/render.
- [ ] Algorithmic complexity is delegated to `analyzing-algorithmic-complexity` when data-scaling questions are material.
- [ ] CPU, rendering, network, bundle, memory, layout, and server dependency costs are distinguished.
- [ ] Long tasks and interaction latency are investigated when relevant.
- [ ] Memory retention/leak claims have evidence.
- [ ] Architectural fixes are prioritized before micro-optimization.
- [ ] Performance changes preserve correctness/accessibility/maintainability.
- [ ] Before/after verification uses comparable conditions.
- [ ] Noise/variance is considered.
- [ ] RUM follow-up is recommended for significant production changes when available.
- [ ] Roadmap evaluations are covered: unnecessary rerenders, large dependency, duplicated request, unvirtualized list, route bundle, expensive chart.
- [ ] Final performance decision is explicit.
