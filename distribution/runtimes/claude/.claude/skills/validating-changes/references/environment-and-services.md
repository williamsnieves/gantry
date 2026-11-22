# Environment and Services

## Discover Requirements

Identify:

- runtime versions;
- package manager;
- environment variables;
- containers;
- databases;
- message brokers;
- browsers;
- cloud emulators;
- external services;
- credentials;
- network access.

## Safety

- Never expose or log secrets.
- Do not use production credentials or mutate production systems.
- Do not create destructive test data without authorization.
- Prefer documented local or isolated test services.
- Do not install or start unrelated infrastructure silently.

## Not-Run Status

When an environment-dependent check cannot run, report:

- exact check;
- required service or credential;
- attempted command;
- observed blocker;
- whether CI is expected to cover it;
- residual risk.

A check not run is not a passing check.
