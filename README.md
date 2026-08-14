# Cities & Climate Learning Lab website

Public website and automated Research Watch prototype for the Cities & Climate Learning Lab (CCLL), based in the School of Resource and Environmental Management at Simon Fraser University.

Gate 3B–4A is a private launch candidate with fact-checked structured content and a transactional Research Watch staging pipeline. Research Watch records may publish without routine human review only when provenance, evidence, risk, deduplication, disclosure and build controls pass. No production deployment is configured.

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

The built site is written to `_site/`. Run `make preview` for a local preview. On macOS, `scripts/quarto.sh` also looks for the Quarto installation bundled with RStudio. Live discovery never runs as part of a build.

## Common maintenance tasks

- Add or edit structured records under `data/`.
- Update theme definitions and search concepts in `config/research_scope.yml`.
- Run offline discovery with `PYTHONPATH=. .venv/bin/python -m research_watch.run --adapter fixture`; live adapters are opt-in.
- Run the explicit 30-day private pilot with `make research-watch-pilot`; it performs network calls to public providers but never runs during a normal build.
- Refresh the proposed ORCID inventory with `make publications-refresh`.
- Create the one-time calibration ZIP with `make calibration-pack` after the pilot.
- Run `make validate` to check schemas and cross-record rules.
- Run `make generate` to refresh generated Quarto fragments.
- Run `make check` before opening a pull request.
- Run `make linkcheck-external` only when explicit network access has been approved.
- After substantive work, update the relevant file in `docs/handoffs/` and run `make handoff HANDOFF_SUMMARY=docs/handoffs/<file>.md` to create a shareable ChatGPT context package.

Generated files under `generated/` are reproducible and should not be edited by hand. See [content governance](docs/content-governance.md) and [architecture](docs/architecture.md) before changing the Research Watch workflow.

Live adapters are selected explicitly with `--adapter openalex`, `crossref`, `bluesky` or `openai_web_search`. The OpenAI adapter requires `OPENAI_API_KEY`; never place it in YAML, source files, reports or command output. See [Research Watch methods](research-watch/methods.qmd), the [pilot evaluation](reports/pilot/evaluation.md), and the [publication metadata workflow](docs/publication-metadata-workflow.md).

Themes are maintained only in `config/research_scope.yml`. Controlled geography, governance, method, climate-domain and sector terms live in `config/vocabularies.yml`. Query changes are versioned under `config/query_packs/` and require control-plane review. Publication metadata follows ORCID → Crossref → publisher priority, with documented owner overrides taking precedence.

## Gate boundaries

Historical scope is preserved in the gate-scope records. Gate 3B–4A does not authorize production deployment, a merge to `main`, DNS changes or scheduled public writes.

## Shareable handoff packages

Handoff summaries are versioned under `docs/handoffs/`. `make handoff` creates the compact context ZIP; `make owner-review` packages the private site and QA; `make calibration-pack` creates the one-time owner-labelling package. ZIP output is ignored so binary artifacts do not become repository history.
