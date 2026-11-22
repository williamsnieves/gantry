---
name: analyzing-algorithmic-complexity
description: Analyzes algorithmic and data-structure complexity across frontend and backend code. Use when input size can grow, nested/repeated scans, sorting, searching, grouping, graph/tree traversal, large collections, transformations, matching, ranking, scheduling, or memory growth may affect scalability. Evaluate time complexity, space complexity, best/average/worst-case behavior, amortized cost, actual expected input sizes, hidden multiplicative work, and data-structure trade-offs. Distinguish algorithmic CPU/memory bottlenecks from I/O, database, network, rendering, and serialization bottlenecks; recommend proportional changes only when evidence and scale justify them. Do not optimize solely because a path is O(n²), ignore constants/input bounds, or use Big O as a substitute for profiling and system-level performance evidence.
---

# Analyzing Algorithmic Complexity

## Purpose

Analyze whether an implementation scales acceptably as input grows.

The core workflow is:

```text
identify hot path / growth dimension
→ determine input variables and realistic bounds
→ derive time + space complexity
→ inspect hidden multiplicative work
→ inspect data-structure choices
→ separate CPU/memory from I/O/system bottlenecks
→ estimate practical impact
→ recommend proportional change
→ verify with benchmark/profile where useful
```

Big O is a reasoning tool.

It is not the final performance verdict.

## Core Principle

```text
asymptotic complexity
+
realistic input size
+
constants
+
memory cost
+
I/O cost
+
profiling evidence
=
optimization priority
```

Never conclude:

```text
O(n²) → must rewrite
```

without understanding `n`.

Likewise, never assume:

```text
O(n) → fast enough
```

if each step performs expensive I/O, parsing, rendering, allocation, or network work.

## Use When

- Nested loops/processes grow with input.
- `map` + `find`, `filter` + `includes`, or repeated scans appear in hot paths.
- Large lists/tables/charts process client-side data.
- Backend jobs aggregate/match/deduplicate/rank large collections.
- Tree or graph traversal is performance-sensitive.
- Sorting/searching/grouping dominates CPU time.
- A repeated membership lookup may benefit from `Set`/`Map`.
- Data structures may be causing avoidable lookup cost.
- A recursive algorithm may grow time/stack/memory excessively.
- Expensive transformations run on every request/render.
- A performance review identifies an expensive list/chart/transform.
- A code review suspects scaling risk.
- A Performance Agent needs computational-complexity evidence.

## Do Not Use When

- The dominant bottleneck is clearly network/database/provider latency and algorithmic work is negligible.
- The input size is permanently tiny and the simpler algorithm is clearer.
- The behavior is not performance-sensitive.
- The question is primarily bundle size, rerenders, Core Web Vitals, caching, query design, or DB indexing.
- The task is to benchmark without understanding the algorithm.
- The request is just to explain Big O academically without reviewing an implementation.
- A change would reduce asymptotic cost while making code much more complex for no practical benefit.

## Inputs

- Code path / algorithm.
- Expected input sizes.
- Maximum supported input size.
- Frequency of execution.
- Data distribution.
- Hot-path evidence.
- Profiling/benchmark data if available.
- Memory constraints.
- Latency budget.
- Frontend/backend execution environment.
- I/O/database/network interactions.
- Existing data structures.
- Accepted readability/maintenance constraints.
- Applicable `AGENTS.md`.

## Outputs

- Input-variable model.
- Time-complexity analysis.
- Space-complexity analysis.
- Best/average/worst-case notes where relevant.
- Amortized-complexity notes where relevant.
- Hidden-work inventory.
- Data-structure assessment.
- Practical scale assessment.
- Bottleneck classification.
- Candidate improvements.
- Trade-off analysis.
- Benchmark/profile recommendation.
- Algorithmic-complexity analysis record.

# Readiness Gate

Use:

```text
READY_TO_ANALYZE_ALGORITHMIC_COMPLEXITY
READY_WITH_CONDITIONS
ALGORITHMIC_COMPLEXITY_NOT_RELEVANT
INPUT_BOUNDS_REQUIRED
HOT_PATH_EVIDENCE_REQUIRED
DATA_DISTRIBUTION_REQUIRED
SYSTEM_BOTTLENECK_ANALYSIS_REQUIRED
BLOCKED
```

