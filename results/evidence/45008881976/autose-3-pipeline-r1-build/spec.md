---
artefact: spec
stage: requirements
issue: 3
issue_kind: bug
base_commit: 758ab062032e4096fc14a4bb219015e83820c890
spec_version: 0.1
mode: new
skill: requirements-spec-builder 1.3-autose
status: PASS
ac_ids: [AC-FR-001-1, AC-FR-002-1, AC-FR-002-2, AC-FR-002-3, AC-FR-002-4, AC-FR-002-5, AC-FR-003-1, AC-FR-003-2, AC-FR-004-1]
inferred_ac_ids: [AC-FR-002-1, AC-FR-002-2, AC-FR-002-3, AC-FR-002-4, AC-FR-002-5, AC-FR-003-1, AC-FR-003-2]
blocking_questions: []
counts: {fr: 4, nfr: 0, con: 0, ac: 9, ac_confirmed: 2, ac_inferred: 7, q_p1: 0, q_p2: 2, q_p3: 0, ign: 0}
---

# Spec for issue #3: TOC extension crashes with TypeError when a heading has `{: id }` without a value

> Status: PASS. No P1 question is open and no conflict affects a functional requirement; the seven `[Inferred]` acceptance criteria are listed for maintainer confirmation.
> Labels: Confirmed = stated in the issue or by a maintainer (quoted) · Inferred = derived, needs confirmation · Open = unknown.

## 1. Summary
- Problem as stated: "TOC extension crashes with TypeError when a heading has `{: id }` without a value" (SRC-001); the reported call is `markdown.markdown("# Heading {: id }", extensions=["toc", "attr_list"])` (SRC-002).
- Kind: bug. In scope: a heading whose `id` attribute is given without a value, when the `toc` extension is enabled (SRC-001, SRC-002, SRC-005). Out of scope: other valueless attributes (not stated; Q-002, ASM-002). Explicit `id` values must keep working (SRC-006).
- Stated environment: Python-Markdown 3.11.2 (git `3f2c551`), Python 3.12, macOS (SRC-007). Context only.

## 2. Requirements

### FR-001 — No crash for a valueless heading id
- Statement: The converter shall not raise an exception when a heading carries an `id` attribute without a value and the `toc` and `attr_list` extensions are enabled.
- Label: Confirmed
- Source: Stated (SRC-002, SRC-005)
- Quote: "no crash"
- Basis: —
- Acceptance criteria:
  - AC-FR-001-1 [Confirmed] (no-error): Given input `# Heading {: id }` with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown`, then no exception is raised and HTML is returned.
- Links: —
- See-also: EV-003, EV-004
- Readiness: Ready — confirmed, atomic, its only AC is confirmed and testable.

### FR-002 — A valueless id counts as no id
- Statement: The converter shall treat a heading whose `id` attribute has no value as a heading without an id: it shall receive the normal auto-generated id and shall appear in the table of contents.
- Label: Confirmed
- Source: Stated (SRC-005)
- Quote: "A heading with an empty `id` should just be treated like a heading without an id: it gets the normal auto-generated id and shows up in the table of contents like every other heading."
- Basis: The word "empty" is ambiguous (TERM-001). This requirement is read as covering the valueless case reported in the issue. The case `id=""` is handled by AC-FR-002-5 and ASM-001. The auto-generated value `heading` in AC-FR-002-1 follows the default slug rule; that rule was not read in this run, so the value is unverified. The `[TOC]` marker in AC-FR-002-3 is assumed to be the documented default; it is unverified in this run.
- Acceptance criteria:
  - AC-FR-002-1 [Inferred] (contains): Given input `# Heading {: id }` with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown`, then the output contains `<h1 id="heading">`.
  - AC-FR-002-2 [Inferred] (not-contains): Given input `# Heading {: id }` with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown`, then the output does not contain `<h1 id>`.
  - AC-FR-002-3 [Inferred] (contains): Given input `[TOC]` followed by a blank line and `# Heading {: id }` with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown`, then the output contains `href="#heading"`.
  - AC-FR-002-4 [Inferred] (property): Given input `# Heading {: id }` followed by a blank line and `# Heading` with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown`, then every `id` attribute value in the output is unique.
  - AC-FR-002-5 [Inferred] (no-error): Given input `# Heading {: id="" }` with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown`, then no exception is raised. This holds under both readings of ASM-001.
- Links: TERM-001, Q-001
- See-also: ASM-001, EV-003, EV-004, EV-007, EV-008
- Readiness: Needs-clarification — waiting for confirmation of the inferred ACs and of ASM-001 (Q-001).

