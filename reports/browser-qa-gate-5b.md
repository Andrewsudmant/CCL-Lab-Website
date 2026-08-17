# Gate 5B rendered browser QA

Date: 2026-08-17

Source: local deterministic `_site` build from the Gate 5B working tree

Browser: Codex in-app browser

## Viewports and pages inspected

- Desktop 1440 × 900: home, Current Conversations, verified publications, the August 2026 delivery-modes paper and one grouped conversation detail.
- Mobile 390 × 844: home, Current Conversations and verified publications.
- 200% layout equivalent 720 × 450: Current Conversations. This halves the desktop CSS viewport to exercise the same reflow pressure; the in-app browser did not expose a numeric zoom setting.

## Observations

- Each inspected page had exactly one H1 and a semantic main/navigation region.
- No inspected page had horizontal overflow: document width equalled viewport width at 1440, 720 and 390 CSS pixels.
- Current Conversations rendered 25 fixture cards; all 25 displayed `no AI generation recorded`, and no card claimed `Identified and summarized using AI`.
- Verified publications rendered 46 entries under the title “Verified publications and outputs.” The August 2026 paper, DOI and exact publication date were present.
- Navigation collapsed to the keyboard-operable mobile menu at 390 pixels.
- The browser recorded no console warnings or errors during the review sequence.

The screenshots under `reports/screenshots/gate-5b/` are the complete current review set. Earlier Research Watch and Gate 3B–5A screenshots were removed so the review package cannot mix stale and final rendered evidence.
