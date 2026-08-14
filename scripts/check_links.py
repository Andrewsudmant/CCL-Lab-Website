#!/usr/bin/env python3
"""Check built-site links. External checks are opt-in and networked."""

from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"] or "")
        if tag in {"a", "link", "script", "img"}:
            target = values.get("href") or values.get("src")
            if target:
                self.links.append(target)


def parsed(path: Path) -> LinkParser:
    parser = LinkParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def check_internal() -> list[str]:
    errors: list[str] = []
    pages = {path: parsed(path) for path in SITE.rglob("*.html")}
    for page, parser in pages.items():
        for link in parser.links:
            url = urlparse(link)
            if url.scheme in {"http", "https", "mailto", "tel", "data"} or link.startswith("//"):
                continue
            raw_path = unquote(url.path)
            target = (SITE / raw_path.lstrip("/")) if raw_path.startswith("/") else (page.parent / raw_path)
            target = target.resolve()
            if not raw_path:
                target = page
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                errors.append(f"{page.relative_to(SITE)}: missing target {link}")
                continue
            if url.fragment and target.suffix == ".html":
                target_parser = pages.get(target, parsed(target))
                if url.fragment not in target_parser.ids:
                    errors.append(f"{page.relative_to(SITE)}: missing fragment #{url.fragment} in {target.relative_to(SITE)}")
    return errors


AUTOMATION_LIMITED_DOMAINS = {"doi.org", "www.doi.org", "bsky.app", "www.linkedin.com", "uk.linkedin.com"}


def check_external() -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    urls: set[str] = set()
    for path in SITE.rglob("*.html"):
        for link in parsed(path).links:
            if urlparse(link).scheme in {"http", "https"}:
                urls.add(link)
    for url in sorted(urls):
        request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "CCLL-link-check/0.1"})
        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                if response.status >= 400:
                    errors.append(f"{url}: HTTP {response.status}")
        except urllib.error.HTTPError as exc:
            # Some canonical providers reject HEAD or automated clients. Retry a
            # minimal GET before recording an environment-limited warning.
            try:
                retry = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 CCLL-link-check/0.2", "Range": "bytes=0-1023"})
                with urllib.request.urlopen(retry, timeout=10) as response:
                    if response.status >= 400:
                        raise urllib.error.HTTPError(url, response.status, "GET failed", response.headers, None)
            except (urllib.error.URLError, TimeoutError) as retry_exc:
                if urlparse(url).netloc.lower() in AUTOMATION_LIMITED_DOMAINS and getattr(retry_exc, "code", None) in {403, 404, 405, 429, 999}:
                    warnings.append(f"{url}: provider blocked automated verification ({retry_exc})")
                else:
                    errors.append(f"{url}: {retry_exc}")
        except (urllib.error.URLError, TimeoutError) as exc:
            errors.append(f"{url}: {exc}")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--external", action="store_true", help="Also make network requests to external links")
    args = parser.parse_args()
    if not SITE.exists():
        print("_site does not exist; run a build first.")
        return 1
    errors = check_internal()
    warnings: list[str] = []
    if args.external:
        external_errors, warnings = check_external()
        errors.extend(external_errors)
    if errors:
        print("Link checks failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    for warning in warnings:
        print(f"External-link warning: {warning}")
    mode = "internal and external" if args.external else "internal (external checks skipped)"
    print(f"Link checks passed: {mode}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
