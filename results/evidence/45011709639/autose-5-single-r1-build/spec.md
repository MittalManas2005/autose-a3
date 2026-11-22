---
artefact: spec
stage: requirements
issue: 5
issue_kind: feature
base_commit: ca2d6d37ae9baf0a946edded6815015f722ee57c
spec_version: 0.1
mode: new
skill: requirements-spec-builder 1.3-autose
status: PASS
ac_ids: [AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-001-4, AC-FR-002-1, AC-FR-003-1, AC-FR-003-2, AC-FR-004-1, AC-FR-004-2]
inferred_ac_ids: [AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-001-4, AC-FR-002-1, AC-FR-003-1, AC-FR-003-2, AC-FR-004-1, AC-FR-004-2]
blocking_questions: []
counts: {fr: 4, nfr: 0, con: 0, ac: 9, ac_confirmed: 0, ac_inferred: 9, q_p1: 0, q_p2: 2, q_p3: 0, ign: 0}
---

# Spec for issue #5: TOC: allow excluding individual headings from the table of contents

> Status: PASS. The issue states the behaviour and the example input and output. Every acceptance criterion is testable through the public API. Each criterion is `[Inferred]` only because its exact oracle fragment is ours, so maintainers should confirm the ACs on the pull request.
> Labels: Confirmed = stated in the issue or by a maintainer (quoted) · Inferred = derived, needs confirmation · Open = unknown.

## 1. Summary
- Problem as stated: "there is currently no way to leave a single heading out (only `toc_depth` for whole levels)" (SRC-001)
- Kind: feature. In scope: a heading with the class `notoc` (set with `attr_list`) is left out of the TOC, and out of `md.toc_tokens`. Out of scope: any other class, and any change to headings without `notoc`. Out of scope and not stated: a configurable class name (ASM-004).

## 2. Requirements
### FR-001 — Heading with class `notoc` is left out of the rendered TOC
- Statement: The `toc` extension shall omit from the generated Table of Contents any heading that has the class `notoc`.
- Label: Confirmed
- Source: Stated (SRC-002)
- Quote: "if a heading has the class `notoc` (set with `attr_list`), leave it out of the TOC"
- Basis: —
- Acceptance criteria:
  - AC-FR-001-1 [Inferred] (contains): Given the input "[TOC]", "", "# One", "", "## Two {: .notoc }", "", "## Three" with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown`, then the output contains `href="#three"`.
  - AC-FR-001-2 [Inferred] (not-contains): Given the same input as AC-FR-001-1, when converted through `markdown.markdown`, then the output does not contain `href="#two"`.
  - AC-FR-001-3 [Inferred] (not-contains): Given the input "[TOC]", "", "# One", "", "## Two {: .other .notoc }", "", "## Three" with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown`, then the output does not contain `href="#two"`.
  - AC-FR-001-4 [Inferred] (contains): Given the input "[TOC]", "", "# One", "", "## Two {: .notoc }", "", "### Four", "", "## Three" with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown`, then the output contains `href="#four"`.
- Links: —
- See-also: ASM-002, ASM-003
- Readiness: Needs-clarification — the ACs are Inferred and await maintainer confirmation of the example oracle.

### FR-002 — Heading with class `notoc` is left out of `md.toc_tokens`
- Statement: The `toc` extension shall omit from `md.toc_tokens` any heading that has the class `notoc`.
- Label: Confirmed
- Source: Stated (SRC-003)
- Quote: "It should also be left out of `md.toc_tokens`"
- Basis: —
- Acceptance criteria:
  - AC-FR-002-1 [Inferred] (property): Given the input "[TOC]", "", "# One", "", "## Two {: .notoc }", "", "## Three" with extensions `["toc", "attr_list"]` on a `markdown.Markdown` instance, when converted with `md.convert`, then the `name` values of all entries in `md.toc_tokens`, including nested `children`, in document order equal `["One", "Three"]`.
- Links: —
- See-also: ASM-002
- Readiness: Needs-clarification — the AC is Inferred.

### FR-003 — Excluded heading is still rendered with its id
- Statement: The `toc` extension shall keep rendering a heading that has the class `notoc` as an ordinary heading element, with its generated `id` attribute.
- Label: Confirmed
- Source: Stated (SRC-004)
- Quote: "The heading itself should still be rendered normally, including its id, so existing links to it keep working."
- Basis: —
- Acceptance criteria:
  - AC-FR-003-1 [Inferred] (contains): Given the input "[TOC]", "", "# One", "", "## Two {: .notoc }", "", "## Three" with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown`, then the output contains `id="two"`.
  - AC-FR-003-2 [Inferred] (contains): Given the same input as AC-FR-003-1, when converted through `markdown.markdown`, then the output contains `>Two</h2>`.
- Links: —
- See-also: ASM-001
- Readiness: Needs-clarification — the ACs are Inferred.

