---
artefact: pr
issue: 4
round: 1
branch: autose/issue-4
pr: 10
pr_url: https://github.com/MittalManas2005/markdown/pull/10
head_sha: fd28997280260e2a401aee8de5afec6b9a9f374e
ci: success
---

# Release (stage 5)

PR: https://github.com/MittalManas2005/markdown/pull/10

## PR description

Fixes #4

Opened by **AutoSE** (round 1). An independent reviewer agent reviews this PR next; **a maintainer decides whether to merge**.

### Acceptance criteria (from the Requirements stage)
- AC-FR-001-1 [Inferred] (contains): Given the block "``` { .python linenums }" followed by line "print(1)" and line "```" (three lines joined by newlines), with extensions ["fenced_code", "attr_list"], when converted through the public `markdown.markdown` call, then the output contains `<pre><code class="language-python">print(1)`.
- AC-FR-001-2 [Inferred] (contains): Given the block "``` { .python linenums=true }" with the same content lines "print(1)" and "```", with extensions ["fenced_code", "attr_list"], when converted through the public `markdown.markdown` call, then the output contains `<pre><code class="language-python">print(1)`.
- AC-FR-001-3 [Inferred] (contains): Given the block "``` { .python linenums="1" }" with the same content lines, with extensions ["fenced_code", "attr_list"], when converted through the public `markdown.markdown` call, then the output contains `<pre><code class="language-python">print(1)`.
- AC-FR-001-4 [Inferred] (contains): Given the block "``` { .python guess_lang }" with the same content lines, with extensions ["fenced_code", "attr_list"], when converted through the public `markdown.markdown` call, then the output contains `<pre><code class="language-python">print(1)`.
- AC-FR-001-5 [Inferred] (contains): Given the block "``` { .python noclasses }" with the same content lines, with extensions ["fenced_code", "attr_list"], when converted through the public `markdown.markdown` call, then the output contains `<pre><code class="language-python">print(1)`.
- AC-FR-001-6 [Inferred] (contains): Given the block "``` { .python linenums guess_lang noclasses }" with the same content lines, with extensions ["fenced_code", "attr_list"], when converted through the public `markdown.markdown` call, then the output contains `<pre><code class="language-python">print(1)`.
- AC-FR-001-7 [Inferred] (contains) (preservation): Given the block "``` { .python linenums }" with the same content lines, with extensions ["fenced_code"] only, when converted through the public `markdown.markdown` call, then the output contains `<pre><code class="language-python">print(1)`.
- AC-FR-002-1 [Inferred] (contains) (preservation): Given the block "``` { .python data-x="y" linenums }" with the content lines "print(1)" and "```", with extensions ["fenced_code", "attr_list"], when converted through the public `markdown.markdown` call, then the output contains `<pre><code class="language-python" data-x="y">print(1)`.
- AC-FR-003-1 [Inferred] (property) (preservation): Given the block "``` { .python linenums=True }" with the content lines "# Some python code" and "```", with extensions ["codehilite", "fenced_code"], when converted through the public `markdown.markdown` call, then the output has the same structure as the expected output of the existing test `testFencedLanguageAttrLinenums` (Pygments-dependent) in `tests/test_syntax/extensions/test_fenced_code.py`.

> Inferred criteria for the maintainer to confirm: AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-001-4, AC-FR-001-5, AC-FR-001-6, AC-FR-001-7, AC-FR-002-1, AC-FR-003-1

### Files changed (planned by the Design stage)
`markdown/extensions/fenced_code.py`, `tests/test_syntax/extensions/test_fenced_code.py`, `docs/changelog.md`

### Tests
AutoSE test stage: PASS; tests run: 1183 (base: 1166).

Artifacts (spec, design, diff, test report): https://github.com/MittalManas2005/markdown/actions/runs/45010355071


## CI check runs on fd28997280260e2a401aee8de5afec6b9a9f374e

| check | status | conclusion |
|---|---|---|
| validate-release | completed | skipped |
| test (py312) | completed | success |
| test (pypy311) | completed | success |
| test (py314) | completed | success |
| lint (pep517check) | completed | success |
| test (py315, 3.15) | completed | success |
| lint (flake8) | completed | success |
| validate-unreleased | completed | success |
| test (pygments) | completed | success |
| test (py313) | completed | success |
| test (py311) | completed | success |
| lint (checklinks) | completed | success |
| check-for-entry | completed | success |
| lint (checkspelling) | completed | success |

## AutoSE stage check: the pull request is open and CI passes

Result: **PASS** (CI: success)
