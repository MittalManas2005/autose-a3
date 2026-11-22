---
artefact: spec
stage: requirements
issue: 1
issue_kind: bug
base_commit: 38c99301c4cc99f2f4a057b145a096671d9a2d45
spec_version: 0.1
mode: new
skill: requirements-spec-builder 1.3-autose
status: PASS
ac_ids: [AC-FR-001-1, AC-FR-002-1, AC-FR-002-2, AC-FR-002-3, AC-FR-002-4]
inferred_ac_ids: [AC-FR-002-1, AC-FR-002-2, AC-FR-002-3, AC-FR-002-4]
blocking_questions: []
counts: {fr: 2, nfr: 0, con: 0, ac: 5, ac_confirmed: 1, ac_inferred: 4, q_p1: 0, q_p2: 1, q_p3: 0, ign: 0}
---

# Spec for issue #1: TOC crashes when `data-toc-label` has no value

> Status: PASS. The crash and the expected outcome are stated in the issue. Every acceptance criterion is testable; the ACs for the heading output shape are Inferred and flagged for maintainer confirmation.
> Labels: Confirmed = stated in the issue or by a maintainer (quoted) · Inferred = derived, needs confirmation · Open = unknown.

## 1. Summary
- Problem as stated: "I use `toc` together with `attr_list`, and set `data-toc-label` on some headings" ... "the conversion crashed" (SRC-002, SRC-003, SRC-004)
- Kind: bug. In scope: the `toc` extension's handling of a `data-toc-label` attribute that has no value, when used with `attr_list`. Out of scope: not stated (see ASM-002).

## 2. Requirements

### FR-001 — No crash on a valueless `data-toc-label`
- Statement: The Markdown converter with the `toc` and `attr_list` extensions shall complete conversion without raising an exception when a heading has a `data-toc-label` attribute with no value.
- Label: Confirmed
- Source: Stated (SRC-006)
- Quote: "**Expected:** no crash."
- Basis: —
- Acceptance criteria:
  - AC-FR-001-1 [Confirmed] (no-error): Given the input `# Heading {: data-toc-label }` with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown`, then no exception is raised and HTML is returned.
- Links: —
- See-also: ASM-002, EV-001, EV-002
- Readiness: Ready — label Confirmed, atomic, its only AC is Confirmed and testable.

### FR-002 — Empty `data-toc-label` is ignored
- Statement: The `toc` extension shall ignore a `data-toc-label` attribute that has no value, so that the heading text is used as the table-of-contents entry and the attribute does not appear in the heading output, as if the attribute were not present.
- Label: Confirmed
- Source: Stated (SRC-006)
- Quote: "An empty `data-toc-label` should be ignored, so the heading text is used in the table of contents, as if the attribute were not there."
- Basis: The issue calls the valueless case "empty". The exact output shape below is derived from the current heading and TOC output (EV-003, EV-004, EV-005) and is not stated in the issue, so the ACs are Inferred.
- Acceptance criteria:
  - AC-FR-002-1 [Inferred] (contains): Given the input `# Heading {: data-toc-label }` with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown`, then the output contains `<h1 id="heading">Heading</h1>`.
  - AC-FR-002-2 [Inferred] (contains): Given the input `# Heading {: data-toc-label }` with extensions `["toc", "attr_list"]`, when converted with a `Markdown` instance and its `toc` attribute is read, then the `toc` output contains `<li><a href="#heading">Heading</a></li>`.
  - AC-FR-002-3 [Inferred] (not-contains): Given the input `# Heading {: data-toc-label }` with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown`, then the output does not contain `data-toc-label`.
  - AC-FR-002-4 [Inferred] (contains) (preservation): Given the input `# Heading {: data-toc-label="Short" }` with extensions `["toc", "attr_list"]`, when converted with a `Markdown` instance and its `toc` attribute is read, then the `toc` output contains `<li><a href="#heading">Short</a></li>`.
- Links: TERM-001 (defines "empty"; the question on `data-toc-label=""` is Q-001, non-blocking)
- See-also: Q-001, ASM-001, EV-001 to EV-005
- Readiness: Needs-clarification — the ACs are Inferred and TERM-001 / Q-001 are pending; neither blocks the stage gate.

