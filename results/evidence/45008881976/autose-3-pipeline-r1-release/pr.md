---
artefact: pr
issue: 3
round: 1
branch: autose/issue-3
pr: 8
pr_url: https://github.com/MittalManas2005/markdown/pull/8
head_sha: 96025e2f0a2dde761ef9b7b0821ae3ebe4f29205
ci: failure
---

# Release (stage 5)

PR: https://github.com/MittalManas2005/markdown/pull/8

## PR description

Fixes #3

Opened by **AutoSE** (round 1). An independent reviewer agent reviews this PR next; **a maintainer decides whether to merge**.

### Acceptance criteria (from the Requirements stage)
- AC-FR-001-1 [Confirmed] (no-error): Given input `# Heading {: id }` with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown`, then no exception is raised and HTML is returned.
- AC-FR-002-1 [Inferred] (contains): Given input `# Heading {: id }` with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown`, then the output contains `<h1 id="heading">`.
- AC-FR-002-2 [Inferred] (not-contains): Given input `# Heading {: id }` with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown`, then the output does not contain `<h1 id>`.
- AC-FR-002-3 [Inferred] (contains): Given input `[TOC]` followed by a blank line and `# Heading {: id }` with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown`, then the output contains `href="#heading"`.
- AC-FR-002-4 [Inferred] (property): Given input `# Heading {: id }` followed by a blank line and `# Heading` with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown`, then every `id` attribute value in the output is unique.
- AC-FR-002-5 [Inferred] (no-error): Given input `# Heading {: id="" }` with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown`, then no exception is raised. This holds under both readings of ASM-001.
- AC-FR-003-1 [Inferred] (contains): Given input `# Heading {: id="intro" }` with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown`, then the output contains `<h1 id="intro">`.
- AC-FR-003-2 [Inferred] (contains) (preservation): Given input `[TOC]` followed by a blank line and `# Heading {: id="intro" }` with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown`, then the output contains `href="#intro"`.
- AC-FR-004-1 [Confirmed] (exact): Given input `# Heading {: id }` with extensions `["attr_list"]`, when converted through `markdown.markdown`, then the output is `<h1 id>Heading</h1>`.

> Inferred criteria for the maintainer to confirm: AC-FR-002-1, AC-FR-002-2, AC-FR-002-3, AC-FR-002-4, AC-FR-002-5, AC-FR-003-1, AC-FR-003-2

### Files changed (planned by the Design stage)
`markdown/extensions/toc.py`, `docs/changelog.md`, `tests/test_syntax/extensions/test_toc.py`, `tests/test_syntax/extensions/test_attr_list.py`

### Tests
AutoSE test stage: PASS; tests run: 1181 (base: 1166).

Artifacts (spec, design, diff, test report): https://github.com/MittalManas2005/markdown/actions/runs/45008881976


## CI check runs on 96025e2f0a2dde761ef9b7b0821ae3ebe4f29205

| check | status | conclusion |
|---|---|---|
| validate-release | completed | skipped |
| test (py315, 3.15) | completed | success |
| lint (checklinks) | completed | success |
| test (py312) | completed | success |
| test (pygments) | completed | success |
| test (py311) | completed | success |
| lint (checkspelling) | completed | failure |
| lint (pep517check) | completed | success |
| test (py313) | completed | success |
| test (pypy311) | completed | success |
| test (py314) | completed | success |
| lint (flake8) | completed | success |
| check-for-entry | completed | success |
| validate-unreleased | completed | success |

## AutoSE stage check: the pull request is open and CI passes

Result: **FAIL** (CI: failure)
