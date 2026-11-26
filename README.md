# Gantry

Universal distribution of the portable software-engineering harness.

## One CLI

```bash
./gantry.sh init --project /path/to/repo
```

`init` looks at the project, proposes the agent tools it uses, a scope and a profile, and asks before it installs. It proposes a tool because the project already has its files (`.claude/`, `.cursor/`, `opencode.json`), or else because its command is on your PATH; it proposes the scope from the frameworks it detects. Every question has that proposal as its default, and a flag is an answer that is not asked again.

Where nothing can be asked (CI, a script), name what you want:

```bash
./gantry.sh init --yes --project .                       # accept the proposal
./gantry.sh install --runtime cursor --project /path/to/repo
./gantry.sh install --runtime claude,codex,cursor,opencode,omp --project .
./gantry.sh install --runtime all --project .
```

On Windows PowerShell:

```powershell
.\gantry.ps1 init --project .
```

## What the installer handles automatically

### Shared once

```text
.harness/
.agents/skills/
AGENTS.md managed block
```

### Runtime overlays

```text
Claude Code
→ .claude/agents/
→ .claude/skills/
→ .claude/rules/

Codex
→ .codex/agents/

Cursor
→ .cursor/agents/
→ .cursor/rules/

OpenCode
→ .opencode/agents/
→ .opencode/commands/

Oh My Pi
→ .omp/agents/
→ .omp/commands/
→ .omp/RULES.md
```

Codex, Cursor, OpenCode and OMP share one `.agents/skills/` installation.

Claude receives only the entry-point skills in `.claude/skills/`; its agents read the shared catalogue on demand.

## Typical setup

```bash
./gantry.sh init    --project ~/code/my-app     # asks, then installs
./gantry.sh doctor  --project ~/code/my-app     # checks it, and says how to fix what is wrong
./gantry.sh upgrade --project ~/code/my-app     # later: bring it to a newer Gantry
```

An install prints a count of files per group; `--verbose` prints every file, and `plan` or `--dry-run` shows what would change without writing.

`upgrade` reinstalls what is there with the version of Gantry you are running. It keeps the runtimes, the scope, the profile and whether the hooks are registered, and never touches `.harness/project.yaml`, `.harness/models.yaml` or `docs/`. Before writing anything it lists every harness file you edited and stops; `--force` replaces them with the harness's version.

`doctor` checks more than the files. It runs the router and the hook with `python3` as an agent would, and reports: an installation older than the CLI, a project that is not a git repository (the router identifies a change through git), check commands the Validator has no entry for, a missing or failing `docs/conventions.md`, and which model each runtime's gates run on. Each finding is followed by a `fix:` line. Errors exit non-zero; warnings and notes do not.

Then:

```text
Cursor     → /harness-run
Codex      → $harness-run
Claude     → /harness-run
OpenCode   → /harness-run
Oh My Pi   → /harness-run
```

## Project description

`gantry install` looks at the project once and writes what it finds to `.harness/project.yaml`: whether the project is new or existing, its languages, package managers and frameworks, its CI, and the commands that run its tests, lint, type checks and build. Nothing is executed and no model is called.

```bash
gantry inspect --project ~/code/my-app          # print it
gantry inspect --project ~/code/my-app --write  # refresh the saved file after changing tooling
```

The Validator starts from those commands instead of rediscovering them on every run. Agents cannot edit the file: the commands that judge a change are not chosen by the agent being judged. Correct it by hand when detection is wrong; a reinstall keeps your version and `inspect --write` replaces it. A command is listed only when the project declares it (a script, a dependency, a build file); anything else is reported as not detected.

## Onboarding

After installing, run the `harness-onboard` skill once in your agent (`/harness-onboard`, or `$harness-onboard` in Codex). It writes `docs/conventions.md`, a file of under 600 words that later runs and reviewers read first.

- In an existing project it reads the code and records what at least two files show, naming a file for each statement. Where the code does the same job two ways it lists both as an open question instead of choosing.
- In a new project it asks at most five questions, each with a default, and records the answers.

The file belongs to the project: edit it freely, and it stays if the harness is removed. `python3 .harness/bin/conventions.py check` verifies its headings, its length and that every path it cites exists.

## Starting a piece of work

