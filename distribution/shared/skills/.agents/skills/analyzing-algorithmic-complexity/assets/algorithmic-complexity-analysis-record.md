# Algorithmic Complexity Analysis Record

## Context

- Path/algorithm:
- Frontend/backend/shared:
- Critical path:
- Execution environment:
- Trigger/frequency:
- Existing performance evidence:
- Latency budget:
- Memory budget:
- Applicable `AGENTS.md`:
- Analyst/date:

## Readiness

- Input variables known:
- Typical bounds known:
- Maximum supported bounds known:
- Frequency known:
- Data distribution known:
- Hot-path evidence:
- Initial status:
- Conditions/blockers:

## Input Variables

| Variable | Meaning | Typical | High | Max supported | User-controlled |
|---|---|---:|---:|---:|---|
| n | | | | | |
| m | | | | | |
| k | | | | | |

## Current Algorithm

```text

```

## Operation Breakdown

| Operation | Complexity | Frequency | Hidden cost |
|---|---|---|---|
| | | | |

## Time Complexity

- Best:
- Average:
- Worst:
- Dominant expression:
- Simplified Big O:
- Multi-variable notation preserved:
- Assumptions:

## Space Complexity

- Additional memory:
- Intermediate collections:
- Recursion stack:
- Cache/index:
- Output memory:
- Peak-risk notes:

## Amortized Behavior

- Applicable:
- Operation:
- Occasional expensive step:
- Amortized result:

## Hidden Multiplicative Work

- loop × scan:
- loop × sort:
- loop × serialization:
- loop × regex:
- loop × render:
- loop × I/O:
- repeated recursive subproblem:
- repeated copying:

## Data Structure Audit

| Current | Operation need | Candidate | Time trade-off | Space trade-off | Semantics risk |
|---|---|---|---|---|---|
| | | | | | |

- Ordering preserved:
- Duplicates preserved:
- Equality semantics preserved:
- Key uniqueness valid:

## Practical Scale Assessment

- Expected operations at typical size:
- Expected operations at max size:
- Execution frequency multiplier:
- Bounded input:
- Adversarial input:
- Classification: NEGLIGIBLE_AT_EXPECTED_SCALE / ACCEPTABLE_WITH_BOUNDED_INPUT / SCALABILITY_RISK / CURRENT_PERFORMANCE_BOTTLENECK / MEMORY_RISK / I/O_DOMINATED / UNKNOWN_REQUIRES_MEASUREMENT

## System Bottleneck Separation

| Cost category | Evidence | Dominant? |
|---|---|---|
| CPU algorithm | | |
| memory/allocation | | |
| database | | |
| network | | |
| provider I/O | | |
| serialization | | |
| rendering/DOM | | |
| bundle/load | | |

- Primary bottleneck:
- Complexity is not primary bottleneck:
- Required handoff:

## I/O Multiplication

- Per-item DB call:
- Per-item HTTP/provider call:
- N+1 pattern:
- Batch available:
- Query/join alternative:
- Round-trip count:

## Candidate Improvements

### Candidate 1

- Change:
- Current time:
- New time:
- Current space:
- New space:
- Expected benefit:
- Readability cost:
- Semantics risk:
- Recommended:

### Candidate 2

- Change:
- Current time:
- New time:
- Current space:
- New space:
- Expected benefit:
- Readability cost:
- Semantics risk:
- Recommended:

## Benchmark / Profile Plan

- Needed:
- Why:
- Tool:
- Dataset sizes:
  - small:
  - typical:
  - high:
  - max:
- Warmup/repetitions:
- CPU profile:
- Memory profile:
- Browser/React profile:
- DB/query plan:
- APM/trace:

## Before / After Evidence

| Metric | Before | After |
|---|---:|---:|
| time complexity | | |
| space complexity | | |
| typical runtime | | |
| high runtime | | |
| max runtime | | |
| peak memory | | |
| I/O count | | |

## Correctness Protection

- Existing tests:
- Regression test:
- Property-based test:
- Ordering:
- Duplicates:
- Boundary inputs:
- Failure semantics:

## Frontend Handoff

- Expensive rerenders:
- Large DOM/list:
- Chart rendering:
- Interaction latency:
- Need `reviewing-frontend-performance`:

## Backend Handoff

- Query/index issue:
- N+1:
- Batch/repository design:
- Worker/job throughput:
- Need backend performance/query review:

## Security Handoff

- Untrusted input:
- ReDoS:
- Unbounded recursion:
- Resource exhaustion:
- Need security review:

## Over/Under-Optimization Audit

- O(n²) but permanently tiny:
- Overcomplicated data structure:
- Cache without invalidation:
- Parallelism before work reduction:
- Quadratic large join:
- Repeated sorting:
- Repeated copying:
- Per-item I/O:
- Unbounded recursion:
- Decision:

## Final Decision

- Decision:
- Complexity risk:
- Primary bottleneck:
- Recommended action:
- Required measurement:
- Required handoff:
