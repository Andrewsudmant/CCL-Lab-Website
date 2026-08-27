from __future__ import annotations

import json

import yaml

from current_conversations.run import ACTIVE_QUERY_PACK, query_for
from scripts.content import ROOT, load_records, research_scope
from scripts.generate_site import generate_all
from scripts.validate_content import CANONICAL_THEME_ORDER, validate_all


THEME_IDS = [item[0] for item in CANONICAL_THEME_ORDER]


def load_pack() -> dict:
    return yaml.safe_load(ACTIVE_QUERY_PACK.read_text(encoding="utf-8"))


def all_queries(pack: dict) -> list[dict]:
    return [query for group in pack["queries"].values() for query in group]


def test_gate_5c_active_pack_is_versioned_and_v1_is_preserved() -> None:
    pack = load_pack()
    assert ACTIVE_QUERY_PACK.name == "current-conversations-v2.yml"
    assert pack["query_pack_id"] == "current-conversations-v2"
    assert pack["version"] == "3.0.0"
    assert pack["supersedes"] == "current-conversations-v1@2.0.0"
    assert (ROOT / "config/query_packs/current-conversations-v1.yml").is_file()
    assert not validate_all()


def test_query_types_separate_theme_intent_from_facets() -> None:
    queries = all_queries(load_pack())
    assert queries
    assert all(query["classification_required"] is True for query in queries)
    assert all(set(query["facets"]) == {"geographies", "sectors", "methods", "climate_domains"} for query in queries)
    assert all(query["theme_intent"] in THEME_IDS for query in queries if query["query_type"] == "theme")
    assert all(query["theme_intent"] is None for query in queries if query["query_type"] in {"facet", "exploratory"})
    assert query_for("openalex", "cc3-a01-geographies")["classification_required"] is True
    assert query_for("openai_web_search", "cc3-w05-tools-facet")["theme_intent"] is None


def test_tools_datasets_and_models_do_not_force_theme_two() -> None:
    tool_queries = [query for query in all_queries(load_pack()) if "tools-facet" in query["id"]]
    assert len(tool_queries) == 4
    assert all(query["query_type"] == "facet" for query in tool_queries)
    assert all(query["theme_intent"] is None for query in tool_queries)
    assert all(set(query["candidate_themes"]) == set(THEME_IDS) for query in tool_queries)


def test_workforce_is_a_facet_and_not_automatically_theme_four() -> None:
    workforce = [query for query in all_queries(load_pack()) if "workforce-facet" in query["id"]]
    assert len(workforce) == 3
    assert all(query["theme_intent"] is None for query in workforce)
    assert all(query["facets"]["sectors"] == ["labour-workforce"] for query in workforce)
    assert all("modes-of-climate-delivery" in query["candidate_themes"] for query in workforce)


def test_canada_and_british_columbia_are_geographical_facets_across_questions() -> None:
    queries = all_queries(load_pack())
    canadian = [query for query in queries if set(query["facets"]["geographies"]) & {"canada", "british-columbia"}]
    intents = {query["theme_intent"] for query in canadian}
    assert set(THEME_IDS) <= intents
    assert None in intents
    assert all("canada" not in query["id"] or query["theme_intent"] != "modes-of-climate-delivery" or "delivery" in query["id"] for query in canadian)


def test_theme_two_queries_name_consequential_evidence_value() -> None:
    queries = [query for query in all_queries(load_pack()) if query["theme_intent"] == "where-new-evidence-matters"]
    assert queries
    required = ("consequential", "value of", "could change", "evaluation priorit", "research priorit")
    assert all(any(term in query["query"].casefold() for term in required) for query in queries)
    forbidden_direct = {"new climate data tool", "municipal dashboard", "decision support platform", "urban climate dataset"}
    assert not any(query["query"].casefold() in forbidden_direct for query in queries)


def test_source_environment_never_determines_one_theme() -> None:
    by_environment: dict[str, set[str | None]] = {}
    for query in all_queries(load_pack()):
        by_environment.setdefault(query["source_environment"], set()).add(query["theme_intent"])
    assert len(by_environment["academic-research"]) >= 5
    assert len(by_environment["policy-and-institutions"]) >= 4
    assert by_environment["bluesky"] == {None}


