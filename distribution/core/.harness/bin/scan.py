#!/usr/bin/env python3
"""Security scan of the lines a change adds. Rules only: same change in, same findings out.

    python3 .harness/bin/scan.py [--project .]

Three kinds of finding:

- secret: a credential in a format a provider issues, or a private key. It
  blocks the Final Pre-PR Gate. A line that carries `gantry:allow` is reported
  as a condition instead, so a person confirms the exception.
- suspect: something that may be a credential (a quoted value assigned to a
  password-like name, a URL with a password, an environment or key file). A
  condition at the final gate.
- risky: a code pattern a security reviewer should look at (dynamic code
  execution, markup injection, queries or shell commands built from strings,
  unsafe deserialization, disabled TLS verification, weak hashes, wildcard
  CORS). It adds the SECURITY trigger to the routing plan, which routes the
  Security gate. It is a reason to look, not a verdict.

Only added lines are scanned, so what the project already contained is not
reported. The value of a finding is never printed.

Standard library only.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ALLOW = "gantry:allow"
MAX_BYTES = 1_000_000

SECRETS = (
    ("private key", re.compile(r"-----BEGIN (?:[A-Z]+ )?PRIVATE KEY")),
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}|\bgithub_pat_[A-Za-z0-9_]{50,}")),
    ("Slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}")),
    ("Stripe live key", re.compile(r"\b[sr]k_live_[A-Za-z0-9]{16,}")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("model provider API key", re.compile(r"\bsk-(?:ant|proj)-[A-Za-z0-9_-]{20,}")),
    ("npm token", re.compile(r"\bnpm_[A-Za-z0-9]{36}\b")),
)

PLACEHOLDER = re.compile(r"example|changeme|change[-_]me|placeholder|dummy|sample|your[-_]|xxxx|\*\*\*|<|\$\{|\{\{|test|fake|localhost", re.I)
ASSIGNED = re.compile(
    r"""(?ix)\b(?:pass(?:word|wd)?|secret|api[-_]?key|access[-_]?key|auth[-_]?token|token|private[-_]?key)\b
        ["']?\s*[:=]\s*["']([^"'\s]{12,})["']""")
URL_PASSWORD = re.compile(r"\b[a-z][a-z0-9+.-]*://[^\s:/@'\"]+:([^\s@'\"]{6,})@[^\s'\"]+")
SUSPECT_FILES = re.compile(r"(?:^|/)(?:\.env(?:\.(?!example|sample|template|dist)[\w.-]+)?|id_rsa|id_ed25519|[^/]+\.(?:pem|p12|pfx|keystore|jks))$")

CODE = (".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte", ".py", ".go", ".rs", ".java", ".kt", ".rb", ".php",
        ".cs", ".swift", ".scala", ".sh")
RISKY = (
    ("dynamic code execution", re.compile(r"(?<![\w.])eval\s*\(|\bnew\s+Function\s*\(|(?<![\w.])exec\s*\(\s*(?:compile|f[\"'])")),
    ("markup injected without escaping", re.compile(r"dangerouslySetInnerHTML|\.(?:inner|outer)HTML\s*=|\bv-html\b|\{@html\b")),
    ("shell command built from a string", re.compile(
        r"shell\s*=\s*True|\bos\.system\s*\(|\bexec(?:Sync)?\s*\(\s*(?:`[^`]*\$\{|[\"'][^\"']*[\"']\s*\+)")),
    ("query built from a string", re.compile(
        r"\$(?:query|execute)RawUnsafe|`\s*(?:select|insert|update|delete)\b[^`]*\$\{|\bf[\"']\s*(?:select|insert|update|delete)\b[^\"']*\{"
        r"|[\"']\s*(?:select|insert|update|delete)\b[^\"']*[\"']\s*(?:\+|%\s*\(|\.format\()", re.I)),
    ("unsafe deserialization", re.compile(r"\bpickle\.loads?\s*\(|\byaml\.load\s*\((?![^)]*Loader)|\bObjectInputStream\b|\bunserialize\s*\(")),
    ("TLS verification disabled", re.compile(
        r"verify\s*=\s*False|rejectUnauthorized\s*:\s*false|InsecureSkipVerify\s*:\s*true|NODE_TLS_REJECT_UNAUTHORIZED")),
    ("weak hash", re.compile(r"createHash\s*\(\s*[\"'](?:md5|sha1)[\"']|\bhashlib\.(?:md5|sha1)\s*\(|MessageDigest\.getInstance\(\s*\"(?:MD5|SHA-?1)\"")),
    ("any origin allowed", re.compile(r"Access-Control-Allow-Origin[\"']?\s*[:,]\s*[\"']\*|\borigin\s*:\s*[\"']\*[\"']")),
)


