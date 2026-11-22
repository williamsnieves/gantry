# testing-frontend-adapters

Tests frontend Infrastructure adapters against faithful technical boundaries.

The exact roadmap evaluations are:

```text
404
malformed payload
auth refresh
offline state
IndexedDB mapping
provider sandbox
```

Primary rule:

```text
real adapter
→ realistic boundary
→ verify technical mapping/failures
→ stable inward semantics
```

Use MSW/test servers/emulators/browser-like storage/sandboxes appropriately. Do not mock the adapter itself.
