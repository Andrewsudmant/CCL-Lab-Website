## Draft 0.1 release candidate — Gate 5I

Readiness: **READY_SUBJECT_TO_OWNER_MANUAL_KEYBOARD_CHECK**. The owner explicitly permits this bounded result to leave draft status. It is not a completed owner keyboard review, PR approval, merge or deployment.

This PR preserves the complete gate history from the existing branch. Gate 5H's public voice, homepage, four-theme architecture, practical examples, 24 ideas, Work-type structures, Our Approach sequence and public-draft boundary are approved and recorded in `docs/decisions/gate-5h-owner-approval-and-draft-release.md`.

### Final bounded corrections

- Removed only *Low carbon cities: is ambitious action affordable?* from prominent Modes of Climate Delivery examples: five remain. Canonical page, complete and selected listings, search and underlying theme relationships are retained.
- Added `/publications/metadata-and-sources.html`. All 46 individual publication pages retain exact bibliographic identity, ordered authors, dates, stable identifiers, output/review status, relationship labels, original-source and correction links. Repeated procedural paragraphs are centralised; distinctive chronology notes remain.
- The 46-record canonical inventory, four themes, 24 idea source records and seven Work records are unchanged. Human-readable status/version labels do not alter canonical values.
- Fixed native focus visibility and two narrow-screen overflow issues without reopening the approved research content or design.

### Verification

- Baseline: 162 tests, 87 pages per profile. Final local run: 174 tests, 88 pages per profile; one known legacy-import deprecation warning.
- Root and `/CCL-Lab-Website/` builds, internal links and static accessibility pass.
- Browser matrix: 102 route/dimension/profile cases; no final overflow, broken images or recorded console errors. Before/after and focus screenshots included.
- Sequential keyboard automation is unreliable. Exact five-minute checklist: `reports/accessibility/gate-5i-keyboard-navigation.md`. Owner must record a real keyboard/zoom result before merge.
- Bounded external checks: 53 of 57 initial endpoints reachable or redirecting; Bluesky GET subsequently passed. LinkedIn refuses the automated method; external Atlas main/about return 503. Redirect targets were not followed. Limits are documented; canonical records were not silently removed.
- Repository and reachable-history secret scans found no configured-pattern matches. No credentials, `.env`, private data, full-text source or owner ZIP added to Git.
- Final local logs and readiness assessment: `reports/qa/gate-5i-final/` and `docs/reviews/gate-5i/draft-0-1-final-readiness.md`. Confirm the **Site checks / build-and-test** runs on the exact PR head in Checks before merging.

### Deployment and governance boundary

Current Conversations remains in development with no public entries, filters, counts or feeds. The Pages workflow is byte-unchanged, manual, confirmation/variable-guarded and environment-gated. No merge, auto-merge, deployment, Pages enabling, environment/secret/variable change, staging write, paid/API-model call, permission change, DNS change or history rewrite occurred.

Full local owner package: `deliverables/CCLL-draft-0-1-final-release-gate-5i-OWNER_REVIEW_REQUIRED.zip`.
Compact handoff: `deliverables/CCLL-project-handoff-2026-08-31.zip`.
Both are ignored, shareable local artifacts; manifests identify the source SHA. The public-source screenshot commit is `7376ab3`; release-evidence commits do not alter the site.

### Exact owner action

Complete the bounded Gate 5I owner review and any manual keyboard checklist. Confirm the final CI run, merge PR #1 with a merge commit, protect `main`, configure the `public-draft` environment and enabling variable, and manually publish Draft 0.1 through the guarded GitHub Pages workflow. After inspecting the live site, disable the deployment variable again. Current Conversations should remain in development.

Exact controls and rollback: `docs/runbooks/publish-draft-0-1-github-pages.md`. Do not squash the gate history. Any reproducible keyboard failure blocks publication pending a bounded fix.
