---
artefact: test_report
issue: 5
round: 1
result: PASS
tests_ran: 1175
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
| AC-FR-002-1 | yes |
| AC-FR-003-1 | yes |
| AC-FR-003-2 | yes |
| AC-FR-004-1 | yes |
| AC-FR-004-2 | yes |

Test files: tests/test_syntax/extensions/test_toc.py

## New tests on the base commit (must fail)

Failed on base: **True**

```
  File "/tmp/autose-base-wvbi3026/wt/tests/test_syntax/extensions/test_toc.py", line 1531, in test_ac_fr_001_3_notoc_token_in_multiple_classes
    self.assertNotIn('href="#two"', html)
AssertionError: 'href="#two"' unexpectedly found in '<div class="toc">\n<ul>\n<li><a href="#one">One</a><ul>\n<li><a href="#two">Two</a></li>\n<li><a href="#three">Three</a></li>\n</ul>\n</li>\n</ul>\n</div>\n<h1 id="one">One</h1>\n<h2 class="other notoc" id="two">Two</h2>\n<h2 id="three">Three</h2>'

======================================================================
FAIL: test_ac_fr_002_1_notoc_heading_absent_from_toc_tokens (tests.test_syntax.extensions.test_toc.TestTocNotoc.test_ac_fr_002_1_notoc_heading_absent_from_toc_tokens)
`AC-FR-002-1`: a heading with the `notoc` class is left out of `toc_tokens`.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/autose-base-wvbi3026/wt/tests/test_syntax/extensions/test_toc.py", line 1545, in test_ac_fr_002_1_notoc_heading_absent_from_toc_tokens
    self.assertEqual(self.flatten_names(md.toc_tokens), ['One', 'Three'])
AssertionError: Lists differ: ['One', 'Two', 'Three'] != ['One', 'Three']

First differing element 1:
'Two'
'Three'

First list contains 1 additional elements.
First extra element 2:
'Three'

- ['One', 'Two', 'Three']
?        -------

+ ['One', 'Three']

----------------------------------------------------------------------
Ran 76 tests in 0.518s

FAILED (failures=3)
```

## Full suite

```
................................................................................................................................s................................................................................sssssssssssssssssssssssssssssssssssssssssssssss............................................................................ss.......................................................................................................................................................................................................................ss................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................
----------------------------------------------------------------------
Ran 1175 tests in 1.605s

OK (skipped=52)
```

## AutoSE stage check: all new and existing tests pass

Result: **PASS**

- all checks passed
