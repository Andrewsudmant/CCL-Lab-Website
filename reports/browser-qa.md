# Rendered-page QA

Date: 2026-08-14  
Browser: Codex in-app browser  
Local URL: `http://localhost:8765/` (not deployed)

## Coverage

The ten principal pages were opened from the rendered `_site` build and captured at
desktop (actual capture 1333 × 1000) and mobile (390 × 844) viewport sizes:

- Home
- Research
- Projects
- People
- Publications
- Research Watch
- Data & Tools
- Opportunities
- About Andrew
- Contact

The 20 PNG captures are stored under `reports/screenshots/desktop/` and
`reports/screenshots/mobile/`.

## Results

- Every page returned the expected H1 and rendered without horizontal overflow at
  the mobile viewport.
- Navigation collapses to a labelled mobile menu; focusable search remains visible.
- The Research Watch full disclosure is prominent at both sizes.
- Every automated item carries the compact “AI-selected and summarized · not
  reviewed by the lab” label.
- Search and theme filtering were exercised: a Canadian-policy filter returned zero
  visible items and updated its live count; searching `stocktake` restored the one
  matching record.
- Browser console inspection after the interaction found no warnings or errors.
- Homepage and Research Watch desktop/mobile captures were visually inspected. An
  initial full-page screenshot stitching artefact was detected; all supplied images
  were replaced with stable viewport captures.

## Limitations

- Static checks and the browser inspection are not a substitute for a full WCAG audit
  with assistive-technology users.
- Safari, Firefox and high-zoom testing remain outstanding.
- Only the first viewport is captured for each principal page; the complete long-page
  content was checked through DOM and static accessibility inspection rather than
  stitched full-page images.
