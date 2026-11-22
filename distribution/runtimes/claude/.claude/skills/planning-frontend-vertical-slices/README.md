# planning-frontend-vertical-slices

Plans the smallest frontend delivery sequence by user-visible behavior.

Each slice connects only the boundaries required by the selected architecture profile:

```text
user intent
→ UI/state/orchestration
→ data or browser boundary
→ visible result
→ accessibility and focused tests
```

The skill preserves capability ownership and prevents technical-layer batching, ceremonial architecture, speculative sharing, and test duplication.
