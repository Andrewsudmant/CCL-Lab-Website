"""Bounded OpenAlex works search."""

from __future__ import annotations
from research_watch.adapters.base import DiscoveryAdapter, get_json
from research_watch.models import DiscoveredItem


def _abstract(index: dict[str, list[int]] | None) -> str | None:
    if not index:
        return None
    pairs = sorted((position, word) for word, positions in index.items() for position in positions)
    return " ".join(word for _, word in pairs)


class OpenAlexAdapter(DiscoveryAdapter):
    name = "openalex"
    endpoint = "https://api.openalex.org/works"

    def search(self, query: str, query_id: str, limit: int = 10) -> list[DiscoveredItem]:
        payload = get_json(self.endpoint, {"search": query, "per-page": min(limit, 25), "select": "id,doi,title,display_name,publication_date,authorships,primary_location,abstract_inverted_index"})
        items = []
        for work in payload.get("results", []):
            location = work.get("primary_location") or {}
            source = location.get("source") or {}
            doi = (work.get("doi") or "").removeprefix("https://doi.org/") or None
            abstract = _abstract(work.get("abstract_inverted_index"))
            items.append(DiscoveredItem(
                title=work.get("display_name") or work.get("title") or "Untitled",
                url=work.get("doi") or work.get("id"), source_name=source.get("display_name") or "OpenAlex",
                source_type="academic-paper", publication_date=work.get("publication_date") or "",
                authors=[a.get("author", {}).get("display_name", "") for a in work.get("authorships", []) if a.get("author")],
                doi=doi, platform_identifier=(work.get("id") or "").rsplit("/", 1)[-1], abstract=abstract,
                evidence_types=["abstract"] if abstract else ["metadata-only"], adapter=self.name,
                query_id=query_id, raw_metadata=work,
            ))
        return items
