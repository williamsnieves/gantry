"""The guided install, the upgrade and the doctor: what a person meets first."""
import builtins
import contextlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from gantry import cli  # noqa: E402

tmp = Path(tempfile.mkdtemp(prefix="gantry-cli-"))


def project(name, files=()):
    root = tmp / name
    root.mkdir()
    for path, text in files:
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_text(text, encoding="utf-8")
    return root


def gantry(*arguments, answers=None, expect=0):
    """Run the CLI in process. `answers` makes it a terminal session that types them."""
    typed = list(answers or [])
    asked = []

    def fake_input(prompt=""):
        asked.append(prompt)
        return typed.pop(0) if typed else ""

    out = io.StringIO()
    real_input, real_interactive = builtins.input, cli.interactive
    builtins.input, cli.interactive = fake_input, (lambda: answers is not None)
    code = 0
    try:
        with contextlib.redirect_stdout(out):
            cli.main([str(a) for a in arguments])
    except SystemExit as stop:
        code = stop.code if isinstance(stop.code, int) else 1 if stop.code else 0
        out.write(str(stop.code) if isinstance(stop.code, str) else "")
    finally:
        builtins.input, cli.interactive = real_input, real_interactive
    assert code == expect, (arguments, code, out.getvalue())
    return out.getvalue(), asked


def config(root):
    return (root / ".harness/harness.config.yaml").read_text()


WEB_AND_API = (("package.json", json.dumps({"dependencies": {"react": "19", "express": "5"}})), ("CLAUDE.md", "# rules\n"))

# Without a terminal nothing can be asked: init says what it would do and changes nothing.
plain = project("plain", WEB_AND_API)
out, _ = gantry("init", "--project", plain, expect=1)
assert "gantry init --yes --runtime claude --scope fullstack --profile standard" in out, out
assert not (plain / ".harness").exists()

# --yes accepts the proposal: the tool the project already uses and the scope its frameworks show.
out, asked = gantry("init", "--yes", "--project", plain)
assert not asked and "scope fullstack, profile standard" in out and (plain / ".claude/agents/reviewer.md").exists(), out
assert "shared-core:" in out and "install shared-core:" not in out, out  # a count per group, not a line per file
assert not list((plain / ".harness").rglob("*.pyc")), "bytecode from a development checkout was installed"
assert "install shared-core: .harness/bin/route.py" in gantry("install", "--runtime", "claude", "--verbose", "--project", plain)[0]

# In a terminal it asks, with what it found as the default, and a wrong answer is asked again.
guided = project("guided", WEB_AND_API)
out, asked = gantry("init", "--project", guided, answers=["nope", "claude,codex", "", "lean", "n", "y", "", "y", ""])
assert "Unsupported runtime(s): nope" in out and "found CLAUDE.md" in out, out
assert [prompt.split(" [")[1] for prompt in asked[:3]] == ["claude]: ", "claude]: ", "fullstack]: "], asked
assert "scope_profile: fullstack" in config(guided) and "delivery_profile: lean" in config(guided)
assert (guided / ".codex/agents/reviewer.toml").exists()
assert not (guided / ".claude/settings.json").exists()  # hooks were declined
assert "receipts: true" in config(guided) and "Review receipts are on" in out, out
assert "mutation: true" in config(guided) and "Mutation testing is on" in out and (guided / ".harness/bin/mutate.py").exists(), out
# A flag is an answer: it is not asked again. Declining at the end changes nothing.
declined = project("declined", WEB_AND_API)
out, asked = gantry("init", "--runtime", "cursor", "--scope", "backend", "--project", declined, answers=["", "", "", "", "n"])
assert len(asked) == 5 and "Nothing was changed." in out and not (declined / ".harness").exists(), (asked, out)
# No tool in the project or named: init says how to name one instead of guessing.
empty = project("empty")
real_which, cli.shutil.which = cli.shutil.which, lambda name: None
out, _ = gantry("init", "--yes", "--project", empty, expect=1)
cli.shutil.which = real_which
assert "Name one: gantry init --runtime" in out and not (empty / ".harness").exists(), out

# A reinstall keeps the scope and profile that were chosen.
gantry("install", "--runtime", "claude", "--no-hooks", "--project", guided)
assert "scope_profile: fullstack" in config(guided) and "delivery_profile: lean" in config(guided)

# The retired `strict` profile is accepted and installed as `standard`, from a flag or from an older installation.
gantry("install", "--runtime", "codex", "--profile", "strict", "--project", declined)
assert "delivery_profile: standard" in config(declined)
(declined / ".harness/harness.config.yaml").write_text(config(declined).replace("delivery_profile: standard", "delivery_profile: strict"))
gantry("upgrade", "--project", declined)
assert "delivery_profile: standard" in config(declined)

