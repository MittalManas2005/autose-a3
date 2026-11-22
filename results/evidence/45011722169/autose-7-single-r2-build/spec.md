---
artefact: spec
stage: requirements
issue: 7
issue_kind: bug
base_commit: ca2d6d37ae9baf0a946edded6815015f722ee57c
spec_version: 0.1
mode: new
skill: requirements-spec-builder 1.3-autose
status: PASS
ac_ids: [AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-001-4]
inferred_ac_ids: [AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-001-4]
blocking_questions: []
counts: {fr: 1, nfr: 0, con: 0, ac: 4, ac_confirmed: 0, ac_inferred: 4, q_p1: 0, q_p2: 1, q_p3: 0, ign: 0}
---

# Spec for issue #7: Links with code in them don't work sometimes

> Status: PASS. The reported defect is clear enough to write testable criteria. The exact failing configuration is an inferred default (ASM-001) that maintainers can confirm on the pull request.
> Labels: Confirmed = stated in the issue or by a maintainer (quoted) · Inferred = derived, needs confirmation · Open = unknown.

## 1. Summary
- Problem as stated: "Some of my links that have code formatting in them don't turn into links, the brackets just show up in the page." (SRC-002)
- Kind: bug. In scope: links whose link text contains a code span and which fail to become `a` elements. Out of scope: anything not tied to that symptom (not stated).
- Reporter's version: Python-Markdown 3.11.2 (SRC-004).

## 2. Requirements
### FR-001 — Links whose text contains a code span become links
- Statement: The converter shall render a link whose link text contains a code span as an `a` element, as it does for links whose text has no code span.
- Label: Confirmed
- Source: Stated (SRC-001, SRC-002)
- Quote: "Some of my links that have code formatting in them don't turn into links, the brackets just show up in the page."
- Basis: The quote states the symptom and the expected result. The concrete failing forms are inferred (ASM-001) from reproduction (EV-005 to EV-007): inline links with a code span in the text already work, while reference-style links whose label is a code span do not.
- Acceptance criteria:
  - AC-FR-001-1 [Inferred] (contains): Given input "[`code`]" followed by a blank line and "[`code`]: http://example.com" with default settings, when converted through `markdown.markdown`, then the output contains `<a href="http://example.com"><code>code</code></a>`.
  - AC-FR-001-2 [Inferred] (contains): Given input "[`code`][]" followed by a blank line and "[`code`]: http://example.com" with default settings, when converted through `markdown.markdown`, then the output contains `<a href="http://example.com"><code>code</code></a>`.
  - AC-FR-001-3 [Inferred] (contains) (preservation): Given input "[`code`](http://example.com)" with default settings, when converted through `markdown.markdown`, then the output contains `<a href="http://example.com"><code>code</code></a>` (EV-005).
  - AC-FR-001-4 [Inferred] (contains) (preservation): Given input "[`code`]" with no matching reference definition, when converted through `markdown.markdown`, then the output contains `[<code>code</code>]` and does not contain `<a `.
- Links: Q-001, TERM-001
- See-also: ASM-001, EV-002, EV-003, EV-004
- Readiness: Needs-clarification — ACs are Inferred and await maintainer confirmation (Q-001, ASM-001).

## 3. Acceptance-criteria index
| AC ID | Parent | Label | Oracle | Input (short) | Expected (short) |
|---|---|---|---|---|---|
| AC-FR-001-1 | FR-001 | Inferred | contains | `[`code`]` + ref def | `<a href="http://example.com"><code>code</code></a>` |
| AC-FR-001-2 | FR-001 | Inferred | contains | `[`code`][]` + ref def | `<a href="http://example.com"><code>code</code></a>` |
| AC-FR-001-3 | FR-001 | Inferred | contains (preservation) | `[`code`](http://example.com)` | `<a href="http://example.com"><code>code</code></a>` |
| AC-FR-001-4 | FR-001 | Inferred | contains (preservation) | `[`code`]` without def | `[<code>code</code>]`, no `<a ` |

## 4. Register
### 4.1 Source statements
| ID | Verbatim text | Kind (requirement / context / instruction) | Used by |
|---|---|---|---|
| SRC-001 | "Some of my links that have code formatting in them don't turn into links" | requirement | FR-001 |
| SRC-002 | "the brackets just show up in the page" | context | FR-001 |
| SRC-003 | "Other links with code in them are fine, so I'm not sure what the difference is." | context | ASM-001, Q-001 |
| SRC-004 | "Python-Markdown 3.11.2" | context | Summary |
| SRC-005 | "Can this be fixed?" | requirement | FR-001 |

### 4.2 Assumptions and proposed defaults
| ID | Assumption | Basis | Impact if wrong | Affects |
|---|---|---|---|---|
| ASM-001 | The failing links are reference-style links whose label is a code span (`[`code`]`, `[`code`][]`). | Reproduction at the base commit: inline links with a code span in the text render correctly (EV-005); reference-style links with a code-span label do not (EV-006, EV-007). The reporter says other code-containing links work (SRC-003). | If other forms also fail, FR-001 needs more ACs; the fix is not wrong but incomplete. | FR-001, AC-FR-001-1..4 |

### 4.3 Questions for maintainers
| ID | Question | Why it matters | Blocks | Priority | Proposed default (ASM or "—") | Status |
|---|---|---|---|---|---|---|
| Q-001 | Is the failing link a reference-style link whose text is a code span (for example "[`code`]" with a "[`code`]: URL" definition)? If not, please paste one failing example. | Confirms the failing configuration in ASM-001. | — | P2 | ASM-001 | Pending |

### 4.4 Conflicts
None.

