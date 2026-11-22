# Artifact Authoring

## Dependency Principle

Create artifacts only when their declared dependencies are satisfied.

Follow the configured artifact instructions and templates. Do not assume every project uses exactly proposal, specs, design, and tasks.

## Common Artifact Responsibilities

### Proposal

Captures:

- intent and problem;
- scope and exclusions;
- expected behavioral impact;
- affected capabilities;
- material risks or dependencies.

### Specifications

Capture:

- behavioral requirements;
- observable scenarios;
- added, modified, or removed behavior;
- compatibility expectations.

### Design

Captures technical direction when required:

- architectural choices;
- constraints;
- alternatives and trade-offs;
- data or interface changes;
- migration, rollout, security, performance, and operational implications.

Do not repeat the proposal or turn design into an implementation transcript.

### Tasks

Translate approved artifacts into an ordered implementation checklist.

### Custom Artifacts

Follow the configured template and dependency contract.

## Consistency Pass

Check:

- proposal scope is reflected in specs;
- design supports the specified behavior;
- tasks cover specs, design, validation, documentation, and operations;
- exclusions do not reappear as tasks;
- open decisions are not silently resolved.
