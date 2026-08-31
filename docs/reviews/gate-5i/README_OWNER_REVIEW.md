# Final Draft 0.1 owner review — Gate 5I

Start here. The website is ready **subject to your bounded manual keyboard check**. PR #1 can leave draft status under the instruction you supplied; this is not a merge, approval or deployment. Current Conversations stays in development.

Gate 5H's voice and architecture are approved and not reopened. This gate removes one redundant prominent Delivery example, consolidates publication procedure in one page, preserves all 46 canonical records and fixes small focus/reflow issues found during review.

Please answer only:

1. Does the publication metadata page explain the process clearly?
2. Do individual publication pages retain enough provenance without repetitive boilerplate?
3. Is the five-example Delivery selection satisfactory?
4. Did the keyboard review identify any accessibility issue?
5. Is the site ready to merge and publish as Draft 0.1?

## Local review

Unzip this package. In its directory, run `python3 -m http.server 8000 --bind 127.0.0.1`. Open `http://127.0.0.1:8000/rendered-root/` and `http://127.0.0.1:8000/rendered-project-path/CCL-Lab-Website/`. These are local-only previews. Do not double-click HTML for search testing: browser restrictions on `file:` URLs can prevent search assets loading. Stop the local server with Ctrl+C.

Review homepage, `/research/modes-of-climate-delivery.html`, `/publications.html`, `/publications/complete.html`, `/publications/metadata-and-sources.html`, and the two representative publication pages in the before/after screenshots. The full site includes 88 pages in each profile. No Research Watch screenshots are used as current evidence.

The keyboard checklist is `review/reports/accessibility/gate-5i-keyboard-navigation.md`. The final readiness report and owner publication runbook are included under `review/docs/`. Automated external checks could not certify LinkedIn or the externally hosted Co-Benefits Atlas (503); the latter's canonical records were not changed. Those checks do not prove an output has disappeared.

## Exact next action

Complete the bounded Gate 5I owner review and any manual keyboard checklist. Confirm the final CI run, merge PR #1 with a merge commit, protect `main`, configure the `public-draft` environment and enabling variable, and manually publish Draft 0.1 through the guarded GitHub Pages workflow. After inspecting the live site, disable the deployment variable again. Current Conversations should remain in development.

Nothing in this archive enables Pages, activates a feed, calls a model, modifies secrets or merges the branch. Keep the archive's manifest with the review so the source commit and file hashes remain traceable.
