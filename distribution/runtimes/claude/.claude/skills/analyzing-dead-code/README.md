# analyzing-dead-code

Determines whether suspected unused code and dependencies are safe to remove.

## Core Boundary

This skill analyzes and plans. It never deletes candidates automatically.

## Candidate Types

- symbols and exports;
- files and modules;
- routes, jobs, and feature paths;
- compatibility layers;
- dependencies;
- configuration and generated artifacts.

## Key Rules

- Model all valid entry points.
- Zero textual references is not proof.
- Inspect dynamic, convention-based, generated, operational, and external usage.
- Separate status from confidence.
- Design removal proof and rollback before deletion.

## Provenance

Adapted from the dead-code and audit references approved in the roadmap.
