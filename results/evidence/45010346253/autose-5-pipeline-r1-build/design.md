---
artefact: design
issue: 5
files:
  - path: markdown/extensions/toc.py
    change: modify
    symbols: [TocTreeprocessor.run]
    new_symbols: []
  - path: tests/test_syntax/extensions/test_toc.py
    change: modify
    symbols: []
    new_symbols: [TestTOC.test_notoc_heading_excluded_from_toc, TestTOC.test_notoc_heading_keeps_id_and_markup, TestTOC.test_notoc_heading_excluded_from_toc_tokens, TestTOC.test_notoc_with_other_classes, TestTOC.test_other_class_unchanged, TestTOC.test_notoc_children_nested_under_included_ancestor, TestTOC.test_notoc_permalink]
  - path: docs/extensions/toc.md
    change: modify
    symbols: []
    new_symbols: []
  - path: docs/changelog.md
    change: modify
    symbols: []
    new_symbols: []
tests: tests/test_syntax/extensions/test_toc.py
---

## Plan

Single behavioural change in the `toc` tree processor. No new option, no new
registry entry, no new public name.

1. **`markdown/extensions/toc.py`, `TocTreeprocessor.run`** (loop at lines 396-421).
   - Compute, for each matched header `el`, whether it is excluded:
     `excluded = "notoc" in (el.attrib.get("class") or "").split()`.
     The `or ""` guard is required: an attribute list such as `{: class }` stores
     `class` as `None` (see `attr_list.py:201-211`, K3), and `None.split()` would raise.
     Splitting on whitespace means `notoc` matches only as a whole class token
     (`notoc-x` does not match) and works among several classes (ASM-003, FR-005).
   - Change the append at lines 414-421 to run only when
     `toc_top <= level <= toc_bottom and not excluded`. This is the only place an
     entry enters `toc_tokens`, so it removes the heading from `md.toc_tokens`
     (FR-003) and therefore from the `[TOC]` div, which `build_toc_div` builds from
     the same nested list (FR-001).
   - Leave everything else untouched:
     - id assignment (lines 402-404) runs before the filter, so the excluded heading
       keeps its id and existing links still work (FR-002, AC-FR-002-1);
     - the `data-toc-label` handling (lines 406-412) is unchanged;
     - anchorlink and permalink (lines 423-426) still run for the excluded heading
       (FR-002, AC-FR-002-3, ASM-001);
     - the rendered heading markup is not modified, so headings with other classes
       are byte-identical to today (FR-004).
   - Child headings are not filtered. They stay in the flat `toc_tokens` list, and
     `nest_toc_tokens` (line 428) nests them under the nearest included ancestor,
     because nesting is computed from levels alone (ASM-002, Q-001, AC-FR-001-4).
     Example: `# One` / `## Two {: .notoc }` / `### Sub` gives `Sub` as a child of `One`.

   Coverage of acceptance criteria:
   - AC-FR-001-1, -2, -3, -4 (TOC membership), AC-FR-001-5 (preservation): item 1 above.
   - AC-FR-002-1, -2 (id and rendered text): unchanged code path, asserted by tests.
   - AC-FR-002-3 (permalink): unchanged code path, asserted by test.
   - AC-FR-003-1 (`toc_tokens` at any depth): item 1 above.
   - AC-FR-004-1, -2 (other classes unchanged): the predicate is false, so no code path changes.
   - AC-FR-005-1 (`notoc` among several classes): the whitespace split.

2. **`tests/test_syntax/extensions/test_toc.py`**: add the new test methods to `TestTOC`
   (class at line 28). They use `self.assertMarkdownRenders` for HTML checks and
   `markdown.Markdown(extensions=["toc", "attr_list"])` with `md.toc` and `md.toc_tokens`
   for TOC and token checks. Each AC from the spec maps to one assertion, as listed in
   the test names above. Existing tests are not modified.

3. **`docs/changelog.md`**: add an entry under `## [Unreleased]` (line 15), in an
   `### Added` subsection (create it above `### Fixed` if absent). Required because
   `markdown/` changes (`docs/contributing.md:535-547`).

4. **`docs/extensions/toc.md`**: add a short paragraph in the `toc` documentation
   (near the `toc_depth` entry, line 225) that a heading with the class `notoc`,
   set with `attr_list`, is left out of the TOC and `md.toc_tokens` while its id
   and content are still rendered. This documents the user-visible behaviour.

No change to `markdown/extensions/attr_list.py`, the registries, or the priority
of `toc` (5).

## Constraints respected

- **K1 (stage interfaces):** `TocTreeprocessor.run(doc)` keeps its signature and
  return convention (returns `None`, as today).
- **K2 (registries and priorities):** no new processor and no priority change. The
  `toc` entry stays `md.treeprocessors.register(tocext, 'toc', 5)` (line 511).
  The change is inside the existing processor.
