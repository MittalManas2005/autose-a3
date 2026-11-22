---
artefact: test_report
issue: 6
round: 1
result: PASS
tests_ran: 1172
base_tests: 1166
---

# Test report

## Acceptance criteria → tests

| AC | covered by a new test |
|---|---|
| AC-FR-001-1 | yes |
| AC-FR-001-2 | yes |
| AC-FR-002-1 | yes |
| AC-FR-003-1 | yes |
| AC-FR-003-2 | yes |

Test files: tests/test_cli_tab_length.py

## New tests on the base commit (must fail)

Failed on base: **True**

```
  File "/tmp/autose-base-cr1c1hn2/wt/markdown/__main__.py", line 94, in parse_options
    (options, args) = parser.parse_args(args, values)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/optparse.py", line 1389, in parse_args
    self.error(str(err))
  File "/opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/optparse.py", line 1569, in error
    self.exit(2, "%s: error: %s\n" % (self.get_prog_name(), msg))
  File "/opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/optparse.py", line 1559, in exit
    sys.exit(status)
SystemExit: 2

======================================================================
ERROR: test_ac_fr_002_1_output_matches_keyword (tests.test_cli_tab_length.TestCliTabLength.test_ac_fr_002_1_output_matches_keyword)
AC-FR-002-1: With `--tab_length=2` the CLI output equals `markdown.markdown(..., tab_length=2)`.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/autose-base-cr1c1hn2/wt/tests/test_cli_tab_length.py", line 53, in test_ac_fr_002_1_output_matches_keyword
    actual = run_cli(['--tab_length=2'], SOURCE)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/autose-base-cr1c1hn2/wt/tests/test_cli_tab_length.py", line 25, in run_cli
    result = subprocess.run(
             ^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.11.18/x64/lib/python3.11/subprocess.py", line 571, in run
    raise CalledProcessError(retcode, process.args,
subprocess.CalledProcessError: Command '['/opt/hostedtoolcache/Python/3.11.18/x64/bin/python', '-m', 'markdown', '--tab_length=2']' returned non-zero exit status 2.

----------------------------------------------------------------------
Ran 6 tests in 0.097s

FAILED (errors=3)
```

## Full suite

```
......................................................................................................................................s................................................................................sssssssssssssssssssssssssssssssssssssssssssssss............................................................................ss.......................................................................................................................................................................................................................ss.......................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................
----------------------------------------------------------------------
Ran 1172 tests in 1.192s

OK (skipped=52)
```

## AutoSE stage check: all new and existing tests pass

Result: **PASS**

- all checks passed
