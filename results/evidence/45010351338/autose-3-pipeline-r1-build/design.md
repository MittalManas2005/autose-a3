---
artefact: design
issue: 3
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
    new_symbols: [TestTOC.test_valueless_id_heading, TestTOC.test_valueless_id_in_toc, TestTOC.test_explicit_id_in_toc, TestTOC.test_empty_id_heading, TestTOC.test_valueless_id_without_toc]
tests: tests/test_syntax/extensions/test_toc.py
---

# Design for issue #3: `toc` crashes with `TypeError` on a valueless `id`

## Plan

The crash is in `TocTreeprocessor.run` (`markdown/extensions/toc.py`). The fix is confined to that method. No new processor is added, and no priority or pipeline stage changes.

### 1. `markdown/extensions/toc.py`, `TocTreeprocessor.run` (satisfies FR-001, FR-002, FR-003)

Root cause, verified in source:
- `attr_list` stores a valueless attribute such as `{: id }` as `None` (`attr_list.py:201-212`, value set at `attr_list.py:212`).
- `toc` runs at priority 5 (`toc.py:511`), after `attr_list` at priority 8 (`attr_list.py:239`). So when `toc` runs, the heading's `id` attribute is already `None`.
- The current guard is `if "id" not in el.attrib:` (`toc.py:403`). It checks key presence, not value, so the `None` id is kept. The value then reaches `unescape(el.attrib["id"])` at `toc.py:417` and raises `TypeError`.

Changes:
- **Line 391-392 (pre-scan of used ids):** only add an id to `used_ids` when it has a non-empty value, so that `None` (and the empty string) never enter the set of strings. Code: `if el.attrib.get("id"): used_ids.add(el.attrib["id"])`. This does not change the output for headings with real ids. An empty id was already handled by `unique()`, which treats `not id` as taken (`toc.py:65`).
- **Line 402-404 (id assignment):** replace `if "id" not in el.attrib:` with `if not el.attrib.get("id"):`, and update the comment to say that a valueless (`None`) or empty id is treated as no id. The generated id then comes from the existing `unique(self.slugify(...), used_ids, id_counters)` call.

Effect on each criterion:
- AC-FR-001-1 and AC-FR-002-1: `# Heading {: id }` has value `None`, so the guard fires. The heading gets `id="heading"`, and `unescape` at line 417 receives a string. Output `<h1 id="heading">Heading</h1>`.
- AC-FR-002-2: with `[TOC]`, the heading now has `heading`, so the TOC link is `<a href="#heading">Heading</a>`. The `add_anchor` and `add_permalink` calls (lines 424, 426) also receive a string.
- AC-FR-002-3: the `toc_tokens` entry has `id` `heading` and `name` `Heading`. `nest_toc_tokens` gives one top-level token.
- AC-FR-002-4 (`{: id="" }`): the empty string is falsy, so the guard fires and the id is generated. This follows ASM-001 and depends on Q-001 (see Risks).
- AC-FR-003-1 and AC-FR-003-2: `id="intro"` is truthy, so the guard does not fire. The id is kept and used in the heading and TOC unchanged.
- FR-004 (AC-FR-004-1): no change. Without `toc`, `attr_list` output is untouched, so `<h1 id>Heading</h1>` remains.

The change is one code path inside one extension. `attr_list` keeps its `None` representation, as its output without `toc` depends on it.

### 2. `docs/changelog.md` (required by the changelog rule)

Add one bullet under `## [Unreleased]` → `### Fixed` (`docs/changelog.md:15-17`). Wording: fix the `toc` extension raising `TypeError` for a heading with a valueless `id` attribute (`{: id }`) when `attr_list` is enabled. Such headings, and headings with an empty `id`, now get the normal generated id and appear in the table of contents. No issue number is cited, because the number is not verified against the upstream tracker.

### 3. `tests/test_syntax/extensions/test_toc.py`, class `TestTOC` (`test_toc.py:28`) (tests for all ACs)

Add five test methods next to `test_escaped_char_in_attr_list` (`test_toc.py:1062`), in the `snake_case` style used by nearby tests:

- `test_valueless_id_heading`: `# Heading {: id }` with `['toc', 'attr_list']` → `<h1 id="heading">Heading</h1>` (AC-FR-001-1, AC-FR-002-1). Use `assertMarkdownRenders` with exact output. It also covers the no-error requirement.
- `test_valueless_id_in_toc`: `[TOC]`, blank line, `# Heading {: id }` with `['toc', 'attr_list']`. Check that the output contains `<a href="#heading">Heading</a>` (AC-FR-002-2). Use `markdown.markdown` and `assertIn`.
- `test_explicit_id_in_toc`: `# Heading {: id="intro" }`, checked for `<h1 id="intro">Heading</h1>` (AC-FR-003-1), and `[TOC]` with the same heading checked for `<a href="#intro">Heading</a>` (AC-FR-003-2).
- `test_empty_id_heading`: `# Heading {: id="" }` with `['toc', 'attr_list']` → `<h1 id="heading">Heading</h1>` (AC-FR-002-4).
- `test_valueless_id_without_toc`: `# Heading {: id }` with `['attr_list']` → `<h1 id>Heading</h1>` (AC-FR-004-1, preservation).

AC-FR-002-3 (`toc_tokens`) is tested by `expected_attrs`, using the same pattern as `test_escaped_char_in_attr_list` (`test_toc.py:1062-1086`), or by reading `md.toc_tokens` after converting with a `markdown.Markdown` instance that has `TocExtension()` and `attr_list`. The expected token is `{'level': 1, 'id': 'heading', 'name': 'Heading', ...}`. Only the top-level token list is checked.

