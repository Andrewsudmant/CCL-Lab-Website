# Browser QA — Gate 5C

Run date: 26 August 2026  
Build inspected: 103-page deterministic Quarto build from `codex/gate-5c-thematic-consistency`.

## Viewports and routes

The homepage, research overview, Our approach, all four theme pages, six project pages, Projects, Outputs, Current Conversations, a representative detail page, the methods/disclosure page and a former-theme transition page were inspected at 1440 × 1000 and 390 × 844 CSS pixels.

Every inspected page had:

- exactly one H1 and a `main` landmark;
- no empty H1–H3 headings;
- document `scrollWidth` equal to `clientWidth` at both widths;
- a responsive navigation control at mobile width; and
- no captured console warning or error.

The transition page exposes `/research/where-new-evidence-matters.html` as its canonical. All active theme pages expose their current canonical route.

## Learning cycle and hierarchy

The homepage text order is problem → four themes → cycle return → featured projects → SFU/geographical context → Current Conversations → people/contact. Theme order matches the registry. The return text is visible without JavaScript and says that consequences generate further learning and return unresolved questions to earlier stages. The cycle had no horizontal overflow at desktop or mobile width.

## 200% equivalent

The in-app browser surface did not expose or report a reliable browser zoom change after standard zoom shortcuts. A 720-CSS-pixel viewport was therefore used as the conservative layout equivalent of a 1440px viewport at 200% for the homepage, Research and Current Conversations. All three retained `scrollWidth == clientWidth`; the learning cycle also retained `scrollWidth == clientWidth`. This verifies reflow/overflow behaviour but is not a claim that the browser UI displayed an independently measurable 200% zoom state.

## Keyboard and focus

Navigation and filter controls are native links, buttons, inputs and selects with no positive `tabindex` ordering. Focusing the brand link produced a visible 3px solid outline. The mobile menu control is a native button labelled “Toggle navigation”, controls `navbarCollapse`, and updates `aria-expanded` when activated. The browser automation surface did not propagate synthetic Tab/Space traversal reliably after focus, so a complete automated sequential-key trace is not claimed. Static accessibility checks and semantic/native-control inspection passed.

## Screenshots

Fresh Gate 5C screenshots are in `reports/screenshots/gate-5c/`:

- `desktop/home.png`
- `desktop/learning-cycle.png`
- `mobile/home.png`
- `mobile/learning-cycle.png`

Only this Gate 5C screenshot directory is included in the owner-review package. Former-gate screenshots are excluded as historical artifacts.

Result: pass, with the documented browser-zoom and synthetic-key limitations.
