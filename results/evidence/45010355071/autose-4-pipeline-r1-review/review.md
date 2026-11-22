---
artefact: review
pr: 10
issue: 4
round: 1
verdict: approve
target_stage: none
reviewer_model: sonnet
---

## AutoSE independent review (round 1)

**Verdict: approve**

The change fixes the crash from the issue. Without codehilite, linenums, guess_lang and noclasses are dropped from the output, and other attributes such as data-x are kept. The full test suite passes and flake8 is clean. One related crash remains when codehilite is enabled with use_pygments=False. I rated it minor because the issue is about the case without codehilite.

### What I verified
- `python -m unittest discover tests` passed: 1183 tests, OK, 52 skipped.
- flake8 on markdown/extensions/fenced_code.py and the test file reports nothing.
- The diff adds a changelog entry, changes only fenced_code.py and its tests, and does not touch CI files.
- Escaping is unchanged. Only the highlight-only keys are filtered, and only when codehilite is not enabled.
- With codehilite enabled, the pygments path is untouched. The new test for it matches the existing linenums behaviour.
- I ran the failing case from the issue with a ~~~ fence and `linenums=false use_pygments=false` under fenced_code + attr_list. It renders without crashing.
- I did not run the changed test module on its own; the full-suite run includes it.

### Commands I ran (from the session transcript, not self-reported)
- `python -m unittest discover tests` (ok)
- `python -m flake8 markdown/extensions/fenced_code.py tests/test_syntax/extensions/test_fenced_code.py` (ok)
- `python -c "import markdown; print(markdown.markdown('''' { .python linenums data-x=y }\nprint(1)\n'''', extensions=['fenced_code','attr_list','codehilite'], ext` (failed)
- `python -c "import markdown; print(markdown.markdown('''' { .python linenums use_pygments }\nprint(1)\n'''', extensions=['fenced_code','attr_list']))"` (failed)
- `python -c "import markdown; print(markdown.markdown('~~~ { .python linenums data-x=y }\nprint(1)\n~~~', extensions=['fenced_code','attr_list','codehilite'], ext` (failed)
- `python -c "import markdown; print(markdown.markdown('~~~ { .python linenums=false use_pygments=false }\nprint(1)\n~~~', extensions=['fenced_code','attr_list']))` (ok)

### Findings

| severity | location | issue | evidence |
|---|---|---|---|
| minor | `markdown/extensions/fenced_code.py`:167 | The filter is skipped whenever codehilite is registered, so `linenums`, `guess_lang` and `noclasses` still reach `_escape_attrib_html`. With codehilite enabled and use_pygments=False, a block using `linenums` still crashes with the same TypeError. This is outside the issue's stated scope. | extensions=['fenced_code','attr_list','codehilite'] with codehilite use_pygments=False, source `~~~ { .python linenums data-x=y }`: TypeError: cannot serialize None (type NoneType) at fenced_code.py:164. |

_The reviewer saw only the issue, the diff and the repository at this PR's head. A maintainer decides whether to merge._
