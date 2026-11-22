# refactoring-backend-toward-hexagonal-architecture

Executes one incremental brownfield refactor:

```text
characterize
→ establish seam
→ move behavior inward
→ introduce required ports/adapters
→ redirect one caller
→ validate
→ remove legacy path only when safe
```

It preserves contracts, data, transactions, idempotency, rollback, and observability while preventing a big-bang rewrite.
