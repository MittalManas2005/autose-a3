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
ac_ids: [AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-001-4, AC-FR-001-5, AC-FR-002-1, AC-FR-002-2, AC-FR-002-3, AC-FR-003-1, AC-FR-004-1, AC-FR-004-2, AC-FR-005-1]
inferred_ac_ids: [AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-001-4, AC-FR-001-5, AC-FR-002-1, AC-FR-002-2, AC-FR-002-3, AC-FR-003-1, AC-FR-004-1, AC-FR-004-2, AC-FR-005-1]
blocking_questions: []
counts: {fr: 5, nfr: 0, con: 0, ac: 12, ac_confirmed: 0, ac_inferred: 12, q_p1: 0, q_p2: 2, q_p3: 0, ign: 0}
---

# Spec for issue #5: TOC: allow excluding individual headings from the table of contents

> Status: PASS. Every requirement has testable acceptance criteria through the public API; all criteria are `[Inferred]` and listed for maintainer confirmation on the pull request.
> Labels: Confirmed = stated in the issue or by a maintainer (quoted) · Inferred = derived, needs confirmation · Open = unknown.

## 1. Summary
- Problem as stated: "there is currently no way to leave a single heading out (only `toc_depth` for whole levels)" (SRC-001)
- Kind: feature. In scope: excluding a heading from the TOC when it carries the class `notoc` set with `attr_list`. Out of scope: any other exclusion mechanism; not stated otherwise (see Q-002 for the compatibility question).

## 2. Requirements

### FR-001 — Heading with class `notoc` is left out of the TOC
- Statement: The toc extension shall leave out of the table of contents any heading that has the class `notoc` set through the attribute list syntax of `attr_list`.
- Label: Confirmed
- Source: Stated (SRC-002), Stated (SRC-003)
- Quote: "if a heading has the class `notoc` (set with `attr_list`), leave it out of the TOC"
- Basis: The example in SRC-003 gives the input and the expected outcome in words. The acceptance criteria are operationalised by the agent as membership checks (contains / not-contains) on the TOC, so they are `[Inferred]`.
- Acceptance criteria:
- AC-FR-001-1 [Inferred] (contains): Given the document lines `[TOC]`, `# One`, `## Two {: .notoc }`, `## Three` (blank lines between them) with extensions ["toc", "attr_list"], when converted through the public API, then the output TOC (`md.toc`) contains `href="#one"`.
- AC-FR-001-2 [Inferred] (contains): Given the same document with extensions ["toc", "attr_list"], when converted through the public API, then the output TOC (`md.toc`) contains `href="#three"`.
- AC-FR-001-3 [Inferred] (not-contains): Given the same document with extensions ["toc", "attr_list"], when converted through the public API, then the output TOC (`md.toc`) does not contain `href="#two"`.
- AC-FR-001-4 [Inferred] (contains): Given the document lines `# One`, `## Two {: .notoc }`, `### Sub` (blank lines between them) with extensions ["toc", "attr_list"], when converted through the public API, then the output TOC (`md.toc`) contains `href="#sub"` (default per ASM-002; see Q-001).
- AC-FR-001-5 [Inferred] (contains) (preservation): Given the document lines `# One`, `## Two`, `## Three` (blank lines between them) with extensions ["toc"], when converted through the public API, then the output TOC (`md.toc`) contains `href="#two"`.
- Links: Q-001 (non-blocking), CNF — none, TERM — none
- See-also: ASM-002, ASM-004, EV-001, EV-004, EV-005
- Readiness: Needs-clarification — ACs are `[Inferred]` and Q-001 is pending.

