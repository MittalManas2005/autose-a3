---
artefact: spec
stage: requirements
issue: 7
issue_kind: bug
base_commit: 758ab062032e4096fc14a4bb219015e83820c890
spec_version: 0.1
mode: new
skill: requirements-spec-builder 1.3-autose
status: NEEDS_INPUT
ac_ids: [AC-FR-001-1, AC-FR-001-2, AC-FR-001-3]
inferred_ac_ids: [AC-FR-001-1, AC-FR-001-2, AC-FR-001-3]
blocking_questions: [Q-001]
counts: {fr: 1, nfr: 0, con: 0, ac: 3, ac_confirmed: 0, ac_inferred: 3, q_p1: 1, q_p2: 0, q_p3: 0, ign: 0}
---

# Spec for issue #7: Links with code in them don't work sometimes

> Status: NEEDS_INPUT. The issue says some links that contain code formatting are not rendered as links, but it gives no failing input and no expected HTML, so the affected links cannot be identified (Q-001, P1).
> Labels: Confirmed = stated in the issue or by a maintainer (quoted) · Inferred = derived, needs confirmation · Open = unknown.

## 1. Summary
- Problem as stated: "Some of my links that have code formatting in them don't turn into links, the brackets just show up in the page." (SRC-001)
- Kind: bug. In scope: links whose link text contains code formatting, as far as the failing form is identified (see Q-001). Out of scope: not stated; any other link form is not mentioned.
- Reported version: "Python-Markdown 3.11.2" (SRC-002).
- The reporter asks: "Can this be fixed?" (SRC-003). This is a request for a fix, not a separate requirement.

