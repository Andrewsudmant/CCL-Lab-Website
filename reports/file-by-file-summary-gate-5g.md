# Gate 5G file-by-file summary

This summary groups generated publication detail pages rather than repeating 46 nearly identical rows. The complete change list remains available in Git.

## Governance and release decisions

- `AGENTS.md` — added durable Gate 5G curation, public-copy, path and release constraints.
- `docs/decisions/gate-5f-owner-approval.md` — recorded the owner’s settled Gate 5F decisions.
- `docs/adr/0007-previous-work-curation-and-draft-release-boundary.md` — separated curation data from canonical records and isolated deployment permission.
- `docs/architecture.md`, `docs/content-governance.md`, `docs/security.md`, `README.md` — documented curated examples, non-public placeholders, dual-path builds and the fail-closed release boundary.
- `docs/runbooks/publish-draft-0-1-github-pages.md` — exact owner inputs, settings, approvals, inspection and rollback steps.
- `docs/runbooks/publish-public-draft-0-1.md` — retained the Gate 5E outline as historical and pointed to the current runbook.

## Curated content and public presentation

- `config/theme_featured_examples.yml` — 22 evidence-supported example/theme relationships, displayed 6 / 4 / 6 / 6 with four bounded cross-listings.
- `schemas/theme-featured-examples.schema.json`, `scripts/validate_content.py` — validate the example bounds, source evidence, copy length, canonical IDs and duplicate limits.
- `scripts/generate_site.py`, four current `research/*.qmd` theme pages — render reader-facing **Conceptual contribution** copy and the full-inventory link.
- `config/research_scope.yml`, `schemas/research-theme.schema.json` — mark all representative examples `public: false`; generation excludes them.
- `config/vocabularies.yml` and generated Work/publication pages — render human labels and semicolon-separated values while retaining stable machine values in source records.
- `data/work/*.yml`, generated `work/*.qmd`, `work.qmd`, `projects.qmd` — retain internal decision provenance but omit non-public sources and audit phrasing from visible pages.
- `publications.qmd`, `generated/publications-complete.qmd`, 46 generated publication detail pages — use **Verified publications and outputs**, retain 46 canonical records, and correct visible metadata/entity handling.
- `current-conversations/how-it-works.qmd` — replaces implementation jargon with public explanations of required fields and deterministic controls.
- `styles.css` — styles visible filter guidance and preserves responsive public presentation.

## Root/project-path portability and release automation

- `_quarto-project-path.yml` — deterministic `/CCL-Lab-Website/` profile and output directory.
- `_quarto.yml`, `.gitignore`, `Makefile` — path-aware footer/navigation, ignored test output, root/project release commands, and deterministic two-profile builds before site-inspecting tests.
- `scripts/check_links.py`, `scripts/check_accessibility.py` — accept explicit site directories; the link checker also accepts a repository base path.
- `.github/workflows/public-draft-pages.yml` — manual, variable-guarded, environment-approved Pages workflow; build remains read-only and deployment permissions are isolated.

## Tests, review evidence and packages

- `tests/test_gate_5g_release_candidate.py` and adjusted Gate 5E/5F/site tests — cover curation, inventory integrity, public language, placeholders, profiles, workflow permissions and closed Current Conversations state.
- `scripts/run_logged_command.py` — records exact QA commands, outputs and exit codes.
- `reports/qa/gate-5g-final/*` — validation, full build, 153-test suite, root checks and project-path release checks.
- `reports/screenshots/gate-5g/*`, `reports/browser-qa-gate-5g.md` — fresh desktop, mobile, reflow and project-path evidence.
- `docs/reviews/gate-5g/*`, `reports/release/*` — owner decision table plus curation, public-copy, metadata, placeholder, link, base-path and hardening audits.
- `scripts/package_gate_5g_review.py` — complete root/project rendered sites and review evidence in an owner-review ZIP.
- `scripts/package_handoff.py`, `docs/handoffs/gate-5g-handoff.md` — compact, governance-focused shareable context package.
- `reports/security/gate-5g-secret-scan.md` — present-tree and reachable-history secret-scan evidence.
