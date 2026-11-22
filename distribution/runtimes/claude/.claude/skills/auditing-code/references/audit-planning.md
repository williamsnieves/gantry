# Audit Planning

## Audit Objective

Define the decision the audit should support:

- release readiness;
- technical-debt prioritization;
- migration risk;
- security posture;
- subsystem reliability;
- dependency health;
- brownfield understanding.

## Scope

Record:

- included directories, services, packages, or diff;
- excluded areas;
- critical user and system flows;
- trust boundaries;
- data sensitivity;
- deployment environment;
- available runtime evidence.

## Baseline Evidence

Inspect:

- architecture and development documentation;
- manifests and dependency locks;
- CI workflows and recent validation;
- tests;
- static-analysis configuration;
- incident or production evidence when available;
- active specifications or changes.

## Audit Strategy

Choose:

- broad sampling;
- critical-path deep dive;
- diff-focused audit;
- risk-focused audit;
- dependency-focused audit.

Do not claim repository-wide coverage from a narrow sample.

## Stop Conditions

Stop or narrow when:

- scope is undefined;
- required source is unavailable;
- generated or vendored code dominates results;
- a critical finding requires immediate escalation;
- evidence quality cannot support conclusions.
