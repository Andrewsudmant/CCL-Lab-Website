# CCLL thematic architecture reframe v1 — owner review required

## Outcome

The website now presents one cumulative research programme organised around four exact, connected questions. The homepage establishes the intellectual purpose before projects or Current Conversations; the cycle visibly returns from consequences to evidence and further learning. Current Conversations remains a secondary, automatically assisted horizon-scanning feature with conspicuous non-endorsement and fixture-provenance disclosure.

## Completed implementation

- Replaced the six-theme registry with four canonical themes in the approved order.
- Added a semantic, responsive learning cycle and four complete landing pages.
- Added a concise Our approach page distinguishing evidence, reachability, relevance, use, delivery, consequences and subsequent learning.
- Mapped every existing project to one primary theme and supported secondary themes; kept method, sector, geography and climate domain separate.
- Added backward-compatible optional project learning fields without rendering empty headings.
- Migrated publications, fixtures, feed clusters, prompts, query assignments, filters, schemas and tests to the four-theme taxonomy.
- Added null/unclassified Current Conversations handling and demonstrated it with three fixtures.
- Preserved former theme URLs as accessible transition pages and updated all active internal links.
- Removed unused generated Research Watch-era listing fragments while retaining intentional former-name transition routes and historical governance evidence.
- Added regression tests and captured final desktop/mobile review evidence.

## Directly migrated content

The four titles, guiding questions, descriptions and boundaries use the approved owner copy. Project summaries, findings boundaries and authoritative sources were preserved. No publication title, quoted text or archived governance record was rewritten merely because it resembled an old theme phrase.

## Material challenges and resolutions

1. The six former themes were not conceptually equivalent to four replacements. Migration therefore used an explicit mapping and separate facets rather than a blind relabel. Data tools are not automatically Theme 2, and Canadian climate policy is not a fifth theme.
2. Some external fixtures do not justify a theme assignment. The cluster schema, generator, UI and filter now support a null primary theme rather than forcing false precision.
3. Static Quarto output cannot create server-side redirects. Accessible transition pages preserve former URLs and identify their canonical destination.
4. Desktop visual QA found the return note inherited a global list-item width cap. A scoped override fixed it, and both desktop and mobile dimensions were rechecked.

## Transparent and traceable governance

- `config/research_scope.yml` is the single authoritative theme registry.
- Record IDs, source IDs, publication provenance, evidence limitations, AI provenance, review state, correction history and stable URLs remain intact.
- Project mapping decisions and claim boundaries are versioned in YAML and summarized in the included mapping document.
- Current Conversations classifications do not imply quality, endorsement, transferability or recommendation; null classification is retained when evidence is insufficient.
- Captured fixtures continue to record `ai_provenance.used=false` and do not claim AI generation or live retrieval.
- Former routes and historic records are not silently deleted; their status is documented.

## Content still requiring owner writing or decisions

- Confirm the six project mappings and the optional learning-contribution wording.
- Decide whether Theme 2 should remain visibly labelled “Developing.”
- Review which Current Conversations fixtures should remain unclassified; fixtures are not a final calibration set.
- Decide whether the homepage should feature a different combination of three projects.
- Supply future partner copy only when partners and permissions are confirmed; none were invented here.

## Technical limitations

- Former routes are transition documents rather than HTTP 301/308 redirects.
- External link validation remains an explicit network-dependent command and was not run in the final offline check.
- Historical reports, ADRs and compatibility routes retain obsolete names as audit evidence; current public programme pages do not display obsolete theme titles.

## Verification summary

- Schema/content validation: passed, 70 records and 15 schemas.
- Quarto production build: passed, 103 HTML pages.
- Automated tests: passed, 85 tests; one known deprecation warning from the compatibility `research_watch` import.
- Internal links: passed.
- Static accessibility checks: passed for 103 pages.
- Desktop/mobile browser inspection: passed after the documented cycle-width correction; no console warnings or errors.
- Credential-free OpenAlex connectivity/query-shape diagnostic: completed for all four themes; the narrow diagnostic phrases returned zero results, so they require later query calibration and are not treated as a relevance benchmark.
- Non-disclosing repository/history secret scan: zero findings across 772 reachable Git blobs and 496 present repository files before commit; the scan is repeated after commit.

No deployment, merge, secret change, credential change, permission change, paid or model API call, force-push or history rewrite occurred. One bounded, credential-free OpenAlex diagnostic was run as documented. See the ZIP manifest for ending Git state and the complete changed-file list.
