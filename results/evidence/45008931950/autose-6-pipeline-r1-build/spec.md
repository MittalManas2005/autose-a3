---
artefact: spec
stage: requirements
issue: 6
issue_kind: feature
base_commit: 758ab062032e4096fc14a4bb219015e83820c890
spec_version: 0.1
mode: new
skill: requirements-spec-builder 1.3-autose
status: PASS
ac_ids: [AC-FR-001-1, AC-FR-001-2, AC-FR-002-1, AC-FR-002-2, AC-FR-002-3, AC-FR-003-1, AC-FR-004-1, AC-FR-005-1, AC-NFR-001-1]
inferred_ac_ids: [AC-FR-001-1, AC-FR-001-2, AC-FR-002-1, AC-FR-002-2, AC-FR-002-3, AC-FR-003-1, AC-FR-004-1, AC-FR-005-1, AC-NFR-001-1]
blocking_questions: []
counts: {fr: 5, nfr: 1, con: 0, ac: 9, ac_confirmed: 0, ac_inferred: 9, q_p1: 0, q_p2: 2, q_p3: 0, ign: 0}
---

# Spec for issue #6: Command line: add an option to set `tab_length`

> Status: PASS. All acceptance criteria are testable through the command line or the library API; the only open points (invalid and out-of-range values) have proposed defaults that do not block work.
> Labels: Confirmed = stated in the issue or by a maintainer (quoted) · Inferred = derived, needs confirmation · Open = unknown.

## 1. Summary
- Problem as stated: "the command line (`python -m markdown` / `markdown_py`) has no way to set it, so the same files render differently in our build script" (SRC-002)
- Kind: feature. In scope: a `--tab_length` command-line option that sets the same `tab_length` value as the library keyword of the same name (SRC-005, SRC-006). Out of scope: any other option; a short flag is not requested (the issue names only the long form).
- Preservation: when the option is not given, output is unchanged (SRC-007).

## 2. Requirements

### FR-001 — Accept the `--tab_length` option
- Statement: The command-line interface shall accept a `--tab_length` option, given either as `--tab_length=N` or as `--tab_length N`.
- Label: Confirmed
- Source: Stated (SRC-005)
- Quote: "add a `--tab_length` option to the command line, used like the existing options (both `--tab_length=2` and `--tab_length 2`)"
- Basis: —
- Acceptance criteria:
  - AC-FR-001-1 [Inferred] (no-error): Given stdin text made of the lines `- a`, an empty line and `  - b`, when run as `python -m markdown --tab_length=2`, then the command exits with status 0 and writes HTML to stdout.
  - AC-FR-001-2 [Inferred] (no-error): Given the same stdin text, when run as `python -m markdown --tab_length 2`, then the command exits with status 0 and writes HTML to stdout.
- Links: —
- See-also: SRC-005, EV-004 (the CLI uses `optparse`-style long options with underscores, e.g. `--output_format`), EV-006, ASM-001
- Readiness: Needs-clarification — the ACs are `[Inferred]` (constructed examples) and need confirmation on the pull request.

### FR-002 — Same effect as the library `tab_length` keyword
- Statement: When `--tab_length=N` is given, the command-line conversion shall produce the same output as `markdown.markdown(text, tab_length=N)` for the same input text.
- Label: Confirmed
- Source: Stated (SRC-006)
- Quote: "It should behave the same as passing `tab_length` to `markdown.markdown()`."
- Basis: —
- Acceptance criteria:
  - AC-FR-002-1 [Inferred] (property): Given the input text `- a`, an empty line, `  - b`, when run as `python -m markdown --tab_length=2`, then the standard output equals the string returned by `markdown.markdown("- a\n\n  - b\n", tab_length=2)`.
  - AC-FR-002-2 [Inferred] (property): Given the same input text, when run as `python -m markdown --tab_length 2`, then the standard output equals the string returned by `markdown.markdown("- a\n\n  - b\n", tab_length=2)`.
  - AC-FR-002-3 [Inferred] (property): Given the same input text, when run as `python -m markdown --tab_length=2`, then the `li` element whose text is `b` is a descendant of the `li` element whose text is `a` (nested list, as the issue reports for the library).