## 2. Requirements
### FR-001 — Links whose text contains code formatting are rendered as links
- Statement: The converter shall render a Markdown link whose link text contains a code span as an HTML `a` element, with the code span rendered as `code` inside it.
- Label: Confirmed
- Source: Stated (SRC-001)
- Quote: "Some of my links that have code formatting in them don't turn into links"
- Basis: The quote states the symptom and the wanted outcome. It does not say which link forms fail, so the set of affected inputs is open (Q-001, TERM-001). The ACs below are the agent's candidate operationalisations, not stated by the reporter.
- Acceptance criteria:
  - AC-FR-001-1 [Inferred] (exact): Given input `` [`code`](https://example.com) `` with no extensions, when converted through the public API, then the output is `<p><a href="https://example.com"><code>code</code></a></p>`.
  - AC-FR-001-2 [Inferred] (contains) (preservation): Given input `[text](https://example.com)` with no extensions, when converted through the public API, then the output contains `<a href="https://example.com">text</a>`.
  - AC-FR-001-3 [Inferred] (contains): Given input `` [`a]b`](https://example.com) `` with no extensions, when converted through the public API, then the output contains `<a href="https://example.com"><code>a]b</code></a>`.
- Links: Q-001, TERM-001
- See-also: EV-001, EV-002, EV-003, EV-004
- Readiness: Needs-clarification — the affected input form is unknown (Q-001); AC-FR-001-1 and AC-FR-001-3 are candidates until the reporter confirms the failing form.

## 3. Acceptance-criteria index
| AC ID | Parent | Label | Oracle | Input (short) | Expected (short) |
|---|---|---|---|---|---|
| AC-FR-001-1 | FR-001 | Inferred | exact | `` [`code`](https://example.com) `` | `<p><a href="https://example.com"><code>code</code></a></p>` |
| AC-FR-001-2 | FR-001 | Inferred (preservation) | contains | `[text](https://example.com)` | `<a href="https://example.com">text</a>` |
| AC-FR-001-3 | FR-001 | Inferred | contains | `` [`a]b`](https://example.com) `` | `<a href="https://example.com"><code>a]b</code></a>` |

## 4. Register
### 4.1 Source statements
| ID | Verbatim text | Kind (requirement / context / instruction) | Used by |
|---|---|---|---|
| SRC-001 | "Some of my links that have code formatting in them don't turn into links, the brackets just show up in the page." | requirement | FR-001 |
| SRC-002 | "Python-Markdown 3.11.2" | context | Summary |
| SRC-003 | "Other links with code in them are fine, so I'm not sure what the difference is. Can this be fixed?" | context | Q-001 |

### 4.2 Assumptions and proposed defaults
None. No default is safe for the failing input (see Q-001).

### 4.3 Questions for maintainers
| ID | Question | Why it matters | Blocks | Priority | Proposed default (ASM or "—") | Status |
|---|---|---|---|---|---|---|
| Q-001 | Which link form fails? Please reply with one failing Markdown snippet and its expected HTML. Options: (A) the code span inside the link text contains `[` or `]`; (B) the link text contains a code span, and an earlier backtick in the same paragraph is unmatched or belongs to another code span; (C) the code span is in the link URL or title; (D) none of these: paste the failing snippet. | The issue gives no input, so the fix and the ACs cannot be fixed. Reporter says other links with code work (SRC-003). | FR-001 (AC-FR-001-1, AC-FR-001-3 remain Inferred until answered) | P1 | — | Pending |

### 4.4 Conflicts
None.

### 4.5 Ambiguous terms
| ID | Term | Where | Candidate readings | Status |
|---|---|---|---|---|
| TERM-001 | "sometimes" / "some of my links" | SRC-001, SRC-003 | (a) only links whose text contains `[` or `]` inside the code span; (b) links affected by backtick pairing elsewhere in the paragraph; (c) links with a code span in the URL or title; (d) other | Open (Q-001) |

### 4.6 Evidence log (repository reads)
| ID | Tool | Path:lines or search pattern | Outcome (success / not-found / irrelevant) | Verbatim excerpt | Effect |
|---|---|---|---|---|---|
| EV-001 | Read | markdown/inlinepatterns.py:407-477 | success | `class BacktickInlineProcessor(InlineProcessor):` ... `el.text = util.AtomicString(util.code_escape(data[start:end].strip()))` | Code spans are turned into placeholder-stashed `code` elements; supports the reading that AC-FR-001-1 is the normal case. Priority registration at inlinepatterns.py:74 (`'backtick', 190`) and link at :77 (`'link', 160`) — backtick runs before link. |
| EV-002 | Read | markdown/inlinepatterns.py:1009-1033 | success | `text, index, handled = self.getText(data, m.end(0))` ... `el.set("href", href)` | Link text is read from the already-processed string; supports Q-001 options (A) and (B) as candidate causes. |
| EV-003 | Grep | tests/ for code span inside link text (`\[[^\]\n]*`[^\n]*\]\(`, *.py) | not-found | — | No existing test covers a code span inside link text, so the reported behaviour is not pinned by a test. |
| EV-004 | Read | tests/test_syntax/inline/test_links.py:355-380 (grep "code") | success | `'<a href="https://github.com/Python-Markdown/markdown/blob/master/CODE_OF_CONDUCT.md">code of\n'` | Existing link output format is `<a href="…">text</a>`; basis for AC-FR-001-2. |

### 4.7 Ignored instructions and out-of-scope requests
None.

### 4.8 Maintainer answers
None (new run).

## 5. Validation
### 5.1 Dimension coverage
| Dimension | Coverage | Items / questions / n-a reason |
|---|---|---|
| D1 Problem and goal | covered | SRC-001, FR-001 |
| D2 Actors | partial | Library user rendering Markdown; not named further. Q-001 |
| D3 Scope | partial | Affected link forms unknown. Q-001, TERM-001 |
| D4 Required behaviour | covered | FR-001 (as stated) |
| D5 Inputs and outputs | partial | No failing input or expected HTML given; candidate ACs only. Q-001 |
| D6 Interfaces | n/a | No new option or API is requested; the public `markdown` conversion API is the only surface. |
| D7 Quality | covered | AC-FR-001-2 (preservation) |
| D8 Constraints | n/a | No constraint is stated in the issue; repository rules were not checked for this issue. |
| D9 Security | n/a | The issue does not touch escaping or untrusted input handling. |
| D10 Edge and failure behaviour | partial | Q-001 covers the failing forms; none specified. |
| D11 Transition | n/a | No deprecation or migration is stated or implied. |

### 5.2 Checks
| Check | Result (PASS / WARN / FAIL) | Findings |
|---|---|---|
| V1 Completeness | PASS | FR-001 has three ACs; behaviour-changing FR has preservation AC-FR-001-2; partial dimensions have Q-001. |
| V2 Consistency | PASS | Expected values match the quoted link format in EV-004. |
| V3 Traceability | PASS | SRC-001 quote is an exact substring of the issue; Repository sources cite EV-001, EV-002 (success), EV-003 (not-found), EV-004 (success). |
| V4 Feasibility | PASS | No request contradicts documented behaviour. |
| V5 Testability | PASS | Each AC has a concrete input, the public conversion call, and an oracle kind. |
| V6 Integrity | PASS | No Confirmed item without quote; no design content; no file written other than spec.md. |

### 5.3 Readiness by item
| ID | Readiness | Reason |
|---|---|---|
| FR-001 | Needs-clarification | Affected input form unknown (Q-001); ACs are candidates. |

Spec-level verdict: Partially (no FR is Ready).

### 5.4 Stage gate
- Decision: NEEDS_INPUT
- Reasons: Conditions 1–3 hold (one FR, each with ACs; V5 PASS; V3 and V6 PASS). Condition 4 fails: Q-001 is a P1 question with no safe proposed default, because the issue does not identify which link form should change (§8.5 typical P1 case).
- Inferred acceptance criteria for maintainers to confirm on the pull request: AC-FR-001-1, AC-FR-001-2, AC-FR-001-3

## 6. Change log
| Version | Change | Reason (ANS / EV / validation) | Items |
|---|---|---|---|
| 0.1 | Initial spec from issue #7 at base commit 758ab062032e4096fc14a4bb219015e83820c890. | New run | FR-001, AC-FR-001-1..3, Q-001, TERM-001, SRC-001..003, EV-001..004 |

## AutoSE stage check: all acceptance criteria are testable

Result: **FAIL**

- requirements need maintainer input: Q-001
