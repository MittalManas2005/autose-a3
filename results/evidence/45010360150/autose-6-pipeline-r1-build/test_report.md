---
artefact: test_report
issue: 6
round: 1
result: PASS
tests_ran: 1183
base_tests: 1166
---

# Test report

## Acceptance criteria → tests

| AC | covered by a new test |
|---|---|
| AC-FR-001-1 | yes |
| AC-FR-001-2 | yes |
| AC-FR-002-1 | yes |
| AC-FR-002-2 | yes |
| AC-FR-003-1 | yes |
| AC-FR-004-1 | yes |
| AC-FR-004-2 | yes |
| AC-FR-005-1 | yes |

Test files: tests/test_apis.py, tests/test_cli_tab_length_ac.py

## New tests on the base commit (must fail)

Failed on base: **True**

```
======================================================================
FAIL: test_ac_fr_003_1_output_matches_library (tests.test_cli_tab_length_ac.TestAcFr003.test_ac_fr_003_1_output_matches_library)
`AC-FR-003-1`: the output equals `markdown.markdown()` with `tab_length=2`.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/autose-base-b_8vir3m/wt/tests/test_cli_tab_length_ac.py", line 83, in test_ac_fr_003_1_output_matches_library
    self.assertEqual(result.returncode, 0)
AssertionError: 2 != 0

======================================================================
FAIL: test_ac_fr_005_1_markdown_py_matches_module (tests.test_cli_tab_length_ac.TestAcFr005.test_ac_fr_005_1_markdown_py_matches_module)
`AC-FR-005-1`: `markdown_py --tab_length=2` equals `python -m markdown --tab_length=2`.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/autose-base-b_8vir3m/wt/tests/test_cli_tab_length_ac.py", line 117, in test_ac_fr_005_1_markdown_py_matches_module
    self.assertEqual(script.stdout, module.stdout)
AssertionError: '<ul>\n<li>\n<p>a</p>\n<ul>\n<li>b</li>\n</ul>\n</li>\n</ul>' != ''
- <ul>
- <li>
- <p>a</p>
- <ul>
- <li>b</li>
- </ul>
- </li>
- </ul>

----------------------------------------------------------------------
Ran 106 tests in 1.257s

FAILED (failures=11, errors=2)
```

## Full suite

```
.................................................................................................................................................s................................................................................sssssssssssssssssssssssssssssssssssssssssssssss............................................................................ss.......................................................................................................................................................................................................................ss.......................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................
----------------------------------------------------------------------
Ran 1183 tests in 2.874s

OK (skipped=52)
```

## AutoSE stage check: all new and existing tests pass

Result: **PASS**

- all checks passed
