#!/usr/bin/env python3
"""Explicit, bounded HEAD-only release diagnostic; never follows redirects."""
from __future__ import annotations

import argparse
import datetime as dt
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit

try:
    from .check_links import DEFAULT_SITE, parsed
except ImportError:
    from check_links import DEFAULT_SITE, parsed

ALLOWED_HOSTS = frozenset({
    "arxiv.org", "bsky.app", "coalitionforurbantransitions.org", "doi.org",
    "edemocracy.northyorks.gov.uk", "eprints.whiterose.ac.uk", "orcid.org",
    "uk.linkedin.com", "ukcobenefitsatlas.net", "www.lse.ac.uk", "www.nature.com",
    "www.research.ed.ac.uk", "www.sfu.ca", "www.theigc.org", "zenodo.org",
})
MAX_URLS = 60


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def source_urls(site: Path) -> list[str]:
    urls = sorted({link for page in site.rglob("*.html") for link in parsed(page).links
                   if urlsplit(link).scheme in {"http", "https"}})
    if not urls or len(urls) > MAX_URLS:
        raise ValueError("External URL count is outside the reviewed 1–60 bound")
    for url in urls:
        parts = urlsplit(url)
        if parts.hostname not in ALLOWED_HOSTS or parts.username or parts.password or parts.port:
            raise ValueError("Unapproved external destination; review the host allowlist")
    return urls


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--network-approved", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not args.network_approved:
        parser.error("Network is off by default; explicit --network-approved is required")
    urls = source_urls(DEFAULT_SITE)
    opener = urllib.request.build_opener(NoRedirect())
    deadline = time.monotonic() + 240
    rows = []
    for url in urls:
        if time.monotonic() >= deadline:
            rows.append((url, "Not checked: total time bound reached")); continue
        request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "CCLL-release-link-check/0.1"})
        try:
            with opener.open(request, timeout=min(8, max(0.01, deadline - time.monotonic()))) as response:
                code = response.status
        except urllib.error.HTTPError as exc:
            code = exc.code
            exc.close()
        except (urllib.error.URLError, TimeoutError, OSError):
            rows.append((url, "Unverified: network/timeout/TLS limitation"))
            time.sleep(0.2); continue
        label = "Reachable" if 200 <= code < 300 else "Redirect (not followed)" if 300 <= code < 400 else "Unverified: automated access refused" if code in {401, 403, 405, 429, 999} else "Unverified: requires owner/source review"
        rows.append((url, f"{label}; HTTP {code}"))
        time.sleep(0.2)
    output = ["# Gate 5I bounded external-link diagnostic", "", f"UTC: {dt.datetime.now(dt.timezone.utc).isoformat()}",
              f"{len(urls)} distinct public-source URLs; {len(ALLOWED_HOSTS)} approved hosts; maximum 60 requests; 8-second timeout; 240-second total limit; 0.2-second minimum interval.",
              "HEAD only. No redirects followed, response bodies read or persisted, API requests, model calls, credentials or provider refreshes. A redirect verifies only the starting endpoint. Non-2xx responses are diagnostics, not proof that the underlying source is absent.", "", "| URL | Result |", "|---|---|"]
    output += [f"| {url} | {status} |" for url, status in rows]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(output) + "\n")
    print(f"Recorded {len(rows)} bounded checks in {args.output}; review all unverified rows.")
    return 0


if __name__ == "__main__": raise SystemExit(main())
