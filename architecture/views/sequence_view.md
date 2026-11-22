# Sequence view: one real run from trigger to review

**Real run:** issue [#6](https://github.com/MittalManas2005/markdown/issues/6) "Command line: add an option to set `tab_length`", baseline attempt 2. Details:
- run [45010360150](https://github.com/MittalManas2005/markdown/actions/runs/45010360150);
- PR [#9](https://github.com/MittalManas2005/markdown/pull/9);
- base commit `ca2d6d3`;
- 22 November 2026, 10:01–10:10 UTC.

The run was started by a maintainer comment `/autose` (a re-run after attempt 1 stopped at CI). Timings come from the job log and `run_state.json`; turns and tokens come from `usage.json`. The evidence is in `results/evidence/45010360150/`.

This run includes one real backward loop: the stage 4 spell check rejected a word in the tester's docstrings, and the tester was sent back once.

```mermaid
sequenceDiagram
  autonumber
  actor M as Maintainer
  participant GH as GitHub (fork)
  participant G as gate job
  participant O as build job: orchestrator
  participant RQ as Requirements (Haiku)
  participant DS as Design (Haiku)
  participant IM as Implementer (Haiku)
  participant TS as Tester (Haiku)
  participant RL as release job (GitHub App)
  participant CI as upstream CI
  participant RV as review job: Reviewer (Sonnet)

  M->>GH: comment "/autose" on issue #6 (10:01:23)
  GH->>G: issue_comment.created
  G->>GH: sender permission = admin; last status marker = stopped_ci
  G->>O: mode=full, issue=6, base=ca2d6d3 (10:01:33)
  Note over O: sandbox self-test ok; agents denied git, web, gh; origin remote removed
  O->>RQ: issue (untrusted file) + A1 skill v1.3.1
  RQ-->>O: spec.md: 5 FRs, 8 ACs, status PASS (11 turns, 17.9k out)
  O->>O: check 1 (spec testable): PASS (10:03:10)
  O->>DS: issue + spec + bundled ARCHITECTURE.md + repo
  DS-->>O: design.md: files and functions (23 turns, 16.5k out)
  O->>O: check 2 (files and functions exist, AST): PASS (10:04:21)
  O->>IM: spec + design + repo
  IM-->>O: markdown/__main__.py, docs (28 turns, 10.5k out)
  O->>O: check 3 (diff guard, compile, flake8, spelling): PASS (10:05:10)
  O->>TS: spec + changed repo
  TS-->>O: tests for 8 ACs (14 turns, 10.7k out)
  O->>O: check 4: coverage, fail-on-base, suite OK, spelling FAIL ("STDIN") (10:06:03)
  O->>TS: test_feedback.md (back to the tester)
  TS-->>O: docstrings fixed (13 turns, 4.5k out)
  O->>O: check 4: PASS (10:06:33)
  O->>RL: build artifact (spec, design, diff.patch, test_report, run_state, usage, transcripts)
  RL->>GH: re-apply diff, diff guard, push autose/issue-6, update PR #9 (App token)
  GH->>CI: pull_request.synchronize
  CI-->>RL: 13 checks pass, 1 skipped (check 5) (10:09:19)
  RL->>RV: PR 9
  RV->>GH: read issue #6 body + diff; check out PR head; trusted AutoSE code from main (python -P)
  RV->>RV: ran 3 commands (unittest suite + probes): all ok (8 turns, 1.3k out)
  RV->>RV: transcript shows a passing unittest run, so approve is valid (ADR-013)
  RV->>GH: APPROVED review as github-actions[bot] (10:09:59)
  GH-->>M: status comment "approved", run and PR links (10:10:17); maintainer decides whether to merge
```

## Differences from the planned view (below)
| Planned | Real run | Why |
|---|---|---|
| Check 3: install, compile, flake8 | Check 3 also runs the repository's spell check on changed code and docs | Baseline attempt 1 failed CI on spelling (ADR-012 note; `checks.check_spelling`) |
| Check 4: coverage, fail-on-base, suite | Check 4 also spell-checks the new tests; a failure goes back to the **tester**, not the implementer | Same; the loop in this run is exactly this case |
| Review job checks out the PR head | It also runs AutoSE's own code from a trusted copy of `main`, never from the PR branch | ADR-014 |
| Reviewer "reads, runs tests" | The approval is accepted only if the reviewer's session transcript contains a passing unittest run | ADR-013 |
| Agents run commands with the plan's credentials | Agent commands run in Claude Code's sandbox without credentials; agents are denied `git` | ADR-012 and its updates |
| Started by a label | This re-run was started by a `/autose` comment. The first attempt (run 45008931950) was started by the label and stopped at stage 5 | Attempt 1 is reported in `results/runs.md` |

## Planned version (2026-11-22, before any run), kept for comparison

```mermaid
sequenceDiagram
  autonumber
  actor M as Maintainer
  participant GH as GitHub (fork)
  participant G as gate job
  participant O as build job: orchestrator
  participant RQ as Requirements agent (Haiku)
  participant DS as Design agent (Haiku)
  participant IM as Implementer agent (Haiku)
  participant TS as Tester agent (Haiku)
  participant RL as release job (GitHub App)
  participant CI as upstream CI
  participant RV as review job + Reviewer (Sonnet)

  M->>GH: add label "autose" to issue #N
  GH->>G: issues.labeled
  G->>GH: check sender permission, read issue via API (to a file)
  G->>O: mode=full, issue=#N, round=1
  O->>RQ: issue (untrusted) + A1 skill
  RQ-->>O: spec.md
  O->>O: check 1: spec parses, status PASS, every AC testable
  O->>DS: issue + spec.md + ARCHITECTURE.md + repo
  DS-->>O: design.md
  O->>O: check 2: files and functions exist (AST)
  O->>IM: spec.md + design.md + repo
  IM-->>O: working-tree changes
  O->>O: check 3: diff guard, install, compile, flake8
  O->>TS: spec.md + changed repo
  TS-->>O: AC tests
  O->>O: check 4: AC coverage, fail-on-base, full suite
  alt tests fail and retries left
    O->>IM: failing-test excerpt (back to stage 3)
  end
  O->>RL: artifacts (spec, design, diff.patch, test_report, run_state, usage)
  RL->>GH: push autose/issue-N, open PR with pr.md (App identity)
  GH->>CI: pull_request event
  CI-->>RL: check runs succeed (check 5)
  RL->>RV: PR number, head SHA
  RV->>GH: read issue + diff, check out PR head
  RV->>RV: Reviewer reads, runs tests, probes edge cases
  RV->>GH: post review (APPROVE or REQUEST_CHANGES) as github-actions[bot]
  alt changes requested and send-backs left (≤ 2)
    RV->>O: round 2 starts at the named stage with the findings
  end
  GH-->>M: status comment with links; maintainer decides whether to merge
```
