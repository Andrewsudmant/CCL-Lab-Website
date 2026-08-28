# Gate 5G public metadata display audit

Audit date: 28 August 2026

Machine values remain stable in YAML and filter attributes. Visible Work metadata is rendered through `config/vocabularies.yml` with semicolon-separated labels.

| Vocabulary | Machine value | Public label | Principal pages affected |
|---|---|---|---|
| Geography | `canada` | Canada | Work landing/detail pages |
| Geography | `global` | Global | Work landing/detail pages |
| Geography | `united-kingdom` | United Kingdom | Work landing/detail pages |
| Geography | `british-columbia` | British Columbia | Records using the value |
| Geography | `sub-saharan-africa` | Sub-Saharan Africa | Publication/Work metadata where present |
| Governance scale | `federal-national` | Federal or national | Work detail pages |
| Governance scale | `provincial-territorial` | Provincial or territorial | Work detail pages |
| Method | `comparative-case-study` | Comparative case study | Work detail pages |
| Method | `institutional-analysis` | Institutional analysis | Work detail pages |
| Method | `place-based-modelling` | Place-based modelling | Work detail pages |
| Method | `distributional-analysis` | Distributional analysis | Work detail pages |
| Method | `data-visualization` | Data visualization | Work detail pages |
| Sector | `urban-infrastructure` | Urban infrastructure | Work detail pages |
| Sector | `cross-sectoral` | Cross-sectoral | Work detail pages |
| Sector | `labour-workforce` | Labour and workforce | Work detail pages |
| Climate domain | `just-transition` | Just transition | Work detail pages |
| Climate domain | `evidence-and-learning` | Evidence and learning | Work detail pages |
| Metadata source | `crossref` | Crossref | Publication detail pages |
| Metadata source | `datacite` | DataCite | Publication detail pages |
| Metadata source | `institutional-repository` | Institutional repository | Publication detail pages |
| Metadata source | `publisher` | Publisher | Publication detail pages |

No ambiguous controlled value was withheld. Regression tests reject the principal raw slugs in visible page text while preserving them in `data-*` attributes for filtering.
