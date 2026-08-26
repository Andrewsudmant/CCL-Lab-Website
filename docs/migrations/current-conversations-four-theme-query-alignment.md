# Current Conversations four-theme query alignment

Migration date: 26 August 2026  
Active pack: `current-conversations-v2@3.0.0`  
Superseded pack retained: `current-conversations-v1@2.0.0`

The earlier file is preserved unchanged as decision evidence. Runtime discovery and validation now select v2 explicitly. No historical candidate, source or cluster identifier was rewritten.

## Design change

- `theme` became `theme_intent`; it records discovery intent, not a final assignment.
- `query_type` distinguishes `theme`, `facet` and `exploratory` searches.
- `candidate_themes` bounds possible analytical relationships without forcing them.
- `facets` records geographies, sectors, methods and climate domains independently.
- `classification_required: true` applies to every query.
- Facet and exploratory queries require `theme_intent: null`.
- Theme 2 queries must contain a consequential uncertainty, value-of-information, evaluation-priority or decision-change concept.
- Null final classification remains valid.

## Former-query migration

| Former query IDs | Former hard-coded theme | New structure | Type | Compatibility treatment | Reason |
|---|---|---|---|---|---|
| `cc-a01-learning`, `cc-w01-learning`, `cc-c01-learning`, `cc-b01-learning` | Geographies of Climate Learning | `cc3-*-01-geographies` | Theme for academic/web/commentary; exploratory for Bluesky | Former pack retained; equivalent analytical intent has new IDs | Focus comparison and transfer on evidence-learning rather than generic networks or diffusion. |
| `cc-a02-governance`, `cc-w02-governance`, `cc-c02-governance`, `cc-b02-governance` | Modes of Climate Delivery | `cc3-*-03-delivery` | Theme for academic/web/commentary; exploratory for Bluesky | New IDs; runtime reads v2 | Require authority, finance, coordination, capacity, participation or maintenance rather than generic implementation. |
| `cc-a03-cobenefits`, `cc-w03-cobenefits`, `cc-c03-cobenefits`, `cc-b03-cobenefits` | Consequences for People and Places | `cc3-*-04-consequences` | Theme for academic/web/commentary; exploratory for Bluesky | New IDs; old source records keep old discovery IDs | Broaden from promotional co-benefit language to benefits, burdens, affordability, adverse effects and distribution. |
| `cc-a04-workforce`, `cc-w04-workforce`, `cc-c04-workforce`, `cc-b04-workforce` | Consequences for People and Places | `cc3-a06-workforce-facet`, `cc3-w06-workforce-facet`, `cc3-c06-workforce-facet`; Bluesky coverage remains exploratory | Facet or exploratory | No forced theme; all results require classification | Workforce can concern future evidence, delivery institutions or consequences. Sector does not determine theme. |
| `cc-a05-tools`, `cc-w05-tools`, `cc-c05-tools`, `cc-b05-tools` | Where New Evidence Matters | `cc3-*-05-tools-facet` | Facet | `theme_intent: null`; all four themes are candidates | A dataset, model, tool or dashboard does not itself establish a consequential evidence priority. |
| `cc-a06-canada`, `cc-w06-canada`, `cc-c06-canada`, `cc-b06-canada` | Modes of Climate Delivery | Canada/BC variants for each analytical question plus `cc3-b06-canada-facet` | Theme variants or facet | Location is stored in `facets.geographies`; no generic Canada-to-Theme-3 rule | Canada and British Columbia are geographies, not analytical contributions. |

## New Theme 2 coverage

The old pack had no query centred on prospective evidence value. v2 adds `cc3-a02-new-evidence`, `cc3-w02-new-evidence` and `cc3-c02-new-evidence`, plus a cautious exploratory Bluesky query. It also adds the British Columbia variants `cc3-a08-bc-new-evidence` and `cc3-w08-bc-new-evidence`. Each query names consequential uncertainty, evaluation priority, value of new information or evidence that could change a decision.

## Canada and British Columbia variants

The active academic and web groups each contain:

- evidence comparison and contextual relevance in Canadian cities;
- consequential evaluation uncertainty in British Columbia;
- federal–provincial–municipal delivery arrangements; and
- distributional consequences of Canadian municipal climate policy.

This structure supports geographical filtering without presuming a theme from location.

## Traceability and limitations

Historical v1 query IDs remain in old records and reports. They are not interpreted retroactively. Live records created by v2 will store their new query ID and version. The query pack improves search intent; it does not establish scientific relevance, completeness, evidential quality, transferability or endorsement.