Give your agent the request through the `harness-start` skill. The agent builds; the harness decides how much has to be settled first.

| Lane | When | Before building |
|---|---|---|
| `DIRECT` | No risk trigger: behavior, data and interfaces stay as they are | Nothing |
| `SPEC` | The accepted behavior changes | Acceptance criteria and slices in `docs/specs/<name>.md` |
| `DESIGN` | Architecture, security, data integrity, migration or compatibility is involved | The same, plus a design, and your approval |

The lane comes from `python3 .harness/bin/route.py lane`, from the same risk triggers that later choose the reviewers; the size of the change is not an input. `python3 .harness/bin/spec.py check` verifies that a specification has its sections, that every acceptance criterion has an id and is delivered by a slice, and that a `DESIGN` change has its design. The agent then builds slice by slice, test first, and `harness-run` reviews the result against the specification.

The routing plan records the lane. When a `SPEC` or `DESIGN` change reaches the Final Pre-PR Gate without an existing file passed as `--behavior-source`, the gate still passes but carries a condition saying the accepted behavior was not written down, so a person sees it in the pull request.

## Which model runs each gate

The router gives every gate a tier, from the gate's job and the lane of the change:

| Gate | `DIRECT` and `SPEC` lanes | `DESIGN` lane |
|---|---|---|
| Validator | `fast` | `standard` |
| Code reviews, QA, Performance, Infrastructure, Detail Analyst | `standard` | `deep` |
| Security, Architecture reviews, Reviewer | `deep` | `deep` |

The tier follows the risk, so nothing is saved on a risky change or on the gates that judge risk. Which model a tier means is the project's decision, in `.harness/models.yaml`:

```yaml
claude:
  fast: haiku
  standard: sonnet
  deep: ""        # empty: the session's own model
```

The installer writes the file with every tier empty, which runs every gate on the session's model as before, and never overwrites it. With a tier filled in, `route.py plan` shows the model beside each gate and the `next:` line is followed by `models: launch validator=haiku`. On Claude Code the hook launches the gate on that model whatever the launch asked for; on other runtimes the lead follows the `models:` line where the runtime lets it choose.

## Shipping, and what happened after

The `harness-ship` skill takes a reviewed change out and closes the loop on it.

```bash
python3 .harness/bin/release.py check --runtime claude
python3 .harness/bin/release.py record --outcome SHIPPED --change "#42 severity filter"
python3 .harness/bin/release.py record --outcome INCIDENT --change "#42" --note "filtered list showed other tenants" --missed SECURITY
```

`check` prints `RELEASE_READY`, `RELEASE_READY_WITH_CONDITIONS` or `RELEASE_BLOCKED`. It requires the Final Pre-PR Gate to pass, and adds what only matters when shipping: a migration, a release-only change, or a change with a `MIGRATION`, `INFRASTRUCTURE` or `DATA_INTEGRITY` trigger needs a `## Rollout` section in its specification (the order it is deployed in, how it is verified in production, how it is undone); a change users will notice carries a condition when the project keeps a changelog and the change does not touch it.

`record` appends a line to `docs/releases.md`. A rollback or an incident says what happened and, with `--missed`, which risk nobody declared when the change was routed. The harness does not deploy and does not watch production: the record is written by whoever saw the outcome. It is the list of what got past the review.

## Checking in CI that what is merged was reviewed

The hooks stop an agent on Claude Code. On every other tool, and for a person, nothing stops a pull request that was never reviewed or that was edited after its review. Review receipts close that gap, and are off unless you ask for them:

```bash
./gantry.sh install --runtime cursor --receipts --project .
```

With receipts on, a passing `route.py ready` writes `.harness/receipts/<digest>.json`: the digest of the change's content, the gate status, its conditions, and each required gate's decision. Commit it with the change. The receipt is not part of the change it describes, so committing it does not invalidate the review; reviewing the change again replaces it. In CI, on pull requests:

```yaml
- uses: actions/checkout@v4
  with:
    fetch-depth: 0                                    # the base branch is needed to find where the change starts
    ref: ${{ github.event.pull_request.head.sha }}    # the change as it was reviewed, not its merge with the base
- run: python3 .harness/bin/route.py verify --base origin/${{ github.base_ref }}
```

