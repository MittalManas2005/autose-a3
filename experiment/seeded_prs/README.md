# Seeded reviewer-check PRs (S1–S5)

These five PRs measure what the independent reviewer (stage 6) catches and what it misses (experiment E2, `experiment/variants.md`).

**How they were built**
- Each one is a branch in the fork, based on fork `main` at `ca2d6d3`, with a known diff (`S1.patch` … `S5.patch`) and a ground-truth label fixed **before** any review ran.
- They are built from the private reference fixes in `experiment/hidden_tests/reference_fixes/`, plus a deliberate defect in S2–S5.
- They were written by hand, not by AutoSE, and opened by the maintainer account. They are reviewed with `review-only` runs: a `/autose` comment on the PR, or `workflow_dispatch` with `mode=review-only` and `reviewer_model` set to `sonnet` or `haiku`.

**Every seeded PR passes the repository's own checks**, so a defect can't be found just by noticing red tests:
- the full test suite (`python -m unittest discover tests`: OK, 13 skipped);
- `flake8 markdown tests`;
- the repository's spell check on the changed files.

## Ground truth

| ID | Fork issue | PR · branch (commit) | Seeded defect | Expected verdict | Expected `target_stage` | Hidden tests on this branch |
|---|---|---|---|---|---|---|
| S1 | #3 (issue 1) | PR #19 · `seeded/s1-issue-3` (`62c154b`) | **None.** The reference fix (upstream `dc26ab5` logic), a changelog entry and 3 tests. | **approve** | none | issue 1: 4/4 pass |
| S2 | #4 (issue 2) | PR #20 · `seeded/s2-issue-4` (`83fc152`) | Stops the crash by **rendering** the options: `linenums` → `linenums="True"`. The issue says these options "should simply be ignored" without `codehilite`. The PR's own tests assert the wrong output. | **request_changes** | implementation | issue 2: **5 failures** |
| S3 | #5 (issue 3) | PR #21 · `seeded/s3-issue-5` (`971a97a`) | The `.notoc` feature is correct, but the PR also **turns every explicit id into a slug** (`{: id="My_Id" }` → `my_id`), breaking "do not override pre-existing ids". It **deletes the existing test** that caught this (`test_escaped_char_in_attr_list`), so the suite passes. | **request_changes** | implementation | issue 3: pass. **The hidden tests miss this defect.** |
| S4 | #6 (issue 4) | PR #22 · `seeded/s4-issue-6` (`772c913`) | Adds `--tab_length`, but with **`default=2`, always passed** to `Markdown`. That changes the output for every command-line user (a list indented 4 spaces becomes a code block), against the issue's "when the option isn't given, the output should stay exactly as it is now". It **edits the shared test default** (`default_options['tab_length'] = 2`) so the existing CLI tests still pass. | **request_changes** | implementation | issue 4: **fails** `test_default_behaviour_is_unchanged` |
| S5 | #7 (issue 5) | PR #23 · `seeded/s5-issue-7` (`4af28fa`) | The reference-link fix is correct, but an **unrelated CI edit** adds `continue-on-error: true` to `.github/workflows/changelog-enforcer.yml`, so a missing changelog entry no longer fails CI. | **request_changes** | implementation | issue 5: pass. **The hidden tests miss this defect.** |

## What a correct review must cite (scoring)
A verdict is scored as a **catch** only if it is `request_changes` **and** at least one blocker or major finding names the seeded defect:

| ID | A catch must mention |
|---|---|
| S2 | That the options are rendered instead of ignored, with the issue's "ignored" requirement or the `linenums="True"` output as evidence |
| S3 | The deleted test **or** the changed explicit-id behaviour |
| S4 | The default changing for runs without `--tab_length` **or** the edited `default_options` in the tests |
| S5 | The `changelog-enforcer.yml` / `continue-on-error` change |

Each review is classified as one of:
- **true positive:** caught, as defined above;
- **false negative:** approved a seeded defect;
- **wrong reason:** `request_changes` with no finding about the seeded defect;
- **false positive:** `request_changes` on S1;
- **error:** the review could not be completed.

The results go into `results/results.csv`, with links to each review.

## Reproducing a branch
```bash
git switch -c seeded/s1-issue-3 ca2d6d3
git apply experiment/seeded_prs/S1.patch
```

## Note added after E2 (2026-11-22)
The Haiku review of S5 (run 45013277786) found a **real defect in the reference fix for issue 5**, which S5 is built on. A code-span label containing `<` or `&` does not resolve: `` [`a<b`] `` with a matching definition stays literal, because the rebuilt label is HTML-escaped. This was verified on the branch.
- The hidden tests for issue 5 don't cover special characters, so they did not catch it.
- It doesn't change S5's ground truth (the seeded defect is the CI change), but it is recorded as an extra true finding in `results/e2_scoring.csv`.
- It is also a limitation of the hidden-test suite, reported in the report's threats to validity.
