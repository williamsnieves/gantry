"""Run a change through every routed gate on a real agent runtime and score the reviews.

    python3 evals/review.py --runtime claude
    python3 evals/review.py --runtime claude --case severity-filter-tenant-leak --trials 3
    python3 evals/review.py --runtime claude --dry-run       # build sandboxes, call nothing

Each case in evals/review-cases/ is a change to evals/fixture, either correct
(a control) or carrying one planted defect. A trial asks the runtime to take the
change through harness-run up to the Final Pre-PR Gate without fixing anything,
then reads the gate ledger and the specialists' reports.

A trial launches one agent per routed gate, so it costs several times a routing
trial in evals/run.py.
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
sys.path.insert(0, str(ROOT / "distribution/core/.harness/bin"))
import route  # noqa: E402
import run  # noqa: E402
import scoring  # noqa: E402
import tracing  # noqa: E402

CASES = ROOT / "evals/review-cases"
# Specialists are launched as subagents; the name of that tool differs between Claude Code versions.
SUBAGENT_TOOLS = ("Agent", "Task")

PROMPT = """{request}
The change is already in this repository's working tree as uncommitted work; inspect it with git.

Use the harness-run skill to take this change through its review, up to and including the Final Pre-PR Gate.

This is a review-only run:
- Do not modify any project file and do not fix anything. If a gate requires changes, record that result and follow the `next:` line the router prints.
- Dependencies are not installed here, so tests, lint and type checks cannot be executed. The project owner accepts that for this run: a check that could not be executed is recorded as a condition, not as a failed or blocked gate, and the change is judged by reading it. Tell every specialist this when you launch it.
- Finish by running `python3 .harness/bin/route.py ready --runtime {runtime}` and report what it prints. Do not create a pull request.
"""


def collect(sandbox: Path, runtime: str) -> tuple[list[str], dict, dict[str, str], str, list[str]]:
    """Read the routing plan, gate ledger and reports the run left behind."""
    status, blockers, _ = route.readiness(sandbox, runtime)
    required: list[str] = []
    plan_path = route.state_dir(sandbox, runtime) / "routing-plan.yaml"
    identity = route.change_identity(sandbox)[0]["value"]
    try:
        plan = route.parse(plan_path.read_text(encoding="utf-8"))
        required = [entry["agent"] for entry in plan["agents"] if entry["applicability"] == "REQUIRED"]
    except (OSError, route.RouteError, KeyError, TypeError):
        pass
    gates, reports = {}, {}
    try:
        ledger = route.load_gates(sandbox, runtime)
    except route.RouteError:
        ledger = {}
    for agent, entry in ledger.items():
        gates[agent] = {
            "decision": entry.get("decision"),
            "current": entry.get("change_identity") == identity,
            "conditions": entry.get("conditions") or [],
            "report": entry.get("report"),
        }
        report = sandbox / str(entry.get("report") or "")
        if report.is_file():
            reports[agent] = report.read_text(encoding="utf-8", errors="replace")
    return required, gates, reports, status, blockers


def run_trial(case_dir: Path, case: dict, args: argparse.Namespace, parent: Path, out: Path, trial: int) -> dict:
    sandbox = run.build_sandbox(case_dir, args.runtime, parent)
    prompt = PROMPT.format(request=case["request"].strip() + "\n", runtime=args.runtime)
    record: dict = {"case": case_dir.name, "trial": trial, "runtime": args.runtime, "has_defect": bool(case.get("defect"))}
    if args.dry_run:
        record.update(dry_run=True, sandbox=str(sandbox), prompt=prompt)
        return record
    trace_file = out / f"{case_dir.name}-{trial}-trace.jsonl"
    record["metrics"] = run.DRIVERS[args.runtime](prompt, sandbox, args, SUBAGENT_TOOLS, trace_file)
    if trace_file.exists():
        events = [json.loads(line) for line in trace_file.read_text(encoding="utf-8").splitlines() if line.strip()]
        record["trace"] = tracing.summarise(events, sandbox)
    required, gates, reports, status, blockers = collect(sandbox, args.runtime)
    record.update(gates=gates, blockers=blockers, side_effects=run.side_effects(sandbox, case_dir / "files"))
    for agent, text in reports.items():
        (out / f"{case_dir.name}-{trial}-{agent}-report.md").write_text(text, encoding="utf-8")
    record["score"] = scoring.score_review(case.get("defect"), required, gates, reports, status)
    if args.keep_sandboxes:
        record["sandbox"] = str(sandbox)
    else:
        shutil.rmtree(sandbox, ignore_errors=True)
    return record


def print_report(records: list[dict]) -> None:
    print()
    print(f"{'case':30} {'trial':>5}  {'result':6} {'gates':>7} {'final gate':28} {'cost $':>7} {'secs':>6}  detail")
    for r in records:
        s, m = r["score"], r["metrics"]
        detail = m.get("error") or s.get("failure") or ("found by " + ", ".join(s["found_by"]) if s.get("found_by") else "")
        cost = f"{m['cost_usd']:.2f}" if m.get("cost_usd") is not None else "-"
        print(f"{r['case']:30} {r['trial']:>5}  {'PASS' if s['passed'] else 'FAIL':6} "
              f"{s['recorded']}/{s['required']:<5} {s['status']:28} {cost:>7} {str(m.get('wall_seconds') or '-'):>6}  {detail}")
        if r.get("side_effects"):
            print(f"{'':30} project files changed during a review-only run: {', '.join(r['side_effects'])}")
    for r in records:
        if r.get("trace"):
            print(f"\n{r['case']} trial {r['trial']}: what each agent read")
            tracing.print_summary(r["trace"])
    defects = [r for r in records if r["has_defect"]]
    controls = [r for r in records if not r["has_defect"]]
    print()
    if defects:
        print(f"defects found: {sum(r['score']['passed'] for r in defects)}/{len(defects)} trials")
    if controls:
        print(f"controls without a false alarm: {sum(r['score']['passed'] for r in controls)}/{len(controls)} trials")
    costs = [r["metrics"]["cost_usd"] for r in records if r["metrics"].get("cost_usd") is not None]
    if costs:
        print(f"cost ${sum(costs):.2f}, wall time {sum(r['metrics'].get('wall_seconds') or 0 for r in records):.0f}s")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run changes through every routed gate and score the reviews.")
    parser.add_argument("--runtime", choices=sorted(run.DRIVERS), required=True)
    parser.add_argument("--case", action="append", help="case id; repeatable; default all")
    parser.add_argument("--trials", type=int, default=1)
    parser.add_argument("--model", help="model passed to the runtime; default is the runtime's own default")
    parser.add_argument("--max-budget-usd", type=float, help="per-trial spending cap passed to the runtime")
    parser.add_argument("--timeout", type=int, default=2400, help="per-trial timeout in seconds")
    parser.add_argument("--out", type=Path, help="results directory; default evals/results/<timestamp>-<runtime>-review")
    parser.add_argument("--keep-sandboxes", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="build sandboxes and print prompts without calling the runtime")
    args = parser.parse_args()

    available = sorted(p.name for p in CASES.iterdir() if (p / "case.yaml").exists())
    selected = args.case or available
    unknown = sorted(set(selected) - set(available))
    if unknown:
        parser.error(f"unknown case(s): {', '.join(unknown)}. Available: {', '.join(available)}")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = args.out or ROOT / "evals/results" / f"{stamp}-{args.runtime}-review"
    parent = Path(tempfile.mkdtemp(prefix="gantry-review-"))
    if not args.dry_run:
        out.mkdir(parents=True, exist_ok=True)
    records = []
    for name in selected:
        case = yaml.safe_load((CASES / name / "case.yaml").read_text(encoding="utf-8"))
        for trial in range(1, args.trials + 1):
            print(f"[{name} trial {trial}/{args.trials}] {'building sandbox' if args.dry_run else 'running'}...", flush=True)
            records.append(run_trial(CASES / name, case, args, parent, out, trial))
    if args.dry_run:
        for r in records:
            print(f"\n--- {r['case']} ({r['sandbox']})\n{r['prompt']}")
        print(f"Sandboxes kept under {parent}")
        return 0
    if not args.keep_sandboxes:
        shutil.rmtree(parent, ignore_errors=True)
    commit = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    (out / "results.json").write_text(json.dumps(
        {"runtime": args.runtime, "model": args.model, "harness_commit": commit, "started": stamp, "records": records},
        indent=2) + "\n", encoding="utf-8")
    print_report(records)
    print(f"results: {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}")
    return 0 if all(r["score"]["passed"] for r in records) else 1


if __name__ == "__main__":
    sys.exit(main())
