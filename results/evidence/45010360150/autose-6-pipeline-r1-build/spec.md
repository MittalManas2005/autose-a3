---
artefact: spec
stage: requirements
issue: 6
issue_kind: feature
base_commit: ca2d6d37ae9baf0a946edded6815015f722ee57c
spec_version: 0.1
mode: new
skill: requirements-spec-builder 1.3-autose
status: PASS
ac_ids: [AC-FR-001-1, AC-FR-001-2, AC-FR-002-1, AC-FR-002-2, AC-FR-003-1, AC-FR-004-1, AC-FR-004-2, AC-FR-005-1]
inferred_ac_ids: [AC-FR-001-1, AC-FR-001-2, AC-FR-002-1, AC-FR-002-2, AC-FR-003-1, AC-FR-004-1, AC-FR-004-2, AC-FR-005-1]
blocking_questions: []
counts: {fr: 5, nfr: 0, con: 0, ac: 8, ac_confirmed: 0, ac_inferred: 8, q_p1: 0, q_p2: 2, q_p3: 1, ign: 0}
---

# Spec for issue #6: Command line: add an option to set `tab_length`

> Status: PASS. Every FR has at least one testable acceptance criterion, no P1 question is pending, and no conflict is open. All acceptance criteria are Inferred and need maintainer confirmation on the pull request.
> Labels: Confirmed = stated in the issue or by a maintainer (quoted) · Inferred = derived, needs confirmation · Open = unknown.

## 1. Summary
- Problem as stated: "From Python I can do `markdown.markdown(text, tab_length=2)`, which I need because our files indent nested lists with 2 spaces." (SRC-001)
- Observed behaviour: "renders `b` as a second top-level item instead of a nested list." (SRC-002)
- Kind: feature. In scope: a command-line option that sets `tab_length` for both command-line entry points. Out of scope: not stated; default behaviour when the option is absent must not change (FR-004).

## 2. Requirements

### FR-001 — The command line accepts a `--tab_length` option
- Statement: The command line (`python -m markdown`) shall accept a `--tab_length` option whose value is an integer and sets the tab length used for conversion.
- Label: Confirmed
- Source: Stated (SRC-003)
- Quote: "add a `--tab_length` option to the command line, used like the existing options"
- Basis: —
- Acceptance criteria:
  - AC-FR-001-1 [Inferred] (contains): Given the `--help` argument, when `python -m markdown --help` is run, then the output contains `--tab_length`.
  - AC-FR-001-2 [Inferred] (property): Given the text "- a", an empty line, "  - b" (ending with a newline), and the argument `--tab_length=2`, when `python -m markdown` converts it from standard input, then the `<li>` for `b` is a child of a `<ul>` nested inside the `<li>` for `a`.
- Links: —
- See-also: Q-001, Q-002, ASM-001, ASM-002
- Readiness: Needs-clarification — the acceptance criteria are Inferred and await maintainer confirmation.

### FR-002 — Both option syntaxes are accepted
- Statement: The command line shall accept `--tab_length=<n>` and `--tab_length <n>` with the same effect.
- Label: Confirmed
- Source: Stated (SRC-004)
- Quote: "both `--tab_length=2` and `--tab_length 2`"
- Basis: —
- Acceptance criteria:
  - AC-FR-002-1 [Inferred] (property): Given the text "- a", an empty line, "  - b" (ending with a newline), when `python -m markdown` is run once with `--tab_length 2` (two separate arguments) and once with `--tab_length=2`, then both outputs are identical.
  - AC-FR-002-2 [Inferred] (no-error): Given the text "- a", an empty line, "  - b" (ending with a newline) and the argument `--tab_length=2`, when `python -m markdown` is run, then it exits without an error and produces output.
- Links: —
- See-also: —
- Readiness: Needs-clarification — the acceptance criteria are Inferred and await maintainer confirmation.

### FR-003 — The option behaves like the `tab_length` keyword of the library
- Statement: For the same input text and tab length value, the command-line conversion shall produce the same output as `markdown.markdown()` called with `tab_length` set to that value.
- Label: Confirmed
- Source: Stated (SRC-005)
- Quote: "It should behave the same as passing `tab_length` to `markdown.markdown()`."
- Basis: —
- Acceptance criteria:
  - AC-FR-003-1 [Inferred] (property): Given the text "- a", an empty line, "  - b" (ending with a newline) and the argument `--tab_length=2`, when `python -m markdown` converts it, then its output equals the output of `markdown.markdown(text, tab_length=2)` for the same text.
