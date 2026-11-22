from pathlib import Path
import tempfile, subprocess, sys, shutil, json, os

ROOT = Path(__file__).resolve().parents[1]
tmp = Path(tempfile.mkdtemp(prefix="gantry-test-"))
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
        [sys.executable, "-m", "gantry", *args],
        cwd=ROOT, env=env, capture_output=True, text=True
    )
    if p.returncode != expect:
        print(p.stdout)
        print(p.stderr)
        raise SystemExit(f"command failed: {args} -> {p.returncode}")
    return p

(project / ".claude").mkdir()
(project / ".claude/settings.json").write_text(json.dumps({
    "permissions": {"allow": ["Bash(npm test:*)"]},
    "hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "echo mine"}]}],
              "Stop": [{"hooks": [{"type": "command", "command": "echo stop"}]}]},
}), encoding="utf-8")

run("plan", "--runtime", "all", "--project", str(project))
assert ".harness/bin/hook.py" not in (project / ".claude/settings.json").read_text()  # plan changes nothing
run("install", "--runtime", "all", "--scope", "fullstack", "--profile", "standard", "--project", str(project))

# Existing configs preserved.
assert (project / ".cursor/settings.json").read_text() == '{"existing":true}\n'
assert (project / ".codex/config.toml").read_text() == 'model = "existing"\n'
assert (project / ".omp/config.yml").read_text() == "existing: true\n"
assert (project / "opencode.json").read_text() == '{"existing":true}\n'
assert "# Existing rules" in (project / "AGENTS.md").read_text()
assert "<!-- GANTRY:START -->" in (project / "AGENTS.md").read_text()

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

# The shared catalogue has compact descriptions; skills are read by path on demand.
shared_skill = (project / ".agents/skills/auditing-code/SKILL.md").read_text()
assert "description: Portable engineering capability `auditing-code`." in shared_skill
assert (project / ".agents/skills/auditing-code/README.md").exists()
# A runtime with native discovery gets only the entry-point skills, so nothing else sits in context.
assert sorted(p.name for p in (project / ".claude/skills").iterdir()) == ["harness-evaluate", "harness-run"]
shared_run = (project / ".agents/skills/harness-run/SKILL.md").read_text()
assert shared_run == (project / ".claude/skills/harness-run/SKILL.md").read_text()
assert "Portable engineering capability" not in shared_run and "Codex Adapter" not in shared_run
# Claude agents preload nothing and point at skills that exist.
qa_agent = (project / ".claude/agents/qa.md").read_text()
assert "\nskills:" not in qa_agent.split("\n---\n")[0]
assert "`.agents/skills/testing-react-components/SKILL.md`" in qa_agent

# Upgrading removes files an earlier version shipped and this one does not, unless they were edited.
state_file = project / ".harness/install-state.json"
state = json.loads(state_file.read_text())
import hashlib
for name, body in (("old-skill", "old\n"), ("kept-skill", "old\n")):
    stale = project / f".claude/skills/{name}/SKILL.md"
    stale.parent.mkdir(parents=True)
    stale.write_text(body)
    state["managed_files"][f".claude/skills/{name}/SKILL.md"] = {
        "owner": "runtime:claude", "sha256": hashlib.sha256(body.encode()).hexdigest()}
state_file.write_text(json.dumps(state))
(project / ".claude/skills/kept-skill/SKILL.md").write_text("edited by the user\n")
dry = run("plan", "--runtime", "claude", "--project", str(project)).stdout
assert "[DRY-RUN] remove: .claude/skills/old-skill/SKILL.md" in dry and (project / ".claude/skills/old-skill/SKILL.md").exists()
out = run("install", "--runtime", "claude", "--project", str(project)).stdout
assert not (project / ".claude/skills/old-skill").exists()
assert "skip locally modified file: .claude/skills/kept-skill/SKILL.md" in out
assert (project / ".claude/skills/kept-skill/SKILL.md").read_text() == "edited by the user\n"
assert (project / ".codex/agents/reviewer.toml").exists()  # other runtimes are not pruned by a claude-only install
run("install", "--runtime", "claude", "--force", "--project", str(project))  # --force drops the edited leftover too
assert not (project / ".claude/skills/kept-skill").exists()

