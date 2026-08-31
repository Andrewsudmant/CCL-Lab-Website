from __future__ import annotations

import hashlib
import html
import json
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit

import pytest

from scripts.content import ROOT, load_records, load_yaml
from scripts.check_links import parsed
from scripts.generate_site import GENERIC_PUBLICATION_SUMMARY, publication_relationship_label, publication_status_label

INVENTORY = ROOT / "reports/content/publication-complete-inventory.json"
RECORDS = json.loads(INVENTORY.read_text())["records"]
METHODS = "publications/metadata-and-sources.html"
PROFILES = [("_site", ""), ("_site-project-path/CCL-Lab-Website", "/CCL-Lab-Website")]


def resolved_links(site, relative, base):
    origin = f"https://local.invalid{base}/{relative}"
    return [urlsplit(urljoin(origin, link)).path + ("#" + urlsplit(link).fragment if urlsplit(link).fragment else "") for link in parsed(site / relative).links]


class Details(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_dl = False
        self.field = None
        self.buffer = []
        self.values = []

    def handle_starttag(self, tag, attrs):
        if tag == "dl" and dict(attrs).get("class") == "publication-details": self.in_dl = True
        if self.in_dl and tag in {"dt", "dd"}: self.field = tag; self.buffer = []

    def handle_data(self, data):
        if self.field: self.buffer.append(data)

    def handle_endtag(self, tag):
        if tag == self.field:
            self.values.append("".join(self.buffer)); self.field = None
        if tag == "dl": self.in_dl = False


def test_canonical_records_and_underlying_relationships_are_byte_frozen():
    # Covers identity, ordered authors, date/precision, DOI/other IDs, type/status,
    # relation values, source evidence, connected work, and selected-publication flags.
    assert len(RECORDS) == 46
    assert hashlib.sha256(INVENTORY.read_bytes()).hexdigest() == "5626e6b7d08e7159a138d3a34dc2defff787cb22a0b650c595494c77cf9ef801"
    assert hashlib.sha256((ROOT / "config/publication_theme_examples.yml").read_bytes()).hexdigest() == "661707342de6fa63ae12c461f7e81736add74ad6bacc561adc83463675d5f9df"
    for relative, expected in {
        "index.qmd": "a066b0f414644697b217bd3741d69364140cca68ae330558da8fde068b7fa9b1",
        "research/our-approach.qmd": "8ce997606c10030fc6e40bfa87c83e74d48a0306eed026210bf51ed1ea9ec13a",
        ".github/workflows/public-draft-pages.yml": "6a6d1e8affef4c48b37f770371ad195b0a51b7ed82e9998aa28f47e03ba93ebc",
    }.items():
        assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == expected


def test_only_the_approved_delivery_display_entry_changed():
    entries = load_yaml(ROOT / "config/theme_featured_examples.yml")["entries"]
    # Entire surviving entry objects, not merely IDs: Gate 5H minus the approved row.
    assert hashlib.sha256(json.dumps(entries, sort_keys=True, separators=(",", ":")).encode()).hexdigest() == "f591ae229e94335bcbab2058ab8403cda9f22e95aa398151063eb6b860e8c526"
    selected = [x for x in entries if x["theme_id"] == "modes-of-climate-delivery"]
    assert len(selected) == 5 and all(x["record_id"] != "low-carbon-cities-affordable" for x in selected)
    assert {x["conceptual_grouping"] for x in selected} == {"Authority and organisational capability", "Participation, implementation and institutional durability", "Finance, ownership and coordination"}
    record = next(x for x in RECORDS if x["record_id"] == "low-carbon-cities-affordable")
    assert record["featured"] and "modes-of-climate-delivery" in record["secondary_themes"]
    assert any(x["theme_id"] == "modes-of-climate-delivery" for x in record["theme_relationships"])


@pytest.mark.parametrize("site_name,base", PROFILES)
def test_every_publication_renders_exact_identity_status_and_routes(site_name, base):
    site = ROOT / site_name
    methods = site / METHODS
    assert methods.is_file()
    assert f'{base}/{METHODS}' in resolved_links(site, "publications.html", base)
    for record in RECORDS:
        page = site / "publications" / f'{record["record_id"]}.html'
        source = page.read_text()
        parser = Details(); parser.feed(source)
        details = dict(zip(parser.values[::2], parser.values[1::2]))
        assert details["Authors"] == html.unescape(", ".join(record["authors"]))
        assert details["Published"] == record["publication_date"]
        assert details["Venue or publisher"] == html.unescape(record["venue"])
        assert details["Output type"] == record["publication_type"].replace("-", " ").capitalize()
        assert details["Peer-review status"] == publication_status_label(record["peer_review_status"])
        if record.get("version"):
            assert details["Version"] == load_yaml(ROOT / "config/vocabularies.yml")["publication_versions"][record["version"]]
        if record["doi"]: assert details["DOI"] == record["doi"]
        else: assert "Stable identifier" in details
        assert html.unescape(record["title"]) in html.unescape(source)
        assert publication_relationship_label(record["relationship_to_lab"]) in source
        assert f'href="{html.escape(record["url"], quote=True)}"' in source
        links = resolved_links(site, f'publications/{record["record_id"]}.html', base)
        assert f'{base}/{METHODS}' in links
        assert f'{base}/{METHODS}#corrections' in links
        assert "No AI-generated bibliographic metadata is used" not in source
        assert "Dates are displayed only to the precision" not in source
        assert "Metadata sources:" not in source


def test_methods_page_explains_source_fidelity_status_and_corrections():
    text = (ROOT / "publications/metadata-and-sources.qmd").read_text()
    for required in ("Publication metadata and sources", "ORCID", "Crossref", "DataCite", "publisher records", "institutional repositories", "owner override", "ordered author lists", "day, a month or a year", "An AI model does not generate or rewrite bibliographic identity", "Conflicting provider values", "Peer-review status not verified", "correction or retraction", "Current lab output", "Work begun before CCLL and continuing", "Foundational prior work", "Associated collaboration", "andrew_sudmant@sfu.ca", "## Corrections"):
        assert required in text
    assert "Different sources supply different fields" in text
    assert "Short descriptions and thematic relationships are separate editorial annotations" in text


def test_only_distinctive_relationship_notes_and_real_descriptions_are_displayed():
    for record in RECORDS:
        source = (ROOT / "publications" / f'{record["record_id"]}.qmd').read_text()
        body = source.split("```{=html}", 1)[1]
        assert GENERIC_PUBLICATION_SUMMARY not in body
        assert "Verified work by Andrew Sudmant that predates" not in body
        assert "Verified work by Andrew Sudmant; the record does not imply" not in body
        if record["abstract_summary"] != GENERIC_PUBLICATION_SUMMARY:
            assert body.count(html.escape(html.unescape(record["abstract_summary"]), quote=True)) == 1
        if record["relationship_to_lab"] != "foundational-prior-work":
            assert html.escape(record["relationship_note"], quote=True) in body
        assert "description-meta:" in source


@pytest.mark.parametrize("site_name,base", PROFILES)
def test_complete_listing_and_search_retain_all_46_records(site_name, base):
    site = ROOT / site_name
    complete = (site / "publications/complete.html").read_text()
    assert complete.count('class="bibliography-entry"') == 46
    search = json.loads((site / "search.json").read_text())
    indexed = {item["href"].split("#")[0].removeprefix(base + "/").lstrip("/") for item in search}
    for record in RECORDS:
        route = f'publications/{record["record_id"]}.html'
        assert route in indexed
        assert resolved_links(site, "publications/complete.html", base).count(f'{base}/{route}') == 1
    assert METHODS in indexed
    delivery = (site / "research/modes-of-climate-delivery.html").read_text()
    assert delivery.count('class="record-card featured-example"') == 5
    assert 'data-record-id="low-carbon-cities-affordable"' not in delivery


def test_no_encoded_venue_leaks_or_unverified_theme_links():
    for record in RECORDS:
        source = (ROOT / "_site/publications" / f'{record["record_id"]}.html').read_text()
        assert "&amp;amp;" not in source
        if not record["theme_relationships"]: assert "Related research themes" not in source
        for work_id in record["connected_work_ids"]: assert f'/work/{work_id}.html' in source


def test_focus_styles_cover_all_native_controls_and_no_positive_tabindex():
    css = (ROOT / "styles.css").read_text()
    assert all(x + ":focus-visible" in css for x in ("a", "button", "input", "select", "textarea", "summary"))
    assert "outline: 3px solid var(--ccl-focus)" in css
    import re
    for page in (ROOT / "_site").rglob("*.html"):
        assert not re.search(r'tabindex=["\'][1-9]', page.read_text())


def test_manual_pages_workflow_remains_fail_closed_and_no_api_dependency():
    # BaseLoader preserves the YAML `on` key instead of interpreting it as bool.
    import yaml
    workflow = yaml.load((ROOT / ".github/workflows/public-draft-pages.yml").read_text(), Loader=yaml.BaseLoader)
    assert set(workflow["on"]) == {"workflow_dispatch"}
    assert workflow["on"]["workflow_dispatch"]["inputs"]["confirm_draft_0_1"]["default"] == "false"
    jobs = workflow["jobs"]
    assert jobs["build"]["permissions"] == {"contents": "read"}
    assert jobs["deploy"]["permissions"] == {"pages": "write", "id-token": "write"}
    assert jobs["deploy"]["environment"]["name"] == "public-draft"
    text = (ROOT / ".github/workflows/public-draft-pages.yml").read_text()
    assert 'test "$ENABLED" = "true"' in text and 'test "$CONFIRMED" = "true"' in text
    assert "assert config[\"site_status\"] == \"draft\"" in text
    assert "captured-fixture" in text and "public_feed_enabled" in text
    assert "path: _site-project-path/CCL-Lab-Website" in text
    assert "secrets." not in text and "OPENAI_API_KEY" not in text


def test_release_link_diagnostic_is_bounded_offline_and_does_not_follow_redirects(tmp_path):
    from scripts.check_release_external_links import NoRedirect, source_urls
    assert NoRedirect().redirect_request(None, None, 302, None, None, "https://example.org") is None
    page = tmp_path / "index.html"
    page.write_text('<a href="https://www.sfu.ca/">SFU</a>')
    assert source_urls(tmp_path) == ["https://www.sfu.ca/"]
    page.write_text('<a href="https://example.org/">Unapproved</a>')
    with pytest.raises(ValueError, match="Unapproved"):
        source_urls(tmp_path)
    page.write_text("".join(f'<a href="https://www.sfu.ca/{i}">Source</a>' for i in range(61)))
    with pytest.raises(ValueError, match="count"):
        source_urls(tmp_path)
