---
artefact: pr
issue: 7
round: 1
branch: autose/issue-7
pr: 12
pr_url: https://github.com/MittalManas2005/markdown/pull/12
head_sha: 692b5de2883be3be7b73e4a74f1077f6580ebf21
ci: success
---

# Release (stage 5)

PR: https://github.com/MittalManas2005/markdown/pull/12

## PR description

Fixes #7

Opened by **AutoSE** (round 1). An independent reviewer agent reviews this PR next; **a maintainer decides whether to merge**.

### Acceptance criteria (from the Requirements stage)
- AC-FR-001-1 [Inferred] (contains): Given input `[`code`][ref]` followed by a blank line and `[ref]: /url`, with no extensions, when converted through the public API, then the output contains `<a href="/url"><code>code</code></a>`.
- AC-FR-001-2 [Inferred] (contains): Given input `[`code`]` followed by a blank line and `[`code`]: /url`, with no extensions, when converted through the public API, then the output contains `<a href="/url"><code>code</code></a>`.
- AC-FR-002-1 [Inferred] (contains) (preservation): Given input `[`code`](/url)` with no extensions, when converted through the public API, then the output contains `<a href="/url"><code>code</code></a>`.
- AC-FR-002-2 [Inferred] (contains) (preservation): Given input `[text][ref]` followed by a blank line and `[ref]: /url`, with no extensions, when converted through the public API, then the output contains `<a href="/url">text</a>`.
- AC-NFR-001-1 [Inferred] (contains) (preservation): Given input `[`<b>x</b>`](/url)` with no extensions, when converted through the public API, then the output contains `<code>&lt;b&gt;x&lt;/b&gt;</code>`.

> Inferred criteria for the maintainer to confirm: AC-FR-001-1, AC-FR-001-2, AC-FR-002-1, AC-FR-002-2, AC-NFR-001-1

### Files changed (planned by the Design stage)
`markdown/inlinepatterns.py`, `markdown/treeprocessors.py`, `docs/changelog.md`, `tests/test_syntax/inline/test_links.py`

### Tests
AutoSE test stage: PASS; tests run: 1179 (base: 1166).

Artifacts (spec, design, diff, test report): https://github.com/MittalManas2005/markdown/actions/runs/45010344467


## CI check runs on 692b5de2883be3be7b73e4a74f1077f6580ebf21

| check | status | conclusion |
|---|---|---|
| validate-release | completed | skipped |
| test (py311) | completed | success |
| lint (flake8) | completed | success |
| test (py313) | completed | success |
| lint (pep517check) | completed | success |
| lint (checkspelling) | completed | success |
| test (py314) | completed | success |
| test (py315, 3.15) | completed | success |
| test (pypy311) | completed | success |
| test (pygments) | completed | success |
| validate-unreleased | completed | success |
| test (py312) | completed | success |
| check-for-entry | completed | success |
| lint (checklinks) | completed | success |

## AutoSE stage check: the pull request is open and CI passes

Result: **PASS** (CI: success)