def test_classifier_prompt_distinguishes_theme_one_and_two_and_permits_null() -> None:
    prompt = (ROOT / "prompts/current-conversations-classification-v1.md").read_text(encoding="utf-8")
    for required in (
        "An evidence gap alone is not Theme 2",
        "A new dataset alone is not Theme 2",
        "A new tool alone is not Theme 2",
        "Geography, sector, method, source environment and output type are facets",
        "null classification is valid",
        "Classification is not an evidence-quality judgement",
        "transferability assessment",
        "policy recommendation",
    ):
        assert required in prompt


def test_unclassified_fixtures_remain_unforced_and_non_ai_disclosure_is_truthful() -> None:
    generate_all()
    clusters = [json.loads(path.read_text(encoding="utf-8")) for path in sorted((ROOT / "data/current-conversations/generated/clusters").glob("*.json"))]
    unclassified = {record["cluster_id"] for record in clusters if record["primary_theme"] is None}
    assert {"ccc-el-nino-urban-heat", "ccc-france-heat-drought", "ccc-reuters-climate-monitor"} <= unclassified
    assert all(record["ai_provenance"]["used"] is False for record in clusters)
    feed = (ROOT / "generated/current-conversations-feed.qmd").read_text(encoding="utf-8")
    assert "Identified and summarized using AI" not in feed
    assert "no AI generation recorded" in feed
    assert "Cross-cutting or not classified by lab theme" in feed


def test_current_conversations_disclosure_and_lab_source_separation() -> None:
    landing = (ROOT / "current-conversations/index.qmd").read_text(encoding="utf-8")
    exact = "Items are collected, classified and summarised automatically to show where the lab’s topics are being discussed. Inclusion does not indicate endorsement, evidential quality or applicability to a particular city."
    assert exact in landing
    assert "validated evidence base" in landing
    assert "not evidence of a live retrieval" in landing
    home = (ROOT / "index.qmd").read_text(encoding="utf-8")
    assert home.index("Featured work") < home.index("External horizon scanning")
    assert "Lab research" in home
    assert "External horizon scanning" in home


def test_public_theme_registry_has_four_equal_intellectual_stages() -> None:
    themes = research_scope()["themes"]
    assert [(item["id"], item["name"]) for item in themes] == CANONICAL_THEME_ORDER
    assert all("portfolio_maturity" not in item for item in themes)
    generate_all()
    principal = "\n".join(
        (ROOT / path).read_text(encoding="utf-8")
        for path in ["index.qmd", "research.qmd", "generated/home-themes.qmd", "generated/research-themes.qmd"]
    )
    assert "theme-status" not in principal
    assert "Established" not in principal
    assert "Developing" not in principal


def test_research_work_records_are_canonical_and_match_owner_mapping() -> None:
    works = load_records("data/work")
    assert len(works) == len({work["work_id"] for work in works}) == 7
    mapping = {work["work_id"]: (work["primary_theme"], work["secondary_themes"]) for work in works}
    assert mapping == {
        "climate-delivery-modes": ("modes-of-climate-delivery", ["geographies-of-climate-learning"]),
        "coben-place-based-model": ("consequences-for-people-and-places", ["where-new-evidence-matters", "modes-of-climate-delivery"]),
        "data-methodologies-climate-impact": ("geographies-of-climate-learning", ["consequences-for-people-and-places"]),
        "geography-urban-climate-evidence": ("geographies-of-climate-learning", ["where-new-evidence-matters"]),
        "occupational-transition-requirements": ("consequences-for-people-and-places", ["where-new-evidence-matters", "modes-of-climate-delivery"]),
        "uk-co-benefits-atlas": ("consequences-for-people-and-places", ["geographies-of-climate-learning"]),
        "uk-co-benefits-atlas-tool": ("consequences-for-people-and-places", ["geographies-of-climate-learning"]),
    }
