# Gate 5H file-by-file summary

## Public pages and generated output

- `index.qmd`: new hero, plain problem statement, shorter pathways and homepage sections; 15.9% word-count reduction.
- `research/our-approach.qmd`: problem-led opening, active-travel illustration before the six states, named actors and inline terms.
- `current-conversations/index.qmd`, `how-it-works.qmd`: ordinary-language opening followed by unchanged safeguards and technical governance.
- `scripts/generate_site.py`: varied theme-card copy, practical examples, term definitions, lighter idea cards and four Work page structures.
- `generated/home-themes.qmd`, `research/*.qmd`, `work/*.qmd`: deterministic regenerated public pages.
- `styles.css`: practical-example, term, idea-narrative and subordinate Work-provenance presentation.

## Controlled content and governance

- `config/theme_featured_examples.yml`: voice-only rewrites for 22 conceptual-contribution statements; IDs, order, themes, evidence and qualifications unchanged.
- `config/plain_language_terms.yml`: nine controlled first-use mappings.
- `config/public_voice_allowlist.yml`: one bounded owner-required use of “evidence to action.”
- `schemas/plain-language-terms.schema.json`: validates the terminology map.
- `docs/decisions/gate-5h-human-cadence-and-accessibility.md`: records the decision and preservation boundary.
- `docs/editorial/public-voice-and-plain-language.md`: durable public-language standard.
- `docs/baseline-gate-5h.md`: untouched Gate 5G baseline and preservation anchors.
- `AGENTS.md`, `README.md`: durable Gate 5H maintenance rules and commands.

## Audits, review and handoff

- `scripts/audit_public_voice.py`: deterministic, advisory-only rendered-text diagnostic.
- `reports/editorial/gate-5h-public-voice-diagnostic.md`: phrase, cadence, sentence, abstract-series, heading and terminology report.
- `docs/reviews/gate-5h/public-copy-before-and-after.md`: substantive copy changes and preserved claims.
- `docs/reviews/gate-5h/non-academic-reader-comprehension-audit.md`: editorial comprehension review, explicitly not user testing.
- `docs/reviews/gate-5h/work-page-type-mapping.md`: seven records mapped to four public structures.
- `docs/reviews/gate-5h/README.md`, `README_OWNER_REVIEW.md`: local review steps and 11 owner questions.
- `reports/browser-qa-gate-5h.md`, `reports/accessibility/gate-5h-accessibility.md`: final rendered QA.
- `reports/screenshots/gate-5h/`: fresh desktop, mobile, reflow and project-path evidence.
- `docs/handoffs/gate-5h-handoff.md`: compact ChatGPT-ready project handoff.

## Tests, commands and packaging

- `tests/test_gate_5h_public_voice.py`: Gate 5H preservation and acceptance coverage.
- earlier Gate tests: revised only where Gate 5H intentionally supersedes former public wording or page headings.
- `Makefile`: adds `public-voice-audit` and `gate-5h-owner-review`.
- `scripts/package_gate_5h_review.py`: packages both complete builds plus bounded review evidence.
- `scripts/package_handoff.py`: adds Gate 5H governance and review context without rendered output.
- `reports/qa/gate-5h-final/*.log`: exact final validation, build, test, check and release-check output.
- `reports/security/gate-5h-secret-scan.*`: repository and history-wide non-disclosing scan.

## Explicitly unchanged

`config/research_scope.yml`, all 24 `data/research-ideas` records, all seven `data/work` records, the 46-publication complete inventory, the guarded Pages workflow and `config/site.yml` remain unchanged.
