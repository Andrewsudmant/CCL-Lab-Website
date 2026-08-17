from __future__ import annotations

import zipfile

from scripts.content import ROOT
from scripts.package_handoff import package
from scripts.package_owner_review import package as package_owner_review


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
