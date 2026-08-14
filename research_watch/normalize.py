"""Deterministic URL/DOI normalization and deduplication."""

from __future__ import annotations
import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from research_watch.models import DiscoveredItem


TRACKING = {"fbclid", "gclid", "mc_cid", "mc_eid"}


def canonical_url(url: str) -> str:
    parts = urlsplit(url)
    query = [(k, v) for k, v in parse_qsl(parts.query) if not k.lower().startswith("utm_") and k.lower() not in TRACKING]
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path.rstrip("/") or "/", urlencode(query), ""))


def canonical_doi(value: str | None) -> str | None:
    if not value:
        return None
    doi = re.sub(r"^(https?://(dx\.)?doi\.org/|doi:\s*)", "", value.strip(), flags=re.I)
    return doi.lower()


def deduplicate(items: list[DiscoveredItem]) -> tuple[list[DiscoveredItem], list[dict[str, str]]]:
    kept: dict[str, DiscoveredItem] = {}
    log = []
    for item in items:
        item.doi = canonical_doi(item.doi)
        item.url = canonical_url(item.url)
        key = f"doi:{item.doi}" if item.doi else f"url:{item.url}"
        if key in kept:
            log.append({"kept": kept[key].url, "removed": item.url, "reason": key.split(":", 1)[0]})
        else:
            kept[key] = item
    return list(kept.values()), log
