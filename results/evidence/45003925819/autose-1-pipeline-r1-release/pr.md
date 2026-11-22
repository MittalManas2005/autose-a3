---
artefact: pr
issue: 1
round: 1
branch: autose/issue-1
pr: 2
pr_url: https://github.com/MittalManas2005/markdown/pull/2
head_sha: 3049d0f2577313f19c283f52fdb0a804b19ae997
ci: success
---

# Release (stage 5)

PR: https://github.com/MittalManas2005/markdown/pull/2

## PR description

Fixes #1

Opened by **AutoSE** (round 1). An independent reviewer agent reviews this PR next; **a maintainer decides whether to merge**.

### Acceptance criteria (from the Requirements stage)
- AC-FR-001-1 [Confirmed] (no-error): Given the input `# Heading {: data-toc-label }` with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown`, then no exception is raised and HTML is returned.
- AC-FR-002-1 [Inferred] (contains): Given the input `# Heading {: data-toc-label }` with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown`, then the output contains `<h1 id="heading">Heading</h1>`.
- AC-FR-002-2 [Inferred] (contains): Given the input `# Heading {: data-toc-label }` with extensions `["toc", "attr_list"]`, when converted with a `Markdown` instance and its `toc` attribute is read, then the `toc` output contains `<li><a href="#heading">Heading</a></li>`.
- AC-FR-002-3 [Inferred] (not-contains): Given the input `# Heading {: data-toc-label }` with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown`, then the output does not contain `data-toc-label`.
- AC-FR-002-4 [Inferred] (contains) (preservation): Given the input `# Heading {: data-toc-label="Short" }` with extensions `["toc", "attr_list"]`, when converted with a `Markdown` instance and its `toc` attribute is read, then the `toc` output contains `<li><a href="#heading">Short</a></li>`.

> Inferred criteria for the maintainer to confirm: AC-FR-002-1, AC-FR-002-2, AC-FR-002-3, AC-FR-002-4

### Files changed (planned by the Design stage)
`markdown/extensions/toc.py`, `docs/changelog.md`, `tests/test_syntax/extensions/test_toc.py`

### Tests
AutoSE test stage: PASS; tests run: 1172 (base: 1166).

Artifacts (spec, design, diff, test report): https://github.com/MittalManas2005/markdown/actions/runs/45003925819


## CI check runs on 3049d0f2577313f19c283f52fdb0a804b19ae997

| check | status | conclusion |
|---|---|---|
| validate-release | completed | skipped |
| test (pygments) | completed | success |
| lint (checkspelling) | completed | success |
| test (py312) | completed | success |
| test (py313) | completed | success |
| test (py311) | completed | success |
| test (py315, 3.15) | completed | success |
| test (py314) | completed | success |
| test (pypy311) | completed | success |
| lint (flake8) | completed | success |
| lint (checklinks) | completed | success |
| lint (pep517check) | completed | success |
| validate-unreleased | completed | success |
| check-for-entry | completed | success |

## AutoSE stage check: the pull request is open and CI passes

Result: **PASS** (CI: success)
