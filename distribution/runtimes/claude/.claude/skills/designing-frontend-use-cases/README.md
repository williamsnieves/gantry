# designing-frontend-use-cases

Designs frontend Application Use Cases around one user or system intention.

It covers:

```text
intention and justification
primary operation
primitive vs Request DTO input
semantic ports
Domain orchestration
Application DTO/result output
failure semantics
cancellation
stale-response ownership
duplicate commands / idempotency
offline and partial success
composition
Use Case tests
```

It rejects React/JSX/browser/HTTP/concrete-adapter leakage, Use Case chaining, endpoint-shaped ceremony, duplicated Domain/backend authority, and Request DTOs with no boundary value.
