# Gate 5H browser QA

Date: 28 August 2026  
Builds: final Gate 5H working tree, later committed without further public-source changes  
Method: local HTTP servers and the in-app browser; no external network calls

## Coverage and result

Result: **PASS**.

- Homepage at 1440 × 1000, 390 × 844 and 640 × 900 (200%-equivalent reflow).
- All four theme openings and complete Geographies of Climate Learning page.
- All 24 idea cards: six per theme, two signature per theme, `One possible approach` on every card, 3/3/2/2/2/2 visible method-tag cadence per theme and accessible non-active/non-funded status.
- All seven Work pages, covering programme, research line, paper, completed project and tool structures.
- Our Approach, including illustration order and exactly six breakdown states.
- Current Conversations landing and methods pages.
- Root and `/CCL-Lab-Website/` project-path homepages.

## Observations

- Homepage principal text and all required section headings rendered in the intended order.
- The homepage has no horizontal overflow at desktop, mobile or 640-pixel reflow.
- Each theme displays a labelled practical example and inline first-use definitions before the formal argument. Current Conversations remains the last major theme section.
- Idea cards collapse to one 339-pixel column at mobile size. The G5 governance qualification and E1 no-ranking boundary remain in their generated pages.
- Work pages use the expected headings by type. Every public panel displays only Work type, Status, Main theme, Geographical focus and Key methods. Relationship/history remains in a native `details` element.
- Our Approach places the hypothetical active-travel illustration before the six states.
- Current Conversations renders no card, filter, count or feed. Non-endorsement remains visible.
- The project-path build loads its stylesheet through `/CCL-Lab-Website/`, and sampled internal links include that base path.
- No sampled page produced horizontal overflow. Browser console logs were empty.

## Keyboard and focus

Primary navigation, links and native `summary` controls are present in the focusable-element set. The stylesheet provides a 3-pixel blue `:focus-visible` outline with 4-pixel offset for links, buttons and explicit tabindex targets. The browser wrapper did not expose a reliable programmatic screenshot of focus after keyboard Tab, so focus styling was also verified statically; this bounded limitation is not a content or navigation failure.

## Visual judgement

The hero is direct and visually dominant without giving equal weight to the older Gate 5F proposition. Practical-example boxes clarify the theme distinctions without appearing as evidence. First-use definitions are compact and visually subordinate. Research ideas remain substantial but read less like a repeated form. The four Work structures are visibly distinct, and the short metadata panel no longer overwhelms the argument. Qualifications remain beside the relevant claim.

## Screenshots

Fresh screenshots are under `reports/screenshots/gate-5h/` for desktop, mobile, reflow and project-path views. Gate 5G screenshots were not copied into this review set.
