# migrating-to-frontend-vertical-slices

Incremental brownfield migration toward business capability vertical slices.

Roadmap evaluations:

```text
global components folder
services folder
shared hook ownership
circular dependencies
monorepo package extraction
```

Core rule:

```text
protect behavior
→ migrate one capability seam
→ define public boundary
→ repair dependency direction
→ validate
→ remove compatibility debt
→ repeat
```

No big-bang rewrite and no `shared/` dumping ground.
