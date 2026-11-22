from pathlib import Path
import tempfile, subprocess, sys, shutil, json, os

ROOT = Path(__file__).resolve().parents[1]
tmp = Path(tempfile.mkdtemp(prefix="leh-v1-test-"))
project = tmp / "repo"
project.mkdir()

(project / "AGENTS.md").write_text("# Existing rules\n", encoding="utf-8")
(project / ".cursor").mkdir()
(project / ".cursor/settings.json").write_text('{"existing":true}\n', encoding="utf-8")
(project / ".codex").mkdir()
(project / ".codex/config.toml").write_text('model = "existing"\n', encoding="utf-8")
(project / ".omp").mkdir()
(project / ".omp/config.yml").write_text("existing: true\n", encoding="utf-8")
(project / "opencode.json").write_text('{"existing":true}\n', encoding="utf-8")

env = os.environ.copy()
env["PYTHONPATH"] = str(ROOT)

def run(*args, expect=0):
    p = subprocess.run(
        [sys.executable, "-m", "leh", *args],
        cwd=ROOT, env=env, capture_output=True, text=True
    )
    if p.returncode != expect:
        print(p.stdout)
        print(p.stderr)
        raise SystemExit(f"command failed: {args} -> {p.returncode}")
    return p

run("plan", "--runtime", "all", "--project", str(project))
run("install", "--runtime", "all", "--scope", "fullstack", "--profile", "standard", "--project", str(project))

# Existing configs preserved.
assert (project / ".cursor/settings.json").read_text() == '{"existing":true}\n'
assert (project / ".codex/config.toml").read_text() == 'model = "existing"\n'
assert (project / ".omp/config.yml").read_text() == "existing: true\n"
assert (project / "opencode.json").read_text() == '{"existing":true}\n'
assert "# Existing rules" in (project / "AGENTS.md").read_text()
assert "<!-- LOOP-ENGINEERING-HARNESS:START -->" in (project / "AGENTS.md").read_text()

# Shared installed once.
assert (project / ".agents/skills/harness-run/SKILL.md").exists()
assert (project / ".harness/core/routing/ROUTING-POLICY.md").exists()
assert (project / ".harness/core/pre-pr/FINAL-PRE-PR-GATE.md").exists()

# All runtime overlays.
assert (project / ".claude/agents/reviewer.md").exists()
assert (project / ".codex/agents/reviewer.toml").exists()
assert (project / ".cursor/agents/reviewer.md").exists()
assert (project / ".opencode/agents/reviewer.md").exists()
assert (project / ".omp/agents/reviewer.md").exists()

run("doctor", "--project", str(project))
run("status", "--project", str(project))

# Remove one runtime; shared stays.
run("uninstall", "--runtime", "cursor", "--project", str(project))
assert not (project / ".cursor/agents/reviewer.md").exists()
assert (project / ".agents/skills/harness-run/SKILL.md").exists()
assert (project / ".codex/agents/reviewer.toml").exists()

# Remove rest and shared.
run("uninstall", "--runtime", "claude,codex,opencode,omp", "--purge-shared", "--project", str(project))
assert not (project / ".codex/agents/reviewer.toml").exists()
assert not (project / ".agents/skills/harness-run/SKILL.md").exists()
assert "<!-- LOOP-ENGINEERING-HARNESS:START -->" not in (project / "AGENTS.md").read_text()
assert "# Existing rules" in (project / "AGENTS.md").read_text()

shutil.rmtree(tmp)
print("UNIVERSAL DISTRIBUTION SMOKE TEST: PASS")
