# Reachability Analysis

## Evidence Sources

Use multiple signals when practical:

- import or dependency graph;
- symbol references;
- call graph;
- registration and dispatch tables;
- configuration references;
- test usage;
- build output;
- package export maps;
- runtime telemetry;
- ownership or consumer evidence.

## Graph Questions

For each candidate:

1. Which entry points could reach it?
2. Is the path direct, transitive, dynamic, or conditional?
3. Which configuration or feature state activates it?
4. Is it used only during build, migration, testing, or operations?
5. Does another repository or package import it?
6. Is the candidate itself generated or referenced by generated code?

## Negative Evidence

A search with zero textual references is not proof of non-use.

Negative evidence becomes stronger when:

- entry points are complete;
- dynamic mechanisms are excluded;
- package exports are checked;
- configuration is checked;
- consumers are inventoried;
- runtime observation covers relevant periods.

## Granularity

Analyze the smallest useful removable unit:

- symbol;
- export;
- file;
- module;
- dependency;
- feature path;
- compatibility layer.

A file may contain both used and unused code.
