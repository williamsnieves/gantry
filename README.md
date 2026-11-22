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