### FR-003 — Explicit heading ids keep working
- Statement: The converter shall keep the explicitly given `id` value of a heading, and shall keep the table-of-contents link to it, when the `toc` and `attr_list` extensions are enabled.
- Label: Confirmed
- Source: Stated (SRC-004, SRC-006)
- Quote: "Ids I set explicitly should keep working as they do now."
- Basis: The exact output strings in the ACs are an operationalisation of "keep working as they do now". The issue states that `{: id="intro" }` works fine with `toc` (SRC-004). The documented behaviour that a manually defined id is kept is in EV-008.
- Acceptance criteria:
  - AC-FR-003-1 [Inferred] (contains): Given input `# Heading {: id="intro" }` with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown`, then the output contains `<h1 id="intro">`.
  - AC-FR-003-2 [Inferred] (contains) (preservation): Given input `[TOC]` followed by a blank line and `# Heading {: id="intro" }` with extensions `["toc", "attr_list"]`, when converted through `markdown.markdown`, then the output contains `href="#intro"`.
- Links: —
- See-also: EV-008, EV-009
- Readiness: Needs-clarification — waiting for confirmation of the inferred ACs.

### FR-004 — Without toc, a valueless id is unchanged
- Statement: The converter shall keep rendering a valueless heading id as before when only the `attr_list` extension is enabled.
- Label: Confirmed
- Source: Stated (SRC-003)
- Quote: "`attr_list` alone gives `<h1 id>Heading</h1>`"
- Basis: —
- Acceptance criteria:
  - AC-FR-004-1 [Confirmed] (exact): Given input `# Heading {: id }` with extensions `["attr_list"]`, when converted through `markdown.markdown`, then the output is `<h1 id>Heading</h1>`.
- Links: —
- See-also: EV-004, EV-005
- Readiness: Ready — confirmed, atomic, its only AC is confirmed and testable.

## 3. Acceptance-criteria index
| AC ID | Parent | Label | Oracle | Input (short) | Expected (short) |
|---|---|---|---|---|---|
| AC-FR-001-1 | FR-001 | Confirmed | no-error | `# Heading {: id }`, toc + attr_list | no exception, HTML returned |
| AC-FR-002-1 | FR-002 | Inferred | contains | `# Heading {: id }`, toc + attr_list | contains `<h1 id="heading">` |
| AC-FR-002-2 | FR-002 | Inferred | not-contains | `# Heading {: id }`, toc + attr_list | not contains `<h1 id>` |
| AC-FR-002-3 | FR-002 | Inferred | contains | `[TOC]` + `# Heading {: id }`, toc + attr_list | contains `href="#heading"` |
| AC-FR-002-4 | FR-002 | Inferred | property | `# Heading {: id }` + `# Heading`, toc + attr_list | all id values unique |
| AC-FR-002-5 | FR-002 | Inferred | no-error | `# Heading {: id="" }`, toc + attr_list | no exception |
| AC-FR-003-1 | FR-003 | Inferred | contains | `# Heading {: id="intro" }`, toc + attr_list | contains `<h1 id="intro">` |
| AC-FR-003-2 | FR-003 | Inferred | contains | `[TOC]` + `# Heading {: id="intro" }`, toc + attr_list | contains `href="#intro"` |
| AC-FR-004-1 | FR-004 | Confirmed | exact | `# Heading {: id }`, attr_list only | `<h1 id>Heading</h1>` |

## 4. Register

### 4.1 Source statements
| ID | Verbatim text | Kind | Used by |
|---|---|---|---|
| SRC-001 | "TOC extension crashes with TypeError when a heading has `{: id }` without a value" | requirement (problem) | FR-001 |
| SRC-002 | `markdown.markdown("# Heading {: id }", extensions=["toc", "attr_list"])` | requirement (reproduction) | FR-001, AC-FR-001-1, AC-FR-002-* |
| SRC-003 | "`attr_list` alone gives `<h1 id>Heading</h1>`" | context / expected behaviour without toc | FR-004 |
| SRC-004 | "`{: id="intro" }` works fine with `toc`" | context / expected behaviour | FR-003 |
| SRC-005 | "A heading with an empty `id` should just be treated like a heading without an id: it gets the normal auto-generated id and shows up in the table of contents like every other heading." | requirement | FR-001, FR-002 |
| SRC-006 | "Ids I set explicitly should keep working as they do now." | requirement (preservation) | FR-003 |
| SRC-007 | "Python-Markdown 3.11.2 (git `3f2c551`), Python 3.12, macOS." | context | — |
| SRC-008 | Traceback excerpt: `TypeError: expected string or bytes-like object, got 'NoneType'` at the TOC extension's `run` method | context (observed failure) | FR-001, RSK-002 |

