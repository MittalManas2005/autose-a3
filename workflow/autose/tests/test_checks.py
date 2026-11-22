"""Unit tests for the deterministic parts of AutoSE (no model calls).

Run from autose-a3/workflow:  python -m unittest discover -s autose/tests -t .
"""
from __future__ import annotations

import json
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest import mock

from autose import checks, claude_runner, gate, review

SPEC_OK = textwrap.dedent("""\
    ---
    status: PASS
    ac_ids: [AC-FR-001-1, AC-FR-001-2]
    inferred_ac_ids: [AC-FR-001-2]
    blocking_questions: []
    ---
    # Spec
    ### FR-001 — no crash
    - Acceptance criteria:
      - AC-FR-001-1 [Confirmed] (no-error): Given "# H {: id }" with ["toc", "attr_list"], when converted, then no exception.
      - AC-FR-001-2 [Inferred] (contains): Given "# H {: id }", when converted, then the output contains '<h1 id="h">'.
    """)


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=repo, text=True, capture_output=True, check=True).stdout


class TestSpecCheck(unittest.TestCase):
    def test_valid_spec_passes(self):
        chk = checks.check_spec(SPEC_OK)
        self.assertTrue(chk.ok, chk.reasons)
        self.assertEqual(chk.data["ac_ids"], ["AC-FR-001-1", "AC-FR-001-2"])

    def test_missing_oracle_fails(self):
        chk = checks.check_spec(SPEC_OK.replace("(contains)", ""))
        self.assertFalse(chk.ok)
        self.assertIn("AC-FR-001-2", chk.reasons[0])

    def test_preservation_marker_accepted(self):
        # Run 45008926010 wrote "(contains, preservation)"; the prompt now asks for "(contains) (preservation)".
        for form in ("(contains, preservation)", "(contains) (preservation)", "(contains)(preservation)"):
            chk = checks.check_spec(SPEC_OK.replace("[Inferred] (contains)", f"[Inferred] {form}"))
            self.assertTrue(chk.ok, (form, chk.reasons))

    def test_preservation_without_oracle_fails(self):
        chk = checks.check_spec(SPEC_OK.replace("[Inferred] (contains)", "[Inferred] (preservation)"))
        self.assertFalse(chk.ok)

    def test_missing_given_when_then_fails(self):
        chk = checks.check_spec(SPEC_OK.replace("when converted, then no exception", "no exception"))
        self.assertFalse(chk.ok)

    def test_fr_without_ac_fails(self):
        chk = checks.check_spec(SPEC_OK.replace("### FR-001 — no crash", "### FR-001 — no crash\n### FR-002 — other"))
        self.assertFalse(chk.ok)
        self.assertTrue(any("FR-002" in r for r in chk.reasons))

    def test_needs_input(self):
        text = SPEC_OK.replace("status: PASS", "status: NEEDS_INPUT").replace("blocking_questions: []",
                                                                             "blocking_questions: [Q-001]")
        chk = checks.check_spec(text)
        self.assertFalse(chk.ok)
        self.assertEqual(chk.data["status"], "NEEDS_INPUT")
        self.assertIn("maintainer input", chk.reasons[0])

    def test_no_front_matter(self):
        self.assertFalse(checks.check_spec("# just text").ok)


class RepoCase(unittest.TestCase):
    def setUp(self):
        self.repo = Path(tempfile.mkdtemp())
        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.email", "t@t")
        git(self.repo, "config", "user.name", "t")
        (self.repo / "markdown").mkdir()
        (self.repo / "tests").mkdir()
        (self.repo / "docs").mkdir()
        (self.repo / "markdown" / "mod.py").write_text("class A:\n    def run(self):\n        pass\n\n\ndef f():\n    pass\n")
        (self.repo / "tests" / "test_a.py").write_text(
            "import unittest\n\n\nclass T(unittest.TestCase):\n    def test_one(self):\n        pass\n\n"
            "    def test_two(self):\n        pass\n")
        (self.repo / "docs" / "changelog.md").write_text("## [Unreleased]\n")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "base")
        self.base = git(self.repo, "rev-parse", "HEAD").strip()