No existing test changes. The `expected_attrs` toc strings in the existing tests are not affected.

## Constraints respected

- **K1 (stage interfaces):** no processor signature or return value changes. `TocTreeprocessor.run` still returns `None` and mutates the tree in place, as before.
- **K2 (registries and priorities):** no new processor is registered and no priority changes. `toc` stays at 5 (`toc.py:511`), and `attr_list` stays at 8 (`attr_list.py:239`). The fix relies on the existing order and does not alter it.
- **K3 (attribute values are `str` or `None`):** this is the constraint the bug breaks. `toc` now handles `None` as "no id", as K3 requires for any code that reads attributes. Its writes are unchanged: it writes only generated `str` ids.
- **K4 (placeholders):** not touched. The change does not read or write stash placeholders.
- **K5 (backward compatibility):** no public name, config option, or extension name changes. The only visible behaviour change is the fixed crash, plus the empty-id case in ASM-001, which was reported as a bug. The change is listed in the changelog.
- **Changelog rule:** `docs/changelog.md` gets an entry under `[Unreleased]` (see plan item 2).
- **Test rule:** every changed behaviour has a test (see plan item 3). Tests use `markdown.test_tools.TestCase` and `assertMarkdownRenders`, and run with `python -m unittest`.
- **Style:** flake8 with max line length 119. The new test lines use the existing `# noqa` pattern only where a multi-line expected string needs it.

## ARCHITECTURE.md vs source

Claims checked by reading the cited source:

| Claim (ARCHITECTURE.md) | Source | Result |
|---|---|---|
| `toc` registers a tree processor at priority 5 | `markdown/extensions/toc.py:511` | Confirmed |
| `toc` unescapes attribute values it reads (lines 408, 417) | `toc.py:408`, `toc.py:417` | Confirmed |
| `attr_list` priority 8 | `markdown/extensions/attr_list.py:239` | Confirmed (`register(..., 'attr_list', 8)`) |
| Valueless attributes are stored as `None` | `attr_list.py:58-63`, `attr_list.py:75-78`, `attr_list.py:201-212` | Confirmed |
| Serializer renders `None` as a bare attribute name (C5, K3) | `markdown/serializers.py:186-196` | Confirmed (lines 186-189 read: `None` → `write(f" {k}")`) |
| `toc` does not handle `None` ids (K3 gap, implied by the bug) | `toc.py:403`, `toc.py:417` | Confirmed: the guard checks key presence only |

Claims from the spec's evidence log (`spec.md` section 4.6) checked by reading:
- `toc.py:391` (`if "id" in el.attrib:`) and `toc.py:417` (`'id': unescape(el.attrib["id"]),`): confirmed.
- `attr_list.py:71` (`(r' ', None)`) and `attr_list.py:78` (docstring): confirmed.
- Existing `toc` tests use `'toc', 'attr_list'` together (`test_toc.py:202`, `:1085`, `:1406`): confirmed by grep. The class is `TestTOC` at `test_toc.py:28`.
- `[Unreleased]` section with `### Fixed` at `docs/changelog.md:15-17`: confirmed.

Discrepancies:
1. **Line reference in the spec (EV-002):** the spec cites `toc.py:385-434` for the `if "id" not in el.attrib:` guard. The guard is at `toc.py:403`, with its comment at `toc.py:402`. The range is correct but imprecise. The implementation targets line 403.
2. **Pinned commit:** ARCHITECTURE.md pins `3f2c551`, while `spec.md` front matter gives `base_commit: ca2d6d3…`. I did not run `git` to check which commit the checkout is at. The line references above were read from the working tree. The implementer should confirm the checkout matches before relying on line numbers.
3. **Spec's ASM-001 and EV-001 wording:** the spec says the current code "keeps any pre-existing `id` attribute, including an empty one (EV-001)". Confirmed at `toc.py:403` (`"id" not in el.attrib`, so an empty value is kept).

No other discrepancies found.

## Risks

- **Q-001 is open (P2).** If maintainers answer "no" (keep `{: id="" }` as an explicit empty id), change the guard in plan item 1 to `if el.attrib.get("id") is None:`, the used-ids guard to `is not None`, and drop AC-FR-002-4 and its test `test_empty_id_heading`. The rest of the design is unaffected. This is a one-line reversal.
- **Behaviour change for empty ids from other sources.** Any heading in the tree with `id=""`, not only one from `attr_list`, now gets a generated id when `toc` runs. In practice, `attr_list` is the only built-in source of such an attribute, so the impact is limited to the case the spec describes.
- **Generated-id collisions.** A `{: id }` heading is no longer in `used_ids` before the generated id is chosen. Because `None` is excluded from `used_ids`, a second heading that slugifies to the same text gets the normal `_1` suffix from `unique()`. This is the existing behaviour for headings without an id, and no test in the spec covers it. Adding one is optional, not required by the acceptance criteria.
- **Test strings.** The `[TOC]` expected output for AC-FR-002-2 and AC-FR-003-2 is checked with `assertIn` rather than exact equality, to match the spec's "contains" oracle and avoid depending on whitespace in the generated TOC div.
- **Runtime verification.** The design relies on reading the code; the implementer must run `python -m unittest tests.test_syntax.extensions.test_toc` and the full discover run to confirm the crash is gone and nothing else changed.

## AutoSE stage check: names the files and functions to change

Result: **PASS**

- all checks passed