### FR-002 — Excluded heading is still rendered normally, with its id
- Statement: The toc extension shall keep rendering a heading that carries the class `notoc` normally, including its `id` attribute and its text content.
- Label: Confirmed
- Source: Stated (SRC-004)
- Quote: "The heading itself should still be rendered normally, including its id, so existing links to it keep working."
- Basis: —
- Acceptance criteria:
- AC-FR-002-1 [Inferred] (contains) (preservation): Given the document lines `# One`, `## Two {: .notoc }`, `## Three` (blank lines between them) with extensions ["toc", "attr_list"], when converted through the public API, then the output HTML contains `id="two"`.
- AC-FR-002-2 [Inferred] (contains): Given the document lines `# One`, `## Two {: .notoc }`, `## Three` (blank lines between them) with extensions ["toc", "attr_list"], when converted through the public API, then the output HTML contains `Two</h2>`.
- AC-FR-002-3 [Inferred] (contains): Given the document lines `# One`, `## Two {: .notoc }` (blank line between them) with extensions ["toc", "attr_list"] and the toc option `permalink` set to `True`, when converted through the public API, then the output HTML contains `class="headerlink" href="#two"` (default per ASM-001; EV-006 shows the permalink markup format).
- Links: —
- See-also: ASM-001, EV-003, EV-006
- Readiness: Needs-clarification — ACs are `[Inferred]`; the permalink behaviour rests on ASM-001.

### FR-003 — Excluded heading is left out of `md.toc_tokens`
- Statement: The toc extension shall leave a heading that carries the class `notoc` out of the `toc_tokens` attribute of the Markdown instance, at every nesting level.
- Label: Confirmed
- Source: Stated (SRC-005)
- Quote: "It should also be left out of `md.toc_tokens`, because we build our sidebar from that."
- Basis: —
- Acceptance criteria:
- AC-FR-003-1 [Inferred] (property): Given the document lines `[TOC]`, `# One`, `## Two {: .notoc }`, `## Three` (blank lines between them) with extensions ["toc", "attr_list"], when converted through the public API, then no entry in `md.toc_tokens`, at any nesting depth, has the id `two`, and entries with the ids `one` and `three` are present.
- Links: FR-001 (same mechanism); preservation for the rest of `toc_tokens` is covered by AC-FR-004-2.
- See-also: EV-003
- Readiness: Needs-clarification — ACs are `[Inferred]`.

### FR-004 — Headings with other classes behave as today
- Statement: The toc extension shall keep the TOC output and `md.toc_tokens` for a heading that has classes other than `notoc` unchanged from the current behaviour.
- Label: Confirmed
- Source: Stated (SRC-006)
- Quote: "Headings with other classes should behave exactly as today."
- Basis: —
- Acceptance criteria:
- AC-FR-004-1 [Inferred] (contains) (preservation): Given the document lines `# One`, `## Two {: .other }`, `## Three` (blank lines between them) with extensions ["toc", "attr_list"], when converted through the public API, then the output TOC (`md.toc`) contains `href="#two"`.
- AC-FR-004-2 [Inferred] (property) (preservation): Given the document lines `# One`, `## Two {: .other }`, `## Three` (blank lines between them) with extensions ["toc", "attr_list"], when converted through the public API, then `md.toc_tokens` equals the `md.toc_tokens` produced by the same document with the `{: .other }` attribute list removed.
- Links: —
- See-also: EV-003, EV-006
- Readiness: Needs-clarification — ACs are `[Inferred]`.

### FR-005 — Several classes, one of them `notoc`
- Statement: The toc extension shall leave out of the TOC a heading whose attribute list gives it the class `notoc` together with other classes.
- Label: Inferred
- Source: Agent-inference
- Quote: —
- Basis: SRC-002 says "has the class `notoc`", which does not say whether other classes may also be present. The reading that `notoc` among several classes still counts is the natural one, but it is not stated. Confirm on the pull request (ASM-003).
- Acceptance criteria:
- AC-FR-005-1 [Inferred] (not-contains): Given the document lines `# One`, `## Two {: .other .notoc }`, `## Three` (blank lines between them) with extensions ["toc", "attr_list"], when converted through the public API, then the output TOC (`md.toc`) does not contain `href="#two"`.
- Links: ASM-003
- See-also: —
- Readiness: Needs-clarification — depends on ASM-003 and the AC is `[Inferred]`.

