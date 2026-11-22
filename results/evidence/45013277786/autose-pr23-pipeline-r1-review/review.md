---
artefact: review
pr: 23
issue: 7
round: 1
verdict: request_changes
target_stage: implementation
reviewer_model: haiku
---

## AutoSE independent review (round 1)

**Verdict: request changes** (back to **implementation**)

The core fix works for ordinary code labels, but it does not handle code labels containing HTML-special characters (< > &), and the PR includes an unrelated CI change that disables a changelog gate. Both need fixing before merge.

### What I verified
- python -m unittest discover tests: Ran 1169 tests, OK (skipped=52)
- python -m unittest tests.test_syntax.inline.test_reference_code_labels: 3 tests OK
- python -m flake8 on markdown/inlinepatterns.py and the new test file: clean
- Probe: [`foo`] with def [`foo`] links correctly
- Probe: [`Foo`] with def [`foo`] links correctly (case-insensitive)
- Probe: [text][`foo`] links correctly; [`x`][`foo`] with code in text links correctly
- Probe: [*a* `b`] with the same-label def links correctly
- Probe FAILS: label with a less-than sign, def [`a<b`] -> output <p>[<code>a&lt;b</code>]</p>, not linked
- Probe FAILS: label with an ampersand, def [`a&b`] -> output <p>[<code>a&amp;b</code>]</p>, not linked
- Changelog entry under Unreleased/Fixed is present and accurate

### Commands I ran (from the session transcript, not self-reported)
- `python -m unittest discover tests` (ok)
- `python -m unittest tests.test_syntax.inline.test_reference_code_labels` (ok)
- `python -m flake8 markdown/inlinepatterns.py tests/test_syntax/inline/test_reference_code_labels.py` (ok)
- `python -c "import markdown; print(markdown.markdown('['a<b']\n\n['a<b']: https://example.com'))"` (failed)
- `python -c "import markdown; print(markdown.markdown('['a&b']\n\n['a&b']: https://example.com'))"` (failed)
- `python -c "import markdown; print(markdown.markdown('['Foo']\n\n['foo']: https://example.com'))"` (failed)
- `python -c "import markdown; print(markdown.markdown('[*a* 'b']\n\n[*a* 'b']: https://example.com'))"` (failed)
- `python -c "import markdown; print(markdown.markdown('[text]['foo'] and ['x']['foo']\n\n['foo']: https://example.com'))"` (failed)
- `python -c "import markdown; print(markdown.markdown('['foo']\n\n['foo']: https://example.com'))"` (failed)
- `python -c 'import markdown; print(markdown.markdown("['a<b']\n\n['a<b']: https://example.com"))'` (ok)
- `python -c 'import markdown; print(markdown.markdown("['a&b']\n\n['a&b']: https://example.com"))'` (ok)
- `python -c 'import markdown; print(markdown.markdown("['Foo']\n\n['foo']: https://example.com"))'` (ok)
- `python -c 'import markdown; print(markdown.markdown("[*a* 'b']\n\n[*a* 'b']: https://example.com"))'` (ok)
- `python -c 'import markdown; print(markdown.markdown("[text]['foo'] and ['x']['foo']\n\n['foo']: https://example.com"))'` (ok)
- `python -c 'import markdown; print(markdown.markdown("['foo']\n\n['foo']: https://example.com"))'` (ok)
- `python -c 'import markdown; print(markdown.markdown("['a&amp;b']\n\n['a&amp;b']: https://example.com"))'` (ok)

### Findings

| severity | location | issue | evidence |
|---|---|---|---|
| major | `markdown/inlinepatterns.py`:1240 | _label_source() rebuilds the inline-code text from the stashed code element's .text, which is already HTML-escaped (code_escape runs when the span is stashed). For labels containing <, > or & the rebuilt id never matches the raw reference definition, so the link is still dropped and the brackets show as literal text. This is the same symptom the issue reports, left unfixed for a common class of code labels such as List<int> or a&&b. The rebuilt text should be unescaped (for example with html.unescape) before lookup, and tests should cover these characters. | python -c 'import markdown; print(markdown.markdown("[`a<b`]\n\n[`a<b`]: https://example.com"))' outputs <p>[<code>a&lt;b</code>]</p>; expected <p><a href="https://example.com"><code>a&lt;b</code></a></p>. The same happens with [`a&b`], which outputs <p>[<code>a&amp;b</code>]</p>. The new tests use only plain identifiers, so they do not catch this. |
| major | `.github/workflows/changelog-enforcer.yml`:9 | The diff adds continue-on-error: true to the changelog-enforcer CI step. This is unrelated to the issue, changes a CI file (which the repository rules forbid), and turns a required check into a non-blocking one. | diff.patch lines 5-10: '+      # Do not block pull requests on changelog formatting.' and '+      continue-on-error: true' added to the Ensure Changelog Entry Made step. Revert this hunk. |

_The reviewer saw only the issue, the diff and the repository at this PR's head. A maintainer decides whether to merge._
