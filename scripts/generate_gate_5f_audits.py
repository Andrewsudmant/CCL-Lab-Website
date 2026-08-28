#!/usr/bin/env python3
"""Generate deterministic Gate 5F editorial audits from governed records."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

try:
    from .content import ROOT, load_records, research_scope
    from .generate_site import HOME_THEME_PROPOSITIONS, work_title
except ImportError:
    from content import ROOT, load_records, research_scope
    from generate_site import HOME_THEME_PROPOSITIONS, work_title

OUT = ROOT / "docs/reviews/gate-5f"


def write(name: str, text: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(text.rstrip() + "\n", encoding="utf-8")


def esc_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def main() -> int:
    themes = research_scope()["themes"]
    ideas = load_records("data/research-ideas")
    works = load_records("data/work")
    publications = json.loads((ROOT / "reports/content/publication-complete-inventory.json").read_text())["records"]
    publications_by_id = {item["record_id"]: item for item in publications}

    home_rows = "\n".join(
        f"| {i} | {t['name']} | {HOME_THEME_PROPOSITIONS[t['id']]} |"
        for i, t in enumerate(themes, 1)
    )
    write("homepage-reader-value-audit.md", f"""# Homepage reader-value audit

Former site-level proposition: “How cities find, generate and use evidence for climate action.” It remains as the secondary tagline.

New principal claim: **Urban climate evidence does not become useful merely because it exists.**

Readers: urban climate researchers; municipal, regional and national policy practitioners; policy intermediaries, city networks and research organisations; prospective students and research collaborators.

Instability: a precedent, gap, policy label or aggregate benefit does not establish relevance, value, deliverability or distribution. Treating the four judgements separately can make evidence appear more transferable, gaps more valuable, policies more implementable and benefits more evenly shared than they are.

Hierarchy: affiliation → lab name → secondary tagline → principal claim → concise explanation → four connected questions → reader pathways → Featured Work → context → Current Conversations.

| Stage | Theme | Homepage proposition |
|---:|---|---|
{home_rows}
""")

    theme_rows = "\n".join(
        f"| {t['name']} | guiding question; two-paragraph description; analytical boundary; what_this_changes; cycle_role; connection_to_next; included questions | Questions the lab investigates; top cycle-role label | What this changes → The proposition; Analytical boundary → What this theme does not assume | after description | restrained paragraph after proposition | How this connects, after ideas |"
        for t in themes
    )
    write("theme-public-scaffolding-audit.md", f"""# Theme public-scaffolding audit

All structured Gate 5E fields remain in `config/research_scope.yml`; only public arrangement and labels changed.

| Theme | Structured fields retained | Public labels removed | Labels renamed | Proposition | Boundary | Cycle connection |
|---|---|---|---|---|---|---|
{theme_rows}
""")

    idea_rows = []
    for item in sorted(ideas, key=lambda x: (x["theme_id"], x["display_order"])):
        why = f"{item['problem_of_understanding']} {item['why_it_may_matter']}"
        idea_rows.append(
            f"| `{item['idea_id']}` | {item['narrative_tier']} | {esc_cell(why)} | {esc_cell(item['possible_research_design'])} | {esc_cell(', '.join(item['public_method_tags']))} | {len(item['suggested_methods'])} retained | {esc_cell(item.get('reader_or_decision_at_stake') or 'blank — owner review')} | yes |"
        )
    write("research-idea-display-audit.md", """# Research-idea display audit

Signature status is reading hierarchy only, not priority, funding readiness or importance. Questions, problems, consequences, possible designs and complete method lists are unchanged from Gate 5E.

| ID | Tier | Public “why this question matters” | Displayed design | Public method tags | Full list | Reader or decision at stake | Substance unchanged |
|---|---|---|---|---|---|---|---|
""" + "\n".join(idea_rows))

    work_rows = []
    for item in works:
        basis = "; ".join(source["label"] for source in item["authoritative_sources"])
        language = "prospective" if item["work_status"] == "ongoing" else "established/source-backed"
        omitted = "Publications, outputs and tools" if not item["connected_publication_ids"] and not item["connected_work_ids"] else "none"
        work_rows.append(
            f"| `{item['work_id']}` | {esc_cell(item['problem_of_understanding'])} | {esc_cell(item['central_question'])} | {esc_cell(item['how_it_investigates'])} | {esc_cell(item['reader_value'])} | {esc_cell(item['evidence_status'])} | {esc_cell(item['claim_boundaries'])} | {esc_cell(basis)} ({language}) | {omitted} |"
        )
    write("work-page-reader-value-audit.md", """# Work-page reader-value audit

