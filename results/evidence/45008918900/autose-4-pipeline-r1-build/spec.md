---
artefact: spec
stage: requirements
issue: 4
issue_kind: bug
base_commit: 758ab062032e4096fc14a4bb219015e83820c890
spec_version: 0.1
mode: new
skill: requirements-spec-builder 1.3-autose
status: PASS
ac_ids: [AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-001-4, AC-FR-001-5, AC-FR-002-1, AC-FR-003-1, AC-NFR-001-1, AC-NFR-001-2, AC-NFR-001-3, AC-NFR-002-1]
inferred_ac_ids: [AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-001-4, AC-FR-001-5, AC-FR-002-1, AC-FR-003-1, AC-NFR-001-1, AC-NFR-001-2, AC-NFR-001-3, AC-NFR-002-1]
blocking_questions: []
counts: {fr: 3, nfr: 2, con: 0, ac: 11, ac_confirmed: 0, ac_inferred: 11, q_p1: 0, q_p2: 1, q_p3: 1, ign: 0}
---

# Spec for issue #4: Fenced code block with `linenums` crashes when codehilite is not enabled

> Status: PASS. All acceptance criteria are testable through `markdown.markdown`; the open questions are P2/P3 and have proposed defaults, so the stage may proceed. All ACs are `[Inferred]` and need maintainer confirmation on the pull request.
> Labels: Confirmed = stated in the issue or by a maintainer (quoted) · Inferred = derived, needs confirmation · Open = unknown.
> In exact oracles, `\n` denotes a newline character.

## 1. Summary
- Problem as stated: "any code block that asks for line numbers crashes the conversion" (SRC-002)
- Kind: bug. In scope: fenced code blocks that use `linenums`, `guess_lang` or `noclasses` with `fenced_code` and `attr_list` enabled and `codehilite` not enabled (SRC-005, SRC-007). Out of scope: other `codehilite`-only option keys (Q-001, ASM-001).

## 2. Requirements

### FR-001 — Ignore codehilite-only options without codehilite
- Statement: When the `fenced_code` and `attr_list` extensions are enabled and `codehilite` is not, the converter shall ignore the `linenums`, `guess_lang` and `noclasses` options of a fenced code block and render the block as if those options were not written.
- Label: Confirmed
- Source: Stated (SRC-002, SRC-005, SRC-007)
- Quote: "these options only mean something for syntax highlighting, so without `codehilite` they should simply be ignored and the block rendered exactly as if I hadn't written them"
- Basis: The quote states the expected behaviour. The option names come from SRC-005. The trigger `attr_list` comes from the reproduction (SRC-003) and the crash path needs it (EV-003: key/value output is gated on `use_attr_list`). The set of options is ambiguous (TERM-001); see Q-001 and ASM-001. Values are covered by AC-FR-001-2, AC-FR-001-3 and AC-FR-001-5; the error message `TypeError: cannot serialize None` matches the flag form only (RSK-001).
- Acceptance criteria:
  - AC-FR-001-1 [Inferred] (exact): Given a fenced block opened by three backticks with attribute list `{ .python linenums }`, body `print(1)`, closed by three backticks, with extensions `["fenced_code", "attr_list"]`, when `markdown.markdown` is called, then the output equals `<pre><code class="language-python">print(1)\n</code></pre>`.
  - AC-FR-001-2 [Inferred] (exact): Given the same block with attribute list `{ .python linenums=true }` and the same extensions, when `markdown.markdown` is called, then the output equals `<pre><code class="language-python">print(1)\n</code></pre>`.
  - AC-FR-001-3 [Inferred] (exact): Given the same block with attribute list `{ .python linenums="1" }` and the same extensions, when `markdown.markdown` is called, then the output equals `<pre><code class="language-python">print(1)\n</code></pre>`.
  - AC-FR-001-4 [Inferred] (exact): Given the same block with attribute list `{ .python guess_lang noclasses }` and the same extensions, when `markdown.markdown` is called, then the output equals `<pre><code class="language-python">print(1)\n</code></pre>`.
  - AC-FR-001-5 [Inferred] (exact): Given the same block with attribute list `{ .python linenums=false }` and the same extensions, when `markdown.markdown` is called, then the output equals `<pre><code class="language-python">print(1)\n</code></pre>`.