class TestDesignCheck(RepoCase):
    def design(self, files: str, body: str = "## ARCHITECTURE.md vs source\nnone") -> str:
        return f"---\nfiles:\n{files}\n---\n{body}\n"

    def test_existing_symbols_pass(self):
        d = self.design("  - path: markdown/mod.py\n    change: modify\n    symbols: [A.run, f]")
        self.assertTrue(checks.check_design(d, self.repo).ok)

    def test_unknown_symbol_fails(self):
        d = self.design("  - path: markdown/mod.py\n    change: modify\n    symbols: [A.nope]")
        chk = checks.check_design(d, self.repo)
        self.assertFalse(chk.ok)
        self.assertIn("A.nope", chk.reasons[0])

    def test_missing_file_fails(self):
        d = self.design("  - path: markdown/missing.py\n    change: modify\n    symbols: [x]")
        self.assertFalse(checks.check_design(d, self.repo).ok)

    def test_new_file_and_new_symbol_pass(self):
        d = self.design("  - path: markdown/new.py\n    change: new\n    new_symbols: [g]")
        self.assertTrue(checks.check_design(d, self.repo).ok)

    def test_outside_allowed_paths_fails(self):
        d = self.design("  - path: .github/workflows/x.yml\n    change: modify\n    symbols: [x]")
        self.assertFalse(checks.check_design(d, self.repo).ok)

    def test_no_symbols_fails(self):
        d = self.design("  - path: markdown/mod.py\n    change: modify\n    symbols: []")
        self.assertFalse(checks.check_design(d, self.repo).ok)

    def test_missing_architecture_section_fails(self):
        d = self.design("  - path: markdown/mod.py\n    change: modify\n    symbols: [f]", body="## Plan\nx")
        self.assertFalse(checks.check_design(d, self.repo).ok)


class TestDiffGuard(RepoCase):
    def guard(self):
        return checks.diff_guard(self.repo, self.base, checks.changed_files(self.repo, self.base))

    def test_allowed_change_with_changelog_passes(self):
        (self.repo / "markdown" / "mod.py").write_text("def f():\n    return 1\n")
        (self.repo / "docs" / "changelog.md").write_text("## [Unreleased]\n* fix\n")
        self.assertTrue(self.guard().ok, self.guard().reasons)

    def test_code_change_without_changelog_fails(self):
        (self.repo / "markdown" / "mod.py").write_text("def f():\n    return 1\n")
        chk = self.guard()
        self.assertFalse(chk.ok)
        self.assertIn("changelog", chk.reasons[0])

    def test_change_outside_allowed_paths_fails(self):
        (self.repo / ".github").mkdir()
        (self.repo / ".github" / "ci.yml").write_text("x")
        self.assertFalse(self.guard().ok)

    def test_removed_test_method_fails(self):
        (self.repo / "tests" / "test_a.py").write_text(
            "import unittest\n\n\nclass T(unittest.TestCase):\n    def test_one(self):\n        pass\n")
        chk = self.guard()
        self.assertFalse(chk.ok)
        self.assertIn("T.test_two", chk.reasons[0])

    def test_deleted_test_file_fails(self):
        (self.repo / "tests" / "test_a.py").unlink()
        self.assertFalse(self.guard().ok)

    def test_no_changes_fails(self):
        self.assertFalse(self.guard().ok)


def cmd(command, ok=True, denied=False, tail="Ran 1172 tests in 3.2s\n\nOK (skipped=13)"):
    return {"command": command, "ok": ok, "denied": denied, "output_tail": tail}


RAN_SUITE = [cmd("python -m unittest discover tests")]


