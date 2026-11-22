# Issue #6: Command line: add an option to set `tab_length`

<untrusted_issue>
From Python I can do `markdown.markdown(text, tab_length=2)`, which I need because our files indent nested lists with 2 spaces. But the command line (`python -m markdown` / `markdown_py`) has no way to set it, so the same files render differently in our build script:

```console
$ printf -- '- a\n\n  - b\n' | python -m markdown
```

renders `b` as a second top-level item instead of a nested list.

**Request:** add a `--tab_length` option to the command line, used like the existing options (both `--tab_length=2` and `--tab_length 2`). It should behave the same as passing `tab_length` to `markdown.markdown()`. When the option isn't given, the output should stay exactly as it is now.

Python-Markdown 3.11.2, Python 3.12.

</untrusted_issue>
