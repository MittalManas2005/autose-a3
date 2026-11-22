# Independent reviewer findings (address every item)

The new --tab_length option defaults to 2, but the library default is 4. Output changes when the option isn't given, which the issue forbids.

- [blocker] markdown/__main__.py:69 default=2 changes the CLI's default tab length from 4 to 2. Existing users with 4-space indented nested lists get different output, which breaks 'When the option isn't given, the output should stay exactly as it is now'. — evidence: Input '- a\n\n    - b\n' through `python -m markdown` with no option produces '<li>a<pre><code>- b\n</code></pre>' instead of a nested <ul>. Fix: default=4 (or leave it out of opts when not given).
- [major] tests/test_apis.py:800 The test default_options was changed to expect 'tab_length': 2, which locks in the wrong default. No test checks end-to-end rendering with the option or that the default matches markdown.markdown. — evidence: diff adds `'tab_length': 2` to default_options. After the fix this should be 4, and the tests should cover the issue's example ('- a\n\n  - b\n' with --tab_length=2).
