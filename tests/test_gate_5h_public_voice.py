from __future__ import annotations

import hashlib
import json
import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from scripts.content import ROOT, load_records, research_scope
from scripts.generate_site import HOME_THEME_PROPOSITIONS, THEME_PRACTICAL_EXAMPLES, generate_all
from scripts.validate_content import CANONICAL_THEME_ORDER


class MainText(HTMLParser):
    def __init__(self) -> None:
        super().__init__(); self.depth = 0; self.hidden = 0; self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "main": self.depth += 1
        if tag in {"script", "style", "noscript"}: self.hidden += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript"} and self.hidden: self.hidden -= 1
        if tag == "main" and self.depth: self.depth -= 1

    def handle_data(self, data: str) -> None:
        if self.depth and not self.hidden: self.parts.append(data)


def digest(pattern: str) -> str:
    value = hashlib.sha256()
    for path in sorted(ROOT.glob(pattern)):
        value.update(path.name.encode()); value.update(path.read_bytes())
    return value.hexdigest()


def page(theme_id: str) -> str:
    return (ROOT / "research" / f"{theme_id}.qmd").read_text()


def test_01_10_fixed_content_is_preserved() -> None:
    # 1–3: titles, order, relationships and complete theme registry.
    assert [(x["id"], x["name"]) for x in research_scope()["themes"]] == CANONICAL_THEME_ORDER
    assert hashlib.sha256((ROOT / "config/research_scope.yml").read_bytes()).hexdigest() == "35bdaee34a658bfc8a1eec9ab1d9fe85feee72efe684de9e95159dec90bab13c"
    # 4–5: all idea questions and signature assignments remain byte-for-byte fixed.
    assert digest("data/research-ideas/*.yml") == "7b2b4ff6b346549fd3225e8a4815a76a38057bf24045910e7f04b0176def1d2f"
    # 6–7: selected IDs and within-theme order remain fixed while contribution prose may change.
    selected = [(x["theme_id"], x["record_type"], x["record_id"]) for x in yaml.safe_load((ROOT / "config/theme_featured_examples.yml").read_text())["entries"]]
    expected = [
        ("geographies-of-climate-learning", "publication", "replicate-generalize-urban-research"),
        ("geographies-of-climate-learning", "publication", "using-crowdsourced-data-to-estimate-the-carbon-footprints-of-global-cities"),
        ("geographies-of-climate-learning", "publication", "producer-cities-and-consumer-cities-using-production-and-consumption-based-carbon-accounts"),
        ("geographies-of-climate-learning", "work", "data-methodologies-climate-impact"),
        ("geographies-of-climate-learning", "publication", "integration-mitigation-adaptation-europe"),
        ("geographies-of-climate-learning", "work", "uk-co-benefits-atlas"),
        ("where-new-evidence-matters", "publication", "replicate-generalize-urban-research"),
        ("where-new-evidence-matters", "publication", "data-scaling-climate-action-governance-uk"),
        ("where-new-evidence-matters", "publication", "fair-weather-forecasting-the-shortcomings-of-big-data-for-sustainable-development-a-case-s"),
        ("where-new-evidence-matters", "publication", "uncovering-blind-spots-in-urban-carbon-management-the-role-of-consumption-based-carbon-acc"),
        ("modes-of-climate-delivery", "publication", "infrastructure-transitions-southern-cities"),
        ("modes-of-climate-delivery", "publication", "missing-the-target-are-local-climate-targets-aligned-with-national-net-zero-ambitions"),
        ("modes-of-climate-delivery", "publication", "supportive-governance-for-city-scale-low-carbon-building-retrofits-a-case-study-from-shang"),
        ("modes-of-climate-delivery", "publication", "financing-climate-action-with-positive-social-impact-how-banking-can-support-a-just-transi"),
        ("modes-of-climate-delivery", "publication", "integration-mitigation-adaptation-europe"),
        ("modes-of-climate-delivery", "publication", "low-carbon-cities-affordable"),
        ("consequences-for-people-and-places", "work", "uk-co-benefits-atlas"),
        ("consequences-for-people-and-places", "publication", "climate-policy-social-policy"),
        ("consequences-for-people-and-places", "publication", "the-social-environmental-health-and-economic-impacts-of-low-carbon-transport-policy-a-revi"),
        ("consequences-for-people-and-places", "publication", "workers-perceptions-of-climate-change-and-the-green-transition-in-yorkshire-and-the-humber"),
        ("consequences-for-people-and-places", "publication", "can-low-carbon-urban-development-be-pro-poor-the-case-of-kolkata-india"),
        ("consequences-for-people-and-places", "publication", "financing-climate-action-with-positive-social-impact-how-banking-can-support-a-just-transi"),
    ]
    assert selected == expected
    # 8–9: publication inventory and complete Work source records are untouched.
    assert hashlib.sha256((ROOT / "reports/content/publication-complete-inventory.json").read_bytes()).hexdigest() == "5626e6b7d08e7159a138d3a34dc2defff787cb22a0b650c595494c77cf9ef801"
    assert digest("data/work/*.yml") == "549e239b19ccf17a45e81f1d48bccd02f385ea0b8023dfaf6adcea03f8eecd20"
    # 10: Current Conversations remains closed.
    assert yaml.safe_load((ROOT / "config/site.yml").read_text())["current_conversations"] == {"status": "in-development", "public_feed_enabled": False}


