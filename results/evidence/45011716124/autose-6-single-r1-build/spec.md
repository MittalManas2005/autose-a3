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
ac_ids: [AC-FR-001-1, AC-FR-001-2, AC-FR-002-1, AC-FR-003-1, AC-FR-003-2]
inferred_ac_ids: [AC-FR-002-1, AC-FR-003-2]
blocking_questions: []
counts: {fr: 3, nfr: 0, con: 0, ac: 5, ac_confirmed: 3, ac_inferred: 2, q_p1: 0, q_p2: 1, q_p3: 0, ign: 0}
---

# Spec for issue #6: Command line: add an option to set `tab_length`

> Status: PASS. Every requirement has testable acceptance criteria through the command-line interface or the public API; the two `[Inferred]` criteria are flagged for confirmation.
> Labels: Confirmed = stated in the issue or by a maintainer (quoted) · Inferred = derived, needs confirmation · Open = unknown.

## 1. Summary
- Problem as stated: "From Python I can do `markdown.markdown(text, tab_length=2)`, which I need because our files indent nested lists with 2 spaces. But the command line (`python -m markdown` / `markdown_py`) has no way to set it" (SRC-001)
- Kind: feature. In scope: a `--tab_length` command-line option with the same effect as the `tab_length` keyword of `markdown.markdown()`. Out of scope: any other command-line option or any change to the library's default tab length (not stated in the issue; see ASM-001).

## 2. Requirements
### FR-001 — Command-line option `--tab_length` is accepted
- Statement: The command line shall accept a `--tab_length` option that takes an integer value, in both the `--tab_length=2` and the `--tab_length 2` forms.
- Label: Confirmed
- Source: Stated (SRC-002)
- Quote: "add a `--tab_length` option to the command line, used like the existing options (both `--tab_length=2` and `--tab_length 2`)"
- Basis: —
- Acceptance criteria:
  - AC-FR-001-1 [Confirmed] (property): Given the command-line arguments `["--tab_length=2"]`, when `markdown.__main__.parse_options` is called, then the returned options dictionary contains `"tab_length"` with the value `2`.
  - AC-FR-001-2 [Confirmed] (property): Given the command-line arguments `["--tab_length", "2"]`, when `markdown.__main__.parse_options` is called, then the returned options dictionary contains `"tab_length"` with the value `2`.
- Links: —
- See-also: ASM-001, Q-001, EV-001, EV-003
- Readiness: Ready — all criteria Confirmed and testable; the non-integer case is covered by ASM-001.

### FR-002 — The option behaves like the `tab_length` keyword
- Statement: When `--tab_length=N` is given, the command line shall convert the input with the same result as `markdown.markdown(text, tab_length=N)`.
- Label: Confirmed
- Source: Stated (SRC-003)
- Quote: "It should behave the same as passing `tab_length` to `markdown.markdown()`."
- Basis: —
- Acceptance criteria:
  - AC-FR-002-1 [Inferred] (property): Given the input `- a` followed by a blank line and `  - b`, with the command-line arguments `["--tab_length=2"]` and the input supplied on standard input, when the command line is run, then its output equals `markdown.markdown("- a\n\n  - b\n", tab_length=2)`. Basis: the issue's example is `printf -- '- a\n\n  - b\n'`; the expected form is derived from the stated equivalence (SRC-003), not from a stated output string.
- Links: —
- See-also: EV-001, EV-002
- Readiness: Needs-clarification — the AC is `[Inferred]` (constructed example), so the requirement is not Ready until a maintainer confirms the example.

### FR-003 — Output is unchanged when the option is not given
- Statement: When `--tab_length` is not given, the command line shall produce the same options and the same output as before this change.
- Label: Confirmed
- Source: Stated (SRC-004)
- Quote: "When the option isn't given, the output should stay exactly as it is now."
- Basis: —
- Acceptance criteria:
  - AC-FR-003-1 [Confirmed] (property) (preservation): Given the command-line arguments `[]`, when `markdown.__main__.parse_options` is called, then the returned options dictionary equals the dictionary asserted by the existing test `TestCliOptionParsing.testNoOptions` (no `"tab_length"` key).
  - AC-FR-003-2 [Inferred] (property) (preservation): Given the input `- a` followed by a blank line and `  - b`, with no `--tab_length` option, when the command line is run, then its output equals `markdown.markdown("- a\n\n  - b\n")` with default settings. Basis: the default `tab_length` is 4 (`markdown/core.py:110`, EV-002); the equality is derived from "stay exactly as it is now".
- Links: —
- See-also: EV-002, EV-003
- Readiness: Needs-clarification — AC-FR-003-2 is `[Inferred]`.

## 3. Acceptance-criteria index
| AC ID | Parent | Label | Oracle | Input (short) | Expected (short) |
|---|---|---|---|---|---|
| AC-FR-001-1 | FR-001 | Confirmed | property | `["--tab_length=2"]` to `parse_options` | options contain `tab_length == 2` |
| AC-FR-001-2 | FR-001 | Confirmed | property | `["--tab_length", "2"]` to `parse_options` | options contain `tab_length == 2` |
| AC-FR-002-1 | FR-002 | Inferred | property | list example, `--tab_length=2`, via CLI | equals `markdown.markdown(..., tab_length=2)` |
| AC-FR-003-1 | FR-003 | Confirmed | property (preservation) | `[]` to `parse_options` | equals `testNoOptions` dictionary |
| AC-FR-003-2 | FR-003 | Inferred | property (preservation) | list example, no option, via CLI | equals default `markdown.markdown(...)` |

