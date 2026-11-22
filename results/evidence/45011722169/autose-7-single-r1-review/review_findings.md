# Independent reviewer findings (address every item)

The fix works for the reference-link cases I tried, but the PR also commits a leftover debugging file, tests/scratch_probe_issue7.py. It is unrelated to the change and deliberately fails when run.

- [major] tests/scratch_probe_issue7.py:1 A scratch probe script was committed to the repository. It is an unrelated file in the test tree. Its `test_probe` ends with `self.fail('probe')` and prints output for 26 inputs. `python -m unittest tests.scratch_probe_issue7` or an IDE test runner would run it and report a failure. — evidence: diff.patch adds tests/scratch_probe_issue7.py (40 lines) with `self.fail('probe')`. The file exists at the PR head.
