---
artefact: review
pr: 9
issue: 6
round: 1
verdict: approve
target_stage: none
reviewer_model: haiku
---

## AutoSE independent review (round 1)

**Verdict: approve**

PR #9 adds a `--tab_length` option to the CLI (`markdown/__main__.py`), forwards it only when given, and documents it in the changelog and `docs/cli.md`. The change resolves issue #6 and leaves the no-option output unchanged. I found no blocker or major problems. Three minor points are noted below.

### What I verified
- Full suite: `python -m unittest discover tests` -> Ran 1183 tests, OK (skipped=52).
- Changed modules: `python -m unittest tests.test_apis tests.test_cli_tab_length_ac` -> Ran 106 tests, OK. This includes the subprocess tests that run `python -m markdown --tab_length=2` and `--tab_length 2`.
- flake8 on markdown/__main__.py, tests/test_apis.py, tests/test_cli_tab_length_ac.py -> no output (clean).
- `parse_options(['--tab_length=2'])` and `parse_options(['--tab_length', '2'])` yield `tab_length: 2`; without the option the key is absent, so the default path is unchanged.
- `markdown.markdown('- a\n\n  - b\n', tab_length=2)` nests `b` under `a`, which matches what the CLI option is meant to produce. `markdown.markdown(..., tab_length=-2)` and `tab_length=0` are forwarded the same way, so the CLI does not add new behaviour there.
- `markdownFromFile(**kwargs)` passes kwargs to `Markdown`, which reads `tab_length` from kwargs (core.py:110), so the option reaches the library.
- Diff touches only docs, `markdown/__main__.py` and tests; no CI files, no escaping or raw-HTML code paths changed.
- Limits: Bash pipes, file writes under /tmp and `--help` were denied in this session, so the end-to-end CLI checks ran via the unit tests and direct `parse_options`/library calls rather than ad-hoc shell runs.

### Commands I ran (from the session transcript, not self-reported)
- `python -m unittest discover tests` (ok)
- `python -m unittest tests.test_apis tests.test_cli_tab_length_ac` (ok)
- `printf -- '- a\n\n  - b\n' | python -m markdown --tab_length 2` (failed)
- `python -m markdown --tab_length=0 /dev/null` (failed)
- `python -m flake8 markdown/__main__.py tests/test_apis.py tests/test_cli_tab_length_ac.py` (ok)
- `python -c "import markdown; print(repr(markdown.markdown('- a\n\n\t- b\n', tab_length=0)))"` (ok)
- `python -m markdown --tab_length 2 /tmp/claude/review6/in.md` (failed)
- `python -m markdown --tab_length=abc /tmp/claude/review6/in.md` (failed)
- `python -m markdown --tab_length=-2 /tmp/claude/review6/in.md` (failed)
- `python -c "from markdown.__main__ import parse_options as p; print(p(['--tab_length=-2'])); print(p(['--tab_length=0']))"` (ok)
- `python -c "import markdown; print(repr(markdown.markdown('- a\n\n  - b\n', tab_length=2))); print(repr(markdown.markdown('- a\n\n  - b\n', tab_length=-2)))"` (ok)
- `python -c "import markdown; print(repr(markdown.markdown('- a\n\n  - b\n', tab_length=2, extensions=['markdown.extensions.toc'])))"` (ok)
- `python -m markdown --help` (failed)

### Findings

| severity | location | issue | evidence |
|---|---|---|---|
| minor | `tests/test_cli_tab_length_ac.py` | New test file duplicates the coverage of `TestCliTabLength` in tests/test_apis.py (same helpers, same inputs, same assertions) and is named and organised around internal acceptance-criterion IDs (`AC-FR-001-1`, `FR-00x`). Those IDs are pipeline artifacts that do not belong in the project's test layout. | tests/test_cli_tab_length_ac.py:1-4 and :205-277 vs tests/test_apis.py:1058-1095 (`TestCliTabLength`). |
| minor | `docs/cli.md` | The `--tab_length` help block in the docs was hand-written and may not match what optparse prints; the `--help` line in the code is 'Number of spaces per tab in the source. Defaults to 4.' Not verified against live `--help` output in this session because that command was denied. | docs/cli.md:26-27 vs markdown/__main__.py:71-73. |
| minor | `markdown/__main__.py` | No validation of non-positive values. `--tab_length=0` or `-2` is accepted and passed to the library, which then renders code blocks with odd indentation. This matches the library's own behaviour, so it is not a regression, but a maintainer may want a bounds check. | `markdown.markdown('- a\n\n  - b\n', tab_length=-2)` -> '<pre><code> a\n\n b\n</code></pre>'; `parse_options(['--tab_length=-2'])` -> tab_length: -2. |

_The reviewer saw only the issue, the diff and the repository at this PR's head. A maintainer decides whether to merge._