# Step 1 — Identify Input Variables

Do not collapse every size into `n`.

Use distinct variables where appropriate:

```text
n = users
m = permissions
v = graph vertices
e = graph edges
k = requested top results
p = pages
c = chart points
```

Example:

```ts
users.map(user =>
  permissions.find(permission => permission.userId === user.id)
)
```

Complexity is:

```text
O(n × m)
```

not automatically `O(n²)` unless `n` and `m` grow together.

# Realistic Bounds

Record:

```text
typical
p95 / high
maximum supported
adversarial / untrusted
```

Example:

```text
n typical = 8
n max = 20
```

An `O(n²)` path may be perfectly acceptable.

But:

```text
n typical = 20,000
n max = 100,000
```

changes the decision.

# Frequency

Complexity impact also depends on how often work runs:

```text
once at startup
once per request
on every keystroke
on every render
per animation frame
per batch item
per cron cycle
```

A moderate algorithm can become expensive if executed at high frequency.

# Time Complexity

Derive the dominant growth term.

Common classes:

```text
O(1)
O(log n)
O(n)
O(n log n)
O(n²)
O(n³)
O(2^n)
O(n!)
```

Use more precise multi-variable notation when useful:

```text
O(n + m)
O(n × m)
O(v + e)
O(n log k)
```

# Sequential Work

Sequential independent passes add:

```text
O(n) + O(n)
→ O(n)
```

Do not incorrectly multiply sequential passes.

Example:

```ts
const active = users.filter(isActive)  // O(n)
const names = active.map(toName)       // O(n)
```

Overall remains:

```text
O(n)
```

ignoring different intermediate sizes.

# Nested Work

Nested work multiplies when the inner work scales with another input.

```ts
for user in users:
  for permission in permissions:
```

→

```text
O(n × m)
```

# Hidden Nested Work

High-level methods can hide multiplication.

Examples:

```text
map + find
filter + includes
sort inside loop
JSON.stringify inside loop
regex over growing strings
deep clone inside traversal
```

Inspect library operations rather than assuming one line means O(1).

# `find`

Array `find`:

```text
O(n)
```

worst-case.

Inside another loop:

```text
O(n × m)
```

A `Map.get` is typically expected average:

```text
O(1)
```

with memory trade-off.

# `includes`

Array membership:

```text
O(n)
```

Repeated membership:

```text
candidate for Set
```

when scale/frequency justifies.

# Sorting

Comparison sort:

```text
O(n log n)
```

typically.

Flag repeated sorting:

```ts
for (...) {
  rows.sort(...)
}
```

if the same or growing collection is sorted repeatedly.

Sort once where semantics permit.

# Searching

Sorted collection + binary search:

```text
O(log n)
```

but sorting cost may be:

```text
O(n log n)
```

If one search only, pre-sorting may not be beneficial.

Consider total lifecycle cost.

# Map / Set

Typical expected operations:

```text
Map.get/set → O(1) average
Set.has/add → O(1) average
```

but space becomes:

```text
O(n)
```

and constants may be larger.

Use when repeated lookup/membership justifies it.

# Objects / Dictionaries

Plain object lookup may also approximate O(1) average for suitable keys.

Choose based on semantics, safety, iteration/order requirements, and codebase conventions.

Do not replace every array with a Map.

# Indexing Pattern

Example:

```ts
const permissionsByUser = new Map(
  permissions.map(p => [p.userId, p])
)

const result = users.map(user => ({
  ...user,
  permission: permissionsByUser.get(user.id),
}))
```

Time:

```text
build Map → O(m)
users pass → O(n)
total → O(n + m)
```

Space:

```text
O(m)
```

Trade-off:

```text
faster repeated lookup
↔ additional memory/index construction
```

# Grouping

Repeated filtering by key:

```ts
parents.map(parent =>
  items.filter(item => item.parentId === parent.id)
)
```

often:

```text
O(n × m)
```

Group once:

```text
O(m)
```

then retrieve groups:

```text
O(n)
```

for total expected:

```text
O(n + m)
```

plus memory.

# Deduplication

Naive:

```ts
result = []
for item:
  if (!result.includes(item)):
```

may be:

```text
O(n²)
```

