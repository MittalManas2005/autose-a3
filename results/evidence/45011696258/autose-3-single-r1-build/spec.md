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
ac_ids: [AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-002-1, AC-FR-003-1]
inferred_ac_ids: [AC-FR-001-2, AC-FR-001-3, AC-FR-002-1, AC-FR-003-1]
blocking_questions: []
counts: {fr: 3, nfr: 0, con: 0, ac: 5, ac_confirmed: 1, ac_inferred: 4, q_p1: 0, q_p2: 1, q_p3: 0, ign: 0}
---

# Spec for issue #3: TOC extension crashes with TypeError when a heading has `{: id }` without a value

> Status: PASS. The crash is a stated defect with a reproducer; every requirement has a testable acceptance criterion, and the exact id values in the oracles are Inferred from the stated rule (allowed by §8.5).
> Labels: Confirmed = stated in the issue or by a maintainer (quoted) · Inferred = derived, needs confirmation · Open = unknown.

## 1. Summary
- Problem as stated: "markdown.markdown("# Heading {: id }", extensions=["toc", "attr_list"])" raises "TypeError: expected string or bytes-like object, got 'NoneType'" (SRC-001, SRC-002)
- Kind: bug. In scope: the `toc` extension's handling of heading `id` attributes that have no value. Out of scope: other extensions; the attr_list syntax itself (not stated, no change requested).

## 2. Requirements
### FR-001 — No crash for a valueless heading id; heading gets the generated id
- Statement: When the `toc` extension processes a heading whose `id` attribute has no value (as produced by `{: id }` through `attr_list`), the converter shall not raise an exception and shall assign the normal auto-generated id to that heading.
- Label: Confirmed
- Source: Stated (SRC-003, SRC-004)
- Quote: "A heading with an empty `id` should just be treated like a heading without an id: it gets the normal auto-generated id"
- Basis: The no-crash part is stated directly. The exact generated value (`heading`) and the TOC link form are Inferred from the repository's existing slug rules (EV-002, EV-005).
- Acceptance criteria:
  - AC-FR-001-1 [Confirmed] (no-error): Given `# Heading {: id }` with extensions `["toc", "attr_list"]`, when `markdown.markdown` is called, then no exception is raised and HTML is returned.
  - AC-FR-001-2 [Inferred] (contains): Given `# Heading {: id }` with extensions `["toc", "attr_list"]`, when `markdown.markdown` is called, then the output contains `<h1 id="heading">Heading</h1>`.
  - AC-FR-001-3 [Inferred] (contains): Given `# Heading {: id }` with extensions `["toc", "attr_list"]`, when `markdown.markdown` is called, then the output contains `<a href="#heading">Heading</a>` inside the table of contents.
- Links: —
- See-also: ASM-001, EV-001, EV-002, EV-003
- Readiness: Needs-clarification — the exact id and TOC oracle values are Inferred, pending confirmation on the pull request

### FR-002 — Explicit id values keep working
- Statement: When a heading has an explicit non-empty `id` set through `attr_list`, the converter shall keep that value unchanged in the heading and the table of contents.
- Label: Confirmed
- Source: Stated (SRC-005)
- Quote: "Ids I set explicitly should keep working as they do now."
- Basis: The stated preservation requirement. The oracle `<h1 id="intro">` is Inferred from the issue's own example `{: id="intro" }` (SRC-006).
- Acceptance criteria:
  - AC-FR-002-1 [Inferred] (contains) (preservation): Given `# Heading {: id="intro" }` with extensions `["toc", "attr_list"]`, when `markdown.markdown` is called, then the output contains `<h1 id="intro">Heading</h1>`.
- Links: —
- See-also: EV-003
- Readiness: Needs-clarification — the oracle is Inferred

