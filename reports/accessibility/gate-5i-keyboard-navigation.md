# Gate 5I keyboard navigation

Status: **READY_SUBJECT_TO_OWNER_MANUAL_KEYBOARD_CHECK**. Automated sequential keyboard navigation is **not certified**. This is the bounded owner check permitted by the brief, not a claimed keyboard pass.

## Concrete browser attempts and evidence

The real in-app browser was used. From homepage body, a Tab press left focus on BODY. Targeted Tab on the Research link focused that link, but subsequent Tab through both supported keypress routes left it there. Enter targeted at the mobile navigation button focused it without expanding it; Enter targeted at native Citation focused SUMMARY without opening it. These consistent failures across native and framework controls indicate an unreliable key-delivery wrapper; they do not establish whether real hardware keyboard navigation passes.

Pointer activation successfully expands the mobile menu and native Citation disclosure. The focus CSS is verifiable: Research navigation, mobile menu, input and Citation summary show `rgb(11, 101, 194) solid 3px`, with a four-pixel offset. The initial navbar outline was overridden by Bootstrap; a scoped focus-visible override fixes that real defect. Screenshots in `reports/screenshots/gate-5i/keyboard/` distinguish the initial attempt from fixed indicators.

## Static order and remaining uncertainty

Both profiles contain semantic navigation, main and footer landmarks, native links, labelled inputs/selects and native details/summary. No positive tabindex occurs in the 88-page site. `browser-measurements.json` records the visible DOM focusable order for every reviewed route and dimension; this is **not an observed Tab sequence**.

Expected order: brand/search/navigation, main-page links and controls in source order, then footer contact/method/correction links. Collapsed mobile navigation exposes the toggle before its expanded links. Theme pages place connected Work, selected examples and research-idea disclosure controls in reading order. Work filters precede records; the publication listing's keyword/type/reset controls precede bibliography links. Publication detail order is DOI, theme/Work links when present, original source, Citation, metadata/correction links, footer. Current Conversations has method/contact links but no content filters or feed entries.

There is no custom skip-navigation link to certify. Main landmarks and headings support assistive-technology navigation; ordinary Tab traversal still includes the header. No scripted positive focus order was added. Absence of traps, reverse traversal, dropdown keyboard handling, Escape behaviour and sticky-header focus visibility require the manual check below. Narrow reflow was tested separately at 320 CSS pixels; it is not a substitute for real browser zoom or screen-reader review.

## Five-minute owner checklist

Use the packaged site through a local HTTP server, or the local preview, in a normal desktop browser. Enable full webpage keyboard navigation first (Safari: Settings → Advanced → Accessibility → “Press Tab to highlight each item on a webpage”; macOS may also require Keyboard navigation). Do not click between sequential Tab steps except to open each next named test page. Repeat any failure in a second browser before classifying it.

1. **0:00–1:00 — Homepage and navigation.** Load `/index.html`. Tab from the address bar into the page, then through header controls and main links. Each stop must have a visible outline and follow reading order. Use Enter on Outputs and About; reach submenu links and use Escape to dismiss. Shift+Tab must reverse without a trap. Narrow to a mobile width; Tab to Toggle navigation, Enter/Space to open, traverse links and close. Focus must remain visible, not hidden behind the sticky header.
2. **1:00–2:00 — Theme and research ideas.** Open `/research/modes-of-climate-delivery.html`. Tab through Work and the five selected examples to “Questions this theme opens”. Reach signature and additional directions and any native disclosure; Enter/Space must toggle without skipping the rest. Confirm reverse Tab works. Use the browser's landmark/heading navigation if supported; do not assume a skip link exists.
3. **2:00–3:00 — Work.** Open `/work.html`. Tab to Keyword, type `delivery`, use the select controls with arrow keys, then Clear. Results/count must update and all seven records return after reset. Open `/work/climate-delivery-modes.html`, traverse source/output links, and return with browser Back. No trap or clipped focus.
4. **3:00–4:00 — Publications.** Open `/publications.html`, follow the full verified list; type `low carbon cities` in Keyword and clear it. Open `/publications/low-carbon-cities-affordable.html`. Reach DOI, original source, Citation and metadata/correction links. Enter/Space on Citation must expand/collapse; Tab can leave it. Visit `/publications/metadata-and-sources.html` and check Corrections.
5. **4:00–5:00 — Current Conversations and footer.** Open `/current-conversations/`, traverse method/contact/footer links and reverse with Shift+Tab. It must remain in development, with no feed/filter controls. At 200% browser zoom confirm usable navigation, visible focus and no horizontal scrolling of ordinary text. Record browser/version, date, reviewer and PASS or the exact route/control/keystroke that failed.

If all steps pass, record the owner's result in the PR/release record before merge. Any reproducible keyboard trap, unreachable control or invisible focus is a release blocker: keep deployment disabled and request a bounded correction. Do not treat this checklist as completed until the owner supplies a result.
