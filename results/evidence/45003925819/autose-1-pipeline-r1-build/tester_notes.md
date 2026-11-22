# Tester notes: issue #1

## Status
The tests were **not executed**. The Bash tool was denied in this run, so `python -m unittest` and flake8 could not be run. Verification was by reading the code only. The next run should execute:

    python -m unittest tests.test_syntax.extensions.test_toc

## Changes
- `tests/test_syntax/extensions/test_toc.py`
  - added `import markdown` at the top;
  - added five methods after `testValuelessTocLabelIgnored` (existing tests untouched).

## Criterion → test mapping
| AC | Test | Oracle |
|---|---|---|
| AC-FR-001-1 | `test_ac_fr_001_1_valueless_toc_label_no_exception` | no exception, `str` returned |
| AC-FR-002-1 | `test_ac_fr_002_1_valueless_toc_label_heading_output` | contains `<h1 id="heading">Heading</h1>` |
| AC-FR-002-2 | `test_ac_fr_002_2_valueless_toc_label_toc_entry_uses_heading_text` | `md.toc` contains `<li><a href="#heading">Heading</a></li>` |
| AC-FR-002-3 | `test_ac_fr_002_3_valueless_toc_label_attribute_not_in_output` | output does not contain `data-toc-label` |
| AC-FR-002-4 | `test_ac_fr_002_4_valued_toc_label_preserved` | `md.toc` contains `<li><a href="#heading">Short</a></li>` |

## Expected behaviour on unchanged code (reasoned, not run)
- AC-FR-001-1, AC-FR-002-1, AC-FR-002-2, AC-FR-002-3 should fail on the unchanged `toc.py`: the valueless `None` reaches `unescape()` and raises `TypeError`.
- AC-FR-002-4 is a preservation check (valued label). It should pass on unchanged code too, by design.

## Points to check
- Line 409 of `markdown/extensions/toc.py` (the new comment) may exceed the 119-character limit. flake8 was not run.
- The staged `testValuelessTocLabelIgnored` covers the same behaviour as the AC tests but has no criterion ID. It was left in place, as the rules require.
