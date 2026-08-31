# Gate 5F browser and visual QA

Date: 2026-08-28  
Browser: Codex in-app Chromium browser against the deterministic local `_site` build at `127.0.0.1`  
Public deployment: none

## Dimensions and coverage

- Desktop: 1280 × 900 CSS pixels.
- Mobile: 390 × 844 CSS pixels.
- 200-percent-equivalent reflow: 720 × 900 CSS pixels, corresponding to a 1440-pixel desktop viewport viewed at 200%.
- Desktop inspection covered the homepage, four theme pages, Work landing page, all seven Work detail pages, Our Approach, Current Conversations and its method page.
- Mobile inspection covered the homepage, representative complete theme and Work pages, Our Approach, Current Conversations and its method page.
- Reflow inspection covered the homepage, a complete theme, a Work page and Our Approach.

## Results

- Every inspected page had exactly one `main` landmark and one `h1`.
- No horizontal overflow remained at desktop, mobile or reflow dimensions.
- An initial 1280-pixel check found 61–77 pixels of overflow on Work pages because Quarto positioned a semantic `aside` in its margin column. The generated metadata panel was changed to a labelled `section`; rebuild and repeat inspection returned zero overflow on all seven Work pages at every tested width.
- Homepage hierarchy, four theme propositions, three reader pathways, Featured Work and secondary Current Conversations treatment were visually distinct.
- Theme openings retained the full argument while proposition and boundary treatment was lighter than Gate 5E.
- Signature cards were distinguishable by restrained border treatment; additional directions retained equal legibility and no priority language.
- Work pages led with the problem and question; metadata remained discoverable later in the page without repeating the primary theme.
- The six-state approach and hypothetical illustration were legible and did not resemble a scoring or recommendation interface.
- The Work filters remained functional: seven records were initially visible and a `delivery` keyword filter reduced the visible set to three.
- No warning or error console messages were captured during principal-page navigation.
- Core content, links, headings, notices and lists are server-rendered HTML. JavaScript is progressive enhancement for search and filters; the site remains readable and navigable without it.
- `styles.css` retains an explicit 3-pixel `:focus-visible` outline with a 4-pixel offset for links, buttons and tabindex elements. Automated key dispatch in the in-app browser did not move focus from `body`, so focus styling was verified statically and remains covered by the rendered CSS review.

## Screenshot provenance

All files under `reports/screenshots/gate-5f/` were regenerated from the Gate 5F local build. Gate 5E screenshots were not copied or reused. Readable viewport captures use `*-opening.png`; full-page captures support complete owner review.
