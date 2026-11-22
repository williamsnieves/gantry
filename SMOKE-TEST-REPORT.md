# Universal Distribution Smoke Test

## Result

**PASS**

## Verified

- `gantry plan --runtime all` completes without modifying the target project.
- `gantry install --runtime all` installs all five runtime overlays.
- Shared `.harness/` core is installed once.
- Shared `.agents/skills/` catalogue is installed once.
- Existing root `AGENTS.md` content is preserved and receives one managed harness block.
- Existing `.cursor/settings.json` is preserved.
- Existing `.codex/config.toml` is preserved.
- Existing `.omp/config.yml` is preserved.
- Existing `opencode.json` is preserved.
- Claude, Codex, Cursor, OpenCode, and OMP specialist adapters are installed.
- `gantry doctor` passes after installation.
- Runtime-specific uninstall removes only that runtime overlay.
- Shared core/skills remain while other runtimes are installed.
- Full uninstall with `--purge-shared` removes harness-managed shared files and preserves pre-existing project guidance.

## Scope

This validates the **universal distribution and installer mechanics**.

It does not replace the live 12-scenario semantic qualification for each runtime/model.

## Supported v1 runtimes

```text
claude
codex
cursor
opencode
omp
```
