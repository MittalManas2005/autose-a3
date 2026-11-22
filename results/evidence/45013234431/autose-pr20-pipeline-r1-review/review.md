---
artefact: review
pr: 20
issue: 4
round: 1
verdict: request_changes
target_stage: implementation
reviewer_model: sonnet
---

## AutoSE independent review (round 1)

**Verdict: request changes** (back to **implementation**)

The crash is fixed, but the fix does the opposite of what the issue asks. Without codehilite, `linenums` and the other highlighting-only options are written onto `<code>` as attributes instead of being ignored.

### What I verified
- `python -m unittest discover tests` passes (1169 tests, 52 skipped)
- Read the diff: the change only stringifies None as 'True' in the kv_pairs join at fenced_code.py:~160
- The new tests assert `linenums="True"` in the output, which contradicts the issue's expected behaviour
- I did not run my own probes of the rendered HTML; the Bash sandbox rejected the backtick-containing commands I tried. The finding rests on the diff and the new tests' expected output.

### Commands I ran (from the session transcript, not self-reported)
- `python -m unittest discover tests` (ok)
- `python -c "import markdown; print(markdown.markdown('''' { .python linenums guess_lang=false noclasses data-x=\"y\" }\nprint(1)\n'''', extensions=['fenced_code'` (failed)
- `python -c "import markdown; print(markdown.markdown(open('.autose_review/issue.md').read().split(''''python')[0][:0] + chr(96)*3 + ' { .python linenums guess_la` (failed)

### Findings

| severity | location | issue | evidence |
|---|---|---|---|
| blocker | `markdown/extensions/fenced_code.py`:160 | The issue says that without codehilite, linenums, linenums=true, linenums="1", guess_lang and noclasses should be ignored, and the block rendered exactly as if they had not been written. Other attributes such as data-x should still be kept. The patch instead emits them as attributes, e.g. `linenums="True"`, so the output differs from the plain block. The patch also does not remove the other highlighting keys, and it is unclear that `linenums="1"` or `guess_lang`/`noclasses` are handled correctly. | The diff turns None into 'True' and writes every key except use_pygments. The new test expects `<pre><code class="language-python" linenums="True">print(1)\n</code></pre>`, where the issue expects `<pre><code class="language-python">print(1)\n</code></pre>`. |
| major | `tests/test_syntax/extensions/test_fenced_code_bool_options.py`:63 | The tests encode the wrong behaviour, and the changelog describes it too ("written to the `<code>` element"). There are no tests for `linenums="1"`, `guess_lang` or `noclasses`. There is no test that a block with these options renders identically to one without, and no test that data-x is kept alongside them. | All three tests expect `linenums="True"` or only data-x; none compares against the output of a block without the options. |

_The reviewer saw only the issue, the diff and the repository at this PR's head. A maintainer decides whether to merge._
