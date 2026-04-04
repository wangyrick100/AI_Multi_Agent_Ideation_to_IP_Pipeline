"""
Semantic Scholar open-access paper search tool.
No API key required for basic searches.
"""
from __future__ import annotations
import logging
from typing import Any, Dict, List

import httpx

logger = logging.getLogger(__name__)

_BASE_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
_FIELDS   = "title,authors,year,abstract,externalIds,url"


async def search_semantic_scholar(
    query: str,
    max_results: int = 5,
) -> List[Dict[str, Any]]:
    """Search Semantic Scholar and return normalised paper dicts."""
    params: Dict[str, Any] = {
        "query":  query,
        "fields": _FIELDS,
        "limit":  max_results,
    }
    headers = {"User-Agent": "InnovationPipelineAgent/1.0"}

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.get(_BASE_URL, params=params, headers=headers)
            resp.raise_for_status()
            data = resp.json()
    except Exception as exc:
        logger.warning("Semantic Scholar search error: %s", exc)
        return []

    results: List[Dict[str, Any]] = []
    for paper in data.get("data", []):
        authors = [a.get("name", "") for a in paper.get("authors", [])][:4]
        year    = paper.get("year") or 0
        abstract = paper.get("abstract") or ""
        url = paper.get("url") or ""
        if not url:
            ext = paper.get("externalIds", {})
            doi = ext.get("DOI", "")
            url = f"https://doi.org/{doi}" if doi else ""

        results.append(
            {
                "title":   paper.get("title", "Untitled"),
                "authors": authors,
                "year":    year,
                "source":  "semantic_scholar",
                "summary": abstract[:600],
                "url":     url,
            }
        )
    return results
