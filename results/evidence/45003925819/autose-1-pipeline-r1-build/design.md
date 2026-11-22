---
artefact: design
issue: 1
files:
  - path: markdown/extensions/toc.py
    change: modify
    symbols: [TocTreeprocessor.run]
    new_symbols: []
  - path: docs/changelog.md
    change: modify
    symbols: []
    new_symbols: []
  - path: tests/test_syntax/extensions/test_toc.py
    change: modify
    symbols: [TestTOC]
    new_symbols: [TestTOC.testValuelessTocLabelIgnored]
tests: tests/test_syntax/extensions/test_toc.py
---

## Plan

### 1. `markdown/extensions/toc.py`, `TocTreeprocessor.run` (lines 406–412)
Current code:
```python
data_toc_label = ''
if 'data-toc-label' in el.attrib:
    data_toc_label = run_postprocessors(unescape(el.attrib['data-toc-label']), self.md)
    name = escape_cdata(strip_tags(data_toc_label))
    del el.attrib['data-toc-label']
```
`attr_list` stores a valueless word as `None` (`attr_list.py`, `_handle_word` returns `t, None`), so `unescape(None)` reaches `re.sub` on `None` and raises the reported `TypeError` (`treeprocessors.py:469-470`, called from `toc.py:408`).

Planned change:
```python
data_toc_label = ''
if 'data-toc-label' in el.attrib:
    label = el.attrib['data-toc-label']
    # attr_list stores a valueless attribute as None: treat it as empty, so the heading text is kept.
    if label is not None:
        data_toc_label = run_postprocessors(unescape(label), self.md)
        # Overwrite name with sanitized value of `data-toc-label`.
        name = escape_cdata(strip_tags(data_toc_label))
    # Remove the data-toc-label attribute as it is no longer needed
    del el.attrib['data-toc-label']
```
- The `del` moves out of the `None` check so that the valueless attribute is removed from the heading as well. Without this, the bare `data-toc-label` would be serialized into the heading (`serializers.py:186-189` renders `None` as a bare name). This covers AC-FR-002-3.
- For the `None` case `data_toc_label` stays `''` and `name` stays the heading text (`strip_tags(innerhtml)`). The `toc_tokens` entry therefore reads `'data-toc-label': ''`, the same as for a heading with no label (see the existing expectations in `test_toc.py`, e.g. line 176). This covers AC-FR-002-1 and AC-FR-002-2.
- The `""` path (`data-toc-label=""`) is unchanged, because `''` is not `None` (ASM-001, Q-001).
- The `valued` path (`data-toc-label="Short"`) is unchanged (AC-FR-002-4, SRC-005).
- AC-FR-001-1 (no exception) is satisfied by the `None` guard.

### 2. `docs/changelog.md`, `[Unreleased]` → `### Fixed` (line 17 onward)
Add one bullet, for example: "Fix a crash in the `toc` extension when a heading has a valueless `data-toc-label` attribute with `attr_list`. The empty label is now ignored." Required because the change is under `markdown/`.

### 3. `tests/test_syntax/extensions/test_toc.py`, class `TestTOC` (line 28)
Add one method, `testValuelessTocLabelIgnored`, next to `testCustomLabelAttributeWithAngleBracket` (line 182). Use `assertMarkdownRenders` (or `markdown.markdown` plus `Markdown.toc`):
- Input `# Heading {: data-toc-label }`, extensions `[TocExtension(), 'attr_list']`:
  - output contains `<h1 id="heading">Heading</h1>` (AC-FR-002-1);
  - output does not contain `data-toc-label` (AC-FR-002-3);
  - no exception (AC-FR-001-1, covered by the test running at all);
  - `md.toc` contains `<li><a href="#heading">Heading</a></li>` (AC-FR-002-2).
- Preservation, input `# Heading {: data-toc-label="Short" }`: `md.toc` contains `<li><a href="#heading">Short</a></li>` (AC-FR-002-4). This is already covered by the existing test at lines 182–203 (`Python support` with a valued label). Adding this case in the new test keeps the valueless and valued behaviour side by side.

