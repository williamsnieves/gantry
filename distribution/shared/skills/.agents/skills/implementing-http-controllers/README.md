# implementing-http-controllers

Implements thin REST delivery adapters around accepted Application Use Cases.

Core guarantees:

- transport-only validation;
- trusted auth/context extraction;
- primitive Application Request mapping;
- one Use Case intention;
- stable success response;
- safe semantic error translation;
- no repository, provider, transaction, or Domain business logic in controllers.
