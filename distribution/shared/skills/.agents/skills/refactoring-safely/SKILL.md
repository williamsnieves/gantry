---
name: refactoring-safely
description: Change how code is built without changing what it does. Use when a reviewer reported a code smell, when the user asks to refactor or clean up code, or before adding a feature to code that is hard to change. It fixes the current behaviour in tests first, applies one refactoring at a time, and reaches for a design pattern only when a simpler refactoring does not remove the smell.
---

# Refactoring Safely

A refactoring is its own change: no new behaviour and no fix in the same pull request. If you find a defect on the way, write it down and leave it; fixing it here would make the tests change, and the tests are the proof.

1. **Name the smell and where it is.** Take it from the reviewer's finding, or read the code and name it yourself: one smell, one file and line range. `references/smells.md` lists the names. If you cannot name a smell, there is nothing to refactor; say so and stop.
2. **Choose the smallest refactoring that removes it.** Read the row for that smell in `references/smells.md`. Take the first refactoring listed. Take a design pattern only when its condition in the table holds in the code today, not in a future you imagine.
3. **Make sure tests describe what the code does now.** Run `python3 .harness/bin/check.py --only test`. Read the tests of the code you will touch. For each behaviour they do not check (a branch, a boundary, an error), add a test that asserts what the code does today, even where that looks wrong.
4. **Pin.** Run `python3 .harness/bin/refactor.py pin` before you change any code. It runs the tests and records every test file. From here on, leave those files as they are.
5. **Refactor in steps.** One refactoring at a time: extract one function, move one method, introduce one class. After each, run `python3 .harness/bin/check.py --only test`. Go on only when it passes.
6. **Check the tests would have noticed.** Run `python3 .harness/bin/mutate.py`. It does nothing unless the project turned mutation testing on. A `survived:` line on code you moved means the pinned tests do not protect it: go back to step 3 for that line, on a fresh pin.
7. **Confirm and hand over.** Run `python3 .harness/bin/refactor.py status`; it must say `REFACTOR: HELD`. Then run the `harness-run` skill. In the pull request, name the smell, the refactorings applied in order, and any pinned test you had to edit and why.

## When a step fails

| What happened | What to do |
|---|---|
| `REFACTOR: NOT PINNED (code is already changed ...)` | Set the edits aside with `git stash`, pin, then `git stash pop`. |
| A test you wrote in step 3 fails on the current code | The test is wrong about what the code does. Fix the test; do not touch the code. |
| The tests fail after a refactoring step | Undo that step (`git checkout -- <files>` for an uncommitted step). Do not edit the test to make it pass. Try a smaller step. |
| A pinned test must change because a name or a path moved | Change only the import or the name, never an assertion. `refactor.py status` will list it and the final gate carries a condition; explain it in the pull request. |
| The behaviour has to change to remove the smell | It is not a refactoring. Run `python3 .harness/bin/refactor.py clear` and start it as a normal change with the `harness-start` skill. |
| The code has no tests and cannot be tested as it is | Make the smallest change that lets a test reach it (pass a dependency in, extract a pure function), by hand and reviewed on its own, before this procedure. |

## What not to do

- Do not introduce a pattern because the code "might need it". A pattern is paid for in indirection on every later read.
- Do not rename, reformat and restructure in the same step: the diff stops showing what moved.
- Do not widen the change to code the smell is not in.
