# validating-backend-architecture

Validates modular hexagonal backend boundaries through executable and manual evidence.

Core direction:

```text
Infrastructure → Application → Domain
```

It checks:

- dependency direction;
- module/public contracts;
- repository and external-service ports;
- concrete adapter isolation;
- thin controllers;
- no Use Case chaining;
- primitive DTO and error boundaries;
- composition-root isolation;
- no runtime DI container or Service Locator;
- test-boundary correctness;
- cycles, transitive leaks, baselines, and accepted exceptions.

The skill reports findings and routes remediation; it does not rewrite code.
