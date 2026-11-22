#!/usr/bin/env python3
"""A stand-in for the `claude` CLI used only by the local flow test (no model calls, no cost).

It reads the role from AUTOSE_ROLE and the scenario from FAKE_SCENARIO, writes the files a real
agent would write, and prints a JSON result in the same shape as `claude -p --output-format json`.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

FIX = Path(os.environ["FAKE_FIXTURES"])
OUT = Path(".autose_out")
role = os.environ.get("AUTOSE_ROLE", "")
scenario = os.environ.get("FAKE_SCENARIO", "happy")
sys.stdin.read()
counter = OUT / f".fake_{role}_calls"
calls = int(counter.read_text()) + 1 if counter.exists() else 1
counter.write_text(str(calls))
structured = None

if role == "requirements":
    name = "spec_needs_input.md" if scenario == "needs_input" else "spec.md"
    (OUT / "spec.md").write_text((FIX / name).read_text())
elif role == "design":
    (OUT / "design.md").write_text((FIX / "design.md").read_text())
elif role == "implementer":
    if scenario == "build_retry" and calls == 1:
        # First attempt forgets the changelog entry -> the diff guard must reject it.
        subprocess.run(["git", "apply", str(FIX / "fix_code_only.patch")], check=True)
    elif scenario == "guard_violation":
        Path(".github/workflows/evil.yml").write_text("on: push\n")
    else:
        if scenario == "build_retry":
            subprocess.run(["git", "checkout", "HEAD", "--", "markdown"], check=True)  # undo attempt 1
        subprocess.run(["git", "apply", str(FIX / "fix_code_only.patch")], check=True)
        cl = Path("docs/changelog.md")
        cl.write_text(cl.read_text().replace("### Fixed\n\n", "### Fixed\n\n* Fix `toc` crash on a valueless `id`.\n", 1))
elif role == "tester":
    target = Path("tests/test_syntax/extensions/test_autose_issue.py")
    vacuous = scenario == "vacuous_tests" and calls == 1
    target.write_text((FIX / ("tests_vacuous.py" if vacuous else "tests_good.py")).read_text())

print(json.dumps({
    "type": "result", "subtype": "success", "is_error": False, "result": f"fake {role} done",
    "session_id": "fake-session", "num_turns": 1, "total_cost_usd": 0,
    "usage": {"input_tokens": 1, "output_tokens": 1, "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0},
    "modelUsage": {"fake-model": {}}, "permission_denials": [], "structured_output": structured,
}))
