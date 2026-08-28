from __future__ import annotations

import hashlib
import re
from pathlib import Path

import yaml

from scripts.content import ROOT, load_records, research_scope
from scripts.generate_site import generate_all
from scripts.validate_content import CANONICAL_THEME_ORDER


DISCLAIMER = "Research idea · not currently an active or funded project"
OLD_ID_FILES = {
    "g1-transfer-conditions", "g2-evidence-absence", "g3-evidence-change",
    "e1-next-case", "e2-causal-evaluation", "e3-consequential-exclusions",
    "d1-delivery-configurations", "d2-delivery-over-time", "d3-canadian-multilevel-delivery",
    "c1-distribution-neighbourhoods", "c2-social-cohesion", "c3-durable-co-benefits",
    "c4-appraisal-adverse-effects",
}


def test_theme_reader_value_contract_and_exact_order() -> None:
    themes = research_scope()["themes"]
    assert [(item["id"], item["name"]) for item in themes] == CANONICAL_THEME_ORDER
    assert len(themes) == 4
    for theme in themes:
        assert theme["guiding_question"] and len(theme["long_description"]) == 2
        assert theme["analytical_boundary"] and theme["what_this_changes"] and theme["connection_to_next"]
        assert not {"status", "maturity", "portfolio_maturity"}.intersection(theme)
        assert "evidence to action" not in " ".join(theme["long_description"]).casefold()
    assert "size of an evidence gap" in themes[1]["what_this_changes"]
    assert "configuration" in themes[2]["analytical_boundary"]
    assert "harms" in themes[3]["analytical_boundary"] and "distribution" in themes[3]["what_this_changes"]
    assert "does not presume" in themes[0]["analytical_boundary"]


def test_24_ideas_have_reader_value_fields_and_no_work_claims() -> None:
    ideas = load_records("data/research-ideas")
    assert len(ideas) == 24
    assert len({item["idea_id"] for item in ideas}) == 24
    assert [sum(item["theme_id"] == theme for item in ideas) for theme, _ in CANONICAL_THEME_ORDER] == [6, 6, 6, 6]
    forbidden = {"funders", "funder", "partners", "partner", "start_date", "outputs", "deliverables", "connected_publication_ids", "parent_work_id"}
    for idea in ideas:
        for field in ("working_title", "question", "problem_of_understanding", "why_it_may_matter", "possible_research_design"):
            assert idea[field]
        assert idea["suggested_methods"] and idea["disclaimer"] == DISCLAIMER
        assert not forbidden.intersection(idea)
    by_id = {item["idea_id"]: item for item in ideas}
    assert by_id["g5-knowledge-admissibility"]["required_qualification"] == "Methods and research governance would need to be developed with appropriate Indigenous or community partners rather than specified unilaterally in advance."
    assert by_id["e1-next-city"]["required_boundary"] == "This is an academic research question, not a proposal for a single public city-ranking or marginal-learning-value score."


def test_gate_5d_idea_ids_are_migrated_not_active_or_duplicated() -> None:
    active = {item["idea_id"] for item in load_records("data/research-ideas")}
    assert not OLD_ID_FILES.intersection(active)
    migration = (ROOT / "docs/migrations/research-ideas-gate-5d-to-gate-5e.md").read_text()
    assert all(f"`{item}`" in migration for item in OLD_ID_FILES)


def test_ideas_do_not_enter_other_public_models() -> None:
    generate_all()
    idea_ids = {item["idea_id"] for item in load_records("data/research-ideas")}
    surfaces = [ROOT / "generated/work.qmd", ROOT / "generated/publications-selected.qmd", ROOT / "generated/publications-complete.qmd", ROOT / "generated/current-conversations-feed.qmd"]
    combined = "\n".join(path.read_text() for path in surfaces)
    assert not idea_ids.intersection(combined.split())
    assert DISCLAIMER not in combined
    assert len(load_records("data/work")) == 7


def test_previous_work_source_records_are_byte_for_byte_frozen() -> None:
    fixture = yaml.safe_load((ROOT / "tests/fixtures/gate-5d-previous-work-freeze.yml").read_text())
    for relative, expected in fixture["source_file_hashes"].items():
        observed = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        assert observed == expected, relative


