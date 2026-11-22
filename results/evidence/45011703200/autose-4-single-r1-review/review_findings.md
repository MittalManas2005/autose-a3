# Independent reviewer findings (address every item)

The fix filters highlight-only options (linenums, guess_lang, noclasses, use_pygments, hl_lines) out of the `<code>` attributes when highlighting is not applied. The TypeError is gone, other attributes are kept, and the tests pass.


