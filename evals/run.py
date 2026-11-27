"""Run the routing scenarios against a real agent runtime and score the result.

    python3 evals/run.py --runtime claude
    python3 evals/run.py --runtime claude --scenario small-frontend --trials 3
    python3 evals/run.py --runtime claude --dry-run          # build sandboxes, call nothing
    python3 evals/run.py --rescore evals/results/<run>       # re-score saved plans, call nothing

Each trial builds a throwaway copy of evals/fixture, installs the harness into
it, applies the case's change as uncommitted work, asks the runtime to produce
the routing plan (and nothing else), then scores that plan against the oracle
in distribution/core/.harness/evals/end-to-end/scenarios/.

Every live trial calls the agent runtime and costs tokens.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import scoring  # noqa: E402

FIXTURE = ROOT / "evals/fixture"
CASES = ROOT / "evals/cases"
SCENARIOS = ROOT / "distribution/core/.harness/evals/end-to-end/scenarios"

PROMPT = """{request}
{change_note}
Use the harness-run skill for this change, but stop once the routing plan is written. Do not launch any specialist agent, do not run Validator, and do not modify any project file other than the routing plan.
"""
CHANGE_NOTE = "The change is already in this repository's working tree as uncommitted work; inspect it with git.\n"
NO_CHANGE_NOTE = "There are no code changes in the working tree for this request.\n"


def run_claude(prompt: str, sandbox: Path, args: argparse.Namespace, extra_tools: tuple[str, ...] = (),
               trace: Path | None = None) -> dict:
    """Run Claude Code headless in the sandbox and return normalised metrics.

    With `trace`, every event of the run is written there as JSON lines.
    """
    command = [
        "claude", "-p", prompt,
        *(("--output-format", "stream-json", "--verbose") if trace else ("--output-format", "json")),
        "--permission-mode", "acceptEdits",
        "--allowedTools", "Read", "Grep", "Glob", "Write", "Edit", "Skill",
        "Bash(git status:*)", "Bash(git diff:*)", "Bash(git log:*)", "Bash(git show:*)", "Bash(ls:*)",
        "Bash(python3 .harness/bin/route.py:*)",
        *extra_tools,
        # Only the sandbox's own configuration: no user settings, memory, or MCP servers.
        "--setting-sources", "project",
        "--strict-mcp-config",
        "--no-session-persistence",
    ]
    if args.model:
        command += ["--model", args.model]
    if args.max_budget_usd:
        command += ["--max-budget-usd", str(args.max_budget_usd)]
    started = time.monotonic()
    try:
        proc = subprocess.run(command, cwd=sandbox, capture_output=True, text=True, timeout=args.timeout)
    except subprocess.TimeoutExpired:
        return {"error": f"timed out after {args.timeout}s", "wall_seconds": round(time.monotonic() - started, 1)}
    wall = round(time.monotonic() - started, 1)
    try:
        if trace:
            trace.write_text(proc.stdout, encoding="utf-8")
            events = [json.loads(line) for line in proc.stdout.splitlines() if line.strip()]
            payload = next(event for event in reversed(events) if event.get("type") == "result")
        else:
            payload = json.loads(proc.stdout)
    except (json.JSONDecodeError, StopIteration):
        return {"error": f"exit {proc.returncode}: {(proc.stderr or proc.stdout).strip()[:500]}", "wall_seconds": wall}
    usage = payload.get("usage") or {}
    metrics = {
        "wall_seconds": wall,
        "turns": payload.get("num_turns"),
        "cost_usd": payload.get("total_cost_usd"),
        "input_tokens": usage.get("input_tokens"),
        "output_tokens": usage.get("output_tokens"),
        "cache_read_tokens": usage.get("cache_read_input_tokens"),
        "cache_write_tokens": usage.get("cache_creation_input_tokens"),
        "models": sorted((payload.get("modelUsage") or {}).keys()),
        "final_message": str(payload.get("result") or "")[:2000],
    }
    if payload.get("is_error"):
        metrics["error"] = f"runtime reported {payload.get('subtype') or 'an error'}"
    return metrics


DRIVERS = {"claude": run_claude}


def git(sandbox: Path, *arguments: str) -> None:
    subprocess.run(
        ["git", "-c", "user.name=gantry-eval", "-c", "user.email=gantry-eval@example.invalid", *arguments],
        cwd=sandbox, check=True, capture_output=True,
    )


def install_dependencies() -> Path:
    """Install the fixture's dependencies once per lockfile and return the node_modules to share.

    Sandboxes link to it, so a review can run the project's tests, type check and lint.
    """
    lock = FIXTURE / "package-lock.json"
    key = hashlib.sha256(lock.read_bytes() + (FIXTURE / "apps/api/prisma/schema.prisma").read_bytes()).hexdigest()[:12]
    cache = ROOT / "evals/.cache" / f"fixture-{key}"
    modules = cache / "node_modules"
    if (cache / ".installed").exists():
        return modules
    shutil.rmtree(cache, ignore_errors=True)
    shutil.copytree(FIXTURE, cache, ignore=shutil.ignore_patterns("node_modules"))
    print(f"installing the fixture's dependencies into {cache.relative_to(ROOT)} (once per lockfile)...", flush=True)
    for command in (["npm", "ci", "--no-audit", "--no-fund"], ["npm", "test"], ["npm", "run", "typecheck"], ["npm", "run", "lint"]):
        proc = subprocess.run(command, cwd=cache, capture_output=True, text=True)
        if proc.returncode != 0:
            raise SystemExit(f"`{' '.join(command)}` failed in the unchanged fixture:\n{(proc.stdout + proc.stderr)[-2000:]}")
    (cache / ".installed").write_text("ok\n", encoding="utf-8")
    return modules


def build_sandbox(case_dir: Path, runtime: str, parent: Path, dependencies: Path | None = None,
                  models: dict[str, str] | None = None, prepare=None) -> Path:
    """Fixture + installed harness committed as the base, case files as uncommitted work.

    With `dependencies`, the sandbox links to that node_modules so the project's checks can be executed.
    """
    sandbox = Path(tempfile.mkdtemp(prefix=f"{case_dir.name}-", dir=parent))
    shutil.copytree(FIXTURE, sandbox, dirs_exist_ok=True, ignore=shutil.ignore_patterns("node_modules"))
    if dependencies:
        (sandbox / "node_modules").symlink_to(dependencies, target_is_directory=True)
    env = {**os.environ, "PYTHONPATH": str(ROOT)}
    subprocess.run(
        [sys.executable, "-m", "gantry", "install", "--runtime", runtime, "--scope", "fullstack", "--project", str(sandbox)],
        check=True, capture_output=True, env=env,
    )
    if models:  # the project's own choice of model per tier, part of the base and not of the change
        lines = "".join(f'  {name}: "{model}"\n' for name, model in models.items())
        (sandbox / ".harness/models.yaml").write_text(f"{runtime}:\n{lines}", encoding="utf-8")
    if prepare:  # a variant of the installed harness, part of the base and not of the change
        prepare(sandbox)
    git(sandbox, "init", "-q", "-b", "main")
    git(sandbox, "add", "-A")
    git(sandbox, "commit", "-q", "-m", "Base application with harness installed")
    overlay = case_dir / "files"
    if overlay.is_dir():
        shutil.copytree(overlay, sandbox, dirs_exist_ok=True)
    return sandbox


def find_plan(sandbox: Path, runtime: str) -> tuple[Path | None, list[str]]:
    """Locate the routing plan; note when it is not where the contract says."""
    expected = sandbox / ".harness/runtime" / runtime / "routing-plan.yaml"
    if expected.exists():
        return expected, []
    candidates = sorted(
        p for p in (sandbox / ".harness/runtime").rglob("*")
        if p.is_file() and p.suffix in (".yaml", ".yml") and "routing" in p.name.lower()
    ) if (sandbox / ".harness/runtime").exists() else []
    if candidates:
        return candidates[0], [f"plan written to {candidates[0].relative_to(sandbox)} instead of {expected.relative_to(sandbox)}"]
    return None, []


def side_effects(sandbox: Path, overlay: Path) -> list[str]:
    """Files changed beyond the case's own change and the harness runtime state."""
    status = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"], cwd=sandbox, capture_output=True, text=True,
    ).stdout
    expected = {p.relative_to(overlay).as_posix() for p in overlay.rglob("*") if p.is_file()} if overlay.is_dir() else set()
    extra = []
    for line in status.splitlines():
        path = line[3:].strip().strip('"')
        if path not in expected and not path.startswith(".harness/runtime/"):
            extra.append(path)
    return sorted(extra)


