"""
Synthesis Agent — IP-readiness report generator.

Takes ideation concepts + prior art analysis and produces:
  - Holistic novelty assessment (score + rating)
  - Executive summary
  - IP-readiness score
  - Actionable next steps for filing
"""
from __future__ import annotations
import copy
import json
import logging
import time
from typing import Any, Dict, List

from config import OPENAI_API_KEY, OPENAI_MODEL, USE_MOCK

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────────────────────
# Prompt
# ──────────────────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are a Senior IP Strategist and Innovation Analyst.

You receive a set of innovation concepts and their prior art analysis.
Your task is to produce a comprehensive IP-readiness report.

Output ONLY valid JSON matching this schema exactly:
{
  "novelty_assessment": {
    "overall_score": <float 0–100>,
    "rating": "<'High' | 'Medium' | 'Low'>",
    "key_differentiators": ["<differentiator 1>", "<differentiator 2>", "<differentiator 3>"],
    "risk_areas": ["<risk 1>", "<risk 2>"],
    "recommendation": "<1–2 sentence recommendation>"
  },
  "executive_summary": "<3–4 paragraphs summarising the innovation opportunity, novelty finding, strategic value, and recommended path>",
  "ip_readiness_score": <float 0–100>,
  "next_steps": [
    "<Actionable step 1>",
    "<Actionable step 2>",
    "<Actionable step 3>",
    "<Actionable step 4>"
  ]
}

