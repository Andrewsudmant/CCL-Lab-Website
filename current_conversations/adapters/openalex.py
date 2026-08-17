"""Bounded OpenAlex works search."""

from __future__ import annotations
from datetime import date, timedelta
from datetime import datetime, timezone
from current_conversations.adapters.base import DiscoveryAdapter, get_json
from current_conversations.models import DiscoveredItem


def _abstract(index: dict[str, list[int]] | None) -> str | None:
    if not index:
        return None
    pairs = sorted((position, word) for word, positions in index.items() for position in positions)
    return " ".join(word for _, word in pairs)


class OpenAlexAdapter(DiscoveryAdapter):
    name = "openalex"
    endpoint = "https://api.openalex.org/works"

    def search(self, query: str, query_id: str, limit: int = 10, lookback_days: int = 30) -> list[DiscoveredItem]:
        parameters = {
            "filter": f"from_publication_date:{date.today() - timedelta(days=lookback_days)},type:article|preprint,language:en,title_and_abstract.search:{query}",
            "per-page": min(limit, 25),
            "sort": "publication_date:desc",
            "select": "id,doi,title,display_name,publication_date,authorships,primary_location,abstract_inverted_index",
            "mailto": "andrew_sudmant@sfu.ca",
        }
        payload = get_json(self.endpoint, parameters)
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
                query_id=query_id, raw_metadata={"provider_parameters": parameters, "openalex_id": work.get("id"), "provider_source_url": location.get("landing_page_url") or source.get("homepage_url"), "retrieved_at": datetime.now(timezone.utc).isoformat(), "fallback_used": False},
            ))
        return items
