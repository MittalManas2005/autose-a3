---
artefact: design
files:
  - path: markdown/inlinepatterns.py
    change: modify
    symbols: [ReferenceInlineProcessor, ReferenceInlineProcessor.handleMatch, ReferenceInlineProcessor.evalId]
    new_symbols: [ReferenceInlineProcessor.code_span_source]
  - path: tests/test_syntax/inline/test_links.py
    change: modify
    symbols: [TestReferenceLinks]
    new_symbols: [test_ac_fr_001_1_short_reference_code_label, test_ac_fr_001_2_implicit_reference_code_label, test_ac_fr_001_3_inline_link_code_text, test_ac_fr_001_4_undefined_reference_code_label]
  - path: docs/changelog.md
    change: modify
    symbols: []
    new_symbols: []
tests: tests/test_syntax/inline/test_links.py
---

## Plan

Root cause (spec EV-001, EV-002, EV-007): the backtick pass (priority 190) runs before the reference pass (170). By the time `ReferenceInlineProcessor.handleMatch` runs, a code span in link text is the placeholder `\x02klzzwxh:NNNN\x03`. `handleMatch` passes that placeholder text to `evalId`, so the reference label becomes the placeholder and never matches a definition such as `[`code`]: http://example.com`. Explicit `[`code`][1]` works because its label is `1`. Inline links work because they never look up a label.

Change:
1. Add `ReferenceInlineProcessor.code_span_source(text)`. It returns `text` with every inline placeholder whose stashed node is a `code` element replaced by that code span's Markdown source (backtick fence plus the unescaped code text). Other placeholders are returned unchanged. It reads the stash only and never alters `data`.
2. In `ReferenceInlineProcessor.handleMatch`, pass `self.code_span_source(text)` to `evalId` instead of `text`. `evalId` uses that argument for both the implicit id (`text.lower()`) and the short form (`ShortReferenceInlineProcessor.evalId`, `ShortImageReferenceInlineProcessor.evalId`). `makeTag` still receives the original placeholder `text`, so rendered output is unchanged.
3. Add the tests (one per AC) to `TestReferenceLinks` in `tests/test_syntax/inline/test_links.py`.
4. Add a `### Fixed` entry under `[Unreleased]` in `docs/changelog.md`.

No signature changes, no new processor, no priority changes.

## Constraints respected
- K1 (stage interfaces): `handleMatch`, `evalId` and `makeTag` keep their signatures; `evalId` still receives a string.
- K2 (registries and priorities): nothing registered or re-prioritised.
- K3 (attribute values): unchanged; `href` and `title` are unaffected.
- K4 (placeholders never altered): `data` and `text` are not modified. The placeholder is only read to find its stashed node, and only the lookup key is rewritten.
- K5 (public surface): `markdown.markdown`, `Markdown`, configuration unchanged; no new mandatory dependency; Python 3.11+ syntax only.
- Repository rule (contributing guide): changelog entry under `[Unreleased]`; tests for every changed feature; flake8 max 119.

## ARCHITECTURE.md vs source
- `inlinepatterns.py:74-77` registration and priorities (backtick 190, escape 180, reference 170, link 160): confirmed in source (spec EV-001). ARCHITECTURE.md agrees.
- `inlinepatterns.py:104-122` regex definitions (`BACKTICK_RE`, `LINK_RE`, `REFERENCE_RE`): confirmed (spec EV-004).
- `inlinepatterns.py:1195-1237` reference lookup (`text` used for `evalId`): confirmed (spec EV-002, EV-003). ARCHITECTURE.md does not describe this detail; it is the root cause here.
- `util.py:71-75` placeholder format (STX/ETX, `klzzwxh:` prefix for inline placeholders): read in this session; `util.INLINE_PLACEHOLDER_RE` is used by `Pattern.unescape`, so reusing it is consistent with existing code.
- The reconstructed code-span source uses `util.code_escape` in reverse. ARCHITECTURE.md does not cover this helper; the source (`util.py:155-163`) is authoritative and was read.
- No discrepancy found between ARCHITECTURE.md and the source for the claims relied on.

## Risks
- Reconstructed source is canonical, not byte-exact. Two raw forms can differ: padded spans (`` ` a ` `` has source label "` a `" but the code text is stripped to "a") and unusual backtick counts. For these, the label lookup can still miss, exactly as before. Behaviour is no worse than today, and the common forms the issue describes are fixed. Acceptable; documented here.
- Image references (`![`code`][]`) inherit `handleMatch`, so they also get the fix. This is intended and consistent, but no AC covers it; flagged, not tested.
- Output for undefined references is unchanged (AC-FR-001-4), and inline links are unchanged (AC-FR-001-3).
- Housekeeping: a temporary probe file `tests/scratch_probe_issue7.py` (created for reproduction) could not be removed because the delete command was denied. It does not match the discovery pattern `test*.py`, so `python -m unittest discover tests` does not run it. It must be deleted manually.
- The `ASM-001` default (reference-style links are the failing form) is inferred; if the maintainer reports another failing form, FR-001 gains ACs.

## Self-critique
- Does the plan cover every criterion? AC-FR-001-1 and -2 are covered by the lookup fix; -3 and -4 are preservation checks that the fix does not change inline links or undefined references.
- Does it respect the constraints? Yes (see above).