- Links: —
- See-also: Q-001, Q-002, ASM-001, ASM-002, TERM-001, RSK-001, EV-001, EV-003, EV-004, EV-005
- Readiness: Needs-clarification — Q-001 (scope of the option set) is open with default ASM-001; ACs are Inferred.

### FR-002 — Keep other block attributes on the code element
- Statement: When the `fenced_code` and `attr_list` extensions are enabled and `codehilite` is not, the converter shall keep the other attributes of a fenced code block, other than the ignored options, on the `<code>` element.
- Label: Confirmed
- Source: Stated (SRC-008)
- Quote: "Other attributes on the block (e.g. `data-x="y"`) should still end up on the `<code>` element like they do today."
- Basis: The quote states the requirement. The exact input combining a flag option with a hyphenated attribute is constructed by the agent, so the AC is Inferred. Hyphenated names are kept (EV-006).
- Acceptance criteria:
  - AC-FR-002-1 [Inferred] (contains): Given a fenced block opened by three backticks with attribute list `{ .python linenums data-x="y" }`, body `print(1)`, closed by three backticks, with extensions `["fenced_code", "attr_list"]`, when `markdown.markdown` is called, then the output contains `<code class="language-python" data-x="y">` and does not contain `linenums`.
- Links: —
- See-also: EV-006, ASM-001
- Readiness: Needs-clarification — AC is Inferred (constructed input).

### FR-003 — Keep codehilite behaviour unchanged
- Statement: When the `codehilite` extension is enabled, the converter shall keep rendering fenced code blocks with `linenums`, `guess_lang` and `noclasses` as it does today, without raising an exception.
- Label: Confirmed
- Source: Stated (SRC-006)
- Quote: "With `codehilite` enabled everything is fine."
- Basis: The quote states that current behaviour is correct. The "no exception" oracle is chosen because the highlighted output depends on whether Pygments is installed (EV-004), so an exact string is not safe.
- Acceptance criteria:
  - AC-FR-003-1 [Inferred] (no-error): Given a fenced block opened by three backticks with attribute list `{ .python linenums }`, body `print(1)`, closed by three backticks, with extensions `["codehilite", "fenced_code"]`, when `markdown.markdown` is called, then no exception is raised and a non-empty output is produced.
- Links: —
- See-also: EV-004
- Readiness: Needs-clarification — AC is Inferred.

### NFR-001 — Compatibility: existing output unchanged
- Statement: The converter shall keep the output of fenced code blocks that do not use the ignored options unchanged, including the handling of `use_pygments` and of other attributes when `attr_list` is enabled.
- Label: Inferred
- Source: Repository (EV-007, EV-003)
- Quote: —
- Basis: Preservation requirement required for any behaviour-changing fix (skill §4.5). The expected strings come from the existing tests (EV-007).
- Acceptance criteria:
  - AC-NFR-001-1 [Inferred] (exact): Given a fenced block with attribute list `{ .python foo=bar use_pygments=False }`, body `# Some python code`, and extensions `["fenced_code", "attr_list"]`, when `markdown.markdown` is called, then the output equals `<pre><code class="language-python" foo="bar"># Some python code\n</code></pre>`.
  - AC-NFR-001-2 [Inferred] (exact): Given a fenced block with attribute list `{ .python foo=bar use_pygments=True }`, body `# Some python code`, and extensions `["fenced_code", "attr_list"]`, when `markdown.markdown` is called, then the output equals `<pre><code class="language-python"># Some python code\n</code></pre>`.
  - AC-NFR-001-3 [Inferred] (exact): Given a fenced block with attribute list `{ .python linenums }`, body `print(1)`, and extensions `["fenced_code"]` only (no `attr_list`), when `markdown.markdown` is called, then the output equals `<pre><code class="language-python">print(1)\n</code></pre>`. Basis: without `attr_list` the key/value output is not built (EV-003).
