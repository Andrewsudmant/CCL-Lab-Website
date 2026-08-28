# Cities & Climate Learning Lab website

Public Quarto website and private, auditable Current Conversations prototype for the Cities & Climate Learning Lab at Simon Fraser University. The research programme is organised around four connected questions: Geographies of Climate Learning; Where New Evidence Matters; Modes of Climate Delivery; and Consequences for People and Places. AI may assist future Current Conversations discovery and annotation; original sources remain authoritative. Current Conversations is publicly marked `In development`, its fixtures are non-public test data, and no production deployment is configured.

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

- `make validate`, `make build`: offline validation and root-site generation.
- `make test`, `make check`: deterministically build both root and provisional `/CCL-Lab-Website/` profiles before tests; `make check` then inspects root links and accessibility.
- `make build-project-path`, `make linkcheck-project-path`, `make release-check`: explicit project-path build and full two-profile release inspection.
- `make publications-refresh`: explicit live ORCID reconciliation followed by the complete publication inventory build.
- `make current-conversations-fixture`: show the captured mixed-source fixture with zero network calls.
- `make current-conversations-pilot`: rebuild private staging and the clearly non-final calibration-generator preview from fixtures.
- `make current-conversations-discover`: run one explicit bounded OpenAlex query; this uses the network.
- `make openalex-diagnostics`: run the four-theme, no-key OpenAlex query diagnostic.
- `make model-benchmark`: evaluate the captured structured-output benchmark without credentials.
- `make public-voice-audit`: inspect rendered copy for repeated cadence, long sentences, stock language and first-use terminology without rewriting it.
- `make calibration-pack`, `make gate-5h-owner-review`, `make handoff`: create bounded owner deliverables.
- `make thematic-owner-review`: create `CCLL_thematic_architecture_reframe_v1_OWNER_REVIEW_REQUIRED.zip` from the final local review materials.

Paid OpenAI web search is disabled unless credentials, model, call/item limits, fresh USD/CAD conversion and the owner’s CAD 2/run and CAD 20/month ceilings are all present. Discovery modes never run during a website build. The protected manual benchmark is artifact-only and read-only. The scheduled workflow’s separate write job is disabled unless explicitly enabled and can target only `automation/current-conversations-staging` after validation and an allowlist check. See the [owner live-benchmark runbook](docs/current-conversations-live-runbook.md).

Generated files under `generated/` are reproducible. The JSON under `data/current-conversations/generated/` is test and regression fixture data and is excluded from the public build while `config/site.yml` keeps the feature in development. People, research work, research ideas and selected publications remain human-editable YAML. Publications may connect directly to themes and do not require a parent work record. Read [architecture](docs/architecture.md), [content governance](docs/content-governance.md), [security](docs/security.md), the [research content model](docs/research-content-model.md) and the [reader-value standard](docs/editorial/reader-value-and-problems-of-understanding.md) before changing the model.

Theme copy must be changed in `config/research_scope.yml`, not duplicated in pages. `scripts/generate_site.py` creates the homepage cycle, research overview, theme pages, work detail pages and theme links from that registry. Public pages use the Gate 5F reader-value hierarchy and the Gate 5H [public voice and plain-language standard](docs/editorial/public-voice-and-plain-language.md), while structured editorial fields remain auditable in YAML. First-use definitions live in `config/plain_language_terms.yml`. Old `/research/themes/...` and `/projects/...` URLs are retained as generated transition pages; new internal links use `/research/<theme>.html` and `/work/<record>.html`.

## Draft 0.1 release boundary

Gate 5G prepares a release candidate but does not authorize paid API calls, staging writes, merge, public deployment, GitHub Pages enablement, DNS changes, analytics, subscriptions, unrestricted crawling or production scheduled writes. `config/theme_featured_examples.yml` controls the illustrative theme-page selection; the verified 46-record inventory remains complete and separate. The default Quarto build targets a domain root, while `_quarto-project-path.yml` configures the provisional GitHub Pages project mount. The workflow in `.github/workflows/public-draft-pages.yml` is manual and fail-closed until the owner later configures the protected environment and enabling variable. Historical documents retain the former “Research Watch” name as evidence; the public and active system name is Current Conversations. See the [Draft 0.1 GitHub Pages runbook](docs/runbooks/publish-draft-0-1-github-pages.md).

Gate 5H changes public cadence, examples, first-use definitions and page structures without changing the academic content model. It keeps the same draft, workflow and deployment boundary. The deterministic voice report is an editorial diagnostic, not an automated quality score or permission to change claims.
