"""
Prior Art Search Agent — novelty validation layer.

For each innovation concept it:
  1. Builds targeted search queries
  2. Searches arXiv and Semantic Scholar in parallel
  3. Scores relevance and surfaces key differences
"""
from __future__ import annotations
import asyncio
import copy
import json
import logging
from typing import Any, Dict, List

from config import (
    ARXIV_MAX_RESULTS,
    OPENAI_API_KEY,
    OPENAI_MODEL,
    SEMANTIC_SCHOLAR_MAX_RESULTS,
    USE_MOCK,
)
from tools.arxiv_search import search_arxiv
from tools.semantic_scholar import search_semantic_scholar

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────────────────────
# Relevance-scoring prompt
# ──────────────────────────────────────────────────────────────────────────────
SCORING_PROMPT = """You are a patent analyst scoring prior-art relevance.

Given an innovation concept and a paper abstract, output ONLY valid JSON:
{
  "relevance_score": <float 0.0–1.0>,
  "key_differences": "<one sentence: how the concept differs from or advances beyond this paper>"
}

A score of 1.0 means the paper describes the exact same idea.
A score below 0.3 means the paper is only tangentially related."""

# ──────────────────────────────────────────────────────────────────────────────
# Mock fallback
# ──────────────────────────────────────────────────────────────────────────────
_MOCK_PRIOR_ART: List[Dict[str, Any]] = [
    {
        "title":           "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks",
        "authors":         ["Patrick Lewis", "Ethan Perez", "Aleksandra Piktus"],
        "year":            2020,
        "source":          "arxiv",
        "relevance_score": 0.65,
        "summary":         (
            "We explore RAG models which combine parametric and non-parametric memory for "
            "language generation, showing strong performance on knowledge-intensive tasks."
        ),
        "url":             "https://arxiv.org/abs/2005.11401",
        "key_differences": (
            "The concept extends RAG by fusing structured knowledge-graph entity embeddings "
            "at each attention layer, providing traceable provenance not available in the original RAG."
        ),
    },
    {
        "title":           "Graph Attention Networks",
        "authors":         ["Petar Veličković", "Guillem Cucurull", "Arantxa Casanova"],
        "year":            2018,
        "source":          "arxiv",
        "relevance_score": 0.52,
        "summary":         (
            "We present graph attention networks (GATs), novel neural network architectures "
            "that operate on graph-structured data using masked self-attentional layers."
        ),
        "url":             "https://arxiv.org/abs/1710.10903",
        "key_differences": (
            "The concept applies GAT inside an LLM cross-attention layer at inference time "
            "rather than as a standalone graph classification model."
        ),
    },
    {
        "title":           "Communication-Efficient Learning of Deep Networks from Decentralized Data",
        "authors":         ["H. Brendan McMahan", "Eider Moore", "Daniel Ramage"],
        "year":            2017,
        "source":          "semantic_scholar",
        "relevance_score": 0.58,
        "summary":         (
            "The FedAvg algorithm combines local stochastic gradient descent on each client "
            "with a server that performs model averaging for federated learning."
        ),
        "url":             "https://arxiv.org/abs/1602.05629",
        "key_differences": (
            "The concept adds differential privacy guarantees and per-client meta-learning "
            "personalisation, going well beyond the original aggregation-only FedAvg approach."
        ),
    },
    {
        "title":           "Deep SHAP: Explaining the Predictions of a Machine-Learning Model",
        "authors":         ["Scott Lundberg", "Su-In Lee"],
        "year":            2017,
        "source":          "semantic_scholar",
        "relevance_score": 0.44,
        "summary":         (
            "SHAP (SHapley Additive exPlanations) unifies several explanation methods and "
            "provides feature importance values with desirable consistency properties."
        ),
        "url":             "https://arxiv.org/abs/1705.07874",
        "key_differences": (
            "The concept wraps SHAP attribution with an NLG layer and an RLHF calibration loop, "
            "transforming raw shapley values into domain-expert–grade natural language rationale."
        ),
    },
]