- Links: TERM-001
- See-also: SRC-001, SRC-003, SRC-004, EV-010, EV-012
- Readiness: Needs-clarification — the ACs are `[Inferred]` and the reading of "behave the same" (TERM-001) needs confirmation.

### FR-003 — Output unchanged when the option is absent
- Statement: When `--tab_length` is not given, the command-line conversion shall produce the same output as it did before this change.
- Label: Confirmed
- Source: Stated (SRC-007)
- Quote: "When the option isn't given, the output should stay exactly as it is now."
- Basis: —
- Acceptance criteria:
  - AC-FR-003-1 [Inferred] (property) (preservation): Given the input text `- a`, an empty line, `  - b`, when run as `python -m markdown` with no `--tab_length` option, then the standard output equals the string returned by `markdown.markdown("- a\n\n  - b\n")` with no `tab_length` keyword, and the `li` element whose text is `b` is not a descendant of the `li` element whose text is `a`.
- Links: —
- See-also: SRC-004, EV-010 (library default of 4)
- Readiness: Needs-clarification — the AC is `[Inferred]`.

### FR-004 — Option listed in `--help`
- Statement: The command-line help output shall list the `--tab_length` option.
- Label: Inferred
- Source: Repository (EV-004, EV-005, EV-006)
- Quote: —
- Basis: The request says the option is "used like the existing options" (SRC-005), and every existing option appears in the `--help` output. Not stated explicitly; confirm on the pull request.
- Acceptance criteria:
  - AC-FR-004-1 [Inferred] (contains): Given no input, when run as `python -m markdown --help`, then the output contains `--tab_length`.
- Links: —
- See-also: RSK-002
- Readiness: Needs-clarification — derived requirement, `[Inferred]` AC.

### FR-005 — Non-integer values are rejected
- Statement: When `--tab_length` is given a value that is not an integer, the command-line interface shall exit with a usage error that names `--tab_length`.
- Label: Inferred
- Source: Agent-inference (proposed default ASM-001)
- Quote: —
- Basis: The library documents `tab_length` as an integer (EV-003, EV-007). The behaviour for invalid input is not stated in the issue. Confirm via Q-001.
- Acceptance criteria:
  - AC-FR-005-1 [Inferred] (contains): Given no input and the option value `abc`, when run as `python -m markdown --tab_length abc`, then the exit status is non-zero and the error output contains `--tab_length`.
- Links: Q-001
- See-also: ASM-001
- Readiness: Needs-clarification — depends on Q-001 (non-blocking, proposed default in place).

### NFR-001 — Compatibility: Existing command-line behaviour preserved
- Statement: The existing command-line options shall keep their current behaviour and output.
- Label: Inferred
- Source: Repository (EV-006, EV-009, EV-011)
- Quote: —
- Basis: The CLI options are parsed into a mapping that existing tests compare exactly (EV-011), and the request requires unchanged output without the option (SRC-007). Category: Compatibility (backward compatibility of the CLI and existing output).
- Acceptance criteria:
  - AC-NFR-001-1 [Inferred] (property) (preservation): Given the input text `- a`, an empty line, `  - b`, when run as `python -m markdown -o html`, then the standard output equals the string returned by `markdown.markdown("- a\n\n  - b\n", output_format='html')`.
- Links: RSK-001
- See-also: FR-003
- Readiness: Needs-clarification — the AC is `[Inferred]`.