A `Set` can often reduce expected time to:

```text
O(n)
```

with:

```text
O(n)
```

extra space.

Only use if equality semantics fit.

# Top-K

Sorting all elements:

```text
O(n log n)
```

for top `k`.

A heap/select approach may be:

```text
O(n log k)
```

or better depending on algorithm.

Do not introduce a heap for small `n` and maintainability cost without need.

# Graph Traversal

Typical:

```text
BFS / DFS → O(v + e)
```

if visited nodes are tracked.

Without visited tracking, cycles can cause:

- repeated work;
- infinite traversal;
- explosive complexity.

# Trees

Balanced search tree:

```text
O(log n)
```

lookup/update.

Unbalanced tree worst case:

```text
O(n)
```

Recursive traversal:

```text
O(n)
```

time and up to:

```text
O(h)
```

stack space.

# Recursion

Review:

```text
recursion depth
duplicate subproblems
stack growth
memoization opportunity
```

Naive Fibonacci-like recursion:

```text
O(2^n)
```

can often become:

```text
O(n)
```

with memoization/iteration.

Do not apply memoization blindly when state space/memory is huge.

# Dynamic Programming

Consider when:

```text
overlapping subproblems
optimal substructure
```

exist.

Record:

```text
time saved
space cost
cache key/state size
```

# Memoization

Memoization trades:

```text
extra memory
+
cache invalidation/identity complexity
```

for reduced recomputation.

Use only when repeated subproblem evaluation is substantial.

# Amortized Complexity

Some operations have expensive occasional steps but low average cost.

Examples:

```text
dynamic array append
hash table resize
```

Record amortized cost when relevant.

Do not mislabel occasional O(n) resize as every append O(n).

# Best / Average / Worst Case

Use when distribution matters.

Example quicksort:

```text
average O(n log n)
worst O(n²)
```

But implementation/runtime may use hybrid algorithms.

Do not claim textbook behavior without checking actual library/runtime when it matters.

# Data Distribution

Complexity can depend on:

- duplicates;
- skew;
- sparsity;
- graph density;
- key distribution;
- sortedness;
- adversarial input.

Record assumptions.

# Space Complexity

Analyze additional memory.

Common:

```text
O(1)
O(log n)
O(n)
O(n + m)
O(n²)
```

Include:

- maps/sets;
- intermediate arrays;
- recursion stack;
- memoization caches;
- copied objects;
- serialization buffers;
- DOM/render structures where relevant.

# Intermediate Collections

Pipelines may allocate multiple arrays:

```ts
items
  .filter(...)
  .map(...)
  .sort(...)
```

Asymptotic space may remain:

```text
O(n)
```

but allocation/constants can still matter.

Do not overstate as O(3n); Big O simplifies to O(n), but practical memory should note three large intermediates.

# Streaming / Iterators

Streaming can reduce memory from:

```text
O(n)
```

to:

```text
O(1) / O(k)
```

when full materialization is unnecessary.

But streaming may complicate code and prevent multiple passes.

Use proportionally.

# Copying

Repeated spread/object/array copies inside loops can create hidden cost.

Example:

```ts
acc = [...acc, item]
```

inside `n` iterations may copy growing arrays repeatedly:

```text
O(n²)
```

time.

Prefer mutation in a local builder or push when semantics permit.

# Immutable Data Trade-Off

Immutability remains valuable.

Avoid pathological repeated full copies.

Use structural sharing or local mutation inside encapsulated construction where project conventions permit.

# String Concatenation

Repeated concatenation may be implementation-dependent.

For large text generation, consider:

```text
array + join
builder
stream
```

if profiling shows cost.

Do not optimize small strings speculatively.

# Serialization

`JSON.stringify`/`parse` are roughly proportional to serialized payload size.

Repeated serialization of the same growing object can dominate CPU/memory.

Avoid inside nested loops where unnecessary.

# Regular Expressions

Regex complexity can be non-linear or catastrophic depending on pattern/input.

Flag:

```text
nested quantifiers
ambiguous backtracking
untrusted long strings
```

when relevant.

Potential:

```text
ReDoS risk
```

requires security review too.

# Hashing / Cryptography

Treat cryptographic cost according to algorithm/input and security parameters.

Do not “optimize” security primitives by weakening them.

