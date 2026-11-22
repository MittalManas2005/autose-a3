---
artefact: test_report
issue: 5
round: 1
result: PASS
tests_ran: 1186
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
| AC-FR-001-5 | yes |
| AC-FR-002-1 | yes |
| AC-FR-002-2 | yes |
| AC-FR-002-3 | yes |
| AC-FR-003-1 | yes |
| AC-FR-004-1 | yes |
| AC-FR-004-2 | yes |
| AC-FR-005-1 | yes |

Test files: tests/test_syntax/extensions/test_toc.py

## New tests on the base commit (must fail)

Failed on base: **True**

```
AssertionError: 'href="#two"' unexpectedly found in '<div class="toc">\n<ul>\n<li><a href="#one">One</a><ul>\n<li><a href="#two">Two</a></li>\n<li><a href="#three">Three</a></li>\n</ul>\n</li>\n</ul>\n</div>\n'

======================================================================
FAIL: test_notoc_heading_excluded_from_toc_tokens (tests.test_syntax.extensions.test_toc.TestTOC.test_notoc_heading_excluded_from_toc_tokens)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/autose-base-sk31uj01/wt/tests/test_syntax/extensions/test_toc.py", line 1550, in test_notoc_heading_excluded_from_toc_tokens
    self.assertNotIn('two', ids)
AssertionError: 'two' unexpectedly found in ['one', 'two', 'three']

======================================================================
FAIL: test_notoc_permalink (tests.test_syntax.extensions.test_toc.TestTOC.test_notoc_permalink)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/autose-base-sk31uj01/wt/tests/test_syntax/extensions/test_toc.py", line 1619, in test_notoc_permalink
    self.assertNotIn('href="#two"', md.toc)
AssertionError: 'href="#two"' unexpectedly found in '<div class="toc">\n<ul>\n<li><a href="#one">One</a><ul>\n<li><a href="#two">Two</a></li>\n</ul>\n</li>\n</ul>\n</div>\n'

======================================================================
FAIL: test_notoc_with_other_classes (tests.test_syntax.extensions.test_toc.TestTOC.test_notoc_with_other_classes)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/autose-base-sk31uj01/wt/tests/test_syntax/extensions/test_toc.py", line 1565, in test_notoc_with_other_classes
    self.assertNotIn('href="#two"', md.toc)
AssertionError: 'href="#two"' unexpectedly found in '<div class="toc">\n<ul>\n<li><a href="#one">One</a><ul>\n<li><a href="#two">Two</a></li>\n<li><a href="#three">Three</a></li>\n</ul>\n</li>\n</ul>\n</div>\n'

----------------------------------------------------------------------
Ran 87 tests in 0.521s

FAILED (failures=8)
```

## Full suite

```
................................................................................................................................s................................................................................sssssssssssssssssssssssssssssssssssssssssssssss............................................................................ss.......................................................................................................................................................................................................................ss...........................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................
----------------------------------------------------------------------
Ran 1186 tests in 1.632s

OK (skipped=52)
```

## AutoSE stage check: all new and existing tests pass

Result: **PASS**

- all checks passed
