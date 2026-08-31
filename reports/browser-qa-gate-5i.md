# Gate 5I browser QA

Reviewed locally in the real in-app browser; no public deployment. Both complete site builds are included in the owner archive. The final 102-case screenshot matrix was regenerated from public-source commit `7376ab3`; subsequent release-documentation commits do not alter the site.

| Dimension | Root routes | Project-path routes | Overflow | Broken images | Recorded console errors |
|---|---:|---:|---:|---:|---:|
| Desktop, 1440 × 1000 | 17 | 17 | 0 | 0 | 0 |
| Mobile, 390 × 844 | 17 | 17 | 0 | 0 | 0 |
| Narrow reflow, 320 × 800 | 17 | 17 | 0 | 0 | 0 |

All 102 cases retain the draft banner. `reports/screenshots/gate-5i/browser-measurements.json` records route, heading, dimensions, DOM focusable order and browser errors; final screenshots use the same matrix. Coverage: homepage, all four themes, Work landing, programme/project/tool/paper Work types, Publications landing/full list, metadata page, low-carbon-cities and August 2026 delivery-paper details, Our Approach and Current Conversations.

The 320-pixel review found a long Consequences heading and intrinsic Work-filter width overflowing by 15 and 4 pixels. A narrow heading rule and shrinkable form controls fix both; the complete matrix was repeated after the fix. The navbar focus outline was being overridden; explicit focus-visible styling now remains visible, with native input/select/summary coverage. No research wording or record changed in those repairs.

Pointer interactions open the mobile menu and Citation disclosure. Work keyword `delivery` changes the count from seven to three; Clear restores seven. Publication keyword `low carbon cities` returns one record and Clear restores 46 in the browser; all 46 indexed records are also regression-tested. The low-carbon-cities item remains in the complete/selected bibliography and search while prominent Delivery count is five. Current Conversations displays development copy only, no fixture feed.

The human visual review checked page typography, metadata readability, status, source/correction routes, mobile navigation, draft banner and representative lower-page sections. Native smooth scrolling needs time to settle before section screenshots. Full-page stitched captures produced duplicated tiles in this wrapper, so they were discarded and replaced with reliable viewport/section screenshots; complete HTML is provided for owner inspection. Before screenshots were reproduced from the actual Gate 5H commit in an isolated detached checkout, not from an owner ZIP. No current Research Watch screenshot was reused.

Sequential keyboard delivery remains unreliable through the wrapper. Computed focus and actual control behaviour are distinguished from unproven Tab traversal in `reports/accessibility/gate-5i-keyboard-navigation.md`. The 320 CSS-pixel viewport is a reflow simulation, not a claim that real 200% browser zoom or a screen reader was tested. The exact five-minute owner check includes real zoom and keyboard traps.

Only current Gate 5I screenshots appear in this package; historical Gate 5H evidence remains intact in Git. Any final documentation/package-only commit does not change the reviewed public source. The archive manifest identifies the final source SHA and hashes every included rendered file and screenshot.
