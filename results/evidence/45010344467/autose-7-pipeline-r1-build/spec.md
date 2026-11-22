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
ac_ids: [AC-FR-001-1, AC-FR-001-2, AC-FR-002-1, AC-FR-002-2, AC-NFR-001-1]
inferred_ac_ids: [AC-FR-001-1, AC-FR-001-2, AC-FR-002-1, AC-FR-002-2, AC-NFR-001-1]
blocking_questions: []
counts: {fr: 2, nfr: 1, con: 0, ac: 5, ac_confirmed: 0, ac_inferred: 5, q_p1: 0, q_p2: 1, q_p3: 1, ign: 0}
---

# Spec for issue #7: Links with code in them don't work sometimes

> Status: PASS. No P1 question is pending. The required behaviour is stated, the failing link form is not, and a safe default is proposed (ASM-001) that makes every link form with a code span in its text behave the same way.
> Labels: Confirmed = stated in the issue or by a maintainer (quoted) · Inferred = derived, needs confirmation · Open = unknown.

## 1. Summary
- Problem as stated: "Some of my links that have code formatting in them don't turn into links, the brackets just show up in the page." (SRC-001)
- Kind: bug. In scope: links whose text contains a code span, and the case where such links fail to render. Out of scope: not stated; no other change requested.
- The failing link form is not stated. The reporter says "Other links with code in them are fine" (SRC-002), so only some forms fail. See Q-001.

## 2. Requirements
### FR-001 — Links whose text contains a code span become links
- Statement: The Markdown converter shall render a link whose text contains a code span as an `a` element, the same as a link whose text contains no code span.
- Label: Confirmed
- Source: Stated (SRC-001)
- Quote: "Some of my links that have code formatting in them don't turn into links"
- Basis: The issue does not say which link syntax fails. The Confirmed part is the symptom; the acceptance criteria are Inferred because they use constructed examples. Repository evidence (EV-003) shows that reference-style links are resolved by their raw label text, which is the likely cause (not executed; see EV-003).
- Acceptance criteria:
  - AC-FR-001-1 [Inferred] (contains): Given input `[`code`][ref]` followed by a blank line and `[ref]: /url`, with no extensions, when converted through the public API, then the output contains `<a href="/url"><code>code</code></a>`.
  - AC-FR-001-2 [Inferred] (contains): Given input `[`code`]` followed by a blank line and `[`code`]: /url`, with no extensions, when converted through the public API, then the output contains `<a href="/url"><code>code</code></a>`.
- Links: Q-001 (P2), ASM-001
- See-also: Q-002, EV-001, EV-002, EV-003, EV-004
- Readiness: Needs-clarification — the failing form is unconfirmed and the acceptance criteria are Inferred.

### FR-002 — Links with code in them that already work keep working
- Statement: The Markdown converter shall keep rendering inline-style links whose text contains a code span, and reference-style links whose label contains no code span, exactly as before.
- Label: Inferred
- Source: Stated (SRC-002)
- Quote: —
- Basis: The issue states that "Other links with code in them are fine" (SRC-002), so the inline form with a code span in its text is reported to work. The reading of the code path (EV-004) indicates it does, but this has not been executed. The reference-style preservation case is a preservation criterion for the same code path (EV-003).
- Acceptance criteria:
  - AC-FR-002-1 [Inferred] (contains) (preservation): Given input `[`code`](/url)` with no extensions, when converted through the public API, then the output contains `<a href="/url"><code>code</code></a>`.
  - AC-FR-002-2 [Inferred] (contains) (preservation): Given input `[text][ref]` followed by a blank line and `[ref]: /url`, with no extensions, when converted through the public API, then the output contains `<a href="/url">text</a>`.
- Links: —
- See-also: EV-004
- Readiness: Needs-clarification — the acceptance criteria are Inferred.

## NFR-001 — Security: code span content stays escaped
- Statement: The Markdown converter shall keep HTML-escaping the content of a code span that appears inside link text.
- Label: Inferred
- Source: Repository (EV-002)
- Quote: —
- Basis: A code span is escaped by the backtick processor before it is placed in the link (EV-002). The change for FR-001 must not remove that escaping, so the criterion guards the output of untrusted text.
- Acceptance criteria:
  - AC-NFR-001-1 [Inferred] (contains) (preservation): Given input `[`<b>x</b>`](/url)` with no extensions, when converted through the public API, then the output contains `<code>&lt;b&gt;x&lt;/b&gt;</code>`.
