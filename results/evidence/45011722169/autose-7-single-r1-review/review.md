---
artefact: review
pr: 18
issue: 7
round: 1
verdict: request_changes
target_stage: implementation
reviewer_model: sonnet
---

## AutoSE independent review (round 1)

**Verdict: request changes** (back to **implementation**)

The fix works for the reference-link cases I tried, but the PR also commits a leftover debugging file, tests/scratch_probe_issue7.py. It is unrelated to the change and deliberately fails when run.

### What I verified
- `python -m unittest discover tests` passes: 1170 tests, 52 skipped. The scratch file is not named test_*.py, so discovery never runs it.
- A code-span label resolves for `[`a`][1]`, `[`a b`]` and `[`a`][]` against a matching definition. A label containing `<` and `&` also resolves.
- An undefined `[`code`]` stays literal text.
- The stray `[]` in `[a][1] [a b] [a][]` also appears with plain-text labels, so it is existing behaviour and not caused by this PR.
- flake8 is clean on `markdown`, the changed test module and the scratch file.
- The changelog entry is present.

### Commands I ran (from the session transcript, not self-reported)
- `python -m unittest discover tests` (ok)
- `python -c "import markdown; print(markdown.markdown('['a'][1] and ['a'][]\n\n[1]: http://x\n['a']: http://y'))"` (failed)
- `python -c "import markdown; print(markdown.markdown('['a'][1]\n\n[1]: http://x'))"` (failed)
- `python -c "import markdown; b=chr(96); print(markdown.markdown('[%sa%s][1] [%sa b%s] [%sa%s][]\n\n[1]: http://x\n[%sa b%s]: http://y\n[%sa%s]: http://z' % ((b,)` (ok)
- `python -c "import markdown; b=chr(96); print(markdown.markdown('[x %sa<&b%s y]\n\n[x %sa<&b%s y]: http://x' % ((b,)*4)))"` (ok)
- `python -c "import markdown; b=chr(96); print(markdown.markdown('x [%sa%s][]\n\n[%sa%s]: http://z' % ((b,)*4)))"` (ok)
- `python -c "import markdown; print(markdown.markdown('x [a][] [b]\n\n[a]: http://z\n[b]: http://y'))"` (ok)
- `python -c "import markdown; print(markdown.markdown('[a][1] [a b] [a][]\n\n[1]: http://x\n[a b]: http://y\n[a]: http://z'))"` (ok)
- `python -m flake8 markdown tests/test_syntax/inline/test_links.py tests/scratch_probe_issue7.py` (ok)

### Findings

| severity | location | issue | evidence |
|---|---|---|---|
| major | `tests/scratch_probe_issue7.py`:1 | A scratch probe script was committed to the repository. It is an unrelated file in the test tree. Its `test_probe` ends with `self.fail('probe')` and prints output for 26 inputs. `python -m unittest tests.scratch_probe_issue7` or an IDE test runner would run it and report a failure. | diff.patch adds tests/scratch_probe_issue7.py (40 lines) with `self.fail('probe')`. The file exists at the PR head. |
| minor | `tests/test_syntax/inline/test_links.py`:117 | The new test names and docstrings use internal spec IDs (`test_ac_fr_001_1`, `AC-FR-001-1`). The repository's tests don't use that convention. The tests also don't cover mixed text and code in a label, or labels whose code contains special characters such as `&`, `<` or backticks. The new `code_span_source` function handles those cases. | tests/test_syntax/inline/test_links.py lines 117-155. |

_The reviewer saw only the issue, the diff and the repository at this PR's head. A maintainer decides whether to merge._