- Links: —
- See-also: EV-003, EV-007
- Readiness: Needs-clarification — label Inferred; ACs Inferred.

### NFR-002 — Security: escaping of kept attributes
- Statement: The converter shall keep sanitising attribute names and escaping attribute values of the attributes it still outputs on the `<code>` element.
- Label: Inferred
- Source: Repository (EV-006)
- Quote: —
- Basis: The fix removes keys before output; the existing sanitisation test must still pass (EV-006). Untrusted input reaches these attributes.
- Acceptance criteria:
  - AC-NFR-002-1 [Inferred] (exact): Given a fenced block with attribute list `{ .python x><svg/onload=alert(1) }`, body `# Some python code`, and extensions `["fenced_code", "attr_list"]`, when `markdown.markdown` is called, then the output equals `<pre><code class="language-python" x_svg_onload="alert(1)"># Some python code\n</code></pre>`.
- Links: —
- See-also: EV-006
- Readiness: Needs-clarification — label Inferred; AC Inferred.

## 3. Acceptance-criteria index
| AC ID | Parent | Label | Oracle | Input (short) | Expected (short) |
|---|---|---|---|---|---|
| AC-FR-001-1 | FR-001 | Inferred | exact | `{ .python linenums }`, fenced_code + attr_list | `<pre><code class="language-python">print(1)\n</code></pre>` |
| AC-FR-001-2 | FR-001 | Inferred | exact | `{ .python linenums=true }`, fenced_code + attr_list | same as AC-FR-001-1 |
| AC-FR-001-3 | FR-001 | Inferred | exact | `{ .python linenums="1" }`, fenced_code + attr_list | same as AC-FR-001-1 |
| AC-FR-001-4 | FR-001 | Inferred | exact | `{ .python guess_lang noclasses }`, fenced_code + attr_list | same as AC-FR-001-1 |
| AC-FR-001-5 | FR-001 | Inferred | exact | `{ .python linenums=false }`, fenced_code + attr_list | same as AC-FR-001-1 |
| AC-FR-002-1 | FR-002 | Inferred | contains | `{ .python linenums data-x="y" }`, fenced_code + attr_list | contains `<code class="language-python" data-x="y">`, no `linenums` |
| AC-FR-003-1 | FR-003 | Inferred | no-error | `{ .python linenums }`, codehilite + fenced_code | no exception, non-empty output |
| AC-NFR-001-1 | NFR-001 | Inferred | exact | `{ .python foo=bar use_pygments=False }`, fenced_code + attr_list | `<pre><code class="language-python" foo="bar"># Some python code\n</code></pre>` |
| AC-NFR-001-2 | NFR-001 | Inferred | exact | `{ .python foo=bar use_pygments=True }`, fenced_code + attr_list | `<pre><code class="language-python"># Some python code\n</code></pre>` |
| AC-NFR-001-3 | NFR-001 | Inferred | exact | `{ .python linenums }`, fenced_code only | `<pre><code class="language-python">print(1)\n</code></pre>` |
| AC-NFR-002-1 | NFR-002 | Inferred | exact | `{ .python x><svg/onload=alert(1) }`, fenced_code + attr_list, body `# Some python code` | `<pre><code class="language-python" x_svg_onload="alert(1)"># Some python code\n</code></pre>` |

## 4. Register

