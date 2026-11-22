# modeling-domain-data

Models domain data from semantics outward, not from tables inward.

Canonical progression:

```text
Conceptual Data Model
→ Logical Data Model
→ Physical Schema only when needed
```

Core rule:

```text
Domain Entity
≠ automatically one DB table
```

Roadmap-required coverage:

```text
entities/concepts
relationships
cardinality
ownership
identifiers
invariants
tenant boundaries
lifecycle
```

Output:

```text
domain-data-model.md
```

Next roadmap skill:

```text
modeling-event-flows
```
