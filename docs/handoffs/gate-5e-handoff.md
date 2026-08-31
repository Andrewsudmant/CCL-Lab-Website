# Cities & Climate Learning Lab — Gate 5E handoff

Status: `GATE_5E_PASS_DRAFT_0_1_CONTENT_CANDIDATE`

## What changed and why

Gate 5E applied the McEnerney-informed reader-value principle: public copy should show the problem a reader can understand differently, not merely name a topic. Each theme now moves from a stable but incomplete understanding through instability and consequence to an analytical intervention, changed understanding and boundary. Theme 2 explicitly rejects the gap trap: missing evidence matters only when producing it could change understanding, appraisal or action.

The owner-approved idea portfolio expanded from 13 to 24 ideas, six per theme. Each record connects a working title, problem, question, consequence, possible research design and methods and says exactly that it is not currently active or funded. The migration table maps every former ID to its successors. The G5 community/Indigenous research-governance qualification and E1 no-ranking boundary are explicit.

Gate 5D Work and publication records remain canonical. Previous-work examples were frozen byte-for-byte and by rendered ID/order so this editorial gate could not silently change source-supported relationships. They require a separate owner review before publication.

Current Conversations is visible but intentionally in development. The public build has no fixture cards, detail pages, filters, counts, timestamps or feeds. Fixture data remains only for tests and future interface/schema work. A single `config/site.yml` source produces the accessible Draft website notice and keeps the feed disabled.

## Challenges and controls

The larger idea portfolio risked turning methods into disconnected lists and making theme pages too dense. The schema now requires a coherent possible design, cards expose the question and payoff without accordions, method tags are capped at five, and the layout moves from two columns to one on mobile. Legacy tests that expected the earlier fixture prototype were migrated to the in-development contract; the underlying clustering and provenance tests remain.

Traceability is maintained through canonical YAML, JSON Schema, the 13-to-24 migration, ADR 0005, deterministic audits, exact qualifications, byte-level previous-work hashes, generated-page order tests, public-leakage tests and the Git/PR history. Original sources remain authoritative. No paid call, secret access, staging write, deployment, merge or history rewrite occurred.

## What remains before public Draft 0.1

The owner must review the Gate 5E content candidate, then separately review the frozen previous-work examples. PR #1 must remain draft until those decisions are incorporated and final CI passes. Merge, branch protection and GitHub Pages configuration are later owner-controlled actions. Current Conversations launch remains a separate future gate.

## Git state

- Branch: `codex/gate-5c-thematic-consistency`
- Pull request: #1, retained as draft
- Deployment: none

## Exact next owner action

Review the Gate 5E Draft 0.1 content candidate, focusing on the four theme arguments, the 24 research ideas, page readability and the Current Conversations in-development state. The selected examples of previous work remain intentionally unchanged and will receive a separate owner review before publication.
