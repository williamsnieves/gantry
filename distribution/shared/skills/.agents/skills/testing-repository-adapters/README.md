# testing-repository-adapters

Tests concrete repository adapters against isolated real persistence.

Core evidence:

- authoritative migrations;
- shared contract parity;
- Domain round trips and reconstitution;
- real constraints and concurrency;
- transactions and rollback;
- ordering, pagination, and deletion;
- invalid stored data and error translation;
- deterministic cleanup and honest infrastructure-failure classification.

Mocks and InMemory repositories are never presented as proof of real persistence behavior.
