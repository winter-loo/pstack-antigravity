#!/usr/bin/env bash
set -euo pipefail

# Sync ONLY the pstack/ subfolder from upstream cursor/plugins into this standalone repo.
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

if [ -n "$(git status --porcelain)" ]; then
  echo "Error: working tree is dirty. Commit or stash changes first." >&2
  exit 1
fi

echo "==> Fetching upstream/main..."
git fetch upstream main

echo "==> Splitting pstack/ subtree from upstream/main..."
SPLIT_SHA="$(git subtree split --prefix=pstack upstream/main)"

echo "==> Fast-forwarding upstream-pstack to $SPLIT_SHA..."
git checkout upstream-pstack
git merge --ff-only "$SPLIT_SHA"

echo "==> Merging upstream-pstack into main..."
git checkout main
if git merge upstream-pstack; then
  echo "==> Clean merge! Running Antigravity adapter..."
  python3 scripts/adapt-antigravity.py
  echo "==> Done. Review with 'git diff', commit if needed, and run './scripts/sync-links.sh'."
else
  echo "==> Merge conflicts detected. Resolve conflicts, then run:"
  echo "    python3 scripts/adapt-antigravity.py"
  echo "    git add -A && git commit"
  echo "    ./scripts/sync-links.sh"
fi
