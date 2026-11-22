# Component view: AutoSE

Status: **design** (2026-11-22, before implementation). It describes the system as decided in ADR-001 … ADR-011 and is updated if an ADR is superseded.

Where things live:
- **Fork** [`MittalManas2005/markdown`](https://github.com/MittalManas2005/markdown): the workflow, the agent code and prompts, and a bundled copy of `ARCHITECTURE.md`.
- **Submission repository** `autose-a3` (private until grading): documentation, a copy of the workflow and agent code, issues, hidden tests, results.

## Diagram

```mermaid
flowchart TB
  subgraph GH[GitHub: fork MittalManas2005/markdown]
    ISSUE[(Issue + comments)]
    PR[(Pull request)]
    CI[Upstream CI workflows<br/>tox.yml, changelog-enforcer, ...]
  end

  subgraph WF[".github/workflows/autose.yml (+ reusable autose-round.yml)"]
    GATE["Job gate<br/>deterministic · contents: read, issues: read<br/>authorize sender, parse command, choose mode"]
    subgraph BUILD["Job build (per round) · contents: read · NO GitHub write token"]
      ORCH{{"Orchestrator<br/>Python state machine<br/>budgets, transitions, checks"}}
      REQ["Requirements agent<br/>Haiku · adapted A1 skill<br/>Read/Grep/Glob"]
      DES["Design agent<br/>Haiku · reads bundled ARCHITECTURE.md<br/>Read/Grep/Glob"]
      IMP["Implementer agent<br/>Haiku · Edit markdown/**, tests/**, docs/**<br/>Bash: compile + unittest"]
      TST["Tester agent<br/>Haiku · Edit tests/** · Bash: unittest"]
      CHK["Deterministic checks<br/>spec parser · design validator · diff guard ·<br/>build/flake8 · test runner · AC coverage"]
    end
    REL["Job release (per round)<br/>deterministic, no LLM<br/>GitHub App token: contents + pull-requests write"]
    REV["Job review (per round)<br/>fresh runner · contents: read, pull-requests: write<br/>(GITHUB_TOKEN = github-actions bot)"]
    REVA["Reviewer agent<br/>Sonnet · Read/Grep/Glob · Bash: unittest, flake8, python -c<br/>sees issue + diff + PR head only"]
    REPORT["Job report<br/>issues: write · status comment"]
  end

  ISSUE -- "label autose / '/autose' comment" --> GATE
  GATE --> ORCH
  ORCH --> REQ --> CHK
  ORCH --> DES --> CHK
  ORCH --> IMP --> CHK
  ORCH --> TST --> CHK
  CHK --> ORCH
  ORCH -- "artifacts: spec.md, design.md, diff.patch,<br/>test_report.md, run_state.json, usage.json" --> REL
  REL -- "push autose/issue-N, open/update PR, pr.md" --> PR
  PR -- "pull_request event (App identity)" --> CI
  CI -- "check runs on head SHA" --> REL
  REL --> REV
  REV --> REVA
  REVA -- "verdict.json + review.md" --> REV
  REV -- "APPROVE / REQUEST_CHANGES review" --> PR
  REV -- "changes requested & rounds left" --> ORCH
  REPORT -- "status + links" --> ISSUE
```

## Components

| Component | Kind | Model / runtime | Tools and permissions | Produces |
|---|---|---|---|---|
| Gate job | deterministic | bash + `gh` | `contents: read`, `issues: read` | mode (`full`, `resume`, `review-only`), issue number, round settings |
| Orchestrator | deterministic | Python 3.12 | runs the agents through `claude -p`, runs the checks, applies the transition table and budgets | `run_state.json`, `usage.json`, stage artifacts |
| Requirements agent | LLM | Claude Haiku, effort medium | Read, Grep, Glob; follows the adapted A1 skill (`autose/skills/requirements-spec-builder.md`) | `spec.md` (PASS / NEEDS_INPUT / FAIL) |
| Design agent | LLM | Claude Haiku, effort medium | Read, Grep, Glob; reads `autose/context/ARCHITECTURE.md` | `design.md` |
| Implementer agent | LLM | Claude Haiku, effort medium | Read, Grep, Glob, Edit/Write limited to `markdown/**`, `tests/**`, `docs/**`; Bash limited to compile and test commands | working-tree change → `diff.patch` |
| Tester agent | LLM | Claude Haiku, effort medium | Read, Grep, Glob, Edit/Write limited to `tests/**`; Bash limited to test commands | AC tests (inside `diff.patch`), input to `test_report.md` |
| Checks | deterministic | Python | spec parser, design validator (AST), diff guard, build + flake8, `unittest` runner (clean environment), AC-coverage, fail-on-base | pass/fail + reasons into the stage artifacts |
| Release job | deterministic | bash + `gh` + GitHub App token | `contents: write`, `pull-requests: write` (App installation token, 1 h lifetime) | branch `autose/issue-N`, PR, `pr.md`, CI result |
| Review job | deterministic shell + LLM | — | `contents: read`, `pull-requests: write` via `GITHUB_TOKEN` | posts the review |
| Reviewer agent | LLM | Claude Sonnet, effort medium | Read, Grep, Glob; Bash limited to `python -m unittest`, `python -m flake8`, `python -c`; no edits, no git, no `gh` | `review.md`, `verdict.json`, session transcript |
| Report job | deterministic | `gh` | `issues: write` | one status comment on the issue with links and the run ID |
| Upstream CI | existing workflows in the fork | — | unchanged upstream configuration | check runs on the PR head commit |

## Interactions that are deliberately absent
- No agent receives a GitHub token with write access. All GitHub writes happen in deterministic steps (ADR-005, ADR-012).
- The review job never downloads build artifacts (`spec.md`, `design.md`, `test_report.md`) and never reads the PR description (ADR-003, ADR-013).
- No agent has web access, and no token in the fork can read `autose-a3`, where the hidden tests live (ADR-012).
- Commands an agent runs (tests, `python -c` probes) get no Claude credentials: Claude Code removes them from their environment (`CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1`, ADR-012). Each agent's session transcript is kept in its job's artifact.
