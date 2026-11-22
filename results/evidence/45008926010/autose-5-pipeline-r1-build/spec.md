---
artefact: spec
stage: requirements
issue: 5
issue_kind: feature
base_commit: 758ab062032e4096fc14a4bb219015e83820c890
spec_version: 0.1
mode: new
skill: requirements-spec-builder 1.3-autose
status: PASS
ac_ids: [AC-FR-001-1, AC-FR-002-1, AC-FR-003-1, AC-FR-004-1]
inferred_ac_ids: [AC-FR-002-1, AC-FR-004-1]
blocking_questions: []
counts: {fr: 4, nfr: 0, con: 0, ac: 4, ac_confirmed: 2, ac_inferred: 2, q_p1: 0, q_p2: 3, q_p3: 0, ign: 0}
---

# Spec for issue #5: TOC: allow excluding individual headings from the table of contents

> Status: PASS. Every requirement has a testable acceptance criterion through the public API, and the open questions have safe proposed defaults (ASM-001 to ASM-003).
> Labels: Confirmed = stated in the issue or by a maintainer (quoted) · Inferred = derived, needs confirmation · Open = unknown.

## 1. Summary
- Problem as stated: "there is currently no way to leave a single heading out (only `toc_depth` for whole levels)." (SRC-002)
- Kind: feature. In scope: a heading marked with the class `notoc` (set with `attr_list`) is left out of the TOC and out of `md.toc_tokens`, and keeps its normal rendering and id. Preserved, not changed: headings with other classes must behave as today (SRC-008). Out of scope: not stated. Not stated: behaviour of child headings under an excluded heading, and of permalinks/anchor links on excluded headings (Q-001, Q-002).

## 2. Requirements

### FR-001 — Exclude headings with class `notoc` from the TOC
- Statement: The Table of Contents extension shall leave out of the generated TOC any heading that carries the class `notoc`.
- Label: Confirmed
- Source: Stated (SRC-003), example in Stated (SRC-004, SRC-005)
- Quote: "if a heading has the class `notoc` (set with `attr_list`), leave it out of the TOC:"
- Basis: —
- Acceptance criteria:
  - AC-FR-001-1 [Confirmed] (property): Given the input "[TOC]\n\n# One\n\n## Two {: .notoc }\n\n## Three" with extensions ["toc", "attr_list"], when converted with `markdown.markdown()`, then the TOC `<a>` link targets are exactly `#one` and `#three` (no `#two`).
- Links: —
- See-also: ASM-002, Q-002 (child headings), EV-005
- Readiness: Ready — all criteria Confirmed; no pending question linked.

### FR-002 — Excluded heading is still rendered with its id
- Statement: The Table of Contents extension shall render a heading carrying the class `notoc` as normal body markup, including its `id` attribute.
- Label: Confirmed
- Source: Stated (SRC-006)
- Quote: "The heading itself should still be rendered normally, including its id, so existing links to it keep working."
- Basis: The exact attribute order and the slug value `two` are inferred from the existing slug behaviour (EV-002), not stated.
- Acceptance criteria:
  - AC-FR-002-1 [Inferred] (contains): Given the input "[TOC]\n\n# One\n\n## Two {: .notoc }\n\n## Three" with extensions ["toc", "attr_list"], when converted with `markdown.markdown()`, then the output contains `id="two"` and `>Two</h2>`.
- Links: TERM-001
- See-also: Q-001, Q-003, ASM-001, ASM-003
- Readiness: Needs-clarification — the AC is Inferred and TERM-001 ("rendered normally") is pending confirmation.

### FR-003 — Excluded heading is left out of `md.toc_tokens`
- Statement: The Table of Contents extension shall omit a heading carrying the class `notoc` from the `md.toc_tokens` list at every nesting level.
- Label: Confirmed
- Source: Stated (SRC-007)
- Quote: "It should also be left out of `md.toc_tokens`, because we build our sidebar from that."
- Basis: —
- Acceptance criteria:
  - AC-FR-003-1 [Confirmed] (property): Given the input "[TOC]\n\n# One\n\n## Two {: .notoc }\n\n## Three" with extensions ["toc", "attr_list"], when converted with a `Markdown` instance and `md.toc_tokens` is read, then no entry at any nesting level has `name` equal to "Two", and entries named "One" and "Three" are present.
