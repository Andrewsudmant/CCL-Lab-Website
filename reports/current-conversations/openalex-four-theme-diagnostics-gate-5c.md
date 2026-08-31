# OpenAlex four-theme no-key diagnostics — Gate 5C

Run date: 2026-08-26

Credential use: none

Scope: up to two provider-native results for every active academic query, using a 365-day diagnostic lookback. The production query pack retains its 30-day bound.

| Query | Type | Theme intent | Results | Obvious false positives | Too narrow? | Old-theme assumption? | Status |
|---|---|---|---:|---:|---|---|---|
| `cc3-a01-geographies` | theme | `geographies-of-climate-learning` | 2 | 0 | not obvious from count | no | pass |
| `cc3-a02-new-evidence` | theme | `where-new-evidence-matters` | 2 | 0 | not obvious from count | no | pass |
| `cc3-a03-delivery` | theme | `modes-of-climate-delivery` | 2 | 0 | not obvious from count | no | pass |
| `cc3-a04-consequences` | theme | `consequences-for-people-and-places` | 2 | 1 | not obvious from count | no | pass |
| `cc3-a05-tools-facet` | facet | `None` | 2 | 0 | not obvious from count | no | pass |
| `cc3-a06-workforce-facet` | facet | `None` | 2 | 2 | not obvious from count | no | pass |
| `cc3-a07-canada-geographies` | theme | `geographies-of-climate-learning` | 2 | 1 | not obvious from count | no | pass |
| `cc3-a08-bc-new-evidence` | theme | `where-new-evidence-matters` | 2 | 2 | not obvious from count | no | pass |
| `cc3-a09-canada-delivery` | theme | `modes-of-climate-delivery` | 2 | 0 | not obvious from count | no | pass |
| `cc3-a10-canada-consequences` | theme | `consequences-for-people-and-places` | 2 | 0 | not obvious from count | no | pass |

This is a connectivity and query-shape diagnostic, not a measure of scientific relevance, completeness or a final calibration set. False-positive notes are conservative heuristics and require human calibration.

## Operator review of this bounded run

The returned titles show that broad OpenAlex full-text ranking can satisfy the multi-term queries through incidental matches. Obvious examples include biomass biorefineries for Theme 2, national-resistance finance for consequences, parental employment for the workforce facet, North Macedonian raw materials for the BC evidence query, and Ethiopian displacement for Canadian delivery. The Canada/geographies and Canada/consequences results also lack an obvious Canadian municipal relationship in their titles. The one clearest plausible hit is the multilevel-governance transportation research-agenda record under Canadian delivery, but even that requires abstract review before classification.

This pattern indicates that most queries are **too broad in provider-native full-text form**, not too narrow. The BC Theme 2 and workforce queries are the clearest calibration priorities. Later no-key work should test structured concept/filter combinations and human-labelled precision without treating result count as success. No returned item was added to fixtures, staging or the public site.

## `cc3-a01-geographies`

- Query: `urban climate evidence geography comparison transfer conditions generalisability`
- Actual provider parameters: `{"filter": "from_publication_date:2025-08-26,type:article|preprint,language:en", "mailto": "andrew_sudmant@sfu.ca", "per-page": 2, "search": "urban climate evidence geography comparison transfer conditions generalisability", "select": "id,doi,title,display_name,publication_date,authorships,primary_location,locations,abstract_inverted_index,cited_by_api_url", "sort": "publication_date:desc"}`
- Result count: 2
- Query errors: none
- Obvious false positives by conservative token-overlap check: 0
- Obvious reason for zero results: none
- Appears too narrow: not obvious from count
- Appears to reproduce an old-theme assumption: no
- Returned records:
- `W7203972937` — Latent paths in mode choice models: incorporating street-level environment features for active travel policy
- `W7116892630` — Local data matters: Improving biodiversity risk and impact assessment through a data quality focus

## `cc3-a02-new-evidence`

- Query: `urban climate consequential uncertainty value of additional information evaluation priorities municipal decision`
- Actual provider parameters: `{"filter": "from_publication_date:2025-08-26,type:article|preprint,language:en", "mailto": "andrew_sudmant@sfu.ca", "per-page": 2, "search": "urban climate consequential uncertainty value of additional information evaluation priorities municipal decision", "select": "id,doi,title,display_name,publication_date,authorships,primary_location,locations,abstract_inverted_index,cited_by_api_url", "sort": "publication_date:desc"}`
- Result count: 2
- Query errors: none
- Obvious false positives by conservative token-overlap check: 0
- Obvious reason for zero results: none
- Appears too narrow: not obvious from count
- Appears to reproduce an old-theme assumption: no
- Returned records:
- `W7203970402` — Cascaded biorefineries for agro-industrial biomass residues: Sustainable waste-to-value engineering
- `W7203663386` — Addressing the governance dilemma of urban low value waste under misalignment

