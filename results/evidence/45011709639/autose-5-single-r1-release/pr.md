---
artefact: pr
issue: 5
round: 1
branch: autose/issue-5-single
pr: 15
pr_url: https://github.com/MittalManas2005/markdown/pull/15
head_sha: 351c7742c8b2aa709a3a67f606f3f14c614ce8e5
ci: success
---

# Release (stage 5)

PR: https://github.com/MittalManas2005/markdown/pull/15

## PR description

Fixes #5

Opened by **AutoSE** (round 1). An independent reviewer agent reviews this PR next; **a maintainer decides whether to merge**.

### Acceptance criteria (from the Requirements stage)
- AC-FR-001-1 [Inferred] (contains): Given the input "[TOC]", "", "# One", "", "## Two {: .notoc }", "", "## Three" with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown`, then the output contains `href="#three"`.
- AC-FR-001-2 [Inferred] (not-contains): Given the same input as AC-FR-001-1, when converted through `markdown.markdown`, then the output does not contain `href="#two"`.
- AC-FR-001-3 [Inferred] (not-contains): Given the input "[TOC]", "", "# One", "", "## Two {: .other .notoc }", "", "## Three" with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown`, then the output does not contain `href="#two"`.
- AC-FR-001-4 [Inferred] (contains): Given the input "[TOC]", "", "# One", "", "## Two {: .notoc }", "", "### Four", "", "## Three" with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown`, then the output contains `href="#four"`.
- AC-FR-002-1 [Inferred] (property): Given the input "[TOC]", "", "# One", "", "## Two {: .notoc }", "", "## Three" with extensions `["toc", "attr_list"]` on a `markdown.Markdown` instance, when converted with `md.convert`, then the `name` values of all entries in `md.toc_tokens`, including nested `children`, in document order equal `["One", "Three"]`.
- AC-FR-003-1 [Inferred] (contains): Given the input "[TOC]", "", "# One", "", "## Two {: .notoc }", "", "## Three" with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown`, then the output contains `id="two"`.
- AC-FR-003-2 [Inferred] (contains): Given the same input as AC-FR-003-1, when converted through `markdown.markdown`, then the output contains `>Two</h2>`.
- AC-FR-004-1 [Inferred] (property) (preservation): Given the input "# One", "", "## Two {: .other }", "", "## Three" with extensions `["toc", "attr_list"]` on a `markdown.Markdown` instance, when converted with `md.convert`, then the `name` values of all entries in `md.toc_tokens`, including nested `children`, in document order equal `["One", "Two", "Three"]`.
- AC-FR-004-2 [Inferred] (contains) (preservation): Given the input "[TOC]", "", "# One", "", "## Two {: .other }", "", "## Three" with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown`, then the output contains `href="#two"`.

> Inferred criteria for the maintainer to confirm: AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-001-4, AC-FR-002-1, AC-FR-003-1, AC-FR-003-2, AC-FR-004-1, AC-FR-004-2

### Files changed (planned by the Design stage)
`markdown/extensions/toc.py`, `tests/test_syntax/extensions/test_toc.py`, `docs/extensions/toc.md`, `docs/changelog.md`

### Tests
AutoSE test stage: PASS; tests run: 1175 (base: 1166).

Artifacts (spec, design, diff, test report): https://github.com/MittalManas2005/markdown/actions/runs/45011709639


## CI check runs on 351c7742c8b2aa709a3a67f606f3f14c614ce8e5

| check | status | conclusion |
|---|---|---|
| validate-release | completed | skipped |
| test (py314) | completed | success |
| lint (pep517check) | completed | success |
| lint (flake8) | completed | success |
| test (py312) | completed | success |
| test (py313) | completed | success |
| test (pypy311) | completed | success |
| lint (checkspelling) | completed | success |
| test (py315, 3.15) | completed | success |
| test (py311) | completed | success |
| test (pygments) | completed | success |
| lint (checklinks) | completed | success |
| check-for-entry | completed | success |
| validate-unreleased | completed | success |

## AutoSE stage check: the pull request is open and CI passes

Result: **PASS** (CI: success)
