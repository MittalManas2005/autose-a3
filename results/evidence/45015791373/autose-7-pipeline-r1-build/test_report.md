---
artefact: test_report
issue: 7
round: 1
result: PASS
tests_ran: 1176
base_tests: 1166
---

# Test report

## Acceptance criteria → tests

| AC | covered by a new test |
|---|---|
| AC-FR-001-2 | yes |
| AC-FR-001-3 | yes |
| AC-FR-001-4 | yes |
| AC-FR-001-5 | yes |
| AC-FR-002-1 | yes |

Test files: tests/test_syntax/inline/test_links.py, tests/test_syntax/inline/test_links_code_label.py

## New tests on the base commit (must fail)

Failed on base: **True**

```
    self.assertMarkdownRenders(
  File "/tmp/autose-base-6ko_8gsw/wt/markdown/test_tools.py", line 77, in assertMarkdownRenders
    self.assertMultiLineEqual(output, expected)
AssertionError: '<p>[<code>foo</code>]</p>' != '<p><a href="https://example.com"><code>foo</code></a></p>'
- <p>[<code>foo</code>]</p>
+ <p><a href="https://example.com"><code>foo</code></a></p>


======================================================================
FAIL: test_ac_fr_001_3_reference_shortcut_code_label (tests.test_syntax.inline.test_links_code_label.TestIssue7CodeInLinkLabel.test_ac_fr_001_3_reference_shortcut_code_label)
`AC-FR-001-3`: a shortcut reference with a code span becomes a link.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/autose-base-6ko_8gsw/wt/tests/test_syntax/inline/test_links_code_label.py", line 46, in test_ac_fr_001_3_reference_shortcut_code_label
    self.assertIn('<a href="https://example.com"><code>foo</code></a>', html)
AssertionError: '<a href="https://example.com"><code>foo</code></a>' not found in '<p>[<code>foo</code>]</p>'

======================================================================
FAIL: test_ac_fr_001_4_reference_full_code_label (tests.test_syntax.inline.test_links_code_label.TestIssue7CodeInLinkLabel.test_ac_fr_001_4_reference_full_code_label)
`AC-FR-001-4`: a full reference with a code span in the `id` becomes a link.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/autose-base-6ko_8gsw/wt/tests/test_syntax/inline/test_links_code_label.py", line 59, in test_ac_fr_001_4_reference_full_code_label
    self.assertIn('<a href="https://example.com">text</a>', html)
AssertionError: '<a href="https://example.com">text</a>' not found in '<p>[text][<code>foo</code>]</p>'

----------------------------------------------------------------------
Ran 50 tests in 0.012s

FAILED (failures=5)
```

## Full suite

```
................................................................................................................................s................................................................................sssssssssssssssssssssssssssssssssssssssssssssss............................................................................ss.......................................................................................................................................................................................................................ss.................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................
----------------------------------------------------------------------
Ran 1176 tests in 1.109s

OK (skipped=52)
```

## AutoSE stage check: all new and existing tests pass

Result: **PASS**

- all checks passed