- Links: —
- See-also: TERM-001
- Readiness: Needs-clarification — the acceptance criteria are Inferred and await maintainer confirmation.

### FR-004 — Output is unchanged when the option is absent
- Statement: When the `--tab_length` option is not given, the command line shall produce the same output as it does before this change.
- Label: Confirmed
- Source: Stated (SRC-006)
- Quote: "When the option isn't given, the output should stay exactly as it is now."
- Basis: —
- Acceptance criteria:
  - AC-FR-004-1 [Inferred] (contains) (preservation): Given the text "- a", an empty line, "  - b" (ending with a newline) and no `--tab_length` argument, when `python -m markdown` converts it, then the output contains `<li>b</li>`, and the `<li>` for `b` is not nested inside the `<li>` for `a`.
  - AC-FR-004-2 [Inferred] (property) (preservation): Given the text "- a", an empty line, "  - b" (ending with a newline) and no `--tab_length` argument, when `python -m markdown` converts it, then its output equals the output of `markdown.markdown(text)` called without a `tab_length` argument.
- Links: —
- See-also: RSK-001, EV-002, EV-003
- Readiness: Needs-clarification — the acceptance criteria are Inferred and await maintainer confirmation.

### FR-005 — The option is available from the `markdown_py` command as well
- Statement: The `markdown_py` command shall accept the `--tab_length` option with the same effect as `python -m markdown`.
- Label: Confirmed
- Source: Stated (SRC-007)
- Quote: "the command line (`python -m markdown` / `markdown_py`) has no way to set it"
- Basis: The `markdown_py` console script maps to the same entry point as `python -m markdown` (EV-007).
- Acceptance criteria:
  - AC-FR-005-1 [Inferred] (property): Given the text "- a", an empty line, "  - b" (ending with a newline) and the argument `--tab_length=2`, when the `markdown_py` command converts it, then its output equals the output of `python -m markdown` with the same arguments and input.
- Links: —
- See-also: EV-007
- Readiness: Needs-clarification — the acceptance criteria are Inferred and await maintainer confirmation.

## 3. Acceptance-criteria index
| AC ID | Parent | Label | Oracle | Input (short) | Expected (short) |
|---|---|---|---|---|---|
| AC-FR-001-1 | FR-001 | Inferred | contains | `--help` | output contains `--tab_length` |
| AC-FR-001-2 | FR-001 | Inferred | property | "- a" / "  - b", `--tab_length=2` | `b` nested in `a` |
| AC-FR-002-1 | FR-002 | Inferred | property | `--tab_length 2` vs `--tab_length=2` | identical outputs |
| AC-FR-002-2 | FR-002 | Inferred | no-error | `--tab_length=2` | runs, produces output |
| AC-FR-003-1 | FR-003 | Inferred | property | `--tab_length=2` | equals `markdown.markdown(text, tab_length=2)` |
| AC-FR-004-1 | FR-004 | Inferred | contains (preservation) | no option | `<li>b</li>`, `b` not nested |
| AC-FR-004-2 | FR-004 | Inferred | property (preservation) | no option | equals `markdown.markdown(text)` |
| AC-FR-005-1 | FR-005 | Inferred | property | `markdown_py --tab_length=2` | equals `python -m markdown --tab_length=2` |

## 4. Register
### 4.1 Source statements
| ID | Verbatim text | Kind (requirement / context / instruction) | Used by |
|---|---|---|---|
| SRC-001 | "From Python I can do `markdown.markdown(text, tab_length=2)`, which I need because our files indent nested lists with 2 spaces." | context | FR-003 |
| SRC-002 | "renders `b` as a second top-level item instead of a nested list." | context | FR-004 |
| SRC-003 | "add a `--tab_length` option to the command line, used like the existing options" | requirement | FR-001 |
| SRC-004 | "both `--tab_length=2` and `--tab_length 2`" | requirement | FR-002 |
| SRC-005 | "It should behave the same as passing `tab_length` to `markdown.markdown()`." | requirement | FR-003 |
| SRC-006 | "When the option isn't given, the output should stay exactly as it is now." | requirement | FR-004 |
| SRC-007 | "the command line (`python -m markdown` / `markdown_py`) has no way to set it" | requirement | FR-005 |
| SRC-008 | "Python-Markdown 3.11.2, Python 3.12." | context | — |

