from __future__ import annotations

import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from scripts.content import ROOT, load_records, research_scope
from scripts.generate_site import generate_all
from scripts.validate_content import CANONICAL_THEME_ORDER, load_schema, validate_all


DISCLAIMER = "Research idea · not currently an active or funded project"
WORK_TYPES = {"research-programme", "research-line", "project", "study", "paper", "report", "tool", "dataset"}
RELATIONSHIPS = {"current-ccll-work", "pre-ccll-work-continuing", "foundational-prior-work", "associated-collaboration"}


def complete_publications() -> list[dict]:
    return json.loads((ROOT / "reports/content/publication-complete-inventory.json").read_text())["records"]


def theme_page(theme_id: str) -> str:
    return (ROOT / "research" / f"{theme_id}.qmd").read_text()


def test_themes_are_four_equal_current_questions_without_status() -> None:
    themes = research_scope()["themes"]
    assert [(item["id"], item["name"]) for item in themes] == CANONICAL_THEME_ORDER
    forbidden = {"status", "maturity", "portfolio_maturity", "established", "developing"}
    assert all(not forbidden.intersection(theme) for theme in themes)
    assert all(len(theme["long_description"]) == 2 for theme in themes)
    assert all(theme["analytical_boundary"] and theme["connection_to_next"] for theme in themes)
    assert "portfolio_maturity" not in load_schema("research-theme.schema.json")["properties"]


def test_research_work_schema_values_parent_and_no_required_funder_partner() -> None:
    schema = load_schema("research-work.schema.json")
    assert set(schema["properties"]["work_type"]["enum"]) == WORK_TYPES
    assert set(schema["properties"]["work_status"]["enum"]) == {"ongoing", "completed"}
    assert set(schema["properties"]["relationship_to_lab"]["enum"]) == RELATIONSHIPS
    assert "null" in schema["properties"]["parent_work_id"]["type"]
    assert not {"funders", "partners", "start_date", "end_date"}.intersection(schema["required"])
    assert validate_all() == []


def test_standalone_paper_validates_without_parent_and_derives_title() -> None:
    work = next(item for item in load_records("data/work") if item["work_id"] == "geography-urban-climate-evidence")
    assert work["work_type"] == "paper" and work["work_status"] == "ongoing"
    assert work["parent_work_id"] is None and work["title"] is None
    assert work["connected_publication_ids"] == ["who-can-learn-geography-urban-climate-evidence"]
    page = (ROOT / "work/geography-urban-climate-evidence.qmd").read_text()
    assert "Who can learn from whom? The geography of urban climate evidence" in page
    assert "readily learn" not in page.casefold()


def test_programme_links_multiple_outputs_and_project_links_active_tool() -> None:
    works = {item["work_id"]: item for item in load_records("data/work")}
    delivery = works["climate-delivery-modes"]
    assert delivery["work_type"] == "research-programme" and delivery["work_status"] == "ongoing"
    assert "from-urban-climate-ambition-to-delivery" in delivery["connected_publication_ids"]
    atlas = works["uk-co-benefits-atlas"]
    tool = works["uk-co-benefits-atlas-tool"]
    assert atlas["work_type"] == "project" and atlas["work_status"] == "completed"
    assert tool["work_type"] == "tool" and tool["work_status"] == "ongoing"
    assert tool["parent_work_id"] == atlas["work_id"] and tool["work_id"] in atlas["connected_tool_ids"]


def test_six_record_migration_matches_owner_decisions() -> None:
    works = {item["work_id"]: item for item in load_records("data/work")}
    expected = {
        "geography-urban-climate-evidence": ("paper", "ongoing", "pre-ccll-work-continuing"),
        "data-methodologies-climate-impact": ("project", "completed", "foundational-prior-work"),
        "climate-delivery-modes": ("research-programme", "ongoing", "current-ccll-work"),
        "coben-place-based-model": ("research-programme", "ongoing", "current-ccll-work"),
        "occupational-transition-requirements": ("research-line", "ongoing", "current-ccll-work"),
        "uk-co-benefits-atlas": ("project", "completed", "foundational-prior-work"),
    }
    assert {key: (works[key]["work_type"], works[key]["work_status"], works[key]["relationship_to_lab"]) for key in expected} == expected
    assert "predict individual employment outcomes" in works["occupational-transition-requirements"]["claim_boundaries"]
    assert "forecasts" in works["coben-place-based-model"]["claim_boundaries"]


