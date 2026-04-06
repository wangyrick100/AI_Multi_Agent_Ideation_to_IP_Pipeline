"""
Supervisor Agent — ReAct-style orchestration planner.

Analyses the user's innovation brief and produces a structured plan that
guides the Ideation and Prior Art agents in the downstream pipeline.
"""
from __future__ import annotations
import copy
import json
import logging
from typing import Any, Dict

from config import OPENAI_API_KEY, OPENAI_MODEL, USE_MOCK

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────────────────────
# Prompt
# ──────────────────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are an Innovation Intelligence Orchestrator — a senior strategic AI planner.
Your role is to analyse an innovation brief and create a precise, actionable plan for downstream agents.

Output ONLY valid JSON (no markdown fences) matching this schema:
{
  "focus_areas": ["<area1>", "<area2>", "<area3>"],
  "innovation_angles": ["<angle1>", "<angle2>", "<angle3>"],
  "validation_priorities": ["<priority1>", "<priority2>"],
  "search_queries": ["<query1>", "<query2>", "<query3>"],
  "strategy": "<one-paragraph strategic framing>"
}

Rules:
- focus_areas:  3-4 specific sub-problems or opportunity spaces within the domain
- innovation_angles: 3-4 novel directions to explore (cross-domain, new tech combos, etc.)
- validation_priorities: 2-3 things that matter most for IP defensibility
- search_queries: 3 tight keyword queries for prior-art paper search (no generic terms)
- strategy: explain WHY these angles are promising and how they connect to trends"""

# ──────────────────────────────────────────────────────────────────────────────
# Mock fallback
# ──────────────────────────────────────────────────────────────────────────────
_MOCK_PLAN: Dict[str, Any] = {
    "focus_areas": [
        "Real-time adaptive knowledge synthesis using transformer architectures",
        "Privacy-preserving cross-institutional data collaboration",
        "Explainable AI-driven decision support for domain experts",
        "Self-improving feedback loops via reinforcement from human interaction",
    ],
    "innovation_angles": [
        "Apply knowledge graph augmentation to reduce hallucination in domain-specific LLMs",
        "Use federated learning to enable multi-party innovation without data exposure",
        "Combine contrastive representation learning with retrieval-augmented generation",
        "Transfer learning from adjacent high-data domains to data-scarce target domains",
    ],
    "validation_priorities": [
        "Novelty of multi-modal knowledge graph + generative AI fusion",
        "Technical differentiation in privacy-preserving collaborative inference",
        "IP defensibility of the adaptive feedback architecture",
    ],
    "search_queries": [
        "knowledge graph augmented language model domain adaptation",
        "federated learning privacy preserving generative model",
        "retrieval augmented generation cross domain transfer learning",
    ],
    "strategy": (
        "The most defensible innovation opportunity lies at the intersection of "
        "structured knowledge reasoning (knowledge graphs) and unstructured "
        "text generation (LLMs), combined with privacy-first collaboration architectures. "
        "This space is rapidly growing yet under-patented, making it ideal for IP filing."
    ),
}


# ──────────────────────────────────────────────────────────────────────────────
# Agent node function (called by LangGraph)
# ──────────────────────────────────────────────────────────────────────────────
async def run_supervisor(state: Dict[str, Any]) -> Dict[str, Any]:
    """LangGraph node: plan the innovation pipeline."""
    from events import emit

    session_id   = state["session_id"]
    domain       = state["domain"]
    problem_space = state["problem_space"]
    user_intent  = state["user_intent"]

    await emit(session_id, {
        "type":    "agent_start",
        "agent":   "supervisor",
        "message": "Analysing innovation brief and creating strategic plan…",
    })

    plan = await _generate_plan(domain, problem_space, user_intent)

    await emit(session_id, {
        "type":    "agent_complete",
        "agent":   "supervisor",
        "message": f"Strategic plan ready — {len(plan['focus_areas'])} focus areas identified.",
        "data":    plan,
    })

    return {
        "supervisor_plan": plan,
        "messages": [{"role": "supervisor", "content": json.dumps(plan)}],
        "stage": "ideation",
    }


# ──────────────────────────────────────────────────────────────────────────────
# LLM / mock logic
# ──────────────────────────────────────────────────────────────────────────────
async def _generate_plan(domain: str, problem_space: str, user_intent: str) -> Dict[str, Any]:
    if USE_MOCK:
        logger.info("Supervisor: using mock plan (no API key)")
        plan = copy.deepcopy(_MOCK_PLAN)
        # Inject user's actual domain into the mock for relevance
        plan["focus_areas"][0] = f"Structured innovation intelligence for {domain}"
        return plan

    user_msg = (
        f"Domain: {domain}\n"
        f"Problem space: {problem_space}\n"
        f"User intent: {user_intent}"
    )
    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import SystemMessage, HumanMessage

        llm = ChatOpenAI(
            model=OPENAI_MODEL,
            api_key=OPENAI_API_KEY,
            temperature=0.7,
            response_format={"type": "json_object"},
        )
        response = await llm.ainvoke(
            [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=user_msg)]
        )
        return json.loads(response.content)
    except Exception as exc:
        logger.warning("Supervisor LLM error — falling back to mock: %s", exc)
        return copy.deepcopy(_MOCK_PLAN)
