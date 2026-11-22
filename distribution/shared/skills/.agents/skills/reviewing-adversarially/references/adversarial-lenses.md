# Adversarial Lenses

Use concrete, domain-relevant lenses rather than a generic checklist.

## Input Hostility

- missing and null values;
- malformed encoding;
- duplicate fields;
- oversized input;
- unexpected but valid values;
- stale identifiers;
- reordered events;
- replayed requests.

## Identity and Authorization

- unauthenticated access;
- privilege escalation;
- cross-tenant identifiers;
- confused deputy behavior;
- authorization checked before versus after lookup;
- cached permissions;
- indirect object access.

## State and Concurrency

- duplicate execution;
- race conditions;
- stale reads;
- lost updates;
- partial writes;
- retry after timeout;
- concurrent cancellation;
- process restart.

## Dependencies

- timeout;
- partial response;
- duplicate webhook;
- out-of-order event;
- contradictory response;
- degraded service;
- rate limit;
- slow success after local timeout.

## Operations

- migration while old code is running;
- rollback after schema change;
- missing configuration;
- multi-region ordering;
- queue redelivery;
- log or metric failure;
- disk, memory, or connection exhaustion.

## Compatibility

- old clients;
- old data;
- mixed versions;
- renamed fields;
- default changes;
- feature-flag transitions;
- public API consumers.
