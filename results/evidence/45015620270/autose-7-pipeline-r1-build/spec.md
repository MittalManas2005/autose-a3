---
artefact: spec
stage: requirements
issue: 7
issue_kind: bug
base_commit: 3b69d28faa5287c08b881c747ea08a0298af07fc
spec_version: 0.1
mode: new
skill: requirements-spec-builder 1.3-autose
status: NEEDS_INPUT
ac_ids: [AC-FR-001-1, AC-FR-001-2]
inferred_ac_ids: [AC-FR-001-1, AC-FR-001-2]
blocking_questions: [Q-001]
counts: {fr: 1, nfr: 0, con: 0, ac: 2, ac_confirmed: 0, ac_inferred: 2, q_p1: 1, q_p2: 0, q_p3: 0, ign: 0}
---

# Spec for issue #7: Links with code in them don't work sometimes

> Status: NEEDS_INPUT. The issue does not say which link input fails, so the behaviour that must change cannot be identified (P1 question Q-001).
> Labels: Confirmed = stated in the issue or by a maintainer (quoted) · Inferred = derived, needs confirmation · Open = unknown.

## 1. Summary
- Problem as stated: "Some of my links that have code formatting in them don't turn into links, the brackets just show up in the page." (SRC-002)
- Stated contrast: "Other links with code in them are fine" (SRC-003). The author did not give an example input.
- Kind: bug. Reported version: "Python-Markdown 3.11.2" (SRC-004). In scope: links whose text contains a code span that fail to render as links. Out of scope: not stated.

