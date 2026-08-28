# ADR 0007: Curated previous work and the Draft 0.1 release boundary

- Status: accepted
- Date: 2026-08-28

## Context

Theme pages need enough completed and foundational work to make each research problem concrete, but the earlier automatic lists had become audit-like bibliographies. At the same time, the site must retain a complete verified record and must be reviewable at both a domain root and the provisional GitHub Pages project path.

## Decision

1. Theme pages show four to six illustrative examples selected for substantive fit, explanatory value, representativeness and non-redundancy. `config/theme_featured_examples.yml` stores display order, theme-specific conceptual contribution, qualification and evidence reviewed.
2. `config/publication_theme_examples.yml`, canonical Work records and the 46-record publication inventory continue to store underlying relationships and provenance. Removing an item from prominent display does not reclassify or delete it.
3. Public cards state what a work helps a reader understand. Source-verification wording, exact evidence, selection reasoning and uncertainty stay in controlled records and audits rather than public copy.
4. Current Conversations does not block Draft 0.1 because its public state is truthfully and consistently “In development” and no feed content is generated.
5. Quarto’s `website.site-path` is the deployment abstraction. The normal profile targets a root; `_quarto-project-path.yml` targets `/CCL-Lab-Website/`. No future custom domain is hardcoded.
6. Deployment remains a separate owner action. The prepared workflow has only `workflow_dispatch`, requires a confirmation input and `PUBLIC_DRAFT_DEPLOY_ENABLED=true`, and gates deployment through the protected `public-draft` environment.

## Consequences

Readers receive shorter, conceptually useful theme pages; the verified bibliography remains comprehensive; cross-listed work can carry different theme-specific explanations without duplicate canonical records. Release testing must cover both profiles. Internal governance remains auditable in Git but absent from public search and visible page copy. A merge alone cannot deploy the site.
