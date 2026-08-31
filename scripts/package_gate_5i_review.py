#!/usr/bin/env python3
"""Package final Draft 0.1 review evidence, never deploy it."""
from pathlib import Path
import zipfile

try:
    from .package_gate_5h_review import ROOT, add_tree, digest, git
except ImportError:
    from package_gate_5h_review import ROOT, add_tree, digest, git

OUTPUT = ROOT / "deliverables/CCLL-draft-0-1-final-release-gate-5i-OWNER_REVIEW_REQUIRED.zip"
README = ROOT / "docs/reviews/gate-5i/README_OWNER_REVIEW.md"
FILES = [
    "docs/baseline-gate-5i.md", "docs/decisions/gate-5h-owner-approval-and-draft-release.md",
    "docs/reviews/gate-5i/delivery-example-curation.md", "docs/reviews/gate-5i/public-copy-before-and-after.md",
    "docs/reviews/gate-5i/draft-0-1-final-readiness.md", "docs/reviews/gate-5i/public-output-audit.md",
    "docs/runbooks/publish-draft-0-1-github-pages.md", ".github/workflows/public-draft-pages.yml",
    "reports/editorial/gate-5i-publication-page-diagnostic.md", "reports/editorial/gate-5i-public-voice-diagnostic.md",
    "reports/accessibility/gate-5i-keyboard-navigation.md", "reports/browser-qa-gate-5i.md",
    "reports/security/gate-5i-secret-scan.md", "reports/release/gate-5i-external-link-audit.md",
    "reports/release/gate-5i-workflow-validation.md", "reports/file-by-file-summary-gate-5i.md",
    "reports/qa/gate-5i-final/release-checks.log", "reports/qa/gate-5i-final/secret-scan.log",
    "reports/qa/gate-5i-baseline/release-checks.log", "tests/test_gate_5i_final_release.py",
    "config/site.yml", "config/theme_featured_examples.yml", "config/publication_theme_examples.yml",
    "reports/content/publication-complete-inventory.json", "publications/metadata-and-sources.qmd",
    "docs/architecture.md", "docs/content-governance.md", "docs/security.md",
]


def package() -> Path:
    files = [(ROOT / p, Path("review") / p) for p in FILES]
    for directory, target in [("_site", "rendered-root"), ("_site-project-path/CCL-Lab-Website", "rendered-project-path/CCL-Lab-Website"), ("reports/screenshots/gate-5i", "review/screenshots/gate-5i")]:
        source = ROOT / directory
        if not source.is_dir(): raise FileNotFoundError(directory)
        add_tree(files, source, Path(target))
    if not README.is_file() or any(not source.is_file() for source, _ in files):
        raise FileNotFoundError("Required Gate 5I review evidence is missing")
    for source, _ in files:
        if source.suffix == ".zip" or source.name.startswith(".env"):
            raise ValueError("Forbidden archive entry")
    manifest = ["Cities & Climate Learning Lab — Gate 5I final owner review",
                f"Branch: {git('branch', '--show-current')}", f"Commit: {git('rev-parse', 'HEAD')}",
                "Readiness: READY_SUBJECT_TO_OWNER_MANUAL_KEYBOARD_CHECK",
                "Deployment: none; Current Conversations: in development", "",
                "SHA-256  Archive path", f"{digest(README)}  00_READ_ME_FIRST.md"]
    OUTPUT.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.write(README, "00_READ_ME_FIRST.md")
        for source, target in files:
            archive.write(source, target); manifest.append(f"{digest(source)}  {target.as_posix()}")
        archive.writestr("MANIFEST.txt", "\n".join(manifest) + "\n")
    return OUTPUT


if __name__ == "__main__": print(package())
