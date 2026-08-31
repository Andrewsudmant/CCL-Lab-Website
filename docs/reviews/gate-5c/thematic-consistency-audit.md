# Gate 5C public thematic-consistency audit

Audit date: 26 August 2026  
Decision basis: owner-approved Gate 5C brief; authoritative project sources recorded in canonical YAML; `config/research_scope.yml`.

| Location | Intended theme or facet | Issue found | Change made | Evidence or owner decision | Effect |
|---|---|---|---|---|---|
| Homepage opening | Whole programme | No Gate 5C defect; both the need to share learning and the danger of unchanged transfer were already present. | Retained precise proposition and problem statement. | Owner-approved proposition and hierarchy. | Public copy |
| Homepage theme cycle | Four equal analytical stages | Theme 2 displayed a “Developing” badge, creating intellectual maturity asymmetry. | Removed all maturity badges; retained internal `portfolio_maturity`. | Owner Gate 5C §4. | Public copy; metadata |
| Homepage featured work | Cycle illustration | Selection had not yet been confirmed in governance evidence. | Confirmed Geography, Climate delivery modes and CoBen in that order; added Atlas as prominent foundational prior work. | Owner Gate 5C §7. | Public copy |
| Research overview | Whole programme and separate facets | Public maturity badge inherited from generator. | Removed badge; retained one registry and explicit facet section. | Owner Gate 5C §§3–4. | Public copy |
| Our approach | Learning states | No residual six-topic structure found. | Retained evidence → relevance → use → delivery → consequences → later learning sequence. | Existing owner-approved reframe. | Public copy |
| Geographies theme | Theme 1 | Data Methodologies was absent as a core project; tool fixtures occupied Theme 2. | Data Methodologies moved to Theme 1; evidence-access/comparison fixtures moved here only where source evidence supports it. | Owner mapping and Theme 1 boundary. | Public copy; metadata |
| New Evidence theme | Theme 2 | Residual core Data Methodologies and multiple tool/model fixtures made Theme 2 a residual tools category. | Removed those assignments. No fixture is forced into Theme 2 without consequential prospective evidence. | Owner Theme 2 test. | Public copy; metadata |
| Delivery theme | Theme 3 | UK Atlas was related merely because it is policy-facing. | Removed Atlas Theme 3 assignment; retained configuration language for delivery work. | Owner mapping and delivery-mode boundary. | Public copy; metadata |
| Consequences theme | Theme 4 | Austin tree-canopy fixture treated AI/tool use as Theme 2. | Reclassified the fixture to consequences based on heat/shade distribution; retained burdens, risks and adverse outcomes language. | Evidence in captured source description; owner boundary. | Public copy; metadata |
| Project pages | Canonical project mappings | Data Methodologies and Atlas mappings were inconsistent; two Atlas learning fields lacked an authoritative basis. | Applied six approved mappings; removed inferred Atlas consequential-uncertainty and next-learning fields. | Owner Gate 5C §§5–6. | Public copy; YAML |
| Publications and Outputs | Theme-linked lab outputs | No active six-theme heading found; “Verified publications and outputs” already replaced the incomplete title. | Retained authoritative metadata and lab/prior-work distinctions. | Existing verified inventory. | Public copy |
| Current Conversations landing | Horizon scanning | Disclosure was already provenance-dependent; classifications still reflected old tools assumptions. | Kept exact adjacent disclosure; regenerated fixtures with evidence-based or null classifications. | Owner Gate 5C §§10–12. | Public copy; fixtures |
| Current Conversations detail pages | External-source classification | Tool type could imply Theme 2 in tags and relevance wording. | Removed forced classifications; disclosure still follows `ai_provenance.used`. | Owner boundary; source evidence. | Public copy; metadata |
| Methods/disclosure page | Governance | Query intent/facet distinction not documented. | Added explicit four-theme, facet and null-classification rules to prompt, architecture and governance docs. | Owner Gate 5C §§11–12. | Public methods; internal governance |
| Filters and generated feeds | Themes plus facets | Theme filter was correct; generated records inherited old fixture assignments. | Regenerated feed and pages from corrected fixtures; unclassified state remains visible. | Canonical registry and fixture evidence. | Public generated content |
| Navigation and page metadata | Current routes | No former theme in principal navigation; transition pages remain searchable route artifacts. | Retained current routes and canonical transition links. | Owner Gate 5C §15. | Public navigation; metadata |
| Schemas | Internal controls | `status` implied theme intellectual status; query schema forced a theme. | Renamed to `portfolio_maturity`; added theme/facet/exploratory query types, nullable intent and mandatory classification. | Owner Gate 5C §§4 and 11. | Internal governance |
| Active prompt | Classification | Theme 1/Theme 2 distinction and facet rules were incomplete. | Added exact analytical tests, non-examples, null validity and non-endorsement boundaries. | Owner Gate 5C §12. | Internal governance |
| Active query pack | Discovery | Tools → Theme 2, Canada → Theme 3 and workforce → Theme 4 were hard-coded. | Added `current-conversations-v2@3.0.0`; preserved v1 and recorded migration. | Owner Gate 5C §11. | Internal governance |

## Residual-assumption tests

| Former assumption | Result |
|---|---|
| Evidence infrastructure as a top-level theme | Absent from current navigation, registry and active route labels. Historical migration/ADR evidence retained. |
| Just transitions as a top-level theme | Absent; workforce and just transition remain facets. |
| Canadian climate policy as a top-level theme | Absent; Canada and British Columbia remain geographies. A lower-case descriptive phrase in an external fixture is not a theme label. |
| Data and tools treated as Theme 2 | Removed from active query intent and corrected in fixtures; generic tools use null intent/classification. |
| Canada treated as Theme 3 | Removed; Canadian and BC variants cover all four analytical questions. |
| Workforce automatically treated as Theme 4 | Removed; workforce queries are facets with Theme 2, 3 and 4 candidates and mandatory classification. |

Historical ADRs, earlier gate reports, v1 query configuration and transition-route slugs remain unchanged where they document past decisions. They are not active public themes.