def score_file(plan_file: Path, oracle: dict) -> dict:
    unscorable = {"scorable": False, "schema_valid": False, "passed": False}
    if not plan_file.exists():
        return {**unscorable, "failure": "no routing plan was written"}
    try:
        plan = yaml.safe_load(plan_file.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return {**unscorable, "failure": f"routing plan is not valid YAML ({str(exc).splitlines()[0]})"}
    return scoring.score_plan(plan, oracle)


def run_trial(case_dir: Path, case: dict, oracle: dict, args: argparse.Namespace, parent: Path, out: Path, trial: int) -> dict:
    sandbox = build_sandbox(case_dir, args.runtime, parent)
    has_change = (case_dir / "files").is_dir()
    prompt = PROMPT.format(request=case["request"].strip() + "\n", change_note=CHANGE_NOTE if has_change else NO_CHANGE_NOTE)
    record: dict = {"scenario": oracle["id"], "trial": trial, "runtime": args.runtime}
    if args.dry_run:
        record.update(dry_run=True, sandbox=str(sandbox), prompt=prompt)
        return record
    record["metrics"] = DRIVERS[args.runtime](prompt, sandbox, args)
    plan_path, notes = find_plan(sandbox, args.runtime)
    record["notes"] = notes
    record["side_effects"] = side_effects(sandbox, case_dir / "files")
    saved = out / f"{oracle['id']}-{trial}-routing-plan.yaml"
    if plan_path is not None:
        shutil.copyfile(plan_path, saved)
    record["score"] = score_file(saved, oracle)
    if not args.keep_sandboxes:
        shutil.rmtree(sandbox, ignore_errors=True)
    else:
        record["sandbox"] = str(sandbox)
    return record


def summarise(records: list[dict]) -> dict:
    by_scenario: dict[str, list[dict]] = {}
    for record in records:
        by_scenario.setdefault(record["scenario"], []).append(record)
    scenarios = {}
    for scenario, items in by_scenario.items():
        scores = [item["score"] for item in items]
        scenarios[scenario] = {
            "passed": sum(bool(s.get("passed")) for s in scores),
            "schema_valid": sum(bool(s.get("schema_valid")) for s in scores),
            "plan_written": sum(s.get("failure") != "no routing plan was written" for s in scores),
            "side_effect_trials": sum(bool(item.get("side_effects")) for item in items),
            **scoring.consistency(scores),
        }
    def total(key: str) -> float | None:
        values = [r["metrics"].get(key) for r in records if r["metrics"].get(key) is not None]
        return round(sum(values), 4) if values else None
    trials = len(records)
    return {
        "trials": trials,
        "passed": sum(s["passed"] for s in scenarios.values()),
        "schema_valid": sum(s["schema_valid"] for s in scenarios.values()),
        "missed_required_trials": sum(bool(r["score"].get("missed_required")) for r in records),
        "unnecessary_gate_trials": sum(bool(r["score"].get("unnecessary")) for r in records),
        "runtime_errors": sum("error" in r["metrics"] for r in records),
        "cost_usd": total("cost_usd"),
        "wall_seconds": total("wall_seconds"),
        "output_tokens": total("output_tokens"),
        "scenarios": scenarios,
    }


def print_report(records: list[dict], summary: dict) -> None:
    print()
    print(f"{'scenario':26} {'trial':>5}  {'result':6} {'schema':6} {'turns':>5} {'cost $':>7} {'secs':>6}  detail")
    for r in records:
        s, m = r["score"], r["metrics"]
        detail = m.get("error") or s.get("failure") or ""
        if not detail and not s.get("schema_valid"):
            detail = f"{len(s.get('schema_problems') or [])} schema problem(s)"
        cost = f"{m['cost_usd']:.3f}" if m.get("cost_usd") is not None else "-"
        print(f"{r['scenario']:26} {r['trial']:>5}  {'PASS' if s.get('passed') else 'FAIL':6} "
              f"{'ok' if s.get('schema_valid') else 'bad':6} {str(m.get('turns') or '-'):>5} {cost:>7} "
              f"{str(m.get('wall_seconds') or '-'):>6}  {detail}")
    print()
    print(f"passed {summary['passed']}/{summary['trials']} trials, schema-valid {summary['schema_valid']}/{summary['trials']}, "
          f"missed a required gate in {summary['missed_required_trials']}, unnecessary gate in {summary['unnecessary_gate_trials']}")
    if any(s["trials"] > 1 for s in summary["scenarios"].values()):
        for name, s in summary["scenarios"].items():
            print(f"  {name}: {s['distinct_decisions']} distinct decision(s) over {s['trials']} trials (agreement {s['agreement']})")
    if summary["cost_usd"] is not None:
        print(f"cost ${summary['cost_usd']:.2f}, wall time {summary['wall_seconds']:.0f}s")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run routing scenarios against an agent runtime.")
    parser.add_argument("--runtime", choices=sorted(DRIVERS))
    parser.add_argument("--rescore", type=Path, metavar="RESULTS_DIR",
                        help="re-score the plans saved by an earlier run instead of calling a runtime")
    parser.add_argument("--scenario", action="append", help="scenario id; repeatable; default all")
    parser.add_argument("--trials", type=int, default=1, help="runs per scenario; more than 1 measures consistency")
    parser.add_argument("--model", help="model passed to the runtime; default is the runtime's own default")
    parser.add_argument("--max-budget-usd", type=float, help="per-trial spending cap passed to the runtime")
    parser.add_argument("--timeout", type=int, default=900, help="per-trial timeout in seconds")
    parser.add_argument("--out", type=Path, help="results directory; default evals/results/<timestamp>-<runtime>")
    parser.add_argument("--keep-sandboxes", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="build sandboxes and print prompts without calling the runtime")
    args = parser.parse_args()

    available = sorted(p.name for p in CASES.iterdir() if (p / "case.yaml").exists())
    selected = args.scenario or available
    unknown = sorted(set(selected) - set(available))
    if unknown:
        parser.error(f"unknown scenario(s): {', '.join(unknown)}. Available: {', '.join(available)}")
    oracle_files = {yaml.safe_load(p.read_text(encoding="utf-8"))["id"]: p for p in SCENARIOS.glob("*.yaml")}

    if args.rescore:
        results_file = args.rescore / "results.json"
        data = json.loads(results_file.read_text(encoding="utf-8"))
        for record in data["records"]:
            oracle = scoring.load_oracle(oracle_files[record["scenario"]])
            record["score"] = score_file(args.rescore / f"{record['scenario']}-{record['trial']}-routing-plan.yaml", oracle)
        data["summary"] = summarise(data["records"])
        results_file.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        print_report(data["records"], data["summary"])
        return 0 if data["summary"]["passed"] == data["summary"]["trials"] else 1
    if not args.runtime:
        parser.error("--runtime is required unless --rescore is given")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = args.out or ROOT / "evals/results" / f"{stamp}-{args.runtime}"
    out.mkdir(parents=True, exist_ok=True)
    parent = Path(tempfile.mkdtemp(prefix="gantry-eval-"))
    records = []
    for name in selected:
        case = yaml.safe_load((CASES / name / "case.yaml").read_text(encoding="utf-8"))
        oracle = scoring.load_oracle(oracle_files[case["scenario"]])
        for trial in range(1, args.trials + 1):
            print(f"[{name} trial {trial}/{args.trials}] {'building sandbox' if args.dry_run else 'running'}...", flush=True)
            records.append(run_trial(CASES / name, case, oracle, args, parent, out, trial))
    if args.dry_run:
        for r in records:
            print(f"\n--- {r['scenario']} ({r['sandbox']})\n{r['prompt']}")
        print(f"Sandboxes kept under {parent}")
        return 0
    if not args.keep_sandboxes:
        shutil.rmtree(parent, ignore_errors=True)
    summary = summarise(records)
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    (out / "results.json").write_text(json.dumps(
        {"runtime": args.runtime, "model": args.model, "harness_commit": commit, "started": stamp,
         "summary": summary, "records": records}, indent=2) + "\n", encoding="utf-8")
    print_report(records, summary)
    print(f"results: {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}")
    return 0 if summary["passed"] == summary["trials"] else 1


if __name__ == "__main__":
    sys.exit(main())
