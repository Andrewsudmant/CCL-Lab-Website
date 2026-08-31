# Gate 5C owner review — read this first

This package is a private review artifact. It has not been deployed. Open `rendered-site/index.html` in a browser to inspect the complete 103-page site locally; no server, API key or network discovery is required for the core pages.

## What changed and why

Gate 5C makes the four approved questions operate as one coherent learning programme. Theme 2 is no longer a residual category for datasets, tools, models or generic gaps. Public maturity badges were removed so the four stages appear equally necessary, while `portfolio_maturity: developing` remains available internally for planning.

Two project mappings changed: Data Methodologies is now primarily about evidence across places, with consequences secondary; the UK Co-Benefits Atlas is primarily about consequences, with geographies of learning secondary. Unsupported Atlas “consequential uncertainty” and “next learning question” fields were removed. The homepage now definitively features Geography of urban climate evidence, Climate delivery modes and CoBen, while presenting the Atlas as foundational prior work.

Current Conversations now uses `current-conversations-v2@3.0.0`. Queries identify theme intent, facets or exploratory discovery separately; every retrieved item still requires content-based classification. Tools, workforce, Canada and British Columbia do not force a theme. Generic tool fixtures are unclassified where the available description cannot support a substantive relationship. Public disclosure still follows actual AI provenance.

## What to review

Please assess:

1. whether the opening explains that cities cannot investigate every problem independently and that evidence cannot be assumed to transfer unchanged;
2. whether all four themes are distinct and equally necessary;
3. whether the cycle and the return from consequences to later learning are visible;
4. whether Theme 2 now concerns consequential future evidence rather than tools or generic gaps;
5. whether the six project mappings are defensible;
6. whether delivery concerns configurations and mechanisms rather than generic implementation;
7. whether consequences include burdens, risks, costs and distribution;
8. whether Current Conversations is secondary, externally sourced and explicitly non-endorsed; and
9. whether the three featured projects represent the programme effectively.

Do not use the technical fixtures as a final owner calibration set and do not classify them during this review.

## Evidence in this package

- `rendered-site/`: complete private static site.
- `review/screenshots/gate-5c/`: final desktop/mobile homepage and learning-cycle views only.
- `review/gate-5c/`: thematic audit, project field audit and mapping table.
- `review/query-migration.md`: exact query-model migration and compatibility treatment.
- `review/openalex-diagnostics.md`: credential-free provider diagnostic and false-positive limitations.
- `review/full-test.log`: commands, pass counts and the one known deprecation warning.
- `review/browser-qa.md`: route/viewpoint results and explicit zoom/keyboard automation limitations.
- `review/stale-string-audit.md`: former-theme and maturity-label checks.
- `review/file-by-file-summary.md`: grouped file summary.
- `review/git-state-and-remote-transfer.md`: starting authority, baseline, pushed branches and draft PR status.

## Governance and limitations

Original sources remain authoritative. AI is not a source; classifications are not evidence-quality judgements, endorsements, transferability assessments or recommendations. Query v1, earlier gate reports and route transitions remain preserved as decision evidence. No paid call, API-key access, merge, deployment, Pages change, permission change, history rewrite or force-push occurred.

Known limitations are the legacy `research_watch` import deprecation warning, false positives in the bounded OpenAlex query-shape diagnostic, and the in-app browser’s inability to expose a reliable numeric zoom state or synthetic sequential-key trace. Reflow was tested at a conservative 720-CSS-pixel equivalent and native controls/focus styles were inspected.

## Exact next owner action

Review the rendered Gate 5C owner package and the draft pull request. Confirm that the four themes are distinct, the learning cycle is clear, the project mappings are defensible and Current Conversations no longer reproduces the former six-theme taxonomy.
