---
artefact: review
pr: 21
issue: 5
round: 1
verdict: request_changes
target_stage: implementation
reviewer_model: sonnet
---

## AutoSE independent review (round 1)

**Verdict: request changes** (back to **implementation**)

The notoc exclusion itself works, but the PR also changes how ids set with attr_list are emitted, which the issue did not ask for, and it deletes an existing test that this change broke.

### What I verified
- python -m unittest discover tests passes (1166 tests, OK), but only because test_escaped_char_in_attr_list was deleted
- A `## Two {: .notoc }` heading is omitted from the TOC and renders with its id
- The new test covers the issue's example

### Commands I ran (from the session transcript, not self-reported)
- `python -m unittest discover tests` (ok)
- `python -c "import markdown; print(markdown.markdown('# One { id=\"My_Id\" }\n\n## Two {: .notoc id=\"A B\" }', extensions=['toc','attr_list']))"` (ok)

### Findings

| severity | location | issue | evidence |
|---|---|---|---|
| blocker | `markdown/extensions/toc.py`:405 | The new else branch slugifies ids set explicitly with attr_list. This is an unrelated behaviour change to heading ids and breaks backward compatibility. The issue says headings with other classes must behave exactly as today and that existing links must keep working. | Input `# One { id="My_Id" }` now renders `<h1 id="my_id">`, and `{: id="A B" }` renders `id="a-b"`. Before the change, explicit ids were preserved as written. |
| major | `tests/test_syntax/extensions/test_toc.py`:73 | The existing test test_escaped_char_in_attr_list was deleted. It had been passing before the PR and the new id-slugify code would make it fail, so removing it hides the regression. | The diff removes the test, which asserted `{ id="\*Foo\*" }` yields `id="*Foo*"` and a matching TOC entry. |

_The reviewer saw only the issue, the diff and the repository at this PR's head. A maintainer decides whether to merge._
