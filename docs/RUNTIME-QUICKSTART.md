# Runtime Quickstart

After `gantry install`, open the repository in the runtime.

| Runtime | Start |
|---|---|
| Claude Code | `/harness-run` |
| Codex | `$harness-run` |
| Cursor | `/harness-run` |
| OpenCode | `/harness-run` |
| Oh My Pi | `/harness-run` |

The runtime reads its adapter and the shared portable harness automatically.

## Where things live

| Concern | Path |
|---|---|
| Portable core | `.harness/core/` |
| Portable agent contracts | `.harness/agents/` |
| E2E oracle | `.harness/evals/` |
| Shared skills | `.agents/skills/` |
| Project harness config | `.harness/harness.config.yaml` |
| Claude agents | `.claude/agents/` |
| Codex agents | `.codex/agents/` |
| Cursor agents | `.cursor/agents/` |
| OpenCode agents | `.opencode/agents/` |
| OMP agents | `.omp/agents/` |

You normally should not need to manage these paths manually.
