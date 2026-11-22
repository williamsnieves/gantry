# designing-react-effects

Decides whether a React Effect is necessary and designs external-system synchronization correctly.

It distinguishes Effects from:

```text
render-time derivation
event handlers
server-state libraries
external-store APIs
```

When an Effect is required, the skill defines ownership, resource identity, dependencies, stale-closure behavior, setup/update/cleanup, Strict Mode, SSR, races, cancellation, and tests.
