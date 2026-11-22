---
artefact: spec
stage: requirements
issue: 7
issue_kind: bug
base_commit: 3b69d28faa5287c08b881c747ea08a0298af07fc
spec_version: 0.2
mode: update
skill: requirements-spec-builder 1.3-autose
status: PASS
ac_ids: [AC-FR-001-2, AC-FR-001-3, AC-FR-001-4, AC-FR-001-5, AC-FR-002-1]
inferred_ac_ids: [AC-FR-001-2, AC-FR-001-3, AC-FR-001-4, AC-FR-001-5, AC-FR-002-1]
blocking_questions: []
counts: {fr: 2, nfr: 0, con: 0, ac: 5, ac_confirmed: 0, ac_inferred: 5, q_p1: 0, q_p2: 0, q_p3: 0, ign: 0}
---

# Spec for issue #7: Links with code in them don't work sometimes

> Status: PASS. The maintainer answer (ANS-001) identified the failing input as reference-style links whose label contains a backtick code span. Every acceptance criterion is testable; the criteria are Inferred and are listed for confirmation on the pull request.
> Labels: Confirmed = stated in the issue or by a maintainer (quoted) · Inferred = derived, needs confirmation · Open = unknown.

## 1. Summary
- Problem as stated: "Some of my links that have code formatting in them don't turn into links, the brackets just show up in the page." (SRC-001)
- Failing input (maintainer answer): "It's reference-style links where the label has backticks in it." (ANS-001)
- Working input (maintainer answer): "Inline links like `[`foo`](https://example.com)` already work." (ANS-001)
- Kind: bug. Reported version: "Python-Markdown 3.11.2" (SRC-004). In scope: reference-style links (shortcut `[`foo`]` and full `[text][`foo`]` forms) whose label contains a code span. Out of scope: inline links (stated to work already; kept as a preservation criterion); all other inputs (not stated).

## 2. Requirements
### FR-001 — Reference-style links with a code span in the label render as links
- Statement: The converter shall render a reference-style link whose label contains a code span, in shortcut form and in full form, as a link like any other reference link.
- Label: Confirmed
- Source: Stakeholder-answer (ANS-001)
- Quote: "It's reference-style links where the label has backticks in it." ; "Those should become links like any other reference link."
- Basis: The maintainer answer names the failing form and the expected behaviour. The expected HTML (link text rendered as `<code>`, href from the definition) is an Inferred operationalisation of "like any other reference link" (EV-006 shows the reference lookup; EV-003 documents code in reference-link labels). No reproduction was run in this stage.
- Acceptance criteria:
  - AC-FR-001-2 [Inferred] (contains) (preservation): Given input `[plain](https://example.com)` with no extensions, when converted through the public API, then the output contains `<a href="https://example.com">plain</a>`. Basis: general inline link behaviour, carried unchanged from v0.1 (EV-004 not re-read; kept as preservation for this FR).
  - AC-FR-001-3 [Inferred] (contains): Given the document `[`foo`]` followed by a blank line and the definition `[`foo`]: https://example.com`, with no extensions, when converted through the public API, then the output contains `<a href="https://example.com"><code>foo</code></a>`. Basis: shortcut form named in ANS-001; expected link text follows the documented code-in-label form (EV-003).
  - AC-FR-001-4 [Inferred] (contains): Given the document `[text][`foo`]` followed by a blank line and the definition `[`foo`]: https://example.com`, with no extensions, when converted through the public API, then the output contains `<a href="https://example.com">text</a>`. Basis: full form named in ANS-001; the link text is the bracketed `text`.
  - AC-FR-001-5 [Inferred] (contains) (preservation): Given the document `[text][foo]` followed by a blank line and the definition `[foo]: https://example.com`, with no extensions, when converted through the public API, then the output contains `<a href="https://example.com">text</a>`. Basis: plain reference link behaviour that must not regress; no existing test was read in this stage (EV-007 found no test with a code span in a reference label).
- Links: —
- See-also: ANS-001, EV-006, EV-007
- Readiness: Needs-clarification — all acceptance criteria are Inferred and must be confirmed by maintainers on the pull request.

