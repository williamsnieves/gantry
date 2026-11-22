# wiring-backend-composition

Creates the explicit backend composition root.

Current project policy:

```text
get*    → cached shared Infrastructure
create* → fresh transient Use Case
```

The skill centralizes adapter selection and configuration, manages startup/shutdown, provides deterministic test reset, and prevents runtime DI containers, Service Locators, scattered environment reads, cached Use Cases, and per-request shared clients.
