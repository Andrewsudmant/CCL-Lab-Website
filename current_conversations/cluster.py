"""Evidence-bounded cross-source clustering and principal-source selection."""

from __future__ import annotations

import hashlib
import re
from itertools import combinations
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from current_conversations.models import DiscoveredItem

ROLE_PRIORITY = {
    "primary-research": 1, "official-policy-source": 2, "dataset-or-tool": 4,
    "official-announcement": 5, "news-reporting": 6, "independent-analysis": 7,
    "research-commentary": 8, "practitioner-commentary": 8, "public-discussion": 9,
}
TRACKING_PARAMETERS = {"fbclid", "gclid", "mc_cid", "mc_eid"}


def normalized_title(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()


def canonical_url(value: str) -> str:
    parts = urlsplit(value.strip())
    host = parts.netloc.casefold().removeprefix("www.")
    path = re.sub(r"/+", "/", parts.path).rstrip("/") or "/"
    query = urlencode(sorted((key, val) for key, val in parse_qsl(parts.query) if not key.casefold().startswith("utm_") and key.casefold() not in TRACKING_PARAMETERS))
    return urlunsplit((parts.scheme.casefold() or "https", host, path, query, ""))


def canonical_doi(value: str | None) -> str | None:
    if not value:
        return None
    match = re.search(r"10\.\d{4,9}/[^\s?#]+", value, flags=re.I)
    return match.group(0).rstrip(".,;)").casefold() if match else None


def _urls(item: DiscoveredItem) -> set[str]:
    values = [item.url, *item.underlying_source_urls]
    values.extend(item.raw_metadata.get("explicit_citation_urls", []))
    return {canonical_url(value) for value in values if isinstance(value, str) and value.startswith(("http://", "https://"))}


def _dois(item: DiscoveredItem) -> set[str]:
    values = [item.doi, item.url, *item.underlying_source_urls]
    values.extend(item.raw_metadata.get("citation_dois", []))
    return {doi for value in values if (doi := canonical_doi(value))}


def _organizations(item: DiscoveredItem) -> set[str]:
    values = [item.source_name, *item.authors]
    values.extend(item.raw_metadata.get("organizations", []))
    return {normalized_title(value) for value in values if isinstance(value, str) and len(normalized_title(value)) >= 4}


def _title_similarity(left: str, right: str) -> float:
    a, b = set(normalized_title(left).split()), set(normalized_title(right).split())
    return len(a & b) / len(a | b) if a and b else 0.0


def relationship_evidence(left: DiscoveredItem, right: DiscoveredItem) -> list[str]:
    evidence: list[str] = []
    left_dois, right_dois = _dois(left), _dois(right)
    left_urls, right_urls = _urls(left), _urls(right)
    direct_left, direct_right = canonical_url(left.url), canonical_url(right.url)
    if left_dois & right_dois:
        evidence.append("shared-doi")
    if direct_left == direct_right:
        evidence.append("canonical-url")
    if direct_left in right_urls or direct_right in left_urls:
        evidence.append("underlying-source-or-citation-link")
    if left.platform_identifier and left.platform_identifier == right.platform_identifier:
        evidence.append("shared-platform-identifier")
    similarity = _title_similarity(left.title, right.title)
    if similarity >= 0.90:
        evidence.append("near-exact-title")
    if _organizations(left) & _organizations(right):
        evidence.append("shared-organization-or-author")
    return evidence


def accepts_relationship(evidence: list[str]) -> bool:
    strong = {"shared-doi", "canonical-url", "underlying-source-or-citation-link", "shared-platform-identifier"}
    return bool(strong & set(evidence)) or {"near-exact-title", "shared-organization-or-author"}.issubset(evidence)


def event_key(item: DiscoveredItem) -> str:
    if doi := canonical_doi(item.doi or item.url):
        return f"doi:{doi}"
    return "source:" + hashlib.sha256(canonical_url(item.url).encode()).hexdigest()[:16]


def principal_source(group: list[DiscoveredItem]) -> tuple[DiscoveredItem, str]:
    chosen = sorted(group, key=lambda item: (ROLE_PRIORITY.get(item.source_role, 99), "metadata-only" in item.evidence_types, not bool(item.doi or item.platform_identifier), canonical_url(item.url)))[0]
    return chosen, f"Selected {chosen.source_role} as the most original available source with the strongest recorded evidence access; exceptions require an explicit override."


def cluster(items: list[DiscoveredItem]) -> tuple[list[DiscoveredItem], list[dict[str, object]]]:
    """Cluster sources only when auditable deterministic evidence accepts the link.

    A model may propose candidate pairs through ``raw_metadata.model_cluster_proposals``.
    Proposals merely bound comparisons; they are never sufficient for acceptance.
    """
    parents = list(range(len(items)))
    pair_evidence: dict[tuple[int, int], list[str]] = {}
    rejected_model_proposals: list[dict[str, object]] = []

    def find(index: int) -> int:
        while parents[index] != index:
            parents[index] = parents[parents[index]]
            index = parents[index]
        return index

    def union(left: int, right: int) -> None:
        a, b = find(left), find(right)
        if a != b:
            parents[b] = a

    url_index = {canonical_url(item.url): index for index, item in enumerate(items)}
    proposed_pairs: set[tuple[int, int]] = set()
    for index, item in enumerate(items):
        for proposal in item.raw_metadata.get("model_cluster_proposals", []):
            if not isinstance(proposal, dict) or proposal.get("confidence", 0) < 0.90:
                continue
            target = url_index.get(canonical_url(str(proposal.get("target_url", ""))))
            if target is not None and target != index:
                proposed_pairs.add(tuple(sorted((index, target))))

    for left, right in combinations(range(len(items)), 2):
        evidence = relationship_evidence(items[left], items[right])
        proposed = (left, right) in proposed_pairs
        if accepts_relationship(evidence):
            if proposed:
                evidence.append("bounded-model-proposal-corroborated")
            union(left, right)
            pair_evidence[(left, right)] = evidence
        elif proposed:
            rejected_model_proposals.append({"left": items[left].url, "right": items[right].url, "reason": "no deterministic corroboration"})

    groups: dict[int, list[int]] = {}
    for index in range(len(items)):
        groups.setdefault(find(index), []).append(index)
    principals: list[DiscoveredItem] = []
    report: list[dict[str, object]] = []
    for indices in groups.values():
        group = [items[index] for index in indices]
        principal, rationale = principal_source(group)
        evidence = sorted({value for pair, values in pair_evidence.items() if pair[0] in indices and pair[1] in indices for value in values})
        basis = event_key(principal) if len(group) == 1 else "evidence:" + hashlib.sha256("|".join(sorted(canonical_url(item.url) for item in group)).encode()).hexdigest()[:16]
        report.append({
            "event_cluster_id": basis, "principal": principal.url, "members": [item.url for item in group],
            "supporting_identifiers": evidence or [event_key(principal)], "principal_source_rationale": rationale,
            "clustering_confidence": 1.0 if any(value in evidence for value in ("shared-doi", "canonical-url")) else 0.9 if evidence else 1.0,
            "method": "cross-source-evidence-v2", "rejected_model_proposals": [proposal for proposal in rejected_model_proposals if proposal["left"] in {item.url for item in group} or proposal["right"] in {item.url for item in group}],
        })
        principals.append(principal)
    return principals, report


def diverse(items: list[DiscoveredItem], maximum: int = 12, per_domain: int = 4) -> list[DiscoveredItem]:
    chosen: list[DiscoveredItem] = []
    domains: dict[str, int] = {}
    for item in items:
        domain = urlsplit(item.url).netloc.lower()
        if domains.get(domain, 0) >= per_domain:
            continue
        chosen.append(item); domains[domain] = domains.get(domain, 0) + 1
        if len(chosen) == maximum:
            break
    return chosen