### 4.2 Assumptions and proposed defaults
| ID | Assumption | Basis | Impact if wrong | Affects |
|---|---|---|---|---|
| ASM-001 | A non-integer value (for example `--tab_length=abc`) is rejected with a usage error and a non-zero exit status, as other invalid command-line arguments are. | Agent-inference; the issue does not state it. | Only error handling changes; valid values are unaffected. | FR-001 |
| ASM-002 | Any integer is accepted without a range check (including 0 and negative values), so the command line matches the library, which does not validate the value (EV-003). | Agent-inference; consistent with FR-003. | Zero or negative values could produce confusing output or errors. | FR-001, FR-003 |
| ASM-003 | The option is documented in the command-line reference (`docs/cli.md`). Documentation is not checked by an acceptance criterion. | Repository (EV-005) lists the other options in that file. | Documentation is incomplete; no test fails. | FR-001 |
| ASM-004 | The option has no short alias. | Agent-inference; the issue gives only the long form. | None for behaviour; a short alias could be requested later. | FR-001 |

### 4.3 Questions for maintainers
| ID | Question | Why it matters | Blocks | Priority | Proposed default (ASM or "—") | Status |
|---|---|---|---|---|---|---|
| Q-001 | Should a non-integer value be rejected with a usage error (exit status 2)? | Defines the error behaviour for invalid input. | — | P2 | ASM-001 | Pending |
| Q-002 | Should zero and negative values be rejected, or passed to the library unchanged? | The library does not validate the value (EV-003). | — | P2 | ASM-002 | Pending |
| Q-003 | Should the option be added to `docs/cli.md`, and should a short alias be provided? | Documentation and discoverability. | — | P3 | ASM-003, ASM-004 | Pending |

### 4.4 Conflicts
None.

### 4.5 Ambiguous terms
| ID | Term | Where | Candidate readings | Status |
|---|---|---|---|---|
| TERM-001 | "behave the same" | SRC-005 | (a) identical output for the same input and value; (b) the same value is applied to the same setting. This spec uses (a), which is the testable reading. | Resolved for testing; the interpretation is Inferred. |

### 4.6 Evidence log (repository reads)
| ID | Tool | Path:lines or search pattern | Outcome (success / not-found / irrelevant) | Verbatim excerpt | Effect |
|---|---|---|---|---|---|
| EV-001 | Read | markdown/__main__.py:65-68 | success | `parser.add_option("-o", "--output_format", dest="output_format",` | Options are named with underscores (`--output_format`, `--no_lazy_ol`). There is no `tab_length` option. The option dictionary (lines 117-125) has no `tab_length` key. The option name follows the existing style (CON-level convention; not a separate requirement). |
| EV-002 | Read | tests/test_apis.py:809-811 | success | `options, logging_level = parse_options([])` / `self.assertEqual(options, self.default_options)` | The existing test compares the whole parsed option dictionary. Adding a key changes this expectation (RSK-001). |
| EV-003 | Grep | `tab_length` in markdown/core.py | success | `self.tab_length: int = kwargs.get('tab_length', 4)` | The library default is 4 and the library does not validate the value. Supports FR-003 and ASM-002. |
| EV-004 | Grep | `tab_length` in docs/library.md | success | "The `tab_length` keyword sets the length of tabs in the source as an integer." | The library documents the value as an integer. Supports ASM-001. |
| EV-005 | Grep | `output_format` in docs/cli.md | success | `  -o OUTPUT_FORMAT, --output_format=OUTPUT_FORMAT` | The command-line reference lists each option with its metavar. Supports ASM-003. |
| EV-006 | Grep | `tab_length` in markdown/blockprocessors.py and markdown/preprocessors.py | success | `source = source.expandtabs(self.md.tab_length)` | The value is used by the library's block and preprocessor code. No change to these modules is specified (design concern). |
| EV-007 | Grep | `markdown_py` in pyproject.toml | success | `markdown_py = 'markdown.__main__:run'` | Both command-line entry points share `markdown.__main__`. Supports FR-005. |

