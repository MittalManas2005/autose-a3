---
artefact: design
issue: 6
files:
  - path: markdown/__main__.py
    change: modify
    symbols: [parse_options]
    new_symbols: []
  - path: docs/changelog.md
    change: modify
    symbols: []
    new_symbols: []
  - path: docs/cli.md
    change: modify
    symbols: []
    new_symbols: []
  - path: tests/test_apis.py
    change: modify
    symbols: [TestCliOptionParsing]
    new_symbols: [TestCliOptionParsing.testTabLengthEqualsForm, TestCliOptionParsing.testTabLengthSpaceForm, TestCliOptionParsing.testTabLengthAbsentNotPassed, TestCliOptionParsing.testTabLengthInvalidValue, TestCliOptionParsing.testTabLengthOutputMatchesLibrary]
tests: tests/test_apis.py
---

## Plan

### 1. `markdown/__main__.py`: `parse_options` (satisfies FR-001, FR-004, FR-005, FR-002, FR-003)

a) Define the option with `optparse`, next to the existing `-n/--no_lazy_ol` option (before `-x`):

```python
parser.add_option("--tab_length", dest="tab_length", type="int", default=None,
                  metavar="TAB_LENGTH",
                  help="Number of spaces per tab in the source. Defaults to 4.")
```

- `optparse` accepts both `--tab_length=2` and `--tab_length 2` for a long option with a separate value, so FR-001 needs no extra code (AC-FR-001-1, AC-FR-001-2).
- `type="int"` makes `optparse` reject `abc` itself. It exits with status 2 and prints a message of the form `option --tab_length: invalid integer value: 'abc'`, which names `--tab_length` (AC-FR-005-1, ASM-001). No custom validation is written.
- `optparse` generates the `--help` line from the definition, so FR-004 (AC-FR-004-1) holds without a separate help edit.
- `default=None` is used so the parser can tell "not given" from any integer.

b) Add the key to the mapping only when the option was given. This goes after the existing `opts = {...}` literal (`__main__.py:117-125`):

```python
if options.tab_length is not None:
    opts['tab_length'] = options.tab_length
```

- When the option is absent, the mapping is unchanged, so the existing test `testNoOptions` (`tests/test_apis.py:809-812`), which compares the whole mapping exactly, keeps passing with no edit (RSK-001). This also satisfies FR-003 and NFR-001 (AC-FR-003-1, AC-NFR-001-1).
- Always adding `'tab_length': None` would be wrong: `Markdown.__init__` reads `kwargs.get('tab_length', 4)` (`markdown/core.py:110`), and a present key with value `None` would return `None` and not the default 4.
- With the option given, `markdownFromFile(**options)` (`__main__.py:148`) forwards the key to `Markdown(**kwargs)` (`markdown/core.py:535`), which sets `self.tab_length` (`core.py:110`). That gives the same output as `markdown.markdown(text, tab_length=N)` (FR-002, AC-FR-002-1, AC-FR-002-2, AC-FR-002-3). The nesting in AC-FR-002-3 comes from the existing list parser, which the tests will check; this design does not change it.
- Values 0 and negative numbers are passed to the library unchanged (ASM-002, Q-002 pending). No range check is added.

### 2. `docs/changelog.md` (satisfies the changelog rule, K5)

Under `## [Unreleased]` (line 15), add a new `### Added` heading above the existing `### Fixed` heading (line 17):

```markdown
### Added

* Add a `--tab_length` option to the command line to set the length of tabs in the
  source, as the `tab_length` keyword of `markdown.markdown()` does.
```

### 3. `docs/cli.md` (documentation of the new option)

In the sample `--help` block (lines 45–67), add the lines for the new option, copied from the actual output of `python -m markdown --help` after the change. Do not change the existing lines. The block already omits `-n/--no_lazy_ol` (RSK-002); that is out of scope and is left as it is.

### 4. `tests/test_apis.py`: `TestCliOptionParsing` (acceptance tests)

Add methods to the existing class (`tests/test_apis.py:790`), using the same style (`parse_options([...])`, `assertEqual`):

- `testTabLengthEqualsForm`: `parse_options(['--tab_length=2'])` gives `options['tab_length'] == 2`. (AC-FR-001-1 at the parser level.)
- `testTabLengthSpaceForm`: `parse_options(['--tab_length', '2'])` gives the same result. (AC-FR-001-2.)
- `testTabLengthAbsentNotPassed`: `parse_options([])` has no `tab_length` key. The existing `testNoOptions` covers the same thing; this test makes the intent explicit. (AC-FR-003-1.)
- `testTabLengthInvalidValue`: `parse_options(['--tab_length', 'abc'])` raises `SystemExit` with code 2, and the stderr text (captured with `contextlib.redirect_stderr(StringIO())`) contains `--tab_length`. (AC-FR-005-1.)
- `testTabLengthOutputMatchesLibrary`: take `options` from `parse_options(['--tab_length=2'])`, run `markdown.markdownFromFile(input=StringIO(text), output=out, **options)` with `text = "- a\n\n  - b\n"`, and assert that `out.getvalue()` equals `markdown.markdown(text, tab_length=2)`. Assert also that the `li` whose text is `b` is nested inside the `li` whose text is `a`. (AC-FR-002-1, AC-FR-002-2 at the path that `python -m markdown` uses, AC-FR-002-3.) The CLI's default output format is `xhtml`, the same as the library's, so no format argument is needed.

