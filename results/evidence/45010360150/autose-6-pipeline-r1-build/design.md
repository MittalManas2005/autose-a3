---
artefact: design
issue: 6
files:
  - path: markdown/__main__.py
    change: modify
    symbols: [parse_options]
    new_symbols: []
  - path: docs/cli.md
    change: modify
    symbols: []
    new_symbols: []
  - path: docs/changelog.md
    change: modify
    symbols: []
    new_symbols: []
  - path: tests/test_apis.py
    change: modify
    symbols: [TestCliOptionParsing]
    new_symbols: [TestCliOptionParsing.testTabLengthOption, TestCliOptionParsing.testTabLengthSpaceSeparated, TestCliOptionParsing.testTabLengthInvalid, TestCliTabLength]
tests: tests/test_apis.py
---

# Design for issue #6: Command line: add an option to set `tab_length`

## Plan

The library already accepts `tab_length` as a keyword (`markdown/core.py:110`), and the CLI already forwards its parsed options to the library (`markdown/__main__.py:117-125`, `:146-148`). The change is therefore confined to the option parser, plus docs and tests. No processor, priority, or library module changes.

### 1. `markdown/__main__.py` (modify `parse_options`)

a. **Register the option** next to the other value-taking options (after `--no_lazy_ol`, before `-x`, around line 70):

- `parser.add_option("--tab_length", dest="tab_length", type="int", default=None, metavar="TAB_LENGTH", help="...")`
- `type="int"` lets optparse parse both `--tab_length=2` and `--tab_length 2` (FR-002), and makes an invalid value a usage error with exit status 2 (ASM-001).
- No short alias (ASM-004).
- Help text: a one-line description that says the value is the length of tabs in the source, in spaces, and that the default is 4.
- `--help` lists the option automatically (AC-FR-001-1).

b. **Forward the value only when it was given**, after the `opts` dictionary is built (`:117-125`):

- `if options.tab_length is not None: opts['tab_length'] = options.tab_length`

Why conditional and not always-present:
- If the key were always present with `default=4`, `parse_options([])` would return a different dictionary. That breaks the existing `testNoOptions` (`tests/test_apis.py:809-811`), which is RSK-001.
- If the key were always present with `default=None`, `Markdown` would receive `tab_length=None`. `core.py:110` would store `None`, and `preprocessors.py:73` (`source.expandtabs(self.md.tab_length)`) would raise `TypeError`. That would break FR-004.
- Omitting the key keeps the no-option path byte-for-byte identical (FR-004, AC-FR-004-1/2).

Data flow once the option is given: `run()` → `markdownFromFile(**opts)` (`markdown/core.py:512-538`) → `Markdown(**kwargs)` → `self.tab_length` (`core.py:110`). `markdownFromFile` reads only `input`, `output`, `encoding` itself and passes the rest to `Markdown`, which already accepts `tab_length` (the same path as `output_format` and `lazy_ol`).

`markdown_py` (FR-005): `pyproject.toml:71` maps it to `markdown.__main__:run`, the same function as `python -m markdown`. No separate change is needed.

### 2. `docs/cli.md` (modify)

- Add the `--tab_length=TAB_LENGTH` entry, with its help text, to the `--help` block at lines 45-67, in the same position the parser emits it (the block is in parser order; the `-n, --no_lazy_ol` entry is already missing from it, so place the new entry between `-o, --output_format` and `-x, --extension`). The help block there is a hand copy of real `--help` output, so the new entry must match the option's help string exactly.
- Optionally add a short paragraph under "Basic Usage" with one example (`python -m markdown --tab_length=2 input.txt`). Not required by any AC; ASM-003 says the option should be documented there.

### 3. `docs/changelog.md` (modify, required)

- Add a `### Added` subsection directly above `### Fixed` under `## [Unreleased]` (line 15-17). Entry: "Add a `--tab_length` option to the command line (`python -m markdown` and `markdown_py`) to set the length of tabs in the source, as the `tab_length` keyword does in the library (#6)."

### 4. `tests/test_apis.py` (modify)

Add tests to `TestCliOptionParsing` (imports already include `parse_options`, `os`, `sys`, `unittest`, `markdown`; line 32, 27-30) and one new subprocess-based class:

- `testTabLengthOption` (FR-002): `parse_options(['--tab_length=2'])` returns the default dict plus `tab_length: 2`.
- `testTabLengthSpaceSeparated` (FR-002): `parse_options(['--tab_length', '2'])` gives the same result.
- `testTabLengthInvalid` (ASM-001, Q-001 pending): `--tab_length=abc` raises `SystemExit` with code 2. Redirect stderr with `contextlib.redirect_stderr` to keep test output clean. The test encodes the proposed default; if Q-001 changes the answer, update this test.
- `testNoOptions` is left unchanged and must still pass, since the key is only added when given.

New class `TestCliTabLength` (the acceptance criteria are CLI-level, so use a subprocess):

