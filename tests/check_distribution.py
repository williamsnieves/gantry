"""Structural integrity checks for the harness distribution.

Run: python3 tests/check_distribution.py

These checks are deterministic and need no agent runtime. They catch the
defects that make installed content misleading to a model: instructions that
point at files that do not exist, duplicated skill copies that drift, invalid
or truncated metadata, and agents that reference unknown skills.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "distribution"
SKILLS = DIST / "shared/skills/.agents/skills"
CORE = DIST / "core/.harness"
RUNTIMES = DIST / "runtimes"

AGENT_FILES = {
    "claude": (".claude/agents", ".md"),
    "codex": (".codex/agents", ".toml"),
    "cursor": (".cursor/agents", ".md"),
    "opencode": (".opencode/agents", ".md"),
    "omp": (".omp/agents", ".md"),
}
LOCAL_REF = re.compile(r"`((?:references|assets|scripts)/[^`\s]+)`")
SKILL_PATH = re.compile(r"\.agents/skills/([a-z0-9-]+)/SKILL\.md")
HARNESS_PATH = re.compile(r"\.harness/((?:core|agents|evals|bin)/[A-Za-z0-9_./-]+\.[a-z]+)")
MIN_DESCRIPTION_CHARS = 40

errors: list[str] = []


def fail(check: str, path: Path, message: str) -> None:
    errors.append(f"[{check}] {path.relative_to(ROOT)}: {message}")


def frontmatter(path: Path, check: str) -> dict | None:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        fail(check, path, "missing frontmatter")
        return None
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        fail(check, path, f"frontmatter is not valid YAML ({str(exc).splitlines()[0]})")
        return None
    if not isinstance(data, dict):
        fail(check, path, "frontmatter is not a mapping")
        return None
    return data


def is_complete_sentence(description: str) -> bool:
    return description.rstrip().endswith((".", "!", "?"))


def check_skills() -> set[str]:
    names: set[str] = set()
    seen_descriptions: dict[str, str] = {}
    for skill_dir in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        skill = skill_dir / "SKILL.md"
        if not skill.exists():
            fail("skill-file", skill_dir, "has no SKILL.md")
            continue
        names.add(skill_dir.name)
        data = frontmatter(skill, "skill-frontmatter")
        if data is not None:
            if data.get("name") != skill_dir.name:
                fail("skill-frontmatter", skill, f"name {data.get('name')!r} does not match directory")
            description = " ".join(str(data.get("description") or "").split())
            if len(description) < MIN_DESCRIPTION_CHARS:
                fail("skill-frontmatter", skill, "description is missing or too short to discriminate")
            elif description in seen_descriptions:
                fail("skill-frontmatter", skill, f"description duplicates {seen_descriptions[description]}")
            else:
                seen_descriptions[description] = skill_dir.name
        for number, line in enumerate(skill.read_text(encoding="utf-8").splitlines(), 1):
            for ref in LOCAL_REF.findall(line):
                if "[" in ref or "<" in ref or "*" in ref:
                    continue  # template placeholder, not a real path
                if not (skill_dir / ref).exists():
                    fail("dangling-reference", skill, f"line {number} points at missing {ref}")
    return names


def check_single_skill_source() -> None:
    for skill in RUNTIMES.rglob("SKILL.md"):
        fail("single-source", skill, "skills must live only under distribution/shared; runtimes are rendered at install time")


def agent_description(path: Path, suffix: str) -> str | None:
    if suffix == ".toml":
        try:
            import tomllib
        except ModuleNotFoundError:  # Python 3.10
            match = re.search(r'^description\s*=\s*"(.*)"\s*$', path.read_text(encoding="utf-8"), re.M)
            return match.group(1) if match else None
        try:
            return tomllib.loads(path.read_text(encoding="utf-8")).get("description")
        except tomllib.TOMLDecodeError as exc:
            fail("agent-metadata", path, f"not valid TOML ({exc})")
            return None
    data = frontmatter(path, "agent-metadata")
    return None if data is None else data.get("description")


def check_agents(skill_names: set[str]) -> None:
    portable = {p.name for p in (CORE / "agents").iterdir() if p.is_dir()}
    for agent in sorted(portable):
        if not (CORE / "agents" / agent / "AGENT.md").exists():
            fail("agent-contract", CORE / "agents" / agent, "has no AGENT.md")
    for runtime, (directory, suffix) in AGENT_FILES.items():
        agent_dir = RUNTIMES / runtime / directory
        found = {p.stem for p in agent_dir.glob(f"*{suffix}")}
        for missing in sorted(portable - found):
            fail("agent-coverage", agent_dir, f"no adapter for portable agent {missing}")
        for extra in sorted(found - portable):
            fail("agent-coverage", agent_dir, f"adapter {extra} has no portable contract")
        for path in sorted(agent_dir.glob(f"*{suffix}")):
            description = agent_description(path, suffix)
            if not description:
                fail("agent-metadata", path, "missing description")
            elif not is_complete_sentence(" ".join(str(description).split())):
                fail("agent-metadata", path, "description is truncated mid-sentence")
            text = path.read_text(encoding="utf-8")
            referenced = set(SKILL_PATH.findall(text))
            if suffix == ".md":
                data = frontmatter(path, "agent-metadata") or {}
                referenced |= {str(s) for s in (data.get("skills") or [])}
                if data.get("skills"):
                    fail("context-budget", path, "preloads skills into every run; list them in the body to be read on demand")
            for name in sorted(referenced - skill_names):
                fail("agent-skill", path, f"references unknown skill {name}")


def check_harness_paths() -> None:
    sources = [p for p in RUNTIMES.rglob("*") if p.is_file()]
    sources += [SKILLS / "harness-run/SKILL.md", SKILLS / "harness-evaluate/SKILL.md"]
    sources += [ROOT / "templates/AGENTS.block.md"]
    for path in sources:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for ref in sorted(set(HARNESS_PATH.findall(text))):
            if not (CORE / ref).exists():
                fail("harness-path", path, f"points at missing .harness/{ref}")


AGENT_LOCAL_REF = re.compile(r"(?<![\w./-])((?:references|assets|scripts|evals|skills)/[A-Za-z0-9_./-]+\.[a-z]+)")


def check_agent_contracts() -> None:
    """Every file an agent contract cites must be installed with it."""
    for agent in sorted(p for p in (CORE / "agents").iterdir() if p.is_dir()):
        for path in sorted(agent.rglob("*.md")):
            text = path.read_text(encoding="utf-8")
            for ref in sorted(set(AGENT_LOCAL_REF.findall(text))):
                if not (agent / ref).exists() and not (path.parent / ref).exists():
                    fail("agent-contract", path, f"cites missing {ref}")
            for ref in sorted(set(HARNESS_PATH.findall(text))):
                if not (CORE / ref).exists():
                    fail("agent-contract", path, f"points at missing .harness/{ref}")


ALWAYS_LOADED = (
    "runtimes/claude/.claude/rules/00-portable-harness.md",
    "runtimes/cursor/.cursor/rules/00-portable-harness.mdc",
    "runtimes/omp/.omp/RULES.md",
)
ALWAYS_LOADED_WORD_LIMIT = 150


def check_always_loaded() -> None:
    """Files a runtime puts in every session stay a short map, not a rulebook."""
    for path in [DIST / relative for relative in ALWAYS_LOADED] + [ROOT / "templates/AGENTS.block.md"]:
        words = len(path.read_text(encoding="utf-8").split())
        if words > ALWAYS_LOADED_WORD_LIMIT:
            fail("context-budget", path, f"{words} words are loaded into every session; the limit is {ALWAYS_LOADED_WORD_LIMIT}")


def main() -> int:
    skill_names = check_skills()
    check_single_skill_source()
    check_agents(skill_names)
    check_harness_paths()
    check_agent_contracts()
    check_always_loaded()
    if errors:
        by_check: dict[str, int] = {}
        for line in errors:
            by_check[line.split("]")[0][1:]] = by_check.get(line.split("]")[0][1:], 0) + 1
        for line in errors:
            print(line)
        print()
        print("DISTRIBUTION CHECK: FAIL")
        for check, count in sorted(by_check.items()):
            print(f"  {check}: {count}")
        return 1
    print(f"DISTRIBUTION CHECK: PASS ({len(skill_names)} skills, {len(AGENT_FILES)} runtimes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
