---
artefact: spec
stage: requirements
issue: 4
issue_kind: bug
base_commit: ca2d6d37ae9baf0a946edded6815015f722ee57c
spec_version: 0.1
mode: new
skill: requirements-spec-builder 1.3-autose
status: PASS
ac_ids: [AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-001-4, AC-FR-001-5, AC-FR-002-1, AC-FR-003-1, AC-FR-004-1]
inferred_ac_ids: [AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-001-4, AC-FR-001-5, AC-FR-002-1, AC-FR-003-1, AC-FR-004-1]
blocking_questions: []
counts: {fr: 4, nfr: 0, con: 0, ac: 8, ac_confirmed: 0, ac_inferred: 8, q_p1: 0, q_p2: 1, q_p3: 0, ign: 0}
---

# Spec for issue #4: Fenced code block with `linenums` crashes when codehilite is not enabled

> Status: PASS. The crash and the expected behaviour are stated in the issue, and every requirement has a testable acceptance criterion. The exact expected output is inferred from existing tests, so the ACs are `[Inferred]` and are listed for maintainer confirmation on the pull request.
> Labels: Confirmed = stated in the issue or by a maintainer (quoted) · Inferred = derived, needs confirmation · Open = unknown.

## 1. Summary
- Problem as stated: "they should simply be ignored and the block rendered exactly as if I hadn't written them" (SRC-002)
- Kind: bug. In scope: highlighting-only options on fenced code blocks when `fenced_code` and `attr_list` are enabled and `codehilite` is not. Out of scope: changing highlighting output when `codehilite` is enabled (preservation, see FR-004).

## 2. Requirements

### FR-001 — Highlighting-only options do not crash and are omitted from `<code>`
- Statement: When `fenced_code` and `attr_list` are enabled and `codehilite` produces no highlighting for a block, the converter shall omit the options `linenums`, `guess_lang` and `noclasses` from the attributes of the `<code>` element, without raising an error.
- Label: Confirmed
- Source: Stated (SRC-001, SRC-002)
- Quote: "they should simply be ignored and the block rendered exactly as if I hadn't written them"; "Same with `linenums=true`, `linenums="1"`, `guess_lang` and `noclasses`"
- Basis: —
- Acceptance criteria:
  - AC-FR-001-1 [Inferred] (exact): Given the fenced block "``` { .python linenums }" / "print(1)" / "```" with extensions ["fenced_code", "attr_list"], when `markdown.markdown` is called, then the output is `<pre><code class="language-python">print(1)\n</code></pre>` (the output equals the output for the same block without `linenums`).
  - AC-FR-001-2 [Inferred] (exact): Given the same block with `{ .python linenums=true }` and extensions ["fenced_code", "attr_list"], when converted, then the output is `<pre><code class="language-python">print(1)\n</code></pre>`.
  - AC-FR-001-3 [Inferred] (exact): Given the same block with `{ .python linenums="1" }` and extensions ["fenced_code", "attr_list"], when converted, then the output is `<pre><code class="language-python">print(1)\n</code></pre>`.
  - AC-FR-001-4 [Inferred] (exact): Given the same block with `{ .python guess_lang=False }` and extensions ["fenced_code", "attr_list"], when converted, then the output is `<pre><code class="language-python">print(1)\n</code></pre>`.
  - AC-FR-001-5 [Inferred] (exact): Given the same block with `{ .python noclasses=True }` and extensions ["fenced_code", "attr_list"], when converted, then the output is `<pre><code class="language-python">print(1)\n</code></pre>`.
- Links: —
- See-also: Q-001, ASM-001, EV-001, EV-002, EV-004
- Readiness: Needs-clarification — ACs are `[Inferred]`; maintainers confirm the exact output on the pull request.

