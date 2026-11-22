---
artefact: pr
issue: 6
round: 1
branch: autose/issue-6-single
pr: 14
pr_url: https://github.com/MittalManas2005/markdown/pull/14
head_sha: b1be4629839bc48cb41c5530af168a9a82bd27da
ci: success
---

# Release (stage 5)

PR: https://github.com/MittalManas2005/markdown/pull/14

## PR description

Fixes #6

Opened by **AutoSE** (round 1). An independent reviewer agent reviews this PR next; **a maintainer decides whether to merge**.

### Acceptance criteria (from the Requirements stage)
- AC-FR-001-1 [Confirmed] (property): Given the command-line arguments `["--tab_length=2"]`, when `markdown.__main__.parse_options` is called, then the returned options dictionary contains `"tab_length"` with the value `2`.
- AC-FR-001-2 [Confirmed] (property): Given the command-line arguments `["--tab_length", "2"]`, when `markdown.__main__.parse_options` is called, then the returned options dictionary contains `"tab_length"` with the value `2`.
- AC-FR-002-1 [Inferred] (property): Given the input `- a` followed by a blank line and `  - b`, with the command-line arguments `["--tab_length=2"]` and the input supplied on standard input, when the command line is run, then its output equals `markdown.markdown("- a\n\n  - b\n", tab_length=2)`. Basis: the issue's example is `printf -- '- a\n\n  - b\n'`; the expected form is derived from the stated equivalence (SRC-003), not from a stated output string.
- AC-FR-003-1 [Confirmed] (property) (preservation): Given the command-line arguments `[]`, when `markdown.__main__.parse_options` is called, then the returned options dictionary equals the dictionary asserted by the existing test `TestCliOptionParsing.testNoOptions` (no `"tab_length"` key).
- AC-FR-003-2 [Inferred] (property) (preservation): Given the input `- a` followed by a blank line and `  - b`, with no `--tab_length` option, when the command line is run, then its output equals `markdown.markdown("- a\n\n  - b\n")` with default settings. Basis: the default `tab_length` is 4 (`markdown/core.py:110`, EV-002); the equality is derived from "stay exactly as it is now".

> Inferred criteria for the maintainer to confirm: AC-FR-002-1, AC-FR-003-2

### Files changed (planned by the Design stage)
`markdown/__main__.py`, `tests/test_cli_tab_length.py`, `docs/cli.md`, `docs/changelog.md`

### Tests
AutoSE test stage: PASS; tests run: 1172 (base: 1166).

Artifacts (spec, design, diff, test report): https://github.com/MittalManas2005/markdown/actions/runs/45011716124


## CI check runs on b1be4629839bc48cb41c5530af168a9a82bd27da

| check | status | conclusion |
|---|---|---|
| validate-release | completed | skipped |
| test (py313) | completed | success |
| test (py315, 3.15) | completed | success |
| test (py314) | completed | success |
| test (pypy311) | completed | success |
| test (py311) | completed | success |
| lint (checkspelling) | completed | success |
| check-for-entry | completed | success |
| lint (flake8) | completed | success |
| test (pygments) | completed | success |
| lint (checklinks) | completed | success |
| test (py312) | completed | success |
| lint (pep517check) | completed | success |
| validate-unreleased | completed | success |

## AutoSE stage check: the pull request is open and CI passes

Result: **PASS** (CI: success)
