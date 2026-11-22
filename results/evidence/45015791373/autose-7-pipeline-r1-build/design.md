---
artefact: design
issue: 7
files:
  - path: markdown/treeprocessors.py
    change: modify
    symbols: [InlineProcessor.run, InlineProcessor.__applyPattern]
    new_symbols: []
  - path: markdown/inlinepatterns.py
    change: modify
    symbols: [ReferenceInlineProcessor.handleMatch, ImageReferenceInlineProcessor]
    new_symbols: [ReferenceInlineProcessor.resolveLabel]
  - path: docs/changelog.md
    change: modify
    symbols: []
    new_symbols: []
  - path: tests/test_syntax/inline/test_links.py
    change: modify
    symbols: []
    new_symbols: []
tests: tests/test_syntax/inline/test_links.py
---

## Plan

### Root cause (verified by reading the source; not executed, because the design role has no run permission)

The inline pipeline runs one pattern at a time over the whole line, and each match is replaced by a placeholder before the next pattern runs (`markdown/treeprocessors.py:253-336`, `__applyPattern`). The order is:

1. `backtick` (190) runs first and replaces `` `foo` `` with a placeholder `STX klzzwxh:NNNN ETX` (`markdown/inlinepatterns.py:74`, `:407-477`; placeholder format `markdown/util.py:71-75`).
2. `reference` (170) and `short_reference` (130) then see the label as `[<placeholder>]`, not as `[`foo`]`.
3. `ReferenceInlineProcessor.handleMatch` takes the label text (shortcut form, `evalId` = `text.lower()`, `inlinepatterns.py:1223-1256`) or the id (full form, `RE_LINK` at `:1199`, `:1229-1237`) and looks it up in `md.references` (`inlinepatterns.py:1216`).
4. The definition `` [`foo`]: https://example.com `` was stored by `ReferenceProcessor.run` under the key `` "`foo`" `` (`markdown/blockprocessors.py:587-594`, which uses `.strip().lower()`). The key never contains a placeholder, so the lookup misses. The processor returns `(None, m.start(0), end)` ("ignore undefined refs", `inlinepatterns.py:1216-1217`), and the brackets stay as literal text around the `<code>` element.

Inline links work because `link` (160) does not look up a key. It only builds an `a` element whose text is the placeholder, and the placeholder is later expanded (`treeprocessors.py:145-250`).

### Chosen fix

Before the reference lookup, expand any inline placeholders in the label back to the source text they replaced. The source is recorded when the placeholder is created. Only the lookup key is expanded. The link text keeps its placeholders, so the rendered output is still `<code>foo</code>` as for inline links.

1. `markdown/treeprocessors.py`
   - `InlineProcessor.run` (`:348-366`): next to `self.stashed_nodes = {}` (`:366`), also reset `self.stashed_source: dict[str, str] = {}`.
   - `InlineProcessor.__applyPattern` (`:253-336`): in the new-style branch (`:325-330`), before building the placeholder, record `data[start:end]` (the source text that the match replaces) under the id of the new placeholder. The id is `"%04d" % len(self.stashed_nodes)` after `__stashNode`, so record it right after `placeholder = self.__stashNode(...)` by extracting the id from the placeholder, or change `__stashNode` to return `(placeholder, id)`. Only `start`/`end` from the match are used; `data` is not changed. The old-style branch (`:331-336`) is `pragma: no cover` and does not need it, but it must not break.
   - No change to `__makePlaceholder`, `__processPlaceholders`, or the placeholder text (K4).

2. `markdown/inlinepatterns.py`
   - New `ReferenceInlineProcessor.resolveLabel(self, label: str) -> str`: while `util.INLINE_PLACEHOLDER_RE` matches `label`, replace each placeholder by `source = stashed_source.get(id)` taken from `self.md.treeprocessors['inline']` (via `getattr(..., 'stashed_source', {})`, so a replaced `inline` processor without the attribute leaves the label unchanged). Return the expanded string. Recursion is bounded because a source string is always shorter than the text it replaced and contains no placeholder of its own in the current patterns. A guard (stop when no placeholder is found, or after a fixed number of rounds) is cheap.
   - `ReferenceInlineProcessor.handleMatch` (`:1201-1221`): after `evalId` and before the `NEWLINE_CLEANUP_RE` step, set `id = self.resolveLabel(id).lower()`. The existing `.lower()` in `evalId` is unchanged, so this only adds a second lower-casing after expansion (placeholders are already lower-case, so this is safe). `makeTag(href, title, text)` still receives the original `text` with placeholders.
   - `ImageReferenceInlineProcessor` (`:1259-1268`): override `resolveLabel` to return `label` unchanged. Image references inherit `handleMatch` from `ReferenceInlineProcessor`, and without this override `![`foo`]` would start matching and put raw placeholder control characters into the `alt` attribute. Keeping image behaviour unchanged is intentional (out of scope, see Risks).

