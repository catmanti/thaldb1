#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ ! -f "fixtures/lookup_seed.json" ]]; then
  echo "Missing fixtures/lookup_seed.json"
  exit 1
fi

.venv/bin/python manage.py loaddata fixtures/lookup_seed.json
echo "Lookup seed data loaded."
