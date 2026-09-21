#!/bin/bash
# Double-click this to put the tracker online (or push an update to it).
cd "$(dirname "$0")" || exit 1
REPO="phoenix-envelopes"
USER="renarsm88"

echo "==============================================="
echo "  Phoenix Envelopes  ->  GitHub Pages"
echo "==============================================="
echo

echo "Rebuilding index.html from the tracker..."
PY=$(command -v python3.11 || command -v python3)
"$PY" make_index.py || { echo "Build failed."; read -n 1 -s -r -p "Press any key."; exit 1; }

if [ ! -d .git ]; then
  echo
  echo "FIRST RUN. This creates a PUBLIC GitHub repository."
  echo "A public repo is what makes GitHub Pages free."
  echo "The page holds her budget figures: monthly take-home, category"
  echo "amounts, savings balance. No names, no account numbers, but it"
  echo "would be reachable by anyone who has the address."
  echo
  read -r -p "Type YES to continue, anything else to stop: " OK
  [ "$OK" = "YES" ] || { echo "Stopped. Nothing was published."; read -n 1 -s -r -p "Press any key."; exit 0; }

  git init -q
  git branch -M main
  git add .
  git commit -q -m "Phoenix Envelopes: monthly spending tracker"
  gh repo create "$REPO" --public --source=. --remote=origin --push || {
    echo "Could not create the repo. Is 'gh auth status' logged in?"
    read -n 1 -s -r -p "Press any key."; exit 1; }
  echo "Turning on GitHub Pages..."
  gh api -X POST "repos/$USER/$REPO/pages" -f "source[branch]=main" -f "source[path]=/" >/dev/null 2>&1 \
    || gh api -X PUT "repos/$USER/$REPO/pages" -f "source[branch]=main" -f "source[path]=/" >/dev/null 2>&1
else
  git add .
  if git diff --cached --quiet; then
    echo "No changes to publish."
  else
    git commit -q -m "Update tracker $(date '+%Y-%m-%d %H:%M')"
    git push -q origin main && echo "Pushed."
  fi
fi

echo
echo "Her link (live within a minute or two of the first push):"
echo
echo "   https://$USER.github.io/$REPO/"
echo
echo "Send her that. It works on any phone, needs no account, and does not"
echo "need this Mac switched on."
echo
read -n 1 -s -r -p "Press any key to close."