### FR-002 — Inline links with a code span in the label keep working
- Statement: The converter shall keep rendering an inline link whose text is a code span as a link.
- Label: Confirmed
- Source: Stakeholder-answer (ANS-001)
- Quote: "Inline links like `[`foo`](https://example.com)` already work."
- Basis: The maintainer states that this form already works; the expected HTML is Inferred from the same statement and EV-001 (code spans are processed before links).
- Acceptance criteria:
  - AC-FR-002-1 [Inferred] (contains) (preservation): Given input `` [`foo`](https://example.com) `` with no extensions, when converted through the public API, then the output contains `<a href="https://example.com"><code>foo</code></a>`. Basis: ANS-001 states that this form already works; the exact output form is inferred.
- Links: —
- See-also: ANS-001, EV-001
- Readiness: Needs-clarification — the acceptance criterion is Inferred and must be confirmed by maintainers on the pull request.

## 3. Acceptance-criteria index
| AC ID | Parent | Label | Oracle | Input (short) | Expected (short) |
|---|---|---|---|---|---|
| AC-FR-001-2 | FR-001 | Inferred (preservation) | contains | `[plain](https://example.com)` | `<a href="https://example.com">plain</a>` |
| AC-FR-001-3 | FR-001 | Inferred | contains | `` [`foo`] `` + definition `` [`foo`]: https://example.com `` | `<a href="https://example.com"><code>foo</code></a>` |
| AC-FR-001-4 | FR-001 | Inferred | contains | `` [text][`foo`] `` + same definition | `<a href="https://example.com">text</a>` |
| AC-FR-001-5 | FR-001 | Inferred (preservation) | contains | `[text][foo]` + `[foo]: https://example.com` | `<a href="https://example.com">text</a>` |
| AC-FR-002-1 | FR-002 | Inferred (preservation) | contains | `` [`foo`](https://example.com) `` | `<a href="https://example.com"><code>foo</code></a>` |

## 4. Register
### 4.1 Source statements
| ID | Verbatim text | Kind (requirement / context / instruction) | Used by |
|---|---|---|---|
| SRC-001 | "Some of my links that have code formatting in them don't turn into links" | requirement | FR-001 |
| SRC-002 | "the brackets just show up in the page" | context | FR-001 |
| SRC-003 | "Other links with code in them are fine, so I'm not sure what the difference is." | context | FR-001, FR-002 |
| SRC-004 | "Python-Markdown 3.11.2" | context | — |

### 4.2 Assumptions and proposed defaults
None.

### 4.3 Questions for maintainers
| ID | Question | Why it matters | Blocks | Priority | Proposed default (ASM or "—") | Status |
|---|---|---|---|---|---|---|
| Q-001 | Which exact Markdown input fails? | Identified by the maintainer. | — | P1 | — | Answered (ANS-001) |

### 4.4 Conflicts
None.

### 4.5 Ambiguous terms
| ID | Term | Where | Candidate readings | Status |
|---|---|---|---|---|
| TERM-001 | "sometimes" | SRC-001 | (a) only when the link text contains a code span; (b) only when another backtick is unmatched in the same paragraph; (c) only for certain characters inside the code span | Resolved by ANS-001: reading (a) for reference-style links, with the label containing backticks. |

### 4.6 Evidence log (repository reads)
| ID | Tool | Path:lines or search pattern | Outcome (success / not-found / irrelevant) | Verbatim excerpt | Effect |
|---|---|---|---|---|---|
| EV-001 | Read | markdown/inlinepatterns.py:74-77 | success | `inlinePatterns.register(BacktickInlineProcessor(BACKTICK_RE), 'backtick', 190)` ; `inlinePatterns.register(LinkInlineProcessor(LINK_RE, md), 'link', 160)` | Code spans (priority 190) run before inline links (priority 160). Supports FR-002 (carried from v0.1). |
| EV-002 | Read | markdown/inlinepatterns.py:1151-1168 (`getText`) | success | `if c == ']': bracket_count -= 1` | Carried from v0.1. Link text is read by bracket counting. |
| EV-003 | Read | docs/contributing.md:288-290 | success | "Note that as the link label contains code, it should be wrapped in a code span and the reference needs to be defined immediately after." | Documents code in reference-link labels. Supports the expected form in AC-FR-001-3 and AC-FR-001-4. |
| EV-004 | Read | docs/changelog.md:34-35 | success | "Fix regression in `BacktickInlineProcessor` where text could be lost when opening and closing backticks did not match (#1668)." | Carried from v0.1. Earlier backtick-pairing bugs existed. |
| EV-005 | Search | tests/test_syntax, pattern `\[[^\]\n]*`[^\]\n]*\]\(` | not-found | — | Carried from v0.1. No syntax test covers a code span inside inline link text. |
| EV-006 | Read | markdown/inlinepatterns.py:76, 83, 1195-1221, 1251-1256 | success | `inlinePatterns.register(ReferenceInlineProcessor(REFERENCE_RE, md), 'reference', 170)` ; `if id not in self.md.references:  # ignore undefined refs` ; `return text.lower(), index, True` | Reference links (priority 170) are resolved by looking up the label text in the stored references; the shortcut form uses the link text as the label. Both run after the backtick pattern (priority 190). The mechanism of the failure is not verified in this stage and is left to Design. |
| EV-007 | Search | tests, pattern for reference label containing a backtick (`\]\[` followed by a backtick) | not-found | — | No existing test contains a code span in a reference label. Supports adding the criteria in FR-001 as new tests. |

### 4.7 Ignored instructions and out-of-scope requests
None.

### 4.8 Maintainer answers
| ID | From | Verbatim answer | Applied to |
|---|---|---|---|
| ANS-001 | @MittalManas2005 (issue #7, comment 7078239165) | "It's reference-style links where the label has backticks in it. For example `[`foo`]` with a definition `[`foo`]: https://example.com`, or `[text][`foo`]` with the same definition. Those should become links like any other reference link. Inline links like `[`foo`](https://example.com)` already work." | Q-001 (answered); TERM-001 (resolved); FR-001 (new statement, Confirmed); FR-002 (new, Confirmed); AC-FR-001-3, AC-FR-001-4 (examples covered); AC-FR-002-1 (inline example covered) |

Examples in ANS-001 and the criterion that covers each:
- `[`foo`]` with definition `[`foo`]: https://example.com` → AC-FR-001-3.
- `[text][`foo`]` with the same definition → AC-FR-001-4.
- `[`foo`](https://example.com)` (already works) → AC-FR-002-1.

## 5. Validation
### 5.1 Dimension coverage
| Dimension | Coverage | Items / questions / n-a reason |
|---|---|---|
| D1 Problem and goal | covered | FR-001, SRC-001, ANS-001 |
| D2 Actors | covered | Library users (implicit); the answer author is the issue author |
| D3 Scope | covered | FR-001 (reference-style links with code in the label); FR-002 (inline links, preservation); everything else out of scope |
| D4 Required behaviour | covered | FR-001 |
| D5 Inputs and outputs | covered | AC-FR-001-3, AC-FR-001-4 (failing inputs); AC-FR-002-1 (working input) |
| D6 Interfaces | n/a (no public API change stated) | — |
| D7 Quality | covered | AC-FR-001-2, AC-FR-001-5, AC-FR-002-1 (preservation) |
| D8 Constraints | covered | EV-003 (documented form) |
| D9 Security | n/a (no escaping or URL change stated) | — |
| D10 Edge and failure behaviour | partial | Undefined references and mixed cases are not stated by the maintainer; no criteria added for them (not required by the answer). |
| D11 Transition | n/a (bug fix; no API change stated) | — |

### 5.2 Checks
| Check | Result (PASS / WARN / FAIL) | Findings |
|---|---|---|
| V1 Completeness | PASS | Every FR has ACs. Every example in ANS-001 has a criterion. Preservation ACs present for FR-001 and FR-002. D10 partial is recorded and does not block. |
| V2 Consistency | PASS | No conflicting items. FR-001 supersedes the v0.1 inline-form statement, which is recorded in the change log. |
| V3 Traceability | PASS | Both Confirmed quotes are exact substrings of ANS-001. Repository items cite EV-001 to EV-007. |
| V4 Feasibility | PASS | No conflict with documented behaviour found. |
| V5 Testability | PASS | Every AC has a concrete input, a public call and a `contains` oracle. |
| V6 Integrity | PASS | Answer text used as data only. No design content. Only `spec.md` written. |

### 5.3 Readiness by item
| ID | Readiness | Reason |
|---|---|---|
| FR-001 | Needs-clarification | Statement Confirmed; ACs Inferred, to be confirmed on the pull request. |
| FR-002 | Needs-clarification | Statement Confirmed; AC Inferred, to be confirmed on the pull request. |

### 5.4 Stage gate
- Decision: PASS
- Reasons: Condition 1 holds (two FRs, each with ACs). Condition 2 holds (V5 PASS for every AC). Condition 3 holds (V3 and V6 PASS). Condition 4 holds: Q-001 is answered (ANS-001), no P1 question is pending and no CNF exists.
- Inferred acceptance criteria for maintainers to confirm on the pull request: AC-FR-001-2, AC-FR-001-3, AC-FR-001-4, AC-FR-001-5, AC-FR-002-1

## 6. Change log
| Version | Change | Reason (ANS / EV / validation) | Items |
|---|---|---|---|
| 0.1 | Initial spec from issue #7 | Issue text; EV-001 to EV-005 | FR-001, AC-FR-001-1, AC-FR-001-2, Q-001, TERM-001 |
| 0.2 | FR-001 restated: the failing input is reference-style links with a code span in the label (shortcut and full forms), not inline links. | ANS-001 (Q-001 answered; TERM-001 resolved) | FR-001 |
| 0.2 | v0.1 criterion 1 (inline form `[`code`](url)`) withdrawn: ANS-001 states that this form already works, so it is no longer a failing case. Its ID is retired and not reused. | ANS-001 | v0.1 AC-FR-001-1 |
| 0.2 | AC-FR-001-2 kept unchanged as a preservation criterion under FR-001. | Carried from v0.1 | AC-FR-001-2 |
| 0.2 | New criteria AC-FR-001-3 (shortcut form), AC-FR-001-4 (full form), AC-FR-001-5 (plain reference-link preservation). | ANS-001 examples; EV-006, EV-007 | AC-FR-001-3, AC-FR-001-4, AC-FR-001-5 |
| 0.2 | FR-002 added: inline links with a code label keep working (stated in ANS-001); preservation AC-FR-002-1. | ANS-001 | FR-002, AC-FR-002-1 |
| 0.2 | Q-001 answered; TERM-001 resolved; status changed from NEEDS_INPUT to PASS. | ANS-001; stage gate §8.5 | Q-001, TERM-001 |
| 0.2 | Evidence added: EV-006 (reference lookup), EV-007 (no reference-label test). | Step 4 evidence within budget | EV-006, EV-007 |

## AutoSE stage check: all acceptance criteria are testable

Result: **PASS**

## AutoSE stage check: all acceptance criteria are testable

Result: **PASS**

- all checks passed