# Guard hooks are merged into existing Claude settings without disturbing them.
def claude_settings():
    return json.loads((project / ".claude/settings.json").read_text())

def harness_hooks():
    return [h["command"] for e in claude_settings()["hooks"]["PreToolUse"] for h in e["hooks"] if ".harness/bin/hook.py" in h["command"]]

assert len(harness_hooks()) == 2
assert claude_settings()["permissions"] == {"allow": ["Bash(npm test:*)"]}
assert claude_settings()["hooks"]["Stop"] and claude_settings()["hooks"]["PreToolUse"][0]["hooks"][0]["command"] == "echo mine"
assert (project / ".harness/bin/hook.py").exists() and (project / ".harness/bin/route.py").exists()

run("doctor", "--project", str(project))
# --no-hooks removes them again, and doctor then says gates are advisory.
run("install", "--runtime", "claude", "--no-hooks", "--project", str(project))
assert harness_hooks() == [] if "PreToolUse" in claude_settings()["hooks"] else True
assert ".harness/bin/hook.py" not in (project / ".claude/settings.json").read_text()
assert "gates are advisory only" in run("doctor", "--project", str(project)).stdout
# Reinstalling over an unmodified install is idempotent.
run("install", "--runtime", "all", "--scope", "fullstack", "--profile", "standard", "--project", str(project))
run("status", "--project", str(project))

assert len(harness_hooks()) == 2  # the reinstall registered them once, not twice

# Remove one runtime; shared stays.
run("uninstall", "--runtime", "cursor", "--project", str(project))
assert not (project / ".cursor/agents/reviewer.md").exists()
assert (project / ".agents/skills/harness-run/SKILL.md").exists()
assert (project / ".codex/agents/reviewer.toml").exists()

# Remove rest and shared.
run("uninstall", "--runtime", "claude,codex,opencode,omp", "--purge-shared", "--project", str(project))
assert ".harness/bin/hook.py" not in (project / ".claude/settings.json").read_text()
assert claude_settings() == {
    "permissions": {"allow": ["Bash(npm test:*)"]},
    "hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "echo mine"}]}],
              "Stop": [{"hooks": [{"type": "command", "command": "echo stop"}]}]},
}
assert not (project / ".codex/agents/reviewer.toml").exists()
assert not (project / ".agents/skills/harness-run/SKILL.md").exists()
assert "<!-- GANTRY:START -->" not in (project / "AGENTS.md").read_text()
assert "# Existing rules" in (project / "AGENTS.md").read_text()

# An AGENTS.md block written before the rename is replaced, not duplicated.
legacy = (
    "# Existing rules\n\n"
    "<!-- LOOP-ENGINEERING-HARNESS:START -->\nold block\n<!-- LOOP-ENGINEERING-HARNESS:END -->\n\n"
    "# Trailing section\n"
)
(project / "AGENTS.md").write_text(legacy, encoding="utf-8")
run("install", "--runtime", "opencode", "--project", str(project))
migrated = (project / "AGENTS.md").read_text()
assert "LOOP-ENGINEERING-HARNESS" not in migrated and "old block" not in migrated
assert migrated.count("<!-- GANTRY:START -->") == 1
assert migrated.startswith("# Existing rules") and "# Trailing section" in migrated
(project / "AGENTS.md").write_text(legacy, encoding="utf-8")
run("uninstall", "--purge-shared", "--project", str(project))
removed = (project / "AGENTS.md").read_text()
assert "LOOP-ENGINEERING-HARNESS" not in removed and "old block" not in removed
assert "# Existing rules" in removed and "# Trailing section" in removed

shutil.rmtree(tmp)
print("UNIVERSAL DISTRIBUTION SMOKE TEST: PASS")
