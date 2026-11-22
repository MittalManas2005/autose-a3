---
artefact: design
issue: 4
files:
  - path: markdown/extensions/fenced_code.py
    change: modify
    symbols: [FencedBlockPreprocessor.__init__, FencedBlockPreprocessor.run]
    new_symbols: []
  - path: tests/test_syntax/extensions/test_fenced_code.py
    change: modify
    symbols: []
    new_symbols: []
  - path: docs/changelog.md
    change: modify
    symbols: []
    new_symbols: []
tests: tests/test_syntax/extensions/test_fenced_code.py
---

## Plan

The crash happens in the non-highlight branch of `FencedBlockPreprocessor.run` (`markdown/extensions/fenced_code.py:146-164`). When `use_attr_list` is true and the block has any config keys, every key except `use_pygments` is written to the `<code>` element as an attribute (`fenced_code.py:155-162`). The codehilite-only keys `linenums`, `guess_lang` and `noclasses` are in `bool_options` (`fenced_code.py:84-89`). `handle_attrs` turns them into `None` (valueless flag, via `parseBoolValue(..., fail_on_errors=False)` at `fenced_code.py:193`) or into `True`/`False` (`=true`, `=1`, `=false`). The serializer then calls `_escape_attrib_html` on a non-string, which raises `TypeError` (`serializers.py:123-137`).

**Change (`markdown/extensions/fenced_code.py`).**
1. In `FencedBlockPreprocessor.__init__`, add an instance attribute next to `bool_options`:
   `self.codehilite_only_options = ('linenums', 'guess_lang', 'noclasses')`.
2. In `FencedBlockPreprocessor.run`, in the `kv_pairs` comprehension (`fenced_code.py:159-162`), also skip keys in `self.codehilite_only_options`:
   `for k, v in config.items() if k != 'use_pygments' and k not in self.codehilite_only_options`.
   The `if` guard on line 155 stays as it is. If every key is filtered out, `kv_pairs` is `''` and the output is the same as a block without the options.
   The `codehilite` highlight path (`fenced_code.py:127-145`) is not touched, and `handle_attrs` still parses the values, so `lang`, `classes`, `id` and `hl_lines` are unchanged.

Acceptance criteria covered:
- AC-FR-001-1..5 (`linenums`, `linenums=true`, `linenums="1"`, `guess_lang noclasses`, `linenums=false`): the three keys are dropped from `kv_pairs`, so the output is `<pre><code class="language-python">print(1)\n</code></pre>`.
- AC-FR-002-1 (`data-x="y"` kept, `linenums` dropped): `data-x` is still emitted through `sanitize_name` and `_escape_attrib_html`.
- AC-FR-003-1 (codehilite enabled): the highlight branch is unchanged; no new code runs on that path.
- AC-NFR-001-1..3 (`foo=bar`, `use_pygments`, no `attr_list`): the only added condition removes three keys, so these outputs are unchanged.
- AC-NFR-002-1 (escaping): values still go through `sanitize_name` and `_escape_attrib_html`.

