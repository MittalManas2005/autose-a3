"""Hidden acceptance tests, issue 2: fenced code boolean options crash when codehilite is not enabled."""
import markdown
from markdown.test_tools import TestCase

EXTS = ['fenced_code', 'attr_list']
PLAIN = '``` { .python }\nprint(1)\n```'


class TestHiddenIssue2(TestCase):

    def test_linenums_is_ignored_without_codehilite(self):
        src = '``` { .python linenums }\nprint(1)\n```'
        self.assertEqual(markdown.markdown(src, extensions=EXTS), markdown.markdown(PLAIN, extensions=EXTS))

    def test_other_codehilite_options_are_ignored_without_codehilite(self):
        for option in ('linenums=true', 'linenums="1"', 'guess_lang', 'noclasses'):
            with self.subTest(option=option):
                src = '``` { .python %s }\nprint(1)\n```' % option
                html = markdown.markdown(src, extensions=EXTS)
                self.assertEqual(html, markdown.markdown(PLAIN, extensions=EXTS))

    def test_custom_attributes_are_still_passed_through(self):  # preservation
        self.assertMarkdownRenders(
            '``` { .python data-x="y" }\nprint(1)\n```',
            '<pre><code class="language-python" data-x="y">print(1)\n</code></pre>',
            extensions=EXTS,
        )