### FR-003 — Empty-string id is treated as a missing id
- Statement: When a heading's `id` attribute is an empty string (for example from `{: id="" }`), the `toc` extension shall treat it as a heading without an id and assign the normal auto-generated id.
- Label: Inferred
- Source: Stated (SRC-003) — applied by agent inference to the explicit empty-string form
- Quote: —
- Basis: The issue says "A heading with an empty `id`" should be treated like one without an id. The issue's reproducer is a valueless id (`None`), not `id=""`. Whether `id=""` is covered is not stated; the proposed default ASM-001 covers it, and Q-001 asks maintainers to confirm.
- Acceptance criteria:
  - AC-FR-003-1 [Inferred] (contains): Given `# Heading {: id="" }` with extensions `["toc", "attr_list"]`, when `markdown.markdown` is called, then the output contains `<h1 id="heading">Heading</h1>`.
- Links: Q-001, ASM-001
- See-also: EV-003
- Readiness: Needs-clarification — depends on Q-001 and ASM-001

## 3. Acceptance-criteria index
| AC ID | Parent | Label | Oracle | Input (short) | Expected (short) |
|---|---|---|---|---|---|
| AC-FR-001-1 | FR-001 | Confirmed | no-error | `# Heading {: id }`, toc+attr_list | no exception, HTML returned |
| AC-FR-001-2 | FR-001 | Inferred | contains | `# Heading {: id }`, toc+attr_list | `<h1 id="heading">Heading</h1>` |
| AC-FR-001-3 | FR-001 | Inferred | contains | `# Heading {: id }`, toc+attr_list | `<a href="#heading">Heading</a>` in TOC |
| AC-FR-002-1 | FR-002 | Inferred | contains | `# Heading {: id="intro" }`, toc+attr_list | `<h1 id="intro">Heading</h1>` |
| AC-FR-003-1 | FR-003 | Inferred | contains | `# Heading {: id="" }`, toc+attr_list | `<h1 id="heading">Heading</h1>` |

## 4. Register
### 4.1 Source statements
| ID | Verbatim text | Kind | Used by |
|---|---|---|---|
| SRC-001 | "I'm using `toc` together with `attr_list`. While drafting a document I left an attribute list on a heading with just `id` (I meant to fill in the value later), and the whole conversion blew up:" | context | FR-001 |
| SRC-002 | "TypeError: expected string or bytes-like object, got 'NoneType'" | requirement (defect) | FR-001 |
| SRC-003 | "**Expected:** no crash. A heading with an empty `id` should just be treated like a heading without an id: it gets the normal auto-generated id and shows up in the table of contents like every other heading." | requirement | FR-001, FR-003 |
| SRC-004 | "shows up in the table of contents like every other heading" | requirement | FR-001 |
| SRC-005 | "Ids I set explicitly should keep working as they do now." | requirement | FR-002 |
| SRC-006 | "`{: id=\"intro\" }` works fine with `toc`." | context | FR-002 |

### 4.2 Assumptions and proposed defaults
| ID | Assumption | Basis | Impact if wrong | Affects |
|---|---|---|---|---|
| ASM-001 | An explicit empty-string id (`id=""`) is treated like a missing id and gets the generated id. | Issue wording "empty `id`" (SRC-003). Changing it only affects the empty-value case, which the issue already calls broken for TOC. Reversible in review. | Explicit `id=""` keeps its current output (`<h1 id="">`), and FR-003 is dropped. | FR-003, AC-FR-003-1 |

### 4.3 Questions for maintainers
| ID | Question | Why it matters | Blocks | Priority | Proposed default (ASM or "—") | Status |
|---|---|---|---|---|---|---|
| Q-001 | Should an explicit empty id (`{: id="" }`) also be replaced by the generated id, as the valueless form `{: id }` is? | The issue only reproduces the valueless form. | — | P2 | ASM-001 | Pending |

### 4.4 Conflicts
None.

### 4.5 Ambiguous terms
| ID | Term | Where | Candidate readings | Status |
|---|---|---|---|---|
| TERM-001 | "empty `id`" | SRC-003 | (a) valueless (`None`), as in the reproducer; (b) valueless or `""`. | Resolved for (a) by the reproducer; (b) covered by ASM-001 / Q-001 |