## 3. Acceptance-criteria index
| AC ID | Parent | Label | Oracle | Input (short) | Expected (short) |
|---|---|---|---|---|---|
| AC-FR-001-1 | FR-001 | Inferred | contains | `# One` / `## Two {: .notoc }` / `## Three`, toc+attr_list | TOC has `href="#one"` |
| AC-FR-001-2 | FR-001 | Inferred | contains | same | TOC has `href="#three"` |
| AC-FR-001-3 | FR-001 | Inferred | not-contains | same | TOC lacks `href="#two"` |
| AC-FR-001-4 | FR-001 | Inferred | contains | `# One` / `## Two {: .notoc }` / `### Sub`, toc+attr_list | TOC has `href="#sub"` |
| AC-FR-001-5 | FR-001 | Inferred | contains (preservation) | `# One` / `## Two` / `## Three`, toc only | TOC has `href="#two"` |
| AC-FR-002-1 | FR-002 | Inferred | contains (preservation) | same as AC-FR-001-1 | HTML has `id="two"` |
| AC-FR-002-2 | FR-002 | Inferred | contains | same as AC-FR-001-1 | HTML has `Two</h2>` |
| AC-FR-002-3 | FR-002 | Inferred | contains | `# One` / `## Two {: .notoc }`, toc+attr_list, permalink=True | HTML has `class="headerlink" href="#two"` |
| AC-FR-003-1 | FR-003 | Inferred | property | same as AC-FR-001-1 | no `toc_tokens` entry with id `two`; `one` and `three` present |
| AC-FR-004-1 | FR-004 | Inferred | contains (preservation) | `# One` / `## Two {: .other }` / `## Three`, toc+attr_list | TOC has `href="#two"` |
| AC-FR-004-2 | FR-004 | Inferred | property (preservation) | same as AC-FR-004-1 | `toc_tokens` equals that without the attribute list |
| AC-FR-005-1 | FR-005 | Inferred | not-contains | `# One` / `## Two {: .other .notoc }` / `## Three`, toc+attr_list | TOC lacks `href="#two"` |

## 4. Register
### 4.1 Source statements
| ID | Verbatim text | Kind (requirement / context / instruction) | Used by |
|---|---|---|---|
| SRC-001 | there is currently no way to leave a single heading out (only `toc_depth` for whole levels) | context | Summary |
| SRC-002 | if a heading has the class `notoc` (set with `attr_list`), leave it out of the TOC | requirement | FR-001, FR-005 |
| SRC-003 | `[TOC]` / `# One` / `## Two {: .notoc }` / `## Three` → should give a TOC with only "One" and "Three". | requirement (example) | FR-001 |
| SRC-004 | The heading itself should still be rendered normally, including its id, so existing links to it keep working. | requirement | FR-002 |
| SRC-005 | It should also be left out of `md.toc_tokens`, because we build our sidebar from that. | requirement | FR-003 |
| SRC-006 | Headings with other classes should behave exactly as today. | requirement | FR-004 |
| SRC-007 | Python-Markdown 3.11.2. | context | Front matter (version reference only) |

### 4.2 Assumptions and proposed defaults
| ID | Assumption | Basis | Impact if wrong | Affects |
|---|---|---|---|---|
| ASM-001 | An excluded heading still receives an anchorlink or permalink when those options are enabled, as any heading does. | EV-003 (anchor and permalink are added regardless of the level filter); EV-006 | AC-FR-002-3 changes | FR-002 |
| ASM-002 | Child headings of an excluded heading stay in the TOC and are nested under the nearest included ancestor. | EV-003 and EV-005 (TOC nesting is built from the remaining tokens); the issue is silent | AC-FR-001-4 changes; Q-001 | FR-001 |
| ASM-003 | A heading whose attribute list gives `notoc` among other classes is excluded too. | SRC-002 says "has the class", with no restriction to a single class | AC-FR-005-1 changes | FR-005 |
| ASM-004 | No configuration option is added. The class name `notoc` is fixed and applies unconditionally whenever the `toc` extension and `attr_list` are enabled. | SRC-002 states no option; EV-001 finds no existing `notoc` term; change is additive | Maintainers would need an option or a different default; Q-002 | FR-001, FR-004 |

