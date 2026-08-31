# Content governance

## Public promise

Current Conversations uses automated discovery and AI-assisted annotation to surface material across research, policy, news, commentary and tools. AI is never treated as a source. Readers receive the original link, source identity/date, evidence limitation and review state. Inclusion does not imply endorsement.

Current Conversations is horizon scanning around the questions the lab studies. A theme assignment records a bounded classification, not evidential quality, transferability or recommendation. Geography, source type and topic remain separate from lab theme. Records may be cross-cutting or unclassified when available evidence does not justify an assignment.

The compact unreviewed label follows the record, not the system's potential capabilities. Use **Identified and summarized using AI · not reviewed by the lab** only when `ai_provenance.used=true`. Captured fixtures with `used=false` say **Captured fixture · no AI generation recorded · not reviewed by the lab**. The landing page also warns that summaries may contain errors or omit context and asks readers to consult original sources.

The four research-theme titles, guiding questions, descriptions and analytical boundaries are owner-approved and canonical in `config/research_scope.yml`. Themes do not have active/completed or maturity status. Research-work relationships must be supported by project material, a canonical publication, an institutional record or an explicit owner-approved programme description; optional learning fields remain absent when evidence is insufficient. Methods and geographies must not be promoted into competing top-level themes.

## Themes, work, outputs and ideas

Themes are current intellectual questions. Research work records actual ongoing or completed activity and must identify its type and relationship to the lab. Prior work may appear as a defensible example of a current theme without being relabelled as a CCLL output. A standalone paper may connect directly to themes and must not receive an invented project parent. Bibliographic facts stay in the canonical publication record and are derived by work rendering rather than copied.

Research ideas are a separate editorial class. Each must state a question, why it may matter, suggested methods, owner-review state and the exact non-active/non-funded disclaimer. Ideas contain no invented funders, partners, dates, deliverables, findings or recruitment claims. They are excluded from Work, publications, Current Conversations, RSS and active/funded counts.

Selected publication examples require a recorded thematic rationale and the authoritative evidence source used to support it. Titles alone are insufficient. MDPI publications may remain in the complete verified bibliography under owner policy but cannot become selected thematic examples.

## Required provenance

Every source retains its source/run ID, original and canonical URL, stable identifier where available, authors or organisation, publisher/platform, source environment and role, publication and retrieval dates, exact evidence basis and limitation, query/adapter version, AI model/prompt when used, risk flags, availability, review and correction state. Every cluster retains its principal and linked source IDs, clustering method/confidence/rationale, themes, dates, summary, uncertainty, decision and history. Cross-source grouping accepts DOI, canonical URL, underlying-source/citation links, platform identifiers, or corroborated organisation-plus-title evidence; a model proposal alone can never merge records.

Bibliographic identity is provider-, repository- or owner-derived, never rewritten by AI. ORCID-only entries remain withheld until an institutional, publisher or commissioning source verifies the record. Explicit overrides retain their authoritative URLs and retrieval date. Captured fixtures are labelled in their records and reports. Public fixture examples are demonstrations, not evidence of present-day provider coverage.

## Evidence-constrained annotation

Academic claims require an abstract or lawful full text; metadata alone supports bibliographic statements only. News, institutional pages, blogs and tools require recorded page evidence. Search annotations are discovery signals, not evidence for substantive claims. Social discussion is commentary and should link to underlying evidence when available. Models are instructed to ignore source-borne instructions and produce only schema-constrained annotations based on recorded evidence.

## Human review and publication

Unreviewed material is not described as approved, selected, recommended or expert-reviewed. A reviewed label requires reviewer identity and date; edits remain traceable. Control-plane changes—code, schemas, prompts, query/source policy, budgets, thresholds, disclosure and workflows—require pull-request review. Content-plane records may be automated only after provenance, evidence, scope, duplicate, risk, diversity, schema, budget and build controls pass.

## Copyright and privacy

Store bibliographic facts, minimal necessary excerpts and concise original annotations, not full articles, paywalled text or raw provider responses. A link does not grant reuse rights. Avoid unexpected personal data; minimize social-post retention and honour lawful privacy or copyright requests.

## Corrections, availability and removal

Never silently rewrite or delete a public item. Record changed fields, date and reason; update availability after rechecks; archive stale discussions; and retain a correction/removal history unless legal or privacy duties require erasure. Critical errors, prompt-injection contamination, unsafe URLs, unsupported claims or identity conflicts are withheld or quarantined, leaving the last valid site intact.

### Themes and discovery facets

Current Conversations classification connects a source to one or more of the four analytical questions; it does not rate evidence or recommend action. The discovery query, source environment and location cannot determine the classification. Geography, sector, method and climate domain remain separate facets. A data tool, model, Canadian source or workforce source may relate to any theme—or remain unclassified—depending on the evidence actually available. `Where New Evidence Matters` is used only for a prospective, consequential evidence question, not for a generic gap, new dataset or new tool.

## Reader-value presentation

Gate 5F separates stored editorial structure from visible public scaffolding. Theme, idea and Work records retain distinct problem, consequence, approach, evidence-status and boundary fields even when templates combine them into fewer reader-facing sections. This preserves provenance and makes later corrections field-specific.

Signature research questions are a reading hierarchy, not a statement of priority, funding readiness or importance. Public method tags are a reviewed subset of the unchanged full method list. Reader or decision-at-stake fields may identify a class of reader already supported by the approved idea, but must not invent users, funders, partners or demand.

Ongoing Work uses prospective language and completed Work uses source-backed language. A missing section is preferable to generic or unsupported prose. The active-travel example is a hypothetical illustration and must remain visibly labelled as neither a finding nor a recommendation.

Gate 5G separates underlying thematic relationship from featured display. A record may remain related to a theme without appearing among its four to six illustrative examples. Public copy states the conceptual contribution; internal records retain the source reviewed, selection basis, uncertainty and correction trail. Cross-listing requires a genuinely different contribution statement for each theme and normally stops at two themes. Removing an item from prominent display never deletes it from the verified inventory or changes authorship and relationship-to-lab provenance.

Controlled-vocabulary values remain stable in data but render through `config/vocabularies.yml`. Internal representative examples are permitted only with `placeholder: true` and `public: false`; generation and regression tests exclude them. Internal Gate labels and owner-decision records remain in Git history and governance documents, not visible public pages or public search.
