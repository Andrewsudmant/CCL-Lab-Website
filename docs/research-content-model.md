# Research content data dictionary

## Research themes

Source: `config/research_scope.yml`; schema: `schemas/research-theme.schema.json`.

Themes define the current intellectual programme. Required public fields are the exact ID/title, homepage description, guiding question, two-paragraph long description, analytical boundary, cycle role and connection to the next stage. Search concepts, included questions, exclusions, geographical priorities, methodological interests and clearly marked placeholder examples support governance and discovery. Active theme records have no status or maturity field.

## Research work

Source: `data/work/*.yml`; schema: `schemas/research-work.schema.json`.

- `work_id`: stable public identity and route key.
- `title`: display title; may be `null` only for a paper/report with exactly one connected publication, from which it is derived.
- `work_type`: `research-programme`, `research-line`, `project`, `study`, `paper`, `report`, `tool` or `dataset`.
- `work_status`: `ongoing` or `completed`.
- `relationship_to_lab`: `current-ccll-work`, `pre-ccll-work-continuing`, `foundational-prior-work` or `associated-collaboration`.
- `parent_work_id`: optional; standalone work validates with `null`.
- `connected_work_ids`, `connected_publication_ids`, `connected_tool_ids`: validated graph links. Bibliographic facts stay in publications.
- Theme/facet fields: one primary theme, optional secondary themes, geographies, governance scales, methods, sectors and climate domains.
- Evidence fields: summary, questions, evidence status, claim boundaries, authoritative sources, verification status/date and optional analytical contribution fields.
- `featured`: homepage selection control; it does not change status or provenance.

Funders, partners, dates, deliverables and findings are not required merely to complete a work template.

## Publications and outputs

Sources: selected YAML plus the generated complete JSON inventory; schema: `schemas/publication.schema.json`.

Bibliographic identity, authors, dates, identifiers, venue and verification sources are canonical. `connected_work_ids` links only genuine relationships and may be empty. `theme_relationships` records a primary/secondary analytical relationship, a concise rationale and the authoritative evidence source reviewed. One publication may appear under several themes without duplication.

## Research ideas

Source: `data/research-ideas/*.yml`; schema: `schemas/research-idea.schema.json`.

Each idea has a stable ID, one theme, a question, why it may matter, at least one suggested method, optional settings/facets, display order, owner-review state and the exact disclaimer `Research idea · not currently an active or funded project`. Idea records have no work status, parent, funder, partner, date, output or publication field.