# Upgrade: same runtimes, scope, profile and hook choice, without naming any of them.
out, _ = gantry("upgrade", "--project", guided)
assert "for claude, codex (hooks stay off" in out and "delivery_profile: lean" in config(guided), out
assert not (guided / ".claude/settings.json").exists() and "receipts: true" in config(guided)  # receipts stay on too
assert "mutation: true" in config(guided)
assert "Mutation testing is on, but no test command is recorded" in gantry("doctor", "--project", guided)[0]
# Receipts that nothing checks are reported, until a CI file runs the verification; they can be turned off again.
out, _ = gantry("doctor", "--project", guided)
assert "no CI file runs `route.py verify`" in out, out
(guided / ".github/workflows").mkdir(parents=True)
(guided / ".github/workflows/ci.yml").write_text("steps:\n  - run: python3 .harness/bin/route.py verify --base origin/main\n")
assert "route.py verify" not in gantry("doctor", "--project", guided)[0]
gantry("install", "--runtime", "claude", "--no-hooks", "--no-receipts", "--no-mutation", "--project", guided)
assert "receipts: false" in config(guided) and "mutation: false" in config(guided)
assert "permissionMode: plan\n" in (guided / ".claude/agents/qa.md").read_text()
out, _ = gantry("upgrade", "--project", empty, expect=1)
assert "run `gantry init`" in out

# An edited file stops the upgrade before anything is written, and every such file is named at once.
state_before = (plain / ".harness/install-state.json").read_text()
for name in ("qa.md", "security.md"):
    with (plain / ".claude/agents" / name).open("a") as file:
        file.write("\nmine\n")
stale = plain / ".harness/bin/route.py"
shipped = stale.read_bytes()
state = json.loads(state_before)
stale.write_text("old\n")  # as if an older version had installed another route.py
state["managed_files"][".harness/bin/route.py"]["sha256"] = cli.sha256(stale)
(plain / ".harness/install-state.json").write_text(json.dumps(state))
out, _ = gantry("upgrade", "--project", plain, expect=1)
assert "2 file(s) would be overwritten" in out and "qa.md: was edited" in out and "security.md: was edited" in out, out
assert stale.read_text() == "old\n" and "Nothing was changed." in out
out, _ = gantry("upgrade", "--dry-run", "--force", "--project", plain)
assert "(1 updated)" in out and "(2 updated)" in out, out
assert stale.read_text() == "old\n"
gantry("upgrade", "--force", "--project", plain)
assert stale.read_bytes() == shipped and "mine" not in (plain / ".claude/agents/qa.md").read_text()
# A file that is already what the harness ships is adopted, not refused: an interrupted install can be rerun.
state = json.loads((plain / ".harness/install-state.json").read_text())
del state["managed_files"][".claude/agents/qa.md"]
(plain / ".harness/install-state.json").write_text(json.dumps(state))
gantry("upgrade", "--project", plain)
assert ".claude/agents/qa.md" in json.loads((plain / ".harness/install-state.json").read_text())["managed_files"]

# Doctor: every problem comes with what to do about it.
out, _ = gantry("doctor", "--project", plain)
assert out.startswith("DOCTOR: PASS WITH WARNINGS") and "not a git repository" in out and "fix: git init" in out, out
assert "docs/conventions.md is not written yet" in out and "every gate runs on the session's model" in out, out
subprocess.run(["git", "init", "-q"], cwd=plain, check=True)
# The review state of the change in progress is local: the installation keeps it out of git by itself.
(plain / ".harness/runtime/claude").mkdir(parents=True)
(plain / ".harness/runtime/claude/routing-plan.yaml").write_text("lane: SPEC\n")
listed = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"], cwd=plain, capture_output=True, text=True).stdout
assert ".harness/bin/route.py" in listed and ".harness/runtime" not in listed, listed
(plain / ".harness/models.yaml").write_text("claude:\n  fast: haiku\n  quick: haiku\n")
(plain / "docs").mkdir()
(plain / "docs/conventions.md").write_text("# Conventions\n")
out, _ = gantry("doctor", "--project", plain)
assert "not a git repository" not in out and "not ignored by git" not in out, out
assert "gates run on fast=haiku; the hook launches each gate on it" in out and "unknown tier quick" in out, out
assert "docs/conventions.md does not pass its check" in out, out
# An installation older than the CLI, a script that cannot run, and a missing file.
stale.write_text("raise SystemExit('boom')\n")
state = json.loads((plain / ".harness/install-state.json").read_text())
state["managed_files"][".harness/bin/route.py"]["sha256"] = cli.sha256(stale)
state["harness_version"] = "0.9.0"
(plain / ".harness/install-state.json").write_text(json.dumps(state))
(plain / ".claude/agents/reviewer.md").unlink()
out, _ = gantry("doctor", "--project", plain, expect=1)
assert out.startswith("DOCTOR: FAIL") and "The installation is 0.9.0; this CLI is" in out and "ships 1 file(s) that differ" in out, out
assert "route.py` does not run: boom" in out and "Missing managed file: .claude/agents/reviewer.md" in out and "fix: gantry upgrade" in out, out
gantry("upgrade", "--project", plain)
assert gantry("doctor", "--project", plain)[0].count("fix: gantry upgrade") == 0

