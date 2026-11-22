---
artefact: pr
issue: 7
round: 1
branch: autose/issue-7
pr: 12
pr_url: https://github.com/MittalManas2005/markdown/pull/12
head_sha: d550cadbe0a34d9643f27ef763d1cda520a56539
ci: success
---

# Release (stage 5)

PR: https://github.com/MittalManas2005/markdown/pull/12

## PR description

Fixes #7

Opened by **AutoSE** (round 1). An independent reviewer agent reviews this PR next; **a maintainer decides whether to merge**.

### Acceptance criteria (from the Requirements stage)
- AC-FR-001-2 [Inferred] (contains) (preservation): Given input `[plain](https://example.com)` with no extensions, when converted through the public API, then the output contains `<a href="https://example.com">plain</a>`. Basis: general inline link behaviour, carried unchanged from v0.1 (EV-004 not re-read; kept as preservation for this FR).
- AC-FR-001-3 [Inferred] (contains): Given the document `[`foo`]` followed by a blank line and the definition `[`foo`]: https://example.com`, with no extensions, when converted through the public API, then the output contains `<a href="https://example.com"><code>foo</code></a>`. Basis: shortcut form named in ANS-001; expected link text follows the documented code-in-label form (EV-003).
- AC-FR-001-4 [Inferred] (contains): Given the document `[text][`foo`]` followed by a blank line and the definition `[`foo`]: https://example.com`, with no extensions, when converted through the public API, then the output contains `<a href="https://example.com">text</a>`. Basis: full form named in ANS-001; the link text is the bracketed `text`.
- AC-FR-001-5 [Inferred] (contains) (preservation): Given the document `[text][foo]` followed by a blank line and the definition `[foo]: https://example.com`, with no extensions, when converted through the public API, then the output contains `<a href="https://example.com">text</a>`. Basis: plain reference link behaviour that must not regress; no existing test was read in this stage (EV-007 found no test with a code span in a reference label).
- AC-FR-002-1 [Inferred] (contains) (preservation): Given input `` [`foo`](https://example.com) `` with no extensions, when converted through the public API, then the output contains `<a href="https://example.com"><code>foo</code></a>`. Basis: ANS-001 states that this form already works; the exact output form is inferred.

> Inferred criteria for the maintainer to confirm: AC-FR-001-2, AC-FR-001-3, AC-FR-001-4, AC-FR-001-5, AC-FR-002-1

### Files changed (planned by the Design stage)
`markdown/treeprocessors.py`, `markdown/inlinepatterns.py`, `docs/changelog.md`, `tests/test_syntax/inline/test_links.py`

### Tests
AutoSE test stage: PASS; tests run: 1176 (base: 1166).

Artifacts (spec, design, diff, test report): https://github.com/MittalManas2005/markdown/actions/runs/45015791373


## CI check runs on d550cadbe0a34d9643f27ef763d1cda520a56539

| check | status | conclusion |
|---|---|---|
| validate-release | completed | skipped |
| test (py312) | completed | success |
| lint (flake8) | completed | success |
| test (py313) | completed | success |
| test (py315, 3.15) | completed | success |
| test (pypy311) | completed | success |
| test (py311) | completed | success |
| test (pygments) | completed | success |
| lint (pep517check) | completed | success |
| test (py314) | completed | success |
| lint (checkspelling) | completed | success |
| check-for-entry | completed | success |
| validate-unreleased | completed | success |
| lint (checklinks) | completed | success |

## AutoSE stage check: the pull request is open and CI passes

Result: **PASS** (CI: success)
