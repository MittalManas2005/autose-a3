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

PR #12 fixes reference links whose label contains a code span (`[`code`]`, `[`code`][]) by matching the label against the raw source of the definition. The fix is correct for the reported case and has no regression path I could find: the change can only turn previously unmatched lookups into matches. The full suite passes, flake8 is clean, and the changelog is updated. Remaining points are minor test-style and edge-case notes.

### What I verified
- Read the issue (#7) and the full diff; the change touches only changelog.md, inlinepatterns.py, treeprocessors.py and test_links.py.
- Ran `python -m unittest discover tests` myself: Ran 1179 tests, OK (skipped=52).
- Ran `python -m flake8` on the three changed Python files: no output (clean).
- Probed `[`code`]` + `[`code`]: /url`, `[`code`][]`, mixed case `[`Code`]`, undefined `[code]` definition (stays unlinked, as before), `[text][ref]` plain text, and inline `[`code`](/url)`: all render as expected.
- Probed multi-code-span labels (`[`a` `b`][]`), labels mixing emphasis and code (`[*x* `y`]`), double-backtick spans, and image references `![`code`][ref]` (alt="code"): all correct.
- Probed HTML inside code spans in labels (`[`<b>`][]`): code text is escaped and the href/title come from the definition only; no escaping regression.
- Reasoned through regressions: `raw_label` only changes the lookup key, and previously the key was a placeholder string that could never match a definition, so no previously-working link can stop resolving.

### Commands I ran (from the session transcript, not self-reported)
- `python -m unittest discover tests` (ok)
- `python -c "import markdown; print(markdown.markdown('!['code'][ref]\n\n[ref]: /img.png'))"` (failed)
- `python -c "import markdown; print(markdown.markdown('[a 'b' c]\n\n[a 'b' c]: /u\n\n[*x* 'y']\n\n[*x* 'y']: /v\n\n['a' 'b'][]\n\n['a' 'b']: /w\n\n[''a'']\n\n[''a` (failed)
- `python -m flake8 markdown/treeprocessors.py markdown/inlinepatterns.py tests/test_syntax/inline/test_links.py` (ok)
- `python -c "import markdown; print(markdown.markdown('['code']\n\n['code']: /url\n\n['code'][]\n\n['code']: /url2', extensions=['attr_list']))"` (failed)
- `python -c 'import markdown; print(markdown.markdown("!['code'][ref]\n\n[ref]: /img.png"))'` (ok)
- `python -c 'import markdown; print(markdown.markdown("[a 'b' c]\n\n[a 'b' c]: /u\n\n[*x* 'y']\n\n[*x* 'y']: /v\n\n['a' 'b'][]\n\n['a' 'b']: /w\n\n[''a'']\n\n[''a` (ok)
- `python -c 'import markdown; print(markdown.markdown("['code']\n\n['code']: /url\n\n['x']: /nothere\n\n['Y' text][ref]\n\n[ref]: /r", extensions=["attr_list"]))'` (ok)
- `python -c 'import markdown; print(markdown.markdown("['a]b']\n\n['a]b']: /u\n\n['<b>'][]\n\n['<b>']: /v \"t\"\n\n['x'\\]\n\n['x'\\]: /esc\n\n['x']: <javascript:` (ok)

### Findings

| severity | location | issue | evidence |
|---|---|---|---|
| minor | `tests/test_syntax/inline/test_links.py`:193 | The new `TestCodeSpanLinkAcceptance` class uses `markdown.markdown(...)` with `assertIn` instead of the repo's `assertMarkdownRenders` convention, and its test names and docstrings embed internal acceptance-criteria IDs (AC-FR-001-1, AC-NFR-001-1) that mean nothing in upstream. It also overlaps with the tests already added to `TestReferenceLinks`. | test_links.py:193-225 duplicate cases already covered at lines 437-552 (e.g. test_ref_link_code_span_text vs test_ac_fr_001_1_reference_code_span_label_becomes_link). assertIn passes even if the surrounding markup is wrong. |
| minor | `markdown/inlinepatterns.py`:1231 | `raw_label` catches only KeyError. If an extension replaces the 'inline' treeprocessor with one that lacks `stashed_source`, this raises AttributeError on every reference label. Existing code at lines 238 and 533 has the same assumption about `stashed_nodes`, so this is a consistency nit, not a new hazard. | inlinepatterns.py:1231 `source = self.md.treeprocessors['inline'].stashed_source` with only `except KeyError`. |
| minor | `tests/test_syntax/inline/test_links.py`:108 | Not fixed and not tested: a code span containing `]` (or `\]`) in a label, such as `[`a]b`]` with a matching `[`a]b`]: /u` definition, still does not link. The cause is the definition regex stopping at the first `]` (blockprocessors ReferenceProcessor), not this change. It is outside the issue's scope, but worth a follow-up note. | Probe: markdown.markdown('[`a]b`]\n\n[`a]b`]: /u') renders `<p>[<code>a]b</code>]</p>` followed by the definition line as a paragraph. |

_The reviewer saw only the issue, the diff and the repository at this PR's head. A maintainer decides whether to merge._
