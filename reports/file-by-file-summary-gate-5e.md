# Gate 5E file-by-file change summary

## Public configuration and content

- `config/research_scope.yml` — exact four-theme reader-value copy and `what_this_changes` fields.
- `config/site.yml` — single Draft 0.1 and Current Conversations state source.
- `data/research-ideas/*.yml` — replaces 13 Gate 5D ideas with 24 owner-approved records, six per theme.
- `data/current-conversations/generated/README.md` — marks retained JSON as non-public test/regression fixtures.
- `index.qmd`, `research/our-approach.qmd` — controlling proposition, exact longer purpose and in-development presentation.
- `current-conversations/index.qmd`, `how-it-works.qmd` — approved status/copy, future tense and controls/limitations.
- deleted Current Conversations detail QMD and feed files — removes fixture outputs from public generation.

## Schemas, generation and design

- `schemas/research-theme.schema.json` — requires `what_this_changes`.
- `schemas/research-idea.schema.json` — requires working title, problem and possible design; permits exact G5/E1 qualifications.
- `schemas/site-config.schema.json` — validates draft/live and feed state.
- `scripts/generate_site.py` — renders expanded idea cards, theme interventions, site banner, and no fixture feed/details.
- `scripts/validate_content.py` — enforces 24 ideas and six per theme.
- `styles.css` — restrained banner, reader-value callout, responsive two-to-one-column idea layout and qualification treatment.
- `_quarto.yml` — includes the generated status banner and removes public feed resources.

## Governance and documentation

- `docs/editorial/reader-value-and-problems-of-understanding.md` — durable editorial standard and gap-trap rule.
- `docs/adr/0005-reader-value-theme-copy-and-public-research-ideas.md` — decision rationale.
- `docs/migrations/research-ideas-gate-5d-to-gate-5e.md` — complete 13-to-24 mapping.
- `docs/reviews/gate-5e/*` — theme, ideas, freeze, Current Conversations and Draft 0.1 audits plus owner instructions.
- `docs/runbooks/publish-public-draft-0-1.md` — later owner-controlled merge/protection/Pages sequence.
- `docs/handoffs/gate-5e-handoff.md` — compact governance-focused handoff.
- `AGENTS.md`, `README.md`, `docs/research-content-model.md`, `docs/contributing-content.md` — durable maintenance guidance.

## Tests, QA and packaging

- `tests/fixtures/gate-5d-previous-work-freeze.yml` — byte hashes and exact rendered selection order.
- `tests/test_gate_5e_draft_candidate.py` and migrated legacy tests — reader-value, portfolio, freeze, fixture exclusion, draft status and no-side-effect controls.
- `scripts/generate_gate_5e_audits.py` — deterministic theme/idea/freeze audit generation.
- `scripts/package_gate_5e_review.py`, `scripts/package_handoff.py`, `Makefile`, `tests/test_handoff_package.py` — fresh Gate 5E packages and checks.
- `reports/screenshots/gate-5e/*`, `reports/browser-qa-gate-5e.md` — fresh final desktop/mobile/reflow evidence.
- `.gitignore` — keeps ZIPs and owner-extracted deliverable directories outside Git.
