---
name: analyzing-dead-code
description: Portable engineering capability `analyzing-dead-code`. Use when the harness
  or a specialist agent explicitly requires this named capability.
---
# Analyzing Dead Code

## Purpose

Determine which code and dependencies are genuinely unused, conditionally used, externally consumed, or unsafe to remove, and produce an evidence-based removal plan.

## Use When

- A repository contains suspected unused exports, files, modules, routes, flags, jobs, or dependencies.
- A migration left obsolete compatibility paths.
- Static analysis reports unreachable or unused candidates.
- A cleanup requires proof before removal.
- Bundle, build, maintenance, or attack-surface reduction depends on identifying dead code.

## Do Not Use When

- The request is a broad correctness, security, or maintainability audit.
- The task is to delete candidates immediately.
- The task is routine linting or mechanical validation.
- The user only wants unused local variables already handled by compiler or linter.
- Runtime, plugin, reflection, or external-consumer evidence is unavailable and removal safety cannot be assessed.

## Inputs

- Target repository, subsystem, package, or candidate list.
- Applicable `AGENTS.md`.
- Source, manifests, configuration, build and packaging rules.
- Tests, scripts, entry points, deployment definitions, and generated-code conventions.
- Optional runtime telemetry, import graphs, public API documentation, or consumer inventory.

## Required Context

1. Read the nearest applicable `AGENTS.md`.
2. Define analysis scope and removal objective.
3. Discover language, framework, build, packaging, and runtime entry-point conventions.
4. Identify generated, vendored, fixture, migration, and example code.
5. Inspect static and dynamic usage mechanisms before classifying candidates.
6. Do not modify or delete code.

## Workflow

1. **Scope:** Define target areas, candidate types, exclusions, and required confidence.
2. **Discover entry points:** Map production, test, build, CLI, job, plugin, route, framework, and package entry points.
3. **Generate candidates:** Use repository-native analyzers and targeted searches to find unused symbols, files, dependencies, and paths.
4. **Trace reachability:** Follow imports, calls, registration, configuration, reflection, serialization, templates, and runtime discovery.
5. **Check external use:** Assess public packages, APIs, scripts, automation, downstream repositories, and operational consumers.
6. **Classify candidates:** Assign status and confidence based on evidence.
7. **Assess removal impact:** Identify coupled tests, docs, configuration, migrations, generated artifacts, and compatibility implications.
8. **Design proof:** Define deletion validation, monitoring, rollback, and staged-removal strategy.
9. **Prioritize:** Order candidates by confidence, value, blast radius, and removal cost.
10. **Report:** Produce an inventory and safe removal plan without deleting anything.

## Decision Points

```text
If a candidate is reachable from a valid entry point:
    classify as used.
Else if it may be loaded dynamically or by convention:
    classify as uncertain until that mechanism is disproved.
Else if it is part of a documented public or operational contract:
    classify as externally consumed or compatibility-sensitive.
Else if evidence proves no valid internal or external path reaches it:
    classify as removable candidate.
Else:
    classify as unknown and define the missing evidence.
```

## Candidate Status

Use exactly one primary status:

- Used
- Conditionally used
- Externally consumed
- Generated or managed
- Deprecated but active
- Removal candidate
- Unknown

## Validation

Verify that:

- every removal candidate has reachability evidence;
- dynamic and convention-based entry points were considered;
- public and operational consumers were assessed;
- generated and managed code was not misclassified;
- tool output was manually interpreted;
- confidence and blast radius are explicit;
- the proposed proof plan could detect an incorrect removal;
- no code was deleted.

## Output

Use `assets/dead-code-analysis-report.md`.

## Completion Criteria

- [ ] Scope and entry points are explicit.
- [ ] Candidate generation methods are documented.
- [ ] Every candidate has status, confidence, and evidence.
- [ ] Dynamic and external consumption risks were considered.
- [ ] Removal impact and dependencies are mapped.
- [ ] A staged validation and rollback plan exists where needed.
- [ ] Candidates are prioritized.
- [ ] No automatic deletion occurred.

## References

- Read `references/entry-point-discovery.md` before generating candidates.
- Read `references/reachability-analysis.md` while tracing candidate usage.
- Read `references/dynamic-and-external-usage.md` for reflection, framework, plugin, and consumer risks.
- Read `references/candidate-classification.md` when assigning status and confidence.
- Read `references/safe-removal-planning.md` before recommending deletion.
- Read `references/tool-assisted-detection.md` when using analyzers.