The changelog entry and the test are the only non-code changes. `docs/extensions/toc.md` is not changed: its text about `data-toc-label` (EV-004) stays accurate.

## Constraints respected
- **K1 (stage interfaces):** no processor signature or return value changes. `TocTreeprocessor.run` still returns `None`.
- **K2 (registries and priorities):** no new processor and no priority change. `toc` stays at 5 (`toc.py:511`). The fix is local to the existing processor.
- **K3 (attribute values are `str` or `None`):** the code that reads `data-toc-label` now handles `None`. No non-string value is written.
- **K4 (stash and placeholders):** `run_postprocessors` still runs on non-`None` labels, so `RawHtmlPostprocessor` placeholders behave as before. The `None` path does not touch placeholders.
- **K5 (backward compatibility):** no public name, option, or entry point changes. Only the crash is removed. Valued and empty-string labels produce the same output as before.
- **Changelog rule:** `[Unreleased]` entry added (`docs/changelog.md:15-17`).
- **Test rule:** a test for the new behaviour is added under `tests/test_syntax/extensions/`. The suite runs with `python -m unittest discover tests`, not pytest.
- **flake8:** the line length limit is 119. The new lines are well within it.

## ARCHITECTURE.md vs source
Verified by reading the source (I could not run code in this session, so no `(run)` checks):
- `toc` tree processor registered at priority 5: `markdown/extensions/toc.py:511` (`md.treeprocessors.register(tocext, 'toc', 5)`). **Matches.**
- `attr_list` tree processor registered at priority 8: `markdown/extensions/attr_list.py:239`. **Matches.**
- `toc` calls `unescape` on attribute values it reads: `toc.py:408` (`data-toc-label`) and `toc.py:417` (`id`). **Matches.**
- `UnescapeTreeprocessor.unescape` is a plain `RE.sub` on its input: `treeprocessors.py:469-470`. The `None` crash comes from here. **Matches the crash described in the spec (SRC-004).**
- `attr_list` returns valueless words with value `None` (`attr_list.py`, `_handle_word`, and `get_attrs_and_remainder` docstring). **Matches.**
- The serializer writes `None` as a bare attribute name: `serializers.py:186-196`. **Matches.**
- Non-string, non-`None` values raise `TypeError` (`serializers.py:80-83`). **Not re-verified in this session; I did not read those lines.**
- Only `toc.py` reads `data-toc-label` in `markdown/` (`toc.py:407-420`). **Confirmed by grep. No other reader.**
- Discrepancies: none found for the claims above. The spec's EV-001 line numbers (407–408) match the source.

## Risks
- **Attribute removal must happen on the `None` path.** If the `del` stayed inside the valued branch, AC-FR-002-3 would fail (`data-toc-label` in the output). The plan moves it out.
- **Behaviour for `data-toc-label=""` is untouched.** If maintainers answer Q-001 with "ignore `\"\"` too", the guard has to change to `if not label:` (or similar), and the test needs a case for it. This is a non-blocking open question.
- **Expected strings are not executed.** AC-FR-002-1 and -2 assume `attr_list` attaches the attribute before `toc` runs (8 before 5, so it does), and that `id` is `heading`. I could not run the reproduction here (shell access was denied). The test stage must confirm the exact strings. If the output differs (for example, an extra attribute or whitespace), adjust the expected string to the real output and say so in the test, not the code.
- **The `toc_tokens` `data-toc-label` value** for a valueless label is `''`. This is a choice I made to match "as if the attribute were not present". Nothing in the ACs checks the token value, so a change there would not break the spec.
- **Other attributes set without a value** (ASM-002) are out of scope. Other extensions that read `None` attributes may have the same problem, but this design does not change them.

## AutoSE stage check: names the files and functions to change

Result: **PASS**

- all checks passed
