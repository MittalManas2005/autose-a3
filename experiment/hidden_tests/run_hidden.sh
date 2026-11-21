#!/usr/bin/env bash
# Run the hidden acceptance tests for one issue against a checkout of the fork.
# Usage: run_hidden.sh <path-to-markdown-checkout> <issue-number 1-5> [python-executable]
# The checkout's own `markdown` package is imported (the tests run with the checkout as the working directory).
set -euo pipefail
CHECKOUT=$(cd "$1" && pwd)
N=$2
PY=${3:-python3}
HERE=$(cd "$(dirname "$0")" && pwd)
cd "$CHECKOUT"
exec "$PY" -m unittest discover -s "$HERE/issue_$N" -t "$HERE/issue_$N" -p 'test_*.py' -v