### 4.1 Source statements
| ID | Verbatim text | Kind (requirement / context / instruction) | Used by |
|---|---|---|---|
| SRC-001 | "I share Markdown files between two sites. One uses `codehilite`, the other only `fenced_code` + `attr_list`." | context | TERM-001, FR-001 |
| SRC-002 | "On the second site, any code block that asks for line numbers crashes the conversion:" | requirement (bug symptom) | FR-001 |
| SRC-003 | `src = "``` { .python linenums }\nprint(1)\n```"` and `markdown.markdown(src, extensions=["fenced_code", "attr_list"])` (reproduction code block, not executed) | context | FR-001, AC-FR-001-1 |
| SRC-004 | "TypeError: cannot serialize None (type NoneType)" | context (error output) | RSK-001 |
| SRC-005 | "Same with `linenums=true`, `linenums="1"`, `guess_lang` and `noclasses`." | requirement | FR-001, AC-FR-001-2..4 |
| SRC-006 | "With `codehilite` enabled everything is fine." | requirement (current behaviour) | FR-003 |
| SRC-007 | "these options only mean something for syntax highlighting, so without `codehilite` they should simply be ignored and the block rendered exactly as if I hadn't written them." | requirement | FR-001 |
| SRC-008 | "Other attributes on the block (e.g. `data-x="y"`) should still end up on the `<code>` element like they do today." | requirement | FR-002 |
| SRC-009 | "Python-Markdown 3.11.2 (git `3f2c551`), Python 3.11." | context (version) | — |

### 4.2 Assumptions and proposed defaults
| ID | Assumption | Basis | Impact if wrong | Affects |
|---|---|---|---|---|
| ASM-001 | Only the three options named in the issue (`linenums`, `guess_lang`, `noclasses`) are ignored; `use_pygments` keeps its existing handling; other keys keep their current behaviour (rendered as attributes) | Issue names the three options (SRC-005). `use_pygments` is already omitted from output (EV-003, comment at fenced_code.py:157-158). No evidence that other keys crash. | A codehilite-only key other than the three stays rendered as an attribute; a maintainer may want it ignored too | FR-001, FR-002, Q-001 |
| ASM-002 | Explicit false values (`linenums=false`) are ignored in the same way as true values | Issue says the options "should simply be ignored" (SRC-007). The value path for `false` was not verified (RSK-001). | A `false` value could still be rendered as an attribute or fail | AC-FR-001-5, Q-002 |

### 4.3 Questions for maintainers
| ID | Question | Why it matters | Blocks | Priority | Proposed default (ASM or "—") | Status |
|---|---|---|---|---|---|---|
| Q-001 | Should the fix ignore only `linenums`, `guess_lang` and `noclasses` (the options named in the issue), or every option that only applies to codehilite (for example `pygments_style` or `css_class`)? | Defines the scope of FR-001 (TERM-001) | — | P2 | ASM-001 | Pending |
| Q-002 | Should an explicit false value such as `linenums=false` also be ignored? | Defines expected output for AC-FR-001-5 | — | P3 | ASM-002 | Pending |

### 4.4 Conflicts
None.

### 4.5 Ambiguous terms
| ID | Term | Where | Candidate readings | Status |
|---|---|---|---|---|
| TERM-001 | "these options" | SRC-007 | (a) exactly `linenums`, `guess_lang`, `noclasses`; (b) every codehilite configuration key; (c) (a) plus `use_pygments` | Open → Q-001 (default ASM-001) |

