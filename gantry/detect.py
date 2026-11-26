"""Describe a project from its files: new or existing, its stack, and the commands that check it.

Nothing here runs project code or calls a model. The result is written to
`.harness/project.yaml` so that every agent starts from the same facts instead
of rediscovering them, and so that the commands that judge a change are not
chosen by the agent being judged.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

SKIP_DIRS = {
    ".git", "node_modules", "vendor", "dist", "build", "out", "target", "coverage", ".venv", "venv",
    "__pycache__", ".next", ".turbo", ".cache", ".idea", ".vscode",
    ".harness", ".agents", ".claude", ".codex", ".cursor", ".opencode", ".omp",
}
LANGUAGES = {
    ".ts": "typescript", ".tsx": "typescript", ".js": "javascript", ".jsx": "javascript", ".mjs": "javascript",
    ".py": "python", ".go": "go", ".rs": "rust", ".java": "java", ".kt": "kotlin", ".rb": "ruby",
    ".cs": "csharp", ".php": "php", ".swift": "swift",
}
TEST_FILE = re.compile(r"(\.|_)(test|spec)\.[a-z]+$|^test_.*\.py$|_test\.go$|Tests?\.(java|kt|cs)$")
# A project with this many source files or fewer is treated as new: there is no code to learn conventions from.
GREENFIELD_MAX_SOURCE_FILES = 3
MAX_FILES_SCANNED = 20000

NODE_LOCKFILES = (("pnpm-lock.yaml", "pnpm"), ("yarn.lock", "yarn"), ("bun.lockb", "bun"), ("bun.lock", "bun"),
                  ("package-lock.json", "npm"))
NODE_FRAMEWORKS = {
    "react": "react", "next": "next", "vue": "vue", "svelte": "svelte", "@angular/core": "angular",
    "express": "express", "fastify": "fastify", "@nestjs/core": "nestjs", "hono": "hono",
    "@prisma/client": "prisma", "prisma": "prisma", "drizzle-orm": "drizzle", "typeorm": "typeorm",
    "vite": "vite", "tailwindcss": "tailwind", "vitest": "vitest", "jest": "jest",
    "@playwright/test": "playwright", "cypress": "cypress", "eslint": "eslint", "typescript": "typescript",
    "@biomejs/biome": "biome",
}
PYTHON_FRAMEWORKS = ("fastapi", "django", "flask", "sqlalchemy", "pydantic", "pytest", "ruff", "black", "mypy", "pyright")
NODE_SCRIPTS = {
    "test": ("test", "test:unit"),
    "lint": ("lint",),
    "typecheck": ("typecheck", "type-check", "check-types", "tsc"),
    "build": ("build",),
    # Only a script that checks: one named `format` usually rewrites the files, which a check must not do.
    "format": ("format:check", "format-check", "check-format", "check:format", "fmt:check", "prettier:check"),
}
TEST_DIRS = {"test", "tests", "__tests__", "spec", "specs", "e2e"}
# Directories two levels down are what a person means by "where things go" in most repositories.
LAYOUT_DEPTH = 2
LAYOUT_MAX = 8
DOC_FILES = ("README.md", "CONTRIBUTING.md", "ARCHITECTURE.md", "AGENTS.md", "CLAUDE.md", "docs/conventions.md",
             "docs/adr", "docs/architecture", "openspec")
CI_FILES = ((".github/workflows", "github-actions"), (".gitlab-ci.yml", "gitlab-ci"), (".circleci", "circleci"),
            ("Jenkinsfile", "jenkins"), ("azure-pipelines.yml", "azure-pipelines"), ("bitbucket-pipelines.yml", "bitbucket"))


def walk(root: Path):
    """Yield project files, skipping dependencies, build output and the harness itself."""
    seen = 0
    stack = [root]
    while stack:
        try:
            entries = sorted(stack.pop().iterdir())
        except OSError:
            continue
        for entry in entries:
            if entry.is_symlink():
                continue
            if entry.is_dir():
                if entry.name not in SKIP_DIRS:
                    stack.append(entry)
            elif entry.is_file():
                seen += 1
                if seen > MAX_FILES_SCANNED:
                    return
                yield entry


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def node(root: Path, found: dict) -> None:
    manifest = root / "package.json"
    if not manifest.is_file():
        return
    try:
        package = json.loads(read(manifest))
    except json.JSONDecodeError:
        found["notes"].append("package.json is not valid JSON; node commands were not detected")
        return
    if not isinstance(package, dict):
        return
    manager = next((name for lock, name in NODE_LOCKFILES if (root / lock).exists()), None)
    declared = str(package.get("packageManager") or "").split("@")[0]
    manager = manager or declared or "npm"
    found["package_managers"].append(manager)
    if package.get("workspaces") or (root / "pnpm-workspace.yaml").exists():
        found["workspaces"] = True
    dependencies: dict = {}
    for manifest_path in [manifest, *sorted(root.glob("*/*/package.json"))[:50]]:
        try:
            data = json.loads(read(manifest_path))
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict):
            for key in ("dependencies", "devDependencies", "peerDependencies"):
                if isinstance(data.get(key), dict):
                    dependencies.update(data[key])
    found["frameworks"] += sorted({label for name, label in NODE_FRAMEWORKS.items() if name in dependencies})
    scripts = package.get("scripts") if isinstance(package.get("scripts"), dict) else {}
    run = f"{manager} run" if manager != "yarn" else "yarn"
    for check, names in NODE_SCRIPTS.items():
        name = next((n for n in names if n in scripts), None)
        if not name:
            continue
        if check == "test" and "no test specified" in str(scripts[name]):
            continue
        command = f"{manager} test" if name == "test" else f"{run} {name}"
        found["checks"].setdefault(check, {"command": command, "source": f"package.json script `{name}`"})


def python(root: Path, found: dict) -> None:
    sources = [name for name in ("pyproject.toml", "requirements.txt", "requirements-dev.txt", "setup.cfg", "setup.py")
               if (root / name).is_file()]
    if not sources:
        return
    text = "\n".join(read(root / name) for name in sources).lower()
    manager = ("uv" if (root / "uv.lock").exists() else "poetry" if (root / "poetry.lock").exists()
               else "pdm" if (root / "pdm.lock").exists() else "pip")
    found["package_managers"].append(manager)
    present = [name for name in PYTHON_FRAMEWORKS if re.search(rf"(^|[^a-z0-9_-]){name}([^a-z0-9_-]|$)", text)]
    found["frameworks"] += present
    prefix = {"uv": "uv run ", "poetry": "poetry run ", "pdm": "pdm run "}.get(manager, "")
    where = ", ".join(sources)
    if "pytest" in present:
        found["checks"].setdefault("test", {"command": f"{prefix}pytest", "source": f"pytest in {where}"})
    if "ruff" in present:
        found["checks"].setdefault("lint", {"command": f"{prefix}ruff check .", "source": f"ruff in {where}"})
    if "black" in present:
        found["checks"].setdefault("format", {"command": f"{prefix}black --check .", "source": f"black in {where}"})
    elif "ruff" in present and "[tool.ruff.format]" in text:
        found["checks"].setdefault("format", {"command": f"{prefix}ruff format --check .", "source": f"[tool.ruff.format] in {where}"})
    for checker, command in (("mypy", "mypy ."), ("pyright", "pyright")):
        if checker in present:
            found["checks"].setdefault("typecheck", {"command": f"{prefix}{command}", "source": f"{checker} in {where}"})


def others(root: Path, found: dict) -> None:
    if (root / "go.mod").is_file():
        found["package_managers"].append("go")
        found["checks"].setdefault("test", {"command": "go test ./...", "source": "go.mod"})
        found["checks"].setdefault("lint", {"command": "go vet ./...", "source": "go.mod"})
        found["checks"].setdefault("build", {"command": "go build ./...", "source": "go.mod"})
    if (root / "Cargo.toml").is_file():
        found["package_managers"].append("cargo")
        found["checks"].setdefault("test", {"command": "cargo test", "source": "Cargo.toml"})
        found["checks"].setdefault("lint", {"command": "cargo clippy -- -D warnings", "source": "Cargo.toml"})
        found["checks"].setdefault("build", {"command": "cargo build", "source": "Cargo.toml"})
        found["checks"].setdefault("format", {"command": "cargo fmt --check", "source": "Cargo.toml"})
    if (root / "pom.xml").is_file():
        found["package_managers"].append("maven")
        found["checks"].setdefault("test", {"command": "mvn -q test", "source": "pom.xml"})
    if (root / "build.gradle").is_file() or (root / "build.gradle.kts").is_file():
        found["package_managers"].append("gradle")
        wrapper = "./gradlew" if (root / "gradlew").is_file() else "gradle"
        found["checks"].setdefault("test", {"command": f"{wrapper} test", "source": "gradle build file"})
    makefile = read(root / "Makefile")
    for check in ("test", "lint", "typecheck", "build"):
        if re.search(rf"^{check}:", makefile, re.M):
            found["checks"].setdefault(check, {"command": f"make {check}", "source": f"Makefile target `{check}`"})
    for target in ("format-check", "fmt-check", "check-format"):
        if re.search(rf"^{target}:", makefile, re.M):
            found["checks"].setdefault("format", {"command": f"make {target}", "source": f"Makefile target `{target}`"})


def detect(project: Path) -> dict:
    """Return the project description. Deterministic for a given tree."""
    root = Path(project)
    counts: dict[str, int] = {}
    areas: dict[str, int] = {}
    source_files = test_files = beside = apart = 0
    for path in walk(root):
        language = LANGUAGES.get(path.suffix.lower())
        if not language:
            continue
        source_files += 1
        counts[language] = counts.get(language, 0) + 1
        parts = path.relative_to(root).parts
        area = "/".join(parts[:min(LAYOUT_DEPTH, len(parts) - 1)]) or "."
        areas[area] = areas.get(area, 0) + 1
        if TEST_FILE.search(path.name):
            test_files += 1
            if any(part in TEST_DIRS for part in parts[:-1]):
                apart += 1
            else:
                beside += 1
    tests = "none" if not test_files else "beside the code" if not apart else "in test directories" if not beside else "mixed"
    layout = [{"path": area, "source_files": n} for area, n in sorted(areas.items(), key=lambda item: (-item[1], item[0]))[:LAYOUT_MAX]]
    found: dict = {"package_managers": [], "frameworks": [], "checks": {}, "workspaces": False, "notes": []}
    node(root, found)
    python(root, found)
    others(root, found)
    kind = "greenfield" if source_files <= GREENFIELD_MAX_SOURCE_FILES else "brownfield"
    missing = [check for check in ("test", "lint", "typecheck") if check not in found["checks"]]
    if kind == "brownfield" and missing:
        found["notes"].append("no command detected for: " + ", ".join(missing) + "; add it under checks or the Validator cannot run it")
    if kind == "brownfield" and not test_files:
        found["notes"].append("no test files found")
    return {
        "kind": kind,
        "source_files": source_files,
        "test_files": test_files,
        "languages": sorted(counts, key=lambda name: (-counts[name], name)),
        "package_managers": list(dict.fromkeys(found["package_managers"])),
        "frameworks": list(dict.fromkeys(found["frameworks"])),
        "workspaces": found["workspaces"],
        "tests": tests,
        "layout": layout,
        "docs": [name for name in DOC_FILES if (root / name).exists()],
        "ci": [label for path, label in CI_FILES if (root / path).exists()],
        "checks": {check: found["checks"][check] for check in ("test", "lint", "typecheck", "build", "format") if check in found["checks"]},
        "notes": found["notes"],
    }


HEADER = """# Written by `gantry inspect --write` from the files of this project.
# Agents read it; they do not edit it. Correct a command here yourself when
# detection got it wrong, and rerun `gantry inspect --write` after changing
# the project's tooling (your corrections are overwritten).
"""


def quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def render(description: dict) -> str:
    """Render the description as YAML that PyYAML and a person can both read."""
    lines = [HEADER.rstrip("\n")]
    for key in ("kind", "source_files", "test_files", "tests", "workspaces"):
        value = description[key]
        lines.append(f"{key}: {str(value).lower() if isinstance(value, bool) else quote(value) if isinstance(value, str) else value}")
    lines.append("layout: []" if not description["layout"] else "layout:")
    for area in description["layout"]:
        lines += [f"  - path: {quote(area['path'])}", f"    source_files: {area['source_files']}"]
    for key in ("languages", "package_managers", "frameworks", "docs", "ci", "notes"):
        items = description[key]
        lines.append(f"{key}: []" if not items else f"{key}:")
        lines += [f"  - {quote(item)}" for item in items]
    checks = description["checks"]
    lines.append("checks: {}" if not checks else "checks:")
    for name, check in checks.items():
        lines += [f"  {name}:", f"    command: {quote(check['command'])}", f"    source: {quote(check['source'])}"]
    return "\n".join(lines) + "\n"


def summary(description: dict) -> list[str]:
    """Lines for a person: what was found and what it means for the first run."""
    join = lambda items: ", ".join(items) or "none detected"
    lines = [
        f"Project: {description['kind']} ({description['source_files']} source files, {description['test_files']} test files)",
        f"  languages:        {join(description['languages'])}",
        f"  package managers: {join(description['package_managers'])}",
        f"  frameworks:       {join(description['frameworks'])}",
        f"  CI:               {join(description['ci'])}",
        f"  tests live:       {description['tests']}",
        f"  largest areas:    {join([area['path'] for area in description['layout'][:4]])}",
    ]
    for name in ("test", "lint", "typecheck", "build", "format"):
        check = description["checks"].get(name)
        lines.append(f"  {name + ':':17} {check['command'] + '  (' + check['source'] + ')' if check else 'not detected'}")
    lines += [f"  note: {note}" for note in description["notes"]]
    if "docs/conventions.md" not in description["docs"]:
        lines.append(
            "  next: run the harness-onboard skill to record this project's conventions from its code"
            if description["kind"] == "brownfield" else
            "  next: run the harness-onboard skill to settle the stack and conventions before the first feature"
        )
    return lines
