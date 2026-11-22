---
artefact: review
pr: 26
issue: 25
round: 1
verdict: approve
target_stage: none
reviewer_model: haiku
---

## AutoSE independent review (round 1)

**Verdict: approve**

The PR fixes the TypeError for a valueless `data-toc-label` under `attr_list`. A valueless attribute arrives as `None`, and the fix skips it so the TOC name stays the heading text. Non-empty labels behave as before, the full suite and flake8 pass, and my probes match the issue's expected output. Only a cosmetic nit remains.

### What I verified
- Ran `python -m unittest discover tests`: Ran 1174 tests, OK (skipped=52).
- Ran `python -m unittest tests.test_syntax.extensions.test_toc`: Ran 75 tests, OK.
- Ran `python -m flake8` on markdown/extensions/toc.py and tests/test_syntax/extensions/test_toc.py: no output (clean).
- Probe `## Setup {: data-toc-label }` with ['toc','attr_list']: HTML is `<h2 id="setup">Setup</h2>` with no exception; the fix avoids the None crash.
- Probe `## Setup {: data-toc-label="" }`: HTML is unchanged and no exception.
- Probe mixed document: valueless heading gets name 'Setup' and data-toc-label ''; the labelled heading gets name 'Xy' (tags stripped) and data-toc-label 'X<b>y</b>' (unchanged behaviour for non-empty labels).
- Read toc.py:407-425: the attribute is still deleted in all cases; only the label processing is guarded by `raw_label is not None`. Id generation and token shape are unchanged.
- Changelog entry is placed under [Unreleased] > Fixed and matches the issue. No CI files were changed.

### Commands I ran (from the session transcript, not self-reported)
- `python -m unittest discover tests` (ok)
- `python -m unittest tests.test_syntax.extensions.test_toc` (ok)
- `python -m flake8 markdown/extensions/toc.py tests/test_syntax/extensions/test_toc.py` (ok)
- `python -c "import markdown; print(repr(markdown.markdown('## Setup {: data-toc-label }', extensions=['toc', 'attr_list'])))"` (ok)
- `python -c "import markdown; print(repr(markdown.markdown('## Setup {: data-toc-label=\"\" }', extensions=['toc', 'attr_list'])))"` (ok)
- `python -c "import markdown; md=markdown.Markdown(extensions=['toc','attr_list']); md.convert('## Setup {: data-toc-label }\n\n## Two {: data-toc-label=\"X<b>y</` (ok)

### Findings

| severity | location | issue | evidence |
|---|---|---|---|
| minor | `tests/test_syntax/extensions/test_toc.py` | New tests are named and docstring-tagged `AC-FR-001-1` through `AC-FR-002-2`. These acceptance-criteria IDs do not appear in the issue or repository docs, so they are opaque to a maintainer. Descriptive names would be clearer. | tests/test_syntax/extensions/test_toc.py:93-129, e.g. `def test_ac_fr_001_1_valueless_label_no_error`. Behaviour is covered correctly; this is style only and does not block approval. |

_The reviewer saw only the issue, the diff and the repository at this PR's head. A maintainer decides whether to merge._
