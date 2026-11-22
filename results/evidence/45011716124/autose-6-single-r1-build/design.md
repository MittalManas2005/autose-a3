---
artefact: design
files:
  - path: markdown/__main__.py
    change: modify
    symbols: [parse_options]
    new_symbols: []
  - path: tests/test_cli_tab_length.py
    change: modify
    symbols: []
    new_symbols: [TestCliTabLength]
  - path: docs/cli.md
    change: modify
    symbols: []
    new_symbols: []
  - path: docs/changelog.md
    change: modify
    symbols: []
    new_symbols: []
tests: tests/test_cli_tab_length.py
---

## Plan
1. In `parse_options` (`markdown/__main__.py`), add `parser.add_option("--tab_length", dest="tab_length", type="int", default=None, metavar="TAB_LENGTH", ...)`. optparse supports both `--tab_length=2` and `--tab_length 2`, and rejects non-integers with exit code 2 (ASM-001).
2. Add `tab_length` to the returned options dictionary **only when it was given** (`if options.tab_length is not None`). The no-option dictionary stays identical, so AC-FR-003-1 and `testNoOptions` keep passing without edits. `markdownFromFile(**opts)` already forwards extra keys to `Markdown(**kwargs)`, which reads `tab_length` (`markdown/core.py:110`), so no change to `core.py` is needed.
3. Add a test module `tests/test_cli_tab_length.py` with one test per AC (`test_ac_fr_001_1_…`, etc.). CLI behaviour is exercised end to end by running `python -m markdown` in a subprocess, plus `parse_options` for the parsing ACs.
4. Document the option in `docs/cli.md` (help listing) and add a `### Added` entry under `[Unreleased]` in `docs/changelog.md`, with identifiers in backticks.

## Constraints respected
- Public API unchanged: no existing option, key or function is renamed or removed (K5).
- No new runtime dependency; Python 3.11+ compatible (K5).
- Only `markdown/`, `tests/`, `docs/` are changed.
- Changelog entry required for changes under `markdown/` (ARCHITECTURE §4.1).
- flake8 with max line length 119.
- Tests use `unittest`; not pytest.

## ARCHITECTURE.md vs source
- Claim: the CLI is `markdown/__main__.py` and `parse_options` builds the dictionary passed to `markdownFromFile`. Verified: `markdown/__main__.py:45-127`, `:148`.
- Claim: `Markdown` reads `tab_length` from kwargs with default 4. Verified: `markdown/core.py:110`.
- Claim: `markdownFromFile` forwards kwargs to `Markdown`. Verified: `markdown/core.py:512-536`.
- No discrepancy found.

## Risks
- Existing test `testNoOptions` asserts the exact dictionary; adding the key unconditionally would break it. Mitigated by adding the key only when given.
- The subprocess test depends on running from the repository (`python -m markdown` must import the checkout). Mitigated by setting `cwd` to the directory that contains the `markdown` package.
- `optparse` `type="int"` accepts negative and zero values; this follows ASM-001.