def test_research_ideas_validate_and_have_no_work_claims() -> None:
    ideas = load_records("data/research-ideas")
    assert len(ideas) == 13
    schema = load_schema("research-idea.schema.json")
    validator = Draft202012Validator(schema)
    forbidden = {"work_status", "status", "funders", "partners", "start_date", "end_date", "outputs", "connected_publication_ids"}
    for idea in ideas:
        assert not list(validator.iter_errors(idea))
        assert idea["question"] and idea["suggested_methods"]
        assert idea["disclaimer"] == DISCLAIMER
        assert not forbidden.intersection(idea)
    counts = {theme_id: sum(item["theme_id"] == theme_id for item in ideas) for theme_id, _ in CANONICAL_THEME_ORDER}
    assert list(counts.values()) == [3, 3, 3, 4]


def test_ideas_are_excluded_from_work_publications_conversations_and_feeds() -> None:
    generate_all()
    idea_ids = {item["idea_id"] for item in load_records("data/research-ideas")}
    surfaces = [
        ROOT / "generated/work.qmd",
        ROOT / "generated/publications-selected.qmd",
        ROOT / "generated/publications-complete.qmd",
        ROOT / "generated/current-conversations-feed.qmd",
        ROOT / "current-conversations/feed.json",
        ROOT / "current-conversations/feed.xml",
    ]
    combined = "\n".join(path.read_text() for path in surfaces)
    assert not any(idea_id in combined for idea_id in idea_ids)
    assert DISCLAIMER not in combined
    assert len(load_records("data/work")) == 7


def test_every_theme_page_uses_required_order_and_distinct_idea_treatment() -> None:
    generate_all()
    for theme_id, _ in CANONICAL_THEME_ORDER:
        page = theme_page(theme_id)
        headings = ["## Ongoing work", "## Selected completed and foundational work", "## Research ideas", "## Connections across the learning cycle", "## External horizon scanning: Current Conversations"]
        positions = [page.index(heading) for heading in headings]
        assert positions == sorted(positions)
        assert "Analytical boundary" in page and "Place in the learning cycle" in page
        assert DISCLAIMER in page and 'class="idea-card"' in page
        assert "No verified records are published in this view yet" not in page
        assert "Items are collected, classified and summarised automatically" in page


def test_selected_theme_examples_are_canonical_supported_deduplicated_and_not_mdpi() -> None:
    records = {item["record_id"]: item for item in complete_publications()}
    all_pages = "\n".join(theme_page(theme_id) for theme_id, _ in CANONICAL_THEME_ORDER)
    for record in records.values():
        if record.get("theme_relationships"):
            for relationship in record["theme_relationships"]:
                assert relationship["rationale"] and relationship["evidence_source"].startswith("https://")
        if record.get("mdpi_excluded"):
            assert f'/publications/{record["record_id"]}.html' not in all_pages
    for theme_id, _ in CANONICAL_THEME_ORDER:
        page = theme_page(theme_id)
        links = [line for line in page.split('href="') if line.startswith("/publications/")]
        publication_paths = [line.split('"', 1)[0] for line in links]
        assert len(publication_paths) == len(set(publication_paths))
    assert "title alone" in (ROOT / "reports/content/theme-examples-audit-gate-5d.md").read_text().casefold()


