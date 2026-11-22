---
artefact: pr
issue: 3
round: 1
branch: autose/issue-3
pr: 8
pr_url: https://github.com/MittalManas2005/markdown/pull/8
head_sha: a0d32f65fe4620d46379fb403255c1acb4c747d5
ci: success
---

# Release (stage 5)

PR: https://github.com/MittalManas2005/markdown/pull/8

## PR description

Fixes #3

Opened by **AutoSE** (round 1). An independent reviewer agent reviews this PR next; **a maintainer decides whether to merge**.

### Acceptance criteria (from the Requirements stage)
- AC-FR-001-1 [Confirmed] (no-error): Given input `# Heading {: id }` with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown()`, then no exception is raised and an HTML string is returned.
- AC-FR-002-1 [Inferred] (exact): Given input `# Heading {: id }` with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown()`, then the output equals `<h1 id="heading">Heading</h1>`.
- AC-FR-002-2 [Inferred] (contains): Given input consisting of the line `[TOC]`, a blank line, and the line `# Heading {: id }`, with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown()`, then the output contains `<a href="#heading">Heading</a>`.
- AC-FR-002-3 [Inferred] (property): Given input `# Heading {: id }` with a `markdown.Markdown` instance configured with `TocExtension()` and `attr_list`, when converted and `toc_tokens` is read, then `toc_tokens` contains exactly one top-level token whose `id` is `heading` and whose `name` is `Heading`.
- AC-FR-002-4 [Inferred] (exact): Given input `# Heading {: id="" }` with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown()`, then the output equals `<h1 id="heading">Heading</h1>`. Basis: ASM-001 (empty-string case, to be confirmed).
- AC-FR-003-1 [Inferred] (exact) (preservation): Given input `# Heading {: id="intro" }` with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown()`, then the output equals `<h1 id="intro">Heading</h1>`.
- AC-FR-003-2 [Inferred] (contains) (preservation): Given input consisting of the line `[TOC]`, a blank line, and the line `# Heading {: id="intro" }`, with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown()`, then the output contains `<a href="#intro">Heading</a>`.
- AC-FR-004-1 [Confirmed] (exact) (preservation): Given input `# Heading {: id }` with extensions `["attr_list"]`, when converted through `markdown.markdown()`, then the output equals `<h1 id>Heading</h1>`.

> Inferred criteria for the maintainer to confirm: AC-FR-002-1, AC-FR-002-2, AC-FR-002-3, AC-FR-002-4, AC-FR-003-1, AC-FR-003-2

### Files changed (planned by the Design stage)
`markdown/extensions/toc.py`, `docs/changelog.md`, `tests/test_syntax/extensions/test_toc.py`

### Tests
AutoSE test stage: PASS; tests run: 1179 (base: 1166).

Artifacts (spec, design, diff, test report): https://github.com/MittalManas2005/markdown/actions/runs/45010351338


## CI check runs on a0d32f65fe4620d46379fb403255c1acb4c747d5

| check | status | conclusion |
|---|---|---|
| validate-release | completed | skipped |
| test (py312) | completed | success |
| test (py315, 3.15) | completed | success |
| lint (checkspelling) | completed | success |
| test (py314) | completed | success |
| test (pygments) | completed | success |
| test (py311) | completed | success |
| lint (checklinks) | completed | success |
| lint (flake8) | completed | success |
| test (py313) | completed | success |
| test (pypy311) | completed | success |
| lint (pep517check) | completed | success |
| validate-unreleased | completed | success |
| check-for-entry | completed | success |

## AutoSE stage check: the pull request is open and CI passes

Result: **PASS** (CI: success)
