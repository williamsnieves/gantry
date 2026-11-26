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
assert node["tests"] == "beside the code" and node["docs"] == [], node
assert node["layout"] == [{"path": "apps/api", "source_files": 5}, {"path": "apps/web", "source_files": 1}], node
assert "build" not in node["checks"] and node["ci"] == ["github-actions"] and node["notes"] == [], node

# PHP, Ruby and .NET: the manager, the frameworks and the commands their own manifests declare.
checks = lambda found: {name: check["command"] for name, check in found["checks"].items()}
laravel = detect.detect(project({
    "composer.json": json.dumps({"require": {"laravel/framework": "^11"}, "require-dev": {"pestphp/pest": "^3", "larastan/larastan": "^3", "laravel/pint": "^1"}}),
    "artisan": "", **{f"app/Models/M{i}.php": "<?php\n" for i in range(5)},
}))
assert laravel["package_managers"] == ["composer"] and {"laravel", "pest", "phpstan", "pint"} <= set(laravel["frameworks"]), laravel
assert checks(laravel) == {"test": "php artisan test", "typecheck": "vendor/bin/phpstan analyse", "format": "vendor/bin/pint --test"}, laravel
assert laravel["languages"] == ["php"] and any("no command detected for: lint" in note for note in laravel["notes"]), laravel
scripted = detect.detect(project({"composer.json": json.dumps({"require-dev": {"phpunit/phpunit": "^11"}, "scripts": {"test": "phpunit", "lint": "phpcs"}})}))
assert checks(scripted) == {"test": "composer run-script test", "lint": "composer run-script lint"}, scripted
rails = detect.detect(project({"Gemfile": "source 'https://rubygems.org'\ngem 'rails'\ngem \"rspec-rails\", group: :test\ngem 'rubocop'\n"}))
assert rails["package_managers"] == ["bundler"] and checks(rails) == {"test": "bundle exec rspec", "lint": "bundle exec rubocop"}, rails
net = detect.detect(project({"Shop.sln": "", "src/Shop/Order.cs": ""}))
assert checks(net) == {"test": "dotnet test", "build": "dotnet build", "format": "dotnet format --verify-no-changes"}, net
# Terraform is noted, not run: its commands need the tool on every machine.
infra = detect.detect(project({"infra/main.tf": "", "infra/modules/db/main.tf": "", "package.json": json.dumps({"scripts": {"test": "vitest run"}})}))
assert "terraform" in infra["frameworks"] and checks(infra) == {"test": "npm test"}, infra
assert any(note.startswith("Terraform files in infra and 1 more") for note in infra["notes"]), infra["notes"]

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
assert py["tests"] == "in test directories" and py["layout"][0] == {"path": "app", "source_files": 4}, py
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
assert "next: run the harness-onboard skill to record this project's conventions" in shown.stdout, shown.stdout
(target / "docs").mkdir()
(target / "docs/conventions.md").write_text("# Project conventions\n")
assert "harness-onboard" not in run("inspect", "--project", str(target)).stdout
assert "settle the stack" in "\n".join(detect.summary(empty))
assert json.loads(run("inspect", "--project", str(target), "--json").stdout)["kind"] == "brownfield"
assert run("inspect", "--project", str(target), "--write").returncode != 0

# The conventions file: headings, length and cited paths are checked; judgement is not.
checker = ROOT / "distribution/core/.harness/bin/conventions.py"
check = lambda: subprocess.run([sys.executable, str(checker), "check", "--project", str(target)], capture_output=True, text=True)
assert check().returncode == 1 and "missing section: ## Structure" in check().stdout
good = """# Project conventions

## Structure
Features live under `src/` (`src/m0.ts`). Run one with `npm test`.

## Patterns
Modules export plain functions (`src/m1.ts:3-9`, `src/m2.ts`).

## Tests
None yet; see `package.json`.

## Do not
Nothing recorded.

## Open questions
Where tests will live.
"""
(target / "docs/conventions.md").write_text(good)
assert check().returncode == 0, check().stdout
(target / "docs/conventions.md").write_text(good.replace("`src/m2.ts`", "`src/missing/handler.ts`") + "word " * 600)
out = check().stdout
assert "cites `src/missing/handler.ts`, which does not exist" in out and "keep it under 600" in out, out
(target / "docs/conventions.md").unlink()
assert "does not exist; run the harness-onboard skill" in check().stdout

print("DETECT TESTS: PASS")
