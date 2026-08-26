from __future__ import annotations

import zipfile

from scripts.content import ROOT
from scripts.package_handoff import package
from scripts.package_owner_review import package as package_owner_review
from scripts.package_gate_5c_review import package as package_gate_5c_review


def test_handoff_package_contains_summary_and_governance(tmp_path) -> None:
    destination = tmp_path / "handoff.zip"
    package(ROOT / "docs/handoffs/gate-0-1-handoff.md", destination)
    with zipfile.ZipFile(destination) as archive:
        names = set(archive.namelist())
        assert "00_READ_ME_FIRST.md" in names
        assert "MANIFEST.txt" in names
        assert "project-context/docs/architecture.md" in names
        assert "project-context/docs/content-governance.md" in names
        assert "project-context/docs/security.md" in names
        assert "project-context/config/research_scope.yml" in names
        assert not any(name.startswith("_site/") for name in names)
        assert not any(".env" in name for name in names)


def test_owner_review_package_contains_site_screenshots_and_manifest(tmp_path) -> None:
    destination = tmp_path / "owner-review.zip"
    package_owner_review(destination)
    with zipfile.ZipFile(destination) as archive:
        names = set(archive.namelist())
        assert "00_READ_ME_FIRST.md" in names
        assert "MANIFEST.txt" in names
        assert "rendered-site/index.html" in names
        assert "review/screenshots/gate-5b/desktop/home.png" in names
        assert "review/screenshots/gate-5b/mobile/home.png" in names
        assert "source/docs/handoffs/gate-5b-handoff.md" in names


def test_gate_5c_owner_review_contains_only_current_review_screenshots(tmp_path) -> None:
    destination = tmp_path / "gate-5c-owner-review.zip"
    package_gate_5c_review(destination)
    with zipfile.ZipFile(destination) as archive:
        names = set(archive.namelist())
        assert "00_READ_ME_FIRST.md" in names
        assert "MANIFEST.txt" in names
        assert "rendered-site/index.html" in names
        assert "rendered-site/research/geographies-of-climate-learning.html" in names
        assert "rendered-site/projects/data-methodologies-climate-impact.html" in names
        assert "review/screenshots/gate-5c/desktop/home.png" in names
        assert "review/screenshots/gate-5c/mobile/learning-cycle.png" in names
        assert "review/query-migration.md" in names
        assert "review/openalex-diagnostics.md" in names
        assert not any("gate-5b" in name or "thematic-architecture-reframe-v1" in name for name in names)
