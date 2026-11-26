#!/usr/bin/env python3
"""What git itself refuses, whoever runs it: an agent in any tool, or a person.

    python3 .harness/bin/githook.py pre-commit
    python3 .harness/bin/githook.py pre-push

Installed as git hooks by `gantry install --git-hooks`. A project that has its
own hooks (husky, lefthook, pre-commit) calls these two lines from them.

- pre-commit and pre-push refuse while the change adds a secret: a credential
  in a format a provider issues, or a private key (see scan.py). A line marked
  `gantry:allow` passes here and is a condition at the final gate.
- pre-push says, without refusing, when the project keeps review receipts and
  this version of the change has none: CI will fail it.

A push is not refused for lacking a review: work in progress is pushed all the
time. The review is enforced where a change is merged, by `route.py verify`.
An error inside this script never blocks git.

Standard library only.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def main(argv: list[str] | None = None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    name = arguments[0] if arguments else "pre-commit"
    root = Path(__file__).resolve().parents[2]
    try:
        import route
        identity, paths = route.change_identity(root)
        secrets = route.scan_change(root, paths)["secret"]
        if secrets:
            verb = "push" if name == "pre-push" else "commit"
            print(f"Gantry: the change adds what looks like a secret ({route.scan.summary(secrets)}); the {verb} was refused.\n"
                  "Remove it, and rotate it if it was ever real. If it is a deliberate example, mark the line `gantry:allow`.",
                  file=sys.stderr)
            return 1
        if name == "pre-push" and route.receipts_enabled(root) and identity["type"] == "content" \
                and not (root / route.receipt_file(identity)).is_file():
            print("Gantry: this version of the change has no review receipt, so `route.py verify` will fail it in CI. "
                  "Pushing work in progress is fine; run the harness-run skill before it is merged.", file=sys.stderr)
    except Exception as error:  # a broken guard must not stop anyone from committing
        print(f"Gantry: the git hook could not run ({error!r}); nothing was checked.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
