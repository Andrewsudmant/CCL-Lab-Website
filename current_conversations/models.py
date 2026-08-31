"""Provider-neutral source and conversation-cluster records."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class DiscoveredItem:
    """Adapter output before canonical source validation."""

    title: str
    url: str
    source_name: str
    source_type: str
    publication_date: str
    authors: list[str] = field(default_factory=list)
    doi: str | None = None
    platform_identifier: str | None = None
    abstract: str | None = None
    evidence_types: list[str] = field(default_factory=lambda: ["metadata-only"])
    adapter: str = "unknown"
    query_id: str = "unknown"
    source_environment: str = "academic-research"
    source_role: str = "primary-research"
    underlying_source_urls: list[str] = field(default_factory=list)
    raw_metadata: dict[str, Any] = field(default_factory=dict)

    def public_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value.pop("raw_metadata", None)
        return value


@dataclass
class ConversationSource:
    source_id: str
    title: str
    original_url: str
    canonical_url: str
    source_environment: str
    source_type: str
    source_role: str
    source_domain: str
    publication_date: str
    retrieval_timestamp: str
    authors_or_organisation: list[str]
    evidence_basis: list[str]
    evidence_limitations: str
    discovery: dict[str, str]
    stable_identifier: dict[str, str] | None = None
    publisher_or_platform: str = "Unknown"
    language: str = "en"
    geographies: list[str] = field(default_factory=lambda: ["global"])
    content_access_status: str = "limited"
    content_hash: str | None = None
    ai_annotation: dict[str, str] | None = None
    risk_flags: list[str] = field(default_factory=list)
    correction_status: str = "none"
    availability_status: str = "available"
    review: dict[str, Any] = field(default_factory=lambda: {"status": "not-reviewed", "reviewer": None, "reviewed_date": None, "edits": []})
    lab_affiliated: bool = False
    mdpi_excluded: bool = False
    captured_fixture: bool = False

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ConversationCluster:
    cluster_id: str
    slug: str
    public_title: str
    discussion_statement: str
    date_first_observed: str
    date_most_recently_observed: str
    principal_source_id: str
    linked_source_ids: list[str]
    primary_theme: str | None
    secondary_themes: list[str]
    geographies: list[str]
    source_environments: list[str]
    principal_source_role: str
    summary: str
    reason_for_relevance: str
    limitations: str
    agreement_disagreement_uncertainty: str
    clustering: dict[str, Any]
    ai_provenance: dict[str, Any]
    publication_decision: str = "withheld"
    correction_status: str = "none"
    availability_status: str = "available"
    history: list[dict[str, str]] = field(default_factory=list)
    homepage_eligible: bool = False
    archive_date: str | None = None
    captured_fixture: bool = False

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)
