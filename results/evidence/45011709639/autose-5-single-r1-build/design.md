---
artefact: design
files:
  - {path: markdown/extensions/toc.py, change: modify, symbols: [TocTreeprocessor, TocTreeprocessor.run], new_symbols: []}
  - {path: tests/test_syntax/extensions/test_toc.py, change: modify, symbols: [], new_symbols: [TestTocNotoc, test_ac_fr_001_1_notoc_heading_omitted_from_toc, test_ac_fr_001_2_notoc_heading_absent_from_toc_links, test_ac_fr_001_3_notoc_token_in_multiple_classes, test_ac_fr_001_4_child_of_notoc_heading_kept, test_ac_fr_002_1_notoc_heading_absent_from_toc_tokens, test_ac_fr_003_1_notoc_heading_keeps_id, test_ac_fr_003_2_notoc_heading_rendered, test_ac_fr_004_1_other_class_heading_kept_in_toc_tokens, test_ac_fr_004_2_other_class_heading_kept_in_toc]}
  - {path: docs/extensions/toc.md, change: modify, symbols: [], new_symbols: []}
  - {path: docs/changelog.md, change: modify, symbols: [], new_symbols: []}
tests: tests/test_syntax/extensions/test_toc.py
---

# Design for issue #5: exclude headings with class `notoc` from the TOC

## Plan

1. **`markdown/extensions/toc.py`, `TocTreeprocessor.run`.** In the heading loop, after the id, `data-toc-label` and level-range checks, decide whether the heading is excluded:
   - `classes = (el.get('class') or '').split()` (the `or ''` handles a valueless `class` stored as `None`, see K3).
   - `excluded = 'notoc' in classes`.
   - Only the `toc_tokens.append({...})` call is guarded by `and not excluded`.
   - Everything else is unchanged: `set_level`, the id generation (`used_ids` and `id_counters` stay identical, so other ids do not move), `data-toc-label` handling, `add_anchor`, `add_permalink`. The heading therefore still renders with its id (FR-003), and `md.toc_tokens` and the TOC div are built from the remaining entries.
   - Nesting: `nest_toc_tokens` is unchanged. Children of an excluded heading are still appended to `toc_tokens` and nest under the nearest included ancestor (ASM-002).
   - Headings without `notoc` take the same code path as before, so their output is unchanged (FR-004).
2. **Tests** in `tests/test_syntax/extensions/test_toc.py`: one `test_ac_fr_*` method per AC (9 methods, listed in `new_symbols`). Syntax tests use `assertMarkdownRenders` where the expected output is exact; the contains/not-contains and property oracles use `markdown.markdown` and `markdown.Markdown` directly, as the spec allows.
3. **Docs.** `docs/extensions/toc.md`: a short paragraph describing the `notoc` class, with `attr_list`.
4. **Changelog.** `docs/changelog.md`, under `## [Unreleased]`, add an `### Added` subsection (before `### Fixed`) with one entry that names `notoc`, `attr_list`, `toc` and `toc_tokens` in backticks.

## Constraints respected

- **K2, registry priority.** No registration changes. `toc` stays at priority 5 and `attr_list` at 8 (EV from `markdown/extensions/toc.py:511` and `markdown/extensions/attr_list.py:239`). The class is set by `attr_list` before the `toc` tree processor runs, so no ordering change is needed.
- **K3, attribute values.** The code reads `class`, which may be `None`. Handled by `or ''`. Nothing is written to the tree.
- **K4, placeholders.** Not touched.
- **K5, backward compatibility.** No public name, option or dependency is added (ASM-004). Output for headings without `notoc` is unchanged.
- **Scope, R7.** Only the processor's loop changes. No new configuration option.
- **Style.** flake8, line length 119. Changelog entry required (`docs/changelog.md`).

## ARCHITECTURE.md vs source

| Claim relied on | Verified in source | Result |
|---|---|---|
| `toc` tree processor registered at priority 5 (`extensions/toc.py:511`) | `markdown/extensions/toc.py:511`: `md.treeprocessors.register(tocext, 'toc', 5)` | Matches |
| `attr_list` at priority 8 (`extensions/attr_list.py:239`) | `markdown/extensions/attr_list.py:239`: `md.treeprocessors.register(AttrListTreeprocessor(md), 'attr_list', 8)` | Matches |
| `.name` in an attribute list becomes a class token | `markdown/extensions/attr_list.py:53-56`: `if t.startswith('.'): return '.', t[1:]` | Matches (the `.` key is later assigned as `class`; the assignment code was not read in this run) |
| Valueless attributes are `None` (K3) | `markdown/extensions/attr_list.py:58-63` | Matches, so `class` can be `None` |
| `toc` writes `toc_tokens` at `toc.py:437` | `markdown/extensions/toc.py:437`: `self.md.toc_tokens = toc_tokens` | Matches |

No discrepancy between the architecture document and the source for the claims used here.

## Risks

- **R1 Nesting surprise.** Children of an excluded heading stay in the TOC (ASM-002, Q-002). If maintainers want them removed too, the change is a different one. Covered by AC-FR-001-4 so the behaviour is explicit.
- **R2 Class string format.** The `class` attribute could hold a value with extra whitespace; `split()` handles that.
- **R3 Existing tests.** The change adds one condition, so only the new tests should change. The full suite is run after the change.
- **R4 Spell check.** Docstrings and docs are spell-checked by CI. Identifiers and option names go in backticks.

## Self-critique

- Every AC (FR-001-1…4, FR-002-1, FR-003-1…2, FR-004-1…2) maps to a test method in `new_symbols`: yes.
- Constraints K2, K3, K5 respected: yes.
- The plan does not change ids or priorities, so existing links keep working: yes.
