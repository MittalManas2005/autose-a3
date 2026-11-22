# Issue #1: TOC crashes when `data-toc-label` has no value

Author: MittalManas2005

<untrusted_issue>
I use `toc` together with `attr_list`, and set `data-toc-label` on some headings to get shorter entries in the table of contents. While editing, I left one heading with just the attribute name and no value, and the conversion crashed:

```python
import markdown
markdown.markdown("# Heading {: data-toc-label }", extensions=["toc", "attr_list"])
```

```
  File ".../markdown/extensions/toc.py", line 408, in run
    data_toc_label = run_postprocessors(unescape(el.attrib['data-toc-label']), self.md)
  File ".../markdown/extensions/toc.py", line 124, in unescape
    return c.unescape(text)
  ...
TypeError: expected string or bytes-like object, got 'NoneType'
```

Without `toc` there is no crash, and `{: data-toc-label="Short" }` works fine with `toc`.

**Expected:** no crash. An empty `data-toc-label` should be ignored, so the heading text is used in the table of contents, as if the attribute were not there. Version 3.11.2 (current main).

</untrusted_issue>
