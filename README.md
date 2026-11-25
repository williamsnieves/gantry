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
