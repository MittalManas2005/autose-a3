---
artefact: review
pr: 17
issue: 4
round: 1
verdict: approve
target_stage: none
reviewer_model: sonnet
---

## AutoSE independent review (round 1)

**Verdict: approve**

The fix filters highlight-only options (linenums, guess_lang, noclasses, use_pygments, hl_lines) out of the `<code>` attributes when highlighting is not applied. The TypeError is gone, other attributes are kept, and the tests pass.

### What I verified
- `python -m unittest discover tests` passes: 1174 tests, 52 skipped.
- `python -m unittest tests.test_syntax.extensions.test_fenced_code` passes: 49 tests.
- flake8 is clean on the changed source and test files.
- `linenums`, `guess_lang`, `noclasses` and `hl_lines`, combined with `data-x="y"` and `use_pygments=false`, render `<pre><code class="language-python" data-x="y">`, so the extra attribute is kept.
- With codehilite enabled but `use_pygments=False`, a block with `linenums` and `data-x` renders with only `data-x`, with no crash.
- The new tests cover every option named in the issue plus `hl_lines`, and they check the exact expected HTML. They also cover attribute retention and unchanged behaviour with codehilite. No existing tests were changed.
- A changelog entry and a docs note were added. The only code change is in `fenced_code.py`, and no CI files were touched.

### Commands I ran (from the session transcript, not self-reported)
- `python -m unittest discover tests` (ok)
- `python -c "import markdown; print(markdown.markdown('''' { .python hl_lines=\"1 3\" linenums=\"1\" data-x=\"y\" use_pygments=false }\nprint(1)\n'''', extensions` (failed)
- `python -c "import markdown; print(markdown.markdown('''' { .python linenums=\"1\" data-x=\"y\" }\nprint(1)\n'''', extensions=[ 'fenced_code','attr_list','codehi` (failed)
- `python -m unittest tests.test_syntax.extensions.test_fenced_code` (ok)
- `python -c "import markdown; f=chr(96)*3; print(markdown.markdown(f+' { .python hl_lines=\"1 3\" linenums=\"1\" data-x=\"y\" use_pygments=false }\nprint(1)\n'+f,` (ok)
- `python -c "import markdown; f=chr(96)*3; print(markdown.markdown(f+' { .python linenums=\"1\" data-x=\"y\" }\nprint(1)\n'+f, extensions=['fenced_code','attr_lis` (ok)
- `python -m flake8 markdown/extensions/fenced_code.py tests/test_syntax/extensions/test_fenced_code.py` (ok)

### Findings

| severity | location | issue | evidence |
|---|---|---|---|
| — | — | — | — |

_The reviewer saw only the issue, the diff and the repository at this PR's head. A maintainer decides whether to merge._