### 4.3 Questions for maintainers
| ID | Question | Why it matters | Blocks | Priority | Proposed default (ASM or "—") | Status |
|---|---|---|---|---|---|---|
| Q-001 | When a heading is left out of the TOC, should its child headings (e.g. `### Sub` below `## Two {: .notoc }`) still appear in the TOC, nested under the nearest included heading? | The issue does not say; the nesting affects the TOC structure and `md.toc_tokens` | — | P2 | ASM-002 | Pending |
| Q-002 | Should a heading that already has the class `notoc` today (set with `attr_list`) be left out of the TOC without any opt-in setting, as proposed? | Existing documents that already use the class `notoc` change their TOC output (RSK-001) | — | P2 | ASM-004 | Pending |

### 4.4 Conflicts
None.

### 4.5 Ambiguous terms
None.

### 4.6 Evidence log (repository reads)
| ID | Tool | Path:lines or search pattern | Outcome (success / not-found / irrelevant) | Verbatim excerpt | Effect |
|---|---|---|---|---|---|
| EV-001 | Grep | `toc_depth\|toc_tokens\|notoc\|permalink` in `markdown/` and `docs/` (tests excluded) | success for `toc_depth`; not-found for `notoc` | `* **`toc_depth`**` (docs/extensions/toc.md:225) | Confirms `toc_depth` is whole-level only; no existing per-heading exclusion or `notoc` term. Basis for FR-001 and ASM-004. |
| EV-002 | Read | docs/extensions/toc.md:60-130 | success | "if this extension is used in conjunction with the [Attribute Lists Extension] and a `data-toc-label` attribute is defined on the header" | Documented precedent that `attr_list` attributes on headings are visible to the toc extension. `toc_tokens` keys documented at lines 71-88. |
| EV-003 | Read | markdown/extensions/toc.py:360-450 | success | `if "id" not in el.attrib:` / `el.attrib["id"] = unique(self.slugify(html.unescape(name), self.sep), used_ids, id_counters)` (lines 403-404) | Ids are assigned before the level filter. `toc_tokens` entries are appended only when `toc_top <= level <= toc_bottom` (lines 414-421). Anchor and permalink are added regardless (lines 423-426). Supports FR-002, FR-003, ASM-001. |
| EV-004 | Grep | `treeprocessors.register` in markdown/extensions/toc.py | success | `md.treeprocessors.register(tocext, 'toc', 5)` (line 511) | The toc tree processor runs at priority 5. |
| EV-005 | Grep | `attr_list\|AttrList` in markdown/extensions/attr_list.py | success | `md.treeprocessors.register(AttrListTreeprocessor(md), 'attr_list', 8)` (line 239) | attr_list is registered at priority 8, above toc at 5. Together with EV-003 (the toc code already reads attributes set by attr_list at line 407) this supports the reading that the class is visible when toc runs. The run order itself was not read from the registry code (unverified). |
| EV-006 | Grep | `class="` in tests/test_syntax/extensions/test_toc.py | success | `'<a class="headerlink" href="#header" title="Permanent link">&para;</a>'` (line 648) | Gives the permalink markup form used in AC-FR-002-3. |
| EV-007 | Grep | `attr_list\|AttrList` in docs/ (files only) | success | docs/extensions/attr_list.md | Confirms that attribute-list documentation exists; no further effect. |
| EV-008 | Grep | `notoc\|toc` count in tests/test_syntax/extensions/test_toc.py | irrelevant | — | Existing toc test file; no `notoc` case exists. |

### 4.7 Ignored instructions and out-of-scope requests
None.

### 4.8 Maintainer answers
None (new spec).

