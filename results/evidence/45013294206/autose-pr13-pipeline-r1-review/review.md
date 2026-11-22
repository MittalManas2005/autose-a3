---
artefact: review
pr: 13
issue: 5
round: 1
verdict: approve
target_stage: none
reviewer_model: haiku
---

## AutoSE independent review (round 1)

**Verdict: approve**

PR #13 does what issue #5 asks. A heading with the class `notoc` is left out of the TOC and out of `md.toc_tokens`, but it is still rendered with its id, text and permalink. Other classes are unchanged, and children of an excluded heading stay in the TOC under the nearest included ancestor. The full suite and the TOC module pass, flake8 is clean, and my edge-case probes behaved as specified.

### What I verified
- Read the issue and the full diff (code, docs, changelog, tests).
- `python -m unittest discover tests` (run by me): Ran 1186 tests, OK (skipped=52).
- `python -m unittest tests.test_syntax.extensions.test_toc` (run by me): Ran 87 tests, OK.
- `python -m flake8 markdown/extensions/toc.py tests/test_syntax/extensions/test_toc.py`: no output, clean.
- Probe: issue example `[TOC]` with `## Two {: .notoc }` gives a TOC with only One and Three; the h2 keeps id="two" and renders normally.
- Probe: `# One {: .notoc }` followed by `## Two`/`### Three`/`## Four` gives top-level Two (with child Three) and Four in toc_tokens; no crash on an excluded top-level heading.
- Probe: all headings excluded gives an empty `<ul></ul>` toc div and an empty toc_tokens list, with no exception.
- Probe: a chain of excluded headings (`## Two` notoc, `### Sub`, `## Three` notoc, `### Sub2` notoc, `#### Deep`) nests Sub under One and Deep under Sub, as documented.
- Probe: toc_depth '2-3' with notoc headings excludes Two and Four, and the remaining levels behave as toc_depth already does.
- Probe: duplicate heading ids with notoc keep unique ids (two, two_1, two_2), and the notoc heading is still excluded from the TOC.
- Probe: near-miss class `notoc-like` is not excluded; `{: class }` with no value does not crash (handled via `or ""`).
- Checked the permalink path: the notoc heading keeps `class="headerlink"` and is absent from md.toc.
- Checked the changelog and docs entries: both describe the behaviour, including that existing `notoc` classes are affected.

### Commands I ran (from the session transcript, not self-reported)
- `python -m unittest discover tests` (ok)
- `python -m unittest tests.test_syntax.extensions.test_toc` (ok)
- `python -c "import markdown; md=markdown.Markdown(extensions=['toc','attr_list']); h=md.convert('# One {: .notoc }\n\n## Two\n\n### Three\n\n## Four'); print(h);` (ok)
- `python -c "import markdown; md=markdown.Markdown(extensions=['toc','attr_list']); h=md.convert('[TOC]\n\n# One {: .notoc }\n\n## Two {: .notoc }\n'); print(h); ` (ok)
- `python -c "import markdown; md=markdown.Markdown(extensions=['toc','attr_list'], extension_configs={'toc':{'toc_depth':'2-3'}}); h=md.convert('[TOC]\n\n# One\n\` (ok)
- `python -c "import markdown; md=markdown.Markdown(extensions=['toc','attr_list']); h=md.convert('# One\n\n## Two {: .notoc }\n\n## Two {: .notoc }\n\n## Two'); p` (ok)
- `python -m flake8 markdown/extensions/toc.py tests/test_syntax/extensions/test_toc.py` (ok)
- `python -c "import markdown; md=markdown.Markdown(extensions=['toc','attr_list']); h=md.convert('[TOC]\n\n# One\n\n## Two {: .notoc }\n\n### Sub\n\n## Three {: .` (ok)
- `python -c "import markdown; md=markdown.Markdown(extensions=['toc','attr_list']); h=md.convert('# One\n\n## Two {: .notoc }\n\n## Three\n\n## Four {: .notoc-lik` (ok)

### Findings

| severity | location | issue | evidence |
|---|---|---|---|
| minor | `tests/test_syntax/extensions/test_toc.py` | Many of the new `test_ac_fr_*` tests duplicate the earlier `test_notoc_*` tests with the same inputs and assertions, and there are two near-identical nested id-collecting helpers (`_toc_token_ids` and an inline `collect_ids`). This adds bulk without adding coverage. | Test file lines ~61-67 (`_toc_token_ids`), ~196-265 and ~304-328 (`test_ac_fr_*`), and ~318-323 (`collect_ids`) repeat the inputs of tests at ~69-184. |

_The reviewer saw only the issue, the diff and the repository at this PR's head. A maintainer decides whether to merge._
