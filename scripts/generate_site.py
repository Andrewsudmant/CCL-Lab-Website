#!/usr/bin/env python3
"""Generate deterministic Quarto fragments and canonical detail/theme pages."""

from __future__ import annotations

import html
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

try:
    from .content import ROOT, load_records, load_yaml, research_scope, theme_index
    from .validate_content import validate_all
except ImportError:
    from content import ROOT, load_records, load_yaml, research_scope, theme_index
    from validate_content import validate_all

OUT = ROOT / "generated"
FULL_DISCLOSURE = "Current Conversations uses automated searches and AI-generated classification, grouping and summaries to identify recent material connected to the lab's research themes. Sources may include academic papers, policy reports, news, blogs, data tools and public posts. Items have not normally been reviewed by a member of the Cities and Climate Learning Lab, and inclusion does not imply endorsement. Coverage is selective and uneven, and summaries may contain errors or omit important context. Please consult the original sources."
FIXTURE_DISCLOSURE = "This captured fixture was assembled without AI generation to test presentation and governance controls. It has not been reviewed by the lab, is not endorsed, and is not evidence of a live retrieval. Consult the original source."
IDEA_DISCLAIMER = "Research idea · not currently an active or funded project"
ENV_LABELS = {
    "academic-research": "Academic research", "policy-and-institutions": "Policy and institutions",
    "news-and-analysis": "News and analysis", "blogs-and-commentary": "Blogs and commentary",
    "data-and-tools": "Data and tools", "bluesky": "Bluesky",
}
ROLE_LABELS = {
    "primary-research": "Original research", "official-policy-source": "Official policy source",
    "official-announcement": "Official announcement", "dataset-or-tool": "Dataset or tool",
    "news-reporting": "Reporting", "independent-analysis": "Independent analysis",
    "research-commentary": "Research commentary", "practitioner-commentary": "Practitioner commentary",
    "public-discussion": "Public discussion",
}
HOME_THEME_PROPOSITIONS = {
    "geographies-of-climate-learning": "Cities often learn from elsewhere. Similarity does not guarantee that the lesson fits.",
    "where-new-evidence-matters": "Not every research gap is worth filling. The useful question is whether new evidence could change a decision.",
    "modes-of-climate-delivery": "A policy is only a starting point. Authority, money, capability and trust determine whether it can be carried through.",
    "consequences-for-people-and-places": "Climate action changes daily life as well as emissions, and its gains and burdens rarely fall evenly.",
}
THEME_PRACTICAL_EXAMPLES = {
    "geographies-of-climate-learning": "A city preparing for more extreme heat might look to Phoenix, Paris or Ahmedabad. The difficult question is not which city looks most similar, but which differences would change the lesson.",
    "where-new-evidence-matters": "A city can always commission another study. The harder question is whether the new evidence would alter its choice or simply add another case to an already crowded field.",
    "modes-of-climate-delivery": "Two cities may adopt the same retrofit policy. In one, a public utility finances and manages the work; in another, individual households must organise it themselves. The policy label is the same, but the form of action is not.",
    "consequences-for-people-and-places": "A transport policy may reduce emissions and improve health while making some journeys more difficult or increasing costs for particular households. Average benefits do not reveal those differences.",
}
THEME_TERM_NOTES = {
    "geographies-of-climate-learning": "Whether a finding is likely to hold beyond the place where it was produced is its <strong>generalisability</strong>. Whether an estimate can be carried to another setting under stated conditions is its <strong>transportability</strong>.",
    "where-new-evidence-matters": "Uncertainty that could change a decision is <strong>consequential uncertainty</strong>. Methods used to judge whether an intervention caused an observed change are called <strong>causal inference</strong>. An estimate of whether resolving uncertainty could improve a decision is the <strong>value of information</strong>. How a policy's costs, benefits and wider effects are assessed is its <strong>appraisal</strong>.",
    "modes-of-climate-delivery": "The way authority, money, capability and responsibility are arranged is a <strong>delivery configuration</strong>.",
    "consequences-for-people-and-places": "How a policy's costs, benefits and wider effects are assessed is its <strong>appraisal</strong>. Wider gains and harms that occur alongside emissions reductions are its <strong>co-benefits and co-costs</strong>.",
}
PUBLIC_METADATA_LABELS = {
    "crossref": "Crossref",
    "datacite": "DataCite",
    "orcid": "ORCID",
    "publisher": "Publisher",
    "institutional-repository": "Institutional repository",
    "institutional-profile": "Institutional profile",
    "owner-verified": "Lab-verified record",
}


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def site_path(path: str) -> str:
    """Return a project-root path; Quarto applies the configured website site-path."""
    return "/" + path.lstrip("/")


def vocabulary_labels(section: str, values: list[str]) -> list[str]:
    vocabulary = load_yaml(ROOT / "config/vocabularies.yml")
    labels_by_value = vocabulary.get(section, {})
    return [labels_by_value.get(value, value.replace("-", " ").capitalize()) for value in values]


