#!/usr/bin/env bash
set -euo pipefail

if [[ -n "${QUARTO_BIN:-}" && -x "${QUARTO_BIN}" ]]; then
  exec "${QUARTO_BIN}" "$@"
fi

if command -v quarto >/dev/null 2>&1; then
  exec quarto "$@"
fi

rstudio_quarto="/Applications/RStudio.app/Contents/Resources/app/quarto/bin/quarto"
if [[ -x "${rstudio_quarto}" ]]; then
  exec "${rstudio_quarto}" "$@"
fi

echo "Quarto was not found. Install Quarto 1.5+ or set QUARTO_BIN." >&2
exit 1
