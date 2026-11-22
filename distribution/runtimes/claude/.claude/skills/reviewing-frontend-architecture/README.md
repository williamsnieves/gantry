# reviewing-frontend-architecture

Performs a holistic frontend architecture review against the definitive frontend standard.

It reviews:

```text
architecture profile and ownership
state and Effects
components and hooks
composition
styling and shared UI
accessibility
errors and recovery
testing
performance
security and privacy
abstractions and migrations
```

The skill explicitly separates mandatory violations, conventions, project-policy mismatches, accepted deviations, and optional suggestions.

It favors evidence-backed severity and the smallest remediation rather than subjective blockers or repository-wide rewrites.


Modern React performance review also checks React Compiler status before recommending `useMemo`, `useCallback`, or `React.memo`. Compiler-enabled new code defaults to compiler-managed memoization; existing manual memoization is not removed mechanically.
