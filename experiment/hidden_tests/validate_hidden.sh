#!/usr/bin/env bash
# Validate every hidden test suite: it must FAIL at the pinned commit (except tests marked "preservation"),
# and PASS once the private reference fix is applied, without breaking the repository's own test suite.
# Usage: validate_hidden.sh <path-to-a-git-clone-of-Python-Markdown> [python-executable]
# Creates and removes a temporary git worktree; the clone itself is not modified.
set -uo pipefail
CLONE=$(cd "$1" && pwd)
PY=${2:-python3}
PIN=3f2c5510bd8d64a73ec18342f740371bcde9b20c
HERE=$(cd "$(dirname "$0")" && pwd)
WT=$(mktemp -d)/wt
git -C "$CLONE" worktree add -q --detach "$WT" "$PIN"
trap 'git -C "$CLONE" worktree remove --force "$WT"' EXIT
for N in 1 2 3 4 5; do
  echo "=================== issue $N"
  git -C "$WT" checkout -q -- . && git -C "$WT" clean -fdq
  echo "--- at pin (expect failures, preservation tests pass):"
  "$HERE/run_hidden.sh" "$WT" "$N" "$PY" 2>&1 | grep -E ' \.\.\. (ok|FAIL|ERROR)$|^(OK|FAILED)'
  git -C "$WT" apply "$HERE/reference_fixes/issue_$N.patch"
  echo "--- with reference fix (expect all ok):"
  "$HERE/run_hidden.sh" "$WT" "$N" "$PY" 2>&1 | grep -E ' \.\.\. (ok|FAIL|ERROR)$|^(OK|FAILED)'
  echo "--- repository suite with reference fix (expect OK):"
  (cd "$WT" && "$PY" -m unittest discover tests 2>&1 | tail -1)
done
