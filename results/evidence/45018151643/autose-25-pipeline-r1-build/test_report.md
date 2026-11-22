---
artefact: test_report
issue: 25
round: 1
result: PASS
tests_ran: 1174
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
| AC-FR-002-2 | yes |

Test files: tests/test_syntax/extensions/test_toc.py

## New tests on the base commit (must fail)

Failed on base: **True**

```

======================================================================
ERROR: test_ac_fr_001_4_valueless_label_toc_links_to_heading (tests.test_syntax.extensions.test_toc.TestTOC.test_ac_fr_001_4_valueless_label_toc_links_to_heading)
`AC-FR-001-4`: the `toc` marker links to the heading ID when the label has no value.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/autose-base-zw9hcqmj/wt/tests/test_syntax/extensions/test_toc.py", line 265, in test_ac_fr_001_4_valueless_label_toc_links_to_heading
    output = markdown.markdown(
             ^^^^^^^^^^^^^^^^^^
  File "/tmp/autose-base-zw9hcqmj/wt/markdown/core.py", line 509, in markdown
    return md.convert(text)
           ^^^^^^^^^^^^^^^^
  File "/tmp/autose-base-zw9hcqmj/wt/markdown/core.py", line 374, in convert
    newRoot = treeprocessor.run(root)
              ^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/autose-base-zw9hcqmj/wt/markdown/extensions/toc.py", line 408, in run
    data_toc_label = run_postprocessors(unescape(el.attrib['data-toc-label']), self.md)
                                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/autose-base-zw9hcqmj/wt/markdown/extensions/toc.py", line 124, in unescape
    return c.unescape(text)
           ^^^^^^^^^^^^^^^^
  File "/tmp/autose-base-zw9hcqmj/wt/markdown/treeprocessors.py", line 470, in unescape
    return self.RE.sub(self._unescape, text)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: expected string or bytes-like object, got 'NoneType'

----------------------------------------------------------------------
Ran 75 tests in 0.426s

FAILED (errors=5)
```

## Full suite

```
................................................................................................................................s................................................................................sssssssssssssssssssssssssssssssssssssssssssssss............................................................................ss.......................................................................................................................................................................................................................ss...............................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................
----------------------------------------------------------------------
Ran 1174 tests in 1.112s

OK (skipped=52)
```

## AutoSE stage check: all new and existing tests pass

Result: **PASS**

- all checks passed