# Database Distinction

Big O of application code does not describe database execution sufficiently.

Possible dominant bottlenecks:

```text
full table scan
missing index
N+1 queries
poor join plan
large sort
network round trips
lock contention
```

Use:

```text
ALGORITHMIC_COMPLEXITY_NOT_PRIMARY_BOTTLENECK
```

when DB/query behavior dominates.

# N+1

Application loop:

```ts
for user:
  await repository.loadPermissions(user.id)
```

may look:

```text
O(n)
```

in application steps, but actual cost is:

```text
n network/DB round trips
```

This is often more important than asymptotic CPU.

Classify:

```text
I/O_MULTIPLICATION
```

not just O(n).

# Batching

Potential improvement:

```text
n remote calls
→ one batch call
```

may dominate any algorithmic optimization.

# Network

Repeated requests, waterfalls, retries, payload size, latency, and serialization can dominate.

Do not recommend `Map` micro-optimization while 100 network requests remain.

# Frontend Rendering Distinction

A frontend path may have:

```text
O(n)
```

data processing but render 50,000 DOM nodes.

The primary problem may be:

```text
rendering/DOM work
```

requiring:

```text
virtualization
pagination
windowing
```

rather than only a faster data transform.

# Frontend Rerenders

Repeated `O(n)` transform across many rerenders may become:

```text
render frequency × n
```

Practical cost can be large even if each call is linear.

Analyze:

```text
algorithm cost
× execution frequency
```

Do not classify rerender architecture purely with Big O; delegate to frontend performance review.

# Charts

Chart preprocessing may contain:

```text
sorting
grouping
aggregation
pairwise comparison
geometry calculation
```

Separate:

```text
data algorithm cost
rendering cost
library cost
```

An expensive chart may need both this skill and frontend performance review.

# Backend Jobs

Batch/ETL/job processing should consider:

```text
items
dependencies
database access
concurrency
memory retention
```

An O(n) loop with one remote call per item can still be unacceptable.

# Concurrency

Parallelism changes wall-clock behavior but not necessarily total work.

Example:

```text
100 O(1) I/O requests in parallel
```

still means 100 requests.

Analyze:

```text
work
latency
concurrency limit
resource pressure
```

separately.

# Parallel CPU

Parallelization can reduce latency but add coordination/memory overhead.

Do not parallelize an inefficient algorithm before addressing unnecessary work.

# Complexity Composition

For pipeline:

```text
load
→ transform
→ sort
→ match
```

separate:

```text
I/O
CPU
memory
```

Then identify dominant term/cost.

# Multiplicative Work Inventory

Look for:

```text
loop × scan
loop × sort
loop × serialization
loop × regex
loop × render
loop × I/O
recursive branch × repeated subproblem
request × repeated transform
```

# Complexity Table

Use:

| Operation | Time | Space | Frequency | Practical risk |
|---|---|---|---|---|
| build lookup | O(m) | O(m) | once | low |
| match users | O(n) | O(n) output | once | low |
| repeated find | O(n×m) | O(1) extra | once | high at scale |

# Practical Cost Model

Big O hides constants.

Estimate:

```text
operation count
input size
frequency
allocation
I/O
runtime environment
```

Example:

```text
n = 10
n² = 100 checks
```

may be trivial.

```text
n = 100,000
n² = 10^10 checks
```

is not.

# Threshold Reasoning

Avoid arbitrary universal thresholds.

Use product/environment evidence.

Possible classifications:

```text
NEGLIGIBLE_AT_EXPECTED_SCALE
ACCEPTABLE_WITH_BOUNDED_INPUT
SCALABILITY_RISK
CURRENT_PERFORMANCE_BOTTLENECK
MEMORY_RISK
I/O_DOMINATED
UNKNOWN_REQUIRES_MEASUREMENT
```

# Bounded Inputs

If input is guaranteed:

```text
max 12 calendar months
max 7 weekdays
max 20 feature flags
```

a simple O(n²) algorithm may be clearer and safer.

Document the bound.

Do not optimize away readability for asymptotic theory.

# Untrusted Inputs

If user/provider input can grow unexpectedly, worst-case behavior matters more.

Consider:

```text
DoS
memory exhaustion
ReDoS
parser blowups
```