def git(root: Path, *arguments: str) -> str | None:
    try:
        proc = subprocess.run(["git", *arguments], cwd=root, capture_output=True, text=True, errors="replace", timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return proc.stdout if proc.returncode == 0 else None


def added_lines(root: Path, paths: list[str], base: str | None) -> list[tuple[str, int, str]]:
    """Every line the change adds, as (path, line number, text). Files new to git are read whole."""
    lines: list[tuple[str, int, str]] = []
    seen: set[str] = set()
    diff = git(root, "diff", "-U0", "--no-color", "--no-ext-diff", base) if base else None
    path, number = None, 0
    for raw in (diff or "").splitlines():
        if raw.startswith("+++ "):
            path = raw[6:] if raw.startswith("+++ b/") else None
            if path:
                seen.add(path)
        elif raw.startswith("@@"):
            match = re.match(r"@@ -\S+ \+(\d+)", raw)
            number = int(match.group(1)) if match else 0
        elif raw.startswith("+") and path:
            lines.append((path, number, raw[1:]))
            number += 1
    for path in paths:
        file = root / path
        if path in seen or not file.is_file() or file.stat().st_size > MAX_BYTES:
            continue
        data = file.read_bytes()
        if b"\0" in data:
            continue
        lines += [(path, index, text) for index, text in enumerate(data.decode("utf-8", errors="replace").splitlines(), 1)]
    return lines


def findings(root: Path, paths: list[str], base: str | None) -> dict[str, list[dict]]:
    """Return {"secret": [...], "allowed": [...], "suspect": [...], "risky": [...]}, each item {what, path, line}."""
    wanted = set(paths)
    out: dict[str, list[dict]] = {"secret": [], "allowed": [], "suspect": [], "risky": []}
    for path in paths:
        if SUSPECT_FILES.search(path) and (root / path).is_file():
            out["suspect"].append({"what": "environment or key file in the change", "path": path, "line": 0})
    for path, number, text in added_lines(root, paths, base):
        if path not in wanted or len(text) > 2000:
            continue
        item = {"path": path, "line": number}
        secret = next((name for name, pattern in SECRETS if pattern.search(text)), None)
        if secret:
            out["allowed" if ALLOW in text else "secret"].append({"what": secret, **item})
            continue
        assigned = ASSIGNED.search(text)
        url = URL_PASSWORD.search(text)
        if assigned and not PLACEHOLDER.search(assigned.group(1)):
            out["suspect"].append({"what": "quoted value assigned to a credential name", **item})
        elif url and not PLACEHOLDER.search(url.group(0)):
            out["suspect"].append({"what": "URL that carries a password", **item})
        if path.endswith(CODE):
            out["risky"] += [{"what": name, **item} for name, pattern in RISKY if pattern.search(text)]
    return out


def where(item: dict) -> str:
    return f"{item['path']}:{item['line']}" if item["line"] else item["path"]


def summary(items: list[dict], limit: int = 4) -> str:
    """`weak hash at a.ts:3, b.ts:9; ... and 2 more`, grouped by what was found."""
    groups: dict[str, list[str]] = {}
    for item in items:
        groups.setdefault(item["what"], []).append(where(item))
    parts = []
    for what, places in groups.items():
        shown = ", ".join(places[:limit]) + (f" and {len(places) - limit} more" if len(places) > limit else "")
        parts.append(f"{what} at {shown}")
    return "; ".join(parts)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="scan.py", description="Security scan of the lines the current change adds.")
    parser.add_argument("--project", default=".")
    args = parser.parse_args(argv)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import route  # noqa: E402

    root = Path(args.project).resolve()
    _, paths = route.change_identity(root)
    found = findings(root, paths, route.base_commit(root))
    labels = (("secret", "blocks the final gate"), ("allowed", f"marked {ALLOW}; a person must confirm"),
              ("suspect", "a person must look"), ("risky", "routes the Security gate"))
    if not any(found.values()):
        print(f"SECURITY SCAN: PASS ({len(paths)} changed files)")
        return 0
    print("SECURITY SCAN: FAIL" if found["secret"] else "SECURITY SCAN: FINDINGS")
    for kind, meaning in labels:
        for item in found[kind]:
            print(f"  {kind}: {item['what']} at {where(item)} ({meaning})")
    return 1 if found["secret"] else 0


if __name__ == "__main__":
    sys.exit(main())
