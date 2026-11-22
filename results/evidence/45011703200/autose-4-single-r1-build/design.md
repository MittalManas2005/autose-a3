---
artefact: design
files:
  - path: markdown/extensions/fenced_code.py
    change: modify
    symbols: [FencedBlockPreprocessor.__init__, FencedBlockPreprocessor.run]
    new_symbols: [FencedBlockPreprocessor.highlight_only_options]
  - path: tests/test_syntax/extensions/test_fenced_code.py
    change: modify
    symbols: [TestFencedCode]
    new_symbols: [TestFencedCode.test_ac_fr_001_1_linenums_ignored_without_codehilite, TestFencedCode.test_ac_fr_001_2_linenums_true_ignored_without_codehilite, TestFencedCode.test_ac_fr_001_3_linenums_quoted_one_ignored_without_codehilite, TestFencedCode.test_ac_fr_001_4_guess_lang_ignored_without_codehilite, TestFencedCode.test_ac_fr_001_5_noclasses_ignored_without_codehilite, TestFencedCode.test_ac_fr_002_1_hl_lines_ignored_without_codehilite, TestFencedCode.test_ac_fr_003_1_other_attributes_kept_without_codehilite, TestFencedCode.test_ac_fr_004_1_codehilite_highlighting_unchanged]
  - path: docs/extensions/fenced_code_blocks.md
    change: modify
    symbols: []
    new_symbols: []
  - path: docs/changelog.md
    change: modify
    symbols: []
    new_symbols: []
tests: tests/test_syntax/extensions/test_fenced_code.py
---

# Design for issue #4

## Plan
1. In `FencedBlockPreprocessor.__init__` (`markdown/extensions/fenced_code.py:77-89`), add the attribute `self.highlight_only_options`, built from the existing `self.bool_options` (`linenums`, `guess_lang`, `noclasses`, `use_pygments`) plus `hl_lines`.
2. In `FencedBlockPreprocessor.run`, in the non-highlighting branch (`fenced_code.py:155-162`), build `kv_pairs` from the keys of `config` that are not in `self.highlight_only_options`. The `use_pygments` filter is subsumed, because `use_pygments` is in that list.
3. Cover every criterion with tests in `TestFencedCode` (`tests/test_syntax/extensions/test_fenced_code.py`), named `test_ac_fr_00X_Y_...`, with the AC ID in the docstring:
   - AC-FR-001-1..5: the five forms of the highlighting-only options (exact output).
   - AC-FR-002-1: `hl_lines`.
   - AC-FR-003-1: `data-x="y"` kept next to `linenums`.
   - AC-FR-004-1: codehilite highlighting still applies (contains `class="codehilite"`). This goes in the `codehilite` test class, `TestFencedCodeWithCodehilite`, or the same file, since the oracle does not depend on Pygments.
4. Add a sentence to `docs/extensions/fenced_code_blocks.md` (after line 216): when highlighting is not used, `linenums`, `guess_lang`, `noclasses`, `hl_lines` and `use_pygments` are omitted from `<code>`.
5. Add a `### Fixed` entry under `[Unreleased]` in `docs/changelog.md`, with identifiers in backticks and a reference to #4.

Expected output for the issue's example after the change: `<pre><code class="language-python">print(1)\n</code></pre>`, the same as without the option.

## Constraints respected
- K1/K2 (pipeline and registry): no change to processor names, priorities or interfaces. `fenced_code_block` stays at 25 (`fenced_code.py:58`).
- K3 (attribute values must be `str` or `None`): the fix stops passing the non-string values (bool, list, None) to the writer. It does not change the writer or the `attr_list` behaviour. The escape helper raises `TypeError` for these values (`serializers.py:80-83`, `serializers.py:123-137`).
- K5 (public API, no runtime dependency): no new public names; no dependency added.
- Existing tests: `testFencedLanguageAttrLinenums`, `testFencedLanguageAttrGuesslang` and `testFencedLanguageAttrNoclasses` run with `codehilite` (their path is the highlighting branch), and are not affected. `testFencedLanguagePygmentsDisabledInAttrNoCodehiliteWithAttrList` (`use_pygments=False` is not written) and `testFencedLanguagePygmentsEnabledInAttrNoCodehiliteWithAttrList` (no attributes when `use_pygments=True`) keep their output, because `use_pygments` is still excluded.
- Changelog required for changes under `markdown/` (`docs/contributing.md:535-547`, per ARCHITECTURE §4.1).
- flake8 max line length 119.

## ARCHITECTURE.md vs source
- ARCHITECTURE C2/C3: `fenced_code_block` at priority 25 (`fenced_code.py:58`). Verified.
- ARCHITECTURE K3: non-string attribute values raise `TypeError`. Verified in `serializers.py:80-83` and `serializers.py:123-137`, where `_escape_attrib_html` catches `TypeError` and re-raises through `_raise_serialization_error`. Note: ARCHITECTURE says the serializer writes `None` as a bare attribute (`serializers.py:186-196`). That path is for the serializer's own attribute writing; the fenced-code path passes the value through `_escape_attrib_html`, so `None` there raises, which matches the issue.
- ARCHITECTURE does not describe the `fenced_code` attribute-writing branch. The claim used here comes from reading `fenced_code.py:155-164` directly. No discrepancy with the source.
- `hl_lines` is a list of ints (`codehilite.py:43-55`). It is not rejected by `_escape_attrib_html` (no exception for lists), so today it renders as `hl_lines="[1, 3]"`. This is reasoned from reading the code and not executed. The new test would fail on the old code if this were wrong, so the test asserts the absence.

## Risks
- A user who relies on `linenums`, `guess_lang`, `noclasses` or `hl_lines` being present as attributes without `codehilite` loses that output. Today those forms crash (for bool and None values), so the only observable change is from a crash to a rendering. For `hl_lines`, the change is from `hl_lines="[1, 3]"` to no attribute. Flagged as Q-001 / ASM-001.
- `use_pygments` is already excluded; its behaviour does not change.
- The new option set also applies when `codehilite` is enabled with `use_pygments=False` and the block falls into the non-highlighting branch. Previously such a block with `attr_list` crashed for the same options, so this is also a fix. No existing test covers that combination.
