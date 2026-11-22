---
name: harness-run
description: Run the complete portable engineering harness through OMP task agents.
---

Load the `harness-run` skill and execute the current change through the portable routing and pre-PR contracts.

Use project agents from `.omp/agents/`.

Prefer native `task` batch fan-out for independent specialist gates. Use structured results, preserve dynamic routing, and never run Reviewer before all REQUIRED gates are terminal.
