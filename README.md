# Cities & Climate Learning Lab website

Public website and governance-first prototype for the Cities & Climate Learning Lab (CCLL), based in the School of Resource and Environmental Management at Simon Fraser University.

This Gate 0–1 implementation is deliberately static. Research Watch uses clearly labelled fixture records; it makes no external API or model calls and publishes nothing automatically.

## Local setup

Requirements:

- Python 3.11 or newer
- Quarto 1.5 or newer
- GNU Make (optional; the shell scripts can be run directly)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
make check
make build
```

The built site is written to `_site/`. Run `make preview` for a local preview. On macOS, `scripts/quarto.sh` also looks for the Quarto installation bundled with RStudio.

## Common maintenance tasks

- Add or edit structured records under `data/`.
- Update theme definitions and search concepts in `config/research_scope.yml`.
- Run `make validate` to check schemas and cross-record rules.
- Run `make generate` to refresh generated Quarto fragments.
- Run `make check` before opening a pull request.
- Run `make linkcheck-external` only when explicit network access has been approved.

Generated files under `generated/` are reproducible and should not be edited by hand. See [content governance](docs/content-governance.md) and [architecture](docs/architecture.md) before changing the Research Watch workflow.

## Gate boundaries

Current scope and exclusions are recorded in [docs/gate-0-1-scope.md](docs/gate-0-1-scope.md). No production deployment is configured.
