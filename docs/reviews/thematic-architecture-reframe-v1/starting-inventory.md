# Starting repository and information-architecture inventory

Recorded before editing on 2026-08-21.

## Authoritative tree

See `starting-git-state.md`. The existing Gate 5B working tree and complete local history were authoritative; no ZIP reconstruction was used.

## Theme and content configuration

- `config/research_scope.yml`: six-theme registry and search concepts.
- `config/vocabularies.yml`: geography, governance-scale, method, climate-domain, sector and source-type facets.
- `config/query_packs/current-conversations-v1.yml`: provider/query assignments.
- `config/source_registry.yml`: permitted source environments and provider policy.
- `data/projects/*.yml`, `data/publications/*.yml`, `data/people/*.yml`: human-editable canonical records.
- `data/current-conversations/generated/{sources,clusters}/*.json`: captured fixture records.

## Starting routes and navigation

The starting Quarto build rendered the homepage; Research, Projects, People, Outputs, Publications, Data & Tools, Current Conversations, Opportunities, About Andrew and Contact; six pages under `/research/themes/`; six project pages; publication pages; and Current Conversations detail and compatibility routes.

Navigation exposed Research, Projects, People, an Outputs menu, “Conversations,” Opportunities and an About menu. Current Conversations was already the active public feature name.

## Starting homepage

The homepage led with the lab name and the subtitle “Research on how cities generate, transfer and use evidence for climate action,” followed by an organising question about turning evidence into action, six independent research-area cards, featured projects and outputs, Current Conversations, people and SFU contact context. Current Conversations followed research content but the six-theme layout did not show a cumulative learning cycle.

## Starting project schema

Projects already required a stable ID, title, status, lab relationship, summary, research questions, dates, primary/secondary themes, geography, governance scales, methods, climate domains, sectors, collaborators, connected publications, outputs/tools, verification date, authoritative sources and verification status. It did not yet support the optional climate-learning contribution fields added in this work package.

## Starting Current Conversations taxonomy

Clusters required one of six themes as a primary classification and up to two secondary themes. Source environment, role, geography and evidentiary basis were separate. There was no null/unclassified primary-theme state. The accepted fixture/provenance, clustering, publication, correction, review and audit controls were already present and were retained.

## Available commands

- Offline: `make validate`, `make generate`, `make test`, `make build`, `make linkcheck`, `make accessibility`, `make check`.
- Explicit network: `make publications-refresh`, `make current-conversations-discover`, `make openalex-diagnostics`.
- Fixture/private controls: `make current-conversations-fixture`, `make current-conversations-pilot`, `make model-benchmark`, `make calibration-pack`.
- Review packaging: `make owner-review`, `make handoff`.

No material conflict was found between the working tree and the latest Gate 5B owner-review material.
