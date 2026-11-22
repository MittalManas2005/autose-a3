---
artefact: pr
issue: 5
round: 1
branch: autose/issue-5
pr: 13
pr_url: https://github.com/MittalManas2005/markdown/pull/13
head_sha: 1bb21178b8e6fa30f36a61fb1eff25c92fe30830
ci: success
---

# Release (stage 5)

PR: https://github.com/MittalManas2005/markdown/pull/13

## PR description

Fixes #5

Opened by **AutoSE** (round 1). An independent reviewer agent reviews this PR next; **a maintainer decides whether to merge**.

### Acceptance criteria (from the Requirements stage)
- AC-FR-001-1 [Inferred] (contains): Given the document lines `[TOC]`, `# One`, `## Two {: .notoc }`, `## Three` (blank lines between them) with extensions ["toc", "attr_list"], when converted through the public API, then the output TOC (`md.toc`) contains `href="#one"`.
- AC-FR-001-2 [Inferred] (contains): Given the same document with extensions ["toc", "attr_list"], when converted through the public API, then the output TOC (`md.toc`) contains `href="#three"`.
- AC-FR-001-3 [Inferred] (not-contains): Given the same document with extensions ["toc", "attr_list"], when converted through the public API, then the output TOC (`md.toc`) does not contain `href="#two"`.
- AC-FR-001-4 [Inferred] (contains): Given the document lines `# One`, `## Two {: .notoc }`, `### Sub` (blank lines between them) with extensions ["toc", "attr_list"], when converted through the public API, then the output TOC (`md.toc`) contains `href="#sub"` (default per ASM-002; see Q-001).
- AC-FR-001-5 [Inferred] (contains) (preservation): Given the document lines `# One`, `## Two`, `## Three` (blank lines between them) with extensions ["toc"], when converted through the public API, then the output TOC (`md.toc`) contains `href="#two"`.
- AC-FR-002-1 [Inferred] (contains) (preservation): Given the document lines `# One`, `## Two {: .notoc }`, `## Three` (blank lines between them) with extensions ["toc", "attr_list"], when converted through the public API, then the output HTML contains `id="two"`.
- AC-FR-002-2 [Inferred] (contains): Given the document lines `# One`, `## Two {: .notoc }`, `## Three` (blank lines between them) with extensions ["toc", "attr_list"], when converted through the public API, then the output HTML contains `Two</h2>`.
- AC-FR-002-3 [Inferred] (contains): Given the document lines `# One`, `## Two {: .notoc }` (blank line between them) with extensions ["toc", "attr_list"] and the toc option `permalink` set to `True`, when converted through the public API, then the output HTML contains `class="headerlink" href="#two"` (default per ASM-001; EV-006 shows the permalink markup format).
- AC-FR-003-1 [Inferred] (property): Given the document lines `[TOC]`, `# One`, `## Two {: .notoc }`, `## Three` (blank lines between them) with extensions ["toc", "attr_list"], when converted through the public API, then no entry in `md.toc_tokens`, at any nesting depth, has the id `two`, and entries with the ids `one` and `three` are present.
- AC-FR-004-1 [Inferred] (contains) (preservation): Given the document lines `# One`, `## Two {: .other }`, `## Three` (blank lines between them) with extensions ["toc", "attr_list"], when converted through the public API, then the output TOC (`md.toc`) contains `href="#two"`.
- AC-FR-004-2 [Inferred] (property) (preservation): Given the document lines `# One`, `## Two {: .other }`, `## Three` (blank lines between them) with extensions ["toc", "attr_list"], when converted through the public API, then `md.toc_tokens` equals the `md.toc_tokens` produced by the same document with the `{: .other }` attribute list removed.
- AC-FR-005-1 [Inferred] (not-contains): Given the document lines `# One`, `## Two {: .other .notoc }`, `## Three` (blank lines between them) with extensions ["toc", "attr_list"], when converted through the public API, then the output TOC (`md.toc`) does not contain `href="#two"`.

> Inferred criteria for the maintainer to confirm: AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-001-4, AC-FR-001-5, AC-FR-002-1, AC-FR-002-2, AC-FR-002-3, AC-FR-003-1, AC-FR-004-1, AC-FR-004-2, AC-FR-005-1

### Files changed (planned by the Design stage)
`markdown/extensions/toc.py`, `tests/test_syntax/extensions/test_toc.py`, `docs/extensions/toc.md`, `docs/changelog.md`

### Tests
AutoSE test stage: PASS; tests run: 1186 (base: 1166).

Artifacts (spec, design, diff, test report): https://github.com/MittalManas2005/markdown/actions/runs/45010346253


## CI check runs on 1bb21178b8e6fa30f36a61fb1eff25c92fe30830

| check | status | conclusion |
|---|---|---|
| validate-release | completed | skipped |
| validate-unreleased | completed | success |
| test (py311) | completed | success |
| test (py314) | completed | success |
| test (py312) | completed | success |
| lint (flake8) | completed | success |
| lint (pep517check) | completed | success |
| test (pypy311) | completed | success |
| test (pygments) | completed | success |
| lint (checklinks) | completed | success |
| test (py313) | completed | success |
| test (py315, 3.15) | completed | success |
| lint (checkspelling) | completed | success |
| check-for-entry | completed | success |

## AutoSE stage check: the pull request is open and CI passes

Result: **PASS** (CI: success)
