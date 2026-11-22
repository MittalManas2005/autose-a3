---
artefact: test_report
issue: 4
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
| AC-FR-001-2 | yes |
| AC-FR-001-3 | yes |
| AC-FR-001-4 | yes |
| AC-FR-001-5 | yes |
| AC-FR-002-1 | yes |
| AC-FR-003-1 | yes |
| AC-NFR-001-1 | yes |
| AC-NFR-001-2 | yes |
| AC-NFR-001-3 | yes |
| AC-NFR-002-1 | yes |

Test files: tests/test_syntax/extensions/test_fenced_code.py, tests/test_syntax/extensions/test_fenced_code_codehilite_only_options.py

## New tests on the base commit (must fail)

Failed on base: **True**

```
TypeError: argument of type 'NoneType' is not iterable

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/tmp/autose-base-jb40cb9f/wt/tests/test_syntax/extensions/test_fenced_code_codehilite_only_options.py", line 59, in test_ac_fr_002_1_other_attributes_kept_on_code_element
    output = markdown.markdown(
             ^^^^^^^^^^^^^^^^^^
  File "/tmp/autose-base-jb40cb9f/wt/markdown/core.py", line 509, in markdown
    return md.convert(text)
           ^^^^^^^^^^^^^^^^
  File "/tmp/autose-base-jb40cb9f/wt/markdown/core.py", line 367, in convert
    self.lines = prep.run(self.lines)
                 ^^^^^^^^^^^^^^^^^^^^
  File "/tmp/autose-base-jb40cb9f/wt/markdown/extensions/fenced_code.py", line 159, in run
    kv_pairs = ''.join(
               ^^^^^^^^
  File "/tmp/autose-base-jb40cb9f/wt/markdown/extensions/fenced_code.py", line 160, in <genexpr>
    f' {sanitize_name(k)}="{_escape_attrib_html(v)}"'
                            ^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/autose-base-jb40cb9f/wt/markdown/serializers.py", line 137, in _escape_attrib_html
    _raise_serialization_error(text)
  File "/tmp/autose-base-jb40cb9f/wt/markdown/serializers.py", line 81, in _raise_serialization_error
    raise TypeError(
TypeError: cannot serialize None (type NoneType)

----------------------------------------------------------------------
Ran 56 tests in 0.047s

FAILED (errors=12)
```

## Full suite

```
................................................................................................................................s................................................................................sssssssssssssssssssssssssssssssssssssssssssssss............................................................................ss.......................................................................................................................................................................................................................ss......................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................
----------------------------------------------------------------------
Ran 1181 tests in 1.603s

OK (skipped=52)
```

## AutoSE stage check: all new and existing tests pass

Result: **PASS**

- all checks passed