## 3. Acceptance-criteria index
| AC ID | Parent | Label | Oracle | Input (short) | Expected (short) |
|---|---|---|---|---|---|
| AC-FR-001-1 | FR-001 | Inferred | no-error | `- a` / blank / `  - b`; `--tab_length=2` | exit 0, HTML written |
| AC-FR-001-2 | FR-001 | Inferred | no-error | same; `--tab_length 2` | exit 0, HTML written |
| AC-FR-002-1 | FR-002 | Inferred | property | same; `--tab_length=2` | equals `markdown.markdown(..., tab_length=2)` |
| AC-FR-002-2 | FR-002 | Inferred | property | same; `--tab_length 2` | equals `markdown.markdown(..., tab_length=2)` |
| AC-FR-002-3 | FR-002 | Inferred | property | same; `--tab_length=2` | `b` item nested in `a` item |
| AC-FR-003-1 | FR-003 | Inferred | property (preservation) | same; no option | equals library default output; `b` not nested |
| AC-FR-004-1 | FR-004 | Inferred | contains | `--help` | contains `--tab_length` |
| AC-FR-005-1 | FR-005 | Inferred | contains | `--tab_length abc` | non-zero exit; error names `--tab_length` |
| AC-NFR-001-1 | NFR-001 | Inferred | property (preservation) | `-o html`, same text | equals `markdown.markdown(..., output_format='html')` |

## 4. Register
### 4.1 Source statements
| ID | Verbatim text | Kind (requirement / context / instruction) | Used by |
|---|---|---|---|
| SRC-001 | From Python I can do `markdown.markdown(text, tab_length=2)`, which I need because our files indent nested lists with 2 spaces. | context | FR-002 |
| SRC-002 | But the command line (`python -m markdown` / `markdown_py`) has no way to set it, so the same files render differently in our build script: | context (problem) | Summary |
| SRC-003 | printf -- '- a\n\n  - b\n' \| python -m markdown | context (reproduction, code block) | FR-002 |
| SRC-004 | renders `b` as a second top-level item instead of a nested list. | context (problem) | FR-003 |
| SRC-005 | **Request:** add a `--tab_length` option to the command line, used like the existing options (both `--tab_length=2` and `--tab_length 2`). | requirement | FR-001 |
| SRC-006 | It should behave the same as passing `tab_length` to `markdown.markdown()`. | requirement | FR-002 |
| SRC-007 | When the option isn't given, the output should stay exactly as it is now. | requirement | FR-003, NFR-001 |
| SRC-008 | Python-Markdown 3.11.2, Python 3.12. | context | — |

### 4.2 Assumptions and proposed defaults
| ID | Assumption | Basis | Impact if wrong | Affects |
|---|---|---|---|---|
| ASM-001 | A non-integer `--tab_length` value is rejected by the command-line parser with a usage error (non-zero exit). | EV-003 (documented as "an integer"), EV-004 (option parser in use) | Invalid input would be handled differently; easy to change in review | FR-005, AC-FR-005-1 |
| ASM-002 | Integer values, including zero and negative values, are passed to the library unchanged; the command line adds no range check. | EV-010 (library reads the keyword with no validation shown), EV-012 (options are forwarded to the library) | Out-of-range values would be handled by the library's behaviour rather than rejected up front | FR-002, Q-002 |

### 4.3 Questions for maintainers
| ID | Question | Why it matters | Blocks | Priority | Proposed default (ASM or "—") | Status |
|---|---|---|---|---|---|---|
| Q-001 | Should a `--tab_length` value that is not an integer (for example `abc`) be rejected with a command-line usage error? (yes / no) | Defines error behaviour for invalid input | — | P2 | ASM-001 (yes) | Pending |
| Q-002 | Should zero or negative `--tab_length` values be passed to the library unchanged, or rejected by the command line? (unchanged / reject) | Defines behaviour for out-of-range integers | — | P2 | ASM-002 (unchanged) | Pending |

### 4.4 Conflicts
None.

### 4.5 Ambiguous terms
| ID | Term | Where | Candidate readings | Status |
|---|---|---|---|---|
| TERM-001 | "behave the same" | SRC-006 | (a) identical output for identical input and value; (b) the option merely accepts the same values | Reading (a) used in AC-FR-002-1/2; maintainers confirm on the pull request |

