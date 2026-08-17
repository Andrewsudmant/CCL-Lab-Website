from __future__ import annotations

import yaml

from scripts.content import ROOT


def test_required_navigation_pages_exist() -> None:
    config = yaml.safe_load((ROOT / "_quarto.yml").read_text(encoding="utf-8"))
    nav = config["website"]["navbar"]["left"]
    hrefs = {item["href"] for item in nav if "href" in item}
    hrefs |= {child["href"] for item in nav for child in item.get("menu", [])}
    required = {
        "research.qmd",
        "projects.qmd",
        "people.qmd",
        "publications.qmd",
        "current-conversations/index.qmd",
        "data-tools.qmd",
        "opportunities.qmd",
        "about-andrew.qmd",
        "contact.qmd",
        "outputs.qmd",
    }
    assert required <= hrefs
    assert (ROOT / "index.qmd").exists()
    for source in required:
        assert (ROOT / source).exists()


def test_site_does_not_configure_deployment() -> None:
    assert not (ROOT / ".openai/hosting.json").exists()
    workflow_text = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / ".github/workflows").glob("*.yml"))
    assert "quarto publish" not in workflow_text.lower()
    assert "pages: write" not in workflow_text.lower()
    assert "deploy-pages" not in workflow_text.lower()
