# modeling-frontend-domain

Decides whether a frontend Domain model is actually justified and models the smallest meaningful Domain when it is.

The skill focuses on:

```text
frontend vs backend authority
entities
Value Objects
pure Domain Services
invariants
domain errors
offline/local models
optimistic ownership
repository-port decisions
serialization
pure Domain tests
```

A valid result may be `NO_FRONTEND_DOMAIN_REQUIRED`.

It prevents ceremonial Domain layers, passive API entities, duplicated backend authority, framework/storage/HTTP leakage, validation-free Value Objects, forwarding services, endpoint-shaped repositories, and speculative shared Domain abstractions.