### 4.6 Evidence log (repository reads)
| ID | Tool | Path:lines or search pattern | Outcome | Verbatim excerpt | Effect |
|---|---|---|---|---|---|
| EV-001 | Grep | `docs/changelog.md` for `Unreleased` | success | "## [Unreleased]" / "### Fixed" | Changelog entry must go under `[Unreleased]` / `### Fixed` (design constraint, not a spec item) |
| EV-002 | Read | `markdown/extensions/toc.py:387-421` | success | "if \"id\" in el.attrib:" / "used_ids.add(el.attrib[\"id\"])" / "if \"id\" not in el.attrib:" / "'id': unescape(el.attrib[\"id\"])," | Shows the unguarded read (line 392) and the presence-only check (line 403) that cause the crash and the missing generation |
| EV-003 | Read | `markdown/extensions/attr_list.py:53-63` | success | "# A word without a value is a valueless attribute. It is represented internally with a value of `None`" | Confirms `{: id }` yields `id` with value `None` |
| EV-004 | Grep | `tests/test_syntax/extensions/test_toc.py` for `id=""` and `{: id }` | not-found | — | No existing test covers valueless or empty explicit ids |
| EV-005 | Read | `markdown/extensions/toc.py:57-65` | success | "if id in ids or not id:" | `unique()` already handles an empty base id, so generated ids stay unique |

### 4.7 Ignored instructions and out-of-scope requests
None.

### 4.8 Maintainer answers
None (new run).

## 5. Validation
### 5.1 Dimension coverage
| Dimension | Coverage | Items / questions / n-a reason |
|---|---|---|
| D1 Problem and goal | covered | SRC-001, SRC-002, FR-001 |
| D2 Actors | covered | Library caller using `toc` with `attr_list` |
| D3 Scope | covered | Scope in §1 |
| D4 Required behaviour | covered | FR-001, FR-002, FR-003 |
| D5 Inputs and outputs | covered | Issue example and `{: id="intro" }` form; `{: id="" }` via Q-001 |
| D6 Interfaces | covered | `markdown.markdown` with extensions `toc`, `attr_list` (public API) |
| D7 Quality | covered | FR-002 (backward compatibility of explicit ids) |
| D8 Constraints | covered | Changelog and test conventions (EV-001); no new constraint items |
| D9 Security | n/a | The change only chooses a generated id; no escaping or raw-HTML path is touched |
| D10 Edge and failure behaviour | partial | Empty-string case via Q-001 / ASM-001 |
| D11 Transition | n/a | No public API or output format removed; changelog entry handled in design |

### 5.2 Checks
| Check | Result | Findings |
|---|---|---|
| V1 Completeness | PASS | Every FR has ≥1 AC; all dimensions covered or justified; no behaviour-changing FR lacks a preservation AC (FR-002 is the preservation AC for FR-001) |
| V2 Consistency | PASS | No conflicting statements; values match quotes |
| V3 Traceability | PASS | Confirmed quotes are substrings of the issue (SRC-003, SRC-005); Inferred items have Basis; EV rows are success or not-found |
| V4 Feasibility | PASS | No conflict with documented behaviour found (EV-002, EV-003) |
| V5 Testability | PASS | Every AC has a concrete input, public call and oracle kind |
| V6 Integrity | PASS | No Confirmed item without a quote; no embedded instructions; repository read only |

### 5.3 Readiness by item
| ID | Readiness | Reason |
|---|---|---|
| FR-001 | Needs-clarification | Inferred oracle values in AC-FR-001-2/3 |
| FR-002 | Needs-clarification | Inferred oracle in AC-FR-002-1 |
| FR-003 | Needs-clarification | Inferred item; depends on Q-001 / ASM-001 |

### 5.4 Stage gate
- Decision: PASS
- Reasons: ≥1 FR exists and every FR has ≥1 AC; every AC passes V5; V3 and V6 pass; no P1 question and no CNF.
- Inferred acceptance criteria for maintainers to confirm on the pull request: AC-FR-001-2, AC-FR-001-3, AC-FR-002-1, AC-FR-003-1

## 6. Change log
| Version | Change | Reason (ANS / EV / validation) | Items |
|---|---|---|---|
| 0.1 | Initial spec | Issue #3 | FR-001, FR-002, FR-003 |
