---
artefact: review
pr: 13
issue: 5
round: 1
verdict: approve
target_stage: none
reviewer_model: sonnet
---

## AutoSE independent review (round 1)

**Verdict: approve**

The change excludes headings with class `notoc` from the TOC and `toc_tokens`, keeps their id and permalink, and leaves other classes alone. The full suite and the TOC module pass, and flake8 is clean.

### What I verified
- Ran `python -m unittest discover tests`: 1186 tests, OK.
- Ran `python -m unittest tests.test_syntax.extensions.test_toc`: 87 tests, OK.
- Ran flake8 on toc.py and test_toc.py: clean.
- Ran the issue example plus nested and h1 cases. `notoc` headings are absent from md.toc and md.toc_tokens, and still render with an id (`<h2 class="notoc" id="two">`).
- Children of an excluded heading stay in the TOC, nested under the nearest included ancestor, as the docs state.
- Handles `{: class }`, where the class is None, without crashing.
- The change is a small edit in toc.py, with a docs/changelog.md entry and a docs/extensions/toc.md note. No CI files were touched.

### Commands I ran (from the session transcript, not self-reported)
- `python -m unittest discover tests` (ok)
- `python -c "import markdown; m=markdown.Markdown(extensions=['toc','attr_list']); print(m.convert('[TOC]\n\n# One\n\n## Two {: .notoc }\n\n### Sub\n\n#### Deep\n` (ok)
- `python -m flake8 markdown/extensions/toc.py tests/test_syntax/extensions/test_toc.py` (ok)
- `python -m unittest tests.test_syntax.extensions.test_toc` (ok)

### Findings

| severity | location | issue | evidence |
|---|---|---|---|
| minor | `tests/test_syntax/extensions/test_toc.py`:1497 | Many of the new tests (the `test_ac_fr_*` ones) duplicate other new tests. They add no extra coverage. | For example, `test_ac_fr_003_1` repeats `test_notoc_heading_excluded_from_toc_tokens`, and `test_ac_fr_004_1` repeats part of `test_other_class_unchanged`. |

_The reviewer saw only the issue, the diff and the repository at this PR's head. A maintainer decides whether to merge._