Escalate to security review when relevant.

# Data Structure Selection

Choose based on operations.

Array:

```text
ordered iteration
small collections
duplicates
simple code
```

Set:

```text
membership
deduplication
unique values
```

Map:

```text
keyed lookup
joins/indexing
group ownership
```

Heap:

```text
top-k / priority
```

Queue/deque:

```text
BFS / scheduling
```

Do not select based on Big O alone; semantics/readability matter.

# Precomputation

Precompute when:

```text
same expensive result reused
inputs stable enough
memory cost acceptable
```

Avoid stale caches and hidden invalidation complexity.

# Caching

Caching is not free.

Record:

```text
cache key
lifetime
invalidation
memory
hit rate
```

Do not use a cache to hide an algorithm that can be simplified directly.

# Algorithm Rewrite Decision

Classify recommendation:

```text
KEEP_SIMPLE_IMPLEMENTATION
ADD_BOUND_OR_GUARD
CHANGE_DATA_STRUCTURE
PRECOMPUTE_INDEX
BATCH_IO
REDUCE_REPEATED_WORK
USE_BETTER_ALGORITHM
VIRTUALIZE_OR_PAGE
PROFILE_FIRST
BENCHMARK_FIRST
ESCALATE_DB_QUERY_REVIEW
ESCALATE_FRONTEND_PERFORMANCE_REVIEW
ESCALATE_SECURITY_REVIEW
```

# Preserve Semantics

Optimization must preserve:

- ordering;
- duplicates;
- equality semantics;
- error behavior;
- stable output;
- determinism;
- transaction meaning.

A `Set` rewrite that removes meaningful duplicates is incorrect.

# Map Key Semantics

Ensure key uniqueness actually matches domain semantics.

Do not index by a field that is not unique.

# Stable Ordering

A hash/indexed approach may change order.

Preserve accepted order explicitly.

# Memory Trade-Off

Example:

```text
O(n×m) time, O(1) extra
```

vs:

```text
O(n+m) time, O(m) extra
```

Choose using:

```text
input sizes
memory budget
frequency
latency target
```

# Readability Trade-Off

If the optimized algorithm is significantly harder to understand, require evidence that benefit matters.

Prefer:

```text
clear + fast enough
```

over:

```text
theoretically optimal + opaque
```

# Complexity Comments

Do not add comments such as:

```text
// O(n)
```

everywhere.

Comment when complexity constraint is non-obvious and important:

```text
// Build an index once to avoid O(users × permissions) matching.
// This path can receive 50k users.
```

# Benchmarking

Benchmark when:

- constants matter;
- two implementations share similar Big O;
- runtime/library behavior is uncertain;
- input distribution matters;
- optimization has complexity/readability trade-off.

Use representative data sizes.

# Benchmark Matrix

Include:

```text
small
typical
high
max supported
```

when practical.

Do not benchmark only 10 elements if production has 100k.

# Warmup / Runtime

For JIT runtimes, account for warmup and repeated measurements when microbenchmarking.

Avoid drawing strong conclusions from one timing.

# Microbenchmark Limits

A microbenchmark does not prove end-to-end latency.

Use profiling/system measurement after algorithm improvement when the user-visible/system performance matters.

# Profiling

Profile when:

```text
hot path uncertain
algorithm is not obviously dominant
rendering/DB/I/O may dominate
```

Potential evidence:

```text
CPU profile
flame graph
React profiler
browser performance trace
APM trace
DB query plan
```

This skill may recommend these but does not replace specialized performance skills.

# Before / After Evidence

For a material optimization record:

```text
old complexity
new complexity
old memory
new memory
representative benchmark/profile
behavioral tests
```

# Regression Tests

Optimization requires correctness tests.

Do not rely on benchmark output as correctness proof.

Keep/add tests at the proper behavior boundary.

# Property-Based Testing

Useful for algorithm rewrites when:

```text
many input combinations
ordering/deduplication
graph/tree logic
equivalence between old/new implementation
```

if repository tooling supports it.

Do not introduce property-testing infrastructure casually.

# Complexity Regression Guard

For truly critical algorithms, a benchmark/size guard may be appropriate.

Examples:

```text
100k items completes under accepted budget
memory stays under accepted budget
```

Keep thresholds environment-aware.

