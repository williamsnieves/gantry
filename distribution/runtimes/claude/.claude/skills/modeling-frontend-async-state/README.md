# modeling-frontend-async-state

Models optional and asynchronous frontend state around valid UI states.

It covers the roadmap cases:

```text
background refresh
optimistic update
partial data
retry
cancellation
Maybe versus discriminated union
```

The skill chooses state ownership first, prevents impossible boolean combinations, distinguishes initial loading from refresh, models data retention, keeps cancellation separate from generic error when appropriate, and avoids duplicating React Query/SWR/Apollo/Relay/RTK Query/framework state inside local hooks.
