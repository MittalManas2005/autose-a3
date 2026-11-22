---
artefact: test_report
issue: 3
round: 1
result: PASS
tests_ran: 1171
base_tests: 1166
---

# Test report

## Acceptance criteria → tests

| AC | covered by a new test |
|---|---|
| AC-FR-001-1 | yes |
| AC-FR-001-2 | yes |
| AC-FR-001-3 | yes |
| AC-FR-002-1 | yes |
| AC-FR-003-1 | yes |

Test files: tests/test_syntax/extensions/test_toc.py

## New tests on the base commit (must fail)

Failed on base: **True**

```
  File "/tmp/autose-base-uw6i7pjq/wt/markdown/extensions/toc.py", line 417, in run
    'id': unescape(el.attrib["id"]),
          ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/autose-base-uw6i7pjq/wt/markdown/extensions/toc.py", line 124, in unescape
    return c.unescape(text)
           ^^^^^^^^^^^^^^^^
  File "/tmp/autose-base-uw6i7pjq/wt/markdown/treeprocessors.py", line 470, in unescape
    return self.RE.sub(self._unescape, text)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: expected string or bytes-like object, got 'NoneType'

======================================================================
FAIL: test_ac_fr_003_1_empty_string_id_generated (tests.test_syntax.extensions.test_toc.TestTOC.test_ac_fr_003_1_empty_string_id_generated)
AC-FR-003-1: a heading with `{: id="" }` gets the auto-generated id (issue #3).
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/autose-base-uw6i7pjq/wt/tests/test_syntax/extensions/test_toc.py", line 1140, in test_ac_fr_003_1_empty_string_id_generated
    self.assertMarkdownRenders(
  File "/tmp/autose-base-uw6i7pjq/wt/markdown/test_tools.py", line 77, in assertMarkdownRenders
    self.assertMultiLineEqual(output, expected)
AssertionError: '<h1 id="">Heading</h1>' != '<h1 id="heading">Heading</h1>'
- <h1 id="">Heading</h1>
+ <h1 id="heading">Heading</h1>
?         +++++++


----------------------------------------------------------------------
Ran 72 tests in 0.305s

FAILED (failures=1, errors=3)
```

## Full suite

```
................................................................................................................................s................................................................................sssssssssssssssssssssssssssssssssssssssssssssss............................................................................ss.......................................................................................................................................................................................................................ss............................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................
----------------------------------------------------------------------
Ran 1171 tests in 0.943s

OK (skipped=52)
```

## AutoSE stage check: all new and existing tests pass

Result: **PASS**

- all checks passed