## 2. Requirements
### FR-001 — Links whose text contains a code span render as links
- Statement: The converter shall render a link whose text contains a code span as a link, not as literal bracket characters.
- Label: Confirmed
- Source: Stated (SRC-001)
- Quote: "links that have code formatting in them don't turn into links"
- Basis: The quote states the symptom only. Which inputs fail is unknown (Q-001). The scope of "sometimes" is not identified. Repository reads (EV-001, EV-002) show that code spans are tokenised before links, so the failing inputs are probably ones where backtick pairing or bracket matching goes wrong. This is unverified: no reproduction was run, because the Requirements stage has no execution rights.
- Acceptance criteria:
  - AC-FR-001-1 [Inferred] (contains): Given input `` [`code`](https://example.com) `` with no extensions, when converted through the public API, then the output contains `<a href="https://example.com"><code>code</code></a>`. Basis: a constructed example; the issue gives none. It is the form that the documentation's code-in-label example describes (EV-003).
  - AC-FR-001-2 [Inferred] (contains) (preservation): Given input `[plain](https://example.com)` with no extensions, when converted through the public API, then the output contains `<a href="https://example.com">plain</a>`. Basis: general link behaviour; not yet confirmed by a test read (EV-004 not checked).
- Links: Q-001
- See-also: EV-001, EV-002, EV-003, EV-004, EV-005
- Readiness: Needs-clarification — the failing input is unknown (Q-001).

## 3. Acceptance-criteria index
| AC ID | Parent | Label | Oracle | Input (short) | Expected (short) |
|---|---|---|---|---|---|
| AC-FR-001-1 | FR-001 | Inferred | contains | `` [`code`](https://example.com) `` | `<a href="https://example.com"><code>code</code></a>` |
| AC-FR-001-2 | FR-001 | Inferred (preservation) | contains | `[plain](https://example.com)` | `<a href="https://example.com">plain</a>` |

## 4. Register
### 4.1 Source statements
| ID | Verbatim text | Kind (requirement / context / instruction) | Used by |
|---|---|---|---|
| SRC-001 | "Some of my links that have code formatting in them don't turn into links" | requirement | FR-001 |
| SRC-002 | "the brackets just show up in the page" | context | FR-001 |
| SRC-003 | "Other links with code in them are fine, so I'm not sure what the difference is." | context | Q-001 |
| SRC-004 | "Python-Markdown 3.11.2" | context | Q-001 |

(SRC-001 and SRC-002 are one quoted sentence pair from the issue body. Both are kept for traceability.)

### 4.2 Assumptions and proposed defaults
None.

### 4.3 Questions for maintainers
| ID | Question | Why it matters | Blocks | Priority | Proposed default (ASM or "—") | Status |
|---|---|---|---|---|---|---|
| Q-001 | Which exact Markdown input fails? Please give a minimal example and the expected HTML. Options: (a) a code span inside link text, e.g. `` [`code`](url) ``; (b) a code span inside the link text plus an unmatched backtick earlier in the paragraph; (c) a code span with `]` or `(` inside it; (d) other (please give the input). | Which behaviour must change cannot be identified without the input. A guessed fix could change correct output. | FR-001 | P1 | — | Pending |

### 4.4 Conflicts
None.

### 4.5 Ambiguous terms
| ID | Term | Where | Candidate readings | Status |
|---|---|---|---|---|
| TERM-001 | "sometimes" | SRC-001 | (a) only when the link text contains a code span; (b) only when another backtick is unmatched in the same paragraph; (c) only for certain characters inside the code span | Pending (Q-001) |

### 4.6 Evidence log (repository reads)
| ID | Tool | Path:lines or search pattern | Outcome (success / not-found / irrelevant) | Verbatim excerpt | Effect |
|---|---|---|---|---|---|
| EV-001 | Read | markdown/inlinepatterns.py:74-77 | success | `inlinePatterns.register(BacktickInlineProcessor(BACKTICK_RE), 'backtick', 190)` ; `inlinePatterns.register(LinkInlineProcessor(LINK_RE, md), 'link', 160)` | Code spans (priority 190) are processed before links (priority 160). A link containing a code span is therefore not expected to fail for that reason alone. Failure must come from pairing or ordering. Basis for TERM-001 and Q-001. |
| EV-002 | Read | markdown/inlinepatterns.py:1151-1168 (`getText`) | success | `if c == ']': bracket_count -= 1` | Link text is read by bracket counting. Bracket characters inside code spans are only hidden if the code span was already replaced before this runs. Supports option (c) in Q-001. |
| EV-003 | Read | docs/contributing.md:288-290 | success | "Note that as the link label contains code, it should be wrapped in a code span and the reference needs to be defined immediately after." | Documents that code in a link label is supported. Supports AC-FR-001-1 as the expected form. Applies to reference-style links only, so the inline form is Inferred. |
| EV-004 | Read | docs/changelog.md:34-35 | success | "Fix regression in `BacktickInlineProcessor` where text could be lost when opening and closing backticks did not match (#1668)." | Earlier backtick-pairing bugs existed. Supports option (b) in Q-001 as a plausible cause. |
| EV-005 | Search | tests/test_syntax, pattern `\[[^\]\n]*`[^\]\n]*\]\(` | not-found | — | No syntax test covers a code span inside inline link text. This gap may explain why the bug is not caught. |

### 4.7 Ignored instructions and out-of-scope requests
None.

### 4.8 Maintainer answers
None (new mode).

## 5. Validation
### 5.1 Dimension coverage
| Dimension | Coverage | Items / questions / n-a reason |
|---|---|---|
| D1 Problem and goal | covered | FR-001, SRC-001 |
| D2 Actors | partial | Library users (implicit); Q-001 |
| D3 Scope | partial | Q-001 (which inputs) |
| D4 Required behaviour | covered | FR-001 (Inferred detail) |
| D5 Inputs and outputs | partial | AC-FR-001-1 constructed; Q-001 |
| D6 Interfaces | n/a (no public API change stated) | — |
| D7 Quality | covered | AC-FR-001-2 (preservation) |
| D8 Constraints | covered | EV-003 (documented form) |
| D9 Security | n/a (no escaping or URL change stated) | — |
| D10 Edge and failure behaviour | partial | TERM-001; Q-001 |
| D11 Transition | n/a (bug fix; no API change stated) | — |

### 5.2 Checks
| Check | Result (PASS / WARN / FAIL) | Findings |
|---|---|---|
| V1 Completeness | WARN | Every FR has an AC. D2, D3, D5 and D10 are partial and each has Q-001. |
| V2 Consistency | PASS | No conflicting items. |
| V3 Traceability | PASS | Confirmed quote is an exact substring of the issue. Repository items cite EV-001 to EV-005. |
| V4 Feasibility | PASS | No conflict with documented behaviour found. |
| V5 Testability | WARN | AC-FR-001-1 and AC-FR-001-2 have concrete inputs and an oracle. The failing input (the thing FR-001 is about) is not yet known, so FR-001 is not fully testable. |
| V6 Integrity | PASS | No instructions in the issue. No design content. Only `spec.md` written. |

### 5.3 Readiness by item
| ID | Readiness | Reason |
|---|---|---|
| FR-001 | Needs-clarification | Failing input unknown (Q-001). |

### 5.4 Stage gate
- Decision: NEEDS_INPUT
- Reasons: Condition 4 fails. Q-001 is a pending P1 question: the issue does not identify which input fails, and no safe proposed default exists. Conditions 1–3 hold (one FR, every FR has an AC, V3 and V6 PASS). V5 is WARN for FR-001, so a maintainer must supply the failing input before testing.
- Inferred acceptance criteria for maintainers to confirm on the pull request: AC-FR-001-1, AC-FR-001-2

## 6. Change log
| Version | Change | Reason (ANS / EV / validation) | Items |
|---|---|---|---|
| 0.1 | Initial spec from issue #7 | Issue text; EV-001 to EV-005 | FR-001, AC-FR-001-1, AC-FR-001-2, Q-001, TERM-001 |

## AutoSE stage check: all acceptance criteria are testable

Result: **FAIL**

- requirements need maintainer input: Q-001
