# testing-react-hooks

Implements focused tests for React custom hooks with meaningful independent contracts.

It covers:

```text
observable state and commands
async load and failure
retry and reset
cancellation
stale responses and races
duplicate commands
optimistic update and rollback
cleanup and subscriptions
dependency injection
feature-semantic server-state wrappers
```

It avoids internal setters, reducer actions, Effects, refs, memoization, concrete adapters, global factories, server-state-library internals, arbitrary sleeps, and duplicated business or adapter cases.
