#!/usr/bin/env bash
# Fail-closed wrapper for interface_guard.py (interface-boundary-guard, agent-native-read-grant).
# Exit 0 allows, exit 2 blocks; any other outcome (missing python3, crash, bad input) is turned
# into a visible block. Synchronized Native realization; regenerated only by /my-interface-agent-native.
dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if ! command -v python3 >/dev/null 2>&1; then
  echo "interface-guard ($1): python3 is unavailable; failing closed." >&2
  exit 2
fi
python3 "$dir/interface_guard.py" "$@"
rc=$?
if [ "$rc" -eq 0 ] || [ "$rc" -eq 2 ]; then
  exit "$rc"
fi
echo "interface-guard ($1): guard failed with exit code $rc; failing closed." >&2
exit 2
