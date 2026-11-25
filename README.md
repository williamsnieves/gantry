# Gantry

Universal distribution of the portable software-engineering harness.

## One CLI

```bash
./gantry.sh install --runtime cursor --project /path/to/repo
```

or:

```bash
./gantry.sh install --runtime claude,codex,cursor,opencode,omp --project .
```

or simply:

```bash
./gantry.sh install --runtime all --project .
```

On Windows PowerShell:

```powershell
.\gantry.ps1 install --runtime all --project .
```

## What the installer handles automatically

### Shared once

```text
.harness/
.agents/skills/
AGENTS.md managed block
```

### Runtime overlays

```text
Claude Code
→ .claude/agents/
→ .claude/skills/
→ .claude/rules/

Codex
→ .codex/agents/

Cursor
→ .cursor/agents/
→ .cursor/rules/

OpenCode
→ .opencode/agents/
→ .opencode/commands/

Oh My Pi
→ .omp/agents/
→ .omp/commands/
→ .omp/RULES.md
```

Codex, Cursor, OpenCode and OMP share one `.agents/skills/` installation.

Claude receives only the entry-point skills in `.claude/skills/`; its agents read the shared catalogue on demand.

## Typical setup

```bash
./gantry.sh plan   --runtime cursor,codex   --scope fullstack   --profile standard   --project ~/code/my-app

./gantry.sh install   --runtime cursor,codex   --scope fullstack   --profile standard   --project ~/code/my-app

./gantry.sh doctor --project ~/code/my-app
```

Then:

```text
Cursor     → /harness-run
Codex      → $harness-run
Claude     → /harness-run
OpenCode   → /harness-run
Oh My Pi   → /harness-run
```

## Project description

`gantry install` looks at the project once and writes what it finds to `.harness/project.yaml`: whether the project is new or existing, its languages, package managers and frameworks, its CI, and the commands that run its tests, lint, type checks and build. Nothing is executed and no model is called.

```bash
gantry inspect --project ~/code/my-app          # print it
gantry inspect --project ~/code/my-app --write  # refresh the saved file after changing tooling
```

The Validator starts from those commands instead of rediscovering them on every run. Agents cannot edit the file: the commands that judge a change are not chosen by the agent being judged. Correct it by hand when detection is wrong; a reinstall keeps your version and `inspect --write` replaces it. A command is listed only when the project declares it (a script, a dependency, a build file); anything else is reported as not detected.

## Onboarding

After installing, run the `harness-onboard` skill once in your agent (`/harness-onboard`, or `$harness-onboard` in Codex). It writes `docs/conventions.md`, a file of under 600 words that later runs and reviewers read first.

- In an existing project it reads the code and records what at least two files show, naming a file for each statement. Where the code does the same job two ways it lists both as an open question instead of choosing.
- In a new project it asks at most five questions, each with a default, and records the answers.

The file belongs to the project: edit it freely, and it stays if the harness is removed. `python3 .harness/bin/conventions.py check` verifies its headings, its length and that every path it cites exists.

## Starting a piece of work

Give your agent the request through the `harness-start` skill. The agent builds; the harness decides how much has to be settled first.

| Lane | When | Before building |
|---|---|---|
| `DIRECT` | No risk trigger: behavior, data and interfaces stay as they are | Nothing |
| `SPEC` | The accepted behavior changes | Acceptance criteria and slices in `docs/specs/<name>.md` |
| `DESIGN` | Architecture, security, data integrity, migration or compatibility is involved | The same, plus a design, and your approval |

The lane comes from `python3 .harness/bin/route.py lane`, from the same risk triggers that later choose the reviewers; the size of the change is not an input. `python3 .harness/bin/spec.py check` verifies that a specification has its sections, that every acceptance criterion has an id and is delivered by a slice, and that a `DESIGN` change has its design. The agent then builds slice by slice, test first, and `harness-run` reviews the result against the specification.

The routing plan records the lane. When a `SPEC` or `DESIGN` change reaches the Final Pre-PR Gate without an existing file passed as `--behavior-source`, the gate still passes but carries a condition saying the accepted behavior was not written down, so a person sees it in the pull request.

## Shipping, and what happened after

The `harness-ship` skill takes a reviewed change out and closes the loop on it.

```bash
python3 .harness/bin/release.py check --runtime claude
python3 .harness/bin/release.py record --outcome SHIPPED --change "#42 severity filter"
python3 .harness/bin/release.py record --outcome INCIDENT --change "#42" --note "filtered list showed other tenants" --missed SECURITY
```

`check` prints `RELEASE_READY`, `RELEASE_READY_WITH_CONDITIONS` or `RELEASE_BLOCKED`. It requires the Final Pre-PR Gate to pass, and adds what only matters when shipping: a migration, a release-only change, or a change with a `MIGRATION`, `INFRASTRUCTURE` or `DATA_INTEGRITY` trigger needs a `## Rollout` section in its specification (the order it is deployed in, how it is verified in production, how it is undone); a change users will notice carries a condition when the project keeps a changelog and the change does not touch it.

`record` appends a line to `docs/releases.md`. A rollback or an incident says what happened and, with `--missed`, which risk nobody declared when the change was routed. The harness does not deploy and does not watch production: the record is written by whoever saw the outcome. It is the list of what got past the review.

## Project scope

```text
fullstack
backend
frontend
architecture
infrastructure
mixed
```

This is advisory context for routing, **not a hard gate suppressor**.

A frontend project can still activate Security or Infrastructure if the actual change creates those risks.

## Delivery profiles

```text
lean
standard
strict
```

They are initial operating presets. Risk triggers and portable gate policy remain authoritative.

## Guardrails