## 4. Register
### 4.1 Source statements
| ID | Verbatim text | Kind | Used by |
|---|---|---|---|
| SRC-001 | "From Python I can do `markdown.markdown(text, tab_length=2)`, which I need because our files indent nested lists with 2 spaces." | context | Summary |
| SRC-002 | "add a `--tab_length` option to the command line, used like the existing options (both `--tab_length=2` and `--tab_length 2`)" | requirement | FR-001 |
| SRC-003 | "It should behave the same as passing `tab_length` to `markdown.markdown()`." | requirement | FR-002 |
| SRC-004 | "When the option isn't given, the output should stay exactly as it is now." | requirement | FR-003 |
| SRC-005 | "renders `b` as a second top-level item instead of a nested list." | context | AC-FR-002-1 (motivation) |

### 4.2 Assumptions and proposed defaults
| ID | Assumption | Basis | Impact if wrong | Affects |
|---|---|---|---|---|
| ASM-001 | The value is an integer, parsed the same way as the other integer-valued options; a non-integer value is rejected by the option parser and does not change output. Any integer (including zero or negative) is passed through unchanged, as the Python keyword does. | The issue gives only `2`. The library accepts any `tab_length` value (`markdown/core.py:110`, EV-002). | A maintainer may want zero or negative values rejected. This is a reversible validation change. | FR-001 |

### 4.3 Questions for maintainers
| ID | Question | Why it matters | Blocks | Priority | Proposed default (ASM or "—") | Status |
|---|---|---|---|---|---|---|
| Q-001 | Should `--tab_length` reject values below 1, or accept any integer as the Python keyword does? | Sets the accepted range of the option. | — | P2 | ASM-001 (accept any integer) | Pending |

### 4.4 Conflicts
None.

### 4.5 Ambiguous terms
None. ("the same as" is defined by the Python keyword in SRC-003.)

### 4.6 Evidence log (repository reads)
| ID | Tool | Path:lines or search pattern | Outcome | Verbatim excerpt | Effect |
|---|---|---|---|---|---|
| EV-001 | Read | `markdown/__main__.py:84-125` | success | `parser.add_option("-q", "--quiet", default=CRITICAL,` ; `opts = {` | Shows the optparse pattern and the options dictionary that is passed to `markdownFromFile`. Used for FR-001 and FR-003. |
| EV-002 | Read | `markdown/core.py:105-110` | success | `tab_length (int): Length of tabs in the source. Default: `4`` ; `self.tab_length: int = kwargs.get('tab_length', 4)` | Default is 4; any value is accepted. Used for ASM-001 and AC-FR-003-2. |
| EV-003 | Grep | pattern `tab_length` in `markdown/__main__.py` | not-found | (no match) | Confirms the CLI has no way to set `tab_length` today (the issue's claim). |
| EV-004 | Read | `tests/test_apis.py:809-812` | success | `options, logging_level = parse_options([])` ; `self.assertEqual(options, self.default_options)` | The existing test pins the no-option dictionary. Used for AC-FR-003-1. |

### 4.7 Ignored instructions and out-of-scope requests
None.

### 4.8 Maintainer answers
None (new run).

## 5. Validation
### 5.1 Dimension coverage
| Dimension | Coverage | Items / questions / n-a reason |
|---|---|---|
| D1 Problem and goal | covered | SRC-001, FR-001 |
| D2 Actors | covered | CLI user (`python -m markdown`, `markdown_py`) |
| D3 Scope | covered | Summary §1 |
| D4 Required behaviour | covered | FR-001, FR-002 |
| D5 Inputs and outputs | partial | Integer value; Q-001 / ASM-001 |
| D6 Interfaces | covered | `--tab_length` option; `markdownFromFile` options dictionary |
| D7 Quality | covered | FR-003 (compatibility) |
| D8 Constraints | n/a | No repository constraint beyond the changelog rule, which is a design/implementation concern |
| D9 Security | n/a | The option does not change escaping or handling of untrusted HTML |
| D10 Edge and failure behaviour | partial | Non-integer value: ASM-001; Q-001 |
| D11 Transition | n/a | Additive option; no removal or deprecation |

### 5.2 Checks
| Check | Result | Findings |
|---|---|---|
| V1 Completeness | PASS | Every FR has ≥1 AC; SRC-002..004 each used; behaviour-changing FR-002 has preservation AC-FR-003-2 |
| V2 Consistency | PASS | No conflicting statements |
| V3 Traceability | PASS | Confirmed quotes copied from the issue; EV rows cited are success or not-found |
| V4 Feasibility | PASS | Option is additive; no documented behaviour contradicted |
| V5 Testability | PASS | Every AC names an input, a public call and an oracle |
| V6 Integrity | PASS | No embedded instructions; no implementation detail in requirements |

### 5.3 Readiness by item
| ID | Readiness | Reason |
|---|---|---|
| FR-001 | Ready | All criteria Confirmed |
| FR-002 | Needs-clarification | AC-FR-002-1 is Inferred |
| FR-003 | Needs-clarification | AC-FR-003-2 is Inferred |

### 5.4 Stage gate
- Decision: PASS
- Reasons: ≥1 FR exists and every FR has ≥1 AC; V5 is PASS for every AC; V3 and V6 are PASS; there is no P1 question and no CNF.
- Inferred acceptance criteria for maintainers to confirm on the pull request: AC-FR-002-1, AC-FR-003-2

## 6. Change log
| Version | Change | Reason (ANS / EV / validation) | Items |
|---|---|---|---|
| 0.1 | Initial spec | Issue #6 | all |
