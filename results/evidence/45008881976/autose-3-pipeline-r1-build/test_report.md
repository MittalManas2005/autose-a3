---
artefact: test_report
issue: 3
round: 1
result: PASS
tests_ran: 1181
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
| AC-FR-002-5 | yes |
| AC-FR-003-1 | yes |
| AC-FR-003-2 | yes |
| AC-FR-004-1 | yes |

Test files: tests/test_syntax/extensions/test_attr_list.py, tests/test_syntax/extensions/test_toc.py

## New tests on the base commit (must fail)

Failed on base: **True**

```
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: expected string or bytes-like object, got 'NoneType'

======================================================================
ERROR: test_valueless_id_unique_with_duplicate_heading (tests.test_syntax.extensions.test_toc.TestTOC.test_valueless_id_unique_with_duplicate_heading)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/autose-base-k8xvk2hz/wt/tests/test_syntax/extensions/test_toc.py", line 1512, in test_valueless_id_unique_with_duplicate_heading
    self.assertMarkdownRenders(
  File "/tmp/autose-base-k8xvk2hz/wt/markdown/test_tools.py", line 76, in assertMarkdownRenders
    output = md.convert(source)
             ^^^^^^^^^^^^^^^^^^
  File "/tmp/autose-base-k8xvk2hz/wt/markdown/core.py", line 374, in convert
    newRoot = treeprocessor.run(root)
              ^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/autose-base-k8xvk2hz/wt/markdown/extensions/toc.py", line 417, in run
    'id': unescape(el.attrib["id"]),
          ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/autose-base-k8xvk2hz/wt/markdown/extensions/toc.py", line 124, in unescape
    return c.unescape(text)
           ^^^^^^^^^^^^^^^^
  File "/tmp/autose-base-k8xvk2hz/wt/markdown/treeprocessors.py", line 470, in unescape
    return self.RE.sub(self._unescape, text)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: expected string or bytes-like object, got 'NoneType'

----------------------------------------------------------------------
Ran 109 tests in 0.514s

FAILED (errors=8)
```

## Full suite

```
................................................................................................................................s................................................................................sssssssssssssssssssssssssssssssssssssssssssssss............................................................................ss.......................................................................................................................................................................................................................ss......................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................
----------------------------------------------------------------------
Ran 1181 tests in 1.535s

OK (skipped=52)
```

## AutoSE stage check: all new and existing tests pass

Result: **PASS**

- all checks passed
