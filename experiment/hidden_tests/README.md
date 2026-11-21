# Hidden acceptance tests

Evaluation material for the five issues in `experiment/issues/`. **None of this is ever placed in the fork** (`MittalManas2005/markdown`), given to any AutoSE agent, or mentioned in a prompt. The agents see only the issue text and the fork.

| Issue | Type | Tests | Preservation tests (pass before and after a fix) |
|---|---|---|---|
| 1 — TOC crash on a valueless `{: id }` | bug | 4 | `test_explicit_id_is_still_respected` |
| 2 — fenced code `linenums` crash without codehilite | bug | 3 (one with 4 subtests) | `test_custom_attributes_are_still_passed_through` |
| 3 — exclude a heading from the TOC with `.notoc` | feature | 4 | `test_notoc_heading_is_still_rendered_with_its_id`, `test_other_classes_do_not_exclude_headings` |
| 4 — CLI `--tab_length` option | feature | 3 | `test_default_behaviour_is_unchanged` |
| 5 — "links with code don't work" (vague; reference labels containing backticks) | vague | 4 | `test_undefined_code_label_stays_literal` |

Every test checks behaviour stated in its issue, through the public API (`markdown.markdown`, `markdown.Markdown`, `toc_tokens`) or the command line. For issue 5, the behaviour is stated in the scripted maintainer answer (`experiment/issues/issue_5_maintainer_answer.md`).

## Running against a pull request

```bash
git clone https://github.com/MittalManas2005/markdown.git /tmp/pr && cd /tmp/pr && git checkout <pr-branch>
python3 -m venv .venv && .venv/bin/pip install -e '.[testing]'
/path/to/autose-a3/experiment/hidden_tests/run_hidden.sh /tmp/pr <issue-number> /tmp/pr/.venv/bin/python
```

## Validation (were the tests meaningful?)
`validate_hidden.sh <clone-of-Python-Markdown> <python>` checks four things for each issue:
1. checks out the pinned commit `3f2c551` in a temporary worktree;
2. runs the hidden tests, which must fail (preservation tests pass);
3. applies the private reference fix from `reference_fixes/` and runs them again, which must all pass;
4. runs the repository's own suite with the fix, which must stay green.

Result on 2026-11-22 (Python 3.12.9, macOS):

| Issue | At pin | With reference fix | Repository suite with fix |
|---|---|---|---|
| 1 | FAILED (errors=3) | OK | OK |
| 2 | FAILED (errors=5) | OK | OK |
| 3 | FAILED (failures=2) | OK | OK |
| 4 | FAILED (failures=2) | OK | OK |
| 5 | FAILED (failures=3) | OK | OK |

### Fairness checks (2026-11-22)
| Check | Result | What it shows |
|---|---|---|
| Fresh clone of the fork, Python 3.11 and 3.14, no Pygments | Same verdicts as above for all 5 issues; repository suite `OK (skipped=13)` | The results don't depend on the Python version or a local environment |
| Upstream's later code (`origin/master` = `5609061`) | Issue 1 **OK**; issues 2–5 fail | Upstream independently fixed issue 1 after the pin (`dc26ab5`), and that fix satisfies our tests, so the expected behaviour matches the maintainers' own choice. Issues 2–5 are unfixed upstream. |
| Issue 2, alternative correct fix (drop non-string values) | OK | The tests are not tied to one implementation |
| Issue 2, wrong fix (render booleans as `linenums="True"`) | FAILED (failures=5); repository suite OK | The tests reject a fix that contradicts the issue, even when the repository's own suite passes |
| Issue 5, alternative design (compare labels with backticks stripped) | OK | The tests are not tied to one implementation |
| Issue 1, partial fix (no crash, but no generated id) | FAILED (failures=3); repository suite OK | The tests enforce the behaviour the issue states ("gets the normal auto-generated id and shows up in the table of contents") |

The first version of the issue-4 reference fix broke 11 existing tests (`tests/test_apis.py`, `TestCliOptionParsing`). Those tests assert the exact default options dictionary. The fix was rewritten to add `tab_length` only when the option is given. An agent working on issue 4 will meet the same constraint.

## Reference fixes (private; used only for validation)
- `issue_1.patch`: the code part of upstream commit `dc26ab5` ("Fix toc crash on a heading with a valueless id attribute"), made after the pin.
- `issue_2.patch` … `issue_5.patch`: written for this project; there is no upstream fix at the time of writing.

They show that the hidden tests can be satisfied. They are not the only correct fixes.

## Environment notes
- The repository's skipped-test count depends on the environment. With Pygments installed but `PYGMENTS_VERSION` unset, 60 codehilite tests are skipped (72 skips in total), against 13 without Pygments. Compare test counts only within one environment.
- Issue 4's tests start a subprocess: `python -m markdown`, with the checkout under test on `PYTHONPATH`.
