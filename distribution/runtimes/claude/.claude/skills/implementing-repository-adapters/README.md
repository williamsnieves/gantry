# implementing-repository-adapters

Implements real persistence behind accepted repository ports.

Core guarantees:

- explicit persistence ↔ Domain mapping;
- valid Domain reconstitution;
- exact contract semantics;
- authoritative constraints and concurrency;
- technical error translation;
- real isolated integration tests;
- shared parity with InMemory behavior;
- no ORM or database leakage inward.
