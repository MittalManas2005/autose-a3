---
artefact: test_report
issue: 1
round: 1
result: PASS
tests_ran: 1172
base_tests: 1166
---

# Test report

## Acceptance criteria → tests

| AC | covered by a new test |
|---|---|
| AC-FR-001-1 | yes |
| AC-FR-002-1 | yes |
| AC-FR-002-2 | yes |
| AC-FR-002-3 | yes |
| AC-FR-002-4 | yes |

Test files: tests/test_syntax/extensions/test_toc.py

## New tests on the base commit (must fail)

Failed on base: **True**

```

======================================================================
ERROR: test_ac_fr_002_3_valueless_toc_label_attribute_not_in_output (tests.test_syntax.extensions.test_toc.TestTOC.test_ac_fr_002_3_valueless_toc_label_attribute_not_in_output)
AC-FR-002-3: Given `# Heading {: data-toc-label }` with extensions `["toc", "attr_list"]`,
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/autose-base-mp5qpepm/wt/tests/test_syntax/extensions/test_toc.py", line 241, in test_ac_fr_002_3_valueless_toc_label_attribute_not_in_output
    html = markdown.markdown('# Heading {: data-toc-label }', extensions=['toc', 'attr_list'])
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/autose-base-mp5qpepm/wt/markdown/core.py", line 509, in markdown
    return md.convert(text)
           ^^^^^^^^^^^^^^^^
  File "/tmp/autose-base-mp5qpepm/wt/markdown/core.py", line 374, in convert
    newRoot = treeprocessor.run(root)
              ^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/autose-base-mp5qpepm/wt/markdown/extensions/toc.py", line 408, in run
    data_toc_label = run_postprocessors(unescape(el.attrib['data-toc-label']), self.md)
                                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/autose-base-mp5qpepm/wt/markdown/extensions/toc.py", line 124, in unescape
    return c.unescape(text)
           ^^^^^^^^^^^^^^^^
  File "/tmp/autose-base-mp5qpepm/wt/markdown/treeprocessors.py", line 470, in unescape
    return self.RE.sub(self._unescape, text)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: expected string or bytes-like object, got 'NoneType'

----------------------------------------------------------------------
Ran 73 tests in 0.516s

FAILED (errors=5)
```

## Full suite

```
................................................................................................................................s................................................................................sssssssssssssssssssssssssssssssssssssssssssssss............................................................................ss.......................................................................................................................................................................................................................ss.............................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................
----------------------------------------------------------------------
Ran 1172 tests in 1.609s

OK (skipped=52)
```

## Tester notes

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

## AutoSE stage check: all new and existing tests pass

Result: **PASS**

- all checks passed
