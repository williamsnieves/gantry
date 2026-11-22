# refactoring-react-features

Brownfield React feature refactoring.

Roadmap evaluations:

```text
oversized component
god hook
direct fetch
shared abstraction overreach
duplicated async state
inaccessible custom widget
```

Core rule:

```text
protect behavior
→ split by responsibility
→ establish correct ownership
→ remove duplicated state/infrastructure leakage
→ restore accessibility
→ validate
```

No splitting by line count and no speculative abstraction.
