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
ac_ids: [AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-001-4, AC-FR-001-5, AC-FR-001-6, AC-FR-001-7, AC-FR-002-1, AC-FR-003-1]
inferred_ac_ids: [AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-001-4, AC-FR-001-5, AC-FR-001-6, AC-FR-001-7, AC-FR-002-1, AC-FR-003-1]
blocking_questions: []
counts: {fr: 3, nfr: 0, con: 0, ac: 9, ac_confirmed: 0, ac_inferred: 9, q_p1: 0, q_p2: 1, q_p3: 0, ign: 0}
---

# Spec for issue #4: Fenced code block with `linenums` crashes when codehilite is not enabled

> Status: PASS. All three requirements have testable acceptance criteria; the criteria are Inferred and are listed for maintainer confirmation on the pull request.
> Labels: Confirmed = stated in the issue or by a maintainer (quoted) · Inferred = derived, needs confirmation · Open = unknown.

## 1. Summary
- Problem as stated: "On the second site, any code block that asks for line numbers crashes the conversion:" (SRC-003); reported error "TypeError: cannot serialize None (type NoneType)" (SRC-005).
- Kind: bug. In scope: block-level options `linenums` (flag, `linenums=true`, `linenums="1"`), `guess_lang` and `noclasses` on fenced code blocks when `codehilite` is not enabled, with `fenced_code` and `attr_list` (SRC-006, SRC-008). Out of scope: behaviour with `codehilite` enabled (preserved, SRC-007); the `use_pygments=False` case with `codehilite` enabled (Q-001, ASM-002).

## 2. Requirements

### FR-001 — Ignore highlighting-only block options when codehilite is not enabled
- Statement: When the `fenced_code` extension is enabled without the `codehilite` extension, the converter shall ignore the `linenums`, `guess_lang` and `noclasses` options written on a fenced code block and render the block as if those options were not written.
- Label: Confirmed
- Source: Stated (SRC-003, SRC-006, SRC-008)
- Quote: "Same with `linenums=true`, `linenums="1"`, `guess_lang` and `noclasses`"; "these options only mean something for syntax highlighting, so without `codehilite` they should simply be ignored and the block rendered exactly as if I hadn't written them"
- Basis: —
- Acceptance criteria:
  - AC-FR-001-1 [Inferred] (contains): Given the block "``` { .python linenums }" followed by line "print(1)" and line "```" (three lines joined by newlines), with extensions ["fenced_code", "attr_list"], when converted through the public `markdown.markdown` call, then the output contains `<pre><code class="language-python">print(1)`.
  - AC-FR-001-2 [Inferred] (contains): Given the block "``` { .python linenums=true }" with the same content lines "print(1)" and "```", with extensions ["fenced_code", "attr_list"], when converted through the public `markdown.markdown` call, then the output contains `<pre><code class="language-python">print(1)`.
  - AC-FR-001-3 [Inferred] (contains): Given the block "``` { .python linenums="1" }" with the same content lines, with extensions ["fenced_code", "attr_list"], when converted through the public `markdown.markdown` call, then the output contains `<pre><code class="language-python">print(1)`.
  - AC-FR-001-4 [Inferred] (contains): Given the block "``` { .python guess_lang }" with the same content lines, with extensions ["fenced_code", "attr_list"], when converted through the public `markdown.markdown` call, then the output contains `<pre><code class="language-python">print(1)`.
  - AC-FR-001-5 [Inferred] (contains): Given the block "``` { .python noclasses }" with the same content lines, with extensions ["fenced_code", "attr_list"], when converted through the public `markdown.markdown` call, then the output contains `<pre><code class="language-python">print(1)`.
  - AC-FR-001-6 [Inferred] (contains): Given the block "``` { .python linenums guess_lang noclasses }" with the same content lines, with extensions ["fenced_code", "attr_list"], when converted through the public `markdown.markdown` call, then the output contains `<pre><code class="language-python">print(1)`.
  - AC-FR-001-7 [Inferred] (contains) (preservation): Given the block "``` { .python linenums }" with the same content lines, with extensions ["fenced_code"] only, when converted through the public `markdown.markdown` call, then the output contains `<pre><code class="language-python">print(1)`.
