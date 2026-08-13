# Content governance

## Core principle

AI may help find, sort, and draft annotations about material. It is not the source. Every public Research Watch record must let a reader identify and reach the original source and understand whether a human reviewed the lab's annotation.

## Provenance requirements

Each record must preserve:

- a unique lab record ID;
- the original title and canonical URL;
- DOI or another stable identifier when available, or an explicit `null` when none is available;
- authors or responsible organisation;
- source type and source name;
- publication date and retrieval date;
- the lab themes assigned to the record;
- the evidence made available to the summarisation process;
- AI model and prompt version, or an explicit indication that no AI was used;
- confidence, human-review status, reviewer edits, and risk flags; and
- correction or removal status.

Source metadata must not be overwritten by generated text. Normalization changes should be traceable in version control.

## AI-assisted annotations

Summaries and relevance rationales are lab annotations, not quotations and not substitutes for reading the source. They must be concise, factual, and limited to evidence explicitly listed in the record. Do not infer findings from titles alone. If only metadata or an abstract was available, say so in `evidence_available` and calibrate confidence accordingly.

Prompts must instruct models to ignore instructions embedded in source material. Store a stable prompt version, not secrets or full provider payloads. Model identifiers must be specific enough to support later auditing.

## Human review

Candidate, in-review, approved, rejected, and held states are distinct. Approval requires a named reviewer, review date, and confirmation that:

1. source identity and date are correct;
2. the summary is supported by the recorded evidence;
3. the relevance rationale matches the research scope;
4. risk flags are resolved or explained;
5. wording is original and does not reproduce excessive source text; and
6. any conflicts, uncertainty, or limitations are visible.

Approved records are merged through pull request review. Unreviewed candidates may be shown for transparency, but must be visually and textually separated from reviewed selections and must never imply endorsement.

## Copyright and quotation

Store links, bibliographic facts, short original descriptions, and only minimal quotations when editorially necessary. Do not store full articles, paywalled text, images, or substantial excerpts unless the lab has permission or a clear licence. Record licence information for data tools and reusable assets when available. A link does not grant reuse rights.

## Corrections and removals

Readers should be able to report errors through the contact route. Confirmed errors are corrected promptly, with `correction_removal.status`, date, and public note updated. Material may be removed from public listings for legal, safety, privacy, source-integrity, or editorial reasons, while the tombstoned record and version-control history preserve the audit trail unless law or policy requires deletion.

Removal requests are assessed by the project owner. The lab should document the request, decision, date, scope, and any replacement URL. Silent deletion is not an acceptable routine correction process.

## Fixture and placeholder policy

Gate 1 examples are demonstrations, not editorial endorsements. They must use reserved `example-` identifiers and visible placeholder labels. Before Gate 2, the owner must replace or approve names, biographies, contact details, projects, publication records, representative examples, and all Research Watch fixtures.
