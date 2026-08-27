# Gate 5D standalone-publications audit

Audit date: 27 August 2026

## Artificial parent relationships removed

| Publication | Former relationship | Gate 5D treatment | Reason |
|---|---|---|---|
| `who-can-learn-geography-urban-climate-evidence` | Attached to project-like `geography-urban-climate-evidence` | Represented as an ongoing paper work record with `parent_work_id: null`; title and bibliographic facts derive from the canonical publication | The verified research object is the paper; no broader programme is evidenced or invented. |
| `replicate-generalize-urban-research` | Attached to `geography-urban-climate-evidence` | Standalone canonical publication directly related to Geographies and New Evidence; no parent work | The relationship was thematic, not evidence of a shared bounded project. |

## Genuine work relationships retained or added

| Publication | Work | Treatment |
|---|---|---|
| `data-scaling-climate-action-governance-uk` | `data-methodologies-climate-impact` | Retained: authoritative University of Edinburgh project record supports the connection. |
| `designing-visualization-atlas-uk-cobenefits` | `uk-co-benefits-atlas` | Retained: the paper explicitly concerns the Atlas project. |
| `from-urban-climate-ambition-to-delivery` | `climate-delivery-modes` | Added: verified publisher record and owner decision identify it as foundational to the ongoing programme. |

All other complete-inventory publications may remain standalone. They can connect directly to themes through evidence-backed `theme_relationships` and do not need project or programme wrappers.

## Duplicate and ambiguity check

- Canonical complete records: 46.
- Duplicate DOI records after normalization: 0.
- Geography preprint exists once as a publication; its work page derives bibliographic identity rather than copying it.
- Atlas project and Atlas tool are distinct work records linked to one another; this is not a duplicate because completion and public availability describe different objects.
- The delivery programme and delivery paper are distinct and explicitly linked.
- Ten ORCID-only groups remain withheld from the public inventory because authoritative metadata is insufficient; no theme or parent relationship was guessed.

## Changes made

`connected_projects` became `connected_work_ids`. The active work schema allows `parent_work_id: null`. Generated theme pages deduplicate a publication when a connected work record already represents it in that theme. Combined Work and publication listings continue to use one canonical ID per record type.
