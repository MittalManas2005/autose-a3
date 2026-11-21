"""Hidden acceptance tests, issue 4: command-line option to set `tab_length`.

Run with the current working directory set to the root of the checkout under test.
"""
import os
import subprocess
import sys
import unittest

import markdown

SRC = '- a\n\n  - b\n'


def run_cli(*args):
    env = dict(os.environ)
    env['PYTHONPATH'] = os.getcwd() + os.pathsep + env.get('PYTHONPATH', '')
    return subprocess.run(
        [sys.executable, '-m', 'markdown', *args],
        input=SRC, capture_output=True, text=True, env=env, cwd=os.getcwd(), timeout=60,
    )


class TestHiddenIssue4(unittest.TestCase):

    def test_tab_length_option_equals_form(self):
        result = run_cli('--tab_length=2')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), markdown.markdown(SRC, tab_length=2, output_format='xhtml'))

    def test_tab_length_option_separate_value(self):
        result = run_cli('--tab_length', '2')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('<li>\n<p>a</p>\n<ul>\n<li>b</li>\n</ul>', result.stdout)

    def test_default_behaviour_is_unchanged(self):  # preservation
        result = run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), markdown.markdown(SRC, output_format='xhtml'))
