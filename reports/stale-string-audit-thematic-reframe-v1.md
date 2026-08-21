# Stale-string audit — thematic architecture reframe v1

Date: 2026-08-21

## Current public build

Repository-wide exact-title searches were followed by a rendered-site search. No current research, homepage, project, publication or Current Conversations page displays any of these former theme titles as a theme label:

- Urban climate learning and evidence transfer
- Climate governance and delivery modes
- Co-benefits, co-costs and place-based valuation
- Just transitions, occupations and workforce change
- Urban climate evidence infrastructure and decision-support tools

The words “Canadian climate policy” remain in one external fixture's relevance text because the approved architecture retains Canadian climate policy as a topic and geography facet. It is not rendered as a fifth theme or filter.

The former-name phrase “Research Watch” remains visible only on `/research-watch/index.html` and `/research-watch/methods.html`, where it explains that those former routes moved to Current Conversations.

## Controlled configuration and records

No obsolete theme ID remains in `config/`, `data/`, `schemas/`, `prompts/` or `current_conversations/`. The only current source-code references to old IDs are the reviewed redirect map and retired-ID validator; tests also name them to assert their absence and route preservation.

## Historical audit evidence

Older gate reports, baselines, ADRs, handoffs, staging snapshots and calibration evidence intentionally retain the terminology that was current when they were created. They are not current public programme copy and were not rewritten, because altering them would weaken the decision trail.

Publication titles and externally sourced titles were preserved exactly even when they contain generic promotional wording or a phrase such as “data-driven.”
