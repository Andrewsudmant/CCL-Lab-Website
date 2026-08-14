from research_watch.models import DiscoveredItem
from research_watch.normalize import canonical_doi, canonical_url, deduplicate
from research_watch.publication import decide


def item(url: str, doi: str | None = None) -> DiscoveredItem:
    return DiscoveredItem("A sufficiently long title", url, "Source", "academic-paper", "2026-01-01", doi=doi)


def test_url_and_doi_normalization() -> None:
    assert canonical_doi("https://doi.org/10.1000/ABC") == "10.1000/abc"
    assert canonical_url("HTTPS://Example.org/x/?utm_source=test&a=1#fragment") == "https://example.org/x?a=1"


def test_deduplication_prefers_first_canonical_record() -> None:
    records, log = deduplicate([item("https://one.test", "10.1/X"), item("https://two.test", "https://doi.org/10.1/x")])
    assert len(records) == 1
    assert log[0]["reason"] == "doi"


def test_automatic_publication_gates() -> None:
    assert decide(True, ["none"], 0.8)[0] == "published"
    assert decide(False, ["title-only"], 0.8)[0] == "withheld"
    assert decide(True, ["prompt-injection"], 0.9)[0] == "quarantined"