## 3. Acceptance-criteria index
| AC ID | Parent | Label | Oracle | Input (short) | Expected (short) |
|---|---|---|---|---|---|
| AC-FR-001-1 | FR-001 | Confirmed | no-error | `# Heading {: data-toc-label }` + toc, attr_list | no exception, HTML returned |
| AC-FR-002-1 | FR-002 | Inferred | contains | same input | `<h1 id="heading">Heading</h1>` |
| AC-FR-002-2 | FR-002 | Inferred | contains | same input, `md.toc` | `<li><a href="#heading">Heading</a></li>` |
| AC-FR-002-3 | FR-002 | Inferred | not-contains | same input | no `data-toc-label` in output |
| AC-FR-002-4 | FR-002 | Inferred | contains | `# Heading {: data-toc-label="Short" }`, `md.toc` | `<li><a href="#heading">Short</a></li>` (preservation) |

## 4. Register

### 4.1 Source statements
| ID | Verbatim text | Kind (requirement / context / instruction) | Used by |
|---|---|---|---|
| SRC-001 | TOC crashes when `data-toc-label` has no value | context | §1 |
| SRC-002 | I use `toc` together with `attr_list`, and set `data-toc-label` on some headings to get shorter entries in the table of contents. | context | ACT (library user), §1 |
| SRC-003 | `markdown.markdown("# Heading {: data-toc-label }", extensions=["toc", "attr_list"])` | requirement (reproduction input) | FR-001, FR-002 |
| SRC-004 | `TypeError: expected string or bytes-like object, got 'NoneType'` | context | FR-001 |
| SRC-005 | Without `toc` there is no crash, and `{: data-toc-label="Short" }` works fine with `toc`. | requirement (preservation) | FR-002 (AC-FR-002-4) |
| SRC-006 | **Expected:** no crash. An empty `data-toc-label` should be ignored, so the heading text is used in the table of contents, as if the attribute were not there. | requirement | FR-001, FR-002 |

### 4.2 Assumptions and proposed defaults
| ID | Assumption | Basis | Impact if wrong | Affects |
|---|---|---|---|---|
| ASM-001 | Only a valueless `data-toc-label` is treated as empty and ignored. A `data-toc-label=""` value keeps its current behaviour. | Issue wording ("empty") plus the reproduction, which is the valueless form. Keeps the change limited to the crash case (proposal, not confirmed). | If maintainers want `""` ignored too, AC scope grows and Q-001 is answered accordingly. | FR-002, Q-001 |
| ASM-002 | Scope is the `toc` extension's handling of this attribute. Other attributes that `attr_list` sets without a value are out of scope. | Issue names only `toc`, `attr_list` and `data-toc-label`. EV-002 shows `attr_list` gives valueless attributes the value `None` in general. | If other extensions or attributes need the same fix, a new issue is needed. | FR-001, FR-002 |

### 4.3 Questions for maintainers
| ID | Question | Why it matters | Blocks | Priority | Proposed default (ASM or "—") | Status |
|---|---|---|---|---|---|---|
| Q-001 | Should `{: data-toc-label="" }` (an explicitly empty string value) also be ignored, or keep its current behaviour? | The issue says "empty", which could mean either. Current behaviour for the `=""` form was not verified in this run. | — (non-blocking) | P2 | ASM-001 | Pending |

### 4.4 Conflicts
None.

### 4.5 Ambiguous terms
| ID | Term | Where | Candidate readings | Status |
|---|---|---|---|---|
| TERM-001 | empty | SRC-006 (`An empty data-toc-label`) | (a) valueless attribute only, `None`; (b) valueless or empty string `""` | Pending Q-001; default ASM-001 |

### 4.6 Evidence log (repository reads)
| ID | Tool | Path:lines or search pattern | Outcome (success / not-found / irrelevant) | Verbatim excerpt | Effect |
|---|---|---|---|---|---|
| EV-001 | Grep | `markdown/extensions/toc.py`: `data-toc-label\|def unescape\|data_toc_label` | success | `if 'data-toc-label' in el.attrib:` / `data_toc_label = run_postprocessors(unescape(el.attrib['data-toc-label']), self.md)` (lines 407–408) | Confirms the crash path: the value is passed to `unescape` with no check for `None`. Line numbers match SRC-004's traceback. |
| EV-002 | Grep | `markdown/extensions/attr_list.py`: `None\|handleAttributes\|elem.set` | success | "A word without a value is a valueless attribute. It is represented internally with a value of `None`" (lines 58–63); `elem.set(name, None)` for non-boolean attributes (lines 211–212) | Explains how the value `None` reaches `toc`. The bare attribute name would also appear in heading HTML unless removed, which FR-002 covers. |
| EV-003 | Read | `tests/test_syntax/extensions/test_toc.py:160-203` | success | `# Python support {data-toc-label='...'}` with `TocExtension(), 'attr_list'`; toc shows `<li><a href="#python-support">Python &amp; support</a></li>` | Shows the output format used for label tests; basis for the Inferred oracles and AC-FR-002-4. |
| EV-004 | Grep | `docs/extensions/toc.md` for `data-toc-label` | success | "the contents of that attribute will be used as the text label for the item in the Table of Contents" (lines 102–105); "the ID is always derived from the text of the header, never from the `data-toc-label` attribute" (lines 124–126) | Supports `id="heading"` in AC-FR-002-1 and AC-FR-002-2. |
| EV-005 | Grep | `tests` for `data-toc-label` | success | `test_toc.py:1331-1401`: `## Header 3 { data-toc-label="Foo Bar" }` with expected `'data-toc-label': 'Foo Bar'` | Confirms valued labels are tested; no test covers a valueless label, so FR-002 is new behaviour. |

