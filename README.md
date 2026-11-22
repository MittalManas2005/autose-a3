# AutoSE: from a GitHub issue to a tested, independently reviewed pull request

AutoSE is a multi-agent system that runs in GitHub Actions. A maintainer labels an issue; AutoSE then:
1. writes a testable spec;
2. plans the change against the real code;
3. implements it;
4. writes and runs acceptance tests;
5. opens a pull request and waits for the project's CI;
6. has an independent reviewer approve it or send it back.

Code checks every stage before it hands over. **AutoSE never merges:** a person decides.

| | |
|---|---|
| **Target repository (fork)** | [MittalManas2005/markdown](https://github.com/MittalManas2005/markdown), a fork of [Python-Markdown/markdown](https://github.com/Python-Markdown/markdown) |
| **Pinned commit** | `3f2c5510bd8d64a73ec18342f740371bcde9b20c` (3.11.2-10-g3f2c551). Fork `main` is this commit plus AutoSE's own files (`autose/`, `.github/workflows/autose*.yml`); `markdown/`, `tests/`, `docs/` and the upstream CI are byte-identical to the pin. |
| **Models** | Claude Haiku (`claude-haiku-5-5`) for Requirements, Design, Implementer, Tester and the single-agent variant. **Reviewer:** Claude Sonnet (`claude-sonnet-5-5`) in the baseline and E1 runs; Claude Haiku by default since [ADR-015](architecture/decisions/ADR-015.md), with Sonnet still selectable. Effort `medium` everywhere. |
| **Agent runtime** | Claude Code CLI 2.1.319, headless (`claude -p`), driven by a Python orchestrator; Claude Pro subscription via `CLAUDE_CODE_OAUTH_TOKEN` |
| **Report** | [`report.pdf`](report.pdf) |
| **Demo** | [Demo video (OneDrive folder)](https://iiithydresearch-my.sharepoint.com/:f:/g/personal/manas_mittal_research_iiit_ac_in/IgBBBr3TTEn4Q4LBgxDO9E7wAZs1QewfuO216DN1abJWD9Y?e=9FMSfE) |

## How to trigger a run (in the fork)
| Action | Who | What happens |
|---|---|---|
| Add the label **`autose`** to an issue | anyone with write access | A full run: stages 1–6 |
| Comment **`/autose`** on an issue | write access (OWNER / MEMBER / COLLABORATOR) | Starts a full run. If the last run stopped with a question (`needs input`), it **resumes**, using the text after `/autose` as the maintainer's answer. |
| Comment **`/autose`** on a pull request | write access; the PR branch must be in the fork | **Review only:** stage 6 on that PR |
| **Actions → AutoSE → Run workflow** | write access | Same, with experiment inputs: `mode` (`full` / `review-only`), `variant` (`pipeline` / `single`), `reviewer_model` (`haiku` / `sonnet`) |

Each run posts a status comment on the issue (or PR), with links to the run and the PR. The PR is opened by the GitHub App `autose-release-mm2005`; the review is posted by `github-actions[bot]`. All stage artifacts (`spec.md`, `design.md`, `diff.patch`, `test_report.md`, `pr.md`, `review.md`, token usage, agent transcripts) are attached to the run.

**Running it in another fork requires:**
- repository secret `CLAUDE_CODE_OAUTH_TOKEN`;
- a GitHub App with *Contents* and *Pull requests* write access only, installed on the fork, with its ID in variable `AUTOSE_APP_ID` and its private key in secret `AUTOSE_APP_PRIVATE_KEY`;
- the setting "Allow GitHub Actions to create and approve pull requests";
- the files from `workflow/`, copied with `workflow/sync_to_fork.sh <fork-clone>`.

## The design in one table
| Stage | Agent | Artifact | Check (decided by code) |
|---|---|---|---|
| 1 Requirements | Requirements agent (adapted A1 skill, [`a1_skill.md`](a1_skill.md)) | `spec.md` | Every acceptance criterion has an ID, an oracle kind and Given/When/Then; status PASS, or stop and ask |
| 2 Design | Design agent (reads [`ARCHITECTURE.md`](ARCHITECTURE.md) and verifies it against the code) | `design.md` | Every named file and function exists (AST) |
| 3 Implementation | Implementer agent | `diff.patch` | Diff guard (allowed paths, no deleted tests, changelog entry), compile, import, flake8, spelling |
| 4 Testing | Tester agent | `test_report.md` | One test per criterion; new tests fail on the old code; full suite passes; spelling |
| 5 Release | Plain code (GitHub App) | `pr.md` + PR | PR open and the project's CI green |
| 6 Review | Independent reviewer, in its own job | `review.md` | Valid verdict; an approval needs a passing test run in the reviewer's own transcript; at most 2 send-backs |

Details: [`architecture/views/`](architecture/views/) (component view, stage map, sequence view of a real run) and 16 ADRs in [`architecture/decisions/`](architecture/decisions/). Three of them were superseded on evidence from real runs: ADR-006 → ADR-015, ADR-008 → ADR-013, ADR-009 → ADR-012.

## Repository layout
| Path | Content |
|---|---|
| `ARCHITECTURE.md` | Architecture of the target (Python-Markdown at the pinned commit): 8 components, 4 ADRs, 5 constraints, 88 source references verified |
| `a1_skill.md` | The A1 requirements skill, adapted for stage 1 (v1.3.1; the original v1.2 is in the git history) |
| `architecture/` | AutoSE's own design: views, ADR-001 … ADR-016, and the decision briefs the ADRs were chosen from |
| `workflow/` | Copy of `.github/workflows/autose*.yml` and all agent code and prompts (`autose/`), the tests (`autose/tests/`, 49 tests) and `sync_to_fork.sh` |
| `experiment/issues/` | The 5 evaluation issues (2 bugs, 2 features, 1 vague), the scripted maintainer answers, and the smoke-test issue |
| `experiment/hidden_tests/` | 18 hidden acceptance tests, the reference fixes, and scripts that validate them (fail at the pin, pass with the reference fix) |
| `experiment/seeded_prs/` | 5 reviewer-check PRs (patches and ground-truth labels) |
| `experiment/variants.md` | Protocol of the two decision experiments, fixed before any run |
| `results/` | `results.csv`, `runs.md` (every run with links, stage pass rates, total tokens), `e2_scoring.csv`, mirrored evidence per run, and `collect_results.py`, which rebuilds them from the run artifacts |

## Results at a glance
Full data, with links to every run, PR and review, is in [`results/runs.md`](results/runs.md).
- **Baseline, attempt 2:** all 5 issues ended with an approved PR. **17 of 18 hidden tests pass.** The miss (#7, the vague issue) led to [ADR-016](architecture/decisions/ADR-016.md).
- **Baseline, attempt 1:** stopped on two system defects, both fixed and reported: a spec-format mismatch, and CI spelling.
- **E1 (5 roles vs one agent):** equal hidden-test results; −5% total tokens for the single agent but more check failures, no clarifying question, and a leftover debug file. ADR-001 stands.
- **E2 (reviewer model):** Sonnet and Haiku each caught 4/4 seeded defects with 0 false verdicts; Haiku found one extra real bug and is about 6.5× cheaper. ADR-006 superseded by ADR-015.

## AI-use disclosure
This assignment was done with substantial AI assistance from Claude Code (Claude Opus 5.5) as an architect and mentor, at my direction. The assistance covered:
- the analysis of the assignment;
- drafting `ARCHITECTURE.md`, the decision briefs, the ADR texts and the views;
- writing the AutoSE code, prompts and tests;
- the hidden tests, reference fixes and seeded PRs;
- running and monitoring the experiments;
- drafting this README and the report.

**Every architectural decision was mine.** For each ADR the assistant prepared options with trade-offs, and I chose; where I disagreed or changed a proposal, the ADR records my decision. I made every commit to this repository and to the fork's `main` myself. The assistant carried out some GitHub actions under my account, each only after my explicit approval:
- opening the evaluation issues;
- adding labels and posting `/autose` comments;
- dispatching experiment runs;
- pushing the seeded-PR branches and opening their PRs;
- applying branch protection. Every run, PR and review cited here is real and linked. No result was edited by hand: the result tables are generated from the runs' artifacts by `results/collect_results.py`.
