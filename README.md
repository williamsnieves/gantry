# Loop Engineering Harness v1

Universal distribution of the portable software-engineering harness.

## One CLI

```bash
./leh.sh install --runtime cursor --project /path/to/repo
```

or:

```bash
./leh.sh install --runtime claude,codex,cursor,opencode,omp --project .
```

or simply:

```bash
./leh.sh install --runtime all --project .
```

On Windows PowerShell:

```powershell
.\leh.ps1 install --runtime all --project .
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

Claude receives its native `.claude/skills/` copy for maximum compatibility.

## Typical setup

```bash
./leh.sh plan   --runtime cursor,codex   --scope fullstack   --profile standard   --project ~/code/my-app

./leh.sh install   --runtime cursor,codex   --scope fullstack   --profile standard   --project ~/code/my-app

./leh.sh doctor --project ~/code/my-app
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
leh install
leh init
leh plan
leh status
leh doctor
leh uninstall
```

## Architecture

```text
                   Loop Engineering Harness
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

## Version

```text
1.0.0
```
