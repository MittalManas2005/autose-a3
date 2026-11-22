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
    symbols: []
    new_symbols: [TestTOC.test_valueless_id_gets_generated_id, TestTOC.test_valueless_id_in_toc_marker_links, TestTOC.test_valueless_id_unique_with_duplicate_heading, TestTOC.test_empty_id_no_error, TestTOC.test_explicit_id_kept_in_toc]
  - path: tests/test_syntax/extensions/test_attr_list.py
    change: modify
    symbols: []
    new_symbols: [TestAttrListValuelessAttributes.test_valueless_id_without_toc_unchanged]
tests: tests/test_syntax/extensions/test_toc.py
---

## Plan

**Root cause (verified).** `attr_list` stores a valueless attribute as `None` (`markdown/extensions/attr_list.py:201-212`, with the `None` design documented at `attr_list.py:58-63`). For `# Heading {: id }`, the heading therefore carries `id=None`. The `attr_list` tree processor runs at priority 8 (`attr_list.py:239`) and `toc` at priority 5 (`toc.py:511`), so `toc` sees `id=None`. `TocTreeprocessor.run` checks only key presence, `if "id" not in el.attrib:` (`toc.py:402-404`), so the generated slug is skipped. The `None` then reaches `unescape(el.attrib["id"])` at `toc.py:417`, which raises the reported `TypeError`. (The same `None` would also break `add_anchor` / `add_permalink` at `toc.py:424/426` when those options are enabled and the heading is within `toc_depth`.)

**Chosen fix: treat a `None` id as absent, inside `toc`.**

1. `markdown/extensions/toc.py`, `TocTreeprocessor.run`:
   - In the first pass (`toc.py:390-392`), add an id to `used_ids` only when its value is not `None`, so `None` never enters the uniqueness set.
   - At `toc.py:403`, change the check to treat a missing or `None` id as absent: `if el.attrib.get("id") is None:` then assign `el.attrib["id"] = unique(self.slugify(...), used_ids, id_counters)` as today. An explicit string id, including `""`, is still "present" and is not regenerated, so `id="intro"` and `id=""` keep today's behaviour.
   - No other lines change. After this point `el.attrib["id"]` is always a `str`, so `unescape` (`toc.py:417`), `add_anchor` and `add_permalink` receive a string. This also satisfies K3 (readers must handle `None`).

   Satisfies: FR-001 / AC-FR-001-1 (no exception); FR-002 / AC-FR-002-1 (`id="heading"`, from the existing slugify rule); AC-FR-002-2 (no bare `id`); AC-FR-002-3 (`[TOC]` link `href="#heading"`, because the generated id is used by `build_toc_div`); AC-FR-002-4 (`unique()` adds the generated id to `used_ids`, so the second `# Heading` becomes `heading_1`); AC-FR-002-5 (`id=""` unchanged, no exception); FR-003 / AC-FR-003-1 and -2 (explicit ids are not touched).

2. `markdown/extensions/attr_list.py`: **no change.** Changing `attr_list` to write `""` for a valueless id would break AC-FR-004-1 and the #1501 behaviour recorded in `docs/changelog.md:38-41`. The `None` representation is the documented design, so the consumer has to handle it.

3. `docs/changelog.md`, under `## [Unreleased]` → `### Fixed` (currently lines 17-41): add a bullet, for example: "Fix a `TypeError` in the `toc` extension when a heading has an `id` attribute without a value (e.g. `# Heading {: id }`) with `attr_list`. Such a heading is now treated as having no id: it gets the auto-generated id and appears in the table of contents." Required because `markdown/` changes (`docs/contributing.md:535-547`).

