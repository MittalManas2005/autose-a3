---
artefact: test_report
issue: 7
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
| AC-FR-001-2 | yes |
| AC-FR-002-1 | yes |
| AC-FR-002-2 | yes |
| AC-NFR-001-1 | yes |

Test files: tests/test_syntax/inline/test_links.py

## New tests on the base commit (must fail)

Failed on base: **True**

```
======================================================================
FAIL: test_ref_link_code_span_mixed_case (tests.test_syntax.inline.test_links.TestReferenceLinks.test_ref_link_code_span_mixed_case)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/autose-base-470u9to9/wt/tests/test_syntax/inline/test_links.py", line 476, in test_ref_link_code_span_mixed_case
    self.assertMarkdownRenders(
  File "/tmp/autose-base-470u9to9/wt/markdown/test_tools.py", line 77, in assertMarkdownRenders
    self.assertMultiLineEqual(output, expected)
AssertionError: '<p>[<code>Code</code>]</p>' != '<p><a href="/url"><code>Code</code></a></p>'
- <p>[<code>Code</code>]</p>
+ <p><a href="/url"><code>Code</code></a></p>


======================================================================
FAIL: test_ref_link_code_span_short (tests.test_syntax.inline.test_links.TestReferenceLinks.test_ref_link_code_span_short)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/autose-base-470u9to9/wt/tests/test_syntax/inline/test_links.py", line 452, in test_ref_link_code_span_short
    self.assertMarkdownRenders(
  File "/tmp/autose-base-470u9to9/wt/markdown/test_tools.py", line 77, in assertMarkdownRenders
    self.assertMultiLineEqual(output, expected)
AssertionError: '<p>[<code>code</code>]</p>' != '<p><a href="/url"><code>code</code></a></p>'
- <p>[<code>code</code>]</p>
+ <p><a href="/url"><code>code</code></a></p>


----------------------------------------------------------------------
Ran 53 tests in 0.018s

FAILED (failures=4)
```

## Full suite

```
................................................................................................................................s................................................................................sssssssssssssssssssssssssssssssssssssssssssssss............................................................................ss.......................................................................................................................................................................................................................ss....................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................
----------------------------------------------------------------------
Ran 1179 tests in 1.510s

OK (skipped=52)
```

## AutoSE stage check: all new and existing tests pass

Result: **PASS**

- all checks passed
