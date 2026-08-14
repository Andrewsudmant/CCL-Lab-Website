#!/usr/bin/env sh
set -eu
if [ -x .venv/bin/python ]; then
  exec .venv/bin/python scripts/generate_site.py
fi
exec python3 scripts/generate_site.py
