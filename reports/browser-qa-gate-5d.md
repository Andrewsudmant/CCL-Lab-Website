# Gate 5D browser QA

Date: 27 August 2026

Rendered commit family: Gate 5D on `codex/gate-5c-thematic-consistency`

Local origin: `http://127.0.0.1:4173/` serving `_site/`; no deployment

## Result

PASS with documented tooling limitations. Fresh screenshots are in `reports/screenshots/gate-5d/`; no Gate 5C screenshot is included in the Gate 5D package.

The in-app browser inspected the homepage, learning cycle, Work listing, all four theme pages, standalone Geography paper, Data Methodologies, Climate delivery modes, CoBen, Occupational transitions, UK Co-Benefits Atlas, completed/foundational and idea sections, Current Conversations, and the Projects transition route.

## Viewports and findings

| Surface | Viewport | Result |
|---|---:|---|
| Desktop | 1440 × 900 CSS px | All required pages rendered without horizontal overflow or captured console errors. |
| Mobile | 390 × 844 CSS px | All required pages reflowed without horizontal overflow; navigation, long titles, idea cards and method labels remained legible. |
| 200% equivalent | 720 × 900 CSS px | All required principal pages had `scrollWidth == clientWidth`; this conservatively represents a 1440 px desktop at 200% effective width. |

The browser did not expose a reliable numeric zoom state, so the enlarged check uses the documented 720-CSS-pixel equivalent rather than claiming a measured browser zoom percentage. Synthetic sequential Tab traversal remained limited, but a principal navigation link accepted keyboard focus and displayed a visible 3 px focus outline. Native form controls remain labelled, and static accessibility checks passed across all 112 rendered pages.

## Editorial inspection

- All four theme pages use the required order: purpose and boundary, ongoing work, selected completed/foundational work, research ideas, learning-cycle connections, and Current Conversations last.
- Theme descriptions remain readable and no status or maturity badge appears.
- Work cards expose type, ongoing/completed status, and relationship to the lab.
- Prior work is explicitly labelled foundational and does not imply SFU/CCLL authorship.
- The standalone Geography paper reads naturally without a parent project.
- Ideas use a distinct pale-ochre treatment and the exact non-active/non-funded disclaimer.
- Current Conversations retains its non-endorsement disclosure and truthful fixture provenance (`ai_provenance.used=false` does not claim AI generation).
- The former Projects route clearly transitions to Work and declares the Work route canonical.

## Evidence

- Desktop screenshots: `reports/screenshots/gate-5d/desktop/`
- Mobile screenshots: `reports/screenshots/gate-5d/mobile/`
- Enlarged-width screenshots: `reports/screenshots/gate-5d/zoom/`
- Console errors captured on principal pages: 0
- Horizontal-overflow failures: 0
