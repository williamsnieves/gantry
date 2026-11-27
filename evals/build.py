"""Ask a real agent runtime to build a change, with and without the harness, and score what it built with tests it never saw.

    python3 evals/build.py --runtime claude                          # every case, with the harness
    python3 evals/build.py --runtime claude --arm bare --arm harness # the same request with and without it
    python3 evals/build.py --runtime claude --case resolve-incident --trials 2
    python3 evals/build.py --solution reference                      # score the reference solutions; calls nothing
    python3 evals/build.py --runtime claude --dry-run                # build sandboxes, call nothing

Each case in evals/build-cases/ is a request for a change to evals/fixture,
with the interface it must keep, and a set of hidden tests. The agent gets the
request and the repository. When it stops, the project's own checks are run on
what it left, then the hidden tests are copied in and run. Hidden tests whose
name starts with `[edge]` cover what the request implies and does not spell
out; the others cover what it says.

Arms:
  harness   the harness is installed and the request is built with harness-start,
            stopping before the review
  bare      the same repository with no harness

`reference/` holds a solution that passes every hidden test and `naive/` one
that passes the plain ones and fails the edges; `--solution` scores them, which
is how the hidden tests themselves are checked.

A live trial calls the agent runtime and costs tokens. It needs npm and network
access once, to install the fixture's dependencies.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import run  # noqa: E402
import tracing  # noqa: E402

CASES = ROOT / "evals/build-cases"
ARMS = ("harness", "bare")
SOLUTIONS = ("reference", "naive")
CHECKS = {"test": ["npm", "test"], "typecheck": ["npm", "run", "typecheck"], "lint": ["npm", "run", "lint"]}
EDGE = "[edge]"
TEST_FILE = (".test.ts", ".test.tsx")

HEADLESS = (
    "Nobody can answer questions during this run: where you would ask, take the answer you would assume and say so at the end. "
    "Dependencies are installed; `npm test`, `npm run typecheck` and `npm run lint` work, and there is no database. "
    "Do not commit and do not open a pull request."
)
PROMPTS = {
    "harness": "{request}\nBuild this with the harness-start skill, through its build step. Stop there: do not run the review "
               "(harness-run). If the lane asks for a person's approval, it is given for this run; do not run `spec.py approve`.\n\n" + HEADLESS + "\n",
    "bare": "{request}\nBuild this.\n\n" + HEADLESS + "\n",
}
BUILD_TOOLS = (
    "Bash(npm test:*)", "Bash(npm run test:*)", "Bash(npm run typecheck:*)", "Bash(npm run lint:*)",
    "Bash(npx vitest:*)", "Bash(npx tsc:*)", "Bash(npx eslint:*)", "Bash(mkdir:*)",
    "Bash(python3 .harness/bin/check.py:*)", "Bash(python3 .harness/bin/spec.py:*)", "Bash(python3 .harness/bin/refactor.py:*)",
)


def changed_files(sandbox: Path) -> list[str]:
    out = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"], cwd=sandbox, capture_output=True, text=True).stdout
    return sorted(line[3:].strip().strip('"') for line in out.splitlines()
                  if line.strip() and not line[3:].startswith((".harness/runtime/", "node_modules")))


def own_tests(sandbox: Path, files: list[str]) -> dict:
    """What the agent wrote to test its own work: test files touched and the test cases in them."""
    touched = [path for path in files if path.endswith(TEST_FILE)]
    cases = 0
    for path in touched:
        text = (sandbox / path).read_text(encoding="utf-8", errors="replace") if (sandbox / path).is_file() else ""
        cases += text.count("\n  it(") + text.count("\n  test(") + text.count("\n    it(") + text.count("\n    test(")
    return {"files": touched, "cases": cases}


def run_checks(sandbox: Path) -> dict[str, bool]:
    return {name: subprocess.run(command, cwd=sandbox, capture_output=True, text=True).returncode == 0 for name, command in CHECKS.items()}


def run_hidden(sandbox: Path, case_dir: Path) -> dict:
    """Copy the hidden tests in, run them, and count: {plain: [passed, total], edge: [passed, total], failed: [names]}."""
    hidden = case_dir / "hidden"
    files = sorted(path.relative_to(hidden).as_posix() for path in hidden.rglob("*") if path.is_file())
    shutil.copytree(hidden, sandbox, dirs_exist_ok=True)
    report = sandbox / ".hidden-report.json"
    proc = subprocess.run(["npx", "vitest", "run", *files, "--reporter=json", f"--outputFile={report.name}"],
                          cwd=sandbox, capture_output=True, text=True)
    score = {"plain": [0, 0], "edge": [0, 0], "failed": []}
    try:
        data = json.loads(report.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {**score, "error": f"the hidden tests could not be run: {(proc.stdout + proc.stderr).strip()[-600:]}"}
    for suite in data.get("testResults", []):
        if not suite.get("assertionResults"):  # a file that does not load: an interface the request named is not there
            score["failed"].append(f"{Path(suite.get('name', '?')).name}: did not load: {str(suite.get('message', '')).strip()[:300]}")
        for test in suite.get("assertionResults", []):
            kind = "edge" if test["title"].startswith(EDGE) else "plain"
            score[kind][1] += 1
            if test["status"] == "passed":
                score[kind][0] += 1
            else:
                score["failed"].append(test["title"])
    for path in files:
        (sandbox / path).unlink()
    report.unlink(missing_ok=True)
    return score


def expected_hidden(case_dir: Path) -> dict[str, int]:
    """How many hidden tests of each kind the case has, read from its files: what a result is counted against."""
    counts = {"plain": 0, "edge": 0}
    for path in (case_dir / "hidden").rglob("*"):
        if path.is_file():
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.strip().startswith("it("):
                    counts["edge" if f'it("{EDGE}' in line else "plain"] += 1
    return counts


def run_trial(case_dir: Path, case: dict, arm: str, args: argparse.Namespace, parent: Path, out: Path | None, trial: int) -> dict:
    sandbox = run.build_sandbox(case_dir, args.runtime or "claude", parent, args.dependencies, install=arm == "harness")
    prompt = PROMPTS[arm].format(request=case["request"].strip() + "\n")
    record: dict = {"case": case_dir.name, "arm": args.solution or arm, "trial": trial}
    if args.dry_run:
        record.update(dry_run=True, sandbox=str(sandbox), prompt=prompt)
        return record
    if args.solution:
        shutil.copytree(case_dir / "reference", sandbox, dirs_exist_ok=True)
        if args.solution == "naive":  # the reference with the files that get the edges wrong
            shutil.copytree(case_dir / "naive", sandbox, dirs_exist_ok=True)
        record["metrics"] = {}
    else:
        trace_file = out / f"{case_dir.name}-{arm}-{trial}-trace.jsonl"
        record["metrics"] = run.DRIVERS[args.runtime](prompt, sandbox, args, BUILD_TOOLS, trace_file)
        if trace_file.exists():
            events = [json.loads(line) for line in trace_file.read_text(encoding="utf-8").splitlines() if line.strip()]
            summary = tracing.summarise(events, sandbox)
            lead = summary["agents"].get("lead", {})
            record["trace"] = {"requests": lead.get("requests"), "context_peak": lead.get("context_peak"),
                               "words_read": lead.get("words_read", {}), "tool_calls": lead.get("tool_calls", {}),
                               "skills_read": sorted(path for path in summary.get("files", {}) if "/skills/" in path)}
            text = trace_file.read_text(encoding="utf-8")
            record["trace"]["ran_check_py"] = "bin/check.py" in text
            record["trace"]["ran_lane"] = "route.py lane" in text
    files = changed_files(sandbox)
    record["changed"] = files
    record["own_tests"] = own_tests(sandbox, files)
    record["specification"] = [path for path in files if path.startswith("docs/specs/")]
    record["checks"] = run_checks(sandbox)
    record["hidden"] = run_hidden(sandbox, case_dir)
    record["expected"] = expected_hidden(case_dir)
    if out and not args.solution:
        diff = subprocess.run(["git", "diff", "HEAD"], cwd=sandbox, capture_output=True, text=True).stdout
        new = "".join(f"\n=== new file: {path}\n{(sandbox / path).read_text(encoding='utf-8', errors='replace')}"
                      for path in files if (sandbox / path).is_file() and path not in diff)
        (out / f"{case_dir.name}-{arm}-{trial}-change.diff").write_text(diff + new, encoding="utf-8")
    if args.keep_sandboxes:
        record["sandbox"] = str(sandbox)
    else:
        shutil.rmtree(sandbox, ignore_errors=True)
    return record


def passed(record: dict, kind: str) -> str:
    got, expected = record["hidden"][kind][0], record["expected"][kind]
    return f"{got}/{expected}"


def print_report(records: list[dict]) -> None:
    print()
    print(f"{'case':20} {'arm':10} {'trial':>5}  {'said':>6} {'edges':>6}  {'checks':16} {'own tests':>9} {'spec':>4} {'cost $':>7} {'secs':>6}  detail")
    for r in records:
        m = r["metrics"]
        checks = " ".join(f"{name[:4]}:{'ok' if ok else 'NO'}" for name, ok in r["checks"].items())
        cost = f"{m['cost_usd']:.2f}" if m.get("cost_usd") is not None else "-"
        detail = m.get("error") or r["hidden"].get("error") or "; ".join(r["hidden"]["failed"])[:160]
        print(f"{r['case']:20} {r['arm']:10} {r['trial']:>5}  {passed(r, 'plain'):>6} {passed(r, 'edge'):>6}  {checks:16} "
              f"{r['own_tests']['cases']:>9} {'yes' if r['specification'] else '-':>4} {cost:>7} {str(m.get('wall_seconds') or '-'):>6}  {detail}")
    print()
    for arm in dict.fromkeys(r["arm"] for r in records):
        mine = [r for r in records if r["arm"] == arm]
        total = lambda kind: (sum(r["hidden"][kind][0] for r in mine), sum(r["expected"][kind] for r in mine))
        costs = [r["metrics"]["cost_usd"] for r in mine if r["metrics"].get("cost_usd") is not None]
        skills = sorted({path for r in mine for path in (r.get("trace") or {}).get("skills_read", [])})
        print(f"{arm}: what the request says {total('plain')[0]}/{total('plain')[1]}, edges {total('edge')[0]}/{total('edge')[1]}, "
              f"checks green in {sum(all(r['checks'].values()) for r in mine)}/{len(mine)} trials"
              + (f", ${sum(costs):.2f}" if costs else "") + (f", skills read: {', '.join(skills)}" if skills else ""))


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a change with and without the harness and score it with hidden tests.")
    parser.add_argument("--runtime", choices=sorted(run.DRIVERS))
    parser.add_argument("--case", action="append", help="case id; repeatable; default all")
    parser.add_argument("--arm", action="append", choices=ARMS, help="repeatable; default harness")
    parser.add_argument("--trials", type=int, default=1)
    parser.add_argument("--model", help="model passed to the runtime; default is the runtime's own default")
    parser.add_argument("--max-budget-usd", type=float, help="per-trial spending cap passed to the runtime")
    parser.add_argument("--timeout", type=int, default=2400, help="per-trial timeout in seconds")
    parser.add_argument("--out", type=Path, help="results directory; default evals/results/<timestamp>-<runtime>-build")
    parser.add_argument("--keep-sandboxes", action="store_true")
    parser.add_argument("--solution", choices=SOLUTIONS, help="score the case's own solution instead of calling a runtime")
    parser.add_argument("--dry-run", action="store_true", help="build sandboxes and print prompts without calling the runtime")
    args = parser.parse_args()
    if not args.runtime and not args.solution:
        parser.error("give --runtime, or --solution to score the cases' own solutions")

    available = sorted(p.name for p in CASES.iterdir() if (p / "case.yaml").exists())
    selected = args.case or available
    unknown = sorted(set(selected) - set(available))
    if unknown:
        parser.error(f"unknown case(s): {', '.join(unknown)}. Available: {', '.join(available)}")
    arms = ["bare"] if args.solution else (args.arm or ["harness"])

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    live = not args.dry_run and not args.solution
    out = (args.out or ROOT / "evals/results" / f"{stamp}-{args.runtime}-build") if live else None
    parent = Path(tempfile.mkdtemp(prefix="gantry-build-"))
    args.dependencies = run.install_dependencies()
    if out:
        out.mkdir(parents=True, exist_ok=True)
    records = []
    for name in selected:
        case = yaml.safe_load((CASES / name / "case.yaml").read_text(encoding="utf-8"))
        for arm in arms:
            for trial in range(1, args.trials + 1):
                print(f"[{name} {args.solution or arm} {trial}/{args.trials}] {'building sandbox' if args.dry_run else 'running'}...", flush=True)
                records.append(run_trial(CASES / name, case, arm, args, parent, out, trial))
    if args.dry_run:
        for r in records:
            print(f"\n--- {r['case']} {r['arm']} ({r['sandbox']})\n{r['prompt']}")
        print(f"Sandboxes kept under {parent}")
        return 0
    if not args.keep_sandboxes:
        shutil.rmtree(parent, ignore_errors=True)
    print_report(records)
    if out:
        commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        (out / "results.json").write_text(json.dumps(
            {"runtime": args.runtime, "model": args.model, "harness_commit": commit, "started": stamp, "records": records}, indent=2), encoding="utf-8")
        print(f"results: {out.relative_to(ROOT)}")
    if args.solution:  # the cases check themselves: a reference passes everything, a naive solution passes what is said and no more
        full = all(r["hidden"][kind][0] == r["expected"][kind] for r in records for kind in ("plain", "edge")) and all(all(r["checks"].values()) for r in records)
        naive = all(r["hidden"]["plain"][0] == r["expected"]["plain"] and r["hidden"]["edge"][0] < r["expected"]["edge"] for r in records)
        ok = full if args.solution == "reference" else naive
        print(f"BUILD CASES ({args.solution}): {'PASS' if ok else 'FAIL'}")
        return 0 if ok else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
