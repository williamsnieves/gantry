# planning-frontend-test-strategy

Maps frontend behavior and risk to the lowest reliable test boundary.

It plans:

```text
Domain
Use Case
adapter
hook
component
accessibility
visual
route/package integration
E2E
manual or assistive-technology evidence
```

The skill defines test doubles, realistic environments, determinism, flakiness controls, CI placement, regression ownership, and evidence gaps.

It prevents all-E2E strategies, duplicate scenarios, Domain mocking, repository mocks where InMemory ports exist, implementation-detail assertions, and automated-accessibility claims of full conformance.