Do not create flaky nanosecond assertions.

# Frontend Example — Repeated Lookup

Before:

```ts
const rows = users.map(user => ({
  user,
  permission: permissions.find(p => p.userId === user.id),
}))
```

Time:

```text
O(n × m)
```

After:

```ts
const byUser = new Map(
  permissions.map(permission => [permission.userId, permission])
)

const rows = users.map(user => ({
  user,
  permission: byUser.get(user.id),
}))
```

Time:

```text
O(n + m)
```

Space:

```text
O(m)
```

Decision depends on actual sizes/frequency.

# Frontend Example — Parent/Child Tree

Before:

```ts
nodes.map(node => ({
  ...node,
  children: nodes.filter(candidate => candidate.parentId === node.id),
}))
```

Potential:

```text
O(n²)
```

Index children by parent:

```text
O(n)
```

expected build + traversal.

But if `n <= 12`, simpler version may be accepted.

# Frontend Example — Search Per Keystroke

A linear search:

```text
O(n)
```

may be fine for 100 items.

For 100k items on every keystroke, consider:

- debouncing;
- indexing;
- server-side search;
- virtualization;
- Web Worker;

depending on bottleneck.

Do not solve solely with a more complex algorithm.

# Backend Example — Repository Join in Memory

Before:

```text
for each order:
  find customer in customer array
```

→

```text
O(n × m)
```

Indexing may produce:

```text
O(n + m)
```

But if data originated from DB, a proper join/query may be better than loading both full sets.

Escalate query review.

# Backend Example — N+1

```ts
for (const order of orders) {
  const customer = await customers.findById(order.customerId)
}
```

Application loop may be O(n), but:

```text
n DB round trips
```

dominates.

Recommendation:

```text
batch / query join / repository method
```

not a Map after loading each row separately.

# Backend Example — Top Rankings

Sort all:

```text
O(n log n)
```

If only top 10 out of millions are needed:

- database ORDER BY/LIMIT;
- heap;
- selection;

may be better depending on ownership.

Do not bring millions into application memory to optimize locally.

# Graph Example

Dependency traversal:

```text
DFS + visited
→ O(v + e)
```

Without visited:

- repeated traversal;
- cycles;
- possible nontermination.

Record memory:

```text
O(v)
```

for visited + recursion/stack.

# Algorithmic Security

High-complexity paths on untrusted input can be security issues.

Examples:

```text
catastrophic regex
quadratic parser
unbounded decompression
graph expansion
hash collision attack
```

Escalate:

```text
ESCALATE_SECURITY_REVIEW
```

# Algorithmic Complexity vs Performance Review

This skill answers:

```text
How does computational work scale?
```

A frontend performance skill answers:

```text
Why is the user experience slow?
```

A backend performance review may answer:

```text
Why is throughput/latency poor?
```

They compose.

# Composition with Frontend Performance

Potential handoff:

```text
reviewing-frontend-performance
→ finds expensive list/chart/transform
→ analyzing-algorithmic-complexity
→ returns scaling/data-structure analysis
→ frontend review combines with render/network/bundle evidence
```

# Composition with Backend Review

Potential handoff:

```text
backend code/performance review
→ finds repeated scans/job growth/N+1-like pattern
→ analyzing-algorithmic-complexity
→ returns CPU/memory analysis
→ backend review decides query/I/O/architecture fix
```

# Composition with Performance Agent

Future:

```text
Performance Agent
├── system evidence
├── frontend/backend performance skills
├── analyzing-algorithmic-complexity
└── validation/benchmark evidence
```

Do not duplicate this skill's algorithm rules into every agent.

# Finding Structure

For each relevant path record:

```text
algorithm/path
input variables
realistic bounds
frequency
current time complexity
current space complexity
hidden work
dominant system cost
risk classification
candidate improvement
new time complexity
new space complexity
trade-offs
measurement needed
```

# Risk Classification

Use:

```text
NO_MEANINGFUL_SCALING_RISK
BOUNDED_COMPLEXITY_ACCEPTABLE
ALGORITHMIC_SCALABILITY_RISK
MEMORY_SCALABILITY_RISK
I_O_MULTIPLICATION
DATABASE_DOMINATED
RENDERING_DOMINATED
NETWORK_DOMINATED
SECURITY_COMPLEXITY_RISK
UNKNOWN_REQUIRES_MEASUREMENT
```

