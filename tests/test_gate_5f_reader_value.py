from __future__ import annotations

import json
import re

import yaml

from scripts.content import ROOT, load_records, research_scope
from scripts.generate_site import HOME_THEME_PROPOSITIONS, generate_all
from scripts.validate_content import CANONICAL_THEME_ORDER, validate_all


def test_homepage_claim_reader_paths_and_order() -> None:
    source = (ROOT / "index.qmd").read_text()
    assert "Cities <span>&</span> Climate<br>Learning Lab" in source
    assert "How cities find, generate and use evidence for climate action." in source
    assert "Urban climate evidence does not become useful merely because it exists." in source
    assert "Treating these questions separately can make evidence appear more transferable" in source
    for heading, destination in {
        "For researchers": "research.html",
        "For policy and practice": "work.html",
        "For prospective students and collaborators": "opportunities.html",
    }.items():
        assert heading in source and f'href="{destination}"' in source
    assert source.index("Who this programme is for") < source.index("Featured work") < source.index("Current Conversations · In development")
    assert not re.search(r"fund(ed|ing)|supervis(ion|or)", source, re.I)


def test_home_theme_cards_are_four_ordered_propositions() -> None:
    generate_all()
    home = (ROOT / "generated/home-themes.qmd").read_text()
    assert home.count('class="cycle-stage"') == 4
    positions = [home.index(name) for _, name in CANONICAL_THEME_ORDER]
    assert positions == sorted(positions)
    for theme in research_scope()["themes"]:
        assert HOME_THEME_PROPOSITIONS[theme["id"]] in home
        assert theme["guiding_question"] not in home
        assert theme["homepage_description"] not in home
        assert f"Explore this question: {theme['name']}" in home


def test_theme_pages_have_lighter_scaffolding_and_preserve_data() -> None:
    generate_all()
    for theme in research_scope()["themes"]:
        page = (ROOT / "research" / f"{theme['id']}.qmd").read_text()
        assert theme["guiding_question"] in page
        assert all(paragraph in page for paragraph in theme["long_description"])
        assert page.count("**The proposition.**") == 1
        assert "**What this theme does not assume.**" in page
        assert "## Questions the lab investigates" not in page
        assert "Place in the learning cycle" not in page
        assert page.index("## Questions this theme opens") < page.index("## How this connects") < page.index("## Current Conversations")
        for field in ("included_questions", "cycle_role", "connection_to_next", "what_this_changes", "analytical_boundary"):
            assert field in theme


def test_idea_hierarchy_public_tags_and_status() -> None:
    ideas = load_records("data/research-ideas")
    assert len(ideas) == 24 and validate_all() == []
    for theme_id, _ in CANONICAL_THEME_ORDER:
        subset = sorted((item for item in ideas if item["theme_id"] == theme_id), key=lambda x: x["display_order"])
        assert [item["narrative_tier"] for item in subset].count("signature") == 2
        assert [item["narrative_tier"] for item in subset].count("additional") == 4
    for item in ideas:
        assert 1 <= len(item["public_method_tags"]) <= 3
        assert set(item["public_method_tags"]) <= set(item["suggested_methods"])
        assert item["disclaimer"] == "Research idea · not currently an active or funded project"
    expected = {
        "geographies-of-climate-learning": {"When similarity misleads", "Evidence in translation"},
        "where-new-evidence-matters": {"The next city worth studying", "When is there enough evidence?"},
        "modes-of-climate-delivery": {"Same policy, different delivery", "Failure after adoption"},
        "consequences-for-people-and-places": {"The cumulative burden of policy packages", "Delivery-contingent co-benefits"},
    }
    for theme_id, titles in expected.items():
        assert {item["working_title"] for item in ideas if item["theme_id"] == theme_id and item["narrative_tier"] == "signature"} == titles


def test_idea_public_copy_preserves_qualifications_and_exclusion() -> None:
    generate_all()
    pages = "\n".join((ROOT / "research" / f"{theme}.qmd").read_text() for theme, _ in CANONICAL_THEME_ORDER)
    assert "Questions at the centre of this theme" in pages
    assert "Additional directions" in pages
    assert "not a ranking of research priority, funding readiness or importance" in pages
    assert "developed with appropriate Indigenous or community partners" in pages
    assert "not a proposal for a single public city-ranking" in pages
    for forbidden in (ROOT / "generated/work.qmd", ROOT / "generated/publications-selected.qmd", ROOT / "generated/current-conversations-feed.qmd"):
        assert "Research idea" not in forbidden.read_text()


