from __future__ import annotations

import json
import re
from html.parser import HTMLParser

import yaml

from scripts.content import ROOT, load_records
from scripts.generate_site import HOME_THEME_PROPOSITIONS, generate_all
from scripts.validate_content import CANONICAL_THEME_ORDER, validate_all


class VisibleText(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hidden_depth = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style"}:
            self.hidden_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"} and self.hidden_depth:
            self.hidden_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self.hidden_depth:
            self.parts.append(data)


def visible_site_text(site_name: str = "_site") -> str:
    values: list[str] = []
    for page in sorted((ROOT / site_name).rglob("*.html")):
        parser = VisibleText()
        parser.feed(page.read_text(errors="ignore"))
        values.append(" ".join(parser.parts))
    return "\n".join(values)


def featured() -> list[dict]:
    return yaml.safe_load((ROOT / "config/theme_featured_examples.yml").read_text())["entries"]


def test_settled_gate_5f_public_decisions_remain_exact() -> None:
    home = (ROOT / "index.qmd").read_text()
    assert "Urban climate evidence does not become useful merely because it exists." in home
    assert all(value in (ROOT / "generated/home-themes.qmd").read_text() for value in HOME_THEME_PROPOSITIONS.values())
    assert all(value in home for value in ("For researchers", "For policy and practice", "For prospective students and collaborators"))
    assert len(load_records("data/research-ideas")) == 24
    approach = (ROOT / "research/our-approach.qmd").read_text()
    assert approach.split('<ol class="approach-states">', 1)[1].split("</ol>", 1)[0].count("<li>") == 6
    assert "Hypothetical illustration" in approach


def test_curated_examples_are_bounded_supported_ordered_and_not_mdpi() -> None:
    assert validate_all() == []
    entries = featured()
    complete = json.loads((ROOT / "reports/content/publication-complete-inventory.json").read_text())["records"]
    complete_by_id = {item["record_id"]: item for item in complete}
    for theme_id, _ in CANONICAL_THEME_ORDER:
        selected = [item for item in entries if item["theme_id"] == theme_id]
        assert 4 <= len(selected) <= 6
        page = (ROOT / "research" / f"{theme_id}.qmd").read_text()
        section = page.split("## Selected completed and foundational work", 1)[1].split("## Questions this theme opens", 1)[0]
        observed = re.findall(r'data-record-id="([^\"]+)"', section)
        assert observed == [item["record_id"] for item in selected]
        assert "Explore all verified publications and outputs related to this theme" in section
        for item in selected:
            assert item["evidence_reviewed"] and 20 <= len(item["contribution"].split()) <= 65
            assert item["contribution"] in section
            if item["record_type"] == "publication":
                assert not complete_by_id[item["record_id"]].get("mdpi_excluded")
    appearances: dict[tuple[str, str], int] = {}
    for item in entries:
        key = (item["record_type"], item["record_id"])
        appearances[key] = appearances.get(key, 0) + 1
    assert max(appearances.values()) <= 2


def test_curation_does_not_delete_or_duplicate_complete_bibliography() -> None:
    inventory = json.loads((ROOT / "reports/content/publication-complete-inventory.json").read_text())["records"]
    assert len(inventory) == 46
    assert len({item["record_id"] for item in inventory}) == 46
    assert len({item["doi"].casefold() for item in inventory if item.get("doi")}) == len([item for item in inventory if item.get("doi")])
    assert any(item["record_id"] == "from-urban-climate-ambition-to-delivery" for item in inventory)


def test_public_contributions_are_conceptual_not_source_audit_copy() -> None:
    forbidden = ("publisher abstract", "institutional full-text record", "verified relationship", "evidence source", "based on https")
    assert all(not any(term in item["contribution"].casefold() for term in forbidden) for item in featured())
    internal = yaml.safe_load((ROOT / "config/publication_theme_examples.yml").read_text())
    assert all(rel["evidence_source"].startswith("https://") and rel["rationale"] for item in internal["records"] for rel in item["theme_relationships"])


def test_public_copy_has_no_internal_gate_language_or_machine_slugs() -> None:
    text = visible_site_text().casefold()
    for forbidden in ("gate 5", "owner-approved", "owner review package", "owner-review package", "handoff package", "record id", " yaml ", "codex"):
        assert forbidden not in text
    for raw in ("united-kingdom", "comparative-case-study", "institutional-analysis", "urban-infrastructure", "canada, global"):
        assert raw not in text
    for label in ("United Kingdom", "Comparative case study", "Institutional analysis", "Urban infrastructure", "Cross-sectoral", "Canada; Global"):
        assert label in visible_site_text()


def test_public_work_sources_are_public_and_internal_decisions_remain_stored() -> None:
    generate_all()
    for work in load_records("data/work"):
        page = (ROOT / "work" / f"{work['work_id']}.qmd").read_text()
        for source in work["authoritative_sources"]:
            if source["source_type"] == "owner-approved-programme":
                assert source["label"] not in page
            elif source.get("url"):
                assert source["url"] in page
    stored = "\n".join(path.read_text() for path in (ROOT / "data/work").glob("*.yml"))
    assert "owner-approved-programme" in stored


def test_internal_placeholders_are_explicitly_non_public() -> None:
    scope = yaml.safe_load((ROOT / "config/research_scope.yml").read_text())
    titles = [example["title"] for theme in scope["themes"] for example in theme["representative_placeholder_examples"]]
    assert titles and all(example["public"] is False for theme in scope["themes"] for example in theme["representative_placeholder_examples"])
    public = visible_site_text()
    assert all(title not in public for title in titles)
    assert not re.search(r"\b(TBC|TBD|lorem|sample project)\b", public, re.I)


def test_project_path_profile_and_generated_paths_are_portable() -> None:
    profile = yaml.safe_load((ROOT / "_quarto-project-path.yml").read_text())
    assert profile["website"]["site-path"] == "/CCL-Lab-Website/"
    assert profile["project"]["output-dir"] == "_site-project-path/CCL-Lab-Website"
    assert "example.com" not in (ROOT / "_quarto.yml").read_text()
    assert "site-path" not in yaml.safe_load((ROOT / "_quarto.yml").read_text())["website"]
    makefile = (ROOT / "Makefile").read_text()
    assert "test: build build-project-path" in makefile
    assert "check: validate build build-project-path" in makefile


def test_pages_workflow_is_manual_fail_closed_and_permission_isolated() -> None:
    workflow = (ROOT / ".github/workflows/public-draft-pages.yml").read_text()
    trigger = workflow.split("permissions:", 1)[0]
    assert "workflow_dispatch:" in trigger
    assert not any(value in trigger for value in ("push:", "pull_request:", "schedule:", "workflow_run:"))
    assert "PUBLIC_DRAFT_DEPLOY_ENABLED" in workflow and "confirm_draft_0_1" in workflow
    assert "name: public-draft" in workflow
    build = workflow.split("  build:", 1)[1].split("  deploy:", 1)[0]
    deploy = workflow.split("  deploy:", 1)[1]
    assert "contents: read" in build and "pages: write" not in build and "id-token: write" not in build
    assert "pages: write" in deploy and "id-token: write" in deploy
    assert "make linkcheck-project-path" in build


def test_current_conversations_and_draft_boundary_remain_closed() -> None:
    config = yaml.safe_load((ROOT / "config/site.yml").read_text())
    assert config == {"site_status": "draft", "site_version": "0.1", "current_conversations": {"status": "in-development", "public_feed_enabled": False}}
    landing = (ROOT / "current-conversations/index.qmd").read_text()
    assert "In development" in landing and "live feed is not yet enabled" in landing
    assert not list((ROOT / "current-conversations").glob("*.json"))
    assert not list((ROOT / "current-conversations").glob("*.xml"))
