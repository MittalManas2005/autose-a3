"""Hidden acceptance tests, issue 3: exclude a heading from the TOC with the class `notoc`."""
import re
import markdown
from markdown.test_tools import TestCase

EXTS = ['toc', 'attr_list']
SRC = '[TOC]\n\n# One\n\n## Two {: .notoc }\n\n## Three\n'


def flatten_ids(tokens):
    ids = []
    for token in tokens:
        ids.append(token['id'])
        ids.extend(flatten_ids(token['children']))
    return ids


def toc_div(html):
    return html.split('</div>', 1)[0]


class TestHiddenIssue3(TestCase):

    def test_notoc_heading_is_not_listed_in_toc(self):
        toc = toc_div(markdown.markdown(SRC, extensions=EXTS))
        self.assertIn('href="#one"', toc)
        self.assertIn('href="#three"', toc)
        self.assertNotIn('href="#two"', toc)

    def test_notoc_heading_is_still_rendered_with_its_id(self):
        html = markdown.markdown(SRC, extensions=EXTS)
        self.assertRegex(html, re.compile(r'<h2[^>]*\bid="two"[^>]*>Two</h2>'))

    def test_notoc_heading_is_not_in_toc_tokens(self):
        md = markdown.Markdown(extensions=EXTS)
        md.convert(SRC)
        self.assertEqual(flatten_ids(md.toc_tokens), ['one', 'three'])

    def test_other_classes_do_not_exclude_headings(self):  # preservation
        md = markdown.Markdown(extensions=EXTS)
        md.convert('# One {: .other }\n\n## Two\n')
        self.assertEqual(flatten_ids(md.toc_tokens), ['one', 'two'])
