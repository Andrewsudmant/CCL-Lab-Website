from __future__ import annotations

import json

from scripts.content import ROOT, load_records, research_scope
from scripts.generate_site import generate_all


THEMES = [
    ("geographies-of-climate-learning", "Geographies of Climate Learning"),
    ("where-new-evidence-matters", "Where New Evidence Matters"),
    ("modes-of-climate-delivery", "Modes of Climate Delivery"),
    ("consequences-for-people-and-places", "Consequences for People and Places"),
]


def test_exact_theme_titles_order_and_routes() -> None:
    generate_all()
    themes = research_scope()["themes"]
    assert [(item["id"], item["name"]) for item in themes] == THEMES
    assert len(themes) == 4
    assert themes[1]["portfolio_maturity"] == "developing"
    assert all("status" not in item for item in themes)
    for theme_id, _ in THEMES:
        assert (ROOT / "research" / f"{theme_id}.qmd").exists()


def test_learning_cycle_is_semantic_and_returns_to_evidence() -> None:
    fragment = (ROOT / "generated/home-themes.qmd").read_text()
    positions = [fragment.index(title) for _, title in THEMES]
    assert positions == sorted(positions)
    assert '<ol class="learning-cycle"' in fragment
    assert "Consequences generate further learning" in fragment
    assert "new evidence and revised judgements" in fragment


def test_homepage_establishes_programme_before_current_conversations() -> None:
    page = (ROOT / "index.qmd").read_text()
    assert "How cities find, generate and use evidence for climate action." in page
    assert page.index("Four connected questions") < page.index("Current Conversations")
    assert page.index("Featured projects and outputs") < page.index("Current Conversations")
    featured = [
        "projects/geography-urban-climate-evidence.html",
        "projects/climate-delivery-modes.html",
        "projects/coben-place-based-model.html",
    ]
    positions = [page.index(path) for path in featured]
    assert positions == sorted(positions)
    assert "UK Co-Benefits Atlas" in page


def test_public_theme_surfaces_do_not_show_portfolio_maturity_badges() -> None:
    generate_all()
    public_theme_sources = [
        ROOT / "generated/home-themes.qmd",
        ROOT / "generated/research-themes.qmd",
        *[ROOT / "research" / f"{theme_id}.qmd" for theme_id, _ in THEMES],
    ]
    visible = "\n".join(path.read_text() for path in public_theme_sources)
    assert "Established" not in visible
    assert "Developing" not in visible
    assert "theme-status" not in visible


def test_project_theme_relationships_and_optional_learning_fields() -> None:
    valid = {item[0] for item in THEMES}
    projects = load_records("data/projects")
    assert projects
    for project in projects:
        assert project["primary_theme"] in valid
        assert set(project["secondary_themes"]) <= valid
        assert project["primary_theme"] not in project["secondary_themes"]
        assert project.get("evidence_status")
        page = (ROOT / "projects" / f'{project["record_id"]}.qmd').read_text()
        assert "How this project contributes to climate learning" in page

    mapping = {record["record_id"]: record for record in projects}
    assert mapping["geography-urban-climate-evidence"]["primary_theme"] == "geographies-of-climate-learning"
    assert mapping["geography-urban-climate-evidence"]["secondary_themes"] == ["where-new-evidence-matters"]
    assert mapping["data-methodologies-climate-impact"]["primary_theme"] == "geographies-of-climate-learning"
    assert mapping["data-methodologies-climate-impact"]["secondary_themes"] == ["consequences-for-people-and-places"]
    assert mapping["climate-delivery-modes"]["secondary_themes"] == ["geographies-of-climate-learning"]
    assert mapping["coben-place-based-model"]["secondary_themes"] == ["where-new-evidence-matters", "modes-of-climate-delivery"]
    assert mapping["occupational-transition-requirements"]["secondary_themes"] == ["where-new-evidence-matters", "modes-of-climate-delivery"]
    atlas = mapping["uk-co-benefits-atlas"]
    assert atlas["primary_theme"] == "consequences-for-people-and-places"
    assert atlas["secondary_themes"] == ["geographies-of-climate-learning"]
    assert "consequential_uncertainty" not in atlas
    assert "next_learning_question" not in atlas
    atlas_page = (ROOT / "projects/uk-co-benefits-atlas.qmd").read_text()
    assert "**Consequential uncertainty:**" not in atlas_page
    assert "**Next learning question:**" not in atlas_page


def test_current_conversations_filters_disclosure_and_unclassified_state() -> None:
    page = (ROOT / "current-conversations/index.qmd").read_text()
    for theme_id, title in THEMES:
        assert f'value="{theme_id}"' in page
        assert title in page
    required = "Items are collected, classified and summarised automatically to show where the lab’s topics are being discussed. Inclusion does not indicate endorsement, evidential quality or applicability to a particular city."
    assert required in page
    assert '__unclassified__' in page
    clusters = [json.loads(path.read_text()) for path in (ROOT / "data/current-conversations/generated/clusters").glob("*.json")]
    assert any(item["primary_theme"] is None for item in clusters)
    generated = (ROOT / "generated/current-conversations-feed.qmd").read_text()
    assert "Cross-cutting or not classified by lab theme" in generated


def test_old_routes_are_transition_pages_and_internal_links_use_new_routes() -> None:
    old_ids = {
        "urban-climate-learning", "evidence-infrastructure-tools", "climate-governance-delivery",
        "co-benefits-place-based-valuation", "just-transitions-workforce", "canadian-climate-policy",
    }
    for old_id in old_ids:
        path = ROOT / "research/themes" / f"{old_id}.qmd"
        assert path.exists()
        assert "This former theme route has moved" in path.read_text()
    generated = "\n".join(path.read_text() for path in (ROOT / "generated").glob("*.qmd"))
    assert 'href="/research/themes/' not in generated


def test_obsolete_theme_titles_are_not_visible_in_current_site() -> None:
    obsolete = [
        "Urban climate learning and evidence transfer",
        "Climate governance and delivery modes",
        "Co-benefits, co-costs and place-based valuation",
        "Just transitions, occupations and workforce change",
        "Urban climate evidence infrastructure and decision-support tools",
        "Canadian climate policy",
    ]
    current_sources = [ROOT / "index.qmd", ROOT / "research.qmd", ROOT / "current-conversations/index.qmd"]
    current_sources += list((ROOT / "research").glob("*.qmd"))
    visible = "\n".join(path.read_text() for path in current_sources)
    assert not any(label in visible for label in obsolete)
