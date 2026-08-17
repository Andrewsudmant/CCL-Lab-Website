"""Conservative clustering and explicit principal-source selection."""

from __future__ import annotations

import hashlib
import re
from urllib.parse import urlsplit

from current_conversations.models import DiscoveredItem

ROLE_PRIORITY = {
    "primary-research": 1,
    "official-policy-source": 2,
    "dataset-or-tool": 4,
    "official-announcement": 5,
    "news-reporting": 6,
    "independent-analysis": 7,
    "research-commentary": 8,
    "practitioner-commentary": 8,
    "public-discussion": 9,
}


def normalized_title(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def event_key(item: DiscoveredItem) -> str:
    if item.doi:
        return f"doi:{item.doi.lower()}"
    if item.platform_identifier:
        return f"platform:{item.platform_identifier}"
    title = normalized_title(item.title)
    basis = title + "|" + (item.authors[0].lower() if item.authors else item.source_name.lower())
    return "title-author:" + hashlib.sha256(basis.encode()).hexdigest()[:16]


def principal_source(group: list[DiscoveredItem]) -> tuple[DiscoveredItem, str]:
    chosen = sorted(
        group,
        key=lambda item: (
            ROLE_PRIORITY.get(item.source_role, 99),
            "metadata-only" in item.evidence_types,
            not bool(item.doi or item.platform_identifier),
        ),
    )[0]
    rationale = (
        f"Selected {chosen.source_role} as the most original available source with "
        f"the strongest recorded evidence access; exceptions require an explicit override."
    )
    return chosen, rationale


def cluster(items: list[DiscoveredItem]) -> tuple[list[DiscoveredItem], list[dict[str, object]]]:
    """Group exact identifiers/links/titles; broad semantic similarity is insufficient."""
    groups: dict[str, list[DiscoveredItem]] = {}
    for item in items:
        groups.setdefault(event_key(item), []).append(item)
    principals: list[DiscoveredItem] = []
    report: list[dict[str, object]] = []
    for key, group in groups.items():
        principal, rationale = principal_source(group)
        principals.append(principal)
        report.append({
            "event_cluster_id": key,
            "principal": principal.url,
            "members": [item.url for item in group],
            "supporting_identifiers": sorted({event_key(item) for item in group}),
            "principal_source_rationale": rationale,
            "clustering_confidence": 1.0 if len({event_key(item) for item in group}) == 1 else 0.75,
            "method": "exact-identifier-url-title-v1",
        })
    return principals, report


def diverse(items: list[DiscoveredItem], maximum: int = 12, per_domain: int = 4) -> list[DiscoveredItem]:
    chosen: list[DiscoveredItem] = []
    domains: dict[str, int] = {}
    for item in items:
        domain = urlsplit(item.url).netloc.lower()
        if domains.get(domain, 0) >= per_domain:
            continue
        chosen.append(item)
        domains[domain] = domains.get(domain, 0) + 1
        if len(chosen) == maximum:
            break
    return chosen