# Severity

Severity depends on:

```text
input growth
frequency
latency/memory impact
critical-path importance
production evidence
adversarial controllability
```

Do not label every O(n²) loop High.

# Over-Optimization Audit

Flag:

- replacing readable code for `n <= 10`;
- Map/Set everywhere;
- caches without invalidation plan;
- complex heap/DP algorithm without measured need;
- parallelism added before unnecessary work removed;
- microbenchmark-driven rewrite with no product impact.

# Under-Optimization Audit

Flag:

- quadratic join over large collections;
- repeated sort inside loop;
- repeated full-copy accumulation;
- unbounded recursion;
- no visited set in cyclic graph;
- per-item remote/DB I/O;
- expensive transform every render/request;
- huge materialized intermediate collections.

# Final Decision

Use:

```text
ALGORITHMIC_COMPLEXITY_ACCEPTABLE
ALGORITHMIC_COMPLEXITY_ACCEPTABLE_WITH_BOUNDS
ALGORITHMIC_OPTIMIZATION_RECOMMENDED
MEMORY_OPTIMIZATION_RECOMMENDED
BATCH_IO_RECOMMENDED
DATA_STRUCTURE_CHANGE_RECOMMENDED
PROFILE_BEFORE_OPTIMIZING
BENCHMARK_BEFORE_OPTIMIZING
ESCALATE_FRONTEND_PERFORMANCE_REVIEW
ESCALATE_BACKEND_PERFORMANCE_OR_QUERY_REVIEW
ESCALATE_SECURITY_REVIEW
ALGORITHMIC_COMPLEXITY_NOT_PRIMARY_BOTTLENECK
BLOCKED
```

## Output

Use `assets/algorithmic-complexity-analysis-record.md`.

## Completion Criteria

- [ ] Input variables are named independently where needed.
- [ ] Typical, high, and maximum supported input sizes are known or explicitly missing.
- [ ] Execution frequency is considered.
- [ ] Current time complexity is derived.
- [ ] Current space complexity is derived.
- [ ] Best/average/worst case is included only where relevant.
- [ ] Amortized complexity is included where relevant.
- [ ] Hidden nested/high-level work is inspected.
- [ ] Repeated lookup/sort/filter/includes/copy/serialization work is evaluated.
- [ ] Data-structure choices are assessed semantically, not mechanically.
- [ ] Ordering, duplicates, equality, and key uniqueness are preserved.
- [ ] Memory trade-offs are explicit.
- [ ] Real input bounds are used to decide whether asymptotic risk matters.
- [ ] Bounded small O(n²) code is allowed when simpler and safe.
- [ ] I/O, DB, network, rendering, serialization, and algorithmic costs are separated.
- [ ] N+1-style I/O multiplication is not misdiagnosed as only an O(n) CPU issue.
- [ ] Frontend rerender/DOM work is delegated to frontend performance review when dominant.
- [ ] Database/index/query issues are escalated rather than “optimized” only in memory.
- [ ] Untrusted worst-case input is escalated to security review when appropriate.
- [ ] Recommendations include old/new time and space complexity.
- [ ] Readability/maintainability trade-offs are recorded.
- [ ] Profiling/benchmarking is requested when constants/dominant bottleneck are uncertain.
- [ ] Benchmarks use representative scale rather than toy-only inputs.
- [ ] Correctness/regression tests protect algorithm rewrites.
- [ ] No optimization is recommended solely because notation looks theoretically worse.
- [ ] Final complexity decision is explicit.

## References

- Read `references/big-o-input-variables-and-realistic-bounds.md` first.
- Read `references/data-structures-lookups-sorting-grouping-and-top-k.md`.
- Read `references/space-amortized-recursion-graphs-and-dynamic-programming.md`.
- Read `references/hidden-work-copying-serialization-regex-and-frequency.md`.
- Read `references/io-database-network-rendering-and-system-bottlenecks.md`.
- Read `references/benchmarking-profiling-and-before-after-evidence.md`.
- Read `references/frontend-backend-and-performance-agent-composition.md`.
- Read `references/algorithmic-complexity-analysis-audit.md` before completion.
