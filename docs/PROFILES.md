# Scope and Delivery Profiles

## Scope profile

The scope profile gives the router a starting context.

```text
fullstack
backend
frontend
architecture
infrastructure
mixed
```

It is advisory.

Example:

```text
scope_profile = frontend
change = browser analytics with user identifiers
```

Security can still become REQUIRED.

## Delivery profile

### lean

Use for small/low-risk projects where non-triggered specialists should stay off aggressively.

### standard

Default balanced behavior.

### strict

Use for high-assurance projects. It may elevate project-policy requirements, but it still must not invent irrelevant gates.

## Principle

```text
profile
≠
permission to bypass risk triggers
```