- Links: —
- See-also: EV-002
- Readiness: Needs-clarification — the acceptance criterion is Inferred.

## 3. Acceptance-criteria index
| AC ID | Parent | Label | Oracle | Input (short) | Expected (short) |
|---|---|---|---|---|---|
| AC-FR-001-1 | FR-001 | Inferred | contains | `[`code`][ref]` + `[ref]: /url` | `<a href="/url"><code>code</code></a>` |
| AC-FR-001-2 | FR-001 | Inferred | contains | `[`code`]` + `` [`code`]: /url `` | `<a href="/url"><code>code</code></a>` |
| AC-FR-002-1 | FR-002 | Inferred | contains (preservation) | `[`code`](/url)` | `<a href="/url"><code>code</code></a>` |
| AC-FR-002-2 | FR-002 | Inferred | contains (preservation) | `[text][ref]` + `[ref]: /url` | `<a href="/url">text</a>` |
| AC-NFR-001-1 | NFR-001 | Inferred | contains (preservation) | `[`<b>x</b>`](/url)` | `<code>&lt;b&gt;x&lt;/b&gt;</code>` |

## 4. Register
### 4.1 Source statements
| ID | Verbatim text | Kind (requirement / context / instruction) | Used by |
|---|---|---|---|
| SRC-001 | "Some of my links that have code formatting in them don't turn into links, the brackets just show up in the page." | requirement | FR-001 |
| SRC-002 | "Other links with code in them are fine" | context | FR-002 |
| SRC-003 | "Can this be fixed?" | requirement | FR-001 |
| SRC-004 | "Python-Markdown 3.11.2" | context | — |

### 4.2 Assumptions and proposed defaults
| ID | Assumption | Basis | Impact if wrong | Affects |
|---|---|---|---|---|
| ASM-001 | Every link form whose label or link text contains a code span (inline style, reference style, short reference) should render as a link, like links without code. | Reference links are designed to resolve by label (EV-003). The issue asks for links with code to become links (SRC-001). The default changes nothing outside the link forms that have a code span in their text, and a maintainer can reverse it in review. | Behaviour of other link forms would change; FR-002 preservation criteria would then need review. | FR-001, AC-FR-001-1, AC-FR-001-2 |

### 4.3 Questions for maintainers
| ID | Question | Why it matters | Blocks | Priority | Proposed default (ASM or "—") | Status |
|---|---|---|---|---|---|---|
| Q-001 | Which link forms fail: inline `[`code`](url)`, reference `[`code`][ref]`, short reference `[`code`]`, or all of them when the link text contains a code span? | The issue does not give an example. The fix depends on which code path is wrong. | FR-001 | P2 | ASM-001 (every form with a code span in its text renders as a link) | Pending |
| Q-002 | Could the reporter post a minimal Markdown input (with the link definition, if any) that does not render as a link? | A concrete input would let the Testing stage confirm the failing case directly. | — | P3 | — | Pending |

### 4.4 Conflicts
None.

### 4.5 Ambiguous terms
| ID | Term | Where | Candidate readings | Status |
|---|---|---|---|---|
| TERM-001 | "code formatting" | SRC-001 | (a) backtick code span (`` `x` ``); (b) any inline formatting. The repository's Markdown has a single code-span syntax, so reading (a) is used. | Resolved by reading (a); recorded for transparency. |

### 4.6 Evidence log (repository reads)
| ID | Tool | Path:lines or search pattern | Outcome (success / not-found / irrelevant) | Verbatim excerpt | Effect |
|---|---|---|---|---|---|
| EV-001 | Grep | `markdown/inlinepatterns.py` for `BACKTICK_RE\|LINK_RE\|REFERENCE_RE` | success | `inlinePatterns.register(BacktickInlineProcessor(BACKTICK_RE), 'backtick', 190)` / `...LinkInlineProcessor(LINK_RE, md), 'link', 160)` / `...ReferenceInlineProcessor(REFERENCE_RE, md), 'reference', 170)` | Backtick processing (priority 190) runs before link and reference processing (160, 170). Code spans are therefore stashed before link brackets are read. |
| EV-002 | Read | `markdown/inlinepatterns.py:467-477` | success | `el.text = util.AtomicString(util.code_escape(data[start:end].strip()))` | Code spans in link text are HTML-escaped and stored as an element (basis for NFR-001). |
| EV-003 | Read | `markdown/inlinepatterns.py:1206-1221` | success | `id, end, handled = self.evalId(data, index, text)` … `if id not in self.md.references:  # ignore undefined refs` | Reference lookup uses the text after backtick processing. A label that contains a code span may be looked up as a placeholder, not as the raw label (basis for FR-001 and ASM-001). Not executed; this is the likely cause and is to be confirmed by the Testing stage. |
| EV-004 | Read | `markdown/inlinepatterns.py:1151-1168` (`getText`) | success | `if c == ']': bracket_count -= 1` | Bracket matching for inline links runs on the text after backtick processing. Code spans no longer contain raw brackets, so inline links with code in the text should resolve (basis for FR-002). Not executed. |
| EV-005 | Grep | `tests` for `\[`[^`]*`\]` | not-found | — | No existing test covers a reference label that contains a code span. |
| EV-006 | Grep | `tests` for `\[`[^`]*`\]\(` | not-found | — | No existing test covers an inline link whose text contains a code span. Coverage of FR-001 and FR-002 is therefore missing. |