Note: `run()` in `__main__.py` is marked `pragma: no cover` and reads `sys.argv`/`sys.stdin`. The tests use `parse_options` plus `markdownFromFile`, which is the same path `run()` takes. The help-text check (AC-FR-004-1) can be a test that `parse_options(['--help'])` exits with code 0 and that the captured stdout contains `--tab_length`, or it can be checked with `python -m markdown --help` in the verification step.

## Constraints respected

- **K1 (stage interfaces):** no preprocessor, block, tree or postprocessor signature is touched.
- **K2 (registries and priorities):** no registry, processor name or priority is added or changed.
- **K3 (attribute values):** `tab_length` is an `int` used as a configuration value; no element attribute is written.
- **K4 (stash and placeholders):** not touched.
- **K5 (backward compatibility):** existing options, the `markdown`, `Markdown` and `markdownFromFile` APIs, and the `parse_options` return shape for invocations without `--tab_length` are unchanged. No dependency is added. The Python version is unchanged.
- **Changelog rule:** `markdown/__main__.py` is under `markdown/`, so a `docs/changelog.md` entry under `[Unreleased]` is added (plan item 2).
- **Development conventions:** tests use `unittest` and go in `tests/` (`tests/test_apis.py`), run with `python -m unittest discover tests`. The new code must pass flake8 with a maximum line length of 119.

## ARCHITECTURE.md vs source

Claims checked in this run (I read the source; I could not run commands, so the claims were checked by reading, not by execution):

| Claim | Source | Result |
|---|---|---|
| CLI is in `markdown/__main__.py` and is part of C1 | `markdown/__main__.py:45` (`parse_options`), `:148` (`markdownFromFile(**options)`) | Verified |
| CLI uses `optparse` | `markdown/__main__.py:23`, `:59` (`optparse.OptionParser`) | Verified (matches spec EV-002 / EV-004) |
| Options are parsed into a mapping that goes to `markdownFromFile` | `markdown/__main__.py:117-127`, `:148` | Verified |
| `Markdown` reads `tab_length` from kwargs with default 4 | `markdown/core.py:110` | Verified |
| `markdown()` forwards kwargs to `Markdown` | `markdown/core.py:484-509`, call at `:508` | Verified |
| `markdownFromFile()` forwards kwargs to `Markdown` | `markdown/core.py:512-538`, call at `:535` | Verified |
| Changelog has an `[Unreleased]` section with a `### Fixed` subsection | `docs/changelog.md:15`, `:17` | Verified |
| Existing test compares the full parsed CLI mapping exactly, for no options | `tests/test_apis.py:794-812` (`testNoOptions`, `assertEqual(options, self.default_options)`) | Verified |
| `docs/cli.md` help block omits `-n/--no_lazy_ol` | `docs/cli.md:45-67` | Verified (spec EV-005, RSK-002) |

**Discrepancies:**

1. **Commit pin.** `ARCHITECTURE.md` says the pinned commit is `3f2c5510…` (`git describe` `3.11.2-10-g3f2c551`). The spec's `base_commit` is `758ab062…`, and the git status shows HEAD at `758ab06`. I could not run `git` to confirm which commit the checkout is at (design is a read-only role, and Bash is not available to me). The plan relies only on the source lines above, which are the code at this checkout. The mismatch should be checked before implementation.
2. No other discrepancies were found among the claims above.

Not checked in this run, and not relied on by the plan: the priorities in C2–C6, the ADRs, K5's file references (`__init__.py:42-48`, `pyproject.toml`), and the contributing-guide references for the changelog rule (`docs/contributing.md:535-547`).

## Risks

- **R1, `None` in the mapping (RSK-001):** handled by the conditional key (plan item 1b). The test `testNoOptions` must not be edited.
- **R2, invalid value message:** the requirement that the error names `--tab_length` depends on the `optparse` message text for `type="int"`. This is expected from the `optparse` implementation, but it has not been run here. The tester should confirm it.
- **R3, zero and negative values (Q-002 open):** they are passed to the library unchanged, which is what ASM-002 says. I did not check how the library renders with `tab_length` of 0 or a negative number. If Q-002 is answered "reject", the change is a range check in `parse_options` after the parser runs, and the tests must be updated.
- **R4, nesting depends on the library:** AC-FR-002-3 depends on the existing list parser treating two-space indentation as nested when `tab_length=2`. The test will show whether this holds.
- **R5, stale docs sample:** the `docs/cli.md` help block is already out of date (RSK-002). Only the new option's lines are added.
- **R6, commit mismatch:** see the discrepancy above.

## AutoSE stage check: names the files and functions to change

Result: **PASS**

- all checks passed
