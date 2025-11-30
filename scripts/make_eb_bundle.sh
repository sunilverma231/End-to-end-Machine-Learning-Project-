#!/usr/bin/env zsh
set -euo pipefail

# Create a clean EB deploy bundle with .ebignore respected
# Usage: scripts/make_eb_bundle.sh

repo_root=$(cd "$(dirname "$0")/.." && pwd)
ts=$(date +%Y%m%d-%H%M%S)
out="${repo_root}/deploy-${ts}.zip"

cd "$repo_root"

# Ensure .ebignore exists
if [[ ! -f .ebignore ]]; then
  echo ".ebignore not found; creating a minimal one..."
  cat > .ebignore <<'EOM'
myenv/
.venv/
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.git/
.DS_Store
notebook/
logs/
EOM
fi

if ! command -v zip &>/dev/null; then
  echo "zip not found. Please install zip (e.g., brew install zip)" >&2
  exit 1
fi

# Build a temp directory and rsync respecting .ebignore
tmpdir=$(mktemp -d)
# Use rsync with --exclude-from to respect .ebignore patterns (best effort)
rsync -a . "$tmpdir" \
  --exclude-from=.ebignore \
  --exclude='.git/' \
  --exclude='*.zip' \
  --exclude='*.log' >/dev/null

(cd "$tmpdir" && zip -r9 "$out" . >/dev/null)
rm -rf "$tmpdir"

echo "Created: $out"
echo "Upload this zip in the EB Console: Environment -> Upload and deploy."
