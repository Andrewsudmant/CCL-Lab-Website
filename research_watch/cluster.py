"""Conservative identifier-aware event clustering and diversity selection."""

from __future__ import annotations
import hashlib
import re
from urllib.parse import urlsplit
from research_watch.models import DiscoveredItem


def normalized_title(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def event_key(item: DiscoveredItem) -> str:
    title = normalized_title(item.title)
    if len(title) >= 20:
        return "exact-title:" + hashlib.sha256(title.encode()).hexdigest()[:16]
    if item.doi:
        return f"doi:{item.doi.lower()}"
    if item.platform_identifier:
        return f"platform:{item.platform_identifier}"
    basis = title + "|" + (item.authors[0].lower() if item.authors else item.source_name.lower())
    return "title-author:" + hashlib.sha256(basis.encode()).hexdigest()[:16]


def cluster(items: list[DiscoveredItem]) -> tuple[list[DiscoveredItem], list[dict[str, object]]]:
    groups: dict[str, list[DiscoveredItem]] = {}
    for item in items:
        groups.setdefault(event_key(item), []).append(item)
    principals, report = [], []
    for key, group in groups.items():
        principal = sorted(group, key=lambda x: (not bool(x.doi), "abstract" not in x.evidence_types, x.source_type != "academic-paper"))[0]
        principals.append(principal)
        report.append({"event_cluster_id": key, "principal": principal.url, "members": [x.url for x in group]})
    return principals, report


def diverse(items: list[DiscoveredItem], maximum: int = 12, per_domain: int = 4) -> list[DiscoveredItem]:
    chosen, domains = [], {}
    for item in items:
        domain = urlsplit(item.url).netloc.lower()
        if domains.get(domain, 0) >= per_domain:
            continue
        chosen.append(item)
        domains[domain] = domains.get(domain, 0) + 1
        if len(chosen) == maximum:
            break
    return chosen
