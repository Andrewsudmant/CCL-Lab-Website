# Cities & Climate Learning Lab — Gate 5G handoff

## What we did and why

Gate 5G turns the Gate 5F owner decisions into a reviewable Draft 0.1 release candidate without publishing it. The four theme pages now use a deliberately small set of verified previous/foundational examples: 6 for Geographies, 4 for New Evidence, 6 for Delivery and 6 for Consequences. Each card explains its conceptual contribution to that theme; four examples are cross-listed under no more than two themes and use different copy in each context. The complete verified inventory remains 46 records, including the August 2026 climate-delivery-modes paper.

We removed internal audit and owner-review language from public pages, translated machine metadata into reader-facing labels, kept internal placeholders explicitly non-public, and retained the underlying provenance in structured source records and Git history. Current Conversations remains visibly **In development**, with no public candidate data, feed or implied lab endorsement.

The same source now builds for a domain root and for GitHub’s `/CCL-Lab-Website/` project path. A new manually dispatched Pages workflow is prepared but deliberately disabled: the owner must approve the content, merge through protected `main`, set a named repository variable, dispatch with an explicit confirmation and approve a protected environment. Only the deployment job receives Pages write permissions.

## Challenges and how they were handled

- The previous-work inventory contained many plausible relationships but too much overlap for a readable public display. We kept the full relationship evidence while moving only 22 theme/example relationships into the prominent configuration.
- Cross-listing risked making examples look generic. Each cross-listed item is capped at two themes and has distinct theme-specific contribution copy.
- Internal provenance phrases were useful for audits but awkward in public prose. They remain in YAML/configuration and review documents while public pages use factual, reader-facing language.
- Root-relative URLs can fail on project Pages. A second Quarto profile, path-aware generated links and two independent link/accessibility passes now test both mount points.
- External automated link checks encountered temporary or access-controlled responses. No restriction was bypassed; the official stable links were retained and the exact results are recorded for human recheck.
- Browser screenshots needed genuine breakpoint validation. The final build was inspected at 1280×720, 390×844 and 720×900, with zero horizontal overflow or broken images in the tested pages.

## Transparent and traceable governance

- Canonical publication and Work records were not replaced by display copy; curation is a separate, schema-validated layer.
- Every featured relationship retains its canonical record ID, exact title, record type, evidence-reviewed URL, decision boundary and public contribution.
- Removal from a prominent theme display does not delete the underlying record or scholarly relationship.
- AI/provider provenance remains conditional on actual structured provenance. Records with `ai_provenance.used: false` do not claim AI generation.
- Internal placeholders must carry `placeholder: true` and `public: false`; tests reject their appearance in rendered HTML.
- Public corrections and removal remain governed by the documented correction route, preserved history and reviewed changes—never silent history rewriting.
- The release workflow fails closed and separates read-only building from the protected write-capable deployment job.
- Both the present repository and all reachable Git blobs are scanned for high-confidence credential patterns before push; scan output never prints secret values.
- The review ZIP includes manifests and SHA-256 hashes so reviewers can identify exactly what they received.

## Verification completed

- 95 structured records validated against 19 schemas.
- 153 automated tests passed; one pre-existing compatibility deprecation warning remains.
- Both 87-page builds passed internal-link and static accessibility checks.
- Browser review covered the homepage, four themes, Work plus all seven detail pages, Verified publications and outputs, Our Approach, Current Conversations, search, and project-path navigation.
- No public deployment, Pages setting, domain/DNS change, API call, paid-model call, staging write or secret handling occurred.

## What the owner should think about next

1. Approve or revise the 6 / 4 / 6 / 6 selected examples and their conceptual-contribution statements.
2. Decide whether the four cross-listings are intellectually necessary and sufficiently distinct.
3. Recheck the temporarily unavailable UK Co-Benefits Atlas and access-restricted publisher/repository links in an ordinary browser.
4. Review the complete rendered sites and responsive screenshots; confirm Draft 0.1 is ready for formal PR review.
5. Establish `main` branch protection and the `public-draft` environment before any merge or release action.
6. Decide the eventual public hostname; canonical and social metadata require another live inspection after that decision.
7. Keep Current Conversations closed until a separate gate approves its live evidence, operational controls and publication status.

The exact future publication sequence is in `docs/runbooks/publish-draft-0-1-github-pages.md`. This handoff does not authorize deployment.
