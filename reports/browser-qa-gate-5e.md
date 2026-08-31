# Gate 5E browser QA

- Date: 2026-08-27
- Local URL: `http://127.0.0.1:8765/`
- Deployment: none
- Browser: Codex in-app Chromium browser
- Viewports: desktop 1440×1000; mobile 390×844; 200%-equivalent reflow 720×900

## Pages inspected

Homepage and learning cycle; all four complete theme pages; all four idea sections; G5 research-governance qualification; E1 no-ranking boundary; Work; Current Conversations landing and methods; Draft website banner; footer; and public search results.

## Results

- PASS — the banner spans the viewport on standard and full-width layouts, has `role=status`, and remains compact (about 40 CSS px on desktop).
- PASS — every theme displays exactly six idea cards; desktop uses two approximately 582 px columns, while mobile and 720 px reflow use one column.
- PASS — desktop, mobile and 200%-equivalent pages reported `scrollWidth == innerWidth`; no horizontal overflow was observed.
- PASS — G5 displays the exact partner-led research-governance qualification; E1 displays the exact academic-question/no-ranking boundary.
- PASS — Current Conversations displays `In development`, has no conversation cards, filters, item counts, fixture timestamps or feed controls, and reads as intentionally unfinished rather than broken.
- PASS — public search returned `Distributional reversals over time` on the Consequences theme page. Fixture leakage is separately checked against the rendered site, search index and sitemap.
- PASS — keyboard focus on the navbar brand computed to a solid 3 px blue outline with a 4 px offset.
- PASS — inspected browser logs contained no warning or error entries.
- PASS — core navigation and content are server-rendered and remain usable without JavaScript; JavaScript enhances search and filters only.
- PASS — heading hierarchy, line length, footer, contrast and card legibility were visually inspected on representative pages.

Fresh evidence is under `reports/screenshots/gate-5e/{desktop,mobile,zoom}/`. No Gate 5D screenshot is included in the Gate 5E package.