### FR-002 — `hl_lines` is treated the same way as the other highlighting-only options
- Statement: When `fenced_code` and `attr_list` are enabled and `codehilite` produces no highlighting for a block, the converter shall omit the option `hl_lines` from the attributes of the `<code>` element, without raising an error.
- Label: Inferred
- Source: Agent-inference
- Quote: —
- Basis: `hl_lines` is a highlighting-only option (the issue's rule: "these options only mean something for syntax highlighting"). It is parsed into a list of ints (EV-007), and the attribute writer does not reject lists, so today the block renders `hl_lines="[1, 3]"` (reasoned from code reading, not executed). Confirm with Q-001.
- Acceptance criteria:
  - AC-FR-002-1 [Inferred] (exact): Given the block "``` { .python hl_lines="1 3" }" / "print(1)" / "```" with extensions ["fenced_code", "attr_list"], when converted, then the output is `<pre><code class="language-python">print(1)\n</code></pre>`.
- Links: Q-001
- See-also: ASM-001
- Readiness: Needs-clarification — depends on Q-001 (proposed default ASM-001).

### FR-003 — Other attributes are kept on `<code>`
- Statement: When `fenced_code` and `attr_list` are enabled and `codehilite` produces no highlighting for a block, the converter shall keep every attribute that is not a highlighting-only option on the `<code>` element, as it does today.
- Label: Confirmed
- Source: Stated (SRC-003)
- Quote: "Other attributes on the block (e.g. `data-x="y"`) should still end up on the `<code>` element like they do today."
- Basis: —
- Acceptance criteria:
  - AC-FR-003-1 [Inferred] (exact) (preservation): Given the block "``` { .python data-x="y" linenums }" / "print(1)" / "```" with extensions ["fenced_code", "attr_list"], when converted, then the output is `<pre><code class="language-python" data-x="y">print(1)\n</code></pre>`.
- Links: —
- See-also: EV-006
- Readiness: Needs-clarification — AC is `[Inferred]`.

### FR-004 — Highlighting with `codehilite` is unchanged
- Statement: When `codehilite` is enabled and highlighting is applied to a block, the converter shall produce the same highlighted output as before this change.
- Label: Inferred
- Source: Repository (EV-004, EV-005)
- Quote: —
- Basis: Existing tests pin the highlighted output (EV-004, EV-005). This is a preservation requirement.
- Acceptance criteria:
  - AC-FR-004-1 [Inferred] (contains) (preservation): Given the block "``` { .python linenums=True }" / "print(1)" / "```" with extensions ["codehilite", "fenced_code"], when converted, then the output contains `class="codehilite"`.
- Links: —
- See-also: EV-004, EV-005
- Readiness: Needs-clarification — AC is `[Inferred]`.

## 3. Acceptance-criteria index
| AC ID | Parent | Label | Oracle | Input (short) | Expected (short) |
|---|---|---|---|---|---|
| AC-FR-001-1 | FR-001 | Inferred | exact | `{ .python linenums }`, fenced_code+attr_list | `<pre><code class="language-python">print(1)\n</code></pre>` |
| AC-FR-001-2 | FR-001 | Inferred | exact | `{ .python linenums=true }` | same as above |
| AC-FR-001-3 | FR-001 | Inferred | exact | `{ .python linenums="1" }` | same as above |
| AC-FR-001-4 | FR-001 | Inferred | exact | `{ .python guess_lang=False }` | same as above |
| AC-FR-001-5 | FR-001 | Inferred | exact | `{ .python noclasses=True }` | same as above |
| AC-FR-002-1 | FR-002 | Inferred | exact | `{ .python hl_lines="1 3" }` | same as above |
| AC-FR-003-1 | FR-003 | Inferred | exact | `{ .python data-x="y" linenums }` | `<pre><code class="language-python" data-x="y">print(1)\n</code></pre>` |
| AC-FR-004-1 | FR-004 | Inferred | contains | `{ .python linenums=True }`, codehilite+fenced_code | contains `class="codehilite"` |

## 4. Register
### 4.1 Source statements
| ID | Verbatim text | Kind (requirement / context / instruction) | Used by |
|---|---|---|---|
| SRC-001 | "Same with `linenums=true`, `linenums="1"`, `guess_lang` and `noclasses`." | requirement | FR-001 |
| SRC-002 | "these options only mean something for syntax highlighting, so without `codehilite` they should simply be ignored and the block rendered exactly as if I hadn't written them." | requirement | FR-001 |
| SRC-003 | "Other attributes on the block (e.g. `data-x="y"`) should still end up on the `<code>` element like they do today." | requirement | FR-003 |
| SRC-004 | "any code block that asks for line numbers crashes the conversion" | context | FR-001 |

### 4.2 Assumptions and proposed defaults
| ID | Assumption | Basis | Impact if wrong | Affects |
|---|---|---|---|---|
| ASM-001 | `hl_lines` is ignored in the same way as the listed options. | Same code path; a highlighting-only option (EV-007, EV-001) | A maintainer may prefer `hl_lines` kept as an attribute; FR-002 and AC-FR-002-1 would change. | FR-002 |

### 4.3 Questions for maintainers
| ID | Question | Why it matters | Blocks | Priority | Proposed default (ASM or "—") | Status |
|---|---|---|---|---|---|---|
| Q-001 | Should `hl_lines` also be omitted from the `<code>` attributes when highlighting is not applied (as proposed), or should it stay as an attribute? | Changes FR-002 and AC-FR-002-1 | — | P2 | ASM-001 | Pending |

### 4.4 Conflicts
None.

### 4.5 Ambiguous terms
None.

### 4.6 Evidence log (repository reads)
| ID | Tool | Path:lines or search pattern | Outcome (success / not-found / irrelevant) | Verbatim excerpt | Effect |
|---|---|---|---|---|---|
| EV-001 | Read | markdown/extensions/fenced_code.py:155-164 | success | "if self.use_attr_list and config and not config.get('use_pygments', False):" ... "for k, v in config.items() if k != 'use_pygments'" | Every config key except `use_pygments` is written as an attribute, including values parsed to bool or None (FR-001). |
| EV-002 | Grep | `_escape_attrib_html`, `parseBoolValue` in markdown/ | success | "raise TypeError(" / "cannot serialize {!r} (type {})" (serializers.py:80-83) | Non-string values raise `TypeError`, matching the issue's error (FR-001). |
| EV-003 | Grep | `linenums\|guess_lang\|noclasses\|hl_lines` in tests/ | success | (tests list only `codehilite`-enabled cases for these options; see EV-004, EV-005) | No existing test covers these options with `attr_list` and no `codehilite`. |
| EV-004 | Read | tests/test_syntax/extensions/test_fenced_code.py:789-814 | success | `'<pre class="codehilite"><code class="language-python linenums"># Some python code\n'` | Codehilite linenums output is pinned (FR-004). |
| EV-005 | Grep | tests/test_syntax/extensions/test_fenced_code.py `attr_list` | success | `extensions=['fenced_code', 'attr_list']` (lines 304-455) | Attribute-output tests exist for the no-codehilite path (FR-003). |
| EV-006 | Read | tests/test_syntax/extensions/test_fenced_code.py:296-305 | success | `<pre><code class="language-python" foo="bar"># Some python code` | Existing non-highlighting attribute output format (FR-003, AC-FR-003-1). |
| EV-007 | Grep | markdown/extensions/codehilite.py `parse_hl_lines` | success | `def parse_hl_lines(expr: str) -> list[int]:` / `return list(map(int, expr.split()))` | `hl_lines` is a list of ints (FR-002). |
| EV-008 | Grep | docs/extensions/fenced_code_blocks.md | success | "So long as code highlighting is not enabled (see below), the key/value pairs will be assigned as attributes on the `<code>` tag in the output." | Documented contract that is the source of the crash (FR-001). |
| EV-009 | Read | docs/extensions/fenced_code_blocks.md:200-216 | success | "If the `attr_list` extension is not enabled, then the key/value pairs will be ignored." | Documentation to update with the omission rule. |
| EV-010 | Read | docs/changelog.md:15-41 | success | "### Fixed" under "## [Unreleased]" | Changelog location for the entry. |

### 4.7 Ignored instructions and out-of-scope requests
None.

### 4.8 Maintainer answers
None (new run).

## 5. Validation
### 5.1 Dimension coverage
| Dimension | Coverage | Items / questions / n-a reason |
|---|---|---|
| D1 Problem and goal | covered | FR-001, SRC-002 |
| D2 Actors | covered | Library user (`markdown.markdown`) with `fenced_code` + `attr_list` |
| D3 Scope | covered | Summary §1 |
| D4 Required behaviour | covered | FR-001, FR-002, FR-003 |
| D5 Inputs and outputs | covered | ACs with exact outputs (Inferred) |
| D6 Interfaces | covered | Public `markdown.markdown` with extensions list |
| D7 Quality | covered | FR-004 (preservation) |
| D8 Constraints | covered | Changelog entry required (EV-010); flake8 119 |
| D9 Security | n/a | Attribute values stay escaped via the existing escape helper; no new raw output |
| D10 Edge and failure behaviour | covered | Bool forms `true`, `"1"`, `False`, `hl_lines` (FR-001, FR-002) |
| D11 Transition | covered | Changelog entry, docs sentence (EV-009) |

### 5.2 Checks
| Check | Result (PASS / WARN / FAIL) | Findings |
|---|---|---|
| V1 Completeness | PASS | Every FR has ≥1 AC; FR-001 and FR-002 change behaviour and FR-003 and FR-004 are the preservation ACs. |
| V2 Consistency | PASS | Expected outputs match the attribute format in EV-006. |
| V3 Traceability | PASS | Confirmed quotes are copied from the issue (checked against issue text). Inferred items have a Basis. |
| V4 Feasibility | PASS | No conflict with documented behaviour; docs say attributes are written when highlighting is off (EV-008), and this change only omits options that cannot be written. |
| V5 Testability | PASS | Every AC has a concrete input, a public call and an oracle. |
| V6 Integrity | PASS | No Confirmed item without a quote; evidence excerpts copied from tool output. |

### 5.3 Readiness by item
| ID | Readiness | Reason |
|---|---|---|
| FR-001 | Needs-clarification | ACs are `[Inferred]`. |
| FR-002 | Needs-clarification | Depends on Q-001. |
| FR-003 | Needs-clarification | AC is `[Inferred]`. |
| FR-004 | Needs-clarification | AC is `[Inferred]`. |

### 5.4 Stage gate
- Decision: PASS
- Reasons: ≥1 FR exists and every FR has ≥1 AC; V5 PASS for every AC; V3 and V6 PASS; no P1 question and no CNF.
- Inferred acceptance criteria for maintainers to confirm on the pull request: AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-001-4, AC-FR-001-5, AC-FR-002-1, AC-FR-003-1, AC-FR-004-1.

## 6. Change log
| Version | Change | Reason (ANS / EV / validation) | Items |
|---|---|---|---|
| 0.1 | Initial spec | Issue #4 | FR-001..FR-004 |
