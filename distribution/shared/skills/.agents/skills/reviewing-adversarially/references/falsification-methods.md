# Falsification Methods

## Counterexample Construction

For each invariant, construct the smallest input or state that could violate it.

## Path Tracing

Trace:

- entry point;
- guards;
- state reads;
- decision branches;
- writes and side effects;
- external calls;
- error and cleanup paths;
- response construction.

## Differential Reasoning

Compare:

- first execution versus retry;
- success versus timeout after side effect;
- authorized versus unauthorized identity;
- single-threaded versus concurrent execution;
- old versus new client or schema;
- local success versus downstream failure.

## Failure Injection Reasoning

Ask what happens when failure occurs:

- before side effect;
- during side effect;
- after side effect but before acknowledgement;
- during rollback;
- during retry;
- during recovery after restart.

## Targeted Evidence

Use when available:

- focused tests;
- reproduction scripts;
- logs or traces;
- database constraints;
- static analysis;
- accepted project documentation.

Do not run destructive experiments against production systems.