- **K3 (attribute values are `str` or `None`):** the code reads `class` and treats
  `None` as empty. It writes no attributes, so no new value types reach the serializer.
- **K4 (stash and placeholders):** not touched. The change does not alter any text
  that contains placeholders; `innerhtml` is still computed as before (line 399).
- **K5 (backward compatibility):** no public name, option or entry-point changes.
  The one visible change is intended: an existing heading with the class `notoc`
  leaves the TOC (Q-002, RSK-001). ASM-004 is the default that no option is added,
  as the spec proposes. The changelog entry records this.
- **Changelog rule:** `docs/changelog.md` gets an `[Unreleased]` entry.
- **Tests:** the suite is run with `python -m unittest discover tests`; tests are
  added as `unittest` methods in the existing class. Pytest is not used.
- **Style:** flake8 max line length 119.

## ARCHITECTURE.md vs source

Verified against the source in this checkout:

- `toc` registered at priority 5: `markdown/extensions/toc.py:511`. Matches ARCHITECTURE 2.3 and spec EV-004.
- `attr_list` registered at priority 8: `markdown/extensions/attr_list.py:239`. Matches ARCHITECTURE 2.3 and spec EV-005.
- Built-in tree processors `inline` 20, `prettify` 10, `unescape` 0: `markdown/treeprocessors.py:42-44`. Matches ARCHITECTURE 2.2 C4.
- Id assignment before the level filter: `toc.py:403-404` for the id, `toc.py:414-421` for the `toc_tokens` append, `toc.py:423-426` for anchor and permalink. Matches spec EV-003.
- `toc` reads `data-toc-label` and `id` with `unescape`: `toc.py:408` and `toc.py:417`. Matches ARCHITECTURE 2.3.
- `attr_list` valueless attributes stored as `None`, and `.class` joined into a space-separated string: `attr_list.py:194-211`. Matches K3. Relevant to the design: `class` can be `None` (`{: class }`), so the code must guard it.
- `nest_toc_tokens` builds nesting from the flat list (`toc.py:196-225`). This is what makes ASM-002 work without special handling.
- Attribute lookup and TOC marker replacement are both driven by `toc_tokens`/`build_toc_div`, so filtering the token list also removes the heading from the `[TOC]` output (`toc.py:380`, `toc.py:428-431`).

Discrepancies:
- **Commit reference.** ARCHITECTURE.md gives the pinned commit as `3f2c551`. The spec's `base_commit` is `ca2d6d3` and the git status shows `ca2d6d3` as HEAD. I did not run `git` (not in my allowed commands), so I cannot say whether these are the same tree. The line numbers cited above match the current checkout, so the design is based on the current checkout. The implementer should confirm the commit before editing.
- **Run order of `attr_list` and `toc`.** ARCHITECTURE 2.3 says `attr_list` runs before `toc`. This follows from the priorities (8 before 5, higher first, per ADR-T2). I did not re-read `util.py` to confirm the sort direction, so this is from the priority numbers, not from the registry code. The class is only needed to be present when `toc` runs, and this claim is consistent with the existing `toc` code reading attributes set by `attr_list`.
- **Spec vs source, valueless `class`.** The spec's assumption is that `class` is always a string when set. Source shows it can be `None` (`attr_list.py:201-211`). Not a discrepancy with ARCHITECTURE, but a gap in the spec. The design handles it.

No other discrepancies found.

## Risks

- **Behaviour change for existing users of `notoc` (RSK-001, Q-002).** Any document that already gives a heading the class `notoc` will lose it from the TOC. This is the intended feature, but it is a visible change without an opt-in. The spec proposes no option (ASM-004). If maintainers want an option, it would be an additional change and would not alter the design here.
- **Child headings (Q-001, ASM-002).** Children of an excluded heading are promoted under the nearest included ancestor. If maintainers want children removed too, the change would be a different predicate on the children, and the design would need revision. The current design follows the spec default.
- **Permalink on excluded heading (ASM-001).** The excluded heading still gets a permalink when permalinks are enabled. If maintainers expect none, `add_permalink` would need a guard. The default is to keep it, as for any heading.
- **Multiple classes (ASM-003).** `notoc` among other classes is excluded by the whitespace split. A reviewer might prefer exact single-class matching; the spec default is to match.
- **Unverified run order** of `attr_list` and `toc` (see above). If `toc` ran before `attr_list`, the class would not be visible and the feature would silently do nothing. The tests for the `attr_list` case will catch this at test time.
- **Changelog placement.** `[Unreleased]` currently starts with `### Fixed`. The implementer should check whether an `### Added` subsection exists before inserting, to keep the changelog structure consistent.

## AutoSE stage check: names the files and functions to change

Result: **PASS**

- all checks passed
