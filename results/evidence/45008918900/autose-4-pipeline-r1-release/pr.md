---
artefact: pr
issue: 4
round: 1
branch: autose/issue-4
pr: 10
pr_url: https://github.com/MittalManas2005/markdown/pull/10
head_sha: 38f5849cb31ace3756bf9325f2804724e4bd2381
ci: failure
---

# Release (stage 5)

PR: https://github.com/MittalManas2005/markdown/pull/10

## PR description

Fixes #4

Opened by **AutoSE** (round 1). An independent reviewer agent reviews this PR next; **a maintainer decides whether to merge**.

### Acceptance criteria (from the Requirements stage)
- AC-FR-001-1 [Inferred] (exact): Given a fenced block opened by three backticks with attribute list `{ .python linenums }`, body `print(1)`, closed by three backticks, with extensions `["fenced_code", "attr_list"]`, when `markdown.markdown` is called, then the output equals `<pre><code class="language-python">print(1)\n</code></pre>`.
- AC-FR-001-2 [Inferred] (exact): Given the same block with attribute list `{ .python linenums=true }` and the same extensions, when `markdown.markdown` is called, then the output equals `<pre><code class="language-python">print(1)\n</code></pre>`.
- AC-FR-001-3 [Inferred] (exact): Given the same block with attribute list `{ .python linenums="1" }` and the same extensions, when `markdown.markdown` is called, then the output equals `<pre><code class="language-python">print(1)\n</code></pre>`.
- AC-FR-001-4 [Inferred] (exact): Given the same block with attribute list `{ .python guess_lang noclasses }` and the same extensions, when `markdown.markdown` is called, then the output equals `<pre><code class="language-python">print(1)\n</code></pre>`.
- AC-FR-001-5 [Inferred] (exact): Given the same block with attribute list `{ .python linenums=false }` and the same extensions, when `markdown.markdown` is called, then the output equals `<pre><code class="language-python">print(1)\n</code></pre>`.
- AC-FR-002-1 [Inferred] (contains): Given a fenced block opened by three backticks with attribute list `{ .python linenums data-x="y" }`, body `print(1)`, closed by three backticks, with extensions `["fenced_code", "attr_list"]`, when `markdown.markdown` is called, then the output contains `<code class="language-python" data-x="y">` and does not contain `linenums`.
- AC-FR-003-1 [Inferred] (no-error): Given a fenced block opened by three backticks with attribute list `{ .python linenums }`, body `print(1)`, closed by three backticks, with extensions `["codehilite", "fenced_code"]`, when `markdown.markdown` is called, then no exception is raised and a non-empty output is produced.
- AC-NFR-001-1 [Inferred] (exact): Given a fenced block with attribute list `{ .python foo=bar use_pygments=False }`, body `# Some python code`, and extensions `["fenced_code", "attr_list"]`, when `markdown.markdown` is called, then the output equals `<pre><code class="language-python" foo="bar"># Some python code\n</code></pre>`.
- AC-NFR-001-2 [Inferred] (exact): Given a fenced block with attribute list `{ .python foo=bar use_pygments=True }`, body `# Some python code`, and extensions `["fenced_code", "attr_list"]`, when `markdown.markdown` is called, then the output equals `<pre><code class="language-python"># Some python code\n</code></pre>`.
- AC-NFR-001-3 [Inferred] (exact): Given a fenced block with attribute list `{ .python linenums }`, body `print(1)`, and extensions `["fenced_code"]` only (no `attr_list`), when `markdown.markdown` is called, then the output equals `<pre><code class="language-python">print(1)\n</code></pre>`. Basis: without `attr_list` the key/value output is not built (EV-003).
- AC-NFR-002-1 [Inferred] (exact): Given a fenced block with attribute list `{ .python x><svg/onload=alert(1) }`, body `# Some python code`, and extensions `["fenced_code", "attr_list"]`, when `markdown.markdown` is called, then the output equals `<pre><code class="language-python" x_svg_onload="alert(1)"># Some python code\n</code></pre>`.

> Inferred criteria for the maintainer to confirm: AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-001-4, AC-FR-001-5, AC-FR-002-1, AC-FR-003-1, AC-NFR-001-1, AC-NFR-001-2, AC-NFR-001-3, AC-NFR-002-1

### Files changed (planned by the Design stage)
`markdown/extensions/fenced_code.py`, `tests/test_syntax/extensions/test_fenced_code.py`, `docs/changelog.md`

### Tests
AutoSE test stage: PASS; tests run: 1181 (base: 1166).

Artifacts (spec, design, diff, test report): https://github.com/MittalManas2005/markdown/actions/runs/45008918900


## CI check runs on 38f5849cb31ace3756bf9325f2804724e4bd2381

| check | status | conclusion |
|---|---|---|
| validate-release | completed | skipped |
| test (py314) | completed | success |
| test (py315, 3.15) | completed | success |
| test (py311) | completed | success |
| lint (pep517check) | completed | success |
| lint (checkspelling) | completed | failure |
| lint (checklinks) | completed | success |
| test (pypy311) | completed | success |
| lint (flake8) | completed | success |
| test (pygments) | completed | success |
| test (py312) | completed | success |
| check-for-entry | completed | success |
| test (py313) | completed | success |
| validate-unreleased | completed | success |

## AutoSE stage check: the pull request is open and CI passes

Result: **FAIL** (CI: failure)
