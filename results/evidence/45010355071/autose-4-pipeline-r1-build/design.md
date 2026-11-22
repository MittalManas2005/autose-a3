---
artefact: design
issue: 4
files:
  - path: markdown/extensions/fenced_code.py
    change: modify
    symbols: [FencedBlockPreprocessor.run]
    new_symbols: [FencedBlockPreprocessor.HIGHLIGHT_ONLY_OPTIONS]
  - path: tests/test_syntax/extensions/test_fenced_code.py
    change: modify
    symbols: [TestFencedCode]
    new_symbols: [testFencedLanguageLinenumsFlagNoCodehiliteWithAttrList, testFencedLanguageLinenumsTrueNoCodehiliteWithAttrList, testFencedLanguageLinenumsQuotedNoCodehiliteWithAttrList, testFencedLanguageGuesslangNoCodehiliteWithAttrList, testFencedLanguageNoclassesNoCodehiliteWithAttrList, testFencedLanguageAllHighlightOptionsNoCodehiliteWithAttrList, testFencedLanguageLinenumsNoCodehiliteNoAttrList, testFencedCodeAttrDataNoCodehiliteWithAttrList]
  - path: docs/changelog.md
    change: modify
    symbols: []
    new_symbols: []
tests: tests/test_syntax/extensions/test_fenced_code.py
---

## Plan

### Root cause (verified by reading the source)
1. `FencedBlockPreprocessor.handle_attrs` (`markdown/extensions/fenced_code.py:181-185`) turns a valueless attribute into `v = k`, so `linenums` becomes the string `"linenums"`.
2. Because `linenums` is in `self.bool_options` (`fenced_code.py:84-89`, `192-193`), it is passed through `parseBoolValue(v, fail_on_errors=False, preserve_none=True)`. `"linenums"` is not a boolean word, so the function falls through and returns `None` (`markdown/util.py:136-152`).
3. With `attr_list` enabled and no `codehilite`, the non-highlighting branch (`fenced_code.py:155-162`) writes every config key into `kv_pairs` with `_escape_attrib_html(v)`. For `None`, `"&" in None` raises `TypeError`, which `_escape_attrib_html` converts to `TypeError("cannot serialize None (type NoneType)")` (`markdown/serializers.py:123-137`). That is the reported error (SRC-005).
4. `linenums=true` and `linenums="1"` fail the same way with `True`, and `guess_lang` / `noclasses` fail with `None` or `True`. `use_pygments` is already excluded at line 160.

### Change 1: `markdown/extensions/fenced_code.py` (FR-001, FR-002, FR-003)
- Add a class constant `FencedBlockPreprocessor.HIGHLIGHT_ONLY_OPTIONS = ('linenums', 'guess_lang', 'noclasses')`, the options that only have meaning for syntax highlighting.
- In `run()`, in the `else` branch where `kv_pairs` is built (lines 155-162), skip keys in `HIGHLIGHT_ONLY_OPTIONS` when `not self.codehilite_conf`. Keep the existing `use_pygments` exclusion and the `self.use_attr_list and config and not config.get('use_pygments', False)` gate unchanged. The effect: when `codehilite` is absent, these options are dropped before any attribute is written, so the block renders as if they were not written (FR-001, TERM-001 reading (a)). Other keys are still written as before, so `data-x="y"` still reaches the `<code>` element (FR-002).
- Gate on `not self.codehilite_conf` and not unconditionally. `codehilite_conf` is `{}` unless `CodeHiliteExtension` is registered (`fenced_code.py:81`, `96-98`), and is non-empty whenever it is. Gating this way keeps the codehilite-enabled behaviour unchanged (FR-003). It also keeps the `codehilite` + `use_pygments=False` case unchanged, which is Q-001 / ASM-002.
- No change to `handle_attrs`, the highlighting branch (lines 127-145), the placeholder/stash logic (lines 166-169), `serializers.py`, or `attr_list.py`.