`verify` computes the digest of the pull request's content and fails when there is no receipt for it, or when the receipt does not record a pass. One edit after the review, committed or not, is a different digest. It prints the conditions the review left, so they are in the CI log.

What a receipt proves is that the router reached a pass for exactly this content. It does not prove who ran the gates: where no hook protects the file, it can be written by hand like any other, and a person reading the pull request sees it in the diff. Each merged change leaves one small file; delete old ones whenever you like.

## What goes into git

Commit the installation: `.harness/`, `.agents/skills/`, the runtime folders and `AGENTS.md`, so everyone on the project works with the same harness, and `.harness/receipts/` when you keep review receipts. `.harness/runtime/` is the exception and the installation ignores it by itself: it holds the routing plan, the gate reports and the approvals of the change in progress, which are local to a working copy. What a reviewer needs from them goes in the pull request, where `harness-ship` puts the conditions.

## Project scope

```text
fullstack
backend
frontend
architecture
infrastructure
mixed
```

This is advisory context for routing, **not a hard gate suppressor**.

A frontend project can still activate Security or Infrastructure if the actual change creates those risks.

## Delivery profiles

```text
lean
standard
```

The profile decides how much the hooks refuse; the routing and the Final Pre-PR Gate are the same in both. `lean` denies only edits to the harness and committing a secret. `standard` also denies weakening a check, launching a gate after the review stopped, and opening or merging a pull request before its gate passes. A `strict` profile existed and did the same as `standard`; it is still accepted and installed as `standard`.

## Quality, security, performance, scalability

Every change is judged for the same four things, and the Final Pre-PR Gate says for each one who judged it:

```text
PRE_PR_PASS
  pillar: quality: validator PASS, backend-code-review PASS, qa PASS, detail-analyst PASS, reviewer PASS
  pillar: security: added lines scanned for secrets and risky patterns; security PASS
  pillar: performance: added lines scanned for queries in loops and unbounded reads; no specialist gate ran, no PERFORMANCE trigger was declared or detected
  pillar: scalability: no specialist gate ran, no PERFORMANCE or INFRASTRUCTURE trigger was declared or detected
```

| Pillar | On every change | When the risk calls for it |
|---|---|---|
| Quality | The project's own checks (Validator), a code review, the Detail Analyst and the Reviewer | QA, when behavior, data integrity, compatibility or user impact changes; mutation testing of the added lines, when the project turned it on |
| Security | A scan of every added line: a secret blocks, a risky pattern routes the Security gate | The Security gate (STRIDE, OWASP Top 10, CWE Top 25, OWASP ASVS), on a `SECURITY` trigger |
| Performance | A scan of every added line of runtime code: a query or request inside a loop, or a list read without a limit, routes the Performance gate | The Performance gate, on a `PERFORMANCE` trigger: a target, a measured regression, data growth, a sensitive path |
| Scalability | The same scan: both patterns are costs that grow with the data | The Performance gate for load and capacity, the Infrastructure gate for how it is deployed and scaled |

The lines go into the pull request unchanged, and into the review receipt when the project keeps them. A pillar that no specialist judged is stated, not left out: the person reading the pull request decides whether that is right for this change. The performance rules are two, on purpose: they are the patterns a line of code shows by itself. A slow algorithm, a missing index or a heavy bundle is not something a rule over added lines can see, so those are reviewed when the agent or the person declares the trigger. A finding is a reason to look, not a verdict: `route.py plan --dismiss "PERFORMANCE=why"` drops it with a written reason, and tests, scripts, seeds and migrations are not scanned for it.

## Would the tests notice? Mutation testing of the change

Tests that execute a line do not necessarily check what it decides. With mutation testing on, the review changes each line the change adds, one small change at a time, and runs the project's own tests against it:

```bash
./gantry.sh install --runtime claude --mutation --project .
python3 .harness/bin/mutate.py
```

```text
MUTATION: SURVIVORS (0 of 1 mutants killed)
  survived: src/pricing.py:6 `>=` changed to `>`
  next: for each survivor, add the test that fails on that change, or say in the pull request why the change makes no difference; then run this again
```

