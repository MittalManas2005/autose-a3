---
artefact: pr
issue: 6
round: 1
branch: autose/issue-6
pr: 9
pr_url: https://github.com/MittalManas2005/markdown/pull/9
head_sha: 60dfa0d120c52a36068676c0ed6900f0ab29d407
ci: failure
---

# Release (stage 5)

PR: https://github.com/MittalManas2005/markdown/pull/9

## PR description

Fixes #6

Opened by **AutoSE** (round 1). An independent reviewer agent reviews this PR next; **a maintainer decides whether to merge**.

### Acceptance criteria (from the Requirements stage)
- AC-FR-001-1 [Inferred] (no-error): Given stdin text made of the lines `- a`, an empty line and `  - b`, when run as `python -m markdown --tab_length=2`, then the command exits with status 0 and writes HTML to stdout.
- AC-FR-001-2 [Inferred] (no-error): Given the same stdin text, when run as `python -m markdown --tab_length 2`, then the command exits with status 0 and writes HTML to stdout.
- AC-FR-002-1 [Inferred] (property): Given the input text `- a`, an empty line, `  - b`, when run as `python -m markdown --tab_length=2`, then the standard output equals the string returned by `markdown.markdown("- a\n\n  - b\n", tab_length=2)`.
- AC-FR-002-2 [Inferred] (property): Given the same input text, when run as `python -m markdown --tab_length 2`, then the standard output equals the string returned by `markdown.markdown("- a\n\n  - b\n", tab_length=2)`.
- AC-FR-002-3 [Inferred] (property): Given the same input text, when run as `python -m markdown --tab_length=2`, then the `li` element whose text is `b` is a descendant of the `li` element whose text is `a` (nested list, as the issue reports for the library).
- AC-FR-003-1 [Inferred] (property) (preservation): Given the input text `- a`, an empty line, `  - b`, when run as `python -m markdown` with no `--tab_length` option, then the standard output equals the string returned by `markdown.markdown("- a\n\n  - b\n")` with no `tab_length` keyword, and the `li` element whose text is `b` is not a descendant of the `li` element whose text is `a`.
- AC-FR-004-1 [Inferred] (contains): Given no input, when run as `python -m markdown --help`, then the output contains `--tab_length`.
- AC-FR-005-1 [Inferred] (contains): Given no input and the option value `abc`, when run as `python -m markdown --tab_length abc`, then the exit status is non-zero and the error output contains `--tab_length`.
- AC-NFR-001-1 [Inferred] (property) (preservation): Given the input text `- a`, an empty line, `  - b`, when run as `python -m markdown -o html`, then the standard output equals the string returned by `markdown.markdown("- a\n\n  - b\n", output_format='html')`.

> Inferred criteria for the maintainer to confirm: AC-FR-001-1, AC-FR-001-2, AC-FR-002-1, AC-FR-002-2, AC-FR-002-3, AC-FR-003-1, AC-FR-004-1, AC-FR-005-1, AC-NFR-001-1

### Files changed (planned by the Design stage)
`markdown/__main__.py`, `docs/changelog.md`, `docs/cli.md`, `tests/test_apis.py`

### Tests
AutoSE test stage: PASS; tests run: 1181 (base: 1166).

Artifacts (spec, design, diff, test report): https://github.com/MittalManas2005/markdown/actions/runs/45008931950


## CI check runs on 60dfa0d120c52a36068676c0ed6900f0ab29d407

| check | status | conclusion |
|---|---|---|
| validate-release | completed | skipped |
| lint (checkspelling) | completed | failure |
| test (py315, 3.15) | completed | success |
| test (py313) | completed | success |
| test (pygments) | completed | success |
| test (py312) | completed | success |
| test (py314) | completed | success |
| lint (checklinks) | completed | success |
| test (py311) | completed | success |
| test (pypy311) | completed | success |
| lint (flake8) | completed | success |
| validate-unreleased | completed | success |
| lint (pep517check) | completed | success |
| check-for-entry | completed | success |

## AutoSE stage check: the pull request is open and CI passes

Result: **FAIL** (CI: failure)
