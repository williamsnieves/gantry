# Installation Guide

## 1. Preview

```bash
./leh.sh plan --runtime cursor --project /path/to/repo
```

## 2. Install

```bash
./leh.sh install   --runtime cursor   --scope fullstack   --profile standard   --project /path/to/repo
```

Multiple runtimes:

```bash
./leh.sh install --runtime claude,codex,cursor,opencode,omp --project /path/to/repo
```

All runtimes:

```bash
./leh.sh install --runtime all --project /path/to/repo
```

## 3. Validate

```bash
./leh.sh doctor --project /path/to/repo
```

## 4. Use

```text
Claude Code → /harness-run
Codex       → $harness-run
Cursor      → /harness-run
OpenCode    → /harness-run
Oh My Pi    → /harness-run
```

You do not manually move skills or agents.

## Existing project files

The universal installer does not write runtime settings files such as:

```text
.codex/config.toml
opencode.json
.cursor/settings.json
.omp/config.yml
```

The runtime adapters already avoid requiring those files for core correctness.

Use the runtime package examples only when you later want model, concurrency, MCP or provider customization.

## Adding another runtime later

Add a new overlay under:

```text
distribution/runtimes/<runtime>/
```

and extend the CLI runtime manifest.

Do not copy portable policy into the new adapter.
