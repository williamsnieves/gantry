# Entry-Point Discovery

Dead-code analysis is only as accurate as its entry-point model.

## Production Entry Points

Inspect as relevant:

- application startup;
- server handlers and routes;
- framework registration;
- command-line binaries;
- scheduled jobs and workers;
- background consumers;
- event handlers;
- package exports;
- mobile or desktop launch points;
- infrastructure handlers;
- migration runners.

## Non-Production Entry Points

Inspect:

- tests and fixtures;
- build scripts;
- generators;
- development tooling;
- examples;
- benchmarks;
- documentation snippets that are executable;
- release and deployment automation.

## Configuration-Driven Entry Points

Inspect:

- manifest fields;
- plugin lists;
- route tables;
- dependency injection;
- feature-flag registries;
- serializer names;
- template and asset references;
- environment-variable-selected modules.

## Boundary

Code used only by valid build, migration, operational, or test processes is not dead merely because production imports do not reach it.

Record the discovered entry-point inventory in the report.
