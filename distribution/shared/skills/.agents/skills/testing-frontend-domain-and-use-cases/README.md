# testing-frontend-domain-and-use-cases

Tests frontend inner layers without React or Infrastructure.

The roadmap purpose is implemented directly:

```text
Domain tests
→ pure

Use Case tests
→ InMemory repositories

true external-service ports
→ stubs/spies

all tests
→ fast + deterministic
```

Although these classes are consumed by a React frontend, Domain/Application tests remain framework-independent.
