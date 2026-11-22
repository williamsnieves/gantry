# testing-frontend-user-journeys

Implements a small, resilient set of critical frontend E2E journeys.

Roadmap purpose:

```text
design critical E2E flows
isolate environment and data
keep tests resilient
preserve useful failure diagnostics
avoid duplicating unit coverage
```

Core rule:

```text
lower levels prove local behavior
E2E proves critical cross-boundary integration
```

Do not build an all-E2E strategy.
