---
artefact: review
pr: 22
issue: 6
round: 1
verdict: request_changes
target_stage: implementation
reviewer_model: haiku
---

## AutoSE independent review (round 1)

**Verdict: request changes** (back to **implementation**)

The --tab_length option is wired up, but its CLI default is 2 instead of the library default of 4. Any CLI run that omits the option now renders differently from before, which the issue explicitly forbids. The new tests encode the wrong default, so they do not catch it.

### What I verified
- python -m unittest discover tests (run by me): Ran 1168 tests, OK (skipped=52)
- python -m unittest tests.test_apis (run by me): Ran 91 tests, OK
- Library default tab_length is 4 (markdown/core.py:110, kwargs.get('tab_length', 4))
- parse_options([]) returns tab_length=2 (markdown/__main__.py:69)
- Without the option, markdown.markdown('- a\n\n    - b\n') renders a nested <ul> (library default 4); with tab_length=2 the same input renders '- b' as a <pre><code> block inside <li>a, so omitting the option changes output
- parse_options(['--tab_length','2']) passes tab_length=2 and the issue's 2-space example nests correctly
- Changelog entry present under Unreleased/Added; no CI files touched; -t short flag does not clash with existing options
- flake8 not run

### Commands I ran (from the session transcript, not self-reported)
- `python -c "import markdown,inspect; print(inspect.signature(markdown.Markdown.__init__))"` (ok)
- `python -m unittest discover tests` (ok)
- `python -m unittest tests.test_apis` (ok)
- `python -c "import markdown; print(repr(markdown.markdown('- a\n\n    - b\n')))"` (ok)
- `python -c "import sys; from markdown.__main__ import parse_options; print(parse_options([])[0]['tab_length'])"` (ok)
- `python -m markdown -- ./dummy 2>/dev/null; python -c "import markdown; print(markdown.markdown('- a\n\n    - b\n', tab_length=2))"` (failed)
- `python -c "import markdown; print(markdown.markdown('- a\n\n    - b\n'))"` (ok)
- `python -c "import markdown; print(markdown.markdown('- a\n\n    - b\n', tab_length=2))"` (ok)
- `python -c "import markdown.__main__ as m; o,_=m.parse_options(['--tab_length','2']); print(o['tab_length']); import markdown; print(markdown.markdown('- a\n\n  ` (ok)

### Findings

| severity | location | issue | evidence |
|---|---|---|---|
| blocker | `markdown/__main__.py`:69 | The --tab_length option defaults to 2, not the library default of 4. Any CLI run without the option now uses tab_length=2, so existing output changes. The issue requires output to be unchanged when the option is absent. | markdown/core.py:110 uses kwargs.get('tab_length', 4). With the PR, parse_options([]) returns tab_length=2. Input '- a\n\n    - b\n' with no option renders at HEAD as a nested <ul> (library default 4). With tab_length=2 it renders as <li>a<pre><code>- b, a changed result for input that never used the option. |
| major | `tests/test_apis.py`:800 | The test fixture default and testNoOptions were changed to expect 'tab_length': 2. This locks in the regression, and no test checks that omitting the option matches the library default of 4. | The diff adds 'tab_length': 2 to default_options in TestCliOptionParsing. testNoOptions asserts parse_options([]) equals that dict, so it passes only because the wrong default is in the test too. |

_The reviewer saw only the issue, the diff and the repository at this PR's head. A maintainer decides whether to merge._
