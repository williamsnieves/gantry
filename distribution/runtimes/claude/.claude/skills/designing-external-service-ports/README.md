# designing-external-service-ports

Designs Application-owned, provider-neutral ports for external collaboration.

The skill defines:

- one focused capability;
- intention-revealing operations;
- neutral inputs and outputs;
- stable success and failure semantics;
- timeout, retry, idempotency, async, and security expectations;
- deterministic test doubles;
- Infrastructure adapter obligations.

It rejects SDK-shaped contracts, HTTP status handling, credentials in Application, generic API clients, and provider-specific leakage.
