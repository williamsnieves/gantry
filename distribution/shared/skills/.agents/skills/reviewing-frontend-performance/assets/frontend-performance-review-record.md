# Frontend Performance Review Record

## Context

- Surface/route:
- User-visible symptom:
- Critical journey:
- Repository/application:
- Framework/version:
- React Compiler/equivalent status:
- Production build:
- Target device/browser:
- Target network:
- Representative data size:
- Existing budgets:
- RUM available:
- Applicable `AGENTS.md`:
- Reviewer/date:

## Readiness

- Reproduction available:
- Representative environment:
- Measurement available:
- Production/field evidence:
- Bundle stats:
- Network trace:
- Profiler trace:
- Memory evidence:
- Initial decision:
- Conditions/blockers:

## Symptom

- User impact:
- Frequency:
- Affected population:
- Trigger:
- Expected:
- Actual:
- Baseline:
- Regression date/change if known:

## Evidence Inventory

| Evidence | Available | Finding |
|---|---|---|
| Core Web Vitals | | |
| React Profiler | | |
| browser Performance trace | | |
| bundle analyzer/stats | | |
| network waterfall | | |
| memory profile | | |
| RUM/APM | | |
| benchmark | | |

## Core Web Vitals

- LCP:
- INP:
- CLS:
- Field/lab:
- p75/summary:
- Main contributor:
- Budget/target:

## Bottleneck Classification

| Category | Evidence | Contribution |
|---|---|---|
| RENDERING | | |
| BUNDLE | | |
| NETWORK | | |
| DATA_FETCHING | | |
| MAIN_THREAD_CPU | | |
| ALGORITHMIC | | |
| MEMORY | | |
| LAYOUT_PAINT | | |
| IMAGE_FONT_ASSET | | |
| THIRD_PARTY | | |
| HYDRATION | | |
| SERVER_DEPENDENCY | | |

- Primary bottleneck:
- Secondary bottleneck:
- Unknowns:

## Finding Template

### PERF-001 — [Title]

- Severity:
- Confidence: CONFIRMED / LIKELY / NEEDS_MEASUREMENT / NOT_REPRODUCED / DEV_ONLY
- Category:
- User impact:
- Evidence:
- Root cause:
- Current behavior:
- Recommended fix:
- Why architectural:
- Expected impact:
- Trade-offs:
- Verification:
- Required handoff:

## Unnecessary Rerenders

- Profiler evidence:
- Render count:
- Render duration:
- Commit duration:
- Parent/context propagation:
- Expensive child:
- Actually harmful:
- React Compiler status:
- Manual memoization justified:
- Architectural fix:

## Large Dependency

- Dependency:
- Route contribution:
- Transfer size:
- Parse/eval:
- Transitive cost:
- Duplicate versions:
- Tree-shaking:
- Initial-route required:
- Lazy-load candidate:
- Remove/alternative:
- Capability/accessibility trade-off:

## Duplicated Request

- Resource:
- Count:
- Production or dev-only:
- Strict Mode false positive:
- Same semantic cache key:
- Trigger:
- SSR/client duplication:
- Retry vs duplicate:
- Server-state owner:
- Correct fix:
- Waterfall effect:

## Unvirtualized List

- Items typical:
- Items max:
- DOM nodes:
- Render/commit:
- Scroll FPS:
- Memory:
- Interaction latency:
- Virtualization justified:
- Pagination alternative:
- Accessibility/keyboard trade-offs:
- Algorithmic preprocessing:
- Need `analyzing-algorithmic-complexity`:

## Route Bundle

- Route:
- Before:
- After:
- Delta:
- Entry chunk:
- Shared chunks:
- Lazy chunks:
- CSS:
- Largest contributors:
- Module evaluation:
- Split boundary:
- Budget/baseline:
- Verification:

## Expensive Chart

- Data points:
- Data fetch:
- Transform:
- Complexity:
- Chart library load:
- Init:
- Layout:
- Render/draw:
- Resize/repaint:
- Animation:
- Main-thread task:
- Lazy-load:
- Downsample:
- Canvas/WebGL/SVG:
- Need `analyzing-algorithmic-complexity`:

## Network Waterfall

| Request | Start dependency | Duplicate | Duration | Payload | Action |
|---|---|---|---:|---:|---|
| | | | | | |

- Parallelizable:
- True dependency:
- Prefetch opportunity:
- Overfetching:
- Cancellation:
- Cache owner:

## Long Tasks / Interaction

| Task | Duration | Trigger | Main work |
|---|---:|---|---|
| | | | |

- Input delay:
- Processing:
- Presentation delay:
- Worker/chunking candidate:
- Unnecessary work first removed:

## Memory

- Initial:
- After interaction:
- After navigation:
- Retained:
- Detached DOM:
- listeners/timers/observers:
- cache growth:
- chart instances:
- Blob/Object URL:
- Leak confirmed:
- Eviction/cleanup:

## Layout / Paint

- Recalculate style:
- Layout:
- Paint:
- Composite:
- DOM size:
- Layout thrashing:
- Large paint area:
- Animation issue:

## Algorithmic Complexity Handoff

- Relevant:
- Path:
- Input sizes:
- Why scaling matters:
- Analysis skill invoked/required:
- Current complexity:
- Proposed complexity:
- Memory trade-off:
- Frontend-specific consequence:

## Prioritization

| Priority | Fix | Category | Expected impact | Cost/risk |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

- Architectural fixes before micro-optimization:
- Premature optimization avoided:

## Before / After Verification

| Metric | Before | After | Environment |
|---|---:|---:|---|
| LCP | | | |
| INP | | | |
| route JS | | | |
| render/commit | | | |
| requests | | | |
| long task | | | |
| memory | | | |
| chart/list interaction | | | |

- Runs/sample count:
- Variance:
- Same conditions:
- Production build:
- RUM follow-up:

## Correctness / Accessibility / Maintainability

- Behavior preserved:
- Keyboard/focus:
- Virtualization accessibility:
- Data correctness:
- Race/cache semantics:
- Maintainability cost:
- Complexity increase justified:

## Roadmap Evaluations

| Case | Status | Evidence |
|---|---|---|
| unnecessary rerenders | | |
| large dependency | | |
| duplicated request | | |
| unvirtualized list | | |
| route bundle | | |
| expensive chart | | |

## Over/Under-Optimization Audit

- blanket memoization:
- virtualization tiny list:
- tiny dynamic imports:
- multilayer caching:
- worker for trivial work:
- large unresolved dependency:
- production duplicate requests:
- long tasks ignored:
- algorithm issue hidden by memoization:
- Decision: EVIDENCE_DRIVEN_PERFORMANCE_REVIEW / PREMATURE_OPTIMIZATION / PERFORMANCE_FIX_OVERCOMPLEX / PERFORMANCE_REVIEW_NOT_REQUIRED

## Final Decision

- Decision:
- Primary bottleneck:
- Required fix:
- Required measurement:
- Required handoff:
- Residual risk:
