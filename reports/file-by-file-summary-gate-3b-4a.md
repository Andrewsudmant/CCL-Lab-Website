# Gate 3B–4A file-by-file change summary

- `AGENTS.md`, `README.md`, `docs/*.md`: updated durable scope, architecture, governance, security, baseline, content audit and plain-language handoff.
- `_quarto.yml`, `index.qmd`, principal `.qmd` pages, `styles.css`: simplified navigation, added Outputs, reordered homepage hierarchy, corrected contact/profile copy and removed internal/development material from the public render.
- `data/people/andrew-sudmant.yml`: canonical approved profile, contact, education, ORCID, IPCC role and verified links; optional image remains null with rights status.
- `data/projects/*.yml`: three cautious current programmes and three verified foundational projects, each with relationship, themes, methods, provenance and safe public wording.
- `data/publications/*.yml`: ten exact, fully attributed foundational records; known invented/truncated records and the non-Andrew Nature article were removed from the publication inventory.
- `schemas/*.json`, `config/*.yml`, `prompts/*.md`: stricter relationship/date/provenance/AI contracts, approved theme statuses, 12-item cap, provider-native query pack and explicit MDPI override.
- `scripts/generate_site.py`: relationship-group rendering, complete publication/person output, generated cross-theme views and Research Watch disclosures.
- `scripts/refresh_publications.py`, `reports/content/*`: real ORCID/Crossref/DataCite-aware reconciliation proposal, conflicts, overrides and readable diff.
- `research_watch/*`, `scripts/run_research_watch_pilot.py`: DataCite enrichment, provider filters, deduplication, event clustering, evidence controls, diversity selection, availability states and atomic last-known-good staging.
- `calibration/research-watch/*`: 35 real candidate records, local labelling HTML with JSON export, CSV fallback, instructions and empty labels.
- `.github/workflows/*`: read-only private artefacts, concurrency/timeouts, disabled-by-default future write control and manual Bluesky diagnostic; no deployment or main write.
- `tests/*`, `reports/qa/*`, `reports/screenshots/*`: more than 50 automated cases plus desktop/mobile/high-zoom browser evidence.
- `scripts/package_*.py`: distinct private launch-candidate, calibration and compact ChatGPT handoff ZIPs.
