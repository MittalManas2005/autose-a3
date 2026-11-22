---
artefact: pr
issue: 6
round: 1
branch: autose/issue-6
pr: 9
pr_url: https://github.com/MittalManas2005/markdown/pull/9
head_sha: 4bd485213973fabf2d25364e1e123b19961b1c89
ci: success
---

# Release (stage 5)

PR: https://github.com/MittalManas2005/markdown/pull/9

## PR description

Fixes #6

Opened by **AutoSE** (round 1). An independent reviewer agent reviews this PR next; **a maintainer decides whether to merge**.

### Acceptance criteria (from the Requirements stage)
- AC-FR-001-1 [Inferred] (contains): Given the `--help` argument, when `python -m markdown --help` is run, then the output contains `--tab_length`.
- AC-FR-001-2 [Inferred] (property): Given the text "- a", an empty line, "  - b" (ending with a newline), and the argument `--tab_length=2`, when `python -m markdown` converts it from standard input, then the `<li>` for `b` is a child of a `<ul>` nested inside the `<li>` for `a`.
- AC-FR-002-1 [Inferred] (property): Given the text "- a", an empty line, "  - b" (ending with a newline), when `python -m markdown` is run once with `--tab_length 2` (two separate arguments) and once with `--tab_length=2`, then both outputs are identical.
- AC-FR-002-2 [Inferred] (no-error): Given the text "- a", an empty line, "  - b" (ending with a newline) and the argument `--tab_length=2`, when `python -m markdown` is run, then it exits without an error and produces output.
- AC-FR-003-1 [Inferred] (property): Given the text "- a", an empty line, "  - b" (ending with a newline) and the argument `--tab_length=2`, when `python -m markdown` converts it, then its output equals the output of `markdown.markdown(text, tab_length=2)` for the same text.
- AC-FR-004-1 [Inferred] (contains) (preservation): Given the text "- a", an empty line, "  - b" (ending with a newline) and no `--tab_length` argument, when `python -m markdown` converts it, then the output contains `<li>b</li>`, and the `<li>` for `b` is not nested inside the `<li>` for `a`.
- AC-FR-004-2 [Inferred] (property) (preservation): Given the text "- a", an empty line, "  - b" (ending with a newline) and no `--tab_length` argument, when `python -m markdown` converts it, then its output equals the output of `markdown.markdown(text)` called without a `tab_length` argument.
- AC-FR-005-1 [Inferred] (property): Given the text "- a", an empty line, "  - b" (ending with a newline) and the argument `--tab_length=2`, when the `markdown_py` command converts it, then its output equals the output of `python -m markdown` with the same arguments and input.

> Inferred criteria for the maintainer to confirm: AC-FR-001-1, AC-FR-001-2, AC-FR-002-1, AC-FR-002-2, AC-FR-003-1, AC-FR-004-1, AC-FR-004-2, AC-FR-005-1

### Files changed (planned by the Design stage)
`markdown/__main__.py`, `docs/cli.md`, `docs/changelog.md`, `tests/test_apis.py`

### Tests
AutoSE test stage: PASS; tests run: 1183 (base: 1166).

Artifacts (spec, design, diff, test report): https://github.com/MittalManas2005/markdown/actions/runs/45010360150


## CI check runs on 4bd485213973fabf2d25364e1e123b19961b1c89

| check | status | conclusion |
|---|---|---|
| validate-release | completed | skipped |
| test (py315, 3.15) | completed | success |
| test (py312) | completed | success |
| test (py314) | completed | success |
| test (pypy311) | completed | success |
| lint (flake8) | completed | success |
| lint (checklinks) | completed | success |
| test (pygments) | completed | success |
| test (py313) | completed | success |
| test (py311) | completed | success |
| lint (pep517check) | completed | success |
| lint (checkspelling) | completed | success |
| validate-unreleased | completed | success |
| check-for-entry | completed | success |

## AutoSE stage check: the pull request is open and CI passes

Result: **PASS** (CI: success)
