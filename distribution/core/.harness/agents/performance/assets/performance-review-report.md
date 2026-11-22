# Performance Review Report

## Gate Decision

- Decision: PERFORMANCE_APPROVED / PERFORMANCE_APPROVED_WITH_CONDITIONS / PERFORMANCE_CHANGES_REQUIRED / BLOCKED_PENDING_DECISION / BLOCKED_PENDING_EVIDENCE / PERFORMANCE_REVIEW_NOT_REQUIRED
- Review version:
- Reviewer:
- Date:
- Target change / PR:
- Scope: FRONTEND / BACKEND / FULL_STACK / JOB / WORKER / INFRA_DEPENDENT
- Re-review required: yes/no

## Performance Trigger

- Accepted target / SLO / budget:
- Baseline regression guard:
- User/system symptom:
- Preventive scale risk:
- Why review is required:

## Authoritative Basis

- Applicable `AGENTS.md`:
- Requirement / OpenSpec / quality scenario:
- Architecture/deployment constraints:
- Project performance budgets:
- Validator evidence:
- QA evidence:
- Code / Architecture Review findings:

## Workload / Environment

- Scenario:
- Input/data size:
- Distribution:
- Request/concurrency rate:
- Duration:
- Device/browser/runtime:
- Network:
- Database dataset:
- Cache state: COLD / WARM / MIXED / N/A
- Environment representativeness:
- Known limitations:

## Measurements

| Metric | Baseline | Candidate | Target/Budget | Evidence | Status |
|---|---:|---:|---:|---|---|
| | | | | | MEETS_TARGET / REGRESSION_WITHIN_BUDGET / VIOLATES_TARGET / REGRESSION_OUTSIDE_BUDGET / INCONCLUSIVE / NO_TARGET |

## Evidence Inventory

| Evidence | Quality | Source | Notes |
|---|---|---|---|
| Production/RUM/APM | HIGH / MEDIUM / LOW | | |
| Browser trace/profiler | | | |
| Bundle analysis | | | |
| Query plan/timing | | | |
| CPU/heap profile | | | |
| Benchmark | | | |
| Load/stress/soak | | | |
| Queue/pool metrics | | | |

## Bottleneck Classification

- Dominant bottleneck: CLIENT_CPU / CLIENT_RENDER / CLIENT_BUNDLE / CLIENT_NETWORK / SERVER_CPU / SERVER_MEMORY / DATABASE / EXTERNAL_IO / SERIALIZATION / ALGORITHM / LOCK_CONTENTION / CONNECTION_POOL / QUEUE_BACKLOG / COLD_START / UNKNOWN
- Secondary contributors:
- Evidence:
- Root-cause confidence:

## Frontend Performance

### Core Web Vitals
- LCP:
- INP:
- CLS:
- Field vs lab:

### Route / Bundle
- Initial/route JS:
- Large dependency:
- Duplicate dependency:
- Waterfall:

### Rendering / Interaction
- Render frequency:
- Long tasks:
- Interaction phases:
- Large list/chart:
- React Compiler enabled:
- Memoization evidence:

### Network
- Duplicate requests:
- Serial waterfalls:
- Payload size:
- Cache/refetch behavior:

## Backend / Runtime Performance

### Latency Breakdown
| Segment | Time / share | Evidence |
|---|---:|---|
| Auth/parsing | | |
| Application/domain | | |
| Database | | |
| External provider | | |
| Serialization | | |
| Queue/wait | | |

### Database
- Query count:
- Query timing:
- Rows examined/returned:
- Query plan:
- Index behavior:
- Lock wait:
- Connection wait:
- N+1:

### CPU / Algorithm
- Hot frames:
- Input dimensions:
- Frequency:
- Complexity:
- Delegated complexity analysis:

### Memory
- Peak:
- Steady-state:
- Growth:
- Retained objects:
- GC:
- Cache/buffer behavior:

### Concurrency / Capacity
- Concurrency:
- Saturation point:
- Connection pool:
- Queue lag:
- Worker throughput:
- Retry amplification:
- Headroom:

## External Dependencies

| Dependency | Latency/error | Contribution | Limit/rate | Evidence |
|---|---|---|---|---|
| | | | | |

## Findings

### PERF-001 — [Title]

- Severity: CRITICAL / HIGH / MEDIUM / LOW
- Confidence: HIGH / MEDIUM / LOW
- Category: BUDGET_REGRESSION / LATENCY / THROUGHPUT / CORE_WEB_VITALS / INTERACTION / BUNDLE / RENDERING / NETWORK / DATABASE / N_PLUS_ONE / EXTERNAL_IO / SERIALIZATION / CPU / MEMORY / ALGORITHMIC_COMPLEXITY / CONCURRENCY / CONNECTION_POOL / QUEUE_CAPACITY / COLD_START / CACHE / CAPACITY / MEASUREMENT_QUALITY
- Target / symptom:
- Workload/environment:
- Baseline:
- Candidate:
- Evidence:
- Bottleneck/root cause:
- Impact:
- Smallest remediation direction:
- Trade-offs:
- Verification measurement:
- Blocking: yes/no
- Handoff / owner:

## Measurement / Decision Questions

| ID | Missing target/evidence/decision | Why needed | Blocking? | Route |
|---|---|---|---|---|
| | | | | Product / Architecture / Infrastructure / Validator |

## Capacity Assessment

- Capacity target:
- Measured capacity:
- Saturation resource:
- Headroom:
- Scaling assumption:
- Capacity result:

## Before / After Verification Plan

| Finding | Metric | Baseline | Required result | Same workload? | Owner |
|---|---|---:|---:|---|---|
| | | | | | |

## Handoffs

| Finding / need | Recipient | Expected output | Blocking | Re-entry condition |
|---|---|---|---|---|
| | Implementation / Validator / Code Review / Architecture Review / QA / Infrastructure / Security / Detail Analyst / Reviewer | | yes/no | |

## Residual Performance Risk

- Evidence limitations:
- Unmeasured environments:
- Deferred load/capacity risk:
- External dependency risk:
- Accepted budget trade-offs:
- Shifted bottleneck risk:

## Performance Summary

- Critical findings:
- High findings:
- Medium findings:
- Low findings:
- Blocking decisions:
- Blocking evidence:
- Budget/SLO result:
- Why final decision is justified:

## Exact Next Action

-