Rejected alternatives:
- Dropping the options in `handle_attrs`: would also change the codehilite branch, which reads `linenums`/`guess_lang`/`noclasses` from `config` (lines 127-143).
- Making the serializer accept `None`/`bool` for arbitrary attributes: would emit `linenums="..."`-style junk on the element and would change the serializer for all extensions (violates K3 intent and the spec's "ignored" reading).

### Change 2: `tests/test_syntax/extensions/test_fenced_code.py`
Add tests to `TestFencedCode` (the class with no `codehilite`), next to `testFencedLanguageNoCodehiliteWithAttrList` (line 289). Use `self.assertMarkdownRenders(source, expected, extensions=[...])` with the fragment expected by each AC; the expected HTML is `<pre><code class="language-python">print(1)\n</code></pre>` (no `id`, no extra attributes):
- AC-FR-001-1: flag `linenums`, `["fenced_code", "attr_list"]`.
- AC-FR-001-2: `linenums=true`.
- AC-FR-001-3: `linenums="1"`.
- AC-FR-001-4: `guess_lang`.
- AC-FR-001-5: `noclasses`.
- AC-FR-001-6: `linenums guess_lang noclasses` together.
- AC-FR-001-7: `linenums`, `["fenced_code"]` only (preservation; ASM-001).
- AC-FR-002-1: `{ .python data-x="y" linenums }`, `["fenced_code", "attr_list"]`, expected `<pre><code class="language-python" data-x="y">print(1)`. Hyphen kept: `NAME_RE` includes `\-` (`markdown/extensions/attr_list.py:99-103`), verified.
- AC-FR-003-1: no new test. The existing `testFencedLanguageAttrLinenums` (line 789) is the preservation oracle; it must keep passing unchanged.

Tests must not depend on Pygments output for the new cases (no `codehilite` is involved).

### Change 3: `docs/changelog.md`
Add a bullet under `## [Unreleased]` → `### Fixed` (line 17 onward), e.g.: "Ignore the `linenums`, `guess_lang` and `noclasses` options on fenced code blocks when the `codehilite` extension is not enabled, instead of raising an error when `attr_list` is also enabled." Required because `markdown/` changes (K5, `docs/contributing.md:535-547`).

### Acceptance-criteria coverage
| AC | Covered by |
|---|---|
| AC-FR-001-1 … -6 | Change 1 (filter) + new tests 1-6 |
| AC-FR-001-7 | Change 1 is inside the `attr_list` gate; test 7 confirms no output without `attr_list` (ASM-001) |
| AC-FR-002-1 | Change 1 keeps non-highlight keys; test 8 |
| AC-FR-003-1 | Change 1 gated on `codehilite` absence; existing `testFencedLanguageAttrLinenums` unchanged |

## Constraints respected
- **K1 (stage interfaces):** `FencedBlockPreprocessor.run(lines) -> list[str]` signature and behaviour contract unchanged.
- **K2 (registries and priorities):** no registration added, removed or re-prioritised; `fenced_code_block` stays at 25 (`fenced_code.py:58`).
- **K3 (attribute values):** the change only removes non-`str`/`None` values from attribute output; it writes no new non-string values. `attr_list` `None` handling is untouched.
- **K4 (stash):** the rendered block still goes through `self.md.htmlStash.store(code)` (`fenced_code.py:166-167`); placeholders are not altered.
- **K5 (backward compatibility):** no public name, option name or entry point changes; no new dependency; Python 3.11 compatible. The only behaviour change is that a configuration that used to raise `TypeError` now renders. Changelog entry added.
- **Changelog rule:** entry under `[Unreleased]` (`docs/changelog.md:15`).
- **Testing convention:** `TestCase.assertMarkdownRenders` under `tests/test_syntax/`; run with `python -m unittest discover tests`.

## ARCHITECTURE.md vs source
Claims checked against the source at this commit:
- `fenced_code_block` registered at priority 25 in `fenced_code.py:58`. **Confirmed.**
- Option keys written to the code element only when `attr_list` is enabled and `use_pygments` is not truthy, `fenced_code.py:155-164`. **Confirmed.** (The spec's EV-002 cites the same lines.)
- Attribute `None` renders as a bare attribute, `serializers.py:186-189`. **Confirmed** (the `if v is None: write(f" {k}")` branch).
- Valueless attributes become `None` in `attr_list`, `attr_list.py:53-63` (`_handle_word` returns `t, None`). **Confirmed.** Also `fenced_code.py:182-185` converts them to `v = k` before `parseBoolValue`.
- `NAME_RE` keeps hyphens, `attr_list.py:99-103` (`\-` in the allowed set). **Confirmed.** This resolves the spec's EV-008 "unverified" note for `data-x`.
- `parseBoolValue` returns `None` for unparsable input when `fail_on_errors=False`, `util.py:136-152`. **Confirmed.**
- Changelog has `## [Unreleased]` at `docs/changelog.md:15`. **Confirmed.**

Discrepancies:
1. **K3 / C5 overstate the serializer's rejection.** ARCHITECTURE says any non-string value raises `TypeError` (`serializers.py:80-83`). In fact the error is raised by the `except` in `_escape_attrib_html` / `_escape_attrib` (`serializers.py:136-137`, `119-120`) and only for types on which `in` or `.replace` fails (for example `None`, `bool`, `int`). A `list` value passes through these helpers without error. The rule for extensions is still "use `str` or `None`", so the design follows it. Not executed; by reading.
2. **Spec EV-003 is slightly imprecise.** The spec says a bare flag "yields None" in `parseBoolValue`. The flag actually becomes the string `"linenums"` (`fenced_code.py:182-185`), and `parseBoolValue` returns `None` because that word is not a boolean. The conclusion (the `None` in the error message) is correct.
3. Not checked (not needed for this change): the priorities cited for `codehilite` (30), `attr_list` (8), `smarty` (6), `toc` (5) in ARCHITECTURE §2.3 and the test count in §4.1.

## Risks
- **Q-001 / ASM-002 (open question):** with `codehilite` enabled and a block setting `use_pygments=False`, the design leaves the existing behaviour unchanged, so `linenums` on such a block can still hit the same `TypeError`. This is deliberate (the spec marks it out of scope). If maintainers answer "yes" to Q-001, removing the `not self.codehilite_conf` gate is a one-line follow-up. That gate is the only thing to flip.
- **Silent drop:** these options are discarded without a warning when `codehilite` is absent. This is the requested behaviour (TERM-001), not a defect, but is worth stating in the PR.
- **`hl_lines` outside `codehilite`** (`fenced_code.py:190-191`, `122-123`) is not covered by the spec and is not changed. Not executed; I did not verify how it renders with `attr_list` enabled and no `codehilite`.
- **Test expectations:** the expected string assumes the current `<pre><code ...>` layout with a trailing newline in `print(1)\n`. Test authors should copy the exact form from the existing tests at lines 253-305 rather than retyping it.
- **Pygments dependency:** AC-FR-003-1 relies on the existing Pygments-dependent test; the new tests do not use Pygments.

## AutoSE stage check: names the files and functions to change

Result: **PASS**

- all checks passed
