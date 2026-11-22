---
artefact: test_report
issue: 4
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
| AC-FR-001-5 | yes |
| AC-FR-002-1 | yes |
| AC-FR-003-1 | yes |
| AC-FR-004-1 | yes |

Test files: tests/test_syntax/extensions/test_fenced_code.py

## New tests on the base commit (must fail)

Failed on base: **True**

```
    kv_pairs = ''.join(
               ^^^^^^^^
  File "/tmp/autose-base-jq5vagan/wt/markdown/extensions/fenced_code.py", line 160, in <genexpr>
    f' {sanitize_name(k)}="{_escape_attrib_html(v)}"'
                            ^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/autose-base-jq5vagan/wt/markdown/serializers.py", line 137, in _escape_attrib_html
    _raise_serialization_error(text)
  File "/tmp/autose-base-jq5vagan/wt/markdown/serializers.py", line 81, in _raise_serialization_error
    raise TypeError(
TypeError: cannot serialize None (type NoneType)

======================================================================
FAIL: test_ac_fr_002_1_hl_lines_ignored_without_codehilite (tests.test_syntax.extensions.test_fenced_code.TestFencedCode.test_ac_fr_002_1_hl_lines_ignored_without_codehilite)
AC-FR-002-1: `hl_lines` is omitted from `<code>` when codehilite is not enabled (issue #4).
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/autose-base-jq5vagan/wt/tests/test_syntax/extensions/test_fenced_code.py", line 500, in test_ac_fr_002_1_hl_lines_ignored_without_codehilite
    self.assertMarkdownRenders(
  File "/tmp/autose-base-jq5vagan/wt/markdown/test_tools.py", line 77, in assertMarkdownRenders
    self.assertMultiLineEqual(output, expected)
AssertionError: '<pre><code class="language-python" hl_lines="[1, 3]">print(1)\n</code></pre>' != '<pre><code class="language-python">print(1)\n</code></pre>'
- <pre><code class="language-python" hl_lines="[1, 3]">print(1)
?                                   ------------------
+ <pre><code class="language-python">print(1)
  </code></pre>

----------------------------------------------------------------------
Ran 49 tests in 0.027s

FAILED (failures=1, errors=6)
```

## Full suite

```
................................................................................................................................s................................................................................sssssssssssssssssssssssssssssssssssssssssssssss............................................................................ss.......................................................................................................................................................................................................................ss...............................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................
----------------------------------------------------------------------
Ran 1174 tests in 0.905s

OK (skipped=52)
```

## AutoSE stage check: all new and existing tests pass

Result: **PASS**

- all checks passed
