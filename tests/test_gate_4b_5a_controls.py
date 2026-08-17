from __future__ import annotations
import json
import tempfile
from pathlib import Path
import pytest

from current_conversations.transaction import publish_current_state
from scripts.content import ROOT
from scripts.stage_current_conversations import verify


def json_records(kind: str) -> list[dict]:
    return [json.loads(path.read_text()) for path in (ROOT / f"data/current-conversations/generated/{kind}").glob("*.json")]


def test_source_cluster_relationships_are_complete() -> None:
    sources = {record["source_id"]: record for record in json_records("sources")}
    clusters = json_records("clusters")
    assert len(sources) == 26 and len(clusters) == 25
    assert set(record["primary_theme"] for record in clusters) == {theme["id"] for theme in __import__("yaml").safe_load((ROOT / "config/research_scope.yml").read_text())["themes"]}
    assert any(record["linked_source_ids"] for record in clusters)
    for cluster in clusters:
        assert cluster["principal_source_id"] in sources
        assert all(source_id in sources for source_id in cluster["linked_source_ids"])


def test_public_disclosure_and_moved_routes() -> None:
    page = (ROOT / "current-conversations/index.qmd").read_text()
    generated = (ROOT / "generated/current-conversations-feed.qmd").read_text()
    assert "inclusion does not imply endorsement" in page
    assert "Captured fixture · no AI generation recorded · not reviewed by the lab" in generated
    assert "Continue to Current Conversations" in (ROOT / "research-watch/index.qmd").read_text()
    detail = (ROOT / "current-conversations/sustainable-urban-data-centres.qmd").read_text()
    assert "\n\n### Also discussed in:" in detail


def test_feeds_preserve_original_source_links() -> None:
    feed = json.loads((ROOT / "current-conversations/feed.json").read_text())
    assert feed["version"] == "https://jsonfeed.org/version/1.1"
    assert len(feed["items"]) == 25
    assert all(item["url"].startswith("/current-conversations/") for item in feed["items"])
    assert "<rss version=\"2.0\">" in (ROOT / "current-conversations/feed.xml").read_text()


def test_complete_and_selected_publication_controls() -> None:
    complete = json.loads((ROOT / "reports/content/publication-complete-inventory.json").read_text())["records"]
    selected = [record for record in complete if record["featured"]]
    assert len(complete) == 46 and len(selected) == 10
    mdpi = [record for record in complete if record.get("mdpi_excluded")]
    assert len(mdpi) == 1 and not mdpi[0]["featured"] and not mdpi[0]["current_conversations_eligible"]


def test_staging_allowlist_accepts_expected_and_rejects_control_plane() -> None:
    verify(["staging/current-conversations/current/run-manifest.json", "current-conversations/feed.json"])
    with pytest.raises(SystemExit):
        verify(["prompts/current-conversations-classification-v1.md"])
    with pytest.raises(SystemExit):
        verify(["staging/current-conversations/current/run-manifest.json"], "main")


def test_atomic_rollback_preserves_last_known_good() -> None:
    with tempfile.TemporaryDirectory() as raw:
        target = Path(raw) / "current"
        source = {"source_id": "ccs-test"}
        cluster = {"cluster_id": "ccc-test"}
        snapshot = {"sources": [source], "clusters": [cluster], "feeds": {"feed.json": "{}"}, "site": {}, "manifest": {}, "budget_ledger": {}}
        publish_current_state(target, snapshot, lambda path: None, "good")
        marker = (target / "run-manifest.json").read_text()
        with pytest.raises(AssertionError):
            publish_current_state(target, snapshot, lambda path: (_ for _ in ()).throw(AssertionError("deliberate")), "bad")
        assert (target / "run-manifest.json").read_text() == marker


def test_workflow_is_private_and_fail_closed() -> None:
    workflow = (ROOT / ".github/workflows/current-conversations-scheduled.yml").read_text()
    assert "automation/current-conversations-staging" in workflow
    assert "CURRENT_CONVERSATIONS_STAGING_WRITE_ENABLED" in workflow
    assert "contents: read" in workflow and "contents: write" in workflow
    assert "actions/deploy-pages" not in workflow.lower()


def test_normal_build_has_no_discovery_side_effect() -> None:
    makefile = (ROOT / "Makefile").read_text()
    recipe = makefile.split("build: generate", 1)[1].split("linkcheck:", 1)[0]
    assert "current-conversations-pilot" not in recipe
    assert "current-conversations-discover" not in recipe
