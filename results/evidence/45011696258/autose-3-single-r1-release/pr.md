---
artefact: pr
issue: 3
round: 1
branch: autose/issue-3-single
pr: 16
pr_url: https://github.com/MittalManas2005/markdown/pull/16
head_sha: 14bd05a76ed951de2dd416536ede189ad30f27eb
ci: success
---

# Release (stage 5)

PR: https://github.com/MittalManas2005/markdown/pull/16

## PR description

Fixes #3

Opened by **AutoSE** (round 1). An independent reviewer agent reviews this PR next; **a maintainer decides whether to merge**.

### Acceptance criteria (from the Requirements stage)
- AC-FR-001-1 [Confirmed] (no-error): Given `# Heading {: id }` with extensions `["toc", "attr_list"]`, when `markdown.markdown` is called, then no exception is raised and HTML is returned.
- AC-FR-001-2 [Inferred] (contains): Given `# Heading {: id }` with extensions `["toc", "attr_list"]`, when `markdown.markdown` is called, then the output contains `<h1 id="heading">Heading</h1>`.
- AC-FR-001-3 [Inferred] (contains): Given `# Heading {: id }` with extensions `["toc", "attr_list"]`, when `markdown.markdown` is called, then the output contains `<a href="#heading">Heading</a>` inside the table of contents.
- AC-FR-002-1 [Inferred] (contains) (preservation): Given `# Heading {: id="intro" }` with extensions `["toc", "attr_list"]`, when `markdown.markdown` is called, then the output contains `<h1 id="intro">Heading</h1>`.
- AC-FR-003-1 [Inferred] (contains): Given `# Heading {: id="" }` with extensions `["toc", "attr_list"]`, when `markdown.markdown` is called, then the output contains `<h1 id="heading">Heading</h1>`.

> Inferred criteria for the maintainer to confirm: AC-FR-001-2, AC-FR-001-3, AC-FR-002-1, AC-FR-003-1

### Files changed (planned by the Design stage)
`markdown/extensions/toc.py`, `docs/changelog.md`, `tests/test_syntax/extensions/test_toc.py`

### Tests
AutoSE test stage: PASS; tests run: 1171 (base: 1166).

Artifacts (spec, design, diff, test report): https://github.com/MittalManas2005/markdown/actions/runs/45011696258


## CI check runs on 14bd05a76ed951de2dd416536ede189ad30f27eb

| check | status | conclusion |
|---|---|---|
| validate-release | completed | skipped |
| test (pypy311) | completed | success |
| lint (checkspelling) | completed | success |
| lint (checklinks) | completed | success |
| lint (pep517check) | completed | success |
| test (py315, 3.15) | completed | success |
| test (py311) | completed | success |
| test (py314) | completed | success |
| test (py312) | completed | success |
| test (py313) | completed | success |
| test (pygments) | completed | success |
| lint (flake8) | completed | success |
| check-for-entry | completed | success |
| validate-unreleased | completed | success |

## AutoSE stage check: the pull request is open and CI passes

Result: **PASS** (CI: success)