- Run `[sys.executable, '-m', 'markdown', ...]` with `cwd` set to the repository root (the parent of the `markdown` package), `stdin` set to the input text, and `capture_output=True`.
- Input text: `"- a\n\n  - b\n"`. (Same input as the spec's ACs.)
- Cover:
  - AC-FR-001-1: `--help` output contains `--tab_length`.
  - AC-FR-001-2: with `--tab_length=2`, `<li>b</li>` sits inside a nested `<ul>` inside the `<li>` for `a`. Check with a substring or `xml.etree` parse; keep it simple.
  - AC-FR-002-1: `--tab_length 2` and `--tab_length=2` give identical stdout.
  - AC-FR-002-2: `--tab_length=2` exits 0 and produces output.
  - AC-FR-003-1: stdout equals `markdown.markdown(text, tab_length=2)` (plus the trailing newline behaviour of the CLI, which the implementer should check by comparing to the same expression used in an existing CLI test if one exists, or by `.strip()` on both sides).
  - AC-FR-004-1: with no option, output contains `<li>b</li>` and that `<li>` is not nested.
  - AC-FR-004-2: with no option, stdout equals `markdown.markdown(text)`.
  - AC-FR-005-1: if `shutil.which('markdown_py')` is `None`, skip with `unittest.skipIf`; otherwise compare its stdout with `python -m markdown` for the same arguments.

No changes to `markdown/core.py`, `markdown/preprocessors.py`, `markdown/blockprocessors.py`, or any extension.

## Constraints respected

- **K1 (stage interfaces).** Not touched.
- **K2 (registries and priorities).** No processor is added or reprioritised. The change is in the CLI option parser, which is not a registry.
- **K3 (attribute values).** Not applicable. `tab_length` is an integer setting, not an element attribute.
- **K4 (stash and placeholders).** Not applicable.
- **K5 (backward compatibility).** Purely additive: a new optional flag with the same default behaviour (default 4 via `core.py:110`). No names, entry points, or config keys are removed or renamed. The existing `Markdown`/`markdown`/`markdownFromFile` signatures are unchanged. Python `>=3.11`, and only the standard library (`optparse`, `subprocess`, `shutil`) is used in tests; no new runtime dependency.
- **Changelog rule.** `markdown/__main__.py` is under `markdown/`, so `docs/changelog.md` gets an `[Unreleased]` entry (`changelog.md:15`).
- **Tests rule.** New feature has tests in the existing `tests/test_apis.py` (`docs/contributing.md:93-96` per ARCHITECTURE; not separately verified).
- **Style.** flake8 max line length 119 (ARCHITECTURE §4.1; `tox.ini:45-46` not re-read in this pass).

## ARCHITECTURE.md vs source

Claims I relied on and checked against source:

| Claim | Where checked | Result |
|---|---|---|
| CLI lives in `markdown/__main__.py`; `parse_options` builds the parser and the `opts` dict | `markdown/__main__.py:45-127` | Confirmed. |
| `run()` forwards `opts` to `markdownFromFile` | `markdown/__main__.py:130-148` | Confirmed (`markdownFromFile(**options)` at `:148`). |
| `Markdown` reads `tab_length` from kwargs, default 4 | `markdown/core.py:110` | Confirmed. |
| `markdown()` / `markdownFromFile()` pass kwargs to `Markdown` | `markdown/core.py:484-538` | Confirmed. |
| Tab length is used by the preprocessors | `markdown/preprocessors.py:73` (`expandtabs(self.md.tab_length)`) | Confirmed by grep. |
| `markdown_py` maps to the same entry point | `pyproject.toml:71` (`markdown_py = 'markdown.__main__:run'`) | Confirmed by grep. |
| Changelog has `## [Unreleased]` and a `### Fixed` subsection | `docs/changelog.md:15`, `:17` | Confirmed. `### Added` does not yet exist under Unreleased. |
| Existing CLI tests compare the full option dict | `tests/test_apis.py:794-811` | Confirmed (this is RSK-001). |

Discrepancies:
- **Commit pin.** `ARCHITECTURE.md` says the pinned commit is `3f2c5510`. The spec's `base_commit` is `ca2d6d37`, and the repository's recent history shows `ca2d6d3` as HEAD. The document is a map, so I based the plan on the source I read in the working checkout. The pin should be reconciled, but it does not change this design.
- **Priorities and processor names (ARCHITECTURE §2.2 C3, C4).** Not relied on by this change, so not re-verified.

No other discrepancies found for the claims this plan uses.

## Risks

- **RSK-001 (test expectation).** `testNoOptions` keeps passing because the key is only added when given. If the maintainers later prefer an always-present key, that test must change in the same PR.
- **Invalid and boundary values (ASM-001, ASM-002, Q-001, Q-002 pending).** Non-integers should give a usage error with exit 2 through optparse's `type="int"`. I did not run this (the design role has no execution), so this is based on optparse's documented behaviour. The library does not validate `tab_length` (`core.py:110`). Zero or negative values are passed through unchanged. Several block processors compute values from `tab_length`, for example `blockprocessors.py:172`, `:348-354`, `:454`, so odd values may produce odd output or regex/slicing edge cases. I did not run these; the implementer should check that `--tab_length=0` and `--tab_length=-1` terminate and do not raise an unexpected exception, and report what they see. If they do misbehave, a range check is a maintainer decision (Q-002), not part of this change.
- **Subprocess tests.** They depend on `sys.executable` and on the working directory containing the `markdown` package. Setting `cwd` to the repository root avoids a dependence on an installed copy. Startup cost is small but not zero.
- **`markdown_py` coverage (AC-FR-005-1).** If `markdown_py` is not on `PATH` in CI, the test is skipped. FR-005 then rests on `pyproject.toml:71`, which is a static fact rather than an executed check.
- **Documentation copy drift.** The `--help` block in `docs/cli.md` is hand-maintained. It must match the new help string, or docs and `--help` will diverge. No test checks this (ASM-003).
- **Spec readiness.** All ACs are Inferred and await maintainer confirmation on the PR (spec status). The plan implements them as written; if maintainers change Q-001 or Q-002, the tests in §4 are the places to update.

## AutoSE stage check: names the files and functions to change

Result: **PASS**

- all checks passed