def display_list(section: str, values: list[str]) -> str:
    return "; ".join(vocabulary_labels(section, values))


def public_metadata_labels(values: list[str]) -> str:
    return "; ".join(PUBLIC_METADATA_LABELS.get(value, value.replace("-", " ").capitalize()) for value in values)


def write_fragment(name: str, body: str) -> None:
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("<!-- Generated by scripts/generate_site.py; do not edit. -->\n```{=html}\n" + body.rstrip() + "\n```\n", encoding="utf-8")


def write_page(path: Path, title: str, description: str, body: str, *, canonical: str | None = None, metadata_only_description: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    canonical_line = f'canonical-url: "{site_path(canonical)}"\n' if canonical else ""
    description_key = "description-meta" if metadata_only_description else "description"
    path.write_text(f'---\ntitle: "{title.replace(chr(34), chr(39))}"\n{description_key}: "{description.replace(chr(34), chr(39))}"\n{canonical_line}---\n\n<!-- Generated by scripts/generate_site.py; do not edit. -->\n\n{body.rstrip()}\n', encoding="utf-8")


def load_json_records(directory: Path) -> list[dict[str, Any]]:
    return [json.loads(path.read_text(encoding="utf-8")) for path in sorted(directory.glob("*.json"))]


def labels(ids: list[str]) -> list[str]:
    themes = theme_index()
    return [themes[item]["name"] for item in ids]


def tags(items: list[str], css: str = "tag-list") -> str:
    return f'<ul class="{css}">' + "".join(f"<li>{esc(item)}</li>" for item in items) + "</ul>"


def linked_tags(primary: str | None, secondary: list[str]) -> str:
    themes = theme_index()
    values = ([(primary, "Primary")] if primary else []) + [(item, "Related") for item in secondary]
    if not values:
        return '<ul class="tag-list"><li>Cross-cutting or not classified by lab theme</li></ul>'
    return '<ul class="tag-list">' + "".join(f'<li><a href="{esc(site_path(f"/research/{item}.html"))}">{esc(themes[item]["name"])}</a><span class="sr-only"> ({kind})</span></li>' for item, kind in values) + "</ul>"


def provenance_label(cluster: dict[str, Any]) -> str:
    if cluster.get("ai_provenance", {}).get("used") is True:
        return "Identified and summarized using AI · not reviewed by the lab"
    if cluster.get("captured_fixture"):
        return "Captured fixture · no AI generation recorded · not reviewed by the lab"
    return "Automatically identified · no AI generation recorded · not reviewed by the lab"


def provenance_disclosure(cluster: dict[str, Any]) -> str:
    return FULL_DISCLOSURE if cluster.get("ai_provenance", {}).get("used") is True else FIXTURE_DISCLOSURE


def record_card(record: dict[str, Any], kind: str) -> str:
    relation = relationship_label(record.get("relationship_to_lab", ""))
    meta = " · ".join(filter(None, [relation, record.get("status"), record.get("venue"), str(record.get("publication_date", ""))[:4]]))
    return f'''<article class="record-card" data-themes="{esc(' '.join([record['primary_theme'], *record['secondary_themes']]))}">
  <p class="record-kicker">{esc(meta.replace('-', ' ').title())}</p>
  <h3><a href="{esc(site_path(f"/{kind}/{record['record_id']}.html"))}">{esc(record['title'])}</a></h3>
  <p>{esc(record.get('summary') or record.get('abstract_summary'))}</p>
  {linked_tags(record['primary_theme'], record['secondary_themes'])}
</article>'''


def work_title(record: dict[str, Any], publications: dict[str, dict[str, Any]]) -> str:
    if record.get("title"):
        return record["title"]
    publication_id = record["connected_publication_ids"][0]
    return publications[publication_id]["title"]


def work_type_label(record: dict[str, Any]) -> str:
    work_type = record["work_type"].replace("-", " ")
    if record["work_status"] == "ongoing":
        if record["work_type"] in {"research-programme", "project", "research-line"}:
            return f"Ongoing {work_type}"
        if record["work_type"] == "tool":
            return "Active tool"
    return work_type.title()


def relationship_label(value: str) -> str:
    return {
        "current-ccll-work": "Current CCLL work",
        "pre-ccll-work-continuing": "Work begun before CCLL and continuing",
        "foundational-prior-work": "Foundational prior work",
        "associated-collaboration": "Associated collaboration",
    }.get(value, value.replace("-", " ").title())


def work_card(record: dict[str, Any], publications: dict[str, dict[str, Any]]) -> str:
    title = work_title(record, publications)
    themes = [record["primary_theme"], *record["secondary_themes"]]
    relation = relationship_label(record["relationship_to_lab"])
    return f'''<article class="record-card work-card" data-status="{esc(record['work_status'])}" data-type="{esc(record['work_type'])}" data-themes="{esc(' '.join(themes))}" data-geography="{esc(' '.join(record['geographies']))}" data-method="{esc(' '.join(record['methods']))}" data-sector="{esc(' '.join(record['sectors']))}">
  <p class="record-kicker">{esc(work_type_label(record))} · {esc(relation)}</p>
  <h3><a href="{esc(site_path(f"/work/{record['work_id']}.html"))}">{esc(title)}</a></h3>
  <p>{esc(record['summary'])}</p>
  {linked_tags(record['primary_theme'], record['secondary_themes'])}
</article>'''


def featured_example_card(
    selection: dict[str, Any],
    works: dict[str, dict[str, Any]],
    publications: dict[str, dict[str, Any]],
) -> str:
    if selection["record_type"] == "work":
        record = works[selection["record_id"]]
        title = work_title(record, publications)
        kicker = f"{work_type_label(record)} · {relationship_label(record['relationship_to_lab'])}"
        target = site_path(f"/work/{record['work_id']}.html")
    else:
        record = publications[selection["record_id"]]
        title = record["title"]
        kicker = " · ".join((record["publication_type"].replace("-", " ").title(), relationship_label(record["relationship_to_lab"]), record["publication_date"][:4]))
        target = site_path(f"/publications/{record['record_id']}.html")
    qualification = f'<p class="example-boundary">{esc(selection["qualification"])}</p>' if selection.get("qualification") else ""
    return f'''<article class="record-card featured-example" data-record-type="{esc(selection['record_type'])}" data-record-id="{esc(selection['record_id'])}" data-group="{esc(selection['conceptual_grouping'])}">
  <p class="record-kicker">{esc(kicker)}</p>
  <h3><a href="{esc(target)}">{esc(title)}</a></h3>
  <p>{esc(selection['contribution'])}</p>
  {qualification}
  {linked_tags(record['primary_theme'], record['secondary_themes'])}
</article>'''


def conversation_card(cluster: dict[str, Any], sources: dict[str, dict[str, Any]]) -> str:
    principal = sources[cluster["principal_source_id"]]
    linked = [sources[source_id] for source_id in cluster["linked_source_ids"]]
    all_sources = [principal, *linked]
    source_links = "".join(f'<li><span class="source-role">{esc(ROLE_LABELS.get(source["source_role"], source["source_role"]))}</span> <a href="{esc(source["original_url"])}">{esc(source["title"])}</a> <span>— {esc(source["publisher_or_platform"])}</span></li>' for source in all_sources)
    grouped = '<span class="grouped-label">Related sources grouped automatically</span>' if linked else '<span class="entry-kind">Standalone conversation entry</span>'
    compact = provenance_label(cluster)
    fixture = '<span class="fixture-label">Captured fixture</span>' if cluster["captured_fixture"] else ""
    environments = " ".join(cluster["source_environments"])
    theme_values = [item for item in [cluster['primary_theme'], *cluster['secondary_themes']] if item]
    return f'''<article class="conversation-card" data-theme="{esc(' '.join(theme_values))}" data-environment="{esc(environments)}" data-geography="{esc(' '.join(cluster['geographies']))}" data-date="{esc(cluster['date_most_recently_observed'])}" data-kind="{'cluster' if linked else 'standalone'}">
  <p class="conversation-flags"><span class="status-badge unreviewed">{esc(compact)}</span>{fixture}{grouped}</p>
  <h3><a href="{esc(site_path(f"/current-conversations/{cluster['slug']}.html"))}">{esc(cluster['public_title'])}</a></h3>
  <p class="record-meta">{esc(cluster['date_most_recently_observed'])} · {esc(ENV_LABELS[principal['source_environment']])} · {esc(ROLE_LABELS.get(principal['source_role'], principal['source_role']))}</p>
  <p>{esc(cluster['summary'])}</p>
  <p><strong>Why it may be relevant</strong><br>{esc(cluster['reason_for_relevance'])}</p>
  <p class="evidence-limitation"><strong>Evidence and interpretation limitation:</strong> {esc(cluster['limitations'])}</p>
  {linked_tags(cluster['primary_theme'], cluster['secondary_themes'])}
  <details><summary>Original sources and roles</summary><ul class="source-list">{source_links}</ul><p>{esc(cluster['agreement_disagreement_uncertainty'])}</p></details>
  <span class="sr-only">{esc(provenance_disclosure(cluster))}</span>
</article>'''


def select_home_clusters(clusters: list[dict[str, Any]], sources: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    chosen: list[dict[str, Any]] = []
    domains: Counter[str] = Counter()
    lab_count = 0
    for cluster in sorted(clusters, key=lambda item: item["date_most_recently_observed"], reverse=True):
        if not cluster["homepage_eligible"] or cluster["publication_decision"] != "published":
            continue
        principal = sources[cluster["principal_source_id"]]
        if domains[principal["source_domain"]] >= 2:
            continue
        if principal["lab_affiliated"] and lab_count >= 1:
            continue
        chosen.append(cluster); domains[principal["source_domain"]] += 1
        lab_count += int(principal["lab_affiliated"])
        if len(chosen) == 6:
            break
    return chosen


def generate_themes(works: list[dict[str, Any]], ideas: list[dict[str, Any]], publications: list[dict[str, Any]], clusters: list[dict[str, Any]], sources: dict[str, dict[str, Any]]) -> None:
    themes = research_scope()["themes"]
    featured = load_yaml(ROOT / "config/theme_featured_examples.yml")["entries"]
    works_by_id = {record["work_id"]: record for record in works}
    publications_by_id = {record["record_id"]: record for record in publications}
    home = ['<ol class="learning-cycle" aria-label="Four connected research questions">']
    details = ['<div class="detail-grid connected-theme-list">']
    legacy_routes = {
        "urban-climate-learning": "geographies-of-climate-learning",
        "evidence-infrastructure-tools": "where-new-evidence-matters",
        "climate-governance-delivery": "modes-of-climate-delivery",
        "co-benefits-place-based-valuation": "consequences-for-people-and-places",
        "just-transitions-workforce": "consequences-for-people-and-places",
        "canadian-climate-policy": "modes-of-climate-delivery",
    }
    for index, theme in enumerate(themes, 1):
        theme_href = site_path(f"/research/{theme['id']}.html")
        home.append(f'''<li class="cycle-stage"><article aria-labelledby="home-theme-{index}"><span class="theme-number">0{index}</span><p class="cycle-role">{esc(theme['cycle_role'])}</p><h3 id="home-theme-{index}"><a href="{esc(theme_href)}" aria-label="Explore {esc(theme['name'])}">{esc(theme['name'])}</a></h3><p class="theme-proposition">{esc(HOME_THEME_PROPOSITIONS[theme['id']])}</p><p><a class="text-link" href="{esc(theme_href)}" aria-label="Explore this question: {esc(theme['name'])}">Explore this question <span aria-hidden="true">→</span></a></p></article></li>''')
        details.append(f'''<article class="detail-card" id="{esc(theme['id'])}"><div class="detail-index">0{index}</div><div><p class="cycle-role">{esc(theme['cycle_role'])}</p><h2><a href="{esc(theme_href)}">{esc(theme['name'])}</a></h2><p class="guiding-question">{esc(theme['guiding_question'])}</p><p>{esc(theme['homepage_description'])}</p><p><a class="text-link" href="{esc(theme_href)}">View the theme programme →</a></p></div><aside class="detail-meta"><strong>Geographic priorities</strong><span>{esc('; '.join(theme['geographical_priorities']))}</span><strong>Methods of interest</strong><span>{esc('; '.join(theme['methodological_interests']))}</span></aside></article>''')
        relevant_work = [record for record in works if record["primary_theme"] == theme["id"] or theme["id"] in record["secondary_themes"]]
        ongoing_work = [record for record in relevant_work if record["work_status"] == "ongoing"]
        selected_examples = [entry for entry in featured if entry["theme_id"] == theme["id"]]
        theme_ideas = sorted([record for record in ideas if record["theme_id"] == theme["id"] and record["owner_review_status"] != "withheld"], key=lambda item: item["display_order"])
        ongoing_html = '<div class="record-list">' + ''.join(work_card(record, publications_by_id) for record in ongoing_work) + '</div>'
        completed_html = '<div class="record-list featured-example-list">' + ''.join(featured_example_card(entry, works_by_id, publications_by_id) for entry in selected_examples) + '</div>'
        def idea_card(item: dict[str, Any], signature: bool) -> str:
            qualifiers = (f'<p class="idea-qualification"><strong>Research governance qualification.</strong> {esc(item["required_qualification"])}</p>' if item.get("required_qualification") else "") + (f'<p class="idea-qualification"><strong>Analytical boundary.</strong> {esc(item["required_boundary"])}</p>' if item.get("required_boundary") else "")
            reader = f'<p class="idea-reader"><strong>Who might use the answer</strong><br>{esc(item["reader_or_decision_at_stake"])}</p>' if signature and item.get("reader_or_decision_at_stake") else ""
            visible_methods = item['public_method_tags'] if signature else item['public_method_tags'][:2]
            return f'''<article class="idea-card{' signature-idea' if signature else ''}" data-narrative-tier="{esc(item['narrative_tier'])}"><p class="idea-badge">Research idea</p><p class="sr-only">{esc(item['disclaimer'])}</p><h3>{esc(item['working_title'])}</h3><p class="idea-question">{esc(item['question'])}</p><p class="idea-narrative">{esc(item['problem_of_understanding'])} {esc(item['why_it_may_matter'])}</p><p class="idea-approach"><strong>One possible approach</strong><br>{esc(item['possible_research_design'])}</p>{qualifiers}{tags(visible_methods, 'method-list')}{reader}</article>'''
        signature_ideas = [item for item in theme_ideas if item["narrative_tier"] == "signature"]
        additional_ideas = [item for item in theme_ideas if item["narrative_tier"] == "additional"]
        idea_html = f'''<h3 class="idea-group-heading">Questions at the centre of this theme</h3><div class="idea-grid signature-grid">{''.join(idea_card(item, True) for item in signature_ideas)}</div><h3 class="idea-group-heading">Additional directions</h3><div class="idea-grid">{''.join(idea_card(item, False) for item in additional_ideas)}</div>'''
        previous_theme = themes[index - 2] if index > 1 else themes[-1]
        next_theme = themes[index] if index < len(themes) else themes[0]
        connections = f'''- **Input from [{previous_theme['name']}]({site_path(f"/research/{previous_theme['id']}.html")}):** {previous_theme['connection_to_next']}
- **Next stage — [{next_theme['name']}]({site_path(f"/research/{next_theme['id']}.html")}):** {theme['connection_to_next']}
- **Return loop:** Consequences generate new evidence, reveal unresolved questions and revise what other cities may plausibly learn.'''
        body = f'''::: {{.practical-example}}
**A practical example**

{THEME_PRACTICAL_EXAMPLES[theme['id']]}
:::

<p class="term-first-use">{THEME_TERM_NOTES[theme['id']]}</p>

{theme['long_description'][0]}

{theme['long_description'][1]}

::: {{.what-this-changes}}
**The proposition.** {theme['what_this_changes']}
:::

**What this theme does not assume.** {theme['analytical_boundary']}

## Ongoing work

```{{=html}}
{ongoing_html}
```

## Selected completed and foundational work

```{{=html}}
{completed_html}
```

[Explore all verified publications and outputs related to this theme →]({site_path('/publications/complete.html')})

## Questions this theme opens

These are possible directions for future research, not active or funded projects.

<span class="sr-only">Each card retains the full status: {IDEA_DISCLAIMER}</span>

This layout provides a reading hierarchy; it is not a ranking of research priority, funding readiness or importance.

```{{=html}}
{idea_html}
```

## How this connects

{connections}

## Current Conversations

Current Conversations is in development. No live public feed is operating, and no automatically identified item is presented on this page.

[How Current Conversations works]({site_path('/current-conversations/how-it-works.html')}).'''
        write_page(ROOT / "research" / f"{theme['id']}.qmd", theme["name"], theme["guiding_question"], body, canonical=f"/research/{theme['id']}.html")
    for old_id, new_id in legacy_routes.items():
        destination = theme_index()[new_id]
        redirect_body = f'''<p class="page-deck">This former theme route has moved into the lab's four-theme research programme.</p>

[Continue to **{destination['name']}**]({site_path(f'/research/{new_id}.html')}).

This transition page preserves older internal and shared links. It does not define a separate research theme.'''
        write_page(ROOT / "research/themes" / f"{old_id}.qmd", "Research theme route updated", destination["homepage_description"], redirect_body, canonical=f"/research/{new_id}.html")
    home.append('<li class="cycle-return"><strong>Consequences generate further learning.</strong> Results change what cities ask next.</li></ol>')
    details.append('<div class="cycle-return-note"><strong>The return matters:</strong> consequences generate new evidence, expose unresolved questions and change what other places can plausibly learn.</div></div>')
    write_fragment("home-themes.qmd", "\n".join(home)); write_fragment("research-themes.qmd", "\n".join(details))


def generate_people() -> None:
    cards = ['<div class="record-list">']
    for person in load_records("data/people"):
        links = " · ".join(f'<a href="{esc(item["url"])}">{esc(item["label"])}</a>' for item in person["profile_links"])
        cards.append(f'''<article class="record-card person-card"><p class="record-kicker">{esc(person['academic_title'])} · {esc(person['lab_role'])}</p><h2>{esc(person['name'])}</h2><p>{esc(person['short_bio'])}</p><p><a href="mailto:{esc(person['email'])}">{esc(person['email'])}</a></p><p>{links}</p>{tags(labels(person['themes']))}</article>''')
    cards.append("</div>"); write_fragment("people.qmd", "\n".join(cards))


def generate_work(works: list[dict[str, Any]], publications: list[dict[str, Any]]) -> None:
    publications_by_id = {record["record_id"]: record for record in publications}
    listing = '<div class="record-list" id="work-results">' + ''.join(work_card(record, publications_by_id) for record in works) + '</div>'
    write_fragment("work.qmd", listing)
    work_by_id = {record["work_id"]: record for record in works}
    for record in works:
        title = work_title(record, publications_by_id)
        public_sources = [item for item in record["authoritative_sources"] if item.get("url") and item.get("source_type") == "public-web"]
        sources = "\n".join(f'- [{item["label"]}]({item["url"]}) — accessed {item["retrieved_date"]}' for item in public_sources)
        publication_connections = "\n".join(f'- [{publications_by_id[item]["title"]}]({site_path(f"/publications/{item}.html")})' for item in record["connected_publication_ids"] if item in publications_by_id)
        work_connections = "\n".join(f'- [{work_title(work_by_id[item], publications_by_id)}]({site_path(f"/work/{item}.html")})' for item in record["connected_work_ids"] if item in work_by_id)
        secondary_html = ", ".join(f'<a href="{esc(site_path(f"/research/{item}.html"))}">{esc(theme_index()[item]["name"])}</a>' for item in record["secondary_themes"]) or "No secondary theme assigned."
        tool_connections = "\n".join(f'- [{work_title(work_by_id[item], publications_by_id)}]({site_path(f"/work/{item}.html")})' for item in record["connected_tool_ids"] if item in work_by_id)
        connected_items = "\n".join(value for value in (publication_connections, work_connections, tool_connections) if value)
        questions = chr(10).join("- " + item for item in record["research_questions"])
        panel_title = "Project at a glance" if record["work_type"] == "project" and record["work_status"] == "completed" else "Work at a glance"
        metadata = f'''<section class="work-at-a-glance" aria-labelledby="work-glance-heading"><h2 id="work-glance-heading">{panel_title}</h2><dl><dt>Work type</dt><dd>{esc(work_type_label(record))}</dd><dt>Status</dt><dd>{esc(record['work_status'].title())}</dd><dt>Main theme</dt><dd><a href="{esc(site_path(f"/research/{record['primary_theme']}.html"))}">{esc(theme_index()[record['primary_theme']]['name'])}</a></dd><dt>Geographical focus</dt><dd>{esc(display_list('geographies', record['geographies']))}</dd><dt>Key methods</dt><dd>{esc(display_list('methods', record['methods']))}</dd></dl></section>'''
        provenance = f'''<details class="work-provenance"><summary>Relationship and record context</summary><p>{esc(relationship_label(record['relationship_to_lab']))} — {esc(record['relationship_note'])}</p><p><strong>Related themes:</strong> {secondary_html}</p></details>'''
        outputs = connected_items or "No separate public output is listed for this record."
        if record["work_type"] in {"research-programme", "research-line"}:
            body = f'''## Why this work began

{record['problem_of_understanding']}

## What we are trying to understand

{record['central_question']}

{questions}

## How we are approaching it

{record['how_it_investigates']}

{record['reader_value']}

## Where the work stands

{record['evidence_status']}

**What not to infer.** {record['claim_boundaries']}

## Publications and outputs

{outputs}'''
        elif record["work_type"] in {"paper", "study", "report"}:
            body = f'''## The question

{record['central_question']}

{record['problem_of_understanding']}

## What the paper examines

{record['how_it_investigates']}

{questions}

## Why the answer matters

{record['reader_value']}

## Evidence and status

{record['evidence_status']}

**What not to infer.** {record['claim_boundaries']}

## Publication

{outputs}'''
        elif record["work_type"] == "project" and record["work_status"] == "completed":
            body = f'''## The problem the project addressed

{record['problem_of_understanding']}

{record['central_question']}

## What the project produced

{record['how_it_investigates']}

## What it helps us understand

{record['reader_value']}

## Limits and context

{record['evidence_status']}

**What not to infer.** {record['claim_boundaries']}

## Outputs and tools

{outputs}'''
        else:
            body = f'''## What the tool shows

{record['summary']}

{record['problem_of_understanding']}

{record['central_question']}

## How it can be used

{record['reader_value']}

## What users should not infer

{record['claim_boundaries']}

## Data and methods

{record['how_it_investigates']}

{record['evidence_status']}

## Related project and publications

{outputs}'''
        body += f'''\n\n```{{=html}}
{metadata}

{provenance}
```

{f'''## Authoritative sources

{sources}''' if sources else ''}
'''
        write_page(ROOT / "work" / f"{record['work_id']}.qmd", title, record["summary"], body, canonical=f"/work/{record['work_id']}.html")
        transition = f'''<p class="page-deck">This record now appears in the broader Work section.</p>

[Continue to **{title}**]({site_path(f"/work/{record['work_id']}.html")}).

The former Projects route is retained so older links continue to resolve. It is not a second canonical record.'''
        write_page(ROOT / "projects" / f"{record['work_id']}.qmd", "Research work route updated", record["summary"], transition, canonical=f"/work/{record['work_id']}.html")


GENERIC_PUBLICATION_SUMMARY = "Verified bibliographic record. Consult the original source for its scope, methods, findings and limitations."


def publication_text(value: Any) -> str:
    """Decode source entities for display, then escape; canonical bytes stay fixed."""
    return esc(html.unescape(str(value)))


def publication_status_label(value: str) -> str:
    return {
        "peer-reviewed": "Peer-reviewed",
        "preprint": "Preprint · not peer-reviewed",
        "working-paper": "Working paper · peer review not established",
        "not-applicable": "Not applicable to this output type",
        "unknown": "Peer-review status not verified",
    }[value]


def publication_relationship_label(value: str) -> str:
    return "Current lab output" if value == "current-ccll-work" else relationship_label(value)


def publication_body(record: dict[str, Any], works: dict[str, dict[str, Any]], publications: dict[str, dict[str, Any]]) -> str:
    details = [("Authors", ", ".join(record["authors"])), ("Published", record["publication_date"]),
               ("Venue or publisher", record["venue"]), ("Output type", record["publication_type"].replace("-", " ").capitalize()),
               ("Peer-review status", publication_status_label(record["peer_review_status"]))]
    for field, label in (("volume", "Volume"), ("issue", "Issue"), ("pages", "Pages"), ("article_number", "Article number"), ("version", "Version"), ("current_version_date", "Current version date")):
        if record.get(field):
            value = vocabulary_labels("publication_versions", [record[field]])[0] if field == "version" else record[field]
            details.append((label, value))
    bibliography = '<dl class="publication-details">' + ''.join(f'<dt>{label}</dt><dd>{publication_text(value)}</dd>' for label, value in details)
    if record.get("doi"):
        bibliography += f'<dt>DOI</dt><dd><a href="{esc("https://doi.org/" + record["doi"])}">{publication_text(record["doi"])}</a></dd>'
    elif record.get("other_identifiers"):
        bibliography += f'<dt>Stable identifier</dt><dd>{publication_text("; ".join(record["other_identifiers"]))}</dd>'
    else:
        bibliography += '<dt>Stable identifier</dt><dd>Original-source URL (no separate identifier recorded)</dd>'
    bibliography += '</dl>'
    relationship = f'<p class="publication-relationship"><strong>Relationship to the lab:</strong> {publication_relationship_label(record["relationship_to_lab"])}</p>'
    # Only distinctive chronology/collaboration notes are public. Every full note
    # remains untouched in the canonical record, including generic prior-work notes.
    if record["relationship_to_lab"] != "foundational-prior-work" or record["record_id"] == "designing-visualization-atlas-uk-cobenefits":
        relationship += f'<p>{publication_text(record["relationship_note"])}</p>'
    summary = f'<p class="publication-description">{publication_text(record["abstract_summary"])}</p>' if record["abstract_summary"] != GENERIC_PUBLICATION_SUMMARY else ""
    # A default classification alone is not a verified public theme relationship.
    relationships = record.get("theme_relationships", [])
    theme_links = '<p class="eyebrow">Related research themes</p>' + linked_tags(record["primary_theme"], record["secondary_themes"]) if relationships else ""
    connections = ''.join(f'<li><a href="{site_path("/work/" + work_id + ".html")}">{publication_text(work_title(works[work_id], publications))}</a></li>' for work_id in record["connected_work_ids"] if work_id in works)
    work_links = f'<p class="eyebrow">Connected work</p><ul>{connections}</ul>' if connections else ""
    mdpi_note = '<p class="notice">Retained in the complete scholarly record; not selected, featured or eligible for Current Conversations.</p>' if record.get("mdpi_excluded") else ""
    return f'''```{{=html}}
{bibliography}
{relationship}
{summary}
{theme_links}
{work_links}
<p><a class="publication-original-source" href="{esc(record['url'])}">Open the original source</a></p>
<details class="publication-citation"><summary>Citation</summary><p>{publication_text(record['citation'])}</p></details>
{mdpi_note}
<p class="record-meta">Record last verified: {record['last_verified_date']}.</p>
<p class="publication-record-links"><a href="{site_path('/publications/metadata-and-sources.html')}">Metadata and sources</a> · <a href="{site_path('/publications/metadata-and-sources.html#corrections')}">Report a correction</a></p>
```'''


def generate_publications(publications: list[dict[str, Any]]) -> None:
    selected = [record for record in publications if record["featured"]]
    write_fragment("publications-selected.qmd", '<div class="record-list">' + ''.join(record_card(record, "publications") for record in selected) + '</div>')
    by_year: dict[str, list[dict[str, Any]]] = {}
    for record in publications: by_year.setdefault(record["publication_date"][:4], []).append(record)
    complete = []
    for year in sorted(by_year, reverse=True):
        complete.append(f'<section class="bibliography-year" id="year-{year}"><h2>{year}</h2><div class="bibliography-list">')
        for record in sorted(by_year[year], key=lambda item: item["title"]):
            status = publication_status_label(record["peer_review_status"])
            mdpi = '<span class="status-badge neutral">Complete record only · not selected</span>' if record.get("mdpi_excluded") else ""
            themes = " ".join([record["primary_theme"], *record["secondary_themes"]])
            complete.append(f'<article class="bibliography-entry" data-year="{year}" data-type="{esc(record["publication_type"])}" data-themes="{esc(themes)}"><h3><a href="{esc(site_path(f"/publications/{record['record_id']}.html"))}">{publication_text(record["title"])}</a></h3><p>{publication_text(", ".join(record["authors"]))}</p><p class="record-meta">{publication_text(record["venue"])} · {esc(record["publication_type"].replace("-", " ").title())} · {esc(status)} {mdpi}</p></article>')
        complete.append('</div></section>')
    write_fragment("publications-complete.qmd", "".join(complete))
    complete_body = '''<p class="page-deck">A complete verified record of Andrew Sudmant's publications and outputs, distinct from the smaller selected set.</p>

Records are grouped by year. Historic outputs are labelled as foundational or prior work and are not presented as products of the new lab. [Publication metadata and sources](/publications/metadata-and-sources.html) explains the records and their status.

```{=html}
<form class="publication-filters" data-publication-filters aria-label="Filter verified publications and outputs">
  <label>Keyword <input type="search" name="query" autocomplete="off"></label>
  <label>Type <select name="type"><option value="">All output types</option><option value="article">Articles</option><option value="preprint">Preprints</option><option value="chapter">Chapters</option><option value="report">Reports</option><option value="dataset">Datasets</option><option value="other">Other</option></select></label>
  <button type="reset">Clear</button><output data-publication-count aria-live="polite"></output>
</form>
```

{{< include ../generated/publications-complete.qmd >}}

[Return to selected publications](__PUBLICATIONS_RETURN__).'''.replace("__PUBLICATIONS_RETURN__", site_path("/publications.html"))
    write_page(ROOT / "publications/complete.qmd", "Verified publications and outputs", "Verified publications and outputs by Andrew Sudmant, with authoritative-source provenance.", complete_body)
    works = {record["work_id"]: record for record in load_records("data/work")}
    publications_by_id = {record["record_id"]: record for record in publications}
    for record in publications:
        body = publication_body(record, works, publications_by_id)
        write_page(ROOT / "publications" / f"{record['record_id']}.qmd", record["title"], record["abstract_summary"], body, metadata_only_description=True)


def generate_conversations(clusters: list[dict[str, Any]], source_list: list[dict[str, Any]]) -> None:
    # Fixture records remain available to schema and regression tests, but Gate 5E
    # deliberately produces no public cards, detail pages or machine-readable feed.
    write_fragment("current-conversations-feed.qmd", "<!-- Current Conversations is in development; no public entries. -->")
    write_fragment("home-current-conversations.qmd", "<!-- Current Conversations is in development; no public entries. -->")
    for feed in (ROOT / "current-conversations/feed.json", ROOT / "current-conversations/feed.xml"):
        feed.unlink(missing_ok=True)


def generate_site_status() -> None:
    config = load_yaml(ROOT / "config/site.yml")
    banner = "<!-- Generated by scripts/generate_site.py from config/site.yml; do not edit. -->\n"
    if config["site_status"] == "draft":
        banner += '''<aside class="site-status-banner column-screen" role="status" aria-label="Draft website status">
  <div><strong>Draft website</strong><span>The Cities and Climate Learning Lab is being established at Simon Fraser University. Some descriptions of developing research and possible future work will continue to be refined.</span></div>
</aside>\n'''
    (ROOT / "assets/site-status.html").write_text(banner, encoding="utf-8")
    (ROOT / "assets/site-scripts.html").write_text(
        f'<script src="{site_path("/assets/site.js")}" defer></script>\n',
        encoding="utf-8",
    )


def generate_all() -> None:
    errors = validate_all()
    if errors: raise ValueError("content validation failed:\n" + "\n".join(errors))
    OUT.mkdir(exist_ok=True)
    works = load_records("data/work")
    ideas = load_records("data/research-ideas")
    complete = json.loads((ROOT / "reports/content/publication-complete-inventory.json").read_text(encoding="utf-8"))["records"]
    sources = load_json_records(ROOT / "data/current-conversations/generated/sources")
    clusters = load_json_records(ROOT / "data/current-conversations/generated/clusters")
    generate_themes(works, ideas, complete, clusters, {record["source_id"]: record for record in sources})
    generate_people(); generate_work(works, complete); generate_publications(complete); generate_conversations(clusters, sources); generate_site_status()
    expected: dict[Path, set[str]] = {
        OUT: {
            "home-themes.qmd", "research-themes.qmd", "people.qmd", "work.qmd",
            "publications-selected.qmd", "publications-complete.qmd",
            "current-conversations-feed.qmd", "home-current-conversations.qmd",
        },
        ROOT / "work": {f"{record['work_id']}.qmd" for record in works},
        ROOT / "projects": {f"{record['work_id']}.qmd" for record in works},
        ROOT / "publications": {"complete.qmd", "metadata-and-sources.qmd", *{f"{record['record_id']}.qmd" for record in complete}},
        ROOT / "research": {"our-approach.qmd", *{f"{theme['id']}.qmd" for theme in research_scope()["themes"]}},
        ROOT / "research/themes": {
            "urban-climate-learning.qmd", "evidence-infrastructure-tools.qmd",
            "climate-governance-delivery.qmd", "co-benefits-place-based-valuation.qmd",
            "just-transitions-workforce.qmd", "canadian-climate-policy.qmd",
        },
        ROOT / "current-conversations": {
            "index.qmd", "how-it-works.qmd",
        },
    }
    # Cleanup happens only after every current page and feed has been written.
    # A generation failure therefore leaves the prior complete source tree intact.
    for directory, names in expected.items():
        for path in directory.glob("*.qmd"):
            if path.name not in names:
                path.unlink()


def main() -> int:
    try: generate_all()
    except ValueError as exc:
        print(exc); return 1
    print("Generated canonical listings, publication views, theme pages and the configured site-status banner.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
