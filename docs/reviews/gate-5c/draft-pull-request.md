## Summary

This pull request reframes the lab website from six parallel topics into four connected analytical questions about how urban climate knowledge becomes cumulative:

1. Geographies of Climate Learning
2. Where New Evidence Matters
3. Modes of Climate Delivery
4. Consequences for People and Places

The homepage and research overview present these questions as a learning cycle in which consequences generate new evidence and revise what other cities may plausibly learn.

## Gate 5C refinements

- Removes public “Established”/“Developing” theme badges while retaining internal portfolio-maturity metadata.
- Applies the six owner-approved project mappings and keeps geography, methods, sectors and climate domains as facets.
- Confirms Geography of urban climate evidence, Climate delivery modes and CoBen as the three featured projects; the UK Co-Benefits Atlas is prominent foundational prior work.
- Prevents Theme 2 from becoming a residual category for tools, datasets, models or generic gaps.
- Introduces `current-conversations-v2@3.0.0`, separating theme intent, facets and exploratory queries while requiring content-based classification and allowing null.
- Removes hard-coded tools → Theme 2, Canada/BC → Theme 3 and workforce → Theme 4 assumptions.
- Preserves v1 query configuration, stable record IDs, former-theme transition routes and earlier decision history.
- Keeps Current Conversations visibly separate from lab-authored work and retains provenance-dependent disclosure.

## Validation

- 70 records and 15 schemas validated
- 99 tests passed; one known compatibility-import deprecation warning
- 103 Quarto pages rendered
- Internal link checks passed
- Static accessibility checks passed for 103 pages
- Desktop/mobile browser QA passed on the required routes with no captured console errors
- 720-CSS-pixel 200%-equivalent reflow check passed; the in-app browser could not expose a reliable numeric zoom state
- Credential-free OpenAlex diagnostic completed; false positives are documented and no result entered public content
- Repository/history secret scan found zero credential-pattern findings across 1,045 reachable blobs and 515 present files

## Outside scope

No paid API call, API-key access, live model benchmark, merge, deployment, GitHub Pages change, DNS change, repository visibility/permission change, secret/environment change, force-push or history rewrite was performed.

## Owner review

The private package is generated locally as `deliverables/CCLL-thematic-consistency-gate-5c-OWNER_REVIEW_REQUIRED.zip` and is intentionally not committed. Please confirm that the themes are distinct, the cycle is clear, Theme 2 is consequential rather than tool-based, the project mappings are defensible and Current Conversations remains secondary and non-endorsed.
