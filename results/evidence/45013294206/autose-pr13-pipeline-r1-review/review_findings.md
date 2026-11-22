# Independent reviewer findings (address every item)

PR #13 does what issue #5 asks. A heading with the class `notoc` is left out of the TOC and out of `md.toc_tokens`, but it is still rendered with its id, text and permalink. Other classes are unchanged, and children of an excluded heading stay in the TOC under the nearest included ancestor. The full suite and the TOC module pass, flake8 is clean, and my edge-case probes behaved as specified.


