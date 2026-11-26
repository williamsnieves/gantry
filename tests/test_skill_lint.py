"""Skill linter, and the catalogue held to what it is today. Run: python3 tests/test_skill_lint.py [--update]

The shipped skills have known findings, recorded in tests/skill-lint-baseline.json.
A skill may lose a finding; it may not gain one, and one that is too long may not grow.
"""
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from gantry import cli, skill_lint  # noqa: E402

BASELINE = ROOT / "tests/skill-lint-baseline.json"
GOOD = """---
name: {name}
description: Does one thing. Use when that thing is needed.
---
# Title

1. Run `tool check`.
2. Read the result.

## When a step fails

Stop and report the output.
"""

with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    skills = root / ".agents/skills"

    def skill(name, text=GOOD, extra=None):
        (skills / name).mkdir(parents=True, exist_ok=True)
        (skills / name / "SKILL.md").write_text(text.format(name=name))
        for path, content in (extra or {}).items():
            (skills / name / path).parent.mkdir(parents=True, exist_ok=True)
            (skills / name / path).write_text(content)

    skill("entry", GOOD + "\nThen read the `named-by-entry` skill.\n")
    skill("named-by-entry", extra={"references/more.md": "See also deep-one.\n"})
    skill("deep-one")                      # named only by a reference file of a reachable skill
    skill("named-by-agent")
    skill("orphan")
    skill("orphan-friend", GOOD + "\nSee orphan.\n")   # naming each other does not make either reachable
    skill("prose", "---\nname: {name}\ndescription: Explains a topic. Use when asked.\n---\n# Topic\n\nSome advice without anything to do.\n")
    skill("long", GOOD + "\n".join(f"line {n}" for n in range(skill_lint.MAX_LINES)))
    skill("misnamed", GOOD.replace("name: {name}", "name: other"))
    skill("wordy", GOOD.replace("Does one thing.", " ".join(["word"] * 70) + "."))
    (root / ".harness/agents").mkdir(parents=True)
    (root / ".harness/agents/reviewer.md").write_text("Read `.agents/skills/named-by-agent/SKILL.md` and `prose`, `long`, `misnamed`, `orphan-friendly`.\n")

    found = skill_lint.lint(skills, [root / ".harness"], ("entry", "wordy"))
    findings = {name: entry["findings"] for name, entry in found.items() if entry["findings"]}
    assert findings == {
        "orphan": ["unreachable"], "orphan-friend": ["unreachable"],
        "prose": ["no-steps", "no-command", "no-recovery"],
        "long": ["long"], "misnamed": ["frontmatter"], "wordy": ["description"],
    }, findings
    text = "\n".join(skill_lint.summary(found))
    assert "Skills: 10," in text and "4 with no finding" in text and "unreachable    2" in text and "      orphan (" in text, text

    # From the CLI: a report by default, a failing exit only when asked.
    import contextlib, io
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        cli.main(["skills", "--project", str(root)])
    assert "no-steps       1" in out.getvalue(), out.getvalue()
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            cli.main(["skills", "--project", str(root), "--strict"])
        raise AssertionError("--strict passed with findings")
    except SystemExit as stop:
        assert stop.code == 1

# The shipped catalogue against its baseline.
found = skill_lint.lint(ROOT / "distribution/shared/skills/.agents/skills", [ROOT / "distribution", ROOT / "templates"], cli.ENTRYPOINT_SKILLS)
now = {name: {"findings": entry["findings"], **({"lines": entry["lines"]} if "long" in entry["findings"] else {})}
       for name, entry in found.items() if entry["findings"]}
if "--update" in sys.argv:
    BASELINE.write_text(json.dumps(now, indent=1, sort_keys=True) + "\n")
    print(f"wrote {BASELINE.name}")
before = json.loads(BASELINE.read_text())
worse, better = [], []
for name, entry in now.items():
    known = before.get(name, {"findings": []})
    worse += [f"{name}: new finding `{rule}` ({skill_lint.RULES[rule]})" for rule in entry["findings"] if rule not in known["findings"]]
    if "long" in known["findings"] and entry.get("lines", 0) > known["lines"]:
        worse.append(f"{name}: already over {skill_lint.MAX_LINES} lines and grew from {known['lines']} to {entry['lines']}")
for name, known in before.items():
    better += [f"{name}: `{rule}`" for rule in known["findings"] if rule not in now.get(name, {"findings": []})["findings"]]
assert not worse, "skills got worse:\n  " + "\n  ".join(worse)
assert not better, "findings were fixed; record it with `python3 tests/test_skill_lint.py --update`:\n  " + "\n  ".join(better)
print(f"SKILL LINT TESTS: PASS ({len(found)} skills, {len(now)} with known findings)")