### 4.2 Assumptions and proposed defaults
| ID | Assumption | Basis | Impact if wrong | Affects |
|---|---|---|---|---|
| ASM-001 | Only a valueless `id` (e.g. `{: id }`) is "empty" for FR-002. An explicit empty value (`{: id="" }`) is not auto-generated and keeps today's output. It must not raise an exception. | Reading of SRC-001 and SRC-005 (the title and the reproduction use the valueless form). Documented rule that explicit ids are not overridden (EV-008). Changing `id=""` would alter output nobody reported. | If maintainers want `id=""` auto-generated too, AC-FR-002-5 is extended and output for `id=""` changes. | FR-002, AC-FR-002-5 |
| ASM-002 | This change covers only the `id` attribute. Other valueless attributes that the TOC extension reads (for example `data-toc-label`, see EV-003 and RSK-001) are out of scope. | Issue is limited to `id` (SRC-001). Proposed default changes nothing beyond the request (default rule (b)). | If maintainers want the same protection for `data-toc-label`, the spec gains a new FR and its ACs. | Scope (Q-002) |

### 4.3 Questions for maintainers
| ID | Question | Why it matters | Blocks | Priority | Proposed default (ASM or "—") | Status |
|---|---|---|---|---|---|---|
| Q-001 | Should `# Heading {: id="" }` (an explicit empty value) also receive an auto-generated id, or keep today's output? (Options: keep today's output / auto-generate.) | Defines what "empty `id`" means in SRC-005 (TERM-001). | — | P2 | ASM-001 (keep today's output) | Pending |
| Q-002 | Should the fix also cover other valueless attributes read by the TOC extension, such as `data-toc-label`, or only `id`? (Options: only `id` / also `data-toc-label`.) | Same crash path may exist for other attributes (RSK-001). | — | P2 | ASM-002 (only `id`) | Pending |

### 4.4 Conflicts
None.

### 4.5 Ambiguous terms
| ID | Term | Where | Candidate readings | Status |
|---|---|---|---|---|
| TERM-001 | "empty `id`" | SRC-005 (title: "without a value") | (a) valueless `id` only (`{: id }`); (b) valueless and explicit empty value (`{: id="" }`) | Open — Q-001, ASM-001 |

### 4.6 Evidence log (repository reads)
| ID | Tool | Path:lines or search pattern | Outcome | Verbatim excerpt | Effect |
|---|---|---|---|---|---|
| EV-001 | Grep | `markdown/extensions/toc.py`, pattern for `attrib[` and `'id'` | success | `417: 'id': unescape(el.attrib["id"]),` | Confirms the failing line named in the traceback reads the `id` attribute without a check for a missing value. |
| EV-002 | Grep | `markdown/extensions/attr_list.py`, pattern `id` | success | `57: return 'id', t[1:]` | Shows `#` shorthand becomes an `id` with a value. Context for FR-003. |
| EV-003 | Read | `markdown/extensions/toc.py` 385–434 | success | `402: # Do not override pre-existing ids` / `403: if "id" not in el.attrib:` / `408: data_toc_label = run_postprocessors(unescape(el.attrib['data-toc-label']), self.md)` | An explicit `id` is not regenerated. A valueless `id` is present in the attributes, so it is never generated and is passed on to unescape. The same pattern applies to `data-toc-label` (RSK-001). |
| EV-004 | Read | `markdown/extensions/attr_list.py` 180–224 | success | `201: elif v is None:` / `212: elem.set(name, None)` | A valueless non-boolean attribute is stored with value `None`, so `id` is present with no value. This is the mechanism behind the issue. |
| EV-005 | Read | `markdown/extensions/attr_list.py` 50–89 | success | `# internally with a value of `None` so that what the user provided can` | Documents that valueless attributes use `None` by design. |
| EV-006 | Grep | `tests/` pattern for valueless attributes | success | `tests/test_syntax/extensions/test_attr_list.py:149: def test_valueless_non_boolean_preserved_xhtml(self):` | Existing tests pin valueless-attribute preservation for attr_list. Search output was truncated at 30 lines, so no toc test with a valueless id was ruled in or out. |
| EV-007 | Grep | `docs/extensions/toc.md`, pattern `id` | success | `By default, all headers will automatically have unique `id` attributes` | Documented: every heading gets a unique id by default. Basis for AC-FR-002-4. |
| EV-008 | Read | `docs/extensions/toc.md` 116–127 | success | `the ID was manually defined in the attribute list to provide a cleaner URL when linking to the header. If the ID is not manually defined, it is always derived from the text of the header` | Documented: manual ids are kept; otherwise the id is derived from the heading text. Basis for FR-002, FR-003, ASM-001. |
| EV-009 | Grep | `tests/test_syntax/extensions/test_toc.py`, pattern for `{:` or `{ id` | success | `r'# `*Foo*` { id="\*Foo\*" }',` | An existing toc test uses an explicit attribute-list id. No toc test with a valueless id appeared in this search. |

### 4.7 Ignored instructions and out-of-scope requests
None. The issue text contains no embedded instructions.

### 4.8 Maintainer answers
None (new spec, no answers supplied).

## 5. Validation

### 5.1 Dimension coverage
| Dimension | Coverage | Items / questions / n-a reason |
|---|---|---|
| D1 Problem and goal | covered | SRC-001, SRC-005; FR-001, FR-002 |
| D2 Actors | covered | Library users of `markdown.markdown` with `toc` and `attr_list` (SRC-002) |
| D3 Scope | covered | In: valueless `id` on headings with toc. Out: other attributes (ASM-002, Q-002) |
| D4 Required behaviour | covered | FR-001, FR-002 |
| D5 Inputs and outputs | covered | Given inputs in AC-FR-001-1, AC-FR-002-*, AC-FR-003-*, AC-FR-004-1 |
| D6 Interfaces | covered | Public `markdown.markdown` call with extension names `toc` and `attr_list` |
| D7 Quality | covered | FR-003 and AC-FR-004-1 preserve existing output; AC-FR-003-2 preserves the TOC link |
| D8 Constraints | n/a | No constraint is stated in the issue. No repository rule was read in this run. |
| D9 Security | n/a | The request changes only how a valueless id is handled. It does not change escaping or handling of untrusted input; explicit id values keep their current handling (FR-003). |
| D10 Edge and failure behaviour | covered | Valueless id (FR-001, FR-002); `id=""` (AC-FR-002-5, Q-001); duplicate headings (AC-FR-002-4) |
| D11 Transition | n/a | No public API change is requested. Changelog policy was not checked in this run. |

### 5.2 Checks
| Check | Result | Findings |
|---|---|---|
| V1 Completeness | PASS | Every dimension is covered or n/a with a reason. Every FR has at least one AC. The behaviour-changing FR-002 and FR-001 have preservation ACs (FR-003, FR-004). |
| V2 Consistency | PASS | FR-002's inferred ACs and ASM-001 agree on the valueless case. No values were changed from the issue. |
| V3 Traceability | PASS | Every FR has a Source. Every Confirmed quote is copied from the issue (checked against the issue text). Every Inferred item has a Basis. Every Repository source cites an EV row with outcome success. IDs are unique. |
| V4 Feasibility | PASS | No request contradicts documented behaviour. Explicit ids and TOC links are documented as kept (EV-008). No CNF was needed. |
| V5 Testability | PASS | Every AC names an input and extension list, a public call and one oracle kind. Oracles are no-error, contains, not-contains, property or exact. |
| V6 Integrity | PASS | No Confirmed item without a quote. No label changed without an answer. No design is stated. No embedded instruction was present. Every evidence read is logged. Only `spec.md` is written. |

Notes for maintainers (not blocking):
- RSK-001: The same crash path may occur for a valueless `data-toc-label`. This was found by reading EV-003 and was not run. Linked to Q-002.
- RSK-002: The crash was not executed in this run (the requirements role may not run code). The failure path is established from the issue's traceback (SRC-008) and the code reads in EV-003 and EV-004.

### 5.3 Readiness by item
| ID | Readiness | Reason |
|---|---|---|
| FR-001 | Ready | Confirmed, atomic, its only AC is confirmed and testable. |
| FR-002 | Needs-clarification | Inferred ACs; linked to TERM-001 and Q-001. |
| FR-003 | Needs-clarification | Inferred ACs. |
| FR-004 | Ready | Confirmed, atomic, its only AC is confirmed and testable. |

Spec-level verdict: Partially (2 of 4 FRs are Ready).

### 5.4 Stage gate
- Decision: PASS
- Reasons: At least one FR exists and every FR has at least one AC (condition 1). V5 is PASS for every AC (condition 2). V3 and V6 are PASS (condition 3). No P1 question is pending and no CNF exists (condition 4).
- Inferred acceptance criteria for maintainers to confirm on the pull request: AC-FR-002-1, AC-FR-002-2, AC-FR-002-3, AC-FR-002-4, AC-FR-002-5, AC-FR-003-1, AC-FR-003-2. Also confirm ASM-001 (Q-001) and ASM-002 (Q-002).

## 6. Change log
| Version | Change | Reason (ANS / EV / validation) | Items |
|---|---|---|---|
| 0.1 | Initial spec from issue #3 at base commit 758ab062032e4096fc14a4bb219015e83820c890. | New mode; issue text plus repository evidence EV-001 to EV-009. | All |

## AutoSE stage check: all acceptance criteria are testable

Result: **PASS**

- all checks passed