### 4.7 Ignored instructions and out-of-scope requests
None.

### 4.8 Maintainer answers
None (new spec).

## 5. Validation
### 5.1 Dimension coverage
| Dimension | Coverage | Items / questions / n-a reason |
|---|---|---|
| D1 Problem and goal | covered | FR-001 (SRC-001) |
| D2 Actors | n/a | Single actor: a library user who converts Markdown with links that contain code spans. |
| D3 Scope | partial | Out-of-scope not stated; ASM-001 limits the change to link forms with a code span in their text. Q-001. |
| D4 Required behaviour | covered | FR-001, FR-002 |
| D5 Inputs and outputs | covered | AC-FR-001-1, AC-FR-001-2, AC-FR-002-1, AC-FR-002-2 |
| D6 Interfaces | n/a | No public API or option change requested. |
| D7 Quality (backward compatibility) | covered | FR-002 (preservation) |
| D8 Constraints | n/a | No stated constraint; no repository rule found in the evidence read. |
| D9 Security | covered | NFR-001 (escaping of code content) |
| D10 Edge and failure behaviour | partial | Combined and malformed inputs not stated; Q-002 asks for a minimal failing input. |
| D11 Transition | n/a | Bug fix; no deprecation or migration implied. |

### 5.2 Checks
| Check | Result (PASS / WARN / FAIL) | Findings |
|---|---|---|
| V1 Completeness | PASS | Every dimension is covered, asked about, or n/a with a reason. FR-001, FR-002 and NFR-001 each have an AC. Preservation AC present (FR-002, NFR-001). |
| V2 Consistency | PASS | No conflicting items. Values in the ACs match the expected HTML form `<a href="...">` used by the repository's link processors (EV-003). |
| V3 Traceability | PASS | Quotes are substrings of the issue (SRC-001, SRC-002). Inferred items have a Basis. Q-001 is linked from FR-001. Repository sources cite EV rows with outcome success or not-found. |
| V4 Feasibility | PASS | No request contradicts documented behaviour. No CNF. |
| V5 Testability | PASS | Each AC has a concrete input, a public call (conversion through the public API), and a contains oracle. |
| V6 Integrity | PASS | Confirmed items carry a quote. No label was changed without an answer. No design or internal function named. No embedded instructions. |

### 5.3 Readiness by item
| ID | Readiness | Reason |
|---|---|---|
| FR-001 | Needs-clarification | Failing form unconfirmed (Q-001); ACs Inferred. |
| FR-002 | Needs-clarification | ACs Inferred. |
| NFR-001 | Needs-clarification | AC Inferred. |

### 5.4 Stage gate
- Decision: PASS
- Reasons: ≥1 FR exists and every FR/NFR has ≥1 AC (condition 1). V5 is PASS for every AC (condition 2). V3 and V6 are PASS (condition 3). No P1 question is pending and there is no CNF (condition 4). Q-001 is P2 because ASM-001 is a safe default: it is consistent with reference-link lookup (EV-003), changes nothing outside link forms with code in their text, and is reversible in review.
- Spec-level verdict (informational): No (no item is Ready).
- Inferred acceptance criteria for maintainers to confirm on the pull request: AC-FR-001-1, AC-FR-001-2, AC-FR-002-1, AC-FR-002-2, AC-NFR-001-1.

## 6. Change log
| Version | Change | Reason (ANS / EV / validation) | Items |
|---|---|---|---|
| 0.1 | Initial spec from issue #7. | Issue text; EV-001 to EV-006. | FR-001, FR-002, NFR-001, Q-001, Q-002, ASM-001 |

## AutoSE stage check: all acceptance criteria are testable

Result: **PASS**

- all checks passed