## `cc3-a03-delivery`

- Query: `urban climate authority finance coordination capacity participation implementation maintenance institutional configurations`
- Actual provider parameters: `{"filter": "from_publication_date:2025-08-26,type:article|preprint,language:en", "mailto": "andrew_sudmant@sfu.ca", "per-page": 2, "search": "urban climate authority finance coordination capacity participation implementation maintenance institutional configurations", "select": "id,doi,title,display_name,publication_date,authorships,primary_location,locations,abstract_inverted_index,cited_by_api_url", "sort": "publication_date:desc"}`
- Result count: 2
- Query errors: none
- Obvious false positives by conservative token-overlap check: 0
- Obvious reason for zero results: none
- Appears too narrow: not obvious from count
- Appears to reproduce an old-theme assumption: no
- Returned records:
- `W4413114706` — Insights into the development and key factors of five European governance innovations for forest ecosystem service provision
- `W7128495702` — Spatial governance under polycrisis: Reconfiguring agglomeration policy

## `cc3-a04-consequences`

- Query: `urban climate action health equity affordability employment burdens adverse outcomes distributional consequences`
- Actual provider parameters: `{"filter": "from_publication_date:2025-08-26,type:article|preprint,language:en", "mailto": "andrew_sudmant@sfu.ca", "per-page": 2, "search": "urban climate action health equity affordability employment burdens adverse outcomes distributional consequences", "select": "id,doi,title,display_name,publication_date,authorships,primary_location,locations,abstract_inverted_index,cited_by_api_url", "sort": "publication_date:desc"}`
- Result count: 2
- Query errors: none
- Obvious false positives by conservative token-overlap check: 1 — FUNDING AND LOGISTICAL SUPPORT FOR THE NATIONAL RESISTANCE IN THE CONTEXT OF IMPLEMENTING THE CONCEPT OF MODERN FINANCE
- Obvious reason for zero results: none
- Appears too narrow: not obvious from count
- Appears to reproduce an old-theme assumption: no
- Returned records:
- `W7203990650` — Urban futures under geopolitical instability: Aligning sustainability and SDGs in the age of global megatrends
- `W7203945108` — FUNDING AND LOGISTICAL SUPPORT FOR THE NATIONAL RESISTANCE IN THE CONTEXT OF IMPLEMENTING THE CONCEPT OF MODERN FINANCE

## `cc3-a05-tools-facet`

- Query: `urban climate dataset model dashboard decision support tool methodology`
- Actual provider parameters: `{"filter": "from_publication_date:2025-08-26,type:article|preprint,language:en", "mailto": "andrew_sudmant@sfu.ca", "per-page": 2, "search": "urban climate dataset model dashboard decision support tool methodology", "select": "id,doi,title,display_name,publication_date,authorships,primary_location,locations,abstract_inverted_index,cited_by_api_url", "sort": "publication_date:desc"}`
- Result count: 2
- Query errors: none
- Obvious false positives by conservative token-overlap check: 0
- Obvious reason for zero results: none
- Appears too narrow: not obvious from count
- Appears to reproduce an old-theme assumption: no
- Returned records:
- `W7203858773` — Climate Decision AI: Transforming Environmental Impact Assessments Through Pre-Emptive Predictive Analytics
- `W7203862818` — Pond diversity in the hands of the community: eDNA metabarcoding meets participatory science in the GenePools project

## `cc3-a06-workforce-facet`

- Query: `urban climate transition workforce occupations skills institutions evidence needs`
- Actual provider parameters: `{"filter": "from_publication_date:2025-08-26,type:article|preprint,language:en", "mailto": "andrew_sudmant@sfu.ca", "per-page": 2, "search": "urban climate transition workforce occupations skills institutions evidence needs", "select": "id,doi,title,display_name,publication_date,authorships,primary_location,locations,abstract_inverted_index,cited_by_api_url", "sort": "publication_date:desc"}`
- Result count: 2
- Query errors: none
- Obvious false positives by conservative token-overlap check: 2 — Mass Worker Education: Governing from the Shop Floor; Parental employment status and preschoolers' emotional and behavioral problems in Western China: a cross-sectional study
- Obvious reason for zero results: none
- Appears too narrow: not obvious from count
- Appears to reproduce an old-theme assumption: no
- Returned records:
- `W7137501488` — Mass Worker Education: Governing from the Shop Floor
- `W7203736336` — Parental employment status and preschoolers' emotional and behavioral problems in Western China: a cross-sectional study