Here the tests tried a total of 99 and of 101; nothing tried 100, so nothing would notice the boundary moving. A survivor is a condition at the Final Pre-PR Gate, not a blocker: a mutant can be equivalent to the original, and a person or QA decides. The quality line of the gate carries the count (`mutation: 4 of 5 changes to the added lines were caught by the tests`).

- **What is mutated:** only added lines of runtime code, never tests, scripts or migrations. Operators: comparison boundaries, equality, `&&`/`||`, a removed negation, `true`/`false`, `+ - *`. Strings, imports and types are left alone.
- **What judges it:** the test command recorded in `.harness/project.yaml`. It is not an argument, so the agent being judged does not choose it, and the tests must pass before any mutation.
- **Bounded:** at most `--max` mutants (12), spread over the added lines, within `--budget` seconds (600). What was not run is said in the same line.
- **Safe to interrupt:** the file is saved before each mutant and put back after it. If a run is killed, the next run or `mutate.py restore` puts it back, and the final gate blocks while a mutant is in the code.
- **A result is for one version:** edit the change, including adding the missing test, and the gate asks for a new run.

It is off unless you turn it on, because it costs test runs: about a dozen per review. It measures whether the tests check what the new lines decide; it does not find defects the operators do not model. In the review cases of this repository it kills every mutant of the change with the planted tenant leak, because the leak is not a boundary or a negation.

## Guardrails

A guardrail is something the harness guarantees whatever the agent decides. None of them is decided by a model: each is a rule over the files, the routing plan and the recorded gate results, so it fires the same way every time. Which ones apply to a change follows its risk: the lane and the triggers choose them, as they choose the reviewers.

`python3 .harness/bin/route.py guardrails` prints the list:

```text
ANY
  the harness's files and routing state are not edited by the agent
    every runtime: the final gate rejects a routing plan or a report that was changed by hand
    with hooks: the edit is denied
SPECIFY
  how much is settled before building follows the risk, not the size
    every runtime: `route.py lane`; `route.py plan` computes the lane again from the change itself
  a specification has its criteria, and each criterion is delivered by a slice
    every runtime: `spec.py check`
  a design is approved by a person
    every runtime: the final gate carries a condition until `spec.py approve` was run on the current text
    with hooks: `spec.py approve` asks the person to confirm; a reviewing agent cannot run it
BUILD
  a failing check is fixed in the code, not by weakening the check
    every runtime: the final gate carries a condition naming any lint, type, test or CI configuration the change edits
    with hooks: the edit and `--no-verify` are denied (not in the lean profile)
  a secret does not leave in the change
    every runtime: `scan.py` reads every added line; the final gate blocks on a credential in a provider's format or a private key, and carries a condition for anything that may be one
    with hooks: `git commit` and `git push` are denied while one is there
  code that needs a security reviewer gets one
    every runtime: a risky pattern in the added lines adds the SECURITY trigger to the routing plan, which routes the Security gate
  code that needs a performance reviewer gets one
    every runtime: a query or request inside a loop, or a list read without a limit, in the added lines adds the PERFORMANCE trigger to the routing plan, which routes the Performance gate; `route.py plan --dismiss` drops it with a written reason
  the tests of a change would notice if its lines were wrong, when the project turned mutation testing on
    every runtime: `mutate.py` changes each added line and runs the project's tests; the final gate carries a condition for every change the tests did not notice, and for a version that was not mutated; it blocks while a mutant is left in the code
REVIEW
  a reviewer reports and does not fix; a report is what the reviewer wrote
    every runtime: the final gate rejects a report changed after its result was recorded
    with hooks: a reviewer can write only its own report, and nobody else can write it
  each gate runs on the model its job and the change's risk call for, when the project maps tiers to models
    every runtime: `route.py plan` records a tier per gate and `next:` names the model to launch
    with hooks: the gate is launched on that model whatever was asked
  the review stops at the first stage that does not pass
    every runtime: `route.py next`; the final gate stays blocked
    with hooks: launching a later gate is denied (not in the lean profile)
  a risk a gate sees outside its own scope is not lost under its pass
    every runtime: `route.py gate --trigger` records it; the router asks for the plan to be rerun with it, and the final gate carries a condition while no routed gate has judged it
  a result counts only for the version of the change it judged
    every runtime: results are tied to a digest of the change; an edit makes them stale
RELEASE
  a pull request is opened only after every required gate passed
    every runtime: `route.py ready` exits non-zero
    with hooks: `gh pr create` is denied (not in the lean profile)
  what is merged is the version that was reviewed, when the project keeps review receipts
    every runtime: `route.py ready` writes a receipt named after the change's digest, committed with the change; `route.py verify`, run in CI, fails when the pull request's content has none
  a change that moves data, schema or infrastructure ships with a written rollout: order, verification, undo
    every runtime: `release.py check` blocks without a `## Rollout` section in the specification
    with hooks: `gh pr merge` is denied while it blocks (not in the lean profile)
  a change users will notice is in the changelog, when the project keeps one
    every runtime: `release.py check` carries a condition