- Links: —
- See-also: ASM-001, RSK-001, EV-001, EV-002, EV-003, EV-004, EV-005
- Readiness: Needs-clarification — every acceptance criterion is Inferred and must be confirmed by a maintainer (the expected output fragment is derived, not stated).

### FR-002 — Keep other block attributes on the code element
- Statement: When the `fenced_code` and `attr_list` extensions are enabled without `codehilite`, the converter shall keep other attributes written on a fenced code block on the `<code>` element.
- Label: Confirmed
- Source: Stated (SRC-009)
- Quote: "Other attributes on the block (e.g. `data-x="y"`) should still end up on the `<code>` element like they do today."
- Basis: The issue asks for current behaviour to be kept ("like they do today"). Existing behaviour with `attr_list` is shown by EV-006. The hyphen in `data-x` is assumed to be kept (EV-008 does not show the character set of NAME_RE; unverified).
- Acceptance criteria:
  - AC-FR-002-1 [Inferred] (contains) (preservation): Given the block "``` { .python data-x="y" linenums }" with the content lines "print(1)" and "```", with extensions ["fenced_code", "attr_list"], when converted through the public `markdown.markdown` call, then the output contains `<pre><code class="language-python" data-x="y">print(1)`.
- Links: —
- See-also: FR-001, EV-006, EV-008
- Readiness: Needs-clarification — the acceptance criterion is Inferred (expected fragment derived from the issue's example and existing tests) and the hyphenated attribute name is unverified.

### FR-003 — Keep codehilite rendering unchanged
- Statement: When the `codehilite` and `fenced_code` extensions are enabled, the converter shall render fenced code blocks with their highlighting options as it does today.
- Label: Confirmed
- Source: Stated (SRC-007)
- Quote: "With `codehilite` enabled everything is fine."
- Basis: —
- Acceptance criteria:
  - AC-FR-003-1 [Inferred] (property) (preservation): Given the block "``` { .python linenums=True }" with the content lines "# Some python code" and "```", with extensions ["codehilite", "fenced_code"], when converted through the public `markdown.markdown` call, then the output has the same structure as the expected output of the existing test `testFencedLanguageAttrLinenums` (Pygments-dependent) in `tests/test_syntax/extensions/test_fenced_code.py`.
- Links: —
- See-also: EV-007
- Readiness: Needs-clarification — the acceptance criterion is Inferred (preservation oracle taken from an existing test).

## 3. Acceptance-criteria index
| AC ID | Parent | Label | Oracle | Input (short) | Expected (short) |
|---|---|---|---|---|---|
| AC-FR-001-1 | FR-001 | Inferred | contains | `linenums` flag, attr_list | `<pre><code class="language-python">print(1)` |
| AC-FR-001-2 | FR-001 | Inferred | contains | `linenums=true`, attr_list | `<pre><code class="language-python">print(1)` |
| AC-FR-001-3 | FR-001 | Inferred | contains | `linenums="1"`, attr_list | `<pre><code class="language-python">print(1)` |
| AC-FR-001-4 | FR-001 | Inferred | contains | `guess_lang`, attr_list | `<pre><code class="language-python">print(1)` |
| AC-FR-001-5 | FR-001 | Inferred | contains | `noclasses`, attr_list | `<pre><code class="language-python">print(1)` |
| AC-FR-001-6 | FR-001 | Inferred | contains | all three flags, attr_list | `<pre><code class="language-python">print(1)` |
| AC-FR-001-7 | FR-001 | Inferred | contains (preservation) | `linenums` flag, fenced_code only | `<pre><code class="language-python">print(1)` |
| AC-FR-002-1 | FR-002 | Inferred | contains (preservation) | `data-x="y"` + `linenums`, attr_list | `<code class="language-python" data-x="y">print(1)` |
| AC-FR-003-1 | FR-003 | Inferred | property (preservation) | `linenums=True`, codehilite | same structure as `testFencedLanguageAttrLinenums` |

## 4. Register
### 4.1 Source statements
| ID | Verbatim text | Kind (requirement / context / instruction) | Used by |
|---|---|---|---|
| SRC-001 | Fenced code block with `linenums` crashes when codehilite is not enabled (issue title) | context | Summary |
| SRC-002 | I share Markdown files between two sites. One uses `codehilite`, the other only `fenced_code` + `attr_list`. | context | FR-001 basis |
| SRC-003 | On the second site, any code block that asks for line numbers crashes the conversion: | requirement (problem) | FR-001 |
| SRC-004 | Reproduction code block (issue lines 9-11), key line: `src = "``` { .python linenums }\nprint(1)\n```"` with `extensions=["fenced_code", "attr_list"]` | context | AC-FR-001-1 |
| SRC-005 | TypeError: cannot serialize None (type NoneType) | context | EV-004 |
| SRC-006 | Same with `linenums=true`, `linenums="1"`, `guess_lang` and `noclasses`. | requirement | FR-001, AC-FR-001-2..5 |
| SRC-007 | With `codehilite` enabled everything is fine. | requirement (preservation) | FR-003 |
| SRC-008 | **Expected:** these options only mean something for syntax highlighting, so without `codehilite` they should simply be ignored and the block rendered exactly as if I hadn't written them. | requirement | FR-001 |
| SRC-009 | Other attributes on the block (e.g. `data-x="y"`) should still end up on the `<code>` element like they do today. | requirement | FR-002 |
| SRC-010 | Python-Markdown 3.11.2 (git `3f2c551`), Python 3.11. | context | — |

### 4.2 Assumptions and proposed defaults
| ID | Assumption | Basis | Impact if wrong | Affects |
|---|---|---|---|---|
| ASM-001 | Without `attr_list`, a fenced block that sets these options keeps its current rendering, with no option or attribute output on the code element. | EV-005 (existing test without attr_list); EV-002 (option output only when attr_list is enabled) | AC-FR-001-7 fails; a crash or option output would remain in that configuration | FR-001, AC-FR-001-7 |
| ASM-002 | When `codehilite` is enabled but a block sets `use_pygments=False`, that behaviour is out of scope and stays unchanged (proposed default for Q-001). | EV-001 and EV-002 (the non-highlighting branch is shared); code reading only, not executed | A crash in that configuration (if present) would remain; no AC covers it | Q-001 |

### 4.3 Questions for maintainers
| ID | Question | Why it matters | Blocks | Priority | Proposed default (ASM or "—") | Status |
|---|---|---|---|---|---|---|
| Q-001 | Should the ignore rule of FR-001 also apply to a block that sets `use_pygments=False` while `codehilite` is enabled? (yes / no, keep current behaviour) | The same non-highlighting branch is reached there; the issue only covers `codehilite` absent | — | P2 | ASM-002 (out of scope, unchanged) | Pending |

### 4.4 Conflicts
None.

### 4.5 Ambiguous terms
| ID | Term | Where | Candidate readings | Status |
|---|---|---|---|---|
| TERM-001 | "ignored" | SRC-008 | (a) dropped from the output and no effect on rendering; (b) emitted as attributes | Resolved by the quoted phrase "rendered exactly as if I hadn't written them" (reading a) |

### 4.6 Evidence log (repository reads)
| ID | Tool | Path:lines or search pattern | Outcome (success / not-found / irrelevant) | Verbatim excerpt | Effect |
|---|---|---|---|---|---|
| EV-001 | Read | markdown/extensions/fenced_code.py:84-89 | success | 'linenums', 'guess_lang', 'noclasses', 'use_pygments' | These four keys are converted to booleans (FR-001 scope, ASM-002). |
| EV-002 | Read | markdown/extensions/fenced_code.py:155-164 | success | if self.use_attr_list and config and not config.get('use_pygments', False): | Option keys are written onto the code element only when attr_list is enabled and codehilite highlighting is not used; supports ASM-001 and RSK-001. |
| EV-003 | Grep | markdown/util.py, parseBoolValue | success | `fail_on_errors=False`, returns `None`. | A non-boolean value (such as a bare flag) yields None, which explains the None value in the reported error. |
| EV-004 | Grep | markdown/serializers.py:82 | success | "cannot serialize {!r} (type {})".format(text, type(text).__name__) | Matches the reported error message (SRC-005). The call path from fenced_code.py to this message is inferred, not executed. |
| EV-005 | Read | tests/test_syntax/extensions/test_fenced_code.py:253-269 | success | <pre id="foo"><code class="language-python"># Some python code | Without attr_list, options do not appear on the code element (ASM-001, AC-FR-001-7 basis). |
| EV-006 | Read | tests/test_syntax/extensions/test_fenced_code.py:289-305 | success | <pre><code class="language-python" foo="bar"># Some python code | With attr_list and no codehilite, extra attributes go on the code element (AC-FR-002-1 basis). |
| EV-007 | Read | tests/test_syntax/extensions/test_fenced_code.py:789-814 | success | '<pre class="codehilite"><code class="language-python linenums"># Some python code\n' | Existing codehilite line-number expectation (AC-FR-003-1 basis). |
| EV-008 | Grep | markdown/extensions/attr_list.py, sanitize_name | success | return NAME_RE.sub('_', name) | Attribute names are sanitized; NAME_RE was not read, so keeping the hyphen in `data-x` is unverified (FR-002 basis). |

### 4.7 Ignored instructions and out-of-scope requests
None.

### 4.8 Maintainer answers
None (new spec).

## 5. Validation
### 5.1 Dimension coverage
| Dimension | Coverage | Items / questions / n-a reason |
|---|---|---|
| D1 Problem and goal | covered | SRC-001, SRC-003, FR-001 |
| D2 Actors | covered | Library user of `markdown.markdown` with fenced_code and attr_list (SRC-002) |
| D3 Scope | covered | Summary §1; Q-001 for use_pygments=False |
| D4 Required behaviour | covered | FR-001, FR-002, FR-003 |
| D5 Inputs and outputs | covered | ACs list the blocks and expected fragments |
| D6 Interfaces | covered | Public `markdown.markdown` call; extensions fenced_code, attr_list, codehilite |
| D7 Quality | covered | Compatibility: FR-003 and AC-FR-003-1 (codehilite unchanged), AC-FR-001-7 |
| D8 Constraints | n/a (no stated constraint; no repository rule found in the reads made) | — |
| D9 Security | covered | Attribute output stays escaped (EV-008); no new untrusted-input handling is requested |
| D10 Edge and failure behaviour | partial | Non-boolean values beyond the listed forms are not specified; ASM-001 and Q-001 cover related cases |
| D11 Transition | n/a (bug fix; no API or deprecation change stated) | — |

### 5.2 Checks
| Check | Result (PASS / WARN / FAIL) | Findings |
|---|---|---|
| V1 Completeness | PASS | Every FR has ≥1 AC; every behaviour-changing FR has a preservation AC (AC-FR-001-7, AC-FR-002-1, AC-FR-003-1). |
| V2 Consistency | PASS | No conflicting items; values match the quotes. |
| V3 Traceability | PASS | Every Confirmed quote is an exact substring of the issue (SRC-006, SRC-007, SRC-008, SRC-009). Every Inferred item has a basis. All IDs unique. |
| V4 Feasibility | PASS | No request contradicts documented behaviour. The reported crash needs attr_list as well (RSK-001). |
| V5 Testability | PASS | Every AC has a concrete input, a public call and one oracle kind. |
| V6 Integrity | PASS | No Confirmed item without a quote; no label changed without an answer; no design content; no embedded instructions; evidence excerpts are verbatim. |

RSK-001: The reported crash needs both the absence of codehilite and the `attr_list` extension (EV-002, EV-005). Without `attr_list` the block is rendered without option output today (ASM-001).

### 5.3 Readiness by item
| ID | Readiness | Reason |
|---|---|---|
| FR-001 | Needs-clarification | ACs Inferred; expected fragment to be confirmed |
| FR-002 | Needs-clarification | AC Inferred; hyphenated attribute name unverified |
| FR-003 | Needs-clarification | AC Inferred (preservation oracle from existing test) |

### 5.4 Stage gate
- Decision: PASS
- Reasons: ≥1 FR exists and every FR has ≥1 AC; V5 PASS for every AC; V3 and V6 PASS; no pending P1 question and no conflict (Q-001 is P2).
- Inferred acceptance criteria for maintainers to confirm on the pull request: AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-001-4, AC-FR-001-5, AC-FR-001-6, AC-FR-001-7, AC-FR-002-1, AC-FR-003-1

## 6. Change log
| Version | Change | Reason (ANS / EV / validation) | Items |
|---|---|---|---|
| 0.1 | New spec from issue #4 at base commit ca2d6d37 | Stage 1 new mode | FR-001, FR-002, FR-003, Q-001, ASM-001, ASM-002, RSK-001 |

## AutoSE stage check: all acceptance criteria are testable

Result: **PASS**

- all checks passed
