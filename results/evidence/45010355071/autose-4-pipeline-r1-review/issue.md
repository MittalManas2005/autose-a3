# Issue #4: Fenced code block with `linenums` crashes when codehilite is not enabled

<untrusted_issue>
I share Markdown files between two sites. One uses `codehilite`, the other only `fenced_code` + `attr_list`. On the second site, any code block that asks for line numbers crashes the conversion:

```python
import markdown
src = "``` { .python linenums }\nprint(1)\n```"
markdown.markdown(src, extensions=["fenced_code", "attr_list"])
```

```
TypeError: cannot serialize None (type NoneType)
```

Same with `linenums=true`, `linenums="1"`, `guess_lang` and `noclasses`. With `codehilite` enabled everything is fine.

**Expected:** these options only mean something for syntax highlighting, so without `codehilite` they should simply be ignored and the block rendered exactly as if I hadn't written them. Other attributes on the block (e.g. `data-x="y"`) should still end up on the `<code>` element like they do today.

Python-Markdown 3.11.2 (git `3f2c551`), Python 3.11.

</untrusted_issue>
