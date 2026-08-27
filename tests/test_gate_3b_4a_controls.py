from __future__ import annotations
import json
from pathlib import Path
import pytest
import yaml

from research_watch.adapters.base import AdapterError
from research_watch.adapters.openai_web import OpenAIWebSearchAdapter
from research_watch.cluster import cluster, diverse, event_key
from research_watch.models import DiscoveredItem
from research_watch.transaction import publish_transaction, recheck_status
from scripts.content import ROOT, load_records, research_scope


def all_public_sources() -> str:
    paths = list(ROOT.glob("*.qmd")) + list((ROOT / "research-watch").glob("*.qmd"))
    return "\n".join(p.read_text(encoding="utf-8") for p in paths)


def test_public_email_is_canonical() -> None:
    person = load_records("data/people")[0]
    assert person["email"] == "andrew_sudmant@sfu.ca"
    assert "andrew_sudmant@sfu.ca" in (ROOT / "contact.qmd").read_text()


def test_old_email_absent_from_public_sources() -> None:
    assert "asudmant@sfu.ca" not in all_public_sources()


def test_personal_owner_review_banner_absent() -> None:
    assert "owner review required" not in all_public_sources().lower()


def test_internal_docs_excluded_from_quarto_render() -> None:
    config = yaml.safe_load((ROOT / "_quarto.yml").read_text())
    rendered = config["project"]["render"]
    assert "docs/*.md" not in rendered and "docs/adr/*.md" not in rendered


def test_internal_docs_absent_from_built_site_and_search() -> None:
    assert not (ROOT / "_site/docs").exists()
    search = (ROOT / "_site/search.json").read_text(encoding="utf-8")
    assert "docs/architecture" not in search and "docs/security" not in search and "baseline-gate" not in search


def test_no_photo_is_supported() -> None:
    person = load_records("data/people")[0]
    assert person["image"] is None and person["image_rights_status"] == "not-supplied"


def test_homepage_watch_limit_and_disclosures() -> None:
    generated = (ROOT / "generated/home-current-conversations.qmd").read_text()
    assert generated.count('<article class="conversation-card') <= 6
    homepage = (ROOT / "index.qmd").read_text()
    assert "Inclusion does not indicate endorsement" in homepage
    assert "Captured fixture · no AI generation recorded" in generated


def test_publications_have_exact_relationship_and_provenance() -> None:
    pubs = load_records("data/publications")
    assert all(p["relationship_to_lab"] in {"current-ccll-work", "pre-ccll-work-continuing", "foundational-prior-work", "associated-collaboration"} for p in pubs)
    assert all(p["metadata_sources"] and p["last_verified_date"] and p["authoritative_sources"] for p in pubs)
    assert all("and collaborators" not in " ".join(p["authors"]).lower() for p in pubs)


def test_known_publication_truth_constraints() -> None:
    pubs = {p["record_id"]: p for p in load_records("data/publications")}
    assert pubs["data-scaling-climate-action-governance-uk"]["title"] == "Data Scaling: Implications for Climate Action and Governance in the UK"
    assert pubs["infrastructure-transitions-southern-cities"]["authors"] == ["Lucy Oates", "Andrew Sudmant"]
    assert all(p.get("doi") != "10.1038/s44284-025-00260-8" for p in pubs.values())
    assert all(p["date_precision"] in {"exact", "month", "year"} for p in pubs.values())
    dois = [p["doi"].lower() for p in pubs.values() if p["doi"]]
    assert len(dois) == len(set(dois))


def test_theme_statuses_and_separation() -> None:
    themes = {t["id"]: t for t in research_scope()["themes"]}
    assert all("portfolio_maturity" not in theme for theme in themes.values())
    for record in load_records("data/work") + load_records("data/publications"):
        assert record["primary_theme"] not in record["geographies"]


def test_canada_is_a_geography_not_a_theme() -> None:
    assert "canadian-climate-policy" not in {theme["id"] for theme in research_scope()["themes"]}
    assert "canada" in yaml.safe_load((ROOT / "config/vocabularies.yml").read_text())["geographies"]


