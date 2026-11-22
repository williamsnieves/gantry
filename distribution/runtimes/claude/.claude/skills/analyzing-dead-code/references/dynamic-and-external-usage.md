# Dynamic and External Usage

## Dynamic Usage Risks

Inspect for:

- reflection;
- string-based lookup;
- decorators and annotations;
- framework auto-discovery;
- dependency injection;
- plugin loading;
- serialization or deserialization names;
- template references;
- dynamic imports;
- file-system scanning;
- convention-based routes;
- native bindings;
- generated registries.

## External Consumption

Assess:

- published package exports;
- public APIs and SDK contracts;
- downstream repositories;
- scripts outside the analyzed directory;
- CI and release automation;
- customer integrations;
- operational runbooks;
- database procedures or scheduled systems;
- infrastructure references.

## Compatibility

A deprecated symbol may still be active because:

- consumers have not migrated;
- a compatibility window remains;
- rollback depends on it;
- old data or events still reference it.

## Evidence Gap

When consumer inventory is incomplete, lower confidence and define a deprecation or telemetry phase instead of recommending immediate removal.
