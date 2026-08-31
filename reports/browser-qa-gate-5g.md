# Gate 5G browser and visual QA

Date: 2026-08-28  
Source commit for public site files: `0c23b3861e539b8f0623619914ad614a75f4b177`  
Browser: Codex in-app Chromium browser against deterministic local builds  
Public deployment: none

## Dimensions and coverage

- Desktop: 1280 × 720 CSS pixels.
- Mobile: 390 × 844 CSS pixels.
- 200-percent-equivalent reflow: 720 × 900 CSS pixels, corresponding to a 1440-pixel layout viewed at 200%.
- Desktop and mobile inspection covered the homepage, all four theme pages, Work landing page, all seven Work detail pages, Verified publications and outputs, Our Approach and Current Conversations.
- Reflow inspection covered the homepage, all four theme pages, Work, Verified publications and outputs, Our Approach and Current Conversations.
- Separate project-path inspection covered the homepage and a clicked theme-page navigation under `/CCL-Lab-Website/`.

## Results

- Every inspected page had exactly one `main` landmark and one `h1`.
- No inspected viewport had horizontal overflow or a broken image.
- Visible page text contained no raw HTML entities, Gate/owner-review language or machine-facing governance terminology.
- Homepage, theme, Work and Current Conversations openings retained the intended hierarchy at desktop and mobile sizes.
- The mobile navigation collapsed to its labelled menu control; headings and the Draft website notice reflowed without clipping.
- Current Conversations remained clearly marked **In development** and showed no public entries, count, feed or endorsement language.
- Searching for `delivery modes` opened the Quarto search overlay and returned nine matching documents, led by the relevant Work and publication pages.
- A real click from the project-path homepage reached `/CCL-Lab-Website/research/geographies-of-climate-learning.html`; the page had no broken image or overflow.
- No warning or error console messages were captured on the root or project-path tabs.
- Browser checks agree with the static link and accessibility checks for both 87-page builds.

## Screenshot provenance

All files under `reports/screenshots/gate-5g/` were generated from the Gate 5G release-candidate build. No Gate 5B–5F or Research Watch screenshot was copied into this set. The set contains:

- 17 desktop captures, including search results;
- 16 mobile captures;
- 9 reflow captures; and
- 2 project-path captures.

The in-app browser screenshot API captures the visible viewport. Complete page review is therefore supported by the two complete rendered-site artifacts in the owner package, alongside the opening-state captures.

