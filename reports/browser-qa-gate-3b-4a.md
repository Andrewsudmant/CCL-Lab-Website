# Browser QA — Gate 3B–4A

Date: 2026-08-14  
Browser: Codex in-app Chromium browser  
Local origin: private `http://127.0.0.1` server; no deployment

## Coverage

Every principal route was loaded and inspected at 1440×1000 and 390×844: Home, Research, all six theme pages, Projects, a current project, a foundational project, People, Outputs, Publications, a long-title/long-author publication, Data and Tools, Research Watch, Research Watch methods, Opportunities, About Andrew and Contact.

At each route the browser confirmed one visible H1, a main landmark, zero broken images and no horizontal document overflow. Theme 5 showed established presentation; Themes 4 and 6 showed developing badges. Current and foundational headings, no-photo People layout, Research Watch disclosures, filters and provenance details were inspected.

## Interaction and accessibility checks

- Desktop Outputs dropdown opened and exposed Publications and Data & Tools; focus remained on the trigger.
- Mobile navigation toggle was discoverable by accessible name, opened correctly and exposed Research.
- Visible keyboard focus styling and `prefers-reduced-motion` overrides are present in the stylesheet.
- At a 640-CSS-pixel reflow test (equivalent to a 1280-wide page at 200% zoom), Home, the longest publication title and Research Watch had no horizontal overflow.
- Browser console warnings/errors: 0.
- Static accessibility check: pass on 34 HTML pages.
- Internal links: pass.

## Screenshot notes

Desktop captures are full-page JPEG files. The browser backend’s mobile full-page stitching produced distorted review images, so the review package intentionally uses accurate 390×844 viewport JPEGs for mobile. The DOM geometry and overflow checks still covered the full page at every route. The 200%-equivalent captures are 640×900 viewport JPEGs.

## Unresolved visual/rights notes

- No portrait is shown; an owner-supplied or rights-cleared image can be added later but is not a launch blocker.
- No SFU logo is used because no approved asset was supplied.
- The local test server requested an unspecified `/favicon.ico` and received 404; this did not produce a browser console error or affect navigation. A rights-neutral project favicon can be selected before production.
