---
artefact: review
pr: 20
issue: 4
round: 1
verdict: request_changes
target_stage: implementation
reviewer_model: haiku
---

## AutoSE independent review (round 1)

**Verdict: request changes** (back to **implementation**)

The crash is gone, but the fix does the opposite of what the issue asks. Without codehilite, codehilite-only options (linenums, guess_lang, noclasses) are now written onto <code> as attributes, where the issue says they should be ignored and the block rendered as if they were absent. The new tests assert that wrong output, and the changelog documents it.

### What I verified
- python -m unittest discover tests: 1169 tests run, OK (skipped=52).
- python -m unittest tests.test_syntax.extensions.test_fenced_code_bool_options: 3 tests, OK.
- '{ .python linenums }' gives <pre><code class="language-python" linenums="True">print(1)\n</code></pre>.
- '{ .python linenums="1" guess_lang noclasses }' gives <code class="language-python" linenums="True" guess_lang="True" noclasses="True">.
- '{ .python linenums=false }' gives linenums="False".
- '{ .python }' (baseline) gives <code class="language-python">.
- Other key=value attributes (data-x="y") still reach <code>, as the issue requires.

### Commands I ran (from the session transcript, not self-reported)
- `python -m unittest tests.test_syntax.extensions.test_fenced_code_bool_options` (ok)
- `python -m unittest discover tests` (ok)
- `python -c "import markdown; print(repr(markdown.markdown('''' { .python linenums }\nprint(1)\n'''', extensions=['fenced_code', 'attr_list'])))"` (failed)
- `python -c "import markdown; print(repr(markdown.markdown('''' { .python linenums=\"1\" guess_lang noclasses }\nprint(1)\n'''', extensions=['fenced_code', 'attr_` (failed)
- `python -c "import markdown; print(repr(markdown.markdown('''' { .python }\nprint(1)\n'''', extensions=['fenced_code', 'attr_list'])))"` (failed)
- `python -c "import markdown; print(repr(markdown.markdown('''' { .python linenums=false }\nprint(1)\n'''', extensions=['fenced_code', 'attr_list'])))"` (failed)
- `python -c "import markdown; bt=chr(96)*3; print(repr(markdown.markdown(bt+' { .python linenums }\nprint(1)\n'+bt, extensions=['fenced_code', 'attr_list'])))"` (ok)
- `python -c "import markdown; bt=chr(96)*3; print(repr(markdown.markdown(bt+' { .python linenums=\"1\" guess_lang noclasses }\nprint(1)\n'+bt, extensions=['fenced` (ok)
- `python -c "import markdown; bt=chr(96)*3; print(repr(markdown.markdown(bt+' { .python }\nprint(1)\n'+bt, extensions=['fenced_code', 'attr_list'])))"` (ok)
- `python -c "import markdown; bt=chr(96)*3; print(repr(markdown.markdown(bt+' { .python linenums=false }\nprint(1)\n'+bt, extensions=['fenced_code', 'attr_list'])` (ok)

### Findings

| severity | location | issue | evidence |
|---|---|---|---|
| blocker | `markdown/extensions/fenced_code.py`:161 | Codehilite-only options are emitted as HTML attributes when codehilite is disabled, instead of being ignored. The patch only changes how None/True values are stringified, so linenums, guess_lang and noclasses still reach the <code> element. | Actual for '``` { .python linenums }' with extensions=['fenced_code','attr_list']: '<pre><code class="language-python" linenums="True">print(1)\n</code></pre>'. Expected per issue (block rendered as if options were not written): '<pre><code class="language-python">print(1)\n</code></pre>'. Same leak for '{ .python linenums="1" guess_lang noclasses }', which gives linenums="True" guess_lang="True" noclasses="True" (issue expects none of these). The fix needs to drop codehilite-only keys in the non-highlighting branch, by key name and not by value type, because linenums="1" is a string and must also be dropped. Attributes such as data-x must still be kept. |
| major | `tests/test_syntax/extensions/test_fenced_code_bool_options.py`:63 | The new tests lock in the incorrect behaviour. They assert linenums="True" on <code>, the opposite of the issue's expected output, so they would pass with the bug and fail with a correct fix. | Lines 63-75 expect '<pre><code class="language-python" linenums="True">print(1)\n</code></pre>' for both '{ .python linenums }' and '{ .python linenums=true }'. The issue expects '<pre><code class="language-python">print(1)\n</code></pre>'. No test covers guess_lang, noclasses, linenums="1" or linenums=false, all of which the issue lists. |
| minor | `docs/changelog.md`:9 | The changelog entry describes the wrong behaviour. It says the option 'is now written to the <code> element', which contradicts the issue. It should say the options are ignored when codehilite is not enabled. | Lines 9-11: '...The option is now written to the `<code>` element like other attributes.' |

_The reviewer saw only the issue, the diff and the repository at this PR's head. A maintainer decides whether to merge._
