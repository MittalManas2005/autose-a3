---
artefact: design
issue: 25
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
    symbols: []
    new_symbols: [TestTOC.testValuelessCustomLabelAttribute, TestTOC.testCustomLabelAttributeWithValue]
tests: tests/test_syntax/extensions/test_toc.py
---

# Design for issue #25: `toc` + `attr_list` TypeError on a valueless `data-toc-label`

## Plan

### Root cause (verified by reading the source)
- `attr_list` stores a valueless attribute as `None`: `markdown/extensions/attr_list.py:208-212` (`elem.set(name, None)` for non-boolean attributes). `{: data-toc-label }` therefore produces `el.attrib['data-toc-label'] is None`.
- `TocTreeprocessor.run` tests only key presence (`markdown/extensions/toc.py:407`) and then passes the value straight into `unescape(...)` (`toc.py:408`). `unescape(None)` fails with the reported `TypeError`. The attribute is also never removed on that path, because the `del` at `toc.py:412` is not reached.

### Change 1: `markdown/extensions/toc.py`, `TocTreeprocessor.run` (lines 406-412)
Read the raw value, remove the attribute, and apply the label only when the value is a string. A `None` value falls back to the heading text. The current block:

```python
data_toc_label = ''
if 'data-toc-label' in el.attrib:
    data_toc_label = run_postprocessors(unescape(el.attrib['data-toc-label']), self.md)
    # Overwrite name with sanitized value of `data-toc-label`.
    name = escape_cdata(strip_tags(data_toc_label))
    # Remove the data-toc-label attribute as it is no longer needed
    del el.attrib['data-toc-label']
```

becomes:

```python
data_toc_label = ''
if 'data-toc-label' in el.attrib:
    raw_label = el.attrib['data-toc-label']
    # Remove the data-toc-label attribute as it is no longer needed
    del el.attrib['data-toc-label']
    # A valueless attribute is stored as None by attr_list. Ignore it, so the
    # name keeps the heading text.
    if raw_label is not None:
        data_toc_label = run_postprocessors(unescape(raw_label), self.md)
        # Overwrite name with sanitized value of `data-toc-label`.
        name = escape_cdata(strip_tags(data_toc_label))
```

Effect per acceptance criterion:
- **AC-FR-001-1 (no error):** `None` no longer reaches `unescape`.
- **AC-FR-001-2 (TOC name is "Setup"):** `name` keeps the value computed at `toc.py:400` from the heading's inner HTML, `"Setup"`.
- **AC-FR-001-3 (`<h2 id="setup">Setup</h2>`):** the ID is set earlier, at `toc.py:403-404`, from the heading text. The attribute is deleted, so it is not serialised.
- **AC-FR-001-4 (`href="#setup"`):** the TOC link uses the item ID (`toc.py:375`), which is unchanged.
- **AC-FR-002-1 and -2 (non-empty label is preserved):** the `is not None` branch runs the same code as before for any string value, so `'Custom'` behaves exactly as now.

Explicit empty values (`data-toc-label=''`) are not changed. They are strings, so they follow the existing path, which yields `name == ''`. This matches ASM-001 and Q-001 in the spec.

Priority and registration are not touched (K2).

### Change 2: `docs/changelog.md`, `## [Unreleased]` → `### Fixed` (line 17)
Add one bullet at the end of the existing `### Fixed` list, for example:

```
* Ignore a valueless `data-toc-label` attribute in the `toc` extension, so the
  Table of Contents entry uses the heading text instead of raising `TypeError`
  when `attr_list` is enabled.
```

No issue or PR number is cited, because the fork's issue numbers are not upstream references.

### Change 3: `tests/test_syntax/extensions/test_toc.py`, class `TestTOC` (class at line 28)
Add two methods next to `testCustomLabelAttributeWithAngleBracket` (line 182), using the same `assertMarkdownRenders` and `expected_attrs` pattern and `extensions=[TocExtension(), 'attr_list']`:

1. `testValuelessCustomLabelAttribute`: source `## Setup {: data-toc-label }`.
   - Expected HTML: `<h2 id="setup">Setup</h2>` (AC-FR-001-3).
   - Expected `toc`: `<div class="toc">\n<ul>\n<li><a href="#setup">Setup</a></li>\n</ul>\n</div>\n` (AC-FR-001-4).
   - Expected `toc_tokens`: one entry with `level` 2, `id` `'setup'`, `name` `'Setup'`, `html` `'Setup'`, `data-toc-label` `''`, `children` `[]` (AC-FR-001-2).
   - `AC-FR-001-1` (no exception) is covered by the test not erroring.