### 4.6 Evidence log (repository reads)
| ID | Tool | Path:lines or search pattern | Outcome (success / not-found / irrelevant) | Verbatim excerpt | Effect |
|---|---|---|---|---|---|
| EV-001 | Grep | `markdown/extensions/fenced_code.py`, pattern `linenums\|guess_lang\|noclasses\|cannot serialize\|use_pygments\|codehilite` | success (`cannot serialize` not-found in source) | `27: from .codehilite import CodeHilite, CodeHiliteExtension, parse_hl_lines` (and matches at lines 84-88, 127, 155-161) | Shows codehilite-only keys are handled in `fenced_code.py`; the TypeError text is not in the repository (the message is from the issue) |
| EV-002 | Grep | `tests`, pattern `linenums\|guess_lang\|noclasses` | success | `markdown.extensions.codehilite.CodeHiliteExtension(linenums=None, guess_lang=False),` (test_fenced_code.py:490) | Existing tests for these options all enable `codehilite`; none pairs them with `attr_list` without `codehilite` (no test found for the crash path) |
| EV-003 | Read | `markdown/extensions/fenced_code.py:75-175` | success | `self.bool_options = [ 'linenums', 'guess_lang', 'noclasses', 'use_pygments' ]`; `if self.use_attr_list and config and not config.get('use_pygments', False):` building `kv_pairs` from `config.items()` with `_escape_attrib_html(v)` | The crash path: key/value pairs are emitted with `attr_list` and no check for `codehilite`. `use_pygments` is omitted from output (comment at 157-158). Basis for AC-FR-001 and the `attr_list` trigger |
| EV-004 | Read | `tests/test_syntax/extensions/test_fenced_code.py:795-858` | success | `'<pre class="codehilite"><code class="language-python linenums"># Some python code\n'` (no-Pygments branch) | Codehilite output is Pygments-dependent; `no-error` oracle used for AC-FR-003-1 |
| EV-005 | Read | `markdown/extensions/fenced_code.py:174-196` (`handle_attrs`) | success | `if v is None: v = k` ; `elif k in self.bool_options: configs[k] = parseBoolValue(v, fail_on_errors=False, preserve_none=True)` | A valueless flag such as `linenums` becomes the value `linenums`, then a boolean; `linenums=true` becomes `True`, `linenums="1"` becomes `True` |
| EV-006 | Grep | `tests/test_syntax/extensions/test_fenced_code.py`, pattern `attr_list\|data-\|bool_options\|use_pygments` | success | `427: <pre><code data-test="{}"># Some python code` ; `319: <pre><code class="language-python" x_svg_onload="alert(1)"># Some python code` | Hyphenated attribute names are kept; attribute-name sanitisation is tested (supports FR-002, NFR-002) |
| EV-007 | Read | `tests/test_syntax/extensions/test_fenced_code.py:296-361` | success | `<pre><code class="language-python" foo="bar"># Some python code` ; `<pre><code class="language-python"># Some python code` (use_pygments=True) | Existing output for `foo=bar` and `use_pygments` with `attr_list` and no codehilite; preservation ACs (NFR-001) |
| EV-008 | Grep | `markdown`, pattern `def parseBoolValue\|def _escape_attrib_html\|return None\|raise ValueError` in `util.py` | success | `markdown/util.py:136: def parseBoolValue(value: str \| None, fail_on_errors: bool = True, preserve_none: bool = False) -> bool \| None:` | Located `parseBoolValue`; `_escape_attrib_html` not located in this search (not-found) |
| EV-009 | Read | `markdown/util.py:136-152` | success | `"""...if ``fail_on_errors=False``, returns ``None``."""` ; `elif fail_on_errors: raise ValueError('Cannot parse bool value: %r' % value)` | An unrecognised flag such as `linenums` yields `None` in `config`, which then reaches `_escape_attrib_html` (EV-003): this matches the reported `cannot serialize None` for the flag form. `True`/`False` values do not go through this path (RSK-001) |

### 4.7 Ignored instructions and out-of-scope requests
None. The issue text contains no instructions to the agent.

### 4.8 Maintainer answers
None (new run).

## 5. Validation

### 5.1 Dimension coverage
| Dimension | Coverage | Items / questions / n-a reason |
|---|---|---|
| D1 Problem and goal | covered | SRC-002, FR-001 |
| D2 Actors | covered | Library users of `markdown.markdown` with `fenced_code` + `attr_list` (SRC-001) |
| D3 Scope | partial | In scope stated (SRC-005, SRC-007); other codehilite-only keys unstated → Q-001, ASM-001 |
| D4 Required behaviour | covered | FR-001, FR-002, FR-003 |
| D5 Inputs and outputs | covered | AC-FR-001-1..5, AC-FR-002-1, AC-FR-003-1 |
| D6 Interfaces | covered | Public call `markdown.markdown` with extensions `fenced_code`, `attr_list`, `codehilite`; no new option |
| D7 Quality | covered | NFR-001 (preservation of existing output) |
| D8 Constraints | n/a | No constraint stated in the issue; no repository contribution rule was searched for this change |
| D9 Security | covered | NFR-002 (attribute-name and value escaping kept) |
| D10 Edge and failure behaviour | covered | Value forms in FR-001 ACs; `false` value Q-002 / ASM-002 |
| D11 Transition | n/a | The issue asks for no API, option or output change for existing working configurations; no changelog rule was checked |

