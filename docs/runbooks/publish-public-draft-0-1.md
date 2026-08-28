# Owner-controlled runbook: publish public Draft 0.1

Gate 5E prepares but does not perform these actions. The owner remains responsible for each approval.

1. Complete review of the Gate 5E theme arguments, 24 research ideas, page readability and Current Conversations in-development presentation. Conduct the selected previous-work-example review separately before publication.
2. Confirm that the review decisions are represented in the source records and that the final branch passes `make validate && make test && make build && make check` from a clean checkout.
3. Review PR #1's complete diff, provenance records, secret-scan result and CI. Keep Current Conversations `in-development` with `public_feed_enabled: false`.
4. When content review is complete, the owner—not automation—may mark PR #1 ready.
5. Confirm final required CI checks and branch protections for `main`, including pull-request review, no direct pushes, no force pushes and no deletion.
6. Merge PR #1 with a merge commit so the gate commits and decision history remain visible. Do not squash the governance history.
7. In a separate authorised action, configure GitHub Pages with least privilege. Do not add deployment permissions to discovery or benchmark jobs.
8. Inspect the live draft at desktop, mobile and 200% equivalent reflow; verify the Draft website banner, navigation, footer, search, correction route and absence of fixture entries/feeds.
9. Retain Current Conversations as `In development`. Launching it requires a separate gate, explicit environment approval, successful artifact-only benchmark and a new publication decision.

Rollback should restore the last-known-good site commit/configuration through a reviewed pull request. Never rewrite published Git history to hide a correction.
