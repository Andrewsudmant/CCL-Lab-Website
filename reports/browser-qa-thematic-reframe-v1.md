# Browser QA — thematic architecture reframe v1

Date: 2026-08-21  
Surface: final local Quarto build served only on `127.0.0.1`  
Viewports: 1440 × 900 desktop and 390 × 844 mobile

## Results

- Homepage: one H1, four cycle stages in canonical order, no horizontal overflow.
- Conceptual order in rendered DOM: themes before projects; projects before Current Conversations.
- Desktop cycle: 1084 px grid and 1083 px return connection after correction of a global list-item `max-width` interaction.
- Mobile cycle: all four stages share the same x-position and have increasing y-positions; the return note spans the 304 px grid width.
- Mobile navigation collapses; no horizontal overflow at 390 px.
- All four theme pages have one matching H1, the required sections and no horizontal overflow.
- Representative climate-delivery project visibly contains “How this project contributes to climate learning.”
- Current Conversations shows 25 fixtures, the full adjacent disclosure and six filter states: four themes, all states, and cross-cutting/unclassified.
- Selecting cross-cutting/unclassified displays three fixtures.
- Browser console: no warnings or errors observed.

## Screenshots

Final screenshots are under `reports/screenshots/thematic-architecture-reframe-v1/`. The set includes desktop and mobile homepage views, desktop and mobile learning-cycle evidence, every theme page, a representative project, and Current Conversations.

## Limitation

This was local static-site QA, not production hosting QA. External-link checks were not run as part of the browser session; the internal route checker passed separately.
