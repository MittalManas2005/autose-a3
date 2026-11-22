---
artefact: pr
issue: 7
round: 1
branch: autose/issue-7-single
pr: 18
pr_url: https://github.com/MittalManas2005/markdown/pull/18
head_sha: f8b03c32005648c7994ac2737aab364750dba82b
ci: success
---

# Release (stage 5)

PR: https://github.com/MittalManas2005/markdown/pull/18

## PR description

Fixes #7

Opened by **AutoSE** (round 1). An independent reviewer agent reviews this PR next; **a maintainer decides whether to merge**.

### Acceptance criteria (from the Requirements stage)
- AC-FR-001-1 [Inferred] (contains): Given input "[`code`]" followed by a blank line and "[`code`]: http://example.com" with default settings, when converted through `markdown.markdown`, then the output contains `<a href="http://example.com"><code>code</code></a>`.
- AC-FR-001-2 [Inferred] (contains): Given input "[`code`][]" followed by a blank line and "[`code`]: http://example.com" with default settings, when converted through `markdown.markdown`, then the output contains `<a href="http://example.com"><code>code</code></a>`.
- AC-FR-001-3 [Inferred] (contains) (preservation): Given input "[`code`](http://example.com)" with default settings, when converted through `markdown.markdown`, then the output contains `<a href="http://example.com"><code>code</code></a>` (EV-005).
- AC-FR-001-4 [Inferred] (contains) (preservation): Given input "[`code`]" with no matching reference definition, when converted through `markdown.markdown`, then the output contains `[<code>code</code>]` and does not contain `<a `.

> Inferred criteria for the maintainer to confirm: AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-001-4

### Files changed (planned by the Design stage)
`markdown/inlinepatterns.py`, `tests/test_syntax/inline/test_links.py`, `docs/changelog.md`

### Tests
AutoSE test stage: PASS; tests run: 1170 (base: 1166).

Artifacts (spec, design, diff, test report): https://github.com/MittalManas2005/markdown/actions/runs/45011722169


## CI check runs on f8b03c32005648c7994ac2737aab364750dba82b

| check | status | conclusion |
|---|---|---|
| validate-release | completed | skipped |
| test (pypy311) | completed | success |
| test (pygments) | completed | success |
| test (py314) | completed | success |
| test (py313) | completed | success |
| test (py312) | completed | success |
| check-for-entry | completed | success |
| test (py315, 3.15) | completed | success |
| lint (checklinks) | completed | success |
| test (py311) | completed | success |
| lint (checkspelling) | completed | success |
| lint (pep517check) | completed | success |
| lint (flake8) | completed | success |
| validate-unreleased | completed | success |

## AutoSE stage check: the pull request is open and CI passes

Result: **PASS** (CI: success)