## 5. Validation
### 5.1 Dimension coverage
| Dimension | Coverage | Items / questions / n-a reason |
|---|---|---|
| D1 Problem and goal | covered | SRC-001, FR-001 |
| D2 Actors | covered | Library users of the toc extension, through the Markdown API (SRC-003 example) |
| D3 Scope | partial | Scope in: FR-001 to FR-005. Out: not stated; Q-002 covers existing `notoc` users |
| D4 Required behaviour | covered | FR-001, FR-003 |
| D5 Inputs and outputs | covered | Given/When/Then in each AC; SRC-003 example |
| D6 Interfaces | covered | `toc` extension, `attr_list`, `md.toc_tokens`; ASM-004 (no new option) |
| D7 Quality | covered | AC-FR-001-5, AC-FR-002-1, AC-FR-004-1, AC-FR-004-2 (compatibility) |
| D8 Constraints | covered | No repository rule found that constrains the change beyond EV-001; n/a for rules |
| D9 Security | n/a | The change only excludes a heading from a generated list; it touches no escaping or untrusted-input handling |
| D10 Edge and failure behaviour | partial | Children (Q-001), several classes (ASM-003) |
| D11 Transition | partial | Existing users of the class `notoc` (Q-002, RSK-001); no changelog requirement found |

### 5.2 Checks
| Check | Result (PASS / WARN / FAIL) | Findings |
|---|---|---|
| V1 Completeness | PASS | Every FR has ≥1 AC; FR-001 and FR-003 have preservation coverage (AC-FR-001-5, AC-FR-004-2); D1–D11 covered or flagged with a question or assumption |
| V2 Consistency | PASS | Values match the quoted text; the example in SRC-003 matches FR-001 |
| V3 Traceability | PASS | Every item has a Source; every Confirmed quote is an exact substring of the issue (SRC-002, SRC-004, SRC-005, SRC-006); every Inferred item has a Basis; Q-001 and Q-002 linked; EV-001 to EV-008 cited with outcome success or not-found |
| V4 Feasibility | PASS | No conflict with documented behaviour found (EV-001, EV-002); no request to change stated values |
| V5 Testability | PASS | Every AC names a concrete input and configuration, a public call (`markdown.Markdown` conversion, `md.toc`, `md.toc_tokens`), and one oracle kind; no unmeasurable qualifier remains |
| V6 Integrity | PASS | No Confirmed label without a quote; no design or internal function names; no embedded instructions present; only `.autose_out/spec.md` written |

### 5.3 Readiness by item
| ID | Readiness | Reason |
|---|---|---|
| FR-001 | Needs-clarification | Q-001 pending; ACs are `[Inferred]` |
| FR-002 | Needs-clarification | ACs are `[Inferred]`; ASM-001 |
| FR-003 | Needs-clarification | ACs are `[Inferred]` |
| FR-004 | Needs-clarification | ACs are `[Inferred]` |
| FR-005 | Needs-clarification | Inferred requirement; ASM-003 |

Spec-level verdict: No (no item is Ready, because every AC is `[Inferred]`). Informational only; the stage gate decides hand-over.

### 5.4 Stage gate
- Decision: PASS
- Reasons: (1) every FR has ≥1 AC (FR-001 to FR-005, 12 ACs in total); (2) V5 is PASS for every AC; (3) V3 and V6 are PASS; (4) no P1 question is pending (Q-001 and Q-002 are P2 with proposed defaults ASM-002 and ASM-004) and there is no CNF.
- Inferred acceptance criteria for maintainers to confirm on the pull request: AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-001-4, AC-FR-001-5, AC-FR-002-1, AC-FR-002-2, AC-FR-002-3, AC-FR-003-1, AC-FR-004-1, AC-FR-004-2, AC-FR-005-1. Decisions to confirm: Q-001 (children, ASM-002), Q-002 (unconditional class, ASM-004), ASM-001 (permalink on excluded heading), ASM-003 (several classes).

## 6. Change log
| Version | Change | Reason (ANS / EV / validation) | Items |
|---|---|---|---|
| 0.1 | Initial spec from issue #5 | Issue text (SRC-001 to SRC-007); EV-001 to EV-008 | FR-001 to FR-005; AC-FR-001-1 to AC-FR-005-1; Q-001, Q-002; ASM-001 to ASM-004; RSK-001 |

### Risk register note
- RSK-001: Headings that already use the class `notoc` will leave the TOC after this change, changing existing output. Linked to Q-002.

## AutoSE stage check: all acceptance criteria are testable

Result: **PASS**

- all checks passed
