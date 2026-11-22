---
artefact: review
pr: 21
issue: 5
round: 1
verdict: request_changes
target_stage: implementation
reviewer_model: haiku
---

## AutoSE independent review (round 1)

**Verdict: request changes** (back to **implementation**)

The notoc exclusion works as the issue describes: the class is honoured, the heading keeps its id and rendering, and it is left out of both the TOC and md.toc_tokens. However, the PR also changes how every explicitly set attr_list id is handled, which breaks existing custom anchors and is outside the issue. It also deletes an existing regression test that would have caught this. Request changes.

### What I verified
- python -m unittest discover tests: Ran 1166 tests, OK (skipped=52) at PR head. This passes only because test_escaped_char_in_attr_list was deleted.
- Issue example `# One / ## Two {: .notoc } / ## Three`: the TOC contains One and Three only; the h2 renders as `<h2 class="notoc" id="two">Two</h2>`; md.toc_tokens ids are ['one'] (Two is excluded).
- Multiple classes: `### Sub {: .notoc .other }` is excluded from the TOC and keeps class "notoc other".
- Custom ids: `# Intro { #my_custom.id }` renders id "my_customid" (base code kept the id as written). `## Sub {: #Some_Id }` with `[link](#Some_Id)` renders id "some_id", so the link is a dead anchor.

### Commands I ran (from the session transcript, not self-reported)
- `python -m unittest discover tests` (ok)
- `python -c "import markdown; print(markdown.markdown(r'# '*Foo*' { id=\"\*Foo\*\" }', extensions=['toc', 'attr_list']))"` (failed)
- `python -c "import markdown; m=markdown.Markdown(extensions=['toc','attr_list']); print(m.convert('[TOC]\n\n# One\n\n## Two {: .notoc }\n\n## Three')); print([t[` (ok)
- `python -c "import markdown; m=markdown.Markdown(extensions=['toc','attr_list']); print(m.convert('# Intro { #my_custom.id }\n\n## Sub {: #Some_Id }\n\n[link](#S` (ok)
- `python -c "import markdown; m=markdown.Markdown(extensions=['toc','attr_list']); print(m.convert('## Two {: .notoc #x }\n\n## Dup {: #x }\n\n### Sub {: .notoc .` (ok)

### Findings

| severity | location | issue | evidence |
|---|---|---|---|
| major | `markdown/extensions/toc.py`:406 | The new `else` branch rewrites every pre-set id from attr_list through slugify, not only ids on notoc headings. Explicit ids are no longer kept as written, so existing anchors and links break, and headings with other classes no longer behave as before. The issue asks that the heading's id be rendered normally and that other headings behave exactly as today. | Probe on PR head: `# Intro { #my_custom.id }` gives `<h1 id="my_customid">`. `## Sub {: #Some_Id }` plus `[link](#Some_Id)` gives `<h2 id="some_id">`, and the link still points at `#Some_Id` (dead anchor). Base code only set an id when none existed, so these ids were emitted verbatim. |
| major | `tests/test_syntax/extensions/test_toc.py`:1079 | The PR deletes the existing test `test_escaped_char_in_attr_list`, which asserts that an attr_list id `\*Foo\*` is emitted and linked as `*Foo*`. Deleting it hides the regression from the id change above and makes the green suite misleading. The test was not weakened or replaced; it was removed without justification. | The diff removes lines 73-97 of tests/test_syntax/extensions/test_toc.py (expected `<h1 id="*Foo*">` and `href="#*Foo*"`). With the new slugify branch that id is normalised, so the original expectation no longer holds. The suite passes only because the test is gone. |

_The reviewer saw only the issue, the diff and the repository at this PR's head. A maintainer decides whether to merge._
