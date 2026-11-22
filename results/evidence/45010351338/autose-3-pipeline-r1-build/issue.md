# Issue #3: TOC extension crashes with TypeError when a heading has `{: id }` without a value

Author: MittalManas2005

<untrusted_issue>
I'm using `toc` together with `attr_list`. While drafting a document I left an attribute list on a heading with just `id` (I meant to fill in the value later), and the whole conversion blew up:

```python
import markdown
markdown.markdown("# Heading {: id }", extensions=["toc", "attr_list"])
```

```
  File ".../markdown/extensions/toc.py", line 417, in run
    'id': unescape(el.attrib["id"]),
  ...
TypeError: expected string or bytes-like object, got 'NoneType'
```

Without `toc` it doesn't crash (`attr_list` alone gives `<h1 id>Heading</h1>`), and `{: id="intro" }` works fine with `toc`.

**Expected:** no crash. A heading with an empty `id` should just be treated like a heading without an id: it gets the normal auto-generated id and shows up in the table of contents like every other heading. Ids I set explicitly should keep working as they do now.

Python-Markdown 3.11.2 (git `3f2c551`), Python 3.12, macOS.

</untrusted_issue>
