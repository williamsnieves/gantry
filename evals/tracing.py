"""Summarise a runtime's event stream: what each agent read and what it cost in context.

Pure functions over the events of `claude -p --output-format stream-json`, so
they can be unit tested without an agent runtime.
"""
from __future__ import annotations

from pathlib import Path

LEAD = "lead"
SUBAGENT_TOOLS = ("Agent", "Task")
# First match wins.
CATEGORIES = (
    ("agent-contract", (".harness/agents/",)),
    ("harness-core", (".harness/core/", ".harness/bin/", ".harness/evals/", ".harness/harness.config.yaml")),
    ("run-state", (".harness/runtime/",)),
    ("skill", (".agents/skills/", ".claude/skills/")),
    ("runtime-adapter", (".claude/", ".codex/", ".cursor/", ".opencode/", ".omp/", "AGENTS.md", "CLAUDE.md")),
)


def category(path: str) -> str:
    for name, prefixes in CATEGORIES:
        if path.startswith(prefixes):
            return name
    return "project"


def relative(raw: str, root: Path) -> str:
    path = Path(raw)
    try:
        return path.resolve().relative_to(root.resolve()).as_posix() if path.is_absolute() else path.as_posix()
    except ValueError:
        return raw


def words_read(root: Path, path: str, offset: int | None, limit: int | None) -> int:
    """Words in the part of the file a Read call returned; 0 if the file is gone."""
    try:
        lines = (root / path).read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return 0
    start = max((offset or 1) - 1, 0)
    chosen = lines[start:start + limit] if limit else lines[start:]
    return sum(len(line.split()) for line in chosen)


def summarise(events: list[dict], root: Path) -> dict:
    """Return per-agent context, output and reading totals, plus the heaviest files.

    `context_peak` is the largest prompt any single request of that agent
    carried (input plus cached tokens): how full its context got.
    `prompt_tokens` adds up the prompts of all its requests: what was paid for,
    mostly at the cached rate. Output tokens are not reported per agent: the
    stream carries only a partial count for each message. The run total is in
    the metrics.
    """
    owner: dict[str, str] = {}  # tool_use id of a launch -> subagent type
    agents: dict[str, dict] = {}
    files: dict[str, dict] = {}
    seen_messages: set[str] = set()

    def agent_of(event: dict) -> dict:
        name = owner.get(event.get("parent_tool_use_id") or "", LEAD)
        return agents.setdefault(name, {
            "launches": 0, "requests": 0, "context_peak": 0, "prompt_tokens": 0,
            "tool_calls": {}, "reads": 0, "words_read": {},
        })

    for event in events:
        if event.get("type") != "assistant":
            continue
        message = event.get("message") or {}
        stats = agent_of(event)
        usage = message.get("usage") or {}
        if usage and message.get("id") not in seen_messages:
            seen_messages.add(message.get("id"))
            prompt = sum(usage.get(key) or 0 for key in ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))
            stats["requests"] += 1
            stats["prompt_tokens"] += prompt
            stats["context_peak"] = max(stats["context_peak"], prompt)
        for block in message.get("content") or []:
            if not isinstance(block, dict) or block.get("type") != "tool_use":
                continue
            tool, tool_input = block.get("name"), block.get("input") or {}
            stats["tool_calls"][tool] = stats["tool_calls"].get(tool, 0) + 1
            if tool in SUBAGENT_TOOLS:
                name = str(tool_input.get("subagent_type") or "unnamed")
                owner[block.get("id")] = name
                launched = agents.setdefault(name, {
                    "launches": 0, "requests": 0, "context_peak": 0, "prompt_tokens": 0,
                    "tool_calls": {}, "reads": 0, "words_read": {},
                })
                launched["launches"] += 1
            elif tool == "Read" and tool_input.get("file_path"):
                path = relative(str(tool_input["file_path"]), root)
                count = words_read(root, path, tool_input.get("offset"), tool_input.get("limit"))
                kind = category(path)
                stats["reads"] += 1
                stats["words_read"][kind] = stats["words_read"].get(kind, 0) + count
                entry = files.setdefault(path, {"category": kind, "reads": 0, "words": 0, "agents": []})
                entry["reads"] += 1
                entry["words"] += count
                name = owner.get(event.get("parent_tool_use_id") or "", LEAD)
                if name not in entry["agents"]:
                    entry["agents"].append(name)

    by_category: dict[str, int] = {}
    for stats in agents.values():
        for kind, count in stats["words_read"].items():
            by_category[kind] = by_category.get(kind, 0) + count
    heaviest = sorted(files.items(), key=lambda item: -item[1]["words"])
    return {
        "agents": agents,
        "words_read_by_category": dict(sorted(by_category.items(), key=lambda item: -item[1])),
        "files": {path: entry for path, entry in heaviest},
    }


def print_summary(summary: dict, top: int = 12) -> None:
    kinds = list(summary["words_read_by_category"])
    print(f"  {'agent':30} {'reqs':>4} {'peak ctx':>9} {'prompt tok':>10} {'reads':>5}  words read: " + ", ".join(kinds))
    for name, stats in sorted(summary["agents"].items(), key=lambda item: -item[1]["prompt_tokens"]):
        read = "  ".join(f"{stats['words_read'].get(kind, 0):>6}" for kind in kinds)
        print(f"  {name:30} {stats['requests']:>4} {stats['context_peak']:>9} {stats['prompt_tokens']:>10} "
              f"{stats['reads']:>5}  {read}")
    print("  words read by category: " + ", ".join(f"{kind} {count}" for kind, count in summary["words_read_by_category"].items()))
    print(f"  heaviest files read (top {top}):")
    for path, entry in list(summary["files"].items())[:top]:
        print(f"    {entry['words']:>7} words  {entry['reads']} read(s) by {len(entry['agents'])} agent(s)  {path}")
