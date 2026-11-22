---
artefact: test_report
issue: 6
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
| AC-FR-002-1 | yes |
| AC-FR-002-2 | yes |
| AC-FR-002-3 | yes |
| AC-FR-003-1 | yes |
| AC-FR-004-1 | yes |
| AC-FR-005-1 | yes |
| AC-NFR-001-1 | yes |

Test files: tests/test_apis.py, tests/test_cli_tab_length.py

## New tests on the base commit (must fail)

Failed on base: **True**

```

__main__.py: error: no such option: --tab_length


======================================================================
FAIL: test_ac_fr_002_3_item_b_nested_in_item_a (tests.test_cli_tab_length.TestTabLengthCliOption.test_ac_fr_002_3_item_b_nested_in_item_a)
AC-FR-002-3: with `--tab_length=2`, the `li` for `b` is a descendant of the `li` for `a`.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/autose-base-9184n7k1/wt/tests/test_cli_tab_length.py", line 85, in test_ac_fr_002_3_item_b_nested_in_item_a
    self.assertEqual(result.returncode, 0, result.stderr.decode('utf-8', 'replace'))
AssertionError: 2 != 0 : Usage: __main__.py [options] [INPUTFILE]
       (STDIN is assumed if no INPUTFILE is given)

__main__.py: error: no such option: --tab_length


======================================================================
FAIL: test_ac_fr_004_1_help_lists_option (tests.test_cli_tab_length.TestTabLengthCliOption.test_ac_fr_004_1_help_lists_option)
AC-FR-004-1: `python -m markdown --help` output contains `--tab_length`.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/tmp/autose-base-9184n7k1/wt/tests/test_cli_tab_length.py", line 112, in test_ac_fr_004_1_help_lists_option
    self.assertIn('--tab_length', result.stdout.decode('utf-8'))
AssertionError: '--tab_length' not found in "Usage: __main__.py [options] [INPUTFILE]\n       (STDIN is assumed if no INPUTFILE is given)\n\nA Python implementation of John Gruber's Markdown. https://python-\nmarkdown.github.io/\n\nOptions:\n  --version             show program's version number and exit\n  -h, --help            show this help message and exit\n  -f OUTPUT_FILE, --file=OUTPUT_FILE\n                        Write output to OUTPUT_FILE. Defaults to STDOUT.\n  -e ENCODING, --encoding=ENCODING\n                        Encoding for input and output files.\n  -o OUTPUT_FORMAT, --output_format=OUTPUT_FORMAT\n                        Use output format 'xhtml' (default) or 'html'.\n  -n, --no_lazy_ol      Observe number of first item of ordered lists.\n  -x EXTENSION, --extension=EXTENSION\n                        Load extension EXTENSION.\n  -c CONFIG_FILE, --extension_configs=CONFIG_FILE\n                        Read extension configurations from CONFIG_FILE.\n                        CONFIG_FILE must be of JSON or YAML format. YAML\n                        format requires that a python YAML library be\n                        installed. The parsed JSON or YAML must result in a\n                        python dictionary which would be accepted by the\n                        'extension_configs' keyword on the markdown.Markdown\n                        class. The extensions must also be loaded with the\n                        `--extension` option.\n  -q, --quiet           Suppress all warnings.\n  -v, --verbose         Print all warnings.\n  --noisy               Print debug messages.\n\nWARNING: The Python-Markdown library does NOT sanitize its HTML output. If you\nare processing Markdown input from an untrusted source, it is your\nresponsibility to ensure that it is properly sanitized. For more information\nsee <https://python-markdown.github.io/sanitization/>.\n"

----------------------------------------------------------------------
Ran 104 tests in 0.638s

FAILED (failures=7, errors=3)
```

## Full suite

```
...............................................................................................................................................s................................................................................sssssssssssssssssssssssssssssssssssssssssssssss............................................................................ss.......................................................................................................................................................................................................................ss.......................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................
----------------------------------------------------------------------
Ran 1181 tests in 2.172s

OK (skipped=52)
```

## AutoSE stage check: all new and existing tests pass

Result: **PASS**

- all checks passed
