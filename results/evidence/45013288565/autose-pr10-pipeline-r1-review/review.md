---
artefact: review
pr: 10
issue: 4
round: 1
verdict: approve
target_stage: none
reviewer_model: haiku
---

## AutoSE independent review (round 1)

**Verdict: approve**

The change fixes the reported crash. Without codehilite, `linenums`, `guess_lang` and `noclasses` are dropped from the `<code>` attributes when attr_list is on, and other attributes such as `data-x` are still emitted. The full suite passes (1183 tests, 52 skipped), flake8 is clean on both changed files, and the changelog entry is in place. One related crash path remains when codehilite is enabled with use_pygments=False; it is pre-existing and outside the issue's literal scope, so I list it as a minor note.

### What I verified
- python -m unittest discover tests: Ran 1183 tests, OK (skipped=52)
- python -m unittest tests.test_syntax.extensions.test_fenced_code: Ran 58 tests, OK
- python -m flake8 on markdown/extensions/fenced_code.py and the test module: no output (clean)
- Issue example ``` { .python linenums }` with ['fenced_code','attr_list'] (no codehilite) now renders <pre><code class="language-python">print(1)</code></pre> instead of raising TypeError
- With codehilite enabled and default pygments settings, the issue example still renders via codehilite (<pre class="codehilite">...), unchanged
- data-x="y" alongside linenums is kept on the <code> element without codehilite
- Changelog entry added under Unreleased / Fixed; the diff touches no CI files
- Gap found: codehilite enabled with use_pygments=False and attr_list still raises TypeError: cannot serialize None for `{ .python linenums }`, because self.codehilite_conf is truthy so the filter is skipped (markdown/extensions/fenced_code.py:167); this is pre-existing and not a regression from this PR

### Commands I ran (from the session transcript, not self-reported)
- `python -m unittest discover tests` (ok)
- `python -c "import markdown; print(markdown.markdown('''' { .python linenums }\nprint(1)\n'''', extensions=['fenced_code', 'attr_list']))"` (failed)
- `python -c "import markdown; print(markdown.markdown('''' { .python linenums }\nprint(1)\n'''', extensions=['fenced_code', 'attr_list', 'codehilite']))"` (failed)
- `python -c "import markdown; print(markdown.markdown('''' { .python linenums }\nprint(1)\n'''', extensions=['fenced_code', 'attr_list', 'codehilite'], extension_` (failed)
- `python -c "import markdown; print(markdown.markdown('''' { .python hl_lines=\"1 2\" data-y=\"z\" }\nprint(1)\n'''', extensions=['fenced_code', 'attr_list']))"` (failed)
- `python -c "import markdown; print(markdown.markdown('''' { .python linenums=\"0\" }\nprint(1)\n'''', extensions=['fenced_code', 'attr_list', 'codehilite'], exte` (failed)
- `python -c "import markdown; F=chr(96)*3; src=F+' { .python linenums }\nprint(1)\n'+F; print(markdown.markdown(src, extensions=['fenced_code', 'attr_list']))"` (ok)
- `python -c "import markdown; F=chr(96)*3; src=F+' { .python linenums }\nprint(1)\n'+F; print(markdown.markdown(src, extensions=['fenced_code', 'attr_list', 'code` (failed)
- `python -c "import markdown; F=chr(96)*3; src=F+' { .python hl_lines=\"1 2\" data-y=\"z\" }\nprint(1)\n'+F; print(markdown.markdown(src, extensions=['fenced_code` (ok)
- `python -c "import markdown; F=chr(96)*3; src=F+' { .python linenums=\"0\" }\nprint(1)\n'+F; print(markdown.markdown(src, extensions=['fenced_code', 'attr_list',` (ok)
- `python -m flake8 markdown/extensions/fenced_code.py tests/test_syntax/extensions/test_fenced_code.py` (ok)
- `python -m unittest tests.test_syntax.extensions.test_fenced_code` (ok)

### Findings

| severity | location | issue | evidence |
|---|---|---|---|
| minor | `markdown/extensions/fenced_code.py`:167 | The filter keys on whether the codehilite extension is registered, not on whether it actually highlights. With codehilite enabled and use_pygments=False, the highlight-only options still reach the attribute serializer and crash with the same TypeError. | markdown.markdown('```{ .python linenums }\nprint(1)\n```' built with chr(96) fences, extensions=['fenced_code','attr_list','codehilite'], extension_configs={'codehilite': {'use_pygments': False}}) raises TypeError: cannot serialize None (type NoneType) at fenced_code.py:163-164. The issue's own scope is 'codehilite not enabled', so this is not a blocker, but the same error remains reachable. A follow-up could key the filter on the effective use_pygments setting, and a test should cover it. |
| minor | `tests/test_syntax/extensions/test_fenced_code.py`:1226 | The new TestFencedCodeHighlightOnlyOptions class largely duplicates the assertMarkdownRenders tests added just above it in the same file, and it uses internal acceptance-criteria IDs (test_ac_fr_001_1 and similar) as test names, which do not match the style of the rest of the suite. | Lines 204-300 repeat the same inputs and expected output as the earlier TestFencedCode tests (for example linenums, linenums=true, and guess_lang). Behaviour is covered either way, so this is a style and maintenance point only. |

_The reviewer saw only the issue, the diff and the repository at this PR's head. A maintainer decides whether to merge._