def test_previous_work_ids_and_display_order_are_frozen() -> None:
    generate_all()
    fixture = yaml.safe_load((ROOT / "tests/fixtures/gate-5d-previous-work-freeze.yml").read_text())
    for theme_id, expected in fixture["selected_previous_work"].items():
        page = (ROOT / "research" / f"{theme_id}.qmd").read_text()
        section = page.split("## Selected completed and foundational work", 1)[1].split("## Questions this theme opens", 1)[0]
        observed = [f"{kind}/{slug[:-5]}" for kind, slug in re.findall(r'href="/(work|publications)/([^\"]+\.html)', section)]
        assert observed == expected


def test_current_conversations_is_in_development_and_has_no_public_entries() -> None:
    generate_all()
    landing = (ROOT / "current-conversations/index.qmd").read_text()
    methods = (ROOT / "current-conversations/how-it-works.qmd").read_text()
    assert "In development" in landing
    assert "The live feed is not yet enabled" in landing
    assert "Inclusion will not indicate endorsement" in landing
    assert "Current Conversations is not yet operating as a live public feed." in methods
    for forbidden in ("watch-filters", "data-conversation-count", "feed.xml", "feed.json", "last updated"):
        assert forbidden.casefold() not in landing.casefold()
    assert not list((ROOT / "current-conversations").glob("*.json"))
    assert not list((ROOT / "current-conversations").glob("*.xml"))
    assert {path.name for path in (ROOT / "current-conversations").glob("*.qmd")} == {"index.qmd", "how-it-works.qmd"}


def test_site_status_is_single_source_and_accessible() -> None:
    generate_all()
    config = yaml.safe_load((ROOT / "config/site.yml").read_text())
    assert config == {"site_status": "draft", "site_version": "0.1", "current_conversations": {"status": "in-development", "public_feed_enabled": False}}
    banner = (ROOT / "assets/site-status.html").read_text()
    assert 'role="status"' in banner and "Draft website" in banner
    assert "being established at Simon Fraser University" in banner
    quarto = yaml.safe_load((ROOT / "_quarto.yml").read_text())
    assert quarto["format"]["html"]["include-before-body"] == "assets/site-status.html"


def test_public_sources_do_not_contain_internal_gate_or_owner_review_copy() -> None:
    generate_all()
    sources = [ROOT / "index.qmd", ROOT / "research.qmd", ROOT / "work.qmd", ROOT / "current-conversations/index.qmd", ROOT / "current-conversations/how-it-works.qmd"]
    sources += list((ROOT / "research").glob("*.qmd"))
    text = "\n".join(path.read_text() for path in sources).casefold()
    assert "gate 5d" not in text and "gate 5e" not in text
    assert "owner review" not in text and "owner-review" not in text


def test_no_build_or_test_api_side_effect_and_no_deployment_workflow() -> None:
    makefile = (ROOT / "Makefile").read_text().casefold()
    build_recipe = makefile.split("build: generate", 1)[1].split("linkcheck:", 1)[0]
    normal = build_recipe + (ROOT / "scripts/pre-render.sh").read_text().casefold()
    assert "curl " not in normal and "openai_api_key" not in normal and "discover" not in normal
    workflows = "\n".join(path.read_text() for path in sorted((ROOT / ".github/workflows").glob("*.yml"))).casefold()
    assert "quarto publish" not in workflows and "pages: write" not in workflows and "deploy-pages" not in workflows


def test_fixture_directory_is_explicitly_non_public() -> None:
    marker = (ROOT / "data/current-conversations/generated/README.md").read_text()
    assert "test and regression fixtures only" in marker.casefold()
    assert "must never be rendered" in marker.casefold()


def test_fixture_ids_and_titles_do_not_leak_into_built_site_search_or_sitemap() -> None:
    generate_all()
    records = []
    for kind in ("sources", "clusters"):
        for path in sorted((ROOT / f"data/current-conversations/generated/{kind}").glob("*.json")):
            records.append(__import__("json").loads(path.read_text()))
    forbidden = {item.get("source_id") or item.get("cluster_id") for item in records}
    forbidden |= {item.get("title") or item.get("public_title") for item in records}
    public_paths = [path for path in (ROOT / "_site").rglob("*") if path.is_file() and path.suffix in {".html", ".json", ".xml"}]
    public = "\n".join(path.read_text(errors="ignore") for path in public_paths)
    assert all(value not in public for value in forbidden if value)
    search = (ROOT / "_site/search.json").read_text()
    assert all(value not in search for value in forbidden if value)
    sitemap = ROOT / "_site/sitemap.xml"
    if sitemap.exists():
        sitemap_text = sitemap.read_text()
        assert all(value not in sitemap_text for value in forbidden if value)
