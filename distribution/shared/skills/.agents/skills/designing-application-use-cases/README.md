# designing-application-use-cases

Designs one intention-focused Application Use Case with:

- stable `execute` boundary;
- primitive Request input;
- Domain conversion;
- inward repository and external-service ports;
- thin orchestration;
- explicit authorization, transaction, and idempotency semantics;
- Response DTO or `void`;
- focused tests.

It rejects Use Case chaining, concrete adapters, Domain logic in Application, HTTP semantics, and Entity outputs.
