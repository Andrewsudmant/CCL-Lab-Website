# Route and copy inventory

## Canonical routes

- `/research/geographies-of-climate-learning.html`
- `/research/where-new-evidence-matters.html`
- `/research/modes-of-climate-delivery.html`
- `/research/consequences-for-people-and-places.html`
- `/research/our-approach.html`

## Preserved former routes

Static Quarto output cannot issue server-side redirects. Six former routes under `/research/themes/` remain as accessible transition pages with canonical metadata and a direct link to a new theme page. The co-benefits and just-transitions routes both lead to Consequences for People and Places; the former Canadian-policy route leads to Modes of Climate Delivery while retaining Canada as a geography/topic facet. All active internal links use new routes.

The `/research-watch/` compatibility routes remain intentionally as naming-transition pages to Current Conversations. They do not restore Research Watch as the active feature name.

## Controlling copy locations

| Copy | Authoritative location |
|---|---|
| Theme titles, questions, descriptions, cycle roles and boundaries | `config/research_scope.yml` |
| Homepage proposition and programme sequence | `index.qmd` plus generated `home-themes.qmd` |
| Approach commitments | `research/our-approach.qmd` |
| Project learning contribution | `data/projects/*.yml`, rendered by `scripts/generate_site.py` |
| Current Conversations descriptor and disclosure | `current-conversations/index.qmd` |
| Classification instructions | `prompts/current-conversations-classification-v1.md` |

Generated theme pages and record listings must not be edited by hand.