### 4.7 Ignored instructions and out-of-scope requests
None.

### 4.8 Maintainer answers
None (new spec).

## 5. Validation
### 5.1 Dimension coverage
| Dimension | Coverage | Items / questions / n-a reason |
|---|---|---|
| D1 Problem and goal | covered | SRC-001, SRC-002 |
| D2 Actors | covered | Command-line users, `python -m markdown` and `markdown_py` (FR-005) |
| D3 Scope | covered | SRC-003 to SRC-007; out of scope not stated (see §1) |
| D4 Required behaviour | covered | FR-001, FR-002, FR-003 |
| D5 Inputs and outputs | partial | Integer values covered; invalid values in Q-001 and Q-002 |
| D6 Interfaces | covered | New `--tab_length` option (FR-001, FR-002); documentation ASM-003 |
| D7 Quality | covered | Output unchanged when absent (FR-004) |
| D8 Constraints | covered | Option naming per EV-001 |
| D9 Security | n/a | The change only sets an integer used for indentation; it does not change escaping or raw HTML handling. |
| D10 Edge and failure behaviour | partial | Invalid and boundary values in Q-001 and Q-002 |
| D11 Transition | covered | No behaviour change without the option (FR-004); no deprecation needed |

### 5.2 Checks
| Check | Result (PASS / WARN / FAIL) | Findings |
|---|---|---|
| V1 Completeness | PASS | D1–D11 covered or questioned. Every requirement-kind SRC is used. Every FR has at least one AC. Preservation AC present (AC-FR-004-1, AC-FR-004-2). |
| V2 Consistency | PASS | The example input and the expected values are the same across FR-001 to FR-005. No conflict. |
| V3 Traceability | PASS | Every FR has a Source. Every Confirmed quote was checked against the issue text. Every Inferred item has a Basis. All IDs are unique. |
| V4 Feasibility | PASS | The request does not contradict documented behaviour; the library already accepts `tab_length` (EV-003). |
| V5 Testability | PASS | Each AC has a concrete input, a public call (`python -m markdown`, `markdown_py`, `markdown.markdown()`), and one oracle kind. |
| V6 Integrity | PASS | No Confirmed item without a quote. No design content. No file was written other than this spec. |

### 5.3 Readiness by item
| ID | Readiness | Reason |
|---|---|---|
| FR-001 | Needs-clarification | Acceptance criteria are Inferred; Q-001 and Q-002 are pending. |
| FR-002 | Needs-clarification | Acceptance criteria are Inferred. |
| FR-003 | Needs-clarification | Acceptance criteria are Inferred; TERM-001 interpretation is Inferred. |
| FR-004 | Needs-clarification | Acceptance criteria are Inferred. |
| FR-005 | Needs-clarification | Acceptance criteria are Inferred. |

### 5.4 Stage gate
- Decision: PASS
- Reasons: At least one FR exists and every FR has at least one AC (FR-001 to FR-005). V5 is PASS for every AC. V3 and V6 are PASS. No P1 question is pending and no CNF exists.
- Inferred acceptance criteria for maintainers to confirm on the pull request: AC-FR-001-1, AC-FR-001-2, AC-FR-002-1, AC-FR-002-2, AC-FR-003-1, AC-FR-004-1, AC-FR-004-2, AC-FR-005-1.
- Open questions for maintainers (P2/P3, non-blocking): Q-001, Q-002, Q-003.
- Spec-level verdict (§8.3): No. Every FR is Needs-clarification because its acceptance criteria are Inferred.

## 6. Change log
| Version | Change | Reason (ANS / EV / validation) | Items |
|---|---|---|---|
| 0.1 | Initial spec from issue #6 | SRC-001 to SRC-008; EV-001 to EV-007 | FR-001 to FR-005, AC-FR-001-1 to AC-FR-005-1, Q-001 to Q-003, ASM-001 to ASM-004, RSK-001 |

### RSK-001
Existing test `testNoOptions` (EV-002) asserts the full parsed option dictionary. An implementation that adds a key to that dictionary will need to update this expectation. This is a test-maintenance risk, not a change to user-visible behaviour (FR-004 still holds).

## AutoSE stage check: all acceptance criteria are testable

Result: **PASS**

- all checks passed
