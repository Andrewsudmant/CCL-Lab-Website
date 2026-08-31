# Gate 5D migration: project-only records to research work

Migration date: 27 August 2026  
Canonical listing: `/work/`  
Former route treatment: every `/projects/<id>.html` page is an accessible transition with `canonical-url` pointing to `/work/<id>.html`; `/projects.html` points to `/work.html`. No second listing is generated.

| Former project ID | Former public type | New work type | Work status | Relationship to lab | Retained ID | Publication relationships | Reason |
|---|---|---|---|---|---|---|---|
| `geography-urban-climate-evidence` | Project | Paper | Ongoing | Work begun before CCLL and continuing | Yes | `who-can-learn-geography-urban-climate-evidence`; no parent work | The verified preprint is the research object. No authoritative broader programme was created merely to supply a parent. |
| `data-methodologies-climate-impact` | Project | Project | Completed | Foundational prior work | Yes | `data-scaling-climate-action-governance-uk` | The University of Edinburgh record supports a bounded completed project and its connected publication. |
| `climate-delivery-modes` | Project | Research programme | Ongoing | Current CCLL work | Yes | `from-urban-climate-ambition-to-delivery` | The work is a continuing comparative programme rather than one bounded project. |
| `coben-place-based-model` | Project | Research programme | Ongoing | Current CCLL work | Yes | None currently verified | The owner-approved work comprises an ongoing modelling and appraisal programme with explicit scenario boundaries. |
| `occupational-transition-requirements` | Project | Research line | Ongoing | Current CCLL work | Yes | None currently verified | The verified scope is a recurring methodological line, not a time-bounded funded project; no individual outcome is predicted. |
| `uk-co-benefits-atlas` | Project | Project | Completed | Foundational prior work | Yes | `designing-visualization-atlas-uk-cobenefits` | The development project is complete and predates CCLL; it was not produced at SFU. |

The live Atlas is represented separately as `uk-co-benefits-atlas-tool`, an ongoing `tool` record whose parent is the completed Atlas project. This preserves the distinction between project completion and continued public tool availability.

## Compatibility and integrity

- `data/projects/` and `schemas/project.schema.json` are no longer active inputs.
- Historical ADRs, audits and Git commits retain former project and theme-status evidence unchanged.
- Canonical publication IDs, DOI/URL identity, dates, authorship and correction history were not duplicated or rewritten.
- The old Geography project's title is now derived from its connected canonical publication; `parent_work_id: null` is valid.
