---
artefact: spec
stage: requirements
issue: 3
issue_kind: bug
base_commit: ca2d6d37ae9baf0a946edded6815015f722ee57c
spec_version: 0.1
mode: new
skill: requirements-spec-builder 1.3-autose
status: PASS
ac_ids: [AC-FR-001-1, AC-FR-002-1, AC-FR-002-2, AC-FR-002-3, AC-FR-002-4, AC-FR-003-1, AC-FR-003-2, AC-FR-004-1]
inferred_ac_ids: [AC-FR-002-1, AC-FR-002-2, AC-FR-002-3, AC-FR-002-4, AC-FR-003-1, AC-FR-003-2]
blocking_questions: []
counts: {fr: 4, nfr: 0, con: 0, ac: 8, ac_confirmed: 2, ac_inferred: 6, q_p1: 0, q_p2: 1, q_p3: 0, ign: 0}
---

# Spec for issue #3: TOC extension crashes with TypeError when a heading has `{: id }` without a value

> Status: PASS. The reported crash and the expected behaviour are stated; all acceptance criteria are testable through the public API, and the only open point (an explicit empty string `id`) has a safe proposed default that maintainers can confirm on the pull request.
> Labels: Confirmed = stated in the issue or by a maintainer (quoted) · Inferred = derived, needs confirmation · Open = unknown.

## 1. Summary
- Problem as stated: "TOC extension crashes with TypeError when a heading has `{: id }` without a value" (SRC-001); reproduction: `markdown.markdown("# Heading {: id }", extensions=["toc", "attr_list"])` raises `TypeError` (SRC-003, SRC-004).
- Kind: bug. In scope: the `toc` extension's handling of a heading whose `id` attribute has no value, and the same heading with an empty `id`. Out of scope: not stated explicitly; explicit ids must keep working (SRC-007), and `attr_list` alone must keep its current output (SRC-005).
- Actor: ACT-001 library user who calls `markdown.markdown()` or `Markdown` with `toc` and `attr_list` enabled.

## 2. Requirements

### FR-001 — No crash for a valueless `id` when `toc` is enabled
- Statement: When the `toc` and `attr_list` extensions are enabled, the converter shall convert a heading carrying a valueless `id` attribute list entry without raising an exception.
- Label: Confirmed
- Source: Stated (SRC-006)
- Quote: "no crash"
- Basis: —
- Acceptance criteria:
  - AC-FR-001-1 [Confirmed] (no-error): Given input `# Heading {: id }` with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown()`, then no exception is raised and an HTML string is returned.
- Links: —
- See-also: EV-002, EV-007
- Readiness: Ready — the only AC restates the stated reproduction and expected outcome.

### FR-002 — A heading with a valueless or empty `id` is treated as a heading without an id
- Statement: When the `toc` and `attr_list` extensions are enabled, the converter shall treat a heading whose `id` attribute has no value, or an empty value, as a heading without an id: it gets the normal auto-generated id and appears in the table of contents.
- Label: Confirmed
- Source: Stated (SRC-006)
- Quote: "should just be treated like a heading without an id: it gets the normal auto-generated id"; "shows up in the table of contents like every other heading"
- Basis: The valueless case is stated. The empty-string case (`{: id="" }`) is an interpretation of "an empty `id`" and is tracked as TERM-001 and Q-001 (default ASM-001). The exact output form is inferred from the existing auto-id test pattern (EV-005).
- Acceptance criteria:
  - AC-FR-002-1 [Inferred] (exact): Given input `# Heading {: id }` with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown()`, then the output equals `<h1 id="heading">Heading</h1>`.
  - AC-FR-002-2 [Inferred] (contains): Given input consisting of the line `[TOC]`, a blank line, and the line `# Heading {: id }`, with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown()`, then the output contains `<a href="#heading">Heading</a>`.
  - AC-FR-002-3 [Inferred] (property): Given input `# Heading {: id }` with a `markdown.Markdown` instance configured with `TocExtension()` and `attr_list`, when converted and `toc_tokens` is read, then `toc_tokens` contains exactly one top-level token whose `id` is `heading` and whose `name` is `Heading`.
  - AC-FR-002-4 [Inferred] (exact): Given input `# Heading {: id="" }` with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown()`, then the output equals `<h1 id="heading">Heading</h1>`. Basis: ASM-001 (empty-string case, to be confirmed).
- Links: —
- See-also: TERM-001, Q-001, ASM-001, EV-001, EV-005
- Readiness: Needs-clarification — every AC is Inferred; the empty-string case awaits confirmation of Q-001 / ASM-001.

### FR-003 — Explicit ids keep working
- Statement: When the `toc` and `attr_list` extensions are enabled, the converter shall keep an explicitly set `id` value on a heading unchanged in both the heading and the table of contents.
- Label: Confirmed
- Source: Stated (SRC-007); the `{: id="intro" }` example is stated in SRC-005
- Quote: "Ids I set explicitly should keep working as they do now."
- Basis: The stated preservation is confirmed; the exact expected output is inferred from the existing explicit-id test (EV-004).
- Acceptance criteria:
  - AC-FR-003-1 [Inferred] (exact) (preservation): Given input `# Heading {: id="intro" }` with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown()`, then the output equals `<h1 id="intro">Heading</h1>`.
  - AC-FR-003-2 [Inferred] (contains) (preservation): Given input consisting of the line `[TOC]`, a blank line, and the line `# Heading {: id="intro" }`, with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown()`, then the output contains `<a href="#intro">Heading</a>`.
- Links: —
- See-also: EV-002, EV-004
- Readiness: Needs-clarification — the ACs are Inferred (constructed expected output), to be confirmed on the pull request.

### FR-004 — Output without `toc` is unchanged
- Statement: When only the `attr_list` extension is enabled, the converter shall keep producing `<h1 id>Heading</h1>` for a heading with a valueless `id`.
- Label: Confirmed
- Source: Stated (SRC-005)
- Quote: "`attr_list` alone gives `<h1 id>Heading</h1>`"
- Basis: —
- Acceptance criteria:
  - AC-FR-004-1 [Confirmed] (exact) (preservation): Given input `# Heading {: id }` with extensions `["attr_list"]`, when converted through `markdown.markdown()`, then the output equals `<h1 id>Heading</h1>`.