def test_11_18_homepage_voice_routes_and_word_count() -> None:
    source = (ROOT / "index.qmd").read_text()
    assert "Cities learn from one another. The hard part is knowing what can travel." in source
    assert "How cities find, generate and use evidence for climate action." in source
    assert "The Cities and Climate Learning Lab studies these connections" in source
    assert all(copy in (ROOT / "generated/home-themes.qmd").read_text() for copy in HOME_THEME_PROPOSITIONS.values())
    assert not all(old in source for old in ("does not by itself", "not simply", "not merely", "not only"))
    assert all(x in source for x in ("For researchers", "For policy and practice", "For prospective students and collaborators", "Featured work", "contact.html"))
    parser = MainText(); parser.feed((ROOT / "_site/index.html").read_text())
    words = re.findall(r"[A-Za-z0-9]+(?:[’'&-][A-Za-z0-9]+)*", " ".join(parser.parts))
    assert 542 <= len(words) <= 614  # 15–25% below the documented 722-word baseline.


def test_19_25_theme_openings_preserve_argument_and_mark_examples() -> None:
    generate_all()
    for theme in research_scope()["themes"]:
        text = page(theme["id"])
        assert "A practical example" in text and THEME_PRACTICAL_EXAMPLES[theme["id"]] in text
        assert text.index("A practical example") < text.index(theme["long_description"][0])
        assert all(value in text for value in theme["long_description"])
        assert theme["what_this_changes"] in text and theme["analytical_boundary"] in text
        assert text.index("## Current Conversations") > text.index("## How this connects")
        assert "finding" not in text.split("::: {.practical-example}", 1)[1].split(":::", 1)[0].casefold()


def test_26_35_idea_cards_are_lighter_without_losing_source_fields() -> None:
    ideas = load_records("data/research-ideas")
    assert len(ideas) == 24
    for theme_id, _ in CANONICAL_THEME_ORDER:
        subset = [x for x in ideas if x["theme_id"] == theme_id]
        assert len(subset) == 6 and sum(x["narrative_tier"] == "signature" for x in subset) == 2
        text = page(theme_id)
        assert text.count('class="idea-card') == 6
        assert text.count("One possible approach") == 6
        assert "<h4>Why this question matters</h4>" not in text and "<h4>How we might study it</h4>" not in text
        assert all(len(x["public_method_tags"]) <= 3 and x["suggested_methods"] for x in subset)
    joined = "\n".join(page(x) for x, _ in CANONICAL_THEME_ORDER)
    assert "developed with appropriate Indigenous or community partners" in joined
    assert "not a proposal for a single public city-ranking" in joined
    assert joined.count("Research idea · not currently an active or funded project") >= 28
    assert "Research idea" not in (ROOT / "generated/current-conversations-feed.qmd").read_text()


