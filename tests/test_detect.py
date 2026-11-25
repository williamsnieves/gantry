"""Project detection: new or existing, stack, and the commands that check it."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import yaml  # noqa: E402

from gantry import detect  # noqa: E402


def project(files: dict[str, str]) -> Path:
    root = Path(tempfile.mkdtemp(prefix="gantry-detect-"))
    for name, text in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return root


# An empty directory, or one with only a manifest, is a new project.
empty = detect.detect(project({"README.md": "# x\n"}))
assert empty["kind"] == "greenfield" and empty["checks"] == {} and empty["notes"] == [], empty

# A Node workspace: manager from the lockfile, commands from scripts, frameworks from every package.
node = detect.detect(project({
    "package.json": json.dumps({"workspaces": ["apps/*"], "scripts": {"test": "vitest run", "lint": "eslint .", "typecheck": "tsc --noEmit"},
                                "devDependencies": {"vitest": "1", "typescript": "5", "eslint": "9"}}),
    "pnpm-lock.yaml": "",
    "apps/web/package.json": json.dumps({"dependencies": {"react": "18"}}),
    "apps/api/package.json": json.dumps({"dependencies": {"express": "4", "@prisma/client": "5"}}),
    **{f"apps/api/src/m{i}.ts": "export {};\n" for i in range(4)},
    "apps/api/src/m0.test.ts": "",
    "apps/web/src/App.tsx": "",
    "node_modules/x/index.js": "",
    ".harness/bin/route.py": "",
    ".github/workflows/ci.yml": "",
}))
assert node["kind"] == "brownfield" and node["source_files"] == 6 and node["test_files"] == 1, node
assert node["languages"] == ["typescript"] and node["package_managers"] == ["pnpm"] and node["workspaces"], node
assert {"react", "express", "prisma", "vitest", "typescript", "eslint"} <= set(node["frameworks"]), node
assert node["checks"]["test"]["command"] == "pnpm test", node
assert node["checks"]["lint"]["command"] == "pnpm run lint" and node["checks"]["typecheck"]["command"] == "pnpm run typecheck", node
assert "build" not in node["checks"] and node["ci"] == ["github-actions"] and node["notes"] == [], node

# The npm placeholder script is not a test command, and an existing project without checks says so.
bare = detect.detect(project({
    "package.json": json.dumps({"scripts": {"test": 'echo "Error: no test specified" && exit 1'}}),
    **{f"src/m{i}.js": "" for i in range(5)},
}))
assert bare["checks"] == {} and bare["package_managers"] == ["npm"], bare
assert any("no command detected for: test, lint, typecheck" in note for note in bare["notes"]), bare
assert "no test files found" in bare["notes"], bare

# Python with uv, and Go.
py = detect.detect(project({
    "pyproject.toml": '[project]\ndependencies = ["fastapi>=0.110"]\n[dependency-groups]\ndev = ["pytest", "ruff", "mypy"]\n',
    "uv.lock": "",
    **{f"app/m{i}.py": "" for i in range(4)},
    "tests/test_app.py": "",
}))
assert py["languages"] == ["python"] and py["package_managers"] == ["uv"] and "fastapi" in py["frameworks"], py
assert [py["checks"][c]["command"] for c in ("test", "lint", "typecheck")] == ["uv run pytest", "uv run ruff check .", "uv run mypy ."], py
go = detect.detect(project({"go.mod": "module x\n", **{f"m{i}.go": "" for i in range(4)}, "m0_test.go": ""}))
assert go["checks"]["test"]["command"] == "go test ./..." and go["test_files"] == 1, go

# A Makefile target is used when nothing more specific was found; a broken manifest is reported, not fatal.
make = detect.detect(project({"Makefile": "test:\n\tgo test\nlint:\n\ttrue\n", "package.json": "{not json"}))
assert make["checks"]["test"] == {"command": "make test", "source": "Makefile target `test`"}, make
assert any("not valid JSON" in note for note in make["notes"]), make

# The saved file is YAML with the same content, whatever characters a command contains.
node["checks"]["test"]["command"] = 'pnpm test -- --reporter="dot": #1'
assert {k: v for k, v in yaml.safe_load(detect.render(node)).items()} == node

# `gantry inspect` prints it, and refuses to write where the harness is not installed.
target = project({"package.json": json.dumps({"scripts": {"test": "vitest"}}), **{f"src/m{i}.ts": "" for i in range(4)}})
run = lambda *args: subprocess.run([sys.executable, "-m", "gantry", *args], cwd=ROOT, capture_output=True, text=True)
shown = run("inspect", "--project", str(target))
assert shown.returncode == 0 and "Project: brownfield" in shown.stdout and "npm test" in shown.stdout, shown.stdout + shown.stderr
assert json.loads(run("inspect", "--project", str(target), "--json").stdout)["kind"] == "brownfield"
assert run("inspect", "--project", str(target), "--write").returncode != 0

print("DETECT TESTS: PASS")
