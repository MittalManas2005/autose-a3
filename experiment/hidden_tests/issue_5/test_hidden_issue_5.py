"""Hidden acceptance tests, issue 5 (vague): reference-style links whose label contains inline code."""
from markdown.test_tools import TestCase

URL = 'https://example.com'


class TestHiddenIssue5(TestCase):

    def test_shortcut_reference_with_code_label(self):
        self.assertMarkdownRenders(
            '[`x`]\n\n[`x`]: %s' % URL,
            '<p><a href="%s"><code>x</code></a></p>' % URL,
        )

    def test_collapsed_reference_with_code_in_label(self):
        self.assertMarkdownRenders(
            '[a `x` b][]\n\n[a `x` b]: %s' % URL,
            '<p><a href="%s">a <code>x</code> b</a></p>' % URL,
        )

    def test_full_reference_with_code_in_id(self):
        self.assertMarkdownRenders(
            '[text][`x`]\n\n[`x`]: %s' % URL,
            '<p><a href="%s">text</a></p>' % URL,
        )

    def test_undefined_code_label_stays_literal(self):  # preservation
        self.assertMarkdownRenders(
            '[`y`]\n\n[`x`]: %s' % URL,
            '<p>[<code>y</code>]</p>',
        )