### 4.6 Evidence log (repository reads)
Budget: 12 of 12 used.

| ID | Tool | Path:lines or search pattern | Outcome (success / not-found / irrelevant) | Verbatim excerpt | Effect |
|---|---|---|---|---|---|
| EV-001 | Grep | `markdown/__main__.py`, `tab_length\|tab-length` | not-found | — | Confirms the CLI has no `tab_length` option today (SRC-002) |
| EV-002 | Grep | `markdown/__main__.py`, `add_argument\(` | not-found | — | The CLI does not use `argparse`; ACs unaffected |
| EV-003 | Grep | `docs/`, `tab_length` | success | "The `tab_length` keyword sets the length of tabs in the source as an integer." (docs/library.md:208) | Integer type documented; supports ASM-001 |
| EV-004 | Grep | `markdown/*.py`, `def run\|add_argument\|parse_options\|--extension\|-x` | success | `parser.add_option("-x", "--extension", action="append", dest="extensions",` (markdown/__main__.py:71) | Options are defined with `optparse`; long names use underscores (FR-001, FR-004) |
| EV-005 | Read | `docs/cli.md`, lines 37–67 (`--help` block) | success | `  -o OUTPUT_FORMAT, --output_format=OUTPUT_FORMAT` | Help lists the existing options (FR-004); the block omits `-n`/`--no_lazy_ol`, so it is out of date (RSK-002) |
| EV-006 | Read | `markdown/__main__.py`, lines 1–155 | success | `    parser.add_option("-n", "--no_lazy_ol", dest="lazy_ol",` | Options parsed into a mapping passed to `markdownFromFile`; no `tab_length` key today |
| EV-007 | Read | `docs/library.md`, lines 204–215 | success | "The default value is `4`." | Library default is 4 (supports FR-003 comparison) |
| EV-008 | Grep | `markdown/__init__.py`, `def markdownFromFile\|def markdown\(\|def __init__` | not-found | — | Functions live elsewhere (see EV-010) |
| EV-009 | Grep | `tests/`, `parse_options\|no_lazy_ol\|output_format=\|extension_configs` | success | `        options, logging_level = parse_options([])` (tests/test_apis.py:810) | CLI parsing is tested through `parse_options` (RSK-001) |
| EV-010 | Grep | `markdown/core.py`, `def markdownFromFile\|def markdown\(\|tab_length\|def __init__` | success | `        self.tab_length: int = kwargs.get('tab_length', 4)` (markdown/core.py:110) | Library reads `tab_length` as a keyword, default 4 (FR-002, ASM-002) |
| EV-011 | Read | `tests/test_apis.py`, lines 790–811 | success | `        self.assertEqual(options, self.default_options)` | An existing test compares the full parsed mapping exactly (RSK-001; NFR-001) |
| EV-012 | Read | `markdown/core.py`, lines 512–538 | success | `    md = Markdown(**kwargs)` | `markdownFromFile` forwards its keyword arguments to `Markdown` (supports ASM-002) |

### 4.7 Ignored instructions and out-of-scope requests
None. The issue text contains no embedded instructions.

### 4.8 Maintainer answers
None (new spec).

### 4.9 Risks
| ID | Risk | Affects | Mitigation for Design |
|---|---|---|---|
| RSK-001 | An existing test (EV-011) asserts the exact parsed-options mapping for an invocation with no options. Any new key in that mapping changes the test's expectation. | FR-003, NFR-001 | Design decides how the option's absence is represented; the expectation in that test is not changed by this spec |
| RSK-002 | The `--help` sample in `docs/cli.md` is already out of date (it omits `-n`/`--no_lazy_ol`, EV-005/EV-006). | FR-004 | Not part of this request; noted only |