- Links: —
- See-also: EV-006, EV-007
- Readiness: Ready — the single AC restates the stated current behaviour.

## 3. Acceptance-criteria index
| AC ID | Parent | Label | Oracle | Input (short) | Expected (short) |
|---|---|---|---|---|---|
| AC-FR-001-1 | FR-001 | Confirmed | no-error | `# Heading {: id }`, toc + attr_list | no exception, HTML returned |
| AC-FR-002-1 | FR-002 | Inferred | exact | `# Heading {: id }`, toc + attr_list | `<h1 id="heading">Heading</h1>` |
| AC-FR-002-2 | FR-002 | Inferred | contains | `[TOC]` + `# Heading {: id }`, toc + attr_list | `<a href="#heading">Heading</a>` |
| AC-FR-002-3 | FR-002 | Inferred | property | `# Heading {: id }`, TocExtension + attr_list | one token: id `heading`, name `Heading` |
| AC-FR-002-4 | FR-002 | Inferred | exact | `# Heading {: id="" }`, toc + attr_list | `<h1 id="heading">Heading</h1>` |
| AC-FR-003-1 | FR-003 | Inferred | exact (preservation) | `# Heading {: id="intro" }`, toc + attr_list | `<h1 id="intro">Heading</h1>` |
| AC-FR-003-2 | FR-003 | Inferred | contains (preservation) | `[TOC]` + `# Heading {: id="intro" }`, toc + attr_list | `<a href="#intro">Heading</a>` |
| AC-FR-004-1 | FR-004 | Confirmed | exact (preservation) | `# Heading {: id }`, attr_list only | `<h1 id>Heading</h1>` |