def test_publication_work_links_use_canonical_ids_and_no_synthetic_parent() -> None:
    records = {item["record_id"]: item for item in complete_publications()}
    assert records["replicate-generalize-urban-research"]["connected_work_ids"] == []
    assert records["who-can-learn-geography-urban-climate-evidence"]["connected_work_ids"] == ["geography-urban-climate-evidence"]
    assert records["from-urban-climate-ambition-to-delivery"]["connected_work_ids"] == ["climate-delivery-modes"]
    assert all("connected_projects" not in item for item in records)


def test_work_navigation_route_and_homepage_labels() -> None:
    config = yaml.safe_load((ROOT / "_quarto.yml").read_text())
    navigation = config["website"]["navbar"]["left"]
    assert any(item.get("href") == "work.qmd" and item.get("text") == "Work" for item in navigation)
    assert not any(item.get("text") == "Projects" for item in navigation)
    assert "Research programmes, projects and studies" in (ROOT / "work.qmd").read_text()
    assert "does not maintain a second canonical listing" in (ROOT / "projects.qmd").read_text()
    homepage = (ROOT / "index.qmd").read_text()
    assert "Featured work" in homepage
    assert "Ongoing paper" in homepage and homepage.count("Ongoing research programme") == 2


def test_work_filters_and_listing_exclude_ideas_and_describe_types() -> None:
    source = (ROOT / "work.qmd").read_text()
    for value in ("ongoing", "completed", "research-programme", "project", "study", "paper", "report", "tool", "dataset"):
        assert f'value="{value}"' in source
    for name in ("theme", "geography", "method", "sector"):
        assert f'name="{name}"' in source
    generated = (ROOT / "generated/work.qmd").read_text()
    assert generated.count('class="record-card work-card"') == 7
    assert DISCLAIMER not in generated


def test_former_project_routes_are_transitions_and_only_work_is_canonical() -> None:
    for work in load_records("data/work"):
        transition = (ROOT / "projects" / f'{work["work_id"]}.qmd').read_text()
        assert "Research work route updated" in transition
        assert f'canonical-url: "/work/{work["work_id"]}.html"' in transition
        assert (ROOT / "work" / f'{work["work_id"]}.qmd').exists()
    assert not (ROOT / "generated/projects.qmd").exists()


def test_current_conversations_remains_external_last_and_ideas_never_enter() -> None:
    exact = "Items are collected, classified and summarised automatically to show where the lab’s topics are being discussed. Inclusion does not indicate endorsement, evidential quality or applicability to a particular city."
    for theme_id, _ in CANONICAL_THEME_ORDER:
        page = theme_page(theme_id)
        assert exact in page
        assert page.index("## Research ideas") < page.index("## External horizon scanning: Current Conversations")
    clusters = [json.loads(path.read_text()) for path in (ROOT / "data/current-conversations/generated/clusters").glob("*.json")]
    assert any(item["primary_theme"] is None for item in clusters)
    assert all("idea_id" not in item and "work_id" not in item for item in clusters)


def test_normal_build_and_generation_have_no_discovery_or_paid_side_effect() -> None:
    makefile = (ROOT / "Makefile").read_text()
    build = makefile.split("build: generate", 1)[1].split("linkcheck:", 1)[0]
    assert "discover" not in build and "benchmark" not in build and "OPENAI_API_KEY" not in build


def test_active_public_copy_has_no_readily_learn_or_theme_maturity_badges() -> None:
    sources = [ROOT / "index.qmd", ROOT / "research.qmd", ROOT / "work.qmd"]
    sources += list((ROOT / "research").glob("*.qmd")) + list((ROOT / "work").glob("*.qmd"))
    text = "\n".join(path.read_text() for path in sources)
    assert "readily learn" not in text.casefold()
    assert "theme-status" not in text
    assert "Established" not in text and "Developing" not in text


def test_governance_documents_are_not_public_routes() -> None:
    config = (ROOT / "_quarto.yml").read_text()
    assert "docs/*.md" not in config and "docs/reviews" not in config
    if (ROOT / "_site/search.json").is_file():
        search = (ROOT / "_site/search.json").read_text()
        assert "research-work-architecture-audit" not in search
