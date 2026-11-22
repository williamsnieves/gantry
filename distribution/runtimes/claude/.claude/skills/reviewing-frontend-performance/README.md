# reviewing-frontend-performance

Evidence-driven frontend performance review.

Roadmap evaluations:

```text
unnecessary rerenders
large dependency
duplicated request
unvirtualized list
route bundle
expensive chart
```

Core flow:

```text
measure
→ classify bottleneck
→ reduce architectural work
→ invoke analyzing-algorithmic-complexity when scaling is involved
→ verify before/after
```

The skill explicitly accounts for React Compiler/equivalent optimization before recommending manual memoization.