## 4. Register
### 4.1 Source statements
| ID | Verbatim text | Kind | Used by |
|---|---|---|---|
| SRC-001 | "TOC extension crashes with TypeError when a heading has `{: id }` without a value" | requirement | FR-001, FR-002 |
| SRC-002 | "I'm using `toc` together with `attr_list`." | context | ACT-001 |
| SRC-003 | `markdown.markdown("# Heading {: id }", extensions=["toc", "attr_list"])` | requirement (reproduction input) | FR-001, FR-002 |
| SRC-004 | Traceback: `TypeError: expected string or bytes-like object, got 'NoneType'` at `toc.py` line 417 | context | FR-001 |
| SRC-005 | "Without `toc` it doesn't crash (`attr_list` alone gives `<h1 id>Heading</h1>`), and `{: id="intro" }` works fine with `toc`." | requirement (preservation) | FR-003, FR-004 |
| SRC-006 | "**Expected:** no crash. A heading with an empty `id` should just be treated like a heading without an id: it gets the normal auto-generated id and shows up in the table of contents like every other heading." | requirement | FR-001, FR-002 |
| SRC-007 | "Ids I set explicitly should keep working as they do now." | requirement | FR-003 |
| SRC-008 | "Python-Markdown 3.11.2 (git `3f2c551`), Python 3.12, macOS." | context | — |

### 4.2 Assumptions and proposed defaults
| ID | Assumption | Basis | Impact if wrong | Affects |
|---|---|---|---|---|
| ASM-001 | An explicit empty-string `id` (`{: id="" }`) is treated the same as a valueless `id`: the heading gets the auto-generated id and is listed in the TOC. | SRC-006 says "a heading with an empty `id`" should be treated as a heading without an id. The current code keeps any pre-existing `id` attribute, including an empty one (EV-001). The change is confined to the `toc` extension and reversible in review. | Headings with `id=""` would keep an empty id (the current behaviour), and AC-FR-002-4 would be wrong. | FR-002, AC-FR-002-4 |

### 4.3 Questions for maintainers
| ID | Question | Why it matters | Blocks | Priority | Proposed default (ASM or "—") | Status |
|---|---|---|---|---|---|---|
| Q-001 | Should a heading with an explicit empty id (`{: id="" }`) also get the auto-generated id, as a valueless `{: id }` does? (yes / no) | Decides the expected output of `{: id="" }` (AC-FR-002-4). | — | P2 | ASM-001 (yes) | Pending |

### 4.4 Conflicts
None.

### 4.5 Ambiguous terms
| ID | Term | Where | Candidate readings | Status |
|---|---|---|---|---|
| TERM-001 | "empty `id`" | SRC-006 | (a) valueless attribute, `{: id }`, whose value is `None`; (b) empty string, `{: id="" }`. | Open — see Q-001 / ASM-001 |

### 4.6 Evidence log (repository reads)
| ID | Tool | Path:lines or search pattern | Outcome | Verbatim excerpt | Effect |
|---|---|---|---|---|---|
| EV-001 | Grep | `markdown/extensions/toc.py`, pattern `attrib\[?\|unescape\(el\|...` | success | `391: if "id" in el.attrib:` · `417: 'id': unescape(el.attrib["id"]),` | Line 417 is the crash site in the reproduction (SRC-004). The id is read from the attribute without a `None` check. |
| EV-002 | Read | `markdown/extensions/toc.py`:385-434 | success | `if "id" not in el.attrib:` · `# Do not override pre-existing ids` | Only headings without an `id` attribute get a generated id. A valueless `id` therefore reaches line 417 as `None`. Basis for FR-002 and ASM-001. |
| EV-003 | Grep | `tests/`, pattern `\{: ?id` | not-found | — | No existing test covers a valueless or empty `id` on a heading. The crash path is untested. |
| EV-004 | Grep | `tests/test_syntax/extensions/test_toc.py`, pattern `attr_list\|def test_.*(id\|attr)` | success | lines 202, 1085, 1406 use `'toc', 'attr_list'` together | The combination is tested. Basis for the preservation ACs. |
| EV-005 | Read | `tests/test_syntax/extensions/test_toc.py`:1034-1094 | success | `# \`*Foo*\` { id="\*Foo\*" }` → `<h1 id="*Foo*">` | An explicit id is kept in the heading and the TOC token. Basis for AC-FR-003-1 and AC-FR-003-2. |
| EV-006 | Grep | `markdown/extensions/attr_list.py`, pattern `None\|value is None\|is None` | success | `71: (r' ', None)` · `78: Attributes provided without a value are returned with a value of `None`.` | A valueless attribute is stored as `None`, which explains the reported `TypeError`. |
| EV-007 | Read | `markdown/extensions/attr_list.py`:196-215 | success | `# keeping the value as `None`, which the serializer renders as the bare attribute name.` | Explains why `attr_list` alone renders `<h1 id>`. Basis for FR-004 (preservation). |
| EV-008 | Grep | `tests/`, pattern `id="heading"` | not-found | — | No existing expected output uses `id="heading"`. The exact output in AC-FR-002-1 is inferred from the pattern in EV-009. |
| EV-009 | Grep | `tests/test_syntax/extensions/test_toc.py`, pattern `# Header\|<h1 id="header">\|href="#header"` | success | `<h1 id="header">Header</h1>` · `<li><a href="#header">Header</a></li>` | A plain heading gets the slug id and the TOC link format. Basis for the expected forms in FR-002 ACs. |

