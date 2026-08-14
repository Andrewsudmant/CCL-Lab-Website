# ADR 0002: Automated publication of unreviewed Research Watch items

- Status: Accepted
- Date: 2026-08-14
- Decision owner: Project owner
- Supersedes: ADR 0001 item-level approval requirement only

## Context

Research Watch is intended to provide timely awareness across academic research, policy reports, news, commentary, data tools and Bluesky discussion. Routine human approval of every item would turn the service into an intermittently updated curated bibliography and make its coverage dependent on reviewer availability.

The owner has decided that individual Research Watch records may be discovered, classified, summarized and published automatically. AI remains a processing mechanism, never the evidentiary source. Inclusion does not represent a lab judgement or endorsement.

## Decision

Human review is optional and is not a prerequisite for Research Watch publication. An automatically generated item may publish only after deterministic controls confirm complete provenance, sufficient evidence, valid structured output, thematic relevance, deduplication, acceptable risk and a successful site build.

Every automatically generated listing carries the compact label `AI-selected and summarized · not reviewed by the lab`. The landing page, homepage feed and methods page carry the fuller notice that automated searches and AI-generated summaries are normally unreviewed, may contain errors, and should be checked against the original source.

Public disclosure replaces any implication of endorsement; it does not replace quality controls. The original source remains directly linked and authoritative.

## Automatic withholding and quarantine

An item is withheld or quarantined when it has any of the following:

- no valid canonical URL or identifiable source;
- missing publication/posting date or retrieval date;
- title-only evidence for a substantive summary;
- inaccessible or insufficient evidence;
- unsupported factual claims or nonconforming model output;
- unresolved critical risk, suspected prompt-injection contamination or unexpected personal information;
- high duplicate probability or unresolved event-cluster conflict;
- thematic relevance below the configured threshold; or
- incomplete disclosure, provenance, prompt/model or discovery-run metadata.

Withheld records may expire automatically and do not require human adjudication. Quarantined records remain internal until they are corrected, expire or receive optional review.

## Changes that still require review

Pull-request review remains required for code, schemas, prompts, query packs, search and source policy, publication thresholds, disclosure wording, governance, security controls and workflow configuration. Automated content generation is separated from these human-reviewed control-plane changes.

## Corrections and removals

Published items retain an auditable correction/removal object and version history. Corrections disclose the date and nature of the change. Removal produces a tombstone or internal audit state rather than silent deletion, except where law or privacy requirements require erasure.

## Consequences

Research Watch can update without routine reviewer availability, but published summaries may be incomplete or wrong. Readers therefore receive conspicuous disclosure, evidence-basis information and direct source links. The project must monitor provenance completeness, broken links, duplicate/event rates, theme and source diversity, model/schema failures and correction/removal patterns.

## Reconsideration triggers

The lab will reconsider automated publication if monitoring shows persistent unsupported claims, inadequate disclosure comprehension, material copyright/privacy incidents, unacceptable correction volume, source manipulation, systematic thematic bias, unsafe prompt-injection behaviour, or failure rates above owner-approved thresholds. A major change in model, evidence access or legal/institutional requirements also triggers review.