class TestVerdictValidation(unittest.TestCase):
    def v(self, **kw):
        base = {"verdict": "approve", "target_stage": "none", "summary": "s", "verified": ["ran tests"],
                "findings": []}
        base.update(kw)
        return base

    def test_approve_ok(self):
        self.assertEqual(review.validate(self.v(), RAN_SUITE), [])

    def test_approve_without_verification_rejected(self):
        self.assertTrue(review.validate(self.v(verified=[]), RAN_SUITE))

    def test_request_changes_needs_serious_finding_and_stage(self):
        self.assertTrue(review.validate(self.v(verdict="request_changes"), RAN_SUITE))
        good = self.v(verdict="request_changes", target_stage="implementation",
                      findings=[{"severity": "major", "file": "a.py", "line": 1, "issue": "x", "evidence": "y"}])
        self.assertEqual(review.validate(good, RAN_SUITE), [])

    def test_request_changes_finding_without_evidence_rejected(self):
        bad = self.v(verdict="request_changes", target_stage="design",
                     findings=[{"severity": "blocker", "file": "a.py", "line": None, "issue": "x", "evidence": " "}])
        self.assertTrue(review.validate(bad, RAN_SUITE))

    # Smoke-test run 45003925819: the reviewer's only shell command was denied and it approved by reading.
    def test_approve_without_running_tests_rejected(self):
        self.assertTrue(review.validate(self.v(), None))   # no transcript at all
        self.assertTrue(review.validate(self.v(), []))     # transcript, but no commands
        self.assertTrue(review.validate(self.v(), [cmd("python -m unittest discover tests | tail -4",
                                                       ok=False, denied=True, tail="Permission denied")]))
        self.assertTrue(review.validate(self.v(), [cmd('python -c "import markdown"')]))

    def test_approve_with_failing_suite_rejected(self):
        failing = [cmd("python -m unittest discover tests", ok=False, tail="FAILED (failures=1)")]
        self.assertTrue(review.validate(self.v(), failing))

    def test_request_changes_does_not_need_a_test_run(self):
        good = self.v(verdict="request_changes", target_stage="implementation",
                      findings=[{"severity": "major", "file": "a.py", "line": 1, "issue": "x", "evidence": "y"}])
        self.assertEqual(review.validate(good, None), [])


class TestTranscript(unittest.TestCase):
    """Executed commands come from Claude Code's own session transcript (format checked with 2.1.319)."""

    def write_transcript(self, root: Path, session: str) -> Path:
        lines = [
            {"message": {"content": [{"type": "tool_use", "id": "t1", "name": "Bash",
                                      "input": {"command": "python -m unittest discover tests"}}]}},
            {"message": {"content": [{"type": "tool_use", "id": "t1", "name": "Bash",   # recorded twice
                                      "input": {"command": "python -m unittest discover tests"}}]}},
            {"message": {"content": [{"type": "tool_result", "tool_use_id": "t1", "is_error": False,
                                      "content": "Ran 1172 tests\n\nOK"}]}},
            {"message": {"content": [{"type": "tool_use", "id": "t2", "name": "Bash",
                                      "input": {"command": "env"}}]}},
            {"message": {"content": [{"type": "tool_result", "tool_use_id": "t2", "is_error": True,
                                      "content": "Permission to use Bash has been denied."}]}},
            {"message": {"content": [{"type": "tool_use", "id": "t3", "name": "Read",
                                      "input": {"file_path": "x"}}]}},
            {"message": {"content": "plain text message"}},
        ]
        path = root / "projects" / "-home-runner-work-markdown" / f"{session}.jsonl"
        path.parent.mkdir(parents=True)
        path.write_text("\n".join(json.dumps(x) for x in lines) + "\n")
        return path

    def test_sandbox_failure_detected(self):
        real = ("Sandbox is required but failed to initialize: Sandbox dependencies not available: socat not "
                "installed. Restart to retry. Running it outside the sandbox (dangerouslyDisableSandbox) is not "
                "allowed either.")  # verbatim from review run 45006857285
        self.assertIn("socat", claude_runner.environment_failure([cmd("python -m unittest discover tests",
                                                                      ok=False, tail=real)]))
        self.assertEqual(claude_runner.environment_failure([cmd("python -m unittest", ok=False,
                                                                tail="FAILED (failures=1)")]), "")
        self.assertEqual(claude_runner.environment_failure(RAN_SUITE), "")
        self.assertEqual(claude_runner.environment_failure(None), "")

    def test_find_and_parse(self):
        with tempfile.TemporaryDirectory() as d, mock.patch.dict("os.environ", {"CLAUDE_CONFIG_DIR": d}):
            path = self.write_transcript(Path(d), "abc-123")
            self.assertEqual(claude_runner.find_transcript("abc-123"), path)
            self.assertIsNone(claude_runner.find_transcript("other"))
            self.assertIsNone(claude_runner.find_transcript(None))
            cmds = claude_runner.executed_commands(path)
        self.assertEqual([c["command"] for c in cmds], ["python -m unittest discover tests", "env"])
        self.assertEqual([(c["ok"], c["denied"]) for c in cmds], [(True, False), (False, True)])
        self.assertTrue(review.ran_test_suite(cmds))