Scoring guidelines:
- ip_readiness_score > 75: Strong — proceed to provisional filing
- ip_readiness_score 50–75: Moderate — refine claims, conduct deeper search
- ip_readiness_score < 50: Risk — significant prior art; recommend design-around
"""

# ──────────────────────────────────────────────────────────────────────────────
# Mock fallback
# ──────────────────────────────────────────────────────────────────────────────
_MOCK_SYNTHESIS: Dict[str, Any] = {
    "novelty_assessment": {
        "overall_score": 78.5,
        "rating": "High",
        "key_differentiators": [
            "Real-time knowledge-graph fusion inside LLM attention layers (not post-hoc retrieval)",
            "RLHF-calibrated explanation generation producing expert-grade natural language rationale",
            "Federated meta-learning combining differential privacy with per-client personalisation",
        ],
        "risk_areas": [
            "RAG and retrieval-augmented LLMs are well-covered in prior art — claims must focus on the graph fusion mechanism",
            "FedAvg and DP-SGD are foundational work; filing must emphasise the personalisation + aggregation combination",
        ],
        "recommendation": (
            "Proceed to provisional patent filing within 90 days. "
            "Focus claims on the novel cross-attention graph fusion mechanism and the RLHF explanation calibration loop, "
            "as these have the strongest differentiation from existing prior art."
        ),
    },
    "executive_summary": (
        "The analysed innovation portfolio demonstrates a high-novelty cluster at the intersection of "
        "structured knowledge reasoning and large-scale generative AI — a space that is rapidly growing "
        "yet remains largely under-patented at the architectural level. "
        "The three concepts collectively address a fundamental gap: existing systems either generate "
        "content (LLMs) or retrieve knowledge (RAG/KG), but none fuse structured graph relationships "
        "directly into the generation attention mechanism at inference time.\n\n"
        "Prior art analysis identified relevant foundational work (RAG, GAT, FedAvg, SHAP) but confirmed "
        "that no existing filing or publication describes the specific architectural combinations proposed here. "
        "The highest-risk area is the retrieval-augmented generation space, where broad claims by "
        "Meta AI, Google, and Microsoft are present — however, the concept's focus on graph-attention "
        "fusion (rather than document retrieval) provides clear differentiation.\n\n"
        "The federated learning concept carries moderate novelty risk given active filing activity in "
        "this space, but the combination of differential privacy + meta-learning personalisation "
        "represents a defensible and practically significant contribution. Similarly, the explainable AI "
        "concept's RLHF calibration loop is genuinely novel and directly addressable by a tight method claim.\n\n"
        "Strategic recommendation: file provisional applications for all three concepts within 90 days "
        "to establish priority dates, then conduct a full Freedom-to-Operate (FTO) analysis before "
        "proceeding to non-provisional filings. The knowledge-graph fusion concept offers the strongest "
        "standalone claim set and should be prioritised."
    ),
    "ip_readiness_score": 78.5,
    "next_steps": [
        "File provisional patent applications for all 3 concepts within 90 days to establish priority dates",
        "Engage a patent attorney specialising in AI/ML for claim drafting — focus on method claims for the KG-attention fusion layer",
        "Conduct a Freedom-to-Operate (FTO) analysis specifically targeting Meta AI RAG patents and Google Brain knowledge graph filings",
        "Build a working PoC for the Knowledge-Graph Augmented Reasoning Engine to strengthen the 'reduction to practice' position",
        "Document all technical decisions, architectural diagrams, and experimental results in a lab notebook with timestamped entries",
    ],
}


# ──────────────────────────────────────────────────────────────────────────────
# Agent node function
# ──────────────────────────────────────────────────────────────────────────────
async def run_synthesis(state: Dict[str, Any]) -> Dict[str, Any]:
    """LangGraph node: synthesise final IP-readiness report."""
    from events import emit

    session_id    = state["session_id"]
    concepts      = state.get("innovation_concepts", [])
    prior_art     = state.get("prior_art_results", [])
    start_ts      = state.get("_start_ts", time.time())

    await emit(session_id, {
        "type":    "agent_start",
        "agent":   "synthesis",
        "message": "Synthesising novelty assessment and IP-readiness report…",
    })

    synthesis = await _generate_synthesis(concepts, prior_art)
    processing_time = round(time.time() - start_ts, 2)

    # Build final output dict
    final_output = {
        "session_id":          state["session_id"],
        "domain":              state["domain"],
        "problem_space":       state["problem_space"],
        "innovation_concepts": concepts,
        "prior_art_results":   prior_art,
        "novelty_assessment":  synthesis["novelty_assessment"],
        "executive_summary":   synthesis["executive_summary"],
        "ip_readiness_score":  synthesis["ip_readiness_score"],
        "next_steps":          synthesis["next_steps"],
        "processing_time":     processing_time,
        "demo_mode":           USE_MOCK,
    }

    await emit(session_id, {
        "type":    "agent_complete",
        "agent":   "synthesis",
        "message": (
            f"IP-readiness report complete. "
            f"Score: {synthesis['ip_readiness_score']:.0f}/100 — "
            f"{synthesis['novelty_assessment']['rating']} novelty."
        ),
        "data": final_output,
    })

    # Signal pipeline complete
    await emit(session_id, {
        "type":    "pipeline_complete",
        "agent":   "synthesis",
        "message": "Pipeline complete.",
        "data":    final_output,
    })

    return {
        "novelty_assessment":  synthesis["novelty_assessment"],
        "executive_summary":   synthesis["executive_summary"],
        "ip_readiness_score":  synthesis["ip_readiness_score"],
        "next_steps":          synthesis["next_steps"],
        "messages":            [{"role": "synthesis", "content": "Report complete"}],
        "stage":               "complete",
        "_final_output":       final_output,
    }


# ──────────────────────────────────────────────────────────────────────────────
# LLM / mock logic
# ──────────────────────────────────────────────────────────────────────────────
async def _generate_synthesis(
    concepts: List[Dict[str, Any]],
    prior_art: List[Dict[str, Any]],
) -> Dict[str, Any]:
    if USE_MOCK:
        logger.info("Synthesis: using mock report (no API key)")
        return copy.deepcopy(_MOCK_SYNTHESIS)

    user_msg = (
        f"Innovation concepts:\n{json.dumps(concepts, indent=2)}\n\n"
        f"Prior art analysis:\n{json.dumps(prior_art, indent=2)}"
    )
    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import SystemMessage, HumanMessage

        llm = ChatOpenAI(
            model=OPENAI_MODEL,
            api_key=OPENAI_API_KEY,
            temperature=0.4,
            response_format={"type": "json_object"},
        )
        response = await llm.ainvoke(
            [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=user_msg)]
        )
        return json.loads(response.content)
    except Exception as exc:
        logger.warning("Synthesis LLM error — falling back to mock: %s", exc)
        return copy.deepcopy(_MOCK_SYNTHESIS)
