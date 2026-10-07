#!/usr/bin/env bash
# One-time setup: check, commit, create the private GitHub repo, deploy to Vercel.
# Run from the repo root on a machine where gh and vercel are logged in.
#   ./scripts/bootstrap.sh [repo-name]
set -euo pipefail
cd "$(dirname "$0")/.."
REPO="${1:-payments-directory-wireframe}"

command -v gh >/dev/null || { echo "gh CLI not found"; exit 1; }
gh auth status >/dev/null 2>&1 || { echo "gh not authenticated. Run: gh auth login"; exit 1; }

python3 scripts/render.py
./scripts/check.sh

[ -d .git ] || git init -b main
git add -A
git commit -m "Add payments directory wireframe, teardown and prompt chain" || echo "Nothing new to commit."

if git remote get-url origin >/dev/null 2>&1; then git push -u origin main
else gh repo create "$REPO" --private --source=. --remote=origin --push; fi

if command -v vercel >/dev/null 2>&1; then
  vercel link --yes
  vercel --prod
else
  echo "Vercel CLI not installed. Import the repo at https://vercel.com/new (preset Other, no build command; vercel.json sets output to site/)."
fi
