"""End-to-end test of the build job's state machine with a fake `claude` (no model calls).

Needs a git clone of Python-Markdown that contains the pinned commit, and a Python environment with
`markdown[testing]` dependencies + flake8 + PyYAML. Skipped unless AUTOSE_TEST_CLONE is set:

    AUTOSE_TEST_CLONE=/path/to/markdown-clone python -m unittest autose.tests.test_flow -v
"""
from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import textwrap
import unittest
import unittest.mock
from pathlib import Path

PIN = "3f2c5510bd8d64a73ec18342f740371bcde9b20c"
HERE = Path(__file__).resolve().parent
AUTOSE_PKG = HERE.parent
CLONE = os.environ.get("AUTOSE_TEST_CLONE")

SPEC = textwrap.dedent("""\
    ---
    artefact: spec
    issue: 1
    status: PASS
    ac_ids: [AC-FR-001-1, AC-FR-001-2]
    inferred_ac_ids: [AC-FR-001-2]
    blocking_questions: []
    ---
    # Spec for issue #1
    ## 2. Requirements
    ### FR-001 — A valueless id does not crash the TOC
    - Acceptance criteria:
      - AC-FR-001-1 [Confirmed] (no-error): Given "# Heading {: id }" with extensions ["toc", "attr_list"], when converted with markdown.markdown, then no exception is raised.
      - AC-FR-001-2 [Inferred] (contains): Given "# Heading {: id }" with ["toc", "attr_list"], when converted, then the output contains '<h1 id="heading">'.
    """)
SPEC_NEEDS_INPUT = SPEC.replace("status: PASS", "status: NEEDS_INPUT").replace(
    "blocking_questions: []", "blocking_questions: [Q-001]")
DESIGN = textwrap.dedent("""\
    ---
    artefact: design
    issue: 1
    files:
      - path: markdown/extensions/toc.py
        change: modify
        symbols: [TocTreeprocessor.run]
        new_symbols: []
      - path: docs/changelog.md
        change: modify
        symbols: []
        new_symbols: []
    tests: tests/test_syntax/extensions/test_toc.py
    ---
    ## Plan
    Treat a valueless id like a missing one.
    ## ARCHITECTURE.md vs source
    Verified toc.py:417 (unescape of the id). No discrepancies.
    """)
TESTS_GOOD = textwrap.dedent('''\
    from markdown.test_tools import TestCase


    class TestAutoseIssue(TestCase):

        def test_ac_fr_001_1_no_crash(self):
            """AC-FR-001-1"""
            self.assertMarkdownRenders('# Heading {: id }', '<h1 id="heading">Heading</h1>',
                                       extensions=['toc', 'attr_list'])

        def test_ac_fr_001_2_generated_id(self):
            """AC-FR-001-2"""
            import markdown
            self.assertIn('<h1 id="heading">', markdown.markdown('# Heading {: id }', extensions=['toc', 'attr_list']))
    ''')
TESTS_VACUOUS = textwrap.dedent('''\
    from markdown.test_tools import TestCase


    class TestAutoseIssue(TestCase):

        def test_ac_fr_001_1_and_ac_fr_001_2_explicit_id(self):
            """AC-FR-001-1 AC-FR-001-2 (does not exercise the bug)"""
            self.assertMarkdownRenders('# Heading {: id="x" }', '<h1 id="x">Heading</h1>',
                                       extensions=['toc', 'attr_list'])
    ''')