**Tests (`tests/test_syntax/extensions/test_fenced_code.py`).** Add cases next to the existing `attr_list` tests in `TestFencedCode` (around lines 296-361) that use `assertMarkdownRenders` for AC-FR-001-1..5, AC-FR-002-1 and AC-NFR-002-1 (the spec's exact strings). Add one no-error case for AC-FR-003-1 in `TestFencedCodeWithCodehilite` (around line 459), or a short test that calls `markdown.markdown` and checks the output is non-empty, because the highlighted output depends on whether Pygments is installed (EV-004). AC-NFR-001-1..3 can be checked by the existing tests (EV-007) plus one no-`attr_list` case (AC-NFR-001-3).

**Changelog (`docs/changelog.md`).** Add a bullet under `## [Unreleased]` → `### Fixed` (the section is at line 15-17): fenced code blocks with `linenums`, `guess_lang` or `noclasses` no longer crash when `fenced_code` and `attr_list` are enabled without `codehilite`; the options are ignored.

## Constraints respected

- **K1 (stage interfaces):** no processor signature or return type changes.
- **K2 (registries and priorities):** no processor is added, renamed or re-prioritised. `fenced_code_block` stays at 25.
- **K3 (attribute values are `str` or `None`):** the fix removes the non-string values (`None`, `True`, `False`) from this path before serialization. The remaining config values are strings (`use_pygments` is still excluded). Note: `hl_lines` can still produce a list (see Risks), which is a pre-existing issue and not changed here.
- **K4 (stash and placeholders):** unchanged; the fenced block still goes through `md.htmlStash.store`.
- **K5 (backward compatibility):** no public name, option or dependency changes. Only configurations that crash today change behaviour. Every key being dropped is always `None` or a `bool` in this branch, and both always raise, so no currently working output changes.
- **Security (NFR-002):** the kept attributes still go through `sanitize_name` and `_escape_attrib_html` (`fenced_code.py:160`).
- **Changelog rule:** a `docs/changelog.md` entry under `[Unreleased]` is required, since `markdown/` changes.
- **Style:** the line length limit is 119 (flake8).

Scope decision: the filter is unconditional (it does not check whether `codehilite` is enabled). FR-001 is written for the case where `codehilite` is not enabled. The unconditional filter also covers `codehilite` enabled with `use_pygments: False` plus `attr_list`, which also crashes today and is not covered by a spec AC. I chose the unconditional filter because the keys are always invalid in this branch. The extra case is listed under Risks.

## ARCHITECTURE.md vs source

Verified by reading the source (not executed; this role has no shell):

| Claim | Source check | Result |
|---|---|---|
| `fenced_code_block` registered at priority 25 (ARCH C2, 2.2) | `markdown/extensions/fenced_code.py:58` | Match |
| `bool_options` list and `use_pygments` omitted from output (spec EV-003) | `fenced_code.py:84-89`, `fenced_code.py:155-162` | Match (the comment is at 157-158) |
| `handle_attrs` maps valueless keys to the key name, then `parseBoolValue(..., preserve_none=True)` (spec EV-005) | `fenced_code.py:182-193` | Match |
| `parseBoolValue` returns `None` for an unknown value when `fail_on_errors=False` (spec EV-009) | `markdown/util.py:136-152` | Match |
| Serializer raises `TypeError("cannot serialize …")` for non-strings; `None` is a bare attribute (ARCH C5, K3) | `markdown/serializers.py:80-83`, `serializers.py:186-196` | Match |
| `_escape_attrib_html` lives in `serializers.py` (spec EV-008 said not found in `util.py`) | `serializers.py:123-137`; `fenced_code.py:30` imports it from there | Match (ARCH does not name the file for this function) |
| `sanitize_name` keeps hyphens by replacing only non-name characters (spec EV-006) | `markdown/extensions/attr_list.py:106-111` | Match (the regex is not read; the `data-` test case in EV-006 is trusted) |
| `parse_hl_lines` returns `list[int]` (used in the `hl_lines` path) | `markdown/extensions/codehilite.py:43` | Match |

**Discrepancies (the source wins):**
1. **Spec RSK-001 is wrong about `linenums=true` and `linenums="1"`.** The spec says these values do not go through the `None` path, so the reported error message is unverified. In fact `parseBoolValue` returns `True` for them, and `_escape_attrib_html(True)` fails on `"&" in True` (`TypeError: argument of type 'bool' is not iterable`). That is caught at `serializers.py:136-137`, and `_raise_serialization_error` reports `cannot serialize True (type bool)`. So all five value forms in AC-FR-001-1..5 crash, not just the flag form. The fix covers all of them, so the plan does not change. The implementer should expect the message to name `True`/`False` for those forms.
2. **Spec EV-008 is not a discrepancy but a location note:** `_escape_attrib_html` is in `serializers.py`, not in `util.py`.
3. **Checkout identity (not verified):** ARCHITECTURE.md pins `3f2c551`. The spec's `base_commit` is `758ab06`. I did not run `git` (no shell in this role), so I could not confirm the checkout matches the pinned commit. The line numbers I checked match ARCHITECTURE.md and the spec, so the source looks like the same version.

## Risks

- **Option scope (Q-001, ASM-001):** only the three named keys are filtered. `hl_lines` is not filtered. With `attr_list` and no `codehilite`, `{ .python hl_lines="1" }` gives `configs['hl_lines'] = [1]`. `_escape_attrib_html` accepts a list without raising (`"&" in [1]` is valid), so the output would be `hl_lines="[1]"` instead of a crash. This is outside the spec's scope and no AC covers it. I did not change it. Flag this for the maintainer; a broader filter would need Q-001 to be answered.
- **Unconditional filter (see Scope decision):** `codehilite` enabled with `use_pygments: False` and `attr_list` now renders instead of crashing. No spec AC covers this case. The highlight path is unchanged.
- **Unverified run:** this design was written by reading code only. The implementer must run the new tests and `python -m flake8` to confirm the exact strings in the ACs, in particular the `\n` at the end of the code body.
- **Assumed test position:** the new tests go in `TestFencedCode` and `TestFencedCodeWithCodehilite`. If the implementer prefers a new test class, that is fine as long as the module stays under `tests/test_syntax/extensions/`.

## AutoSE stage check: names the files and functions to change

Result: **PASS**

- all checks passed