A guardrail is something the harness guarantees whatever the agent decides. None of them is decided by a model: each is a rule over the files, the routing plan and the recorded gate results, so it fires the same way every time. Which ones apply to a change follows its risk: the lane and the triggers choose them, as they choose the reviewers.

`python3 .harness/bin/route.py guardrails` prints the list:

```text
ANY
  the harness's files and routing state are not edited by the agent
    every runtime: the final gate rejects a routing plan or a report that was changed by hand
    with hooks: the edit is denied
SPECIFY
  how much is settled before building follows the risk, not the size
    every runtime: `route.py lane`; `route.py plan` computes the lane again from the change itself
  a specification has its criteria, and each criterion is delivered by a slice
    every runtime: `spec.py check`
  a design is approved by a person
    every runtime: the final gate carries a condition until `spec.py approve` was run on the current text
    with hooks: `spec.py approve` asks the person to confirm; a reviewing agent cannot run it
BUILD
  a failing check is fixed in the code, not by weakening the check
    every runtime: the final gate carries a condition naming any lint, type, test or CI configuration the change edits
    with hooks: the edit and `--no-verify` are denied (not in the lean profile)
  a secret does not leave in the change
    every runtime: `scan.py` reads every added line; the final gate blocks on a credential in a provider's format or a private key, and carries a condition for anything that may be one
    with hooks: `git commit` and `git push` are denied while one is there
  code that needs a security reviewer gets one
    every runtime: a risky pattern in the added lines adds the SECURITY trigger to the routing plan, which routes the Security gate
REVIEW
  a reviewer reports and does not fix; a report is what the reviewer wrote
    every runtime: the final gate rejects a report changed after its result was recorded
    with hooks: a reviewer can write only its own report, and nobody else can write it
  the review stops at the first stage that does not pass
    every runtime: `route.py next`; the final gate stays blocked
    with hooks: launching a later gate is denied (not in the lean profile)
  a risk a gate sees outside its own scope is not lost under its pass
    every runtime: `route.py gate --trigger` records it; the router asks for the plan to be rerun with it, and the final gate carries a condition while no routed gate has judged it
  a result counts only for the version of the change it judged
    every runtime: results are tied to a digest of the change; an edit makes them stale
RELEASE
  a pull request is opened only after every required gate passed
    every runtime: `route.py ready` exits non-zero
    with hooks: `gh pr create` is denied (not in the lean profile)
  a change that moves data, schema or infrastructure ships with a written rollout: order, verification, undo
    every runtime: `release.py check` blocks without a `## Rollout` section in the specification
    with hooks: `gh pr merge` is denied while it blocks (not in the lean profile)
  a change users will notice is in the changelog, when the project keeps one
    every runtime: `release.py check` carries a condition
OPERATE
  what happened after shipping is written down, and a failure names the risk nobody declared
    every runtime: `release.py record` appends to docs/releases.md; nothing forces it to be run
```

The security scan (`python3 .harness/bin/scan.py`) reads only the lines the change adds. A credential in a format a provider issues, or a private key, blocks the final gate; a line marked `gantry:allow` becomes a condition a person confirms. A value that may be a credential is a condition. A risky code pattern (dynamic code execution, unescaped markup, queries or shell commands built from strings, unsafe deserialization, disabled TLS verification, weak hashes, wildcard CORS) is not a verdict: it adds the `SECURITY` trigger, so the Security gate, which works from STRIDE, the OWASP Top 10, the CWE Top 25 and OWASP ASVS, reviews the change.

"Every runtime" is what holds on any tool, because the router computes it. "With hooks" is what a runtime with command hooks adds by refusing the action when it is attempted; today that is Claude Code. A hook is a first barrier, not a boundary: a shell command can still write a file, which is why each guardrail also has a check at the final gate.

## Safety

The installer:

- preserves unrelated runtime configuration;
- manages one bounded block in `AGENTS.md`;
- tracks every installed harness-owned file and its SHA-256;
- refuses to overwrite unmanaged files without `--force`;
- refuses to overwrite locally modified harness files without `--force`;
- supports `plan`/dry-run;
- supports `doctor`;
- supports runtime-by-runtime uninstall;
- can purge shared core/skills after all runtimes are removed.

## CLI

```text
gantry install
gantry init
gantry plan
gantry status
gantry doctor
gantry uninstall
```

## Architecture

```text
                            Gantry
                              │
                 shared portable installation
                    .harness/
                  .agents/skills/
                      AGENTS.md
                              │
       ┌──────────┬───────────┼──────────┬──────────┐
       ↓          ↓           ↓          ↓          ↓
    Claude      Codex       Cursor    OpenCode     OMP
   .claude/    .codex/     .cursor/   .opencode/  .omp/
```

Runtime adapters execute the same routing, handoff, blocking, re-review and Final Pre-PR contracts.

## Development

```bash
pip install "PyYAML>=6.0"
python3 tests/check_distribution.py   # structural integrity of distribution/
python3 tests/smoke_test.py           # install / doctor / uninstall round trip
python3 tests/test_detect.py          # project detection
python3 tests/test_spec.py            # specification check
python3 tests/test_scan.py            # security scan of added lines
python3 tests/test_release.py         # release gate and release record
python3 tests/test_eval_scoring.py    # scenario scorer
python3 tests/test_route.py           # deterministic router
python3 tests/test_hook.py            # pre-tool-use guard
```

`evals/` runs the routing scenarios against a real agent runtime; see [evals/README.md](evals/README.md).

Skills live once under `distribution/shared/skills/`. The installer renders them per runtime; do not add skill copies under `distribution/runtimes/`.

## Version

```text
1.0.0
```
