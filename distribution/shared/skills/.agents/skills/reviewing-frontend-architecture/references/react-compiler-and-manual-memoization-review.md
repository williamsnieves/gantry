# React Compiler and Manual Memoization Review

React Compiler is a build-time optimizer that automatically handles memoization for React components and hooks.

Review policy:

```text
check compiler status first
→ determine affected compilation scope
→ prefer compiler-managed memoization for new compiled code
→ use manual memoization only for precise semantic identity or measured performance needs
```

For compiler-enabled new code:

- do not recommend `useMemo`, `useCallback`, or `React.memo` as routine hygiene;
- rely on compiler optimization first;
- use manual memoization as an escape hatch when precise control is required.

For non-compiled code:

- manual memoization still requires evidence;
- profile expensive rendering or calculations before increasing complexity.

For existing memoization during compiler adoption:

- do not remove mechanically;
- removal can change compiler output;
- preserve until tests/profiling show simplification is safe.

React Compiler primarily optimizes React components and hooks. It does not globally memoize every external function or share memoized results across unrelated components.

Memoization must never be used to fix correctness defects such as stale state, races, wrong Effect dependencies, or invalid ownership.