def test_work_landing_and_all_detail_arguments() -> None:
    generate_all()
    landing = (ROOT / "work.qmd").read_text()
    assert 'title: "Work"' in landing and "Ongoing and foundational research across the four themes" in landing
    assert "invented parent" not in landing and "data model" not in landing
    for work in load_records("data/work"):
        page = (ROOT / "work" / f"{work['work_id']}.qmd").read_text()
        headings = ["## The problem", "## What this work asks", "## How the work investigates it", "## What better understanding could make possible", "## Evidence status and boundaries"]
        assert [page.index(h) for h in headings] == sorted(page.index(h) for h in headings)
        assert page.count("Primary theme") == 1
        assert "Work at a glance" in page
        if any(source.get("url") and source.get("source_type") == "public-web" for source in work["authoritative_sources"]):
            assert "## Authoritative sources" in page
        for field in ("problem_of_understanding", "central_question", "how_it_investigates", "reader_value", "evidence_status", "claim_boundaries"):
            assert work[field] in page
        if work["work_status"] == "ongoing":
            assert not re.search(r"\b(proves|demonstrates|has shown)\b", work["reader_value"], re.I)


def test_our_approach_is_six_state_and_hypothetical() -> None:
    source = (ROOT / "research/our-approach.qmd").read_text()
    assert "linear path from evidence to action" in source
    ordered = source.split('<ol class="approach-states">', 1)[1].split("</ol>", 1)[0]
    assert ordered.count("<li>") == 6
    assert "This is a hypothetical illustration of the four questions, not a finding or policy recommendation." in source
    assert "transferability score" not in source and "rank cities" not in source
    assert all(commitment in source for commitment in ("Contextual relevance", "Evidence status", "Indigenous knowledge", "universal best practices"))


def test_current_conversations_problem_state_and_no_public_fixture() -> None:
    landing = (ROOT / "current-conversations/index.qmd").read_text()
    methods = (ROOT / "current-conversations/how-it-works.qmd").read_text()
    assert "Discussion of urban climate evidence is dispersed" in landing
    assert "In development" in landing and "The live feed is not yet enabled" in landing
    assert "visibility as evidence quality, endorsement or applicability" in landing
    for forbidden in ("watch-filters", "data-conversation-count", "feed.json", "feed.xml", "last-updated"):
        assert forbidden not in landing
    assert "dispersed across source environments" in methods


def test_previous_work_gate_5f_proposal_remains_private_historical_evidence() -> None:
    fixture = yaml.safe_load((ROOT / "tests/fixtures/gate-5d-previous-work-freeze.yml").read_text())
    assert fixture["selected_previous_work"]
    proposal = (ROOT / "docs/reviews/gate-5f/previous-work-reader-value-proposal.md").read_text()
    assert "not implemented" in proposal.casefold()
    assert "previous-work-reader-value-proposal" not in (ROOT / "_quarto.yml").read_text()


def test_no_network_paid_or_staging_side_effect_and_pages_is_manual() -> None:
    makefile = (ROOT / "Makefile").read_text()
    normal = makefile.split("build: generate", 1)[1].split("linkcheck:", 1)[0] + (ROOT / "scripts/pre-render.sh").read_text()
    assert not any(value in normal for value in ("curl ", "OPENAI_API_KEY", "discover", "benchmark", "staging-write"))
    workflows = "\n".join(path.read_text() for path in (ROOT / ".github/workflows").glob("*.yml"))
    pages = (ROOT / ".github/workflows/public-draft-pages.yml").read_text()
    assert "quarto publish" not in workflows
    assert "workflow_dispatch" in pages and "PUBLIC_DRAFT_DEPLOY_ENABLED" in pages
    site = yaml.safe_load((ROOT / "config/site.yml").read_text())
    assert site["current_conversations"] == {"status": "in-development", "public_feed_enabled": False}


def test_gate_5f_audits_are_complete() -> None:
    required = {
        "homepage-reader-value-audit.md",
        "theme-public-scaffolding-audit.md",
        "research-idea-display-audit.md",
        "work-page-reader-value-audit.md",
        "our-approach-and-illustration-audit.md",
        "current-conversations-reader-problem-audit.md",
        "previous-work-reader-value-proposal.md",
    }
    assert required <= {path.name for path in (ROOT / "docs/reviews/gate-5f").glob("*.md")}
    assert (ROOT / "docs/adr/0006-site-level-reader-value-and-public-scaffolding.md").is_file()
    assert (ROOT / "docs/editorial/site-level-reader-value.md").is_file()