OPERATE
  what happened after shipping is written down, and a failure names the risk nobody declared
    every runtime: `release.py record` appends to docs/releases.md; nothing forces it to be run
```

The security scan (`python3 .harness/bin/scan.py`) reads only the lines the change adds. A credential in a format a provider issues, or a private key, blocks the final gate; a line marked `gantry:allow` becomes a condition a person confirms. A value that may be a credential is a condition. A risky code pattern (dynamic code execution, unescaped markup, queries or shell commands built from strings, unsafe deserialization, disabled TLS verification, weak hashes, wildcard CORS) is not a verdict: it adds the `SECURITY` trigger, so the Security gate, which works from STRIDE, the OWASP Top 10, the CWE Top 25 and OWASP ASVS, reviews the change. The same scan reads added lines of runtime code for a query or request inside a loop and for a list read without a limit; either adds the `PERFORMANCE` trigger, so the Performance gate reviews the change.

"Every runtime" is what holds on any tool, because the router computes it. "With hooks" is what a runtime with command hooks adds by refusing the action when it is attempted; today that is Claude Code. A hook is a first barrier, not a boundary: a shell command can still write a file, which is why each guardrail also has a check at the final gate.

## Safety

The installer:

- preserves unrelated runtime configuration;
- manages one bounded block in `AGENTS.md`;
- tracks every installed harness-owned file and its SHA-256;
- refuses to overwrite unmanaged files without `--force`;
- refuses to overwrite locally modified harness files without `--force`;
- supports `plan`/dry-run;
- supports `doctor`;
- supports runtime-by-runtime uninstall;
- can purge shared core/skills after all runtimes are removed.

## CLI

```text
gantry init        guided install; --yes accepts what it proposes
gantry install     the same without questions; --runtime is required
gantry plan        what install would change
gantry upgrade     bring the installation to this version, keeping its choices
gantry doctor      check the installation and say how to fix it
gantry status      what is installed
gantry inspect     what the project is; --write saves it
gantry uninstall   remove runtimes; --purge-shared removes everything
```

## Architecture

```text
                            Gantry
                              │
                 shared portable installation
                    .harness/
                  .agents/skills/
                      AGENTS.md
                              │
       ┌──────────┬───────────┼──────────┬──────────┐
       ↓          ↓           ↓          ↓          ↓
    Claude      Codex       Cursor    OpenCode     OMP
   .claude/    .codex/     .cursor/   .opencode/  .omp/
```

Runtime adapters execute the same routing, handoff, blocking, re-review and Final Pre-PR contracts.

## Development

```bash
pip install "PyYAML>=6.0"
python3 tests/check_distribution.py   # structural integrity of distribution/
python3 tests/smoke_test.py           # install / doctor / uninstall round trip
python3 tests/test_cli.py             # guided install, upgrade and doctor
python3 tests/test_detect.py          # project detection
python3 tests/test_spec.py            # specification check
python3 tests/test_scan.py            # security scan of added lines
python3 tests/test_mutate.py          # mutation testing of added lines
python3 tests/test_release.py         # release gate and release record
python3 tests/test_eval_scoring.py    # scenario scorer
python3 tests/test_route.py           # deterministic router
python3 tests/test_hook.py            # pre-tool-use guard
```

`evals/` runs the routing scenarios against a real agent runtime; see [evals/README.md](evals/README.md).

Skills live once under `distribution/shared/skills/`. The installer renders them per runtime; do not add skill copies under `distribution/runtimes/`.

## Version

```text
1.0.0
```
