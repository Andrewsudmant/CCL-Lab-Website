#!/usr/bin/env python3
"""Practical static accessibility checks for generated HTML."""

from __future__ import annotations

import argparse
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SITE = ROOT / "_site"


class AccessibilityParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.html_lang: str | None = None
        self.main_count = 0
        self.h1_count = 0
        self.images_missing_alt = 0
        self.empty_links = 0
        self._in_link = False
        self._link_has_label = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "html":
            self.html_lang = values.get("lang")
        elif tag == "main":
            self.main_count += 1
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "img" and "alt" not in values:
            self.images_missing_alt += 1
        elif tag == "a":
            self._in_link = True
            self._link_has_label = bool(values.get("aria-label") or values.get("title"))
            if values.get("class") and "anchorjs-link" in (values.get("class") or ""):
                self._link_has_label = True

    def handle_data(self, data: str) -> None:
        if self._in_link and data.strip():
            self._link_has_label = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._in_link:
            if not self._link_has_label:
                self.empty_links += 1
            self._in_link = False


def main() -> int:
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--site-dir", type=Path, default=DEFAULT_SITE, help="Rendered site directory")
    args = argument_parser.parse_args()
    site = args.site_dir.resolve()
    if not site.exists():
        print(f"{site} does not exist; run a build first.")
        return 1
    errors: list[str] = []
    pages = sorted(site.rglob("*.html"))
    for page in pages:
        parser = AccessibilityParser()
        parser.feed(page.read_text(encoding="utf-8"))
        label = page.relative_to(site)
        if not parser.html_lang:
            errors.append(f"{label}: missing document language")
        if parser.main_count != 1:
            errors.append(f"{label}: expected one main landmark, found {parser.main_count}")
        if parser.h1_count != 1:
            errors.append(f"{label}: expected one h1, found {parser.h1_count}")
        if parser.images_missing_alt:
            errors.append(f"{label}: {parser.images_missing_alt} image(s) missing alt attributes")
        if parser.empty_links:
            errors.append(f"{label}: {parser.empty_links} link(s) without accessible text")
    if errors:
        print("Static accessibility checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Static accessibility checks passed for {len(pages)} HTML pages.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