@unittest.skipUnless(CLONE, "set AUTOSE_TEST_CLONE to a Python-Markdown clone to run the flow test")
class TestFlow(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.fixtures = Path(tempfile.mkdtemp(prefix="autose-fix-"))
        (cls.fixtures / "spec.md").write_text(SPEC)
        (cls.fixtures / "spec_needs_input.md").write_text(SPEC_NEEDS_INPUT)
        (cls.fixtures / "design.md").write_text(DESIGN)
        (cls.fixtures / "tests_good.py").write_text(TESTS_GOOD)
        (cls.fixtures / "tests_vacuous.py").write_text(TESTS_VACUOUS)
        fix = subprocess.run(["git", "diff", "dc26ab5^", "dc26ab5", "--", "markdown"], cwd=CLONE,
                             text=True, capture_output=True, check=True).stdout
        (cls.fixtures / "fix_code_only.patch").write_text(fix)
        cls.bin = Path(tempfile.mkdtemp(prefix="autose-bin-"))
        fake = cls.bin / "claude"
        fake.write_text(f"#!{sys.executable}\n" + (HERE / "fake_claude.py").read_text())
        fake.chmod(fake.stat().st_mode | stat.S_IEXEC)

    def run_build(self, scenario: str, **extra: str) -> tuple[dict, Path]:
        wt = Path(tempfile.mkdtemp(prefix="autose-wt-")) / "fork"
        subprocess.run(["git", "worktree", "add", "--detach", str(wt), PIN], cwd=CLONE, check=True,
                       capture_output=True)
        self.addCleanup(subprocess.run, ["git", "worktree", "remove", "--force", str(wt)], cwd=CLONE,
                        capture_output=True)
        shutil.copytree(AUTOSE_PKG, wt / "autose", ignore=shutil.ignore_patterns("tests", "__pycache__"))
        # Like the real fork: the AutoSE code is committed on main, and that commit is the base.
        for cmd in (["git", "add", "autose"], ["git", "-c", "user.name=t", "-c", "user.email=t@t",
                                               "commit", "-q", "-m", "add autose"]):
            subprocess.run(cmd, cwd=wt, check=True, capture_output=True)
        base = subprocess.run(["git", "rev-parse", "HEAD"], cwd=wt, text=True, capture_output=True).stdout.strip()
        (wt / ".autose_out").mkdir()
        (wt / ".autose_out" / "issue.json").write_text(json.dumps(
            {"number": 1, "title": "TOC crashes on {: id }", "body": "crash", "author": {"login": "u"}}))
        env = dict(os.environ, PATH=f"{self.bin}{os.pathsep}{Path(sys.executable).parent}{os.pathsep}"
                                    f"{os.environ['PATH']}",
                   FAKE_FIXTURES=str(self.fixtures), FAKE_SCENARIO=scenario,
                   CLAUDE_CONFIG_DIR=tempfile.mkdtemp(prefix="autose-claude-"), **extra)
        proc = subprocess.run([sys.executable, "-m", "autose.orchestrator", "--issue", "1", "--round", "1",
                               "--start-stage", "requirements", "--base-sha", base], cwd=wt, env=env,
                              text=True, capture_output=True, timeout=900)
        self.assertEqual(proc.returncode, 0, proc.stdout[-3000:] + proc.stderr[-3000:])
        state = json.loads((wt / ".autose_out" / "run_state.json").read_text())
        return state, wt

    def test_happy_path_reaches_release(self):
        state, wt = self.run_build("happy")
        self.assertEqual(state["status"], "ready", state)
        out = wt / ".autose_out"
        for name in ("spec.md", "design.md", "diff.patch", "round.patch", "test_report.md", "usage.json"):
            self.assertTrue((out / name).exists(), name)
        patch = (out / "diff.patch").read_text()
        self.assertIn("markdown/extensions/toc.py", patch)
        self.assertIn("docs/changelog.md", patch)
        self.assertNotIn(".autose_out", patch)
        self.assertIn("Result: **PASS**", (out / "test_report.md").read_text())

    def test_build_check_failure_retries_implementer(self):
        state, _ = self.run_build("build_retry")
        self.assertEqual(state["status"], "ready", state)
        retries = [t for t in state["transitions"] if t["reason"].startswith("build check failed")]
        self.assertEqual(len(retries), 1)

    def test_vacuous_tests_send_work_back_to_tester(self):
        state, _ = self.run_build("vacuous_tests")
        self.assertEqual(state["status"], "ready", state)
        self.assertTrue(any(t["reason"].startswith("vacuous") for t in state["transitions"]), state["transitions"])

    def test_needs_input_stops_at_stage_one(self):
        state, wt = self.run_build("needs_input")
        self.assertEqual(state["status"], "needs_input")
        self.assertEqual(state["stop_stage"], 1)
        self.assertTrue((wt / ".autose_out" / "STOPPED.md").exists())

    def test_broken_sandbox_stops_at_once_with_environment_reason(self):
        state, wt = self.run_build("sandbox_broken")
        self.assertEqual((state["status"], state["stop_stage"]), ("failed", 3))
        self.assertIn("sandbox is unavailable", state["stop_reason"])
        self.assertIn("not a code defect", state["stop_reason"])
        self.assertEqual((wt / ".autose_out" / ".fake_implementer_calls").read_text(), "1")  # no retries
        self.assertTrue((wt / ".autose_out" / "logs" / "3-implementation-implementer-1.transcript.jsonl").exists())

    def test_guard_violation_stops_the_run(self):
        state, _ = self.run_build("guard_violation")
        self.assertEqual(state["status"], "failed")
        self.assertIn(".github", json.dumps(state["checks"]))


@unittest.skipUnless(CLONE and shutil.which("aspell"), "needs AUTOSE_TEST_CLONE, aspell and pyspelling")
class TestSpellingCheck(unittest.TestCase):
    """The stage 3/4 spell check reproduces CI's `checkspelling` failure from baseline run 45008881976."""

    def test_new_misspelling_in_test_docstring_is_reported(self):
        sys.path.insert(0, str(AUTOSE_PKG.parent))
        from autose import checks
        wt = Path(tempfile.mkdtemp(prefix="autose-spell-")) / "fork"
        subprocess.run(["git", "worktree", "add", "--detach", str(wt), PIN], cwd=CLONE, check=True, capture_output=True)
        self.addCleanup(subprocess.run, ["git", "worktree", "remove", "--force", str(wt)], cwd=CLONE,
                        capture_output=True)
        test_file = wt / "tests" / "test_autose_spelling.py"
        env_path = f"{Path(sys.executable).parent}{os.pathsep}{os.environ['PATH']}"
        with unittest.mock.patch.dict(os.environ, {"PATH": env_path}):
            if not checks.spelling_available(wt):
                self.skipTest("pyspelling not importable by `python`")
            test_file.write_text('def test_a():\n    """Given ["toc", "attr_list"] the attr is kept."""\n')
            bad = checks.check_spelling(wt, PIN, ["tests/test_autose_spelling.py"])
            test_file.write_text('def test_a():\n    """Given `["toc", "attr_list"]` the `attr` is kept."""\n')
            good = checks.check_spelling(wt, PIN, ["tests/test_autose_spelling.py"])
            unchanged = checks.check_spelling(wt, PIN, ["docs/changelog.md"])  # words already in `main` don't count
        self.assertFalse(bad.ok)
        self.assertIn("attr", bad.data["misspelled"]["tests/test_autose_spelling.py"])
        self.assertTrue(good.ok, good.reasons)
        self.assertTrue(unchanged.ok, unchanged.reasons)


if __name__ == "__main__":
    unittest.main()