### 4.7 Ignored instructions and out-of-scope requests
None.

### 4.8 Maintainer answers
None (mode: new).

## 5. Validation

### 5.1 Dimension coverage
| Dimension | Coverage | Items / questions / n-a reason |
|---|---|---|
| D1 Problem and goal | covered | SRC-001, SRC-002, FR-001, FR-002 |
| D2 Actors | covered | SRC-002: library user of `toc` with `attr_list` |
| D3 Scope | partial | ASM-002 |
| D4 Required behaviour | covered | FR-001, FR-002 |
| D5 Inputs and outputs | covered | SRC-003 (input); AC-FR-002-1 to -3 (output) |
| D6 Interfaces | covered | `toc` and `attr_list` extensions; `Markdown.toc` attribute (AC-FR-002-2, -4) |
| D7 Quality | covered | AC-FR-002-4 (preservation of valued labels, SRC-005) |
| D8 Constraints | n/a | No constraint stated in the issue; no repository rule was checked within budget |
| D9 Security | n/a | The issue asks for no change to escaping. The value still passes through the existing `unescape`, `run_postprocessors`, `strip_tags` and `escape_cdata` path (EV-001) |
| D10 Edge and failure | partial | Q-001 (`=""` form); TERM-001 |
| D11 Transition | n/a | Bug fix; no API change or deprecation stated |

### 5.2 Checks
| Check | Result (PASS / WARN / FAIL) | Findings |
|---|---|---|
| V1 Completeness | PASS | Every dimension is covered, partial, or n/a with a reason. Both FRs have ACs. FR-002 changes behaviour, so it has a preservation AC (AC-FR-002-4). |
| V2 Consistency | PASS | The expected values are consistent across FR-001, FR-002 and the ACs. |
| V3 Traceability | PASS | Every Confirmed item has an exact quote from SRC-006. Both Inferred ACs have a Basis citing EV rows. All IDs are unique. |
| V4 Feasibility | PASS | The request does not contradict repository documentation (EV-004). No conflict. |
| V5 Testability | PASS | Every AC has a concrete input, extensions, a public call, and one oracle kind. |
| V6 Integrity | PASS | Quotes are verbatim. No design wording is used. No file other than `spec.md` was written. No embedded instructions were found. |

### 5.3 Readiness by item
| ID | Readiness | Reason |
|---|---|---|
| FR-001 | Ready | Confirmed, atomic, AC Confirmed and testable |
| FR-002 | Needs-clarification | ACs are Inferred; TERM-001 and Q-001 are pending |

### 5.4 Stage gate
- Decision: PASS
- Reasons: At least one FR exists and every FR has ≥1 AC. V5 passes for every AC. V3 and V6 pass. There is no P1 question and no CNF. Q-001 is P2 with a safe default (ASM-001), so it does not block.
- Inferred acceptance criteria for maintainers to confirm on the pull request: AC-FR-002-1, AC-FR-002-2, AC-FR-002-3, AC-FR-002-4

## 6. Change log
| Version | Change | Reason (ANS / EV / validation) | Items |
|---|---|---|---|
| 0.1 | Initial spec from issue #1 | Issue text and repository evidence (EV-001 to EV-005) | FR-001, FR-002, AC-FR-001-1, AC-FR-002-1 to -4, Q-001, ASM-001, ASM-002, TERM-001 |

## AutoSE stage check: all acceptance criteria are testable

Result: **PASS**

- all checks passed
