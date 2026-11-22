---
artefact: pr
issue: 25
round: 1
branch: autose/issue-25
pr: 26
pr_url: https://github.com/MittalManas2005/markdown/pull/26
head_sha: 291c2e4a788b88888a726433b43605d1d615ce32
ci: success
---

# Release (stage 5)

PR: https://github.com/MittalManas2005/markdown/pull/26

## PR description

Fixes #25

Opened by **AutoSE** (round 1). An independent reviewer agent reviews this PR next; **a maintainer decides whether to merge**.

### Acceptance criteria (from the Requirements stage)
- AC-FR-001-1 [Confirmed] (no-error): Given the input `## Setup {: data-toc-label }` with extensions ["toc", "attr_list"], when converted through the public API `markdown.markdown`, then no exception is raised and HTML is produced.
- AC-FR-001-2 [Confirmed] (property): Given the input `## Setup {: data-toc-label }` with extensions ["toc", "attr_list"], when converted through the public API and the resulting `toc_tokens` are read, then the list has one entry and that entry's `name` is "Setup".
- AC-FR-001-3 [Inferred] (contains): Given the input `## Setup {: data-toc-label }` with extensions ["toc", "attr_list"], when converted through the public API, then the output contains `<h2 id="setup">Setup</h2>`. Basis: the ID is derived from the heading text when none is set (EV-001); the attribute is not part of the header HTML (EV-003). Confirm the exact header markup on the pull request.
- AC-FR-001-4 [Inferred] (contains): Given the input `[TOC]` followed by a blank line and `## Setup {: data-toc-label }`, with extensions ["toc", "attr_list"], when converted through the public API, then the output contains `href="#setup"`. Basis: the TOC links to the heading ID (EV-001); the issue gives no TOC markup, so this fragment is the agent's choice. Confirm on the pull request.
- AC-FR-002-1 [Inferred] (property) (preservation): Given the input `## Setup { data-toc-label='Custom' }` with extensions ["toc", "attr_list"], when converted through the public API and the resulting `toc_tokens` are read, then that entry's `name` is "Custom".
- AC-FR-002-2 [Inferred] (contains) (preservation): Given the input `## Setup { data-toc-label='Custom' }` with extensions ["toc", "attr_list"], when converted through the public API, then the output contains `<h2 id="setup">Setup</h2>`.

> Inferred criteria for the maintainer to confirm: AC-FR-001-3, AC-FR-001-4, AC-FR-002-1, AC-FR-002-2

### Files changed (planned by the Design stage)
`markdown/extensions/toc.py`, `docs/changelog.md`, `tests/test_syntax/extensions/test_toc.py`

### Tests
AutoSE test stage: PASS; tests run: 1174 (base: 1166).

Artifacts (spec, design, diff, test report): https://github.com/MittalManas2005/markdown/actions/runs/45018151643


## CI check runs on 291c2e4a788b88888a726433b43605d1d615ce32

| check | status | conclusion |
|---|---|---|
| validate-release | completed | skipped |
| test (py312) | completed | success |
| test (py313) | completed | success |
| test (py314) | completed | success |
| test (py311) | completed | success |
| test (pypy311) | completed | success |
| lint (pep517check) | completed | success |
| test (pygments) | completed | success |
| lint (checkspelling) | completed | success |
| lint (flake8) | completed | success |
| test (py315, 3.15) | completed | success |
| check-for-entry | completed | success |
| validate-unreleased | completed | success |
| lint (checklinks) | completed | success |

## AutoSE stage check: the pull request is open and CI passes

Result: **PASS** (CI: success)
