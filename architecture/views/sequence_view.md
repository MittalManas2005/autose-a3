# Sequence view: one run from trigger to review

Status: **planned** (2026-11-22). The assignment asks for a sequence view of *one real run*. After the first complete run this file will be updated with the real run's ID, links, timings and any differences from the plan, and the planned version kept below it for comparison.

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