- Links: —
- See-also: EV-004, EV-006
- Readiness: Ready — all criteria Confirmed; no pending question linked.

### FR-004 — Headings with other classes behave as today
- Statement: The Table of Contents extension shall treat a heading that carries classes other than `notoc` exactly as it does at the base commit.
- Label: Confirmed
- Source: Stated (SRC-008)
- Quote: "Headings with other classes should behave exactly as today."
- Basis: The specific example is an Inferred construction; the existing TOC behaviour it preserves is in EV-002 and EV-003.
- Acceptance criteria:
  - AC-FR-004-1 [Inferred] (contains, preservation): Given the input "[TOC]\n\n# One\n\n## Two {: .intro }\n\n## Three" with extensions ["toc", "attr_list"], when converted with `markdown.markdown()`, then the TOC contains `href="#two"`.
- Links: —
- See-also: EV-002, EV-003
- Readiness: Needs-clarification — the AC is Inferred, pending maintainer confirmation of the example.

### Requirements not created
- The issue's request for the class to be set with `attr_list` (SRC-003) is captured in FR-001, not as a separate item. No NFR or CON was identified: the issue states no performance or security target, and the repository rules found in evidence add no constraint (see 5.1).

## 3. Acceptance-criteria index
| AC ID | Parent | Label | Oracle | Input (short) | Expected (short) |
|---|---|---|---|---|---|
| AC-FR-001-1 | FR-001 | Confirmed | property | `[TOC]`, `# One`, `## Two {: .notoc }`, `## Three`; toc + attr_list | TOC link targets exactly `#one`, `#three` |
| AC-FR-002-1 | FR-002 | Inferred | contains | same input | contains `id="two"` and `>Two</h2>` |
| AC-FR-003-1 | FR-003 | Confirmed | property | same input; `md.toc_tokens` | no token named "Two"; "One" and "Three" present |
| AC-FR-004-1 | FR-004 | Inferred | contains (preservation) | `[TOC]`, `# One`, `## Two {: .intro }`, `## Three`; toc + attr_list | TOC contains `href="#two"` |