class TestGate(unittest.TestCase):
    def setUp(self):
        self.write = mock.patch.object(gate, "has_write", return_value=True).start()
        self.status = mock.patch.object(gate, "last_status", return_value={}).start()
        self.same_repo_patcher = mock.patch.object(gate, "same_repo_pr", return_value=True)
        self.same_repo = self.same_repo_patcher.start()
        self.addCleanup(mock.patch.stopall)

    def test_label_autose_starts_full_run(self):
        d = gate.decide("issues", {"label": {"name": "autose"}, "issue": {"number": 3}, "sender": {"login": "m"}},
                        "o/r", "sha")
        self.assertEqual((d["run"], d["mode"], d["issue"]), ("true", "full", "3"))

    def test_other_label_ignored(self):
        d = gate.decide("issues", {"label": {"name": "bug"}, "issue": {"number": 3}}, "o/r", "sha")
        self.assertEqual(d["run"], "false")

    def test_comment_from_outsider_ignored(self):
        ev = {"issue": {"number": 3}, "comment": {"body": "/autose", "user": {"login": "x", "type": "User"},
                                                  "author_association": "NONE"}}
        self.assertEqual(gate.decide("issue_comment", ev, "o/r", "sha")["run"], "false")

    def test_comment_from_bot_ignored(self):
        ev = {"issue": {"number": 3}, "comment": {"body": "/autose", "user": {"login": "b", "type": "Bot"},
                                                  "author_association": "OWNER"}}
        self.assertEqual(gate.decide("issue_comment", ev, "o/r", "sha")["run"], "false")

    def test_comment_on_pr_is_review_only(self):
        ev = {"issue": {"number": 9, "pull_request": {}}, "comment": {
            "body": "/autose", "user": {"login": "m", "type": "User"}, "author_association": "OWNER"}}
        d = gate.decide("issue_comment", ev, "o/r", "sha")
        self.assertEqual((d["mode"], d["pr"]), ("review-only", "9"))

    def test_review_of_pr_from_another_fork_refused(self):
        self.same_repo.return_value = False
        ev = {"issue": {"number": 9, "pull_request": {}}, "comment": {
            "body": "/autose", "user": {"login": "m", "type": "User"}, "author_association": "OWNER"}}
        self.assertEqual(gate.decide("issue_comment", ev, "o/r", "sha")["run"], "false")
        dispatch = {"inputs": {"number": "9", "mode": "review-only"}, "sender": {"login": "m"}}
        self.assertEqual(gate.decide("workflow_dispatch", dispatch, "o/r", "sha")["run"], "false")

    def test_same_repo_pr_reads_head_repository(self):
        self.same_repo_patcher.stop()
        with mock.patch.object(gate, "gh_json", return_value={"head": {"repo": {"full_name": "o/r"}}}):
            self.assertTrue(gate.same_repo_pr("o/r", "9"))
        with mock.patch.object(gate, "gh_json", return_value={"head": {"repo": {"full_name": "evil/r"}}}):
            self.assertFalse(gate.same_repo_pr("o/r", "9"))
        with mock.patch.object(gate, "gh_json", return_value=None):
            self.assertFalse(gate.same_repo_pr("o/r", "9"))

    def test_comment_after_needs_input_resumes(self):
        self.status.return_value = {"state": "needs_input", "run_id": "123", "variant": "pipeline"}
        ev = {"issue": {"number": 5}, "comment": {"body": "/autose it's reference links",
                                                  "user": {"login": "m", "type": "User"},
                                                  "author_association": "OWNER"}}
        with tempfile.TemporaryDirectory() as tmp, mock.patch("os.getcwd", return_value=tmp):
            import os
            old = os.getcwd()
            os.chdir(tmp)
            try:
                d = gate.decide("issue_comment", ev, "o/r", "sha")
                self.assertIn("reference links", Path(".autose_gate/answers_raw.md").read_text())
            finally:
                os.chdir(old)
        self.assertEqual((d["mode"], d["prev_run_id"]), ("resume", "123"))

    def test_user_without_write_access_ignored(self):
        self.write.return_value = False
        d = gate.decide("issues", {"label": {"name": "autose"}, "issue": {"number": 3}, "sender": {"login": "t"}},
                        "o/r", "sha")
        self.assertEqual(d["run"], "false")


if __name__ == "__main__":
    unittest.main()
