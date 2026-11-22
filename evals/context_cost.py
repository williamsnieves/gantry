"""Measure what the harness adds to every session before any work starts.

    python3 evals/context_cost.py --runtime claude

Sends the same trivial prompt to the runtime in two throwaway copies of
evals/fixture: one bare, one with the harness installed. The difference in
input tokens is the always-on cost: skill descriptions, rules files and the
AGENTS.md block that load whether or not the session uses the harness.

Costs a few cents per run.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "evals/fixture"
PROMPT = "Reply with the single word OK. Do not use any tool."


def claude_input_tokens(sandbox: Path, model: str | None) -> dict:
    command = ["claude", "-p", PROMPT, "--output-format", "json", "--setting-sources", "project",
               "--strict-mcp-config", "--no-session-persistence"]
    if model:
        command += ["--model", model]
    proc = subprocess.run(command, cwd=sandbox, capture_output=True, text=True, timeout=300)
    payload = json.loads(proc.stdout)
    usage = payload.get("usage") or {}
    total = sum(usage.get(key) or 0 for key in ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))
    return {"input_tokens": total, "turns": payload.get("num_turns"), "cost_usd": payload.get("total_cost_usd")}


DRIVERS = {"claude": claude_input_tokens}


def main() -> int:
    parser = argparse.ArgumentParser(description="Measure the harness's always-on context cost.")
    parser.add_argument("--runtime", choices=sorted(DRIVERS), required=True)
    parser.add_argument("--model")
    args = parser.parse_args()

    parent = Path(tempfile.mkdtemp(prefix="gantry-context-"))
    results = {}
    try:
        for variant in ("bare", "installed"):
            sandbox = parent / variant
            shutil.copytree(FIXTURE, sandbox)
            if variant == "installed":
                subprocess.run(
                    [sys.executable, "-m", "gantry", "install", "--runtime", args.runtime, "--project", str(sandbox)],
                    check=True, capture_output=True, env={**os.environ, "PYTHONPATH": str(ROOT)},
                )
            subprocess.run(["git", "init", "-q"], cwd=sandbox, check=True, capture_output=True)
            results[variant] = DRIVERS[args.runtime](sandbox, args.model)
    finally:
        shutil.rmtree(parent, ignore_errors=True)

    overhead = results["installed"]["input_tokens"] - results["bare"]["input_tokens"]
    for variant, result in results.items():
        print(f"{variant:10} {result['input_tokens']:>8} input tokens  ({result['turns']} turn)")
    print(f"{'overhead':10} {overhead:>8} input tokens added to every session by the harness")
    return 0


if __name__ == "__main__":
    sys.exit(main())
