# Gate 4B–5A rendered browser QA

Date: 2026-08-17  
Surface: local Quarto build in the Codex in-app browser; no external transmission.

## Views inspected

- Current Conversations at 1440 × 900: one H1, 25 cards, no horizontal overflow, visible disclosure and full navigation.
- Current Conversations at 390 × 844: one H1, collapsed navigation, single-column reflow, no horizontal overflow.
- Current Conversations at 200% browser zoom: content reflowed without horizontal page overflow; disclosure, filter and cards remained readable. The viewport screenshot is retained.
- Complete publication record at 1440 × 900 and 390 × 844: 36 bibliography entries, one H1 and no horizontal overflow.
- Multi-source detail at 1440 × 900: grouped label, two distinct source links and corrected H3 hierarchy for principal and related sources.

## Interaction and diagnostics

The theme filter reduced 25 entries to 10 evidence-infrastructure entries and Clear restored all 25. The live status text updated at each step. Desktop/mobile console checks returned no warnings or errors. Static accessibility checks passed all 88 built pages, including label/control associations, heading rules, image alternatives and landmark checks.

The in-app browser’s synthetic Tab command did not move page focus from `body`, so keyboard traversal was not independently proven through that browser surface in this run. Visible focus CSS and semantic controls remain covered by source/static tests; a manual screen-reader and keyboard pass is recommended before production.

## Defect found and resolved

The first render joined the related-source Markdown heading directly after the principal-source link, leaving it inline. The generator now inserts a blank line, the regression test requires it, and the rebuilt DOM exposes two separate source headings. No unresolved visual blocker was found.
