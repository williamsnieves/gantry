# Audit Dimensions

Apply only dimensions relevant to the target.

## Architecture and Flow

- unclear ownership;
- boundary violations;
- hidden coupling;
- circular dependencies;
- inconsistent source of truth;
- unsafe failure propagation;
- missing idempotency;
- concurrency and lifecycle errors.

## Correctness and Types

- violated invariants;
- unchecked null or optional values;
- unsafe casts;
- swallowed errors;
- partial state updates;
- stale state;
- race conditions;
- invalid assumptions about external contracts.

## Security

- authentication and authorization gaps;
- input validation;
- injection paths;
- secret exposure;
- insecure defaults;
- sensitive logging;
- path traversal or SSRF;
- dependency misuse;
- missing rate or abuse controls.

## Performance and Resources

- avoidable repeated work;
- unbounded collections;
- N+1 or expensive query patterns;
- blocking I/O;
- missing backpressure;
- memory or handle leaks;
- cache correctness;
- excessive serialization;
- retry amplification.

## Maintainability

- excessive complexity;
- duplication;
- unclear interfaces;
- fragile tests;
- configuration drift;
- undocumented contracts;
- obsolete compatibility layers;
- dead-code candidates;
- unused dependencies.

## Library and Dependency Use

- unsupported or deprecated APIs;
- duplicate libraries;
- unsafe wrappers;
- version conflicts;
- reinvented platform capabilities;
- incorrect lifecycle or concurrency use.
