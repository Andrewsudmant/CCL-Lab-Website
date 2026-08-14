"""Provider-neutral discovery records."""

from __future__ import annotations
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class DiscoveredItem:
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
    raw_metadata: dict[str, Any] = field(default_factory=dict)

    def public_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value.pop("raw_metadata", None)
        return value