### FR-004 — Headings with other classes are unchanged
- Statement: The `toc` extension shall include in the TOC and in `md.toc_tokens` any heading whose classes do not include `notoc`, exactly as it does today.
- Label: Confirmed
- Source: Stated (SRC-005)
- Quote: "Headings with other classes should behave exactly as today."
- Basis: —
- Acceptance criteria:
  - AC-FR-004-1 [Inferred] (property) (preservation): Given the input "# One", "", "## Two {: .other }", "", "## Three" with extensions `["toc", "attr_list"]` on a `markdown.Markdown` instance, when converted with `md.convert`, then the `name` values of all entries in `md.toc_tokens`, including nested `children`, in document order equal `["One", "Two", "Three"]`.
  - AC-FR-004-2 [Inferred] (contains) (preservation): Given the input "[TOC]", "", "# One", "", "## Two {: .other }", "", "## Three" with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown`, then the output contains `href="#two"`.
- Links: —
- See-also: EV-001, EV-002
- Readiness: Needs-clarification — the ACs are Inferred.

## 3. Acceptance-criteria index
| AC ID | Parent | Label | Oracle | Input (short) | Expected (short) |
|---|---|---|---|---|---|
| AC-FR-001-1 | FR-001 | Inferred | contains | `notoc` on `## Two` | output contains `href="#three"` |
| AC-FR-001-2 | FR-001 | Inferred | not-contains | `notoc` on `## Two` | output does not contain `href="#two"` |
| AC-FR-001-3 | FR-001 | Inferred | not-contains | `.other .notoc` on `## Two` | output does not contain `href="#two"` |
| AC-FR-001-4 | FR-001 | Inferred | contains | `notoc` on `## Two`, child `### Four` | output contains `href="#four"` |
| AC-FR-002-1 | FR-002 | Inferred | property | `notoc` on `## Two`, `Markdown` instance | flattened `toc_tokens` names = `["One", "Three"]` |
| AC-FR-003-1 | FR-003 | Inferred | contains | `notoc` on `## Two` | output contains `id="two"` |
| AC-FR-003-2 | FR-003 | Inferred | contains | `notoc` on `## Two` | output contains `>Two</h2>` |
| AC-FR-004-1 | FR-004 | Inferred | property (preservation) | `.other` on `## Two`, `Markdown` instance | flattened `toc_tokens` names = `["One", "Two", "Three"]` |
| AC-FR-004-2 | FR-004 | Inferred | contains (preservation) | `.other` on `## Two` | output contains `href="#two"` |

## 4. Register
### 4.1 Source statements
| ID | Verbatim text | Kind (requirement / context / instruction) | Used by |
|---|---|---|---|
| SRC-001 | "there is currently no way to leave a single heading out (only `toc_depth` for whole levels)" | context | §1 |
| SRC-002 | "if a heading has the class `notoc` (set with `attr_list`), leave it out of the TOC" | requirement | FR-001 |
| SRC-003 | "It should also be left out of `md.toc_tokens`" | requirement | FR-002 |
| SRC-004 | "The heading itself should still be rendered normally, including its id, so existing links to it keep working." | requirement | FR-003 |
| SRC-005 | "Headings with other classes should behave exactly as today." | requirement | FR-004 |
| SRC-006 | `[TOC]` / `# One` / `## Two {: .notoc }` / `## Three` example; "should give a TOC with only "One" and "Three"." | requirement (example) | FR-001, AC-FR-001-1 |

### 4.2 Assumptions and proposed defaults
| ID | Assumption | Basis | Impact if wrong | Affects |
|---|---|---|---|---|
| ASM-001 | The `notoc` class stays on the rendered heading element in the output (not removed), because the issue asks for the heading to be "rendered normally". | Stated (SRC-004); no evidence either way | Output would differ by one class attribute; a maintainer can reverse in review | FR-003 (Q-001) |
| ASM-002 | Headings nested under an excluded heading (e.g. `### Four` under `## Two {: .notoc }`) stay in the TOC, and nest under their nearest included ancestor. | Not stated; the issue only says to leave out the heading itself. Follows from `nest_toc_tokens` (EV-001). | Child entries would be dropped or re-nested | FR-001, FR-002 (Q-002) |
| ASM-003 | `notoc` is matched as a whole token in the element's class list (so `.other .notoc` matches and `.notocx` does not). | The issue says "has the class `notoc`"; class lists are whitespace-separated (EV-002) | Substring matching would exclude unintended headings | FR-001 |
| ASM-004 | The class name is fixed at `notoc`, with no new `toc` configuration option. | The issue asks for the class `notoc` and does not ask for an option; a new option would widen the public surface | A maintainer may want a configurable name instead | Scope |

### 4.3 Questions for maintainers
| ID | Question | Why it matters | Blocks | Priority | Proposed default (ASM or "—") | Status |
|---|---|---|---|---|---|---|
| Q-001 | Should the `notoc` class remain on the rendered heading element? | Determines the exact HTML output | — | P2 | ASM-001 | Pending |
| Q-002 | Should headings nested under an excluded heading remain in the TOC? | Determines the nesting of `toc_tokens` | — | P2 | ASM-002 | Pending |

### 4.4 Conflicts
None.

