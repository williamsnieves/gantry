# extracting-domain-model-from-legacy-code

Discovers the business model hidden inside legacy backend behavior before refactoring.

It gathers evidence from product behavior, tests, public contracts, persistence, incidents, jobs, and provider mappings; separates Domain meaning from technical concerns; and proposes:

```text
Entities
Value Objects
Domain Services
invariants
state transitions
semantic errors
repository concepts
```

The skill records confidence, contradictions, unknown legacy data, and product decisions. It does not modify production code.
