# Independent reviewer findings (address every item)

The change fixes the reported crash. Without codehilite, `linenums`, `guess_lang` and `noclasses` are dropped from the `<code>` attributes when attr_list is on, and other attributes such as `data-x` are still emitted. The full suite passes (1183 tests, 52 skipped), flake8 is clean on both changed files, and the changelog entry is in place. One related crash path remains when codehilite is enabled with use_pygments=False; it is pre-existing and outside the issue's literal scope, so I list it as a minor note.


