# Issue #7: Links with code in them don't work sometimes

<untrusted_issue>
Some of my links that have code formatting in them don't turn into links, the brackets just show up in the page. Other links with code in them are fine, so I'm not sure what the difference is. Can this be fixed?

Python-Markdown 3.11.2

</untrusted_issue>

## Maintainer answers (clarifications posted on the issue; part of the requirements)

<untrusted_answers>
It's reference-style links where the label has backticks in it. For example `[`foo`]` with a definition `[`foo`]: https://example.com`, or `[text][`foo`]` with the same definition. Those should become links like any other reference link. Inline links like `[`foo`](https://example.com)` already work.
</untrusted_answers>

<untrusted_answers>
It's reference-style links where the label has backticks in it. For example `[`foo`]` with a definition `[`foo`]: https://example.com`, or `[text][`foo`]` with the same definition. Those should become links like any other reference link. Inline links like `[`foo`](https://example.com)` already work.
</untrusted_answers>

<untrusted_answers>
It's reference-style links where the label has backticks in it. For example `[`foo`]` with a definition `[`foo`]: https://example.com`, or `[text][`foo`]` with the same definition. Those should become links like any other reference link. Inline links like `[`foo`](https://example.com)` already work.
</untrusted_answers>
