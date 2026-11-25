"""The specification check: structure and traceability, not judgement."""
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "distribution/core/.harness/bin/spec.py"
work = Path(tempfile.mkdtemp(prefix="gantry-spec-"))
spec = work / "spec.md"


def check(text, lane="SPEC"):
    spec.write_text(text, encoding="utf-8")
    proc = subprocess.run([sys.executable, str(CHECKER), "check", str(spec), "--lane", lane], capture_output=True, text=True)
    return proc.returncode, proc.stdout


GOOD = """# Filter incidents by severity

## Problem
On-call engineers cannot narrow the incident list during a major outage.

## Behavior
- AC-1: `GET /incidents?severity=SEV1` returns only SEV1 incidents of the caller's tenant.
- **AC-2**: An unknown severity is rejected with 400.

## Out of scope
Wiring the control into a screen.

## Slices
1. Endpoint filter with its validation (AC-1, AC-2)

## Open questions
None.
"""

assert check(GOOD) == (0, "SPEC: PASS\n"), check(GOOD)

# A DESIGN-lane change needs its design, and passing tells the agent to wait for approval.
code, out = check(GOOD, "DESIGN")
assert code == 1 and "missing section: ## Design" in out, out
designed = GOOD.replace("## Slices", "## Design\nKeep the tenant predicate unconditional and add the severity to it. Rejected: a second repository method, which duplicates the scoping rule. Undo by removing the query parameter.\n\n## Slices")
code, out = check(designed, "DESIGN")
assert code == 0 and "wait for their approval before building" in out, out
code, out = check(GOOD.replace("## Slices", "## Design\nTBD.\n\n## Slices"), "DESIGN")
assert code == 1 and "too short to judge" in out, out

# Every criterion is delivered by a slice, and slices name only real criteria.
code, out = check(GOOD.replace("(AC-1, AC-2)", "(AC-1, AC-7)"))
assert code == 1 and "AC-2 is not delivered by any slice" in out and "refers to AC-7" in out, out
code, out = check(GOOD.replace("**AC-2**", "AC-1"))
assert code == 1 and "AC-1 appears more than once" in out, out

# Prose without criteria, a missing section, and a specification that is really several.
code, out = check(GOOD.replace("- AC-1: ", "").replace("- **AC-2**: ", "").replace(" (AC-1, AC-2)", ""))
assert code == 1 and "has no acceptance criteria" in out, out
code, out = check(GOOD.replace("## Out of scope\nWiring the control into a screen.\n\n", ""))
assert code == 1 and "missing section: ## Out of scope" in out, out
code, out = check(GOOD + "word " * 800)
assert code == 1 and "more than one specification" in out, out

# Open questions do not fail the check; they are put in front of the reader.
code, out = check(GOOD.replace("None.", "- Should SEV4 exist?\n- Who may filter?"))
assert code == 0 and "note: 2 open question(s)" in out, out

missing = subprocess.run([sys.executable, str(CHECKER), "check", str(work / "nope.md")], capture_output=True, text=True)
assert missing.returncode == 1 and "does not exist" in missing.stdout

# Approval records the text a person approved; a specification that fails the check cannot be approved.
def approve(name, text):
    (work / "docs/specs").mkdir(parents=True, exist_ok=True)
    (work / "docs/specs" / name).write_text(text, encoding="utf-8")
    proc = subprocess.run([sys.executable, str(CHECKER), "approve", f"docs/specs/{name}", "--project", str(work)],
                          capture_output=True, text=True)
    return proc.returncode, proc.stdout

code, out = approve("filter.md", GOOD)
assert code == 1 and "NOT APPROVED" in out and "missing section: ## Design" in out, out
assert not (work / ".harness/runtime/approvals.json").exists()
code, out = approve("filter.md", designed)
assert code == 0 and "SPEC: APPROVED (docs/specs/filter.md)" in out, out
recorded = json.loads((work / ".harness/runtime/approvals.json").read_text())
assert recorded["docs/specs/filter.md"]["sha256"] == hashlib.sha256(designed.encode()).hexdigest(), recorded
outside = subprocess.run([sys.executable, str(CHECKER), "approve", "/etc/hosts", "--project", str(work)], capture_output=True, text=True)
assert outside.returncode == 1 and "outside the project" in outside.stdout

print("SPEC TESTS: PASS")
