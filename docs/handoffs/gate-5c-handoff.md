# Cities & Climate Learning Lab — Gate 5C handoff

Status: `GATE_5C_PASS_THEMATIC_CONSISTENCY_AND_REMOTE_PR`

## What changed and why

Gate 5C refined the four-theme reframe rather than rebuilding it. The public programme now treats all four questions as equally necessary stages in a cycle. Theme 2 retains an internal `portfolio_maturity: developing` value for planning, but no public “Developing” badge makes it look intellectually provisional.

The main conceptual correction was to stop `Where New Evidence Matters` becoming a home for anything involving data, tools or gaps. It now requires a prospective question about evidence that could resolve consequential uncertainty, clarify a mechanism, correct an exclusion that restricts learning or materially change a decision. A dataset, model, dashboard, under-researched place or method is not enough on its own.

Project mappings were aligned with that rule. Data Methodologies is now primarily Geographies of Climate Learning with Consequences secondary. The UK Co-Benefits Atlas is primarily Consequences with Geographies secondary; two unsupported learning-template fields were removed. The other four owner-approved mappings were retained. Geography, methods, sectors and climate domains remain separate facets.

The homepage definitively features Geography of urban climate evidence, Climate delivery modes and CoBen, in that order. The Atlas is presented prominently as foundational prior work rather than a principal current project.

## Current Conversations alignment

`current-conversations-v2@3.0.0` is the active query pack. It distinguishes theme, facet and exploratory queries; records `theme_intent` separately from final classification; and requires content-based classification for every result. Tools, workforce, Canada and British Columbia no longer force Theme 2, 4 or 3. Canadian and BC variants cover all four analytical questions. Null classification remains valid.

The classifier prompt explicitly distinguishes existing evidence across places (Theme 1) from choices about consequential new evidence (Theme 2). It also states that geography, sector, method, source environment and output type are facets and that classification is not quality assessment, endorsement, transferability assessment or policy advice.

Fixture classifications were corrected only from the evidence already recorded. Tool/model fixtures without enough substantive evidence are unclassified; the three previously unclassified fixtures remain unclassified. These fixtures are technical interface tests, not a final owner calibration set. Because `ai_provenance.used=false`, their public labels do not claim AI generation or live retrieval.

## Challenges and trade-offs

- The earlier taxonomy had embedded tools, Canada and workforce into theme-specific searches. A versioned v2 pack was added instead of silently rewriting v1, preserving migration evidence and historical query IDs.
- OpenAlex returned two records for every active academic diagnostic query but many were obvious false positives. The report identifies workforce and the BC Theme 2 query as priority calibration areas and does not treat counts as relevance or completeness.
- The in-app browser did not expose a reliable numeric zoom state or synthetic sequential-key traversal. Responsive reflow was tested at a conservative 720-CSS-pixel equivalent of 200% on a 1440px viewport, native controls and focus styles were inspected, and this limitation is explicit in the QA report.
- The remote was empty while the complete reviewed history was local. Local `main` was fast-forwarded to the stable Gate 5B tip, preserving the entire graph and creating a meaningful thematic PR diff.

## Transparent and traceable governance

The four themes come from one versioned registry. Project records remain canonical and retain authoritative sources, verification dates, relationship to the lab, claim boundaries and separate facets. Optional learning fields remain absent when evidence is insufficient. Query v1, migration tables, old route transitions, previous gate reports and stable source/cluster IDs remain available as decision evidence.

Current Conversations retains original and canonical URLs, stable identifiers, source/cluster IDs, publication/retrieval dates, exact evidence access, query/adapter version, AI provenance, review state, risk flags, corrections and cluster history. AI is a discovery/annotation layer, never the source. External items remain visually and semantically separate from lab-authored projects and outputs. Corrections are recorded rather than silently deleted, and failed runs preserve last-known-good content.

The pre-first-push repository/history scan found zero credential-pattern findings across 1,045 reachable blobs and 515 present files; a later post-handoff scan also found zero findings across 1,050 blobs and 518 files. No paid call, API-key access, merge, deployment, Pages setting, DNS, permission, secret/environment, force-push or history rewrite occurred.

## Quality and Git state

- 70 records and 15 schemas validated
- 99 tests passed; one known compatibility-import deprecation warning
- 103 pages rendered
- Internal links passed
- Static accessibility passed for all 103 HTML pages
- Desktop/mobile route QA passed with no captured console errors
- Credential-free OpenAlex diagnostic completed; false positives documented
- `main`: `8be464c` (stable Gate 5B baseline)
- preserved thematic branch: `5db2584`
- Gate 5C feature branch: `codex/gate-5c-thematic-consistency`
- draft PR: https://github.com/Andrewsudmant/CCL-Lab-Website/pull/1

## What to think about next

1. Confirm the four themes are distinct and the return loop is intellectually clear.
2. Confirm the six project mappings and the three featured projects.
3. Decide whether the Theme 2 portfolio needs additional owner-approved project/output evidence before public launch; do not fill the gap with tools.
4. Calibrate OpenAlex queries against a reviewed mixed-source owner set, focusing on false positives and geographical filters rather than result volume.
5. Review the current null fixture classifications without treating fixtures as the final calibration set.
6. Decide whether to approve and merge the draft PR. A later, separately authorised gate may address hosting, production deployment or a paid benchmark.

## Exact next owner action

Review the rendered Gate 5C owner package and the draft pull request. Confirm that the four themes are distinct, the learning cycle is clear, the project mappings are defensible and Current Conversations no longer reproduces the former six-theme taxonomy.
