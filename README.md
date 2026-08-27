# Cities & Climate Learning Lab website

Public Quarto website and private, auditable Current Conversations prototype for the Cities & Climate Learning Lab at Simon Fraser University. The research programme is organised around four connected questions: Geographies of Climate Learning; Where New Evidence Matters; Modes of Climate Delivery; and Consequences for People and Places. AI may assist Current Conversations discovery and annotation; original sources remain authoritative. No production deployment is configured.

## Local setup

Requirements: Python 3.11+, Quarto 1.5+, and optionally GNU Make.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
make check
make build
```

The static site is written to `_site/`. `make preview` serves it locally. Normal validation, generation and builds make no network or paid API calls.

## Maintenance commands

- `make validate`, `make test`, `make build`, `make check`: offline quality controls.
- `make publications-refresh`: explicit live ORCID reconciliation followed by the complete publication inventory build.
- `make current-conversations-fixture`: show the captured mixed-source fixture with zero network calls.
- `make current-conversations-pilot`: rebuild private staging and the clearly non-final calibration-generator preview from fixtures.
- `make current-conversations-discover`: run one explicit bounded OpenAlex query; this uses the network.
- `make openalex-diagnostics`: run the four-theme, no-key OpenAlex query diagnostic.
- `make model-benchmark`: evaluate the captured structured-output benchmark without credentials.
- `make calibration-pack`, `make owner-review`, `make handoff`: create gate-specific owner deliverables.
- `make thematic-owner-review`: create `CCLL_thematic_architecture_reframe_v1_OWNER_REVIEW_REQUIRED.zip` from the final local review materials.

Paid OpenAI web search is disabled unless credentials, model, call/item limits, fresh USD/CAD conversion and the owner’s CAD 2/run and CAD 20/month ceilings are all present. Discovery modes never run during a website build. The protected manual benchmark is artifact-only and read-only. The scheduled workflow’s separate write job is disabled unless explicitly enabled and can target only `automation/current-conversations-staging` after validation and an allowlist check. See the [owner live-benchmark runbook](docs/current-conversations-live-runbook.md).

Generated files under `generated/` are reproducible. Canonical Current Conversations sources and clusters are JSON under `data/current-conversations/generated/`; people, research work, research ideas and selected publications remain human-editable YAML. Publications may connect directly to themes and do not require a parent work record. Read [architecture](docs/architecture.md), [content governance](docs/content-governance.md), [security](docs/security.md) and the [Gate 5D work migration](docs/migrations/project-to-research-work-gate-5d.md) before changing the model.

Theme copy must be changed in `config/research_scope.yml`, not duplicated in pages. `scripts/generate_site.py` creates the homepage cycle, research overview, theme pages, work detail pages and theme links from that registry. Old `/research/themes/...` and `/projects/...` URLs are retained as generated transition pages; new internal links use `/research/<theme>.html` and `/work/<record>.html`.

## Gate boundary

Gate 5B does not authorize a paid API call before owner merge/manual dispatch/environment approval, a merge to `main` by automation, public deployment, DNS changes, analytics, subscriptions, unrestricted crawling or production scheduled writes. Historical documents retain the former “Research Watch” name as evidence; the public and active system name is Current Conversations.
