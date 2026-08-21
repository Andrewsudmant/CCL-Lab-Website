# File-by-file summary — thematic architecture reframe v1

| Files | Change and reason |
|---|---|
| `config/research_scope.yml` | Replaced six themes with the four exact owner-approved questions, descriptions, cycle roles and boundaries. |
| `config/query_packs/current-conversations-v1.yml` | Migrated assignments to the four themes and versioned the active query configuration `2.0.0`; geography-specific queries remain facets. |
| `schemas/research-*.json` | Enforced four registry entries and added guiding-question/cycle-role fields. |
| `schemas/project.schema.json`, `data/projects/*.yml` | Added backward-compatible learning-contribution fields and explicit, evidence-bounded project mappings. |
| `schemas/current-conversation-cluster.schema.json`, `schemas/current-conversations-ai-output-v1.schema.json`, `current_conversations/models.py` | Added a nullable primary-theme state so uncertain/cross-cutting content is not forced into a theme. |
| `tests/fixtures/current-conversations/*`, `data/current-conversations/generated/**`, `scripts/build_current_conversations_fixtures.py` | Migrated fixture taxonomy, demonstrated three unclassified records, and made regeneration preserve version/provenance decisions. |
| `reports/content/publication-complete-inventory.json`, `data/publications/*.yml` | Crosswalked publication theme relationships without changing bibliographic titles or provenance. |
| `scripts/generate_site.py` | Generates semantic learning cycle, new routes, theme pages, project learning sections, null-state tags and former-route transition pages from one registry; removes unused legacy fragments. |
| `index.qmd`, `research.qmd`, `research/our-approach.qmd` | Reframed the homepage and research architecture around a cumulative programme and added the concise approach explanation. |
| `current-conversations/*.qmd`, feeds, prompt and `assets/site.js` | Updated descriptor, adjacent disclosure, filters, links and unclassified filtering while preserving horizon-scanning boundaries and actual provenance. |
| `_quarto.yml`, `styles.css` | Added research routes, full Current Conversations nav label and restrained responsive cycle styling; fixed list-item width interaction. |
| `tests/*.py` | Updated legacy assertions and added exact-order, routes, mapping, disclosure, cycle and unclassified-state regression coverage. |
| `AGENTS.md`, `README.md`, architecture/governance docs | Made the four-theme source of truth and scope constraints durable for future work. |
| `docs/reviews/thematic-architecture-reframe-v1/**` | Recorded starting state, mapping, routes, copy ownership, challenges, residual decisions and owner review. |
| `reports/browser-qa-thematic-reframe-v1.md`, `reports/screenshots/thematic-architecture-reframe-v1/**` | Captured final desktop/mobile evidence for the homepage, cycle, four themes, project and feed. |
| `reports/current-conversations/openalex-no-key-diagnostics.md` | Re-ran the bounded credential-free query-shape diagnostic against the four themes. |
| `scripts/package_thematic_review.py`, `scripts/package_handoff.py`, `Makefile` | Added reproducible owner-review and updated ChatGPT handoff packaging. |