# Git hooks: what git itself refuses, in any tool and for a person. Tried with real commits.
def git(root, *arguments, expect=0):
    proc = subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid", *arguments], cwd=root, capture_output=True, text=True)
    assert proc.returncode == expect, (arguments, proc.returncode, proc.stdout, proc.stderr)
    return proc.stdout + proc.stderr

hooked = project("hooked", (("src/app.ts", "export const a = 1;\n"),))
out, _ = gantry("install", "--runtime", "cursor", "--git-hooks", "--project", hooked)
assert "not a git repository yet" in out and "git_hooks: true" in config(hooked), out
git(hooked, "init", "-q", "-b", "main")
assert "pre-commit and pre-push does not reach the harness" in gantry("doctor", "--project", hooked)[0]
out, _ = gantry("upgrade", "--project", hooked)  # a fresh clone gets them the same way
assert "git hook: pre-commit" in out and "git hook: pre-push" in out, out
assert "does not reach the harness" not in gantry("doctor", "--project", hooked)[0]
assert "git hook:" not in gantry("upgrade", "--project", hooked)[0]  # nothing to rewrite the second time
git(hooked, "add", "-A")
git(hooked, "commit", "-q", "-m", "base")
git(hooked, "checkout", "-q", "-b", "feature")
token = "gh" + "p_" + "a1B2" * 9  # built from pieces so this file holds nothing a scanner would stop
(hooked / "src/app.ts").write_text(f'export const token = "{token}";\n')
out = git(hooked, "commit", "-q", "-am", "leak", expect=1)
assert "looks like a secret (GitHub token at src/app.ts:1); the commit was refused" in out and token not in out, out
(hooked / "src/app.ts").write_text(f'export const token = "{token}"; // gantry:allow documented example\n')
git(hooked, "commit", "-q", "-am", "an example a person will confirm at the gate")
(hooked / "src/app.ts").write_text("export const a = 2;\n")
git(hooked, "commit", "-q", "-am", "clean")
# A project's own hook is never overwritten; it is told the line to add, and doctor accepts it once it calls the harness.
own = hooked / ".git/hooks/pre-commit"
own.write_text("#!/bin/sh\necho mine\n")
out, _ = gantry("upgrade", "--project", hooked)
assert "keep: your own pre-commit hook" in out and "python3 .harness/bin/githook.py pre-commit" in out and own.read_text() == "#!/bin/sh\necho mine\n", out
assert "pre-commit does not reach the harness" in gantry("doctor", "--project", hooked)[0]
own.write_text("#!/bin/sh\necho mine\npython3 .harness/bin/githook.py pre-commit\n")
assert "does not reach the harness" not in gantry("doctor", "--project", hooked)[0]
# Turning them off removes the harness's hook and leaves the project's own.
out, _ = gantry("install", "--runtime", "cursor", "--no-git-hooks", "--project", hooked)
assert "remove git hook: pre-push" in out and not (hooked / ".git/hooks/pre-push").exists() and own.exists(), out
assert "git_hooks: false" in config(hooked)

# `gantry check` runs the commands the project recorded, with no model, and exits non-zero when one fails.
(plain / ".harness/project.yaml").write_text(f'checks:\n  lint:\n    command: "{sys.executable} -c pass"\n')
out, _ = gantry("check", "--project", plain)
assert "check: lint       PASS" in out and "CHECKS: PASS (passed: lint)" in out, out
assert "CHECKS: PASS (passed: lint)" in gantry("check", "--status", "--project", plain)[0]
(plain / ".harness/project.yaml").write_text(f'checks:\n  lint:\n    command: "{sys.executable} -c raise(SystemExit(3))"\n')
out, _ = gantry("check", "--only", "lint", "--project", plain, expect=1)
assert "check: lint       FAIL (exit 3)" in out, out
assert "older than this command" in gantry("check", "--project", empty, expect=1)[0]

shutil.rmtree(tmp)
print("CLI TESTS: PASS")
