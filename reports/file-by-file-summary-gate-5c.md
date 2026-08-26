# Gate 5C file-by-file change summary

## Research architecture and public pages

| File or bounded group | Change |
|---|---|
| `config/research_scope.yml` | Renamed theme status to internal `portfolio_maturity`; kept exact titles/order. |
| `schemas/research-theme.schema.json` | Documents portfolio maturity as internal planning metadata. |
| `scripts/generate_site.py` | Removed public maturity badges while retaining registry-driven generation and omission of empty learning fields. |
| `data/projects/data-methodologies-climate-impact.yml` | Theme 1 primary, Theme 4 secondary; removed retired evidence-tools programme wording. |
| `data/projects/uk-co-benefits-atlas.yml` | Theme 4 primary, Theme 1 secondary; removed unsupported Theme 2/3 mappings and two inferred fields. |
| `index.qmd` | Confirms the approved three featured projects and identifies the Atlas as foundational prior work. |
| `generated/home-themes.qmd`, `generated/research-themes.qmd` | Regenerated equal-status theme/cycle cards. |
| `generated/projects.qmd`, `projects/*.qmd`, `research/*.qmd` | Regenerated affected mappings, cross-listings and theme pages from canonical records. |

## Current Conversations

| File or bounded group | Change |
|---|---|
| `config/query_packs/current-conversations-v2.yml` | New active v3.0.0 pack with theme/facet/exploratory types, nullable intent, separate facets and mandatory classification. |
| `config/query_packs/current-conversations-v1.yml` | Preserved unchanged as migration evidence. |
| `schemas/current-conversations-query-pack.schema.json` | Enforces the new query architecture and four canonical IDs. |
| `schemas/current-conversations-ai-output-v1.schema.json` | Constrains primary/secondary theme output to canonical IDs or null. |
| `prompts/current-conversations-classification-v1.md` | Adds Theme 1/2 distinction, non-examples, facet rules, null validity and non-endorsement limits. |
| `current_conversations/run.py` | Loads v2 explicitly and reports query type/intent/classification requirement. |
| `current_conversations/adapters/openalex.py` | Exposes exact provider-native parameters for auditable diagnostics. |
| `scripts/diagnose_openalex.py` | Runs every active academic query and records parameters, errors, counts, likely false positives and old-theme checks. |
| `tests/fixtures/current-conversations/mixed-source-gate-4b-5a.yml` | Corrects evidence-supported classifications and leaves generic tools unclassified. |
| `scripts/build_current_conversations_fixtures.py` | Versions regenerated fixture provenance as Gate 5C without claiming AI use. |
| `data/current-conversations/generated/sources/*.json` | Regenerated query/run provenance and corrected source annotation wording. |
| `data/current-conversations/generated/clusters/*.json` | Regenerated evidence-based or null classifications; stable IDs retained. |
| `current-conversations/*.qmd`, `current-conversations/feed.json`, `generated/*current-conversations*.qmd` | Regenerated public fixture views, feed and cards with truthful provenance. |
| `.github/workflows/current-conversations-live-benchmark.yml` | Selectable manual benchmark inputs now use reviewed v2 web-query IDs; permissions and artifact-only behaviour unchanged. |
| `docs/current-conversations-live-runbook.md` | Updates exact first-run input and explains query intent versus classification. |

## Governance, tests and review evidence

| File or bounded group | Change |
|---|---|
| `AGENTS.md` | Adds durable Gate 5C theme/facet/maturity rules and preserves no-paid-call/no-deploy boundaries. |
| `docs/architecture.md`, `docs/content-governance.md` | Records active query model, facet separation, null classification and Theme 2 boundary. |
| `docs/migrations/current-conversations-four-theme-query-alignment.md` | Retains old query IDs and explains every migration family. |
| `docs/reviews/gate-5c/*.md` | Owner README, thematic audit, project mapping and field-by-field claim audit. |
| `tests/test_gate_5c_thematic_consistency.py` | Covers active pack, Theme 2, facets, Canada/BC, workforce, null fixtures, disclosure and canonical mappings. |
| `tests/test_thematic_architecture.py` | Covers internal maturity, no public badges, exact featured projects and approved mappings. |
| `tests/test_gate_3b_4a_controls.py`, `tests/test_gate_4b_5a_controls.py` | Removes obsolete `status` and forced-fixture-coverage assumptions. |
| `tests/test_handoff_package.py` | Verifies the Gate 5C package and excludes former-gate screenshots. |
| `scripts/package_gate_5c_review.py`, `Makefile` | Adds deterministic `make gate-5c-owner-review`. |
| `scripts/package_handoff.py` | Adds v2 query configuration to compact handoff context. |
| `reports/current-conversations/openalex-four-theme-diagnostics-gate-5c.md` | Records credential-free results and false-positive limitations. |
| `reports/browser-qa-gate-5c.md`, `reports/stale-string-audit-gate-5c.md`, `reports/qa/gate-5c-final/full-test.log` | Final QA evidence and known limitations. |
| `reports/screenshots/gate-5c/*` | Fresh final desktop/mobile homepage and learning-cycle screenshots only. |
