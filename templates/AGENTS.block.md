<!-- GANTRY:START -->
# Gantry harness

Start a feature, fix or migration with the `harness-start` skill; before a pull request, run `harness-run`. Questions and exploration need neither.

- Routing and the Final Pre-PR Gate are computed by `python3 .harness/bin/route.py`. Never write a routing plan or a gate record by hand.
- Change size is not change risk: classify a change by what it touches, not by how many lines it has.
- Specialist agents in `the runtime's agents directory` are read-only reviewers. They report; they do not implement fixes.
- Do not edit `.harness/`, installed agent or skill files, or existing lint, type, test and CI configuration to make a check pass. Ask the user.

Where things are: contracts in `.harness/core/` and `.harness/agents/`, skills in `.agents/skills/`, settings in `.harness/harness.config.yaml`, stack and check commands in `.harness/project.yaml`, project conventions in `docs/conventions.md` (read it first).
<!-- GANTRY:END -->