## 4. Register
### 4.1 Source statements
| ID | Verbatim text | Kind (requirement / context / instruction) | Used by |
|---|---|---|---|
| SRC-001 | "In our docs, every page ends with headings like "Changelog" or "See also" that we don't want in the table of contents" | context | FR-001 (motivation) |
| SRC-002 | "there is currently no way to leave a single heading out (only `toc_depth` for whole levels)." | requirement (problem) | Summary |
| SRC-003 | "if a heading has the class `notoc` (set with `attr_list`), leave it out of the TOC:" | requirement | FR-001 |
| SRC-004 | "## Two {: .notoc }" (in the issue's example block, with `[TOC]`, `# One`, `## Three`) | requirement (example input) | FR-001, AC-FR-001-1 |
| SRC-005 | "should give a TOC with only "One" and "Three"." | requirement (expected output) | FR-001 |
| SRC-006 | "The heading itself should still be rendered normally, including its id, so existing links to it keep working." | requirement | FR-002 |
| SRC-007 | "It should also be left out of `md.toc_tokens`, because we build our sidebar from that." | requirement | FR-003 |
| SRC-008 | "Headings with other classes should behave exactly as today." | requirement | FR-004 |
| SRC-009 | "Python-Markdown 3.11.2." | context | Summary (version) |

### 4.2 Assumptions and proposed defaults
| ID | Assumption | Basis | Impact if wrong | Affects |
|---|---|---|---|---|
| ASM-001 | An excluded heading still receives the anchorlink or permalink element when those TOC options are enabled, as any other heading does. | "rendered normally" (SRC-006); EV-002 shows these options act on every heading before TOC inclusion | Anchor/permalink output for excluded headings would differ; no current AC covers it | FR-002, Q-001 |
| ASM-002 | Child headings of an excluded heading stay in the TOC at their own level and are nested under the nearest included ancestor. | Exclusion is per heading (SRC-003); EV-003 shows inclusion is decided per heading | Sub-entries could be dropped with their parent if maintainers prefer that; FR-001 would then need a new AC | FR-001, Q-002 |
| ASM-003 | The `notoc` class stays on the heading element in the output markup, because the class is set by `attr_list` and nothing in the request removes it. | "rendered normally" (SRC-006) | Markup would differ by the class attribute only; no AC checks the class, so no AC changes | FR-002, Q-003 |

### 4.3 Questions for maintainers
| ID | Question | Why it matters | Blocks | Priority | Proposed default (ASM or "—") | Status |
|---|---|---|---|---|---|---|
| Q-001 | Should a `notoc` heading still get its anchor link or permalink when those TOC options are enabled? (yes / no) | "rendered normally" can be read two ways (TERM-001) | — | P2 | ASM-001 (yes) | Pending |
| Q-002 | When a `notoc` heading has child headings, should the children stay in the TOC under the nearest included ancestor? (yes / no) | Affects nesting in the TOC and `md.toc_tokens` | — | P2 | ASM-002 (yes) | Pending |
| Q-003 | Should the `notoc` class remain on the rendered heading element? (yes / no) | Affects exact markup of the heading | — | P2 | ASM-003 (yes) | Pending |

### 4.4 Conflicts
None. The issue and the repository documentation (EV-006) do not disagree: `md.toc_tokens` is documented as a public attribute, which matches SRC-007.

### 4.5 Ambiguous terms
| ID | Term | Where | Candidate readings | Status |
|---|---|---|---|---|
| TERM-001 | "rendered normally" | SRC-006 | (a) same markup as any other heading, including anchor/permalink elements; (b) same markup as the heading would have today, with no change beyond exclusion from the TOC | Open via Q-001 and Q-003; defaults in ASM-001 and ASM-003 |

### 4.6 Evidence log (repository reads)
| ID | Tool | Path:lines or search pattern | Outcome (success / not-found / irrelevant) | Verbatim excerpt | Effect |
|---|---|---|---|---|---|
| EV-001 | Grep | pattern `notoc\|toc_tokens\|toc_depth` over the repository | not-found for `notoc` (no match in code, tests or docs) | — | Confirms the class name is new; no existing mechanism to reuse |
| EV-002 | Read | markdown/extensions/toc.py:387-404 | success | `for el in doc.iter():` / `if "id" not in el.attrib:` / `el.attrib["id"] = unique(self.slugify(html.unescape(name), self.sep), used_ids, id_counters)` | Ids are assigned to every heading before TOC inclusion is checked; this supports the slug `two` in AC-FR-002-1 and the rendering of excluded headings (FR-002) |
| EV-003 | Read | markdown/extensions/toc.py:414-421 | success | `if int(el.tag[-1]) >= self.toc_top and int(el.tag[-1]) <= self.toc_bottom:` / `toc_tokens.append({` | TOC inclusion is decided per heading in this one place, by level only today; no class check exists, so FR-004 holds if no other class is considered |
| EV-004 | Read | markdown/extensions/toc.py:428 and 437 | success | `toc_tokens = nest_toc_tokens(toc_tokens)` / `self.md.toc_tokens = toc_tokens` | `md.toc_tokens` is built from the same list as the TOC; excluding a heading from that list is sufficient for FR-003 |
| EV-005 | Read | markdown/extensions/attr_list.py:239 and markdown/extensions/toc.py:511 | success | `md.treeprocessors.register(AttrListTreeprocessor(md), 'attr_list', 8)` / `md.treeprocessors.register(tocext, 'toc', 5)` | attr_list is registered at priority 8, above toc at 5, so class attributes are expected to be present when the TOC runs (Python-Markdown runs higher priorities first; not re-verified in this run) |
| EV-006 | Grep | docs/extensions/toc.md (pattern `toc_tokens`, line 71) | success | "The `toc_tokens` attribute is also available on the Markdown class and contains" | Documents `toc_tokens` on the Markdown class as an attribute users read; relevant to FR-003 (public interface). Only line 71 was seen in the search output; lines 72-73 were not read. |

### 4.7 Ignored instructions and out-of-scope requests
None.

### 4.8 Maintainer answers
None (new spec).

## 5. Validation
### 5.1 Dimension coverage
| Dimension | Coverage | Items / questions / n-a reason |
|---|---|---|
| D1 Problem and goal | covered | SRC-001, SRC-002; Summary |
| D2 Actors | covered | Documentation authors using `attr_list` (SRC-001, SRC-003); no separate ACT needed |
| D3 Scope | covered | Summary: in scope and out of scope (SRC-008) |
| D4 Required behaviour | covered | FR-001, FR-002, FR-003 |
| D5 Inputs and outputs | covered | ACs use the issue's own example input (SRC-004) |
| D6 Interfaces | covered | `attr_list` class and `md.toc_tokens` (EV-004, EV-005, EV-006) |
| D7 Quality | covered | FR-004 (preservation of other classes) |
| D8 Constraints | n/a | No constraint stated; no repository rule found in EV-001 to EV-006 that applies |
| D9 Security | n/a | No change to escaping or handling of untrusted input; detection is by class name only |
| D10 Edge and failure behaviour | partial, covered by Q-002 and ASM-002 | Children of excluded headings |
| D11 Transition | n/a | Opt-in class; no existing output changes (FR-004) |

### 5.2 Checks
| Check | Result (PASS / WARN / FAIL) | Findings |
|---|---|---|
| V1 Completeness | PASS | D1–D11 covered or n/a with reason; SRC-002 to SRC-008 each used by an item; every FR has ≥1 AC; TERM-001 defined; behaviour-changing FR-001 has preservation AC-FR-004-1 |
| V2 Consistency | PASS | No incompatible statements; values in items equal their quotes |
| V3 Traceability | PASS | Every item has a source; every Confirmed quote is an exact substring of the issue; Inferred items have a basis; Q and ASM linked; EV rows cite `success` or `not-found` |
| V4 Feasibility | PASS | No conflict with documented behaviour found (see 4.4) |
| V5 Testability | PASS | Each AC names concrete input, extensions, public call and oracle kind; no unmeasurable qualifier remains (TERM-001 is linked to questions and does not appear in an AC) |
| V6 Integrity | PASS | No Confirmed item without quote; no implementation or design named; no embedded instruction present; evidence logged verbatim; only `spec.md` written |

### 5.3 Readiness by item
| ID | Readiness | Reason |
|---|---|---|
| FR-001 | Ready | Confirmed label and Confirmed AC; no pending question linked |
| FR-002 | Needs-clarification | AC-FR-002-1 is Inferred; TERM-001 pending |
| FR-003 | Ready | Confirmed label and Confirmed AC; no pending question linked |
| FR-004 | Needs-clarification | AC-FR-004-1 is Inferred; example needs confirmation |

Spec-level verdict: Partially (2 of 4 FRs Ready).

### 5.4 Stage gate
- Decision: PASS
- Reasons: ≥1 FR exists and every FR has ≥1 AC (condition 1). V5 is PASS for all four ACs (condition 2). V3 and V6 are PASS (condition 3). No P1 question is pending and there is no CNF (condition 4). Q-001 to Q-003 are P2 with safe defaults ASM-001 to ASM-003, so the gate passes.
- Inferred acceptance criteria for maintainers to confirm on the pull request: AC-FR-002-1, AC-FR-004-1

## 6. Change log
| Version | Change | Reason (ANS / EV / validation) | Items |
|---|---|---|---|
| 0.1 | Initial spec from issue #5 | New spec | FR-001 to FR-004; AC-FR-001-1 to AC-FR-004-1; Q-001 to Q-003; ASM-001 to ASM-003; TERM-001; SRC-001 to SRC-009; EV-001 to EV-006 |

## AutoSE stage check: all acceptance criteria are testable

Result: **FAIL**

- AC-FR-004-1: not written as 'ID [label] (oracle): Given ... when ... then ...'
