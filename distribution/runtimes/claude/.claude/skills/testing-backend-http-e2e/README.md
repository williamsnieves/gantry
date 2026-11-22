# testing-backend-http-e2e

Tests critical backend behavior through a composed application and real HTTP requests.

Recommended full E2E:

```text
real HTTP
+ real controller/Application/Domain
+ real repository adapters
+ isolated real database
+ controlled provider-neutral external doubles
```

The skill validates public contracts and cross-layer side effects while avoiding duplication of exhaustive Domain, Use Case, repository, and provider-adapter suites.
