# Gate 5D research-work architecture audit

Audit date: 27 August 2026

## Result

The public and active semantic model is **Work**, not Projects. `data/work/` and `schemas/research-work.schema.json` are the active inputs. The canonical listing is `/work.html`; `projects.qmd` and generated `/projects/<id>.html` files are transition pages only and declare `/work/` canonical URLs.

## Required distinctions

| Concept | Active representation | Status behaviour | Publication behaviour |
|---|---|---|---|
| Theme | Four records in `config/research_scope.yml` | No status or maturity fields | May connect to publications through evidence-backed rationales |
| Research work | Seven records in `data/work/` | `ongoing` or `completed` | May connect to zero or more canonical publications; parent is optional |
| Publication/output | Ten selected YAML records plus 46-record complete inventory | Bibliographic publication status only | One canonical record; may remain standalone |
| Research idea | Thirteen records in `data/research-ideas/` | Draft/approved/withheld owner-review state only | Cannot link into publication, Work or Current Conversations listings |

## Six-record migration result

- Geography: ongoing standalone paper, `parent_work_id: null`, pre-CCLL work continuing.
- Data Methodologies: completed foundational project.
- Climate delivery modes: ongoing current CCLL research programme connected to the verified 2026 paper.
- CoBen: ongoing current CCLL research programme with conditional-scenario boundaries retained.
- Occupational transitions: ongoing current CCLL research line. A research line was chosen because the verified scope is a recurring methodological agenda without evidence of bounded dates, funder or deliverables.
- UK Co-Benefits Atlas: completed foundational project plus separately linked active public tool.

## Integrity controls

Validation rejects unknown work/publication/tool links, self-links, duplicate IDs, non-tool `connected_tool_ids`, unsupported work types/statuses/relationships, and non-paper/report records with derived titles. A paper/report with `title: null` must have exactly one connected publication. Work does not require funders, partners or dates. Generated detail pages omit empty connected-publication sections instead of printing database failure messages.

No Current Conversations schema, query rule, cluster identity or feed source was incorporated into research work. No external conversation item can become lab work through generation.
