# Gate 5H owner review — human cadence and plain language

Status: `GATE_5H_PASS_DRAFT_0_1_VOICE_AND_ACCESSIBILITY` subject to final owner review. This package contains the root and provisional GitHub Pages builds from the packaged commit. Nothing was deployed.

## What changed and why

The Gate 5G release candidate had sound academic boundaries, but repeated sentence shapes, abstract lists and page templates made the public voice feel institutional. Gate 5H keeps the judgement and changes the cadence. The homepage now leads with “Cities learn from one another. The hard part is knowing what can travel.” Each theme opens with a practical scenario. Nine technical terms receive controlled first-use explanations. Research-idea cards are shorter. Work pages follow four structures suited to different research types. Our Approach puts the example before the abstraction, and Current Conversations begins in everyday language.

## What remained fixed

The four theme titles, order, scope, boundaries and links remain unchanged. All 24 idea questions, tiers and source fields remain unchanged. The seven Work source records, statuses and claim boundaries remain unchanged. The 46-record verified publication inventory remains unchanged. Selected previous-work IDs, order, themes, qualifications and evidence remain unchanged; only their public contribution sentences changed. Current Conversations remains in development with no entries, filters, count, feed or network call. The guarded Pages workflow remains manual and disabled by default.

## Challenges and controls

The principal trade-off was making dense ideas approachable without converting uncertainty into certainty. We kept verbatim claim boundaries, put illustrations in labelled boxes, introduced terms before using them technically and made diagnostics advisory rather than automatic. The homepage is 15.9% shorter (607 versus 722 main-content words) despite the fuller new hero. Git hashes and acceptance tests freeze the canonical theme, idea, Work and publication records.

## How governance remains transparent and traceable

Source records remain authoritative. Public presentation is generated from reviewed YAML; Git retains the former wording and every change. The before-and-after table records public edits and their basis. Work pages keep evidence status, “what not to infer,” authoritative links and subordinate provenance. Current Conversations disclosure follows actual provenance, and the feature remains closed. Corrections and removals retain their existing route and history. The ZIP manifest gives a SHA-256 digest for every included file.

## Review these first

1. `review/docs/reviews/gate-5h/public-copy-before-and-after.md`
2. `review/docs/reviews/gate-5h/non-academic-reader-comprehension-audit.md`
3. `review/reports/editorial/gate-5h-public-voice-diagnostic.md`
4. desktop/mobile/reflow screenshots under `review/screenshots/gate-5h/`
5. the four theme pages, representative idea cards and all seven Work pages in `rendered-root/`

## Owner questions

1. Does the site now sound like identifiable researchers rather than an institutional template?
2. Is the homepage more direct and memorable?
3. Do the theme examples help readers understand the distinctions?
4. Are technical terms explained without oversimplifying them?
5. Do the research ideas retain their intellectual depth with less repetitive presentation?
6. Do Work pages now suit their different kinds of research?
7. Does Our Approach become easier to understand when the example comes first?
8. Is Current Conversations clear to a reader unfamiliar with automated evidence systems?
9. Has any necessary qualification been lost?
10. Is the site ready to publish as Draft 0.1?
11. Should “Low carbon cities: is ambitious action affordable?” remain a prominent Delivery example?

## Next action

Review this package for voice, clarity and accessibility. If approved, decide the optional Delivery-example question, mark PR #1 ready, confirm final CI, merge with a merge commit, protect `main`, configure the `public-draft` environment and enabling variable, and manually publish Draft 0.1 through the guarded GitHub Pages workflow. Current Conversations should remain in development.
