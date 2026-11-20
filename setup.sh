#!/usr/bin/env bash
# One-time setup: virtualenv, dependencies, headless browser, and starter config files.
#   ./setup.sh                 uses python3
#   PYTHON=python3.12 ./setup.sh
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

PY="${PYTHON:-python3}"
if ! "$PY" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>/dev/null; then
  echo "Python 3.10 or newer is required (found: $("$PY" --version 2>&1)). Set PYTHON=/path/to/python3.x" >&2
  exit 1
fi

echo "==> Creating virtual environment (.venv)"
"$PY" -m venv .venv
# shellcheck disable=SC1091
. .venv/bin/activate
python -m pip install --quiet --upgrade pip

echo "==> Installing the application and its dependencies (a few minutes)"
pip install --quiet -e ./job-finder-src pytest

echo "==> Installing the headless browser used to read job pages and render PDFs"
playwright install chromium

echo "==> Creating your private config files (never committed)"
[ -f .env ] || cp .env.example .env
[ -f candidate_profile.json ] || cp candidate_profile.example.json candidate_profile.json
chmod 600 .env candidate_profile.json
mkdir -p applications_tracker applications data

cat <<'EOF'

Setup finished. Next:
  1. Edit .env                      add GEMINI_API_KEY and MASTER_RESUME_PATH (full path to your resume PDF)
  2. Edit candidate_profile.json    your real details, experience, skills and search preferences
  3. ./jf doctor                    every line should say ok
  4. ./jf scan                      find jobs (see README.md for the whole workflow)
EOF
