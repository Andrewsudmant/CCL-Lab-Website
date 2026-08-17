# Gate 5B file-by-file summary

## Governance and operations

- `AGENTS.md` — makes provenance-aware disclosure and the Gate 5B paid-call boundary durable.
- `README.md` — documents clean local checks, no-key diagnostics, artifact-only benchmarking and the live runbook.
- `docs/architecture.md` — records the cross-source evidence graph and read/write workflow separation.
- `docs/content-governance.md` — ties public wording to `ai_provenance.used` and defines deterministic cluster acceptance.
- `docs/security.md` — confines the API key to the protected environment and documents strict output/injection controls.
- `docs/gate-5b-scope.md` — states the authorized work and explicit exclusions.
- `docs/current-conversations-live-runbook.md` — lists exact inputs, variables, review sequence, later staging approval and incident steps.
- `docs/handoffs/gate-5b-handoff.md` — plain-language shareable project handoff.

## Publications

- `config/publication_authoritative_overrides.yml` — auditable publisher/repository facts for the August paper and resolved ORCID outputs; retains one evidence-based exclusion.
- `scripts/refresh_publications.py` — continues live ORCID/Crossref/DataCite reconciliation without paid services.
- `scripts/build_complete_publications.py` — adds authoritative non-DOI records, normalizes HTML entities and separates resolved, excluded and unresolved ORCID records.
- `reports/content/publication-*.{json,csv,md}` — refreshed 46-record inventory, provider proposal, conflicts, ten unresolved records and Gate 5B reconciliation.
- `publications/complete.qmd` and `generated/publications-complete.qmd` — renamed “Verified publications and outputs,” now showing 46 records.
- `publications/*.qmd` — deterministic detail pages, including the August 2026 delivery-modes paper and nine repository-verified reports.

## Current Conversations implementation

- `current_conversations/cluster.py` — clusters across DOI, canonical/underlying/citation URLs, identifiers and corroborated title/organisation evidence; model-only proposals are rejected.
- `current_conversations/adapters/openalex.py` — uses provider-native `search`, structural filters and retained provider/alternate-location metadata.
- `scripts/diagnose_openalex.py` — bounded no-key diagnostic across all six themes.
- `current_conversations/adapters/openai_web.py` — current Responses `web_search` tool, strict local validation, stable-source fields and deterministic injection flags.
- `schemas/current-conversations-web-discovery-v1.schema.json` — strict `additionalProperties: false` structured-output contract.
- `current_conversations/budget.py` — fail-closed CAD authorization and aggregate token/cost ledger.
- `scripts/benchmark_current_conversations_models.py` and `tests/fixtures/openai-web/responses-api-mock.json` — credential-free mocked request/response benchmark.
- `scripts/generate_site.py` and generated conversation/theme pages — actual-provenance disclosure for cards, theme listings and detail pages.
- `scripts/run_current_conversations_pilot.py`, `scripts/package_calibration.py`, `calibration/current-conversations-generator/` — clearly labelled generator preview, not a final owner calibration set.

## Automation and QA

- `.github/workflows/current-conversations-live-benchmark.yml` — manual, protected-environment, `contents: read`, artifact-only live benchmark.
- `.github/workflows/current-conversations-scheduled.yml` — read discovery job plus separately guarded write job with branch/path checks; no benchmark secret.
- `.github/workflows/ci.yml` and `Makefile` — deterministic site build before tests that inspect `_site`.
- `tests/test_gate_5b_controls.py` — clustering, schema, injection, missing-secret, corrupt-ledger, over-budget, rollback/LKG, disclosure, publication and workflow tests.
- Existing tests — updated expected inventory and fixture disclosure while retaining prior gate regression coverage.
- `reports/current-conversations/openalex-no-key-diagnostics.md` — actual six-theme no-key results.
- `reports/current-conversations/model-benchmark.md` — mocked-only benchmark, explicitly reporting zero live models and CAD 0.00.
- `reports/screenshots/gate-5b/` and `reports/browser-qa-gate-5b.md` — wholly fresh desktop/mobile/zoom-equivalent evidence; all stale Research Watch screenshots removed.
- `scripts/check_browser_qa_artifacts.py`, `scripts/package_owner_review.py`, `scripts/package_handoff.py` — Gate 5B evidence and shareable ZIP packaging.
