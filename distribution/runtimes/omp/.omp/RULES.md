# Gantry harness

For meaningful implementation, remediation, migration, review or release work headed to a pull request, use `/harness-run`. Questions and exploration do not need it.

- Routing and the Final Pre-PR Gate are computed by `python3 .harness/bin/route.py`. Never write a routing plan or a gate record by hand.
- Change size is not change risk: classify a change by what it touches, not by how many lines it has.
- Specialist agents in `.omp/agents/` are read-only reviewers. They report; they do not implement fixes.
- Do not edit `.harness/`, installed agent or skill files, or existing lint, type, test and CI configuration to make a check pass. Ask the user.
- The main session owns routing, task fan-out and fan-in. Specialist agents do not spawn nested workers.
