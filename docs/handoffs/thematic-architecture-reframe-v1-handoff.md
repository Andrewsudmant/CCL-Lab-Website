# Cities and Climate Learning Lab thematic reframe handoff

## What changed and why

The website now presents the lab as one cumulative programme rather than six adjacent topics and an external-content feed. Four exact questions move from existing knowledge across places, to choices about new evidence, to institutional delivery, to consequences—and visibly return to further evidence and learning. This puts the lab's intellectual identity before Current Conversations.

The existing Quarto architecture, design system, accessibility provisions, feed pipeline, provenance controls, tests and deployment boundaries were preserved. Current Conversations was aligned to the new taxonomy without becoming an evidence rating, matching or recommendation system.

## Challenges and decisions

The former themes did not map one-for-one. Data tools, Canadian policy, sectors and methods were separated into facets; project and publication mappings follow their analytical contribution. Three external fixtures remain unclassified because their available evidence does not justify a lab-theme claim. Former static URLs are preserved through transition pages because a static Quarto build cannot issue server redirects.

Visual QA exposed one CSS interaction that narrowed the return note. It was fixed with a scoped override and rechecked at 1440 × 900 and 390 × 844.

## Transparent and traceable governance

The theme registry, project mappings, route decisions and tests are versioned. Original source metadata, stable identifiers, retrieval evidence, AI provenance, review status and correction history remain unchanged. Theme classification is explicitly separate from evidence quality, endorsement and transferability. Non-AI fixtures continue to disclose that no AI generation or live retrieval is recorded.

## What to consider next

- Owner-review the six project mappings and learning-contribution text.
- Confirm whether Theme 2 should remain labelled developing.
- Calibrate live Current Conversations examples before changing fixture classifications.
- Decide whether the featured homepage project selection best represents the programme.
- If production routing later supports redirects, replace transition documents with reviewed 301/308 rules while retaining the migration record.

## Verification and boundaries

Validation, 85 tests, the 103-page build, internal links and static accessibility checks pass. Desktop/mobile browser QA passes with no console warnings. One compatibility-import deprecation warning remains. No deployment, merge, paid or model API call, secret change, permission change or history rewrite occurred.

The credential-free four-theme OpenAlex connectivity diagnostic completed without provider errors, but its deliberately narrow phrase queries returned no results. This is a calibration question for later work, not evidence that no relevant research exists.

A non-disclosing scan found no suspected credentials or private keys in reachable Git history or present repository files. No secrets were added to fixtures, prompts, logs or packages.
