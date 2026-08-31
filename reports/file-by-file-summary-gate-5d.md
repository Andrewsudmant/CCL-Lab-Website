# Gate 5D file-by-file change summary

## Research model and canonical data

| File or bounded group | Change and reason |
|---|---|
| `config/research_scope.yml`, `schemas/research-theme.schema.json` | Remove active status/maturity fields; expand all four current themes with guiding questions, two-paragraph descriptions, analytical boundaries and cycle links. |
| `schemas/research-work.schema.json`, `data/work/*.yml` | Replace the project-only model with typed Work records and optional parents; distinguish five ongoing and two completed records and preserve provenance/claim boundaries. |
| `schemas/research-idea.schema.json`, `data/research-ideas/*.yml` | Add 13 separately governed possible research directions with the exact non-commitment disclosure. |
| `schemas/publication.schema.json`, `data/publications/*.yml` | Replace project links with Work links and add evidence-backed theme relationships/rationales while permitting standalone publications. |
| `config/publication_theme_examples.yml`, `schemas/publication-theme-examples.schema.json` | Store source-backed selected examples separately from canonical bibliography identity; exclude title-only and MDPI promotion. |
| `config/publication_authoritative_overrides.yml`, `reports/content/publication-complete-inventory.json` | Correct authoritative metadata and rebuild the 46-record verified inventory; retain ten unresolved ORCID-only groups outside the public inventory. |

## Generation, routes and presentation

| File or bounded group | Change and reason |
|---|---|
| `scripts/generate_site.py` | Generate Work, theme, publication and transition pages; deduplicate connected publications; make cleanup occur only after successful generation so the last complete source tree survives failures. |
| `work.qmd`, `generated/work.qmd`, `work/*.qmd` | Add the canonical filterable Work listing and seven detail pages. |
| `projects.qmd`, `projects/*.qmd` | Preserve old URLs as explicit transition pages with canonical Work URLs; no duplicate Projects listing. |
| `research/*.qmd`, `generated/home-themes.qmd`, `generated/research-themes.qmd` | Regenerate the four-theme cycle and required theme-page section order. |
| `index.qmd`, `_quarto.yml` | Rename navigation and homepage surface to Work/Featured work while preserving the accepted visual design. |
| `assets/site.js`, `styles.css` | Add accessible Work filters and visually distinct idea cards, status/type labels and responsive behaviour. |
| `publications/*.qmd`, `generated/publications-selected.qmd` | Regenerate canonical publication detail/listing views with corrected entity rendering and Work/theme metadata. |

## Governance, migration and review evidence

| File or bounded group | Change and reason |
|---|---|
| `docs/adr/0004-themes-work-publications-ideas.md` | Record why themes, Work, publications and ideas are separate concepts. |
| `docs/migrations/project-to-research-work-gate-5d.md` | Record the six former-project migrations, retained IDs and compatibility routes. |
| `docs/research-content-model.md`, `docs/architecture.md`, `docs/content-governance.md`, `docs/security.md`, `AGENTS.md` | Make the model, source thresholds, attribution, idea governance and security boundaries durable. |
| `reports/content/theme-examples-audit-gate-5d.md` | Record evidence source, rationale, uncertainty and treatment for every promoted or excluded example. |
| `reports/content/standalone-publications-audit-gate-5d.md` | Record removed artificial parents, retained genuine relationships, deduplication and withheld records. |
| `docs/reviews/gate-5d/*.md` | Provide owner-facing architecture, theme, idea and package reviews. |
| `reports/browser-qa-gate-5d.md`, `reports/screenshots/gate-5d/**` | Record fresh desktop/mobile/enlarged visual QA from the Gate 5D render. |
| `reports/security/gate-5d-secret-scan.md` | Record the repository/history integrity scan without disclosing candidate values. |

## Validation and packaging

| File or bounded group | Change and reason |
|---|---|
| `scripts/validate_content.py` | Validate the Work/idea/example schemas, links, identities and cross-record constraints. |
| `tests/test_gate_5d_research_work.py`, updated existing tests | Cover theme equality, work types/statuses, optional parents, idea isolation, routes, disclosures, deduplication and clean build order. |
| `scripts/package_gate_5d_review.py`, `Makefile` | Build a deterministic owner package containing the private rendered site, screenshots, schemas, records, audits and QA. |
| `scripts/package_handoff.py`, `docs/handoffs/gate-5d-handoff.md` | Produce the compact governance-focused shareable ZIP requested for future ChatGPT/Codex continuation. |
