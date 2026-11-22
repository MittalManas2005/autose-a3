#!/usr/bin/env bash
# Copy the AutoSE workflow and agent code from autose-a3/workflow/ into a clone of the fork,
# refreshing the bundled copies of ARCHITECTURE.md and the A1 skill first (ADR-003, ADR-011).
# Usage: workflow/sync_to_fork.sh <path-to-clone-of-MittalManas2005/markdown>
set -euo pipefail
FORK=$(cd "$1" && pwd)
HERE=$(cd "$(dirname "$0")" && pwd)
A3=$(cd "$HERE/.." && pwd)

git -C "$FORK" rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "not a git clone: $FORK" >&2; exit 1; }
[ -f "$FORK/markdown/core.py" ] || { echo "not a Python-Markdown checkout: $FORK" >&2; exit 1; }

mkdir -p "$HERE/autose/context" "$HERE/autose/skills"
cp "$A3/ARCHITECTURE.md" "$HERE/autose/context/ARCHITECTURE.md"
cp "$A3/a1_skill.md" "$HERE/autose/skills/requirements-spec-builder.md"

mkdir -p "$FORK/.github/workflows"
cp "$HERE/.github/workflows/autose.yml" "$HERE/.github/workflows/autose-round.yml" "$FORK/.github/workflows/"
rm -rf "$FORK/autose"
rsync -a --exclude '__pycache__' --exclude 'tests/' "$HERE/autose/" "$FORK/autose/"

echo "Synced into $FORK. Bundled copies (must match the originals in autose-a3):"
for pair in "ARCHITECTURE.md:autose/context/ARCHITECTURE.md" "a1_skill.md:autose/skills/requirements-spec-builder.md"; do
  src=${pair%%:*}; dst=${pair##*:}
  a=$(shasum -a 256 "$A3/$src" | cut -c1-16); b=$(shasum -a 256 "$FORK/$dst" | cut -c1-16)
  printf '  %-45s %s  %s\n' "$dst" "$b" "$([ "$a" = "$b" ] && echo OK || echo MISMATCH)"
done