def test_canonical_cross_listing_does_not_duplicate_records() -> None:
    projects = load_records("data/work")
    ids = [p["work_id"] for p in projects]
    assert len(ids) == len(set(ids))
    assert any(p["secondary_themes"] for p in projects)


def test_identifier_clustering_and_diversity() -> None:
    a = DiscoveredItem("Same work", "https://doi.org/10.1234/x", "A", "academic-paper", "2026-08-01", ["A"], "10.1234/x", abstract="evidence", evidence_types=["abstract"])
    b = DiscoveredItem("Coverage", "https://news.test/x", "B", "news-analysis", "2026-08-02", ["B"], "10.1234/x", abstract="coverage")
    principals, report = cluster([a, b])
    assert len(principals) == 1 and len(report[0]["members"]) == 2
    items = [DiscoveredItem(str(i), f"https://one.test/{i}", "A", "academic-paper", "2026-08-01") for i in range(3)]
    assert len(diverse(items, maximum=3, per_domain=2)) == 2


def test_missing_openai_configuration_fails_before_network(monkeypatch) -> None:
    for key in ("OPENAI_API_KEY", "OPENAI_MODEL", "OPENAI_MAX_COST_PER_RUN", "OPENAI_MAX_ITEMS_PER_RUN"):
        monkeypatch.delenv(key, raising=False)
    with pytest.raises(AdapterError, match="no OpenAI request"):
        OpenAIWebSearchAdapter().search("urban climate", "test", 1)


def test_transaction_commit_and_rollback(tmp_path: Path) -> None:
    target = tmp_path / "current"
    first = [{"record_id": "one", "publication": {"decision": "published"}}]
    publish_transaction(target, first, lambda p: None, "one")
    before = (target / "published/001-one.json").read_text()
    with pytest.raises(RuntimeError):
        publish_transaction(target, [{"record_id": "two"}], lambda p: (_ for _ in ()).throw(RuntimeError("fail")), "two")
    assert (target / "published/001-one.json").read_text() == before
    assert json.loads((target.parent / "failure-two.json").read_text())["last_known_good_preserved"] is True
    manifest = json.loads((target / "run-manifest.json").read_text())
    assert manifest["record_count"] == 1 and manifest["status"] == "validated"


@pytest.mark.parametrize(("status", "redirected", "expected"), [(404, False, "unavailable"), (200, True, "redirected"), (200, False, "available"), (None, False, "under-review")])
def test_recheck_states(status, redirected, expected) -> None:
    assert recheck_status(status, redirected) == expected


def test_raw_provider_payloads_and_secrets_are_not_tracked() -> None:
    tracked_text = "\n".join(p.read_text(errors="ignore") for base in (ROOT / "data", ROOT / "config") for p in base.rglob("*") if p.is_file())
    assert "sk-" not in tracked_text
    assert not list(ROOT.glob("**/raw-provider*"))


def test_pipeline_is_not_a_build_side_effect() -> None:
    makefile = (ROOT / "Makefile").read_text()
    build_recipe = makefile.split("build: generate", 1)[1].split("linkcheck:", 1)[0]
    assert "pilot" not in build_recipe and "discover" not in build_recipe


@pytest.mark.parametrize("route", ["index.qmd", "research.qmd", "work.qmd", "projects.qmd", "people.qmd", "outputs.qmd", "publications.qmd", "data-tools.qmd", "opportunities.qmd", "about-andrew.qmd", "contact.qmd", "current-conversations/index.qmd", "current-conversations/how-it-works.qmd", "research-watch/index.qmd", "research-watch/methods.qmd"])
def test_important_public_routes_remain(route: str) -> None:
    assert (ROOT / route).is_file()


@pytest.mark.parametrize("theme_id", ["geographies-of-climate-learning", "where-new-evidence-matters", "modes-of-climate-delivery", "consequences-for-people-and-places"])
def test_each_theme_page_is_generated(theme_id: str) -> None:
    assert (ROOT / "research" / f"{theme_id}.qmd").is_file()