# ──────────────────────────────────────────────────────────────────────────────
# Agent node function
# ──────────────────────────────────────────────────────────────────────────────
async def run_prior_art(state: Dict[str, Any]) -> Dict[str, Any]:
    """LangGraph node: search and score prior art for each concept."""
    from events import emit

    session_id = state["session_id"]
    concepts   = state.get("innovation_concepts", [])
    supervisor_plan = state.get("supervisor_plan", {})
    search_queries  = supervisor_plan.get("search_queries", [])

    await emit(session_id, {
        "type":    "agent_start",
        "agent":   "prior_art",
        "message": f"Searching academic prior art for {len(concepts)} concepts…",
    })

    if USE_MOCK:
        # In demo mode rotate through the mock papers so each concept gets a
        # stable, concept-specific sample without mutating shared state.
        results = []
        for i, concept in enumerate(concepts[:3]):
            slice_start = (i * 2) % len(_MOCK_PRIOR_ART)
            mocks = _MOCK_PRIOR_ART[slice_start:slice_start + 2]
            if len(mocks) < 2:
                mocks += _MOCK_PRIOR_ART[: 2 - len(mocks)]
            results.append({
                "concept_index": i,
                "concept_title": concept.get("title", f"Concept {i+1}"),
                "results": copy.deepcopy(mocks),
            })
        await emit(session_id, {
            "type":    "agent_complete",
            "agent":   "prior_art",
            "message": f"Prior art search complete (demo mode). {sum(len(r['results']) for r in results)} papers found.",
            "data":    {"prior_art_results": results},
        })
        return {
            "prior_art_results": results,
            "messages": [{"role": "prior_art", "content": "Prior art search complete (demo)"}],
            "stage": "synthesis",
        }

    # Live mode: search in parallel per concept
    results = []
    for i, concept in enumerate(concepts):
        await emit(session_id, {
            "type":    "agent_progress",
            "agent":   "prior_art",
            "message": f"Searching prior art for concept {i+1}/{len(concepts)}: {concept.get('title','')[:60]}…",
        })

        # Build concept-level search query
        title   = concept.get("title", "")
        tech    = concept.get("technical_approach", "")[:120]
        query   = f"{title} {tech}"
        if search_queries:
            query = search_queries[min(i, len(search_queries) - 1)]

        # Parallel search
        arxiv_hits, ss_hits = await asyncio.gather(
            search_arxiv(query, ARXIV_MAX_RESULTS),
            search_semantic_scholar(query, SEMANTIC_SCHOLAR_MAX_RESULTS),
        )
        raw_papers = (arxiv_hits + ss_hits)[:8]

        # Score each paper with LLM
        scored = await _score_papers(concept, raw_papers)
        scored.sort(key=lambda p: p["relevance_score"], reverse=True)

        results.append({
            "concept_index": i,
            "concept_title": concept.get("title", f"Concept {i+1}"),
            "results":       scored[:5],
        })

    await emit(session_id, {
        "type":    "agent_complete",
        "agent":   "prior_art",
        "message": f"Prior art search complete. {sum(len(r['results']) for r in results)} papers analysed.",
        "data":    {"prior_art_results": results},
    })

    return {
        "prior_art_results": results,
        "messages": [{"role": "prior_art", "content": "Prior art search complete"}],
        "stage": "synthesis",
    }


async def _score_papers(
    concept: Dict[str, Any],
    papers: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Score each paper's relevance to the concept using LLM (with fallback)."""
    if not papers:
        return []

    score_payloads = await asyncio.gather(
        *(_score_single_paper(concept, paper) for paper in papers)
    )
    return [{**paper, **score_data} for paper, score_data in zip(papers, score_payloads)]


async def _score_single_paper(
    concept: Dict[str, Any],
    paper: Dict[str, Any],
) -> Dict[str, Any]:
    default = {"relevance_score": 0.4, "key_differences": "Concept extends this work with novel technical contributions."}
    if USE_MOCK:
        return default

    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import SystemMessage, HumanMessage

        llm = ChatOpenAI(
            model=OPENAI_MODEL,
            api_key=OPENAI_API_KEY,
            temperature=0.2,
            response_format={"type": "json_object"},
        )
        user_msg = (
            f"Innovation concept: {concept.get('title','')}\n"
            f"Technical approach: {concept.get('technical_approach','')[:200]}\n\n"
            f"Paper title: {paper.get('title','')}\n"
            f"Abstract: {paper.get('summary','')[:400]}"
        )
        response = await llm.ainvoke(
            [SystemMessage(content=SCORING_PROMPT), HumanMessage(content=user_msg)]
        )
        return json.loads(response.content)
    except Exception as exc:
        logger.warning("Prior art scoring LLM error: %s", exc)
        return default
