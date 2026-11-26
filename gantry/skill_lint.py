"""Lint skills: is each one short enough to read, written as steps, and reachable from something that runs?

A skill is text an agent pays for every time it reads it, and text nothing
names is never read at all. The rules are structural and deterministic; none
judges whether the advice in a skill is right.

    long          SKILL.md is over 500 lines: keep the procedure there and move detail to references/, read on demand
    no-steps      the procedure is not written as numbered steps
    no-command    nothing concrete to run or produce: no code block and no inline code
    no-recovery   no heading says what to do when a step fails or the work is blocked
    unreachable   no agent, contract or reachable skill names it, so nothing will ever read it
    description   an entry-point skill's description, which sits in every session, is over 60 words
    frontmatter   no name or description, or the name is not the directory's

Standard library only.
"""
from __future__ import annotations

import re
from pathlib import Path

MAX_LINES = 500
MAX_ENTRY_DESCRIPTION_WORDS = 60
RULES = {
    "long": f"over {MAX_LINES} lines; move detail to references/ and read it on demand",
    "no-steps": "no numbered steps",
    "no-command": "no code block or inline code: nothing concrete to run or produce",
    "no-recovery": "no heading for what to do when a step fails or the work is blocked",
    "unreachable": "nothing names it: no agent, contract or reachable skill",
    "description": f"entry-point description over {MAX_ENTRY_DESCRIPTION_WORDS} words, loaded in every session",
    "frontmatter": "name or description missing, or the name is not the directory's",
}
STEP = re.compile(r"^\s*\d+\.\s+\S", re.M)
RECOVERY = re.compile(r"^#{1,4} .*(fail|error|recover|troubleshoot|goes wrong|blocked|stop|escalat|cannot|pitfall|anti-pattern)", re.I | re.M)
CODE = re.compile(r"```|`[^`\n]+`")
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
REFERENCE_SUFFIXES = (".md", ".mdc", ".toml", ".yaml", ".yml", ".json")


def field(header: str, name: str) -> str:
    match = re.search(rf"^{name}:\s*(.*)$", header, re.M)
    return match.group(1).strip().strip("\"'") if match else ""


def named_in(name: str, text: str) -> bool:
    return bool(re.search(rf"(?<![\w-]){re.escape(name)}(?![\w-])", text))


def lint(skills_dir: Path, referenced_from: list[Path], entrypoints: tuple[str, ...] = ()) -> dict[str, dict]:
    """{skill: {"lines": n, "findings": [rule, ...]}} for every skill directory under `skills_dir`."""
    skills = {p.name: p / "SKILL.md" for p in sorted(skills_dir.iterdir()) if (p / "SKILL.md").is_file()} if skills_dir.is_dir() else {}
    texts = {name: path.read_text(encoding="utf-8", errors="replace") for name, path in skills.items()}
    inside = skills_dir.resolve()

    def read_all(root: Path) -> str:
        files = [root] if root.is_file() else [p for p in sorted(root.rglob("*")) if p.is_file() and p.suffix in REFERENCE_SUFFIXES]
        return "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in files)

    # What names a skill from outside the catalogue: agents, contracts, instruction files.
    outside = "\n".join(read_all(p) for root in referenced_from
                        for p in ([root] if root.is_file() else sorted(root.rglob("*")))
                        if p.is_file() and p.suffix in REFERENCE_SUFFIXES and inside not in p.resolve().parents)
    whole = {name: read_all(path.parent) for name, path in skills.items()}   # a skill and its own references
    reachable = {name for name in skills if name in entrypoints or named_in(name, outside)}
    grew = True
    while grew:   # a skill named by a reachable skill is reachable
        more = {name for name in skills if name not in reachable and any(named_in(name, whole[other]) for other in reachable)}
        grew, reachable = bool(more), reachable | more
    found = {}
    for name, text in texts.items():
        header = FRONTMATTER.match(text)
        body = text[header.end():] if header else text
        description = field(header.group(1), "description") if header else ""
        problems = []
        if not header or field(header.group(1), "name") != name or not description:
            problems.append("frontmatter")
        if len(text.splitlines()) > MAX_LINES:
            problems.append("long")
        if not STEP.search(body):
            problems.append("no-steps")
        if not CODE.search(body):
            problems.append("no-command")
        if not RECOVERY.search(body):
            problems.append("no-recovery")
        if name not in reachable:
            problems.append("unreachable")
        if name in entrypoints and len(description.split()) > MAX_ENTRY_DESCRIPTION_WORDS:
            problems.append("description")
        found[name] = {"lines": len(text.splitlines()), "words": len(body.split()), "findings": problems}
    return found


def summary(found: dict[str, dict], verbose: bool = False) -> list[str]:
    clean = sum(1 for entry in found.values() if not entry["findings"])
    lines = [f"Skills: {len(found)}, {sum(e['words'] for e in found.values())} words in total; {clean} with no finding"]
    for rule, meaning in RULES.items():
        hit = sorted(name for name, entry in found.items() if rule in entry["findings"])
        if hit:
            lines.append(f"  {rule:<12} {len(hit):>3}  {meaning}")
            if verbose or len(hit) <= 5:
                lines += [f"      {name} ({found[name]['lines']} lines)" for name in hit]
    return lines
