---
artefact: test_report
issue: 7
round: 2
result: PASS
tests_ran: 1170
base_tests: 1166
---

# Test report

## Acceptance criteria → tests

| AC | covered by a new test |
|---|---|
| AC-FR-001-1 | yes |
| AC-FR-001-2 | yes |
| AC-FR-001-3 | yes |
| AC-FR-001-4 | yes |

Test files: tests/scratch_probe_issue7.py, tests/test_syntax/inline/test_links.py

## New tests on the base commit (must fail)

Failed on base: **True**

```
AC-FR-001-1: A short reference whose label is a code span resolves to its definition.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/autose-base-m3ogq9z2/wt/tests/test_syntax/inline/test_links.py", line 440, in test_ac_fr_001_1_short_reference_code_label
    self.assertMarkdownRenders(
  File "/tmp/autose-base-m3ogq9z2/wt/markdown/test_tools.py", line 77, in assertMarkdownRenders
    self.assertMultiLineEqual(output, expected)
AssertionError: '<p>[<code>code</code>]</p>' != '<p><a href="http://example.com"><code>code</code></a></p>'
- <p>[<code>code</code>]</p>
+ <p><a href="http://example.com"><code>code</code></a></p>


======================================================================
FAIL: test_ac_fr_001_2_implicit_reference_code_label (tests.test_syntax.inline.test_links.TestReferenceLinks.test_ac_fr_001_2_implicit_reference_code_label)
AC-FR-001-2: An implicit reference whose label is a code span resolves to its definition.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/autose-base-m3ogq9z2/wt/tests/test_syntax/inline/test_links.py", line 453, in test_ac_fr_001_2_implicit_reference_code_label
    self.assertMarkdownRenders(
  File "/tmp/autose-base-m3ogq9z2/wt/markdown/test_tools.py", line 77, in assertMarkdownRenders
    self.assertMultiLineEqual(output, expected)
AssertionError: '<p>[<code>code</code>][]</p>' != '<p><a href="http://example.com"><code>code</code></a></p>'
- <p>[<code>code</code>][]</p>
+ <p><a href="http://example.com"><code>code</code></a></p>


----------------------------------------------------------------------
Ran 45 tests in 0.019s

FAILED (failures=3)
```

## Full suite

```
................................................................................................................................s................................................................................sssssssssssssssssssssssssssssssssssssssssssssss............................................................................ss.......................................................................................................................................................................................................................ss...........................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................
----------------------------------------------------------------------
Ran 1170 tests in 1.168s

OK (skipped=52)
```

## AutoSE stage check: all new and existing tests pass

Result: **PASS**

- all checks passed