## `cc3-a07-canada-geographies`

- Query: `Canadian municipal climate evidence transfer comparison contextual relevance`
- Actual provider parameters: `{"filter": "from_publication_date:2025-08-26,type:article|preprint,language:en", "mailto": "andrew_sudmant@sfu.ca", "per-page": 2, "search": "Canadian municipal climate evidence transfer comparison contextual relevance", "select": "id,doi,title,display_name,publication_date,authorships,primary_location,locations,abstract_inverted_index,cited_by_api_url", "sort": "publication_date:desc"}`
- Result count: 2
- Query errors: none
- Obvious false positives by conservative token-overlap check: 1 — Classifying and aligning financial incentives for disaster-resilient housing: a framework from Sri Lanka
- Obvious reason for zero results: none
- Appears too narrow: not obvious from count
- Appears to reproduce an old-theme assumption: no
- Returned records:
- `W7204137518` — Occurrence, fate, monitoring challenges, and bio-based adsorbents for sustainable remediation of emerging contaminants in low- and middle-income countries
- `W7203791827` — Classifying and aligning financial incentives for disaster-resilient housing: a framework from Sri Lanka

## `cc3-a08-bc-new-evidence`

- Query: `British Columbia municipal climate policy evaluation consequential uncertainty research priority`
- Actual provider parameters: `{"filter": "from_publication_date:2025-08-26,type:article|preprint,language:en", "mailto": "andrew_sudmant@sfu.ca", "per-page": 2, "search": "British Columbia municipal climate policy evaluation consequential uncertainty research priority", "select": "id,doi,title,display_name,publication_date,authorships,primary_location,locations,abstract_inverted_index,cited_by_api_url", "sort": "publication_date:desc"}`
- Result count: 2
- Query errors: none
- Obvious false positives by conservative token-overlap check: 2 — Analysis of critical raw materials industry in North Macedonia: Geological endowment, institutional frictions and pathways into European supply chains; GAC-MAC 2026 St. John's Meeting: Abstracts, Volume 49
- Obvious reason for zero results: none
- Appears too narrow: not obvious from count
- Appears to reproduce an old-theme assumption: no
- Returned records:
- `W7202417840` — Analysis of critical raw materials industry in North Macedonia: Geological endowment, institutional frictions and pathways into European supply chains
- `W7167894793` — GAC-MAC 2026 St. John's Meeting: Abstracts, Volume 49

## `cc3-a09-canada-delivery`

- Query: `Canada federal provincial municipal climate authority finance coordination delivery arrangements`
- Actual provider parameters: `{"filter": "from_publication_date:2025-08-26,type:article|preprint,language:en", "mailto": "andrew_sudmant@sfu.ca", "per-page": 2, "search": "Canada federal provincial municipal climate authority finance coordination delivery arrangements", "select": "id,doi,title,display_name,publication_date,authorships,primary_location,locations,abstract_inverted_index,cited_by_api_url", "sort": "publication_date:desc"}`
- Result count: 2
- Query errors: none
- Obvious false positives by conservative token-overlap check: 0
- Obvious reason for zero results: none
- Appears too narrow: not obvious from count
- Appears to reproduce an old-theme assumption: no
- Returned records:
- `W7202248191` — Multilevel governance and the decarbonisation of transportation: towards a research agenda
- `W7202127186` — The Northern Ethiopia War and the persistence of internal displacement: subnational evidence from a difference-in-differences analysis

## `cc3-a10-canada-consequences`

- Query: `Canadian municipal climate policy affordability health employment distributional consequences`
- Actual provider parameters: `{"filter": "from_publication_date:2025-08-26,type:article|preprint,language:en", "mailto": "andrew_sudmant@sfu.ca", "per-page": 2, "search": "Canadian municipal climate policy affordability health employment distributional consequences", "select": "id,doi,title,display_name,publication_date,authorships,primary_location,locations,abstract_inverted_index,cited_by_api_url", "sort": "publication_date:desc"}`
- Result count: 2
- Query errors: none
- Obvious false positives by conservative token-overlap check: 0
- Obvious reason for zero results: none
- Appears too narrow: not obvious from count
- Appears to reproduce an old-theme assumption: no
- Returned records:
- `W7203919053` — Unincorporated and Unequal: Housing and Environmental Inequality Among Women Farmworkers in Rural California
- `W7203791827` — Classifying and aligning financial incentives for disaster-resilient housing: a framework from Sri Lanka