3. `docs/changelog.md`: add a `### Fixed` entry under `## [Unreleased]` (line 15) for reference-style links whose label contains a code span (issue #7).

### Acceptance criteria covered

- AC-FR-001-3 (shortcut `` [`foo`] `` + `` [`foo`]: https://example.com ``): `short_reference` looks up `resolveLabel("<placeholder>")` = `` "`foo`" `` → key found → `<a href="https://example.com"><code>foo</code></a>`.
- AC-FR-001-4 (`` [text][`foo`] ``): `reference` evaluates the id from `RE_LINK`, expands it to `` "`foo`" `` → found → `<a href="https://example.com">text</a>`.
- AC-FR-001-2, AC-FR-001-5 (no placeholder in the label): `resolveLabel` is the identity → unchanged.
- AC-FR-002-1 (`` [`foo`](https://example.com) ``): inline link path (`LinkInlineProcessor`, `:1009-1172`) is not modified → unchanged.

Tests: add syntax tests to `tests/test_syntax/inline/test_links.py` using `self.assertMarkdownRenders(source, expected_html)` (no extensions), one per AC above, plus one for the image form `![`foo`]` with the definition, asserting the output contains no STX/ETX characters and no `<img` (current behaviour), so the image decision is pinned by a test. Optionally a test for `[`foo`][]` (empty id, `evalId` uses `text.lower()`), which must also match.

## Constraints respected

- **K1 (stage interfaces):** no signature changes to `run`, `handleMatch`, `getText`, `evalId`, `makeTag`. The new method `resolveLabel` is additive; `ImageReferenceInlineProcessor` overrides it, and no third-party caller is affected.
- **K2 (registries and priorities):** no priority or name changed (`backtick` 190, `reference` 170, `short_reference` 130, `link` 160 stay). The fix is local to the reference patterns, so no new ordering assumption is introduced.
- **K3 (attribute values):** nothing new is written to attributes. `href` is still the definition's string and `alt` is unchanged for images.
- **K4 (placeholders):** placeholder text is never altered; it is only read when building the lookup key. Output still contains the placeholders, so `__processPlaceholders` substitutes them as today.
- **K5 (backward compatibility):** no public name or signature changes. The only behavioural change is that `[`code`]`-style reference labels now match, which is the requested fix. Existing lookups without placeholders are unchanged (identity).
- **Changelog rule:** `docs/changelog.md` `[Unreleased]` entry included.
- **Tests:** syntax tests under `tests/test_syntax/inline/`, run with `python -m unittest discover tests`.

## ARCHITECTURE.md vs source

Claims checked against the source read in this run (line numbers are from the checked-out working tree):

- Pipeline stage split and `Treeprocessor.run(root) -> Element | None`: `markdown/treeprocessors.py:65` (verified).
- Inline registrations `backtick` 190, `escape` 180, `reference` 170, `link` 160, `short_reference` 130, `em_strong` 60: `markdown/inlinepatterns.py:74-93` (verified).
- Built-in tree processors `inline` 20, `prettify` 10, `unescape` 0: `markdown/treeprocessors.py:42-44` (verified; `Registry.__getitem__` accepts names, `markdown/util.py:334-343`).
- Placeholder mechanism for inline processing (`InlineProcessor` placeholders and `stashed_nodes`): `markdown/treeprocessors.py:80-93`, `:114-118`, `:366` (verified). Placeholder constants `markdown/util.py:71-75` (verified). `AtomicString` `markdown/util.py:186-188` (verified).
- The `inline` tree processor is an `InlineProcessor` instance under the name `inline`: `markdown/treeprocessors.py:42` (verified).
- `ReferenceProcessor` stores `id = label.strip().lower()`: `markdown/blockprocessors.py:587-594` (verified, not in ARCHITECTURE.md).
- The spec's EV-001 and EV-006 line references (`inlinepatterns.py:74-77`, `:1195-1221`, `:1251-1256`): verified.

Discrepancies:

- **Commit identity.** `ARCHITECTURE.md` pins commit `3f2c5510` (`3.11.2-10-g3f2c551`). `spec.md` has `base_commit: 3b69d28`, which is the checked-out HEAD. I did not confirm which commit the line numbers above refer to. The line numbers I read match the spec's EV references, so the working tree matches the spec. The pinned commit should be checked by the implementer before any line-number-based edit.
- No other discrepancies found for the claims above. `ARCHITECTURE.md` describes the registries, priorities and stash correctly for the parts checked. Not checked: the block-processor priority table (`blockprocessors.py:45-55`), `serializers.py:80-83,186-196`, and `util.py:67-81` in full. None of these are relied on by this plan except that attribute values stay strings (see Risks).

## Risks

1. **Source capture in `__applyPattern`.** `data[start:end]` is the text the match replaces. For code spans, that is the raw backtick string, which is exactly the definition key form (for a single-backtick span). For multi-backtick or whitespace-padded spans (e.g. ``` `` foo `` ```), the raw source differs from the stripped content, so the key will be the raw span. That is the correct behaviour for a matching definition written the same way, but a definition written as `` `foo` `` for a `` `` foo `` `` label will not match. This matches how Markdown source is compared elsewhere; it is an edge case, not in the spec.
2. **Cross-object access.** The reference pattern reads `self.md.treeprocessors['inline'].stashed_source`. This couples the pattern to the inline tree processor. The `getattr` default keeps it safe when `inline` is replaced. An alternative is to expose the map on `md`; it was rejected as a larger change to the core object.
3. **Re-entrant `run`.** `InlineProcessor.run` resets the stash on every call (`:366`). The new map is reset in the same place, so it stays in step with `stashed_nodes`. If a nested run ever happened during the same placeholder lifetime, both would be reset together, as they are today.
4. **Images (out of scope).** `![`foo`]` remains unchanged because of the `ImageReferenceInlineProcessor.resolveLabel` override. Fixing image references with code labels would need an `alt` text that strips placeholders to their rendered text; I recommend a follow-up issue, not this change.
5. **Expansion of placeholders from `escape` (180).** A label such as `[foo\*]` now expands its escape placeholder to `\*` before lookup. Before this change such labels never matched (a placeholder cannot be in a definition key), so no currently-working input changes. The output text is unaffected.
6. **Not executed.** The root cause and the expected outputs were established by reading the code. The implementer must run the new tests and the full suite (`python -m unittest discover tests`) and flake8 (`max-line-length = 119`), and must confirm that the shortcut and full forms produce the outputs in the ACs.

## AutoSE stage check: names the files and functions to change

Result: **PASS**

- all checks passed