def test_36_45_work_pages_use_four_supported_public_structures() -> None:
    structures = {
        "research-programme": ("## Why this work began", "## What we are trying to understand", "## Where the work stands"),
        "research-line": ("## Why this work began", "## What we are trying to understand", "## Where the work stands"),
        "paper": ("## The question", "## What the paper examines", "## Evidence and status"),
        "project": ("## The problem the project addressed", "## What the project produced", "## Limits and context"),
        "tool": ("## What the tool shows", "## How it can be used", "## What users should not infer"),
    }
    for work in load_records("data/work"):
        text = (ROOT / "work" / f"{work['work_id']}.qmd").read_text()
        assert all(h in text for h in structures[work["work_type"]])
        assert work["evidence_status"] in text and work["claim_boundaries"] in text
        assert text.count("<dt>Main theme</dt>") == 1
        panel = text.split('<section class="work-at-a-glance"', 1)[1].split("</section>", 1)[0]
        assert all(label in panel for label in ("Work type", "Status", "Main theme", "Geographical focus", "Key methods"))
        assert not any(label in panel for label in ("Secondary themes", "Climate domains", "Sectors", "Relationship to the lab"))
        if work["work_status"] == "ongoing": assert not re.search(r"\b(proves|demonstrates|has shown)\b", text, re.I)


def test_46_50_approach_starts_with_example_and_keeps_six_states() -> None:
    text = (ROOT / "research/our-approach.qmd").read_text()
    assert text.index("## Illustration: expanding active travel") < text.index("## Where urban climate learning can break down")
    assert "This is a hypothetical illustration of the four questions, not a finding or policy recommendation." in text
    assert text.split('<ol class="approach-states">', 1)[1].split("</ol>", 1)[0].count("<li>") == 6
    assert all(value in text for value in ("produce evidence", "judge relevance", "choose new evidence", "organise delivery", "experience consequences", "revise later decisions"))
    assert "transferability score" not in text and "recommend active travel" not in text.casefold()


def test_51_55_current_conversations_is_plain_closed_and_offline() -> None:
    landing = (ROOT / "current-conversations/index.qmd").read_text()
    assert "New work on cities and climate appears in many places" in landing
    assert "In development" in landing and "The live feed is not yet enabled" in landing
    assert "Appearing here will not mean that the lab endorses a source" in landing
    assert not any(x in landing for x in ("watch-filters", "data-conversation-count", "feed.json", "feed.xml", "last-updated"))
    assert not list((ROOT / "current-conversations").glob("*.json")) and not list((ROOT / "current-conversations").glob("*.xml"))


def test_56_61_diagnostic_and_term_map_are_deterministic_advisory_only() -> None:
    term_map = yaml.safe_load((ROOT / "config/plain_language_terms.yml").read_text())
    schema = json.loads((ROOT / "schemas/plain-language-terms.schema.json").read_text())
    assert not list(Draft202012Validator(schema).iter_errors(term_map)) and len(term_map["terms"]) == 9
    tracked = [ROOT / "index.qmd", ROOT / "research/our-approach.qmd", ROOT / "current-conversations/index.qmd"]
    before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in tracked}
    command = [str(ROOT / ".venv/bin/python"), str(ROOT / "scripts/audit_public_voice.py")]
    subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    first = (ROOT / "reports/editorial/gate-5h-public-voice-diagnostic.md").read_bytes()
    subprocess.run(command, cwd=ROOT, check=True, capture_output=True, text=True)
    assert first == (ROOT / "reports/editorial/gate-5h-public-voice-diagnostic.md").read_bytes()
    assert before == {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in tracked}
    report = first.decode()
    assert all(heading in report for heading in ("Repeated four-word", "Repeated sentence openings", "Sentences over 30 words", "Abstract-noun series", "Repeated visible heading sequences", "Technical terms used before"))
    assert "not a readability score or an automatic release gate" in report and "None on mapped pages" in report
    assert "`evidence to action`: 1 — allow-listed" in report


def test_62_77_two_profiles_and_fail_closed_release_scaffolding_exist() -> None:
    make = (ROOT / "Makefile").read_text()
    assert "test: build build-project-path" in make and "check: validate build build-project-path" in make
    assert (ROOT / "_site/index.html").is_file() and (ROOT / "_site-project-path/CCL-Lab-Website/index.html").is_file()
    workflow = (ROOT / ".github/workflows/public-draft-pages.yml").read_text()
    assert "workflow_dispatch" in workflow and "PUBLIC_DRAFT_DEPLOY_ENABLED" in workflow
    assert "push:" not in workflow.split("permissions:", 1)[0]
    assert yaml.safe_load((ROOT / "config/site.yml").read_text())["site_status"] == "draft"
    assert (ROOT / "scripts/check_links.py").is_file() and (ROOT / "scripts/check_accessibility.py").is_file()
    assert (ROOT / "scripts/check_browser_qa_artifacts.py").is_file()