### 4.7 Ignored instructions and out-of-scope requests
None.

### 4.8 Maintainer answers
None (new spec).

## 5. Validation
### 5.1 Dimension coverage
| Dimension | Coverage | Items / questions / n-a reason |
|---|---|---|
| D1 Problem and goal | covered | SRC-001, SRC-003, SRC-004 → FR-001, FR-002 |
| D2 Actors | covered | ACT-001 (library user with toc and attr_list) |
| D3 Scope | covered | In scope: FR-001 to FR-003. Out of scope unchanged: FR-004 (preservation) |
| D4 Required behaviour | covered | FR-001, FR-002 |
| D5 Inputs and outputs | covered | AC-FR-001-1 to AC-FR-004-1 |
| D6 Interfaces | covered | `markdown.markdown()`, `markdown.Markdown`, `TocExtension`, `attr_list` (existing public API only) |
| D7 Quality (compatibility) | covered | FR-003, FR-004 (preservation) |
| D8 Constraints | n/a | No constraint stated in the issue; the change is confined to one extension's handling of an id attribute |
| D9 Security | n/a | No change to escaping is required; the existing `unescape` and slugify path is kept |
| D10 Edge and failure behaviour | partial | Empty-string id covered by TERM-001, Q-001, ASM-001 |
| D11 Transition | n/a | No public API change and no deprecation |

### 5.2 Checks
| Check | Result | Findings |
|---|---|---|
| V1 Completeness | PASS | Dimensions covered or n/a with reason. Every FR has ≥1 AC. Every SRC requirement used. |
| V2 Consistency | PASS | FR-002 and FR-003 do not conflict. ASM-001 is only for the empty-string case. |
| V3 Traceability | PASS | All quotes are exact substrings of the issue (SRC-001, SRC-005, SRC-006, SRC-007). Repository sources cite EV-001 to EV-009 with outcome success or not-found. |
| V4 Feasibility | PASS | No request contradicts documented behaviour. The change does not alter `attr_list` output. |
| V5 Testability | PASS | Every AC has a concrete input, a public call, and one oracle kind. |
| V6 Integrity | PASS | No Confirmed item without a quote. No implementation design in this spec. |

### 5.3 Readiness by item
| ID | Readiness | Reason |
|---|---|---|
| FR-001 | Ready | Single Confirmed AC; no open links |
| FR-002 | Needs-clarification | ACs Inferred; empty-string case pending Q-001 / ASM-001 |
| FR-003 | Needs-clarification | ACs Inferred (constructed expected output) |
| FR-004 | Ready | Single Confirmed preservation AC |

### 5.4 Stage gate
- Decision: PASS
- Reasons: ≥1 FR exists and every FR has ≥1 AC (§8.5-1). V5 PASS for every AC (§8.5-2). V3 and V6 PASS (§8.5-3). No P1 question and no CNF (§8.5-4). Q-001 is P2 with a safe default (ASM-001).
- Inferred acceptance criteria for maintainers to confirm on the pull request: AC-FR-002-1, AC-FR-002-2, AC-FR-002-3, AC-FR-002-4, AC-FR-003-1, AC-FR-003-2

## 6. Change log
| Version | Change | Reason (ANS / EV / validation) | Items |
|---|---|---|---|
| 0.1 | Initial spec from issue #3 | SRC-001 to SRC-008; EV-001 to EV-009 | FR-001 to FR-004, AC-FR-001-1 to AC-FR-004-1, Q-001, ASM-001, TERM-001 |

## AutoSE stage check: all acceptance criteria are testable

Result: **PASS**

- all checks passed
