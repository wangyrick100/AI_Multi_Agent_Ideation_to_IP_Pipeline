"""
arXiv academic paper search tool.
Uses the arxiv Python library (falls back to REST if library unavailable).
"""
from __future__ import annotations
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Any

logger = logging.getLogger(__name__)
_executor = ThreadPoolExecutor(max_workers=2)


def _sync_search(query: str, max_results: int) -> List[Dict[str, Any]]:
    """Blocking arXiv search – runs in a thread-pool executor."""
    try:
        import arxiv

        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance,
        )
        results: List[Dict[str, Any]] = []
        client = arxiv.Client(num_retries=2, delay_seconds=1)
        for paper in client.results(search):
            results.append(
                {
                    "title": paper.title,
                    "authors": [a.name for a in paper.authors][:4],
                    "year": paper.published.year if paper.published else 0,
                    "source": "arxiv",
                    "summary": paper.summary[:600] if paper.summary else "",
                    "url": paper.entry_id,
                }
            )
        return results
    except Exception as exc:
        logger.warning("arXiv search error: %s", exc)
        return []


async def search_arxiv(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """Async wrapper around the blocking arXiv search."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(_executor, _sync_search, query, max_results)
