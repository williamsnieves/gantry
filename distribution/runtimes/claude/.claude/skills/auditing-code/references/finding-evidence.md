# Finding Evidence

## Evidence Levels

### Confirmed

Supported by direct code path, reproducible behavior, failing test, configuration, or reliable runtime evidence.

### High-Confidence Risk

The vulnerable or incorrect path is present, but full triggering conditions cannot be reproduced locally.

### Observation

A maintainability or operational concern supported by evidence but not currently shown to cause failure.

### Question

A material uncertainty requiring owner input or further investigation.

## Minimum Evidence

A finding should identify:

- exact location;
- relevant code or configuration behavior;
- input or state that activates it;
- resulting failure or exposure;
- why existing controls do not prevent it.

## False-Positive Controls

Before reporting:

- trace callers and guards;
- inspect framework behavior;
- check environment-specific configuration;
- inspect tests and generated code;
- confirm the code is reachable;
- distinguish example, fixture, migration, and production paths.

## Root Cause

Group multiple symptoms when they share one cause.

Do not inflate counts by reporting every manifestation as a separate defect.