Public pages lead with reader-facing arguments. Ongoing records use prospective language; completed records distinguish source-backed contribution from impact. Unsupported output sections are omitted.

| Work | Problem | Central question | Approach | Reader value | Evidence status | Boundary | Source basis and wording | Omitted |
|---|---|---|---|---|---|---|---|---|
""" + "\n".join(work_rows))

    write("our-approach-and-illustration-audit.md", """# Our Approach and illustration audit

- Exactly six breakdown states connect evidence visibility, relevance, new-evidence choice, interpretation and delivery, distributed consequences, and later revision.
- The states describe where the existing four-theme cycle can break down; they do not create a competing framework.
- The active-travel illustration is visibly labelled hypothetical and is not a finding or policy recommendation.
- The illustration makes no fixed outcome claim, transferability score, city ranking, assessment tool or recommendation.
- Existing commitments on context, evidence status, failures, multiple knowledge forms, authority, justice and non-universal best practice remain.
""")

    write("current-conversations-reader-problem-audit.md", """# Current Conversations reader-problem audit

- The opening now identifies fragmented discussion and difficulty tracing framing and underlying sources before describing the proposed feature.
- Public status remains **In development** and the live feed remains disabled.
- Public pages contain no fixture cards, entries, counts, filters, feeds, timestamps or demonstration summaries.
- Inclusion remains non-endorsement and does not establish evidence quality or applicability.
- Generation, build and tests make no Current Conversations discovery, API or paid-model call.
""")

    fixture = yaml.safe_load((ROOT / "tests/fixtures/gate-5d-previous-work-freeze.yml").read_text())
    proposal_rows = []
    works_by_id = {item["work_id"]: item for item in works}
    group = {
        "geographies-of-climate-learning": "comparison, evidence boundaries and scaling",
        "where-new-evidence-matters": "consequential gaps and unresolved disagreement",
        "modes-of-climate-delivery": "authority, finance, coordination and institutional durability",
        "consequences-for-people-and-places": "distribution, appraisal boundaries and place-based effects",
    }
    for theme_id, selected in fixture["selected_previous_work"].items():
        for canonical in selected:
            kind, record_id = canonical.split("/", 1)
            if kind == "work":
                record = works_by_id[record_id]
                rationale = record["summary"]
                verification = record["evidence_status"]
                evidence = "; ".join((source.get("url") or source["label"]) for source in record["authoritative_sources"])
                title = work_title(record, publications_by_id)
            else:
                record = publications_by_id[record_id]
                rel = next(rel for rel in record["theme_relationships"] if rel["theme_id"] == theme_id)
                rationale = rel["rationale"]
                verification = f"Verified relationship based on {rel['evidence_source']}"
                evidence = rel["evidence_source"]
                title = record["title"]
            proposal = f"Later copy could state how “{title}” helps readers examine {group[theme_id]}, while preserving the existing evidence boundary and relationship to the lab."
            proposal_rows.append(f"| {themes[[t['id'] for t in themes].index(theme_id)]['name']} | `{canonical}` | {esc_cell(rationale)} | {esc_cell(verification)} | {esc_cell(proposal)} | {group[theme_id]} | retain pending owner curation | {esc_cell(evidence)} |")
    write("previous-work-reader-value-proposal.md", """# Previous-work reader-value proposal — not implemented

**Private Gate 5F proposal.** No wording in this report is published. Selection, display order, theme assignment, relationship-to-lab classification and public rationale remain frozen for the separate owner curation gate.

| Theme | Canonical ID | Current public rationale | Current verification wording | Proposed later conceptual contribution | Suggested grouping | Recommendation | Evidence |
|---|---|---|---|---|---|---|---|
""" + "\n".join(proposal_rows))
    print(f"Generated Gate 5F audits in {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