4. Tests (acceptance criteria, using `self.assertMarkdownRenders`):
   - `tests/test_syntax/extensions/test_toc.py`, class `TestTOC`:
     - `test_valueless_id_gets_generated_id`: `# Heading {: id }`, extensions `['toc', 'attr_list']`, expect output containing `<h1 id="heading">Heading</h1>` (AC-FR-002-1, AC-FR-002-2 via the exact expected string; AC-FR-001-1 via the absence of an exception). Use `expected_attrs` only if it stays simple; otherwise assert the HTML and check the `toc_tokens` `id` value is `heading`.
     - `test_valueless_id_in_toc_marker_links`: `[TOC]\n\n# Heading {: id }` → output contains `href="#heading"` (AC-FR-002-3).
     - `test_valueless_id_unique_with_duplicate_heading`: `# Heading {: id }\n\n# Heading` → `id="heading"` and `id="heading_1"`; assert every `id` value is unique (AC-FR-002-4).
     - `test_empty_id_no_error`: `# Heading {: id="" }` → no exception; output `<h1 id="">Heading</h1>` (AC-FR-002-5, keeps today's output per ASM-001). Pinning the exact output is intentional, so that a future change to `id=""` is a visible decision.
     - `test_explicit_id_kept_in_toc`: `[TOC]\n\n# Heading {: id="intro" }` → `<h1 id="intro">` and `href="#intro"` (AC-FR-003-1, AC-FR-003-2).
   - `tests/test_syntax/extensions/test_attr_list.py`, class `TestAttrListValuelessAttributes`: `test_valueless_id_without_toc_unchanged`: `# Heading {: id }` with `['attr_list']` → `<h1 id>Heading</h1>` (AC-FR-004-1). This is a regression guard showing the fix stays in `toc`.

Test target: `python -m unittest tests.test_syntax.extensions.test_toc` and `tests.test_syntax.extensions.test_attr_list`, then the full `python -m unittest discover tests`, then `python -m flake8` (max line 119).

## Constraints respected

- **K1 (stage interfaces):** `TocTreeprocessor.run(doc) -> None` is unchanged; no signature changes.
- **K2 (registries and priorities):** no priority or name changes. `toc` stays at 5 and `attr_list` at 8, and no new processor is registered.
- **K3 (attribute values `str` or `None`):** the fix makes the reader handle `None` (the consumer side that K3 requires). The writer side is unchanged, and `attr_list` keeps storing `None`.
- **K4 (placeholders):** not touched.
- **K5 (backward compatibility):** the public API is unchanged. Only the output for a valueless heading id changes, from a crash to a generated id. The explicit-id and `id=""` outputs are unchanged. The change adds a line to the changelog.
- **Tests and changelog conventions (`docs/contributing.md:93-96`, `:535-547`):** tests and a changelog entry are included. Tests use `unittest` with `assertMarkdownRenders`, not pytest.
- **Style:** flake8, line length 119.

Scope: Q-002 / ASM-002. Only `id` is handled. `data-toc-label` is not changed (see Risks).

## ARCHITECTURE.md vs source

Verified against the source (checked by reading each cited line):

| Claim | Source | Result |
|---|---|---|
| `toc` tree processor at priority 5 | `markdown/extensions/toc.py:511` | Matches |
| `attr_list` tree processor at priority 8 | `markdown/extensions/attr_list.py:239` | Matches |
| `attr_list` stores valueless attributes as `None` (K3) | `attr_list.py:201-212`, comment at `:58-63` | Matches |
| serializer writes `None` as a bare name | `markdown/serializers.py:186-190` | Matches (ARCHITECTURE cites 186-196, which covers the whole block) |
| serializer raises `TypeError` for other non-strings | `serializers.py:80-83`, `:119-120` | Matches |
| `toc` unescapes the attribute values it reads (`toc.py:408`, `:417`) | `toc.py:408`, `:417` | Matches |
| Only `id` is affected; `data-toc-label` read at `toc.py:407-408` | `toc.py:407-408` | Matches, same unguarded pattern |

Discrepancies: none found in the claims this plan relies on.

Points about the spec (`.autose_out/spec.md`) that I verified:
- EV-001 and EV-003 quotes match `toc.py:403-408` and `toc.py:417`.
- EV-008 (`docs/extensions/toc.md`: manual ids are kept, other ids are derived from the heading text) is consistent with the plan.
- The `unique()` helper (`toc.py:57-87`) adds the id it returns to `ids` (`toc.py:86`), so the duplicate-heading case in AC-FR-002-4 works with the plan's `used_ids` handling.
- The crash point depends on configuration. With the default `toc_depth` the crash is at `toc.py:417`. With `toc_depth` excluding that heading level it would not reach `:417`, but with `anchorlink` or `permalink` enabled it would fail at `toc.py:424` or `:426`. Generating the id before any use covers all of these paths.

## Risks

1. **Empty heading text** (`# {: id }`): the generated slug is `""`, and `unique("")` gives `_1` (`toc.py:65`). This is the same result a text-less heading gets today, so it is not a regression, but no test covers it. Not in the ACs.
2. **`data-toc-label` without a value** (RSK-001 / Q-002): `toc.py:407-408` has the same unguarded pattern (`unescape(None)`). It is out of scope per ASM-002. If the maintainers want it, it needs a new FR and ACs. It is a separate, one-line-class fix and can follow.
3. **`id=""` behaviour (Q-001 / ASM-001):** the plan keeps today's output (`id=""`, `href="#"`). If maintainers decide an empty id should also be generated, the check at `toc.py:403` changes to `if not el.attrib.get("id"):`, AC-FR-002-5 changes, and the `id=""` test is updated. This is a one-line change and does not affect the rest of the design.
4. **Test runtime and placement:** tests are in `test_toc.py`, which is large. Adding methods to `TestTOC` is consistent with the existing `test_escaped_char_in_id` pattern (`test_toc.py:1036`).
5. **Unverified in this stage:** the spec's assumption that the slug for "Heading" is `heading` (default `slugify`) and that `[TOC]` is the default marker. The design relies on both. The tests will confirm them. I did not run the code (the design role has no Bash).

## AutoSE stage check: names the files and functions to change

Result: **PASS**

- all checks passed
