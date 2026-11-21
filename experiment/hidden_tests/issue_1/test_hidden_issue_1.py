"""Hidden acceptance tests, issue 1: TOC crashes on a heading with a valueless `id` attribute."""
import markdown
from markdown.test_tools import TestCase

EXTS = ['toc', 'attr_list']


class TestHiddenIssue1(TestCase):

    def test_valueless_id_does_not_crash_and_gets_generated_id(self):
        self.assertMarkdownRenders('# Heading {: id }', '<h1 id="heading">Heading</h1>', extensions=EXTS)

    def test_valueless_id_heading_is_listed_in_toc(self):
        md = markdown.Markdown(extensions=EXTS)
        html = md.convert('[TOC]\n\n# Heading {: id }')
        self.assertIn('<a href="#heading">Heading</a>', html)
        self.assertEqual([token['id'] for token in md.toc_tokens], ['heading'])

    def test_valueless_id_gets_unique_generated_id(self):
        self.assertMarkdownRenders(
            '# Same\n\n# Same {: id }',
            '<h1 id="same">Same</h1>\n<h1 id="same_1">Same</h1>',
            extensions=EXTS,
        )

    def test_explicit_id_is_still_respected(self):  # preservation: passes before and after a fix
        self.assertMarkdownRenders('# Heading {: id="custom" }', '<h1 id="custom">Heading</h1>', extensions=EXTS)