### 4.5 Ambiguous terms
| ID | Term | Where | Candidate readings | Status |
|---|---|---|---|---|
| TERM-001 | "the class `notoc`" | SRC-002 | (a) a whole class token; (b) any class string containing `notoc` | Resolved as (a) in ASM-003, pending review |

### 4.6 Evidence log (repository reads)
| ID | Tool | Path:lines or search pattern | Outcome (success / not-found / irrelevant) | Verbatim excerpt | Effect |
|---|---|---|---|---|---|
| EV-001 | Read | markdown/extensions/toc.py:396-421 | success | `if int(el.tag[-1]) >= self.toc_top and int(el.tag[-1]) <= self.toc_bottom:` / `toc_tokens.append({` | The token append is the single point where a heading enters `toc_tokens`; the exclusion check belongs there. Supports FR-002 and ASM-002. |
| EV-002 | Read | markdown/extensions/attr_list.py:53-63 | success | `if t.startswith('.'):` / `return '.', t[1:]` | `.name` in attribute lists is a class token, so `notoc` arrives as a class string. Supports ASM-003 and the input form in the ACs. |
| EV-003 | Read | markdown/extensions/attr_list.py:75-87 | success | `attrs, remainder = _scanner.scan(attrs_string)` | Valueless words are stored as `None`. Relevant to K3 in the architecture document; `notoc` is a `.` class, not a valueless word. |
| EV-004 | Read | markdown/extensions/toc.py:402-404 | success | `if "id" not in el.attrib:` / `el.attrib["id"] = unique(...)` | Ids are generated for every heading, so excluding a heading from the TOC must not change id generation. Supports FR-003. |
| EV-005 | Read | docs/extensions/toc.md:71-73 | success | "The `toc_tokens` attribute is also available on the Markdown class" | The `toc_tokens` attribute is public, so FR-002 is testable through the public API. |
| EV-006 | Read | docs/changelog.md:15-17 | success | "## [Unreleased]" / "### Fixed" | An `[Unreleased]` section exists for the changelog entry. |

### 4.7 Ignored instructions and out-of-scope requests
None.

### 4.8 Maintainer answers
None (new mode).

## 5. Validation
### 5.1 Dimension coverage
| Dimension | Coverage | Items / questions / n-a reason |
|---|---|---|
| D1 Problem and goal | covered | SRC-001, FR-001 |
| D2 Actors | covered | Library users of the `toc` extension (SRC-001: "our docs") |
| D3 Scope | covered | §1 |
| D4 Required behaviour | covered | FR-001, FR-002 |
| D5 Inputs and outputs | covered | ACs use the issue's example input |
| D6 Interfaces | covered | `toc` extension output, `md.toc_tokens`; no new option (ASM-004) |
| D7 Quality | covered | FR-003, FR-004 (backward compatibility) |
| D8 Constraints | covered | EV-006 (changelog); K5 in architecture (no new dependency) |
| D9 Security | n/a (no change to escaping; the class value is only compared) | — |
| D10 Edge and failure | partial | Nested children (Q-002); multi-class (ASM-003) |
| D11 Transition | covered | Changelog entry under `[Unreleased]` (EV-006) |

### 5.2 Checks
| Check | Result (PASS / WARN / FAIL) | Findings |
|---|---|---|
| V1 Completeness | PASS | Every FR has ≥1 AC; D1–D11 covered; the behaviour-changing FR-001/FR-002 have their preservation counterpart in FR-004. |
| V2 Consistency | PASS | No conflicting items. Values match the issue quotes. |
| V3 Traceability | PASS | Every Confirmed quote is copied from the issue. Inferred items have a Basis or an ASM. |
| V4 Feasibility | PASS | Nothing contradicts documented behaviour (EV-005). |
| V5 Testability | PASS | Every AC has a concrete input, a public call (`markdown.markdown` or `md.convert`) and one oracle kind. |
| V6 Integrity | PASS | No Confirmed item without a quote. No design content. No embedded instruction was present. |

### 5.3 Readiness by item
| ID | Readiness | Reason |
|---|---|---|
| FR-001 | Needs-clarification | ACs are Inferred; Q-002 open |
| FR-002 | Needs-clarification | AC is Inferred; Q-002 open |
| FR-003 | Needs-clarification | ACs are Inferred; Q-001 open |
| FR-004 | Needs-clarification | ACs are Inferred |

### 5.4 Stage gate
- Decision: PASS
- Reasons: ≥1 FR exists and every FR has ≥1 AC; V5 PASS for every AC; V3 and V6 PASS; no P1 question and no CNF.
- Spec-level verdict: Partially (all items are Confirmed, but every AC is Inferred).
- Inferred acceptance criteria for maintainers to confirm on the pull request: AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-001-4, AC-FR-002-1, AC-FR-003-1, AC-FR-003-2, AC-FR-004-1, AC-FR-004-2

## 6. Change log
| Version | Change | Reason (ANS / EV / validation) | Items |
|---|---|---|---|
| 0.1 | Initial spec | Issue #5 | all |
