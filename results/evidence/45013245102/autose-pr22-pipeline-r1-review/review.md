---
artefact: review
pr: 22
issue: 6
round: 1
verdict: request_changes
target_stage: implementation
reviewer_model: sonnet
---

## AutoSE independent review (round 1)

**Verdict: request changes** (back to **implementation**)

The new --tab_length option defaults to 2, but the library default is 4. Output changes when the option isn't given, which the issue forbids.

### What I verified
- python -m unittest discover tests passes (1168 tests, OK), but the tests encode the wrong default
- Ran `python -m markdown` with '- a\n\n    - b\n' and no option. It renders b as a code block instead of a nested list, so default behaviour regressed.

### Commands I ran (from the session transcript, not self-reported)
- `python -c "import subprocess;print(subprocess.run(['python','-m','markdown'],input='- a\n\n    - b\n',capture_output=True,text=True).stdout)"` (ok)
- `python -m unittest discover tests` (ok)

### Findings

| severity | location | issue | evidence |
|---|---|---|---|
| blocker | `markdown/__main__.py`:69 | default=2 changes the CLI's default tab length from 4 to 2. Existing users with 4-space indented nested lists get different output, which breaks 'When the option isn't given, the output should stay exactly as it is now'. | Input '- a\n\n    - b\n' through `python -m markdown` with no option produces '<li>a<pre><code>- b\n</code></pre>' instead of a nested <ul>. Fix: default=4 (or leave it out of opts when not given). |
| major | `tests/test_apis.py`:800 | The test default_options was changed to expect 'tab_length': 2, which locks in the wrong default. No test checks end-to-end rendering with the option or that the default matches markdown.markdown. | diff adds `'tab_length': 2` to default_options. After the fix this should be 4, and the tests should cover the issue's example ('- a\n\n  - b\n' with --tab_length=2). |

_The reviewer saw only the issue, the diff and the repository at this PR's head. A maintainer decides whether to merge._
