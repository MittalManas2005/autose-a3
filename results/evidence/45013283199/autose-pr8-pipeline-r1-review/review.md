---
artefact: review
pr: 8
issue: 3
round: 1
verdict: approve
target_stage: none
reviewer_model: haiku
---

## AutoSE independent review (round 1)

**Verdict: approve**

The fix resolves issue #3. A valueless (`None`) or empty `id` on a heading is now treated as no id, so the heading gets the generated slug, appears in the TOC, and the crash at `toc.py:418` no longer occurs. Explicit ids are unchanged, and the no-toc rendering `<h1 id>` is preserved. The full suite and the TOC module pass, and flake8 is clean on both changed files.

### What I verified
- Read issue #3 and diff; the change is limited to markdown/extensions/toc.py (used_ids collection at line 392 and the generated-id check at line 404), a changelog entry under Unreleased/Fixed, and new tests.
- `python -m unittest discover tests`: Ran 1179 tests, OK (skipped=52).
- `python -m unittest tests.test_syntax.extensions.test_toc`: Ran 80 tests, OK.
- `python -m flake8 markdown/extensions/toc.py tests/test_syntax/extensions/test_toc.py`: no output (clean).
- Probe `# Heading {: id }` with toc+attr_list -> `<h1 id="heading">Heading</h1>`, no exception.
- Probe duplicates: `# Heading {: id }`, `# Heading`, `## Heading {: id="" }`, `# Heading {: id }` -> ids heading, heading_1, heading_2, heading_3 (no collisions).
- Probe explicit id colliding with generated slug: `# Heading {: id="heading" }` then `# Heading {: id }` -> second gets heading_1; explicit id kept.
- Probe `[TOC]` with valueless id heading: TOC links `#heading`, token id/name correct.
- Probe toc `permalink: True` with valueless id: permalink anchor uses generated id `heading`.
- Probe custom `slugify` config: valueless id heading receives the custom slug `x`.
- Checked that explicit ids (`id="intro"`) keep working in TOC and HTML; no-toc `{: id }` output unchanged (`<h1 id>Heading</h1>`); escaping paths untouched.

### Commands I ran (from the session transcript, not self-reported)
- `python -m unittest discover tests` (ok)
- `python -m unittest tests.test_syntax.extensions.test_toc` (ok)
- `python -m flake8 markdown/extensions/toc.py tests/test_syntax/extensions/test_toc.py` (ok)
- `python -c "import markdown; print(markdown.markdown('# Heading {: id }\n\n# Heading\n\n## Heading {: id=\"\" }\n\n# Heading {: id }', extensions=['toc', 'attr_l` (ok)
- `python -c "import markdown; print(markdown.markdown('[TOC]\n\n# Heading {: id }\n\n# Other {: id=\"heading-1\" }\n\n# Heading\n\n# Heading {: id }', extensions=` (ok)
- `python -c "import markdown; print(markdown.markdown('# Heading {: id }', extensions=['toc', 'attr_list', 'anchorlink', 'permalink']))"` (failed)
- `python -c "import markdown; print(markdown.markdown('# Heading {: id }', extensions=['toc', 'attr_list'], extension_configs={'toc': {'slugify': lambda v, s: 'x'` (ok)
- `python -c "import markdown; print(markdown.markdown('# Heading {: id=\"heading\" }\n\n# Heading {: id }', extensions=['toc', 'attr_list']))"` (ok)
- `python -c "import markdown; print(markdown.markdown('[TOC]\n\n# Heading {: id }', extensions=['toc', 'attr_list'], extension_configs={'toc': {'permalink': True}` (ok)

### Findings

| severity | location | issue | evidence |
|---|---|---|---|
| — | — | — | — |

_The reviewer saw only the issue, the diff and the repository at this PR's head. A maintainer decides whether to merge._
