"""
LangGraph workflow — assembles the 4 agent nodes into a linear pipeline.

Flow:  START → supervisor → ideation → prior_art → synthesis → END
"""
from __future__ import annotations
import time
from typing import Annotated, Any, Dict, List, Optional, Sequence
import operator

from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict

from agents.supervisor import run_supervisor
from agents.ideation   import run_ideation
from agents.prior_art  import run_prior_art
from agents.synthesis  import run_synthesis


# ──────────────────────────────────────────────────────────────────────────────
# Shared pipeline state
# ──────────────────────────────────────────────────────────────────────────────
class InnovationState(TypedDict):
    # ── Inputs ────────────────────────────────────────────────────────────────
    session_id:     str
    domain:         str
    problem_space:  str
    user_intent:    str
    depth:          str
    _start_ts:      float

    # ── Cumulative message log (append-only) ─────────────────────────────────
    messages: Annotated[List[Dict[str, Any]], operator.add]

    # ── Agent outputs ─────────────────────────────────────────────────────────
    supervisor_plan:    Dict[str, Any]
    innovation_concepts: List[Dict[str, Any]]
    prior_art_results:  List[Dict[str, Any]]
    novelty_assessment: Dict[str, Any]
    executive_summary:  str
    ip_readiness_score: float
    next_steps:         List[str]

    # ── Internal / debug ──────────────────────────────────────────────────────
    stage:          str
    error:          Optional[str]
    _final_output:  Optional[Dict[str, Any]]


# ──────────────────────────────────────────────────────────────────────────────
# Graph builder
# ──────────────────────────────────────────────────────────────────────────────
def build_graph():
    """Compile and return the LangGraph innovation pipeline."""
    graph = StateGraph(InnovationState)

    graph.add_node("supervisor", run_supervisor)
    graph.add_node("ideation",   run_ideation)
    graph.add_node("prior_art",  run_prior_art)
    graph.add_node("synthesis",  run_synthesis)

    graph.add_edge(START,        "supervisor")
    graph.add_edge("supervisor", "ideation")
    graph.add_edge("ideation",   "prior_art")
    graph.add_edge("prior_art",  "synthesis")
    graph.add_edge("synthesis",  END)

    return graph.compile()


# ──────────────────────────────────────────────────────────────────────────────
# Singleton
# ──────────────────────────────────────────────────────────────────────────────
_graph = None


def get_graph():
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph


def make_initial_state(
    session_id: str,
    domain: str,
    problem_space: str,
    user_intent: str,
    depth: str = "standard",
) -> InnovationState:
    return InnovationState(
        session_id=session_id,
        domain=domain,
        problem_space=problem_space,
        user_intent=user_intent,
        depth=depth,
        _start_ts=time.time(),
        messages=[],
        supervisor_plan={},
        innovation_concepts=[],
        prior_art_results=[],
        novelty_assessment={},
        executive_summary="",
        ip_readiness_score=0.0,
        next_steps=[],
        stage="supervisor",
        error=None,
        _final_output=None,
    )
