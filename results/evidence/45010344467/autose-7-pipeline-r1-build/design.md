---
artefact: design
issue: 7
files:
  - path: markdown/inlinepatterns.py
    change: modify
    symbols: [ReferenceInlineProcessor.handleMatch]
    new_symbols: [ReferenceInlineProcessor.raw_label]
  - path: markdown/treeprocessors.py
    change: modify
    symbols: [InlineProcessor.run, InlineProcessor.__applyPattern, InlineProcessor.__stashNode]
    new_symbols: []
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

### Root cause (from the source, not yet executed)

Inline patterns run in one loop over `data` (`treeprocessors.py:135-141`). Priorities: `backtick` 190 (`inlinepatterns.py:74`), `escape` 180, `reference` 170 (`:76`), `link` 160 (`:77`), `short_reference` 130 (`:83`). When `backtick` matches, `__applyPattern` replaces the code span in `data` with a placeholder (`treeprocessors.py:323-330`), so later patterns see `\x02klzzwxh:NNNN\x03`, not `` `code` ``.

- `ReferenceInlineProcessor.handleMatch` gets `text` from `getText`, i.e. the placeholder-laden label (`inlinepatterns.py:1206`).
- `[text][id]` looks up `id` taken from the second bracket (`evalId`, `:1229-1234`). A code span in the text does not affect it. **This form already works.**
- `[`code`]` (short) and `[`code`][]` (collapsed) take the key from `text` (`ShortReferenceInlineProcessor.evalId` `:1253-1256`; `ReferenceInlineProcessor.evalId` `:1235-1236`). The key is then the placeholder, so `if id not in self.md.references` fails (`:1216`), and the brackets are output literally. The definition was stored under the raw label, e.g. `` "`code`" `` (`blockprocessors.py:591-594`).
- Inline links `[`code`](/url)` use `getText` and `makeTag`, and the placeholder in the text is resolved later (`treeprocessors.py:310-316`, `:228-230`). No lookup depends on the label text, so they should already work (matches the issue's "other links with code are fine").

So the failing forms are the short and collapsed reference forms. Candidate fix: look up the raw label. The display text stays the placeholder, so the output and K4 are unchanged.

### Change 1: record the raw source of code spans (`markdown/treeprocessors.py`)

- In `InlineProcessor.run` (`:366`), next to `self.stashed_nodes = {}`, add `self.stashed_source: dict[str, str] = {}`. It must be reset on every run, because placeholder ids restart at `0000` for each document, and a stale entry would map to the wrong text.
- Extend `__stashNode(node, type)` with an optional `source: str | None = None`. When it is given, record `self.stashed_source[id] = source`.
- In `__applyPattern`, at the stash call (`:323`), pass the raw source **only for code spans**: when `new_style` is true and `pattern` is a `BacktickInlineProcessor`, pass `data[start:end]`. `start`/`end` are the values returned by `handleMatch` (`:286`), and for backticks they delimit the whole span including the backticks (`inlinepatterns.py:470-475`).
- Record only code spans, not escapes. Escape placeholders (ESC 180) are also present in reference labels. Recording them would change `[a\*b][]` lookups, which is outside issue #7 (see Risks).

### Change 2: look up the raw label (`markdown/inlinepatterns.py`)

- New method `ReferenceInlineProcessor.raw_label(self, text: str) -> str`. It replaces each placeholder matched by `util.INLINE_PLACEHOLDER_RE` with `stashed_source[id]` when a record exists, and leaves it unchanged otherwise. It reads the stash the same way `Pattern.unescape` does (`inlinepatterns.py:237-240`: `self.md.treeprocessors['inline']`, `KeyError` falls back to the input text).
- In `ReferenceInlineProcessor.handleMatch` (`:1201-1221`), pass `self.raw_label(text)` to `evalId` instead of `text`. Keep `text` for `makeTag` (`:1221`) so the link text stays the rendered code element.
- Result: `text.lower()` in the two `evalId` fallbacks now sees the raw label (e.g. `` `code` ``), which matches the definition key. The placeholder-free lowercase is safe: placeholders are ASCII lowercase plus digits (`util.py:71-75`), and the raw label is lowercased in the same way as the definition key (`blockprocessors.py:591`).
- Images share `handleMatch` (`ImageReferenceInlineProcessor`, `ShortImageReferenceInlineProcessor`). They get the same fix. This is intended (see Risks).

### Change 3: changelog and tests

- `docs/changelog.md`, under `[Unreleased]`: a "Fixed" entry, e.g. "Reference-style links whose text is a code span (`` [`code`] `` and `` [`code`][] ``) are now recognised when the reference is defined with the same code span."
- `tests/test_syntax/inline/test_links.py` (file exists; `test_code.py` and `test_images.py` are the neighbours). Add `assertMarkdownRenders` cases:
  - AC-FR-001-1: `` [`code`][ref]`` + blank line + `` [ref]: /url `` → `<p><a href="/url"><code>code</code></a></p>`.
  - AC-FR-001-2: `` [`code`] `` + blank line + `` [`code`]: /url `` → `<p><a href="/url"><code>code</code></a></p>`.
  - Collapsed form (extra, same fix): `` [`code`][] `` with the same definition → same output.
  - AC-FR-002-1, AC-FR-002-2, AC-NFR-001-1 as preservation tests (inline `[`code`](/url)`, `[text][ref]`, and `` [`<b>x</b>`](/url) `` → `<code>&lt;b&gt;x&lt;/b&gt;</code>`).

No change to any processor name, priority, or registry (K2). No change to any public signature (K1, K5); `evalId` keeps its signature and only receives a different string.

## Constraints respected

- **K1 (stage interfaces):** inline processors keep `handleMatch` and return values. `InlineProcessor.run` keeps returning the root. `__stashNode` is private (name-mangled) and gets an optional argument.
- **K2 (registries and priorities):** no priority or name changes. The fix sits inside the existing `reference` processor, which already runs after `backtick`.
- **K3 (attribute values):** no attribute is added. `makeTag` still sets `href`/`title` as strings, and `alt` is unescaped as before.
- **K4 (placeholders):** placeholders are never changed in the tree. The new code only reads placeholder ids to find raw source for the lookup key. The stashed element and the placeholder text in the output are the same as before.
- **K5 (backward compatibility):** no public name changed. `ReferenceInlineProcessor.evalId` is called with a different string, which subclasses of it will also see; the signature is unchanged. Python >= 3.11 and no new dependency.
- **Changelog rule:** `markdown/` is changed, so `docs/changelog.md` gets an `[Unreleased]` entry.
- **Tests:** the new cases go in the syntax tests using `assertMarkdownRenders`. Run with `python -m unittest discover tests`, not pytest.

## ARCHITECTURE.md vs source

Verified by reading the source at the pinned commit:

- Pipeline and stage order: `core.py` was not re-read for this design. Not relied on beyond the inline stage.
- C4 inline priorities: `backtick` 190, `escape` 180, `reference` 170, `link` 160, `image_link` 150, `image_reference` 140, `short_reference` 130, `em_strong` 60 (`inlinepatterns.py:74-93`). **Matches.**
- C4 placeholders: `InlineProcessor` placeholder logic at `treeprocessors.py:81-93`, `:172-251`. `util.py:67-81` (STX/ETX) and `util.py:71-75` (`INLINE_PLACEHOLDER_*`). **Matches.** Placeholders are lowercase ASCII, so `.lower()` does not corrupt them.
- `AtomicString` not reprocessed: `util.py:186-188`; `treeprocessors.py:132` (`isinstance(data, util.AtomicString)`). **Matches.**
- `Pattern.unescape` reading `md.treeprocessors['inline'].stashed_nodes`: `inlinepatterns.py:237-240`. **Matches**; the design copies this access pattern.
- K4 / ADR-T3 stash claim (placeholders restored after serialization): `postprocessors.py:73-93` not re-read here; used only as background.

**Discrepancies with the spec and the architecture document:**

1. **Spec EV-003 is only partly right.** The spec says reference links "are resolved by their raw label text". In the code, only the short form `[x]` and the collapsed form `[x][]` use the label text (`evalId`, `inlinepatterns.py:1235-1236`, `:1253-1256`). The explicit form `[text][id]` uses the id (`:1229-1234`). AC-FR-001-1 (`[`code`][ref]`) should therefore already pass, and is a regression guard, not a failing test. This is not yet executed: the design role has no Bash, so this is verified by reading only.
2. **Spec EV-004 not executed.** The claim that inline links with code work is based on reading `getText` (`:1151-1168`). Not run.
3. **Spec Q-001** remains open. The fix targets the short and collapsed forms. If the Testing stage finds that `[`code`](/url)` or `[`code`][ref]` fails for another reason, this design must be revisited.

Nothing in ARCHITECTURE.md was contradicted by the source for the claims used here.

## Risks

- **Stale stash records across runs.** Placeholder ids restart from `0000` for each document. If `stashed_source` is not reset alongside `stashed_nodes` in `run` (`:366`), a reused `Markdown` instance could map a placeholder to a previous document's code span. The reset is mandatory.
- **Reference-image side effect.** `![`x`]` with a definition `` [`x`]: /img `` now resolves too (shared `handleMatch`). Intended, but it is a behaviour change for images; the changelog entry should say links and images.
- **Escapes in labels stay broken.** `[a\*b][]` is still not resolved, because escape placeholders are not recorded. This is deliberate: recording them would change more than the issue asks for. If the maintainers want that, it is a follow-up.
- **Label whitespace.** The code element stores the stripped code text, but the raw source keeps its spaces. `` [` code `]`` now looks up `` ` code ` ``, which matches a definition written exactly that way. That is the correct key, since definitions are raw.
- **Third-party subclasses of `ReferenceInlineProcessor`** that override `evalId` and expect the placeholder string now receive raw text. This is a semantic change, not a signature change; no known bundled extension overrides it (not checked across the whole tree; `extensions/` was not searched).
- **Performance.** One dict write per code span, plus a regex substitution only on reference labels. Negligible; the stash path is hot, so keep the recording to the code-span branch.
- **Not executed.** No test was run in this stage. The root cause is from reading `treeprocessors.py:135-141, 253-330` and `inlinepatterns.py:1201-1237`. The Testing stage must confirm that AC-FR-001-2 fails before the change and passes after it.

## AutoSE stage check: names the files and functions to change

Result: **PASS**

- all checks passed