### 5.2 Checks
| Check | Result (PASS / WARN / FAIL) | Findings |
|---|---|---|
| V1 Completeness | PASS | Every dimension covered, partial (D3 → Q-001) or n/a with reason. Every requirement SRC used. Every FR/NFR has ≥1 AC. TERM-001 recorded. FR-001 (behaviour-changing) has preservation ACs NFR-001-1..3 and NFR-002-1. |
| V2 Consistency | PASS | FR-001 and FR-002 agree: FR-002 excludes the ignored options. No incompatible behaviour. |
| V3 Traceability | PASS | All items have a Source. Quotes checked against the issue: SRC-005, SRC-006, SRC-007, SRC-008 are exact substrings. Repository sources cite EV rows with outcome success or not-found. |
| V4 Feasibility | PASS | Consistent with the existing `use_pygments` handling (EV-003). No CNF. RSK-001 notes an unverified value path. |
| V5 Testability | PASS | Each AC has a concrete input and extensions, the public call `markdown.markdown`, and one oracle kind. No unmeasurable qualifiers remain (TERM-001 is linked to Q-001). |
| V6 Integrity | PASS | No Confirmed item without a quote. No label was upgraded. No design or internal function named. Issue content was not executed; only the repository was read. Only `.autose_out/spec.md` was written. |

### 5.3 Readiness by item
| ID | Readiness | Reason |
|---|---|---|
| FR-001 | Needs-clarification | Q-001 open (default ASM-001); ACs Inferred |
| FR-002 | Needs-clarification | AC-FR-002-1 Inferred (constructed input) |
| FR-003 | Needs-clarification | AC-FR-003-1 Inferred |
| NFR-001 | Needs-clarification | Label Inferred; ACs Inferred |
| NFR-002 | Needs-clarification | Label Inferred; AC Inferred |

### 5.4 Stage gate
- Decision: PASS
- Reasons: ≥1 FR exists and every FR/NFR has ≥1 AC (V1); V5 PASS for every AC; V3 and V6 PASS; no P1 question and no CNF. Open questions Q-001 (P2) and Q-002 (P3) have proposed defaults ASM-001 and ASM-002.
- Spec-level verdict (§8.3): No item is Ready, because every AC is Inferred. This is informational only.
- Inferred acceptance criteria for maintainers to confirm on the pull request: AC-FR-001-1, AC-FR-001-2, AC-FR-001-3, AC-FR-001-4, AC-FR-001-5, AC-FR-002-1, AC-FR-003-1, AC-NFR-001-1, AC-NFR-001-2, AC-NFR-001-3, AC-NFR-002-1

### 5.5 Risks
- RSK-001 (Repository, EV-005, EV-008, EV-009): The `cannot serialize None` message is explained for the flag form (`linenums` → `None`). For `linenums=true` and `linenums="1"` the value is `True`, which does not pass through the `None` path, so the reported message for those forms is not verified. The `false` value path is also unverified. The fix must cover all value forms in AC-FR-001-1..5, and the implementation must confirm the behaviour by running the ACs.

## 6. Change log
| Version | Change | Reason (ANS / EV / validation) | Items |
|---|---|---|---|
| 0.1 | Initial spec from issue #4 | Issue text (SRC-001..009); repository evidence EV-001..EV-009 | FR-001..003, NFR-001..002, ASM-001..002, Q-001..002, TERM-001, RSK-001 |

## AutoSE stage check: all acceptance criteria are testable

Result: **PASS**

- all checks passed
