# Gate 5F file-by-file change summary

## Public pages and design

- `index.qmd` — adds the principal claim, cost of separating the four judgements, three reader pathways and link to the worked illustration.
- `work.qmd` — renames the public page to Work and replaces maintainer-oriented model copy with reader-facing programme copy.
- `research/our-approach.qmd` — replaces eight taxonomy states with six breakdown states and adds the hypothetical active-travel illustration.
- `current-conversations/index.qmd` and `current-conversations/how-it-works.qmd` — lead with dispersed discussion and source-tracing as the reader problem; keep the live feed disabled.
- `styles.css` — styles the secondary tagline, reader pathways, destabilising propositions, signature/additional idea hierarchy, Work metadata panel and static illustration; adds responsive rules.

## Structured records and schemas

- `data/research-ideas/*.yml` (24 files) — add `narrative_tier`, no-more-than-three `public_method_tags` and a bounded reader/decision-at-stake field; questions, problems, designs and full method lists remain unchanged.
- `schemas/research-idea.schema.json` — validates the new public-display governance fields and method-tag maximum.
- `data/work/*.yml` (7 files) — add problem, central question, investigative approach and reader-value fields while retaining evidence status, boundaries, sources and canonical relationships.
- `schemas/research-work.schema.json` — requires and validates the argument-led Work fields.
- `tests/fixtures/gate-5d-previous-work-freeze.yml` — freezes the selection source, canonical IDs and display order rather than blocking legitimate new Work argument fields.

## Deterministic generation

- `scripts/generate_site.py` — generates the four homepage propositions, lighter theme scaffolding, two-plus-four idea hierarchy and argument-led Work pages; the metadata element uses a content section to prevent Quarto margin overflow.
- `generated/home-themes.qmd` — regenerated homepage cycle cards.
- `research/{geographies-of-climate-learning,where-new-evidence-matters,modes-of-climate-delivery,consequences-for-people-and-places}.qmd` — regenerated canonical theme pages.
- `work/*.qmd` (7 files) — regenerated canonical Work detail pages.

## Governance and editorial decisions

- `AGENTS.md`, `README.md`, `docs/content-governance.md`, `docs/security.md` — record the durable Gate 5F editorial, provenance, security and scope rules.
- `docs/editorial/site-level-reader-value.md` — defines readers, instability, consequence, changed understanding, boundaries and next actions.
- `docs/adr/0006-site-level-reader-value-and-public-scaffolding.md` — records why public scaffolding was reduced while structured fields remain.
- `docs/baseline-gate-5f.md` and `reports/qa/gate-5f-baseline/*.log` — preserve the untouched Gate 5E baseline.
- `docs/reviews/gate-5f/*.md` — owner guide and seven required audits, including the clearly private, not-implemented previous-work proposal.
- `scripts/generate_gate_5f_audits.py` — reproducibly generates record-level audits from governed data.

## Tests, QA and packaging

- `tests/test_gate_5f_reader_value.py` — covers homepage, theme cards/pages, all 24 ideas, all seven Work pages, Our Approach, Current Conversations, previous-work freeze and offline boundary.
- `tests/test_gate_5d_research_work.py`, `tests/test_gate_5e_draft_candidate.py`, `tests/test_thematic_architecture.py` — update historical expectations without weakening substantive protections.
- `Makefile` and `scripts/package_gate_5f_review.py` — add the bounded Gate 5F owner-review target.
- `scripts/package_handoff.py` — includes Gate 5F decisions, audits and QA in future compact handoffs.
- `reports/browser-qa-gate-5f.md` and `reports/screenshots/gate-5f/` — record fresh desktop, mobile and reflow evidence from the committed Gate 5F source.
- `reports/qa/gate-5f-final/*.log` — retain validation, test, build, check and accessibility results.
- `reports/security/gate-5f-secret-scan.md` — records the final repository/history credential-pattern scan.

No deployment, Pages, DNS, API, paid-model, staging-write, secret/environment or repository-permission change is included.