### 4.5 Ambiguous terms
| ID | Term | Where | Candidate readings | Status |
|---|---|---|---|---|
| TERM-001 | "sometimes" (SRC-001 / SRC-003) | Issue body | (a) reference-style links with a code-span label; (b) links whose code span contains brackets or parentheses; (c) links inside lists or other containers. Reproduction supports (a) only (EV-005 to EV-007). | Resolved as ASM-001 (default), question Q-001 open |

### 4.6 Evidence log (repository reads and reproduction)
| ID | Tool | Path:lines or search pattern | Outcome (success / not-found / irrelevant) | Verbatim excerpt | Effect |
|---|---|---|---|---|---|
| EV-001 | Read | markdown/inlinepatterns.py:74-77 | success | `inlinePatterns.register(BacktickInlineProcessor(BACKTICK_RE), 'backtick', 190)` | Backtick pass (190) runs before the reference (170) and link (160) passes, so code spans in link text are already placeholders when links are matched. |
| EV-002 | Read | markdown/inlinepatterns.py:1195-1221 | success | `text, index, handled = self.getText(data, m.end(0))` | Reference lookup key is built from the placeholder-containing text, not from the Markdown source. Basis for FR-001 and ASM-001. |
| EV-003 | Read | markdown/inlinepatterns.py:1223-1237 | success | `id = m.group(1).lower()` / `id = text.lower()` | Implicit (`[text][]`) and short (`[text]`) forms use the same text. Both are affected. |
| EV-004 | Read | markdown/inlinepatterns.py:104-122 | success | `BACKTICK_RE = r'(?:(?<!\\)((?:\\{2})+)(?=`+)\|(?<!\\)`)'` | Confirms code-span matching is a separate, earlier pass. |
| EV-005 | Run (reproduction at base commit, temporary probe `tests/scratch_probe_issue7.py`, which is still in the tree and must be deleted manually) | `markdown.markdown` on "[`code`](http://x)" | success | `<p><a href="http://x"><code>code</code></a></p>` | Inline link with code text works. Basis for AC-FR-001-3 (preservation). |
| EV-006 | Run (same probe) | `markdown.markdown` on "[`code`][1]" with "[1]: http://x" | success | `<p><a href="http://x"><code>code</code></a></p>` | Explicit reference works because the label is not the code span. |
| EV-007 | Run (same probe) | `markdown.markdown` on "[`code`]" with "[`code`]: http://x" | success | `<p>[<code>code</code>]</p>` (run: "[`x`]" with no definition gives `<p>[<code>x</code>]</p>`) | Reproduces the reported symptom: the short reference does not resolve. Basis for ASM-001 and AC-FR-001-1. |

Budget note: the requirements stage is read-only and limited to 12 reads/searches (§5.3). The combined single-session run exceeded that count. The extra reads were needed to locate the cause and are logged in full above.

### 4.7 Ignored instructions and out-of-scope requests
None.

### 4.8 Maintainer answers
None (new spec).

## 5. Validation
### 5.1 Dimension coverage
| Dimension | Coverage | Items / questions / n-a reason |
|---|---|---|
| D1 Problem and goal | covered | FR-001, SRC-001, SRC-002 |
| D2 Actors | covered | Library users calling `markdown.markdown` (Summary) |
| D3 Scope | partial | Out of scope not stated; covered by TERM-001 and Q-001 |
| D4 Required behaviour | covered | FR-001 |
| D5 Inputs and outputs | covered | AC-FR-001-1..4 |
| D6 Interfaces | covered | Public `markdown.markdown` only; no new option |
| D7 Quality | covered | AC-FR-001-3, AC-FR-001-4 (preservation) |
| D8 Constraints | n/a | No repository constraint affects requirements beyond the changelog rule (CON not required here) |
| D9 Security | n/a | The change does not touch escaping of raw HTML or URLs |
| D10 Edge and failure behaviour | partial | Undefined reference covered by AC-FR-001-4; other edge cases not stated (TERM-001) |
| D11 Transition | n/a | No API or output change for other inputs is intended |

### 5.2 Checks
| Check | Result (PASS / WARN / FAIL) | Findings |
|---|---|---|
| V1 Completeness | PASS | Every FR has ACs; every behaviour-changing FR has a preservation AC (AC-FR-001-3, AC-FR-001-4). |
| V2 Consistency | PASS | No conflicting items. |
| V3 Traceability | PASS | FR-001 quote is an exact substring of the issue. Repository evidence cites EV rows with outcome success. |
| V4 Feasibility | PASS | No V4 finding; no documented behaviour contradicted. |
| V5 Testability | PASS | Each AC names a concrete input, a public call and an oracle (contains). |
| V6 Integrity | PASS | No Confirmed item without a quote; ACs are Inferred. No design in this spec. Evidence rows are copied from tool output. A temporary probe file (tests/scratch_probe_issue7.py) could not be removed because the delete command was denied; it is not matched by the test discovery pattern (see design.md Risks). |

### 5.3 Readiness by item
| ID | Readiness | Reason |
|---|---|---|
| FR-001 | Needs-clarification | ACs are Inferred; ASM-001 and Q-001 pending. |

### 5.4 Stage gate
- Decision: PASS
- Reasons: ≥1 FR exists and it has ACs; all ACs pass V5; V3 and V6 pass; no P1 question is pending and there is no CNF.
- Inferred acceptance criteria for maintainers to confirm on the pull request: AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-001-4

## 6. Change log
| Version | Change | Reason (ANS / EV / validation) | Items |
|---|---|---|---|
| 0.1 | Initial spec | Issue #7 | FR-001, AC-FR-001-1..4, ASM-001, Q-001, TERM-001 |
