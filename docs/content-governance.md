# Content governance

## Core principle and disclosure

AI may discover, classify and summarize material. It is not the source. Every public record links to the original source, describes the evidence available to the system and states whether human review occurred.

Automatically generated material normally publishes without human review when deterministic controls pass. It must never be described as endorsed, recommended, approved, expert-selected or reviewed by the lab.

The full public notice is:

> Research Watch uses automated searches and AI-generated classification and summaries. Items have not normally been reviewed by a member of the Cities & Climate Learning Lab, and inclusion does not imply endorsement. Summaries may contain errors or omit important context. Please consult the original source.

Each unreviewed item carries: **AI-selected and summarized · not reviewed by the lab**.

## Required provenance

Each public Research Watch record preserves:

- unique record and discovery-run IDs;
- canonical title, URL and stable/platform identifier where available;
- authors or responsible organisation, source name and source type;
- publication/posting date, retrieval timestamp and adapter;
- query-pack/theme-query version;
- primary and secondary theme assignments with score and rationale;
- separate geographical tags;
- concise summary and relevance note;
- exact evidence types and a limitation statement;
- model, prompt and structured-output versions;
- confidence label and basis;
- publication decision, deterministic checks and risk flags;
- optional human reviewer/date/edits; and
- correction, availability and removal status.

Source metadata is never overwritten by generated text. Normalization and classification transformations remain traceable in the run manifest.

## Evidence-constrained annotations

Academic findings or methods require at least an abstract or legally accessible full text. News, blogs and institutional summaries require page-body evidence; search snippets may support only a clearly limited discovery note. Bluesky content is minimized and, when it links to an underlying paper/report, is treated as commentary around the principal source.

Titles alone cannot support substantive findings. Summaries must be concise, original, factual and limited to recorded evidence. Prompts instruct models to ignore embedded instructions and return explicit evidence limitations.

## Automated publication

Human review is not required. Publication requires a valid source, date, evidence basis, complete provenance and disclosure, sufficient thematic relevance, successful schema validation, no critical risk, no unresolved duplicate/event conflict and a successful site build.

Items with unsupported claims, missing identity/date, title-only inference, inaccessible evidence, suspicious URLs, prompt-injection contamination, unexpected personal data or nonconforming output are withheld or quarantined. Failure does not create a reviewer obligation and must not alter the last valid public store.

## Optional human review

Human review may occur before or after publication. A factual reviewed label requires reviewer identity and review date. Reviewer edits remain recorded. Absence of those fields always renders the automated, unreviewed label.

## Code and policy review

Changes to code, schemas, prompts, query packs, source policy, thresholds, disclosure language and governance require pull-request review. Individual records generated under those reviewed controls do not.

## Copyright, corrections and removal

Store bibliographic facts, minimal identifying excerpts and original annotations—not unrestricted full articles, paywalled text or raw provider payloads. A link does not grant reuse rights.

Corrections record date, reason and changed fields. Removal or archival records the decision and preserves an audit trail unless legal/privacy requirements mandate erasure. Scheduled rechecks record broken or redirected sources and availability changes.