2. `testCustomLabelAttributeWithValue`: source `## Setup { data-toc-label='Custom' }`. Expected `<h2 id="setup">Setup</h2>` in the HTML, and a `toc_tokens` entry with `name` `'Custom'` and `data-toc-label` `'Custom'` (AC-FR-002-1 and AC-FR-002-2).

Both tests are new and cover the spec's ACs. No existing test expectations change. The existing tests use `'data-toc-label': ''` for headings without a label, and that value is preserved.

## Constraints respected
- **K1 (stage interfaces):** no change to any processor signature or return value.
- **K2 (registries and priorities):** no registration or priority changes. `toc` stays at 5, `attr_list` at 8.
- **K3 (attribute values are `str` or `None`):** this change is the K3 requirement applied in the reader. Code that reads attributes now handles `None`. The writer side is not changed.
- **K4 (stash / placeholders):** not affected. The label is still run through `run_postprocessors`, as before.
- **K5 (backward compatibility):** no public name, option or output changes for any input that worked before. The only changed behaviour is that a valueless attribute, which used to raise, now falls back. This is a bug fix and is recorded in the changelog.
- **Changelog rule:** `markdown/` is changed, so `docs/changelog.md` gets an `[Unreleased]` entry (Change 2).
- **Tests:** new syntax tests use `markdown.test_tools.TestCase` (Change 3). Run with `python -m unittest discover tests` or the single module `python -m unittest tests.test_syntax.extensions.test_toc`.
- **Style:** line length 119 for the code and tests. flake8 applies.

Documentation (`docs/extensions/toc.md`) is not changed. The spec does not ask for it, and the Custom Labels section stays accurate.

## ARCHITECTURE.md vs source

Claims verified by reading the source (I did not run code: the design role is read-only):

| Claim | Source | Result |
|---|---|---|
| `toc` tree processor registered at priority 5 | `markdown/extensions/toc.py:511` (`register(tocext, 'toc', 5)`) | matches |
| `attr_list` tree processor at priority 8 | `markdown/extensions/attr_list.py:239` | matches |
| `toc` reads and unescapes `data-toc-label` itself | `toc.py:407-408`, `toc.py:417` | matches |
| Valueless non-boolean attributes stored as `None` | `attr_list.py:201-212` (`elem.set(name, None)` at line 212) | matches |
| Serializer: `None` → bare attribute; other non-string → `TypeError` | `serializers.py:80-83`, `serializers.py:186-196` | matches |
| `[Unreleased]` section in changelog | `docs/changelog.md:15`, `### Fixed` at line 17 | matches |
| Documented custom-label behaviour; `data-toc-label` absent from header HTML; no rule for empty values | `docs/extensions/toc.md:101-130` | matches (spec EV-003/EV-004) |
| Existing test that derives the TOC name from the label | `tests/test_syntax/extensions/test_toc.py:182-202` | matches (the spec cites 185-198, which is the same test) |

Discrepancies:
- **Pinned commit.** `ARCHITECTURE.md` pins `3f2c5510…` (describe `3.11.2-10-g3f2c551`). The spec's `base_commit` and the repository HEAD are `3b69d28`. This is a document-metadata difference. I checked the line numbers above against the working tree, and they match. Nothing in the plan depends on the pinned commit.
- No code-versus-document discrepancies were found for the claims above.

## Risks
- **Not executed.** The design role has no execution rights. The root-cause analysis relies on reading `attr_list` and `toc`. The implementer should first reproduce the `TypeError` with the issue's snippet, to confirm the crash comes from `toc.py:408` and not from elsewhere.
- **Open question Q-001 / ASM-001.** An explicit empty value (`data-toc-label=''`) keeps its current behaviour, which gives an empty TOC name. If maintainers want `''` to fall back as well, the design needs an extra branch and an extra test. This is a P2 question and does not block the fix.
- **Inferred ACs.** AC-FR-001-3, AC-FR-001-4, AC-FR-002-1 and AC-FR-002-2 are Inferred. Their exact markup expectations (`<h2 id="setup">Setup</h2>`, `href="#setup"`) should be confirmed in review.
- **Other valueless attributes (Q-002).** The same `None` value can reach other code that reads attributes. This change fixes only `data-toc-label`, as the spec scopes it. Other readers of `None` are not audited here.
- **Changelog entry.** The bullet is worded without an issue number, so no upstream reference is implied.

## AutoSE stage check: names the files and functions to change

Result: **PASS**

- all checks passed