## 5. Validation
### 5.1 Dimension coverage
| Dimension | Coverage | Items / questions / n-a reason |
|---|---|---|
| D1 Problem and goal | covered | SRC-001, SRC-002, SRC-004 → Summary |
| D2 Actors | covered | CLI user (`python -m markdown`, `markdown_py`) — SRC-002 |
| D3 Scope | covered | Summary: only `--tab_length`; short flag not requested |
| D4 Required behaviour | covered | FR-001, FR-002 |
| D5 Inputs and outputs | covered | FR-001 (forms), AC inputs in §2–3 |
| D6 Interfaces | covered | New CLI option; library keyword unchanged (FR-002) |
| D7 Quality | covered | NFR-001 (compatibility); performance not stated → n/a |
| D8 Constraints | covered | Option spelling follows existing underscore names (EV-004) |
| D9 Security | n/a | The option only sets a numeric tab width; it does not touch escaping, raw HTML or URLs |
| D10 Edge and failure behaviour | partial | FR-005, ASM-001, ASM-002, Q-001, Q-002 |
| D11 Transition | n/a | Adds an option; no existing behaviour is removed or deprecated; no changelog rule found in evidence reads that I checked |

### 5.2 Checks
| Check | Result (PASS / WARN / FAIL) | Findings |
|---|---|---|
| V1 Completeness | PASS | Every FR/NFR has ≥1 AC; behaviour-changing FR-001/FR-002 have the preservation ACs AC-FR-003-1 and AC-NFR-001-1; D1–D11 covered or n/a with reason. |
| V2 Consistency | PASS | No conflicting items. Values match quotes (`--tab_length=2`, `--tab_length 2`, `tab_length`). |
| V3 Traceability | PASS | Each Confirmed item quotes SRC-005/006/007 exactly. Inferred items have Basis or Source. Repository sources cite EV rows with success or not-found. IDs unique. |
| V4 Feasibility | PASS | No request contradicts documented behaviour. WARN (non-blocking): `docs/cli.md` help block is already out of date (RSK-002). |
| V5 Testability | PASS | Every AC names an input, a public command or API call, and one oracle kind. No unmeasurable qualifier remains; "behave the same" is defined by TERM-001 as identical output. |
| V6 Integrity | PASS | No Confirmed item without a quote. No design or internal function names. No instructions in the issue to ignore. Every evidence read logged (12 of 12). Only `.autose_out/spec.md` written. |

### 5.3 Readiness by item
| ID | Readiness | Reason |
|---|---|---|
| FR-001 | Needs-clarification | ACs `[Inferred]`; confirm the constructed examples on the PR |
| FR-002 | Needs-clarification | ACs `[Inferred]`; TERM-001 reading to confirm |
| FR-003 | Needs-clarification | AC `[Inferred]` (preservation) |
| FR-004 | Needs-clarification | Derived requirement, `[Inferred]` |
| FR-005 | Needs-clarification | Depends on Q-001 (default ASM-001 in place) |
| NFR-001 | Needs-clarification | AC `[Inferred]` |

Spec-level verdict: Partially (no item is Ready because every AC is `[Inferred]`). Informational only.

### 5.4 Stage gate
- Decision: PASS
- Reasons: ≥1 FR exists and every FR/NFR has ≥1 AC (condition 1). V5 is PASS for every AC (condition 2). V3 and V6 are PASS (condition 3). No P1 question and no CNF exists (condition 4).
- Inferred acceptance criteria for maintainers to confirm on the pull request: AC-FR-001-1, AC-FR-001-2, AC-FR-002-1, AC-FR-002-2, AC-FR-002-3, AC-FR-003-1, AC-FR-004-1, AC-FR-005-1, AC-NFR-001-1.
- Open P2 questions (non-blocking): Q-001, Q-002.

## 6. Change log
| Version | Change | Reason (ANS / EV / validation) | Items |
|---|---|---|---|
| 0.1 | Initial spec from issue #6 | New run; EV-001–EV-012 | All |

## AutoSE stage check: all acceptance criteria are testable

Result: **PASS**

- all checks passed
