---
artefact: pr
issue: 4
round: 1
branch: autose/issue-4-single
pr: 17
pr_url: https://github.com/MittalManas2005/markdown/pull/17
head_sha: 6c440b222bfe34ffc3d2a0447c495beba0b15b52
ci: success
---

# Release (stage 5)

PR: https://github.com/MittalManas2005/markdown/pull/17

## PR description

Fixes #4

Opened by **AutoSE** (round 1). An independent reviewer agent reviews this PR next; **a maintainer decides whether to merge**.

### Acceptance criteria (from the Requirements stage)
- AC-FR-001-1 [Inferred] (exact): Given the fenced block "``` { .python linenums }" / "print(1)" / "```" with extensions ["fenced_code", "attr_list"], when `markdown.markdown` is called, then the output is `<pre><code class="language-python">print(1)\n</code></pre>` (the output equals the output for the same block without `linenums`).
- AC-FR-001-2 [Inferred] (exact): Given the same block with `{ .python linenums=true }` and extensions ["fenced_code", "attr_list"], when converted, then the output is `<pre><code class="language-python">print(1)\n</code></pre>`.
- AC-FR-001-3 [Inferred] (exact): Given the same block with `{ .python linenums="1" }` and extensions ["fenced_code", "attr_list"], when converted, then the output is `<pre><code class="language-python">print(1)\n</code></pre>`.
- AC-FR-001-4 [Inferred] (exact): Given the same block with `{ .python guess_lang=False }` and extensions ["fenced_code", "attr_list"], when converted, then the output is `<pre><code class="language-python">print(1)\n</code></pre>`.
- AC-FR-001-5 [Inferred] (exact): Given the same block with `{ .python noclasses=True }` and extensions ["fenced_code", "attr_list"], when converted, then the output is `<pre><code class="language-python">print(1)\n</code></pre>`.
- AC-FR-002-1 [Inferred] (exact): Given the block "``` { .python hl_lines="1 3" }" / "print(1)" / "```" with extensions ["fenced_code", "attr_list"], when converted, then the output is `<pre><code class="language-python">print(1)\n</code></pre>`.
- AC-FR-003-1 [Inferred] (exact) (preservation): Given the block "``` { .python data-x="y" linenums }" / "print(1)" / "```" with extensions ["fenced_code", "attr_list"], when converted, then the output is `<pre><code class="language-python" data-x="y">print(1)\n</code></pre>`.
- AC-FR-004-1 [Inferred] (contains) (preservation): Given the block "``` { .python linenums=True }" / "print(1)" / "```" with extensions ["codehilite", "fenced_code"], when converted, then the output contains `class="codehilite"`.

> Inferred criteria for the maintainer to confirm: AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-001-4, AC-FR-001-5, AC-FR-002-1, AC-FR-003-1, AC-FR-004-1

### Files changed (planned by the Design stage)
`markdown/extensions/fenced_code.py`, `tests/test_syntax/extensions/test_fenced_code.py`, `docs/extensions/fenced_code_blocks.md`, `docs/changelog.md`

### Tests
AutoSE test stage: PASS; tests run: 1174 (base: 1166).

Artifacts (spec, design, diff, test report): https://github.com/MittalManas2005/markdown/actions/runs/45011703200


## CI check runs on 6c440b222bfe34ffc3d2a0447c495beba0b15b52

| check | status | conclusion |
|---|---|---|
| validate-release | completed | skipped |
| check-for-entry | completed | success |
| lint (checklinks) | completed | success |
| test (py311) | completed | success |
| test (py314) | completed | success |
| test (pygments) | completed | success |
| test (pypy311) | completed | success |
| lint (pep517check) | completed | success |
| test (py312) | completed | success |
| lint (flake8) | completed | success |
| test (py313) | completed | success |
| test (py315, 3.15) | completed | success |
| lint (checkspelling) | completed | success |
| validate-unreleased | completed | success |

## AutoSE stage check: the pull request is open and CI passes

Result: **PASS** (CI: success)
