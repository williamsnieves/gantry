# implementing-external-service-adapters

Implements provider-specific Infrastructure adapters behind accepted Application ports.

Core guarantees:

- exact port fidelity;
- explicit provider request/response mapping;
- stable semantic failure translation;
- safe timeout, retry, idempotency, rate-limit, and reconciliation;
- credentials and SDK details isolated in Infrastructure;
- realistic sandbox/emulator/contract evidence;
- no vendor leakage inward.
