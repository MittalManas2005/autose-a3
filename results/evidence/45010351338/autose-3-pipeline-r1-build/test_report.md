---
artefact: test_report
issue: 3
round: 1
result: PASS
tests_ran: 1179
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
| AC-FR-003-1 | yes |
| AC-FR-003-2 | yes |
| AC-FR-004-1 | yes |

Test files: tests/test_syntax/extensions/test_toc.py

## New tests on the base commit (must fail)

Failed on base: **True**

```
FAIL: test_empty_id_heading (tests.test_syntax.extensions.test_toc.TestTOC.test_empty_id_heading)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/autose-base-qeexsegd/wt/tests/test_syntax/extensions/test_toc.py", line 1115, in test_empty_id_heading
    self.assertMarkdownRenders(
  File "/tmp/autose-base-qeexsegd/wt/markdown/test_tools.py", line 77, in assertMarkdownRenders
    self.assertMultiLineEqual(output, expected)
AssertionError: '<h1 id="">Heading</h1>' != '<h1 id="heading">Heading</h1>'
- <h1 id="">Heading</h1>
+ <h1 id="heading">Heading</h1>
?         +++++++


======================================================================
FAIL: test_ac_fr_002_4_empty_id_gets_generated_id (tests.test_syntax.extensions.test_toc.TestTOCValuelessIdAcceptance.test_ac_fr_002_4_empty_id_gets_generated_id)
`AC-FR-002-4`: an empty `id` (`id=""`) heading gets the generated `slug` id.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/autose-base-qeexsegd/wt/tests/test_syntax/extensions/test_toc.py", line 1575, in test_ac_fr_002_4_empty_id_gets_generated_id
    self.assertEqual(
AssertionError: '<h1 id="">Heading</h1>' != '<h1 id="heading">Heading</h1>'
- <h1 id="">Heading</h1>
+ <h1 id="heading">Heading</h1>
?         +++++++


----------------------------------------------------------------------
Ran 80 tests in 0.515s

FAILED (failures=2, errors=6)
```

## Full suite

```
................................................................................................................................s................................................................................sssssssssssssssssssssssssssssssssssssssssssssss............................................................................ss.......................................................................................................................................................................................................................ss....................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................
----------------------------------------------------------------------
Ran 1179 tests in 1.610s

OK (skipped=52)
```

## AutoSE stage check: all new and existing tests pass

Result: **PASS**

- all checks passed
