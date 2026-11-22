---
artefact: design
files:
  - {path: markdown/extensions/toc.py, change: modify, symbols: [TocTreeprocessor.run], new_symbols: []}
  - {path: docs/changelog.md, change: modify, symbols: [], new_symbols: []}
  - {path: tests/test_syntax/extensions/test_toc.py, change: modify, symbols: [TestTOC], new_symbols: [test_ac_fr_001_1_valueless_id_no_error, test_ac_fr_001_2_valueless_id_generated, test_ac_fr_001_3_valueless_id_in_toc, test_ac_fr_002_1_explicit_id_preserved, test_ac_fr_003_1_empty_string_id_generated]}
tests: tests/test_syntax/extensions/test_toc.py
---

# Design for issue #3

## Plan

Change one spot in the `toc` tree processor. `TocTreeprocessor.run` (`markdown/extensions/toc.py:387-438`) currently tests presence, not value:

1. **Collecting used ids** (`toc.py:390-392`): replace `if "id" in el.attrib:` / `used_ids.add(el.attrib["id"])` with a read of the value and add it only when it is truthy. This keeps `None` (valueless) and `""` out of `used_ids`.
2. **Generating ids** (`toc.py:403-404`): replace `if "id" not in el.attrib:` with `if not el.get("id"):`. This assigns the generated id when the attribute is missing, valueless (`None`), or empty (`""`). Existing non-empty ids are left as they are ("Do not override pre-existing ids").
3. No other change is needed. After step 2 every heading that reaches `unescape(el.attrib["id"])` (`toc.py:417`), `add_anchor` (`toc.py:424`) or `add_permalink` (`toc.py:426`) has a string id. Explicit non-empty ids follow the same path as before, so FR-002 holds by construction.

Changelog: add a `### Fixed` bullet under `## [Unreleased]` in `docs/changelog.md` (EV-001), with `toc`, `id` and the attribute syntax in backticks.

Tests: add the five test methods listed in the front matter to `TestTOC` in `tests/test_syntax/extensions/test_toc.py`, one per AC. Each has the AC ID in its docstring. They use `assertMarkdownRenders` with `extensions=['toc', 'attr_list']` (for the `toc` output, use `expected_attrs` as in `test_escaped_char_in_attr_list`, `test_escaped_char_in_id`). Expected strings for AC-FR-001-2/3, AC-FR-002-1 and AC-FR-003-1 are the spec's oracle strings.

Behaviour change (intended, covered by ASM-001): an explicit `{: id="" }` now receives the generated id instead of `id=""`. The reproducer `{: id }` (value `None`) is the case the issue reports.

## Constraints respected

- **K1 / K2 (stage interfaces, priorities):** no processor is added, removed or re-prioritised. `toc` stays at priority 5 (`toc.py:511`).
- **K3 (attribute values are `str` or `None`):** the fix reads `None` safely and writes only `str` values. The serializer receives a `str` for every generated id.
- **K4 (placeholders):** no inline or placeholder text is touched.
- **K5 (public surface):** no name, option or signature changes.
- **Changelog convention (EV-001):** entry under `[Unreleased]`.
- **Test convention:** `unittest` with `markdown.test_tools.TestCase`; no pytest.
- **Style:** flake8, line length 119.

## ARCHITECTURE.md vs source

Each claim the plan relies on was checked against the source at `ca2d6d3`:

| Claim (ARCHITECTURE.md) | Source check | Result |
|---|---|---|
| `toc` registers at priority 5 (`extensions/toc.py:511`) | `toc.py:511` is outside the file's read range in this run; the grep of the file shows `attrib["id"]` reads only at 392, 404, 417, 424, 426 | Not contradicted; the priority is not changed by this plan |
| `attr_list` stores valueless attributes as `None` (K3, `extensions/attr_list.py:59-63`) | `attr_list.py:58-63` reads "A word without a value is a valueless attribute ... represented internally with a value of `None`" | Confirmed (EV-003) |
| `toc` unescapes attribute values itself (`extensions/toc.py:408`, `:417`) | `toc.py:417` `'id': unescape(el.attrib["id"])` | Confirmed; line numbers match the issue's traceback |

The architecture document's pinned commit (`3f2c551`) differs from the base commit of this run (`ca2d6d3`). The claims above were checked against the base commit, which is the source of truth.

## Risks

- **R1 — `id=""` behaviour change.** Explicit `id=""` output changes from `<h1 id="">` to a generated id. Mitigation: ASM-001 / Q-001; the change is one line and reversible in review.
- **R2 — duplicate-id handling.** Generated ids for valueless headings must not collide with explicit ids. `unique()` checks `used_ids` (`toc.py:57-81`); the used-ids set is built from all explicit non-empty ids, so this holds.
- **R3 — `used_ids` built without `""`.** Only truthy ids are added. `unique()` already treats an empty base as needing a suffix (`toc.py:65`), so an empty id never reaches the output.
- **R4 — other extensions reading `None` ids.** Out of scope. The issue is limited to `toc`. No other extension is changed.
