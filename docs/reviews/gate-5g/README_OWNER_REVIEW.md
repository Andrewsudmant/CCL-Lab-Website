# Gate 5G owner review: Draft 0.1 release candidate

This package is a review artifact, not a deployed website. It contains the complete root-path render, the complete `/CCL-Lab-Website/` test render, final screenshots, audits, test logs, the manual release workflow and its owner runbook. No API or paid-model call was made.

## Review locally

Unzip the package and, from its root, run either:

```bash
python3 -m http.server 8000 --directory rendered-root
```

or:

```bash
python3 -m http.server 8001 --directory rendered-project-path
```

Open `http://127.0.0.1:8000/` for the root build. For the project-path copy, open `http://127.0.0.1:8001/CCL-Lab-Website/`.

## Decisions requested

1. Do the 6 / 4 / 6 / 6 previous-work selections represent the four themes accurately and without avoidable repetition?
2. Does each **Conceptual contribution** explain what the example changes in the lab’s way of understanding the theme?
3. Are the four cross-listed examples justified in both themes, with sufficiently distinct copy?
4. Should any currently unselected but still verified output replace a prominent example?
5. Are the public qualification statements appropriately cautious about inference, implementation and conditional estimates?
6. Does **Verified publications and outputs** communicate the intended boundary of the 46-record inventory?
7. Are the visible metadata labels, separators and source descriptions clear to a general academic reader?
8. Is the Draft 0.1 release boundary acceptable: manual dispatch, owner confirmation, repository-variable guard and protected-environment approval?
9. After reviewing the screenshots and local renders, is this candidate suitable to move from draft PR to formal review?

Record requested changes in the pull request. Do not publish from this ZIP. Publication remains a separate owner-controlled sequence documented in `review/runbook.md`; Current Conversations remains in development and exposes no public entries or feed.

## Known items to recheck before publication

- The UK Co-Benefits Atlas returned HTTP 503 during the bounded external-link audit; its official URLs are retained because this appears temporary.
- Several publishers, SSRN and LinkedIn rejected the automated audit client; those links need ordinary human-browser review, not access-control bypassing.
- No public domain has been approved, so canonical/social metadata must be inspected again after the owner configures the eventual Pages URL.

