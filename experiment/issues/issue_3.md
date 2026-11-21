<!-- type: feature -->
# TOC: allow excluding individual headings from the table of contents

Feature request. In our docs, every page ends with headings like "Changelog" or "See also" that we don't want in the table of contents, but there is currently no way to leave a single heading out (only `toc_depth` for whole levels).

**Proposal:** if a heading has the class `notoc` (set with `attr_list`), leave it out of the TOC:

```markdown
[TOC]

# One

## Two {: .notoc }

## Three
```

should give a TOC with only "One" and "Three".

The heading itself should still be rendered normally, including its id, so existing links to it keep working. It should also be left out of `md.toc_tokens`, because we build our sidebar from that. Headings with other classes should behave exactly as today.

Python-Markdown 3.11.2.
