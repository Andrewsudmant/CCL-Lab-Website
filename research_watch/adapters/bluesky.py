"""Bounded public Bluesky AppView search."""

from __future__ import annotations
from research_watch.adapters.base import DiscoveryAdapter, get_json
from research_watch.models import DiscoveredItem


class BlueskyAdapter(DiscoveryAdapter):
    name = "bluesky"
    endpoint = "https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts"

    def search(self, query: str, query_id: str, limit: int = 10) -> list[DiscoveredItem]:
        payload = get_json(self.endpoint, {"q": query, "limit": min(limit, 25), "sort": "latest"})
        items = []
        for post in payload.get("posts", []):
            record = post.get("record") or {}
            author = post.get("author") or {}
            uri = post.get("uri", "")
            rkey = uri.rsplit("/", 1)[-1]
            handle = author.get("handle", "unknown")
            text = record.get("text", "").strip()
            items.append(DiscoveredItem(title=(text[:117] + "…") if len(text) > 120 else text or "Bluesky post",
                url=f"https://bsky.app/profile/{handle}/post/{rkey}", source_name="Bluesky",
                source_type="bluesky", publication_date=(record.get("createdAt") or "")[:10],
                authors=[author.get("displayName") or handle], platform_identifier=uri, abstract=text,
                evidence_types=["bluesky-post"], adapter=self.name, query_id=query_id, raw_metadata=post))
        return items
