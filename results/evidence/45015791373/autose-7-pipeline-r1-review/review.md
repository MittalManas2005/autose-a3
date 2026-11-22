---
artefact: review
pr: 12
issue: 7
round: 1
verdict: approve
target_stage: none
reviewer_model: haiku
---

## AutoSE independent review (round 1)

**Verdict: approve**

The change fixes the reported bug: reference links whose label contains a code span (shortcut, full, and empty-id forms) now resolve to their definition. The full suite passes, the changed link modules pass, and flake8 is clean on the changed files. The remaining findings are minor and do not block merge.

### What I verified
- python -m unittest discover tests: 1176 tests, OK (skipped=52), run by me
- python -m unittest tests.test_syntax.inline.test_links tests.test_syntax.inline.test_links_code_label: 50 tests OK, run by me
- python -m flake8 on the four changed Python files: no output
- Probe: [`foo`] with def [`foo`] links with <code>foo</code>; [text][`foo`] links; [`foo`][] links
- Probe: [`foo`] with def [foo] does not link (correct, labels differ); [`Foo`] matches def [`foo`] (case-insensitive, consistent with plain refs)
- Probe: [a `b` c][`x` y] with matching def links and keeps the inner code span; [![`x`](i.png)][`foo`] links and keeps the image
- Probe: inline [`foo`](url) still works; undefined [`foo`] stays [<code>foo</code>]; image ref ![`foo`] output unchanged
- resolveLabel terminates: a stash source only references earlier placeholders, and unknown placeholders are left unchanged
- Compared with pre-existing behaviour: [see [a](x)][foo] already nests anchors on the base code, so nested output for autolink labels is the same pre-existing pattern
- ARCHITECTURE.md K1-K5: no signature or priority changes, placeholder text is read from the stash and never altered, public names unchanged

### Commands I ran (from the session transcript, not self-reported)
- `python -m unittest discover tests` (ok)
- `python -m unittest tests.test_syntax.inline.test_links tests.test_syntax.inline.test_links_code_label` (ok)
- `python -m flake8 markdown/inlinepatterns.py markdown/treeprocessors.py tests/test_syntax/inline/test_links.py tests/test_syntax/inline/test_links_code_label.py` (ok)
- `python -c "import markdown; print(markdown.markdown('['foo']\n\n['foo']: https://example.com\n'))"` (failed)
- `python -c "import markdown; print(markdown.markdown('[*foo*]\n\n[*foo*]: https://example.com\n\n[*foo*][x]\n\n[x]: https://b.example\n'))"` (ok)
- `python -c "import markdown; print(markdown.markdown('['foo']\n\n[foo]: https://example.com\n\n['Foo']\n\n['foo']: https://c.example\n'))"` (failed)
- `python -c "import markdown; print(markdown.markdown('[!['x'](i.png)]['foo']\n\n['foo']: https://example.com\n\n[a 'b' c]['x' y]\n\n[a 'b' c]: https://d.example\` (failed)
- `python -c "import markdown; print(markdown.markdown('[<http://a.example>]\n\n[<http://a.example>]: https://f.example\n\n['a']\n\n['a']: https://g.example \"T\"\` (failed)
- `python -c "import markdown; b=chr(96); print(markdown.markdown('['+b+'foo'+b+']\n\n[foo]: https://example.com\n\n['+b+'Foo'+b+']\n\n['+b+'foo'+b+']: https://c.e` (ok)
- `python -c "import markdown; b=chr(96); print(markdown.markdown('[!['+b+'x'+b+'](i.png)]['+b+'foo'+b+']\n\n['+b+'foo'+b+']: https://example.com\n\n[a '+b+'b'+b+'` (ok)
- `python -c "import markdown; b=chr(96); print(markdown.markdown('[<http://a.example>]\n\n[<http://a.example>]: https://f.example\n\n['+b+'a'+b+']\n\n['+b+'a'+b+'` (ok)
- `python -c "import markdown; b=chr(96); print(markdown.markdown('['+b+'a'+b+' ['+b+'b'+b+']]\n\n['+b+'a'+b+' '+b+'b'+b+']: https://z.example\n\n[x]['+b+'a'+b+']\` (ok)
- `git archive --format=tar --output=$TMPDIR/base.tar HEAD markdown` (denied)
- `python -c "import markdown; print(markdown.markdown('see [a](https://x.example) here\n\n[see [a](https://x.example)][foo]\n\n[foo]: https://y.example\n'))"` (ok)

### Findings

| severity | location | issue | evidence |
|---|---|---|---|
| minor | `markdown/inlinepatterns.py` | resolveLabel expands every inline placeholder in a reference label, not only code spans. Emphasis labels such as [*foo*] with def [*foo*] now link, which was not asked for. This matches CommonMark label matching, so it is probably acceptable but is wider than the issue. | Probe: markdown.markdown('[*foo*]\n\n[*foo*]: https://example.com') now gives <a href="https://example.com"><em>foo</em></a>. Base code did not link because the id was the placeholder text. |
| minor | `markdown/inlinepatterns.py` | An autolink inside a reference label now links to the definition and produces nested anchors. This is invalid HTML and CommonMark would not form a link here. | Probe: [<http://a.example>] with def [<http://a.example>]: https://f.example gives <a href="https://f.example"><a href="http://a.example">http://a.example</a></a>. Base output was bracketed text plus a separate autolink. The same nesting already occurs on base for [see [a](x)][foo] with def foo. |
| minor | `tests/test_syntax/inline/test_links_code_label.py` | The new test module duplicates the cases already added to test_links.py, copies the project license docstring, and uses AC-FR-* identifiers that refer to no artifact in the repository. Test names such as test_ac_fr_001_2 (plain inline link) are unrelated to the issue. | tests/test_syntax/inline/test_links_code_label.py:213-266 versus tests/test_syntax/inline/test_links.py:206-266 cover the same inputs. Module passes (50 tests OK with test_links). |
| minor | `tests/test_syntax/inline/test_links.py` | test_image_ref_code_in_label_unchanged locks in the broken output ![<code>foo</code>] for image references instead of leaving the behaviour unasserted. A later fix would have to change this test. | tests/test_syntax/inline/test_links.py test_image_ref_code_in_label_unchanged expects <p>![<code>foo</code>]</p>. |

_The reviewer saw only the issue, the diff and the repository at this PR's head. A maintainer decides whether to merge._
