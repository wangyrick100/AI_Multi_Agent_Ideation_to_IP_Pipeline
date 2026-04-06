"""
Ideation Agent — structured innovation concept generator.

Uses knowledge-graph context + LLM reasoning to produce 3 rich,
IP-ready innovation concepts grounded in the supervisor's plan.
"""
from __future__ import annotations
import copy
import json
import logging
from typing import Any, Dict, List

from config import OPENAI_API_KEY, OPENAI_MODEL, USE_MOCK
from knowledge.knowledge_graph import get_knowledge_graph

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────────────────────
# Prompt
# ──────────────────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are an Innovation Ideation Agent with deep expertise in technology strategy and IP.

You receive:
1. A structured innovation plan from the Supervisor
2. A knowledge graph context summarising applicable technologies and patterns

Generate exactly 3 innovation concepts and output ONLY valid JSON — an array of 3 objects.
Each object must match this schema exactly:
{
  "title": "Short compelling title (max 10 words)",
  "description": "2–3 sentence description of the concept",
  "technical_approach": "Specific technical implementation (mention concrete algorithms/architectures)",
  "use_cases": ["Use case 1", "Use case 2", "Use case 3"],
  "implementation_pathway": "Step-by-step pathway from PoC to production (3–5 steps)",
  "strategic_positioning": "Market/competitive positioning rationale",
  "novelty_indicators": ["What makes this novel — indicator 1", "indicator 2", "indicator 3"]
}

Rules:
- Be technically specific: name algorithms, frameworks, and data modalities.
- Cross-domain connections score higher — explicitly link techniques from adjacent fields.
- Each concept must be genuinely distinct (different technical approach / target use-case).
- The novelty_indicators should be precise enough to inform a patent claim."""

# ──────────────────────────────────────────────────────────────────────────────
# Mock fallback data
# ──────────────────────────────────────────────────────────────────────────────
_MOCK_CONCEPTS: List[Dict[str, Any]] = [
    {
        "title": "Knowledge-Graph Augmented Adaptive Reasoning Engine",
        "description": (
            "A hybrid system that dynamically augments transformer-based language models "
            "with domain-specific knowledge graphs at inference time, enabling accurate "
            "chain-of-thought reasoning without retraining. "
            "The system continuously updates graph embeddings from new literature and expert feedback."
        ),
        "technical_approach": (
            "Combine a frozen LLM backbone (GPT-4 class) with a real-time graph attention network (GAT) "
            "that injects structured entity relationships via cross-attention layers. "
            "Use FAISS for sub-second nearest-neighbour retrieval from the knowledge graph embedding space."
        ),
        "use_cases": [
            "Clinical decision support with real-time medical literature grounding",
            "Regulatory compliance analysis with auto-updated legal knowledge graph",
            "R&D literature synthesis across multi-discipline research corpora",
        ],
        "implementation_pathway": (
            "1. Build domain knowledge graph from structured sources (Wikidata, PubMed MeSH). "
            "2. Train graph encoder (GraphSAGE) on entity-relationship triples. "
            "3. Implement cross-attention fusion layer between LLM and graph embeddings. "
            "4. Integrate retrieval pipeline with streaming KG updates. "
            "5. Deploy as a FastAPI microservice with LangChain tool integration."
        ),
        "strategic_positioning": (
            "Targets high-stakes regulated industries (healthcare, legal, finance) where "
            "factual accuracy is non-negotiable. Differentiates from RAG-only solutions by "
            "providing structured, traceable reasoning chains — a key requirement for auditable AI."
        ),
        "novelty_indicators": [
            "Real-time GAT-LLM cross-attention fusion at inference (not fine-tuning time)",
            "Dynamic knowledge graph updates integrated into the inference loop",
            "Structured provenance tracking linking each generation token to a graph node",
        ],
    },
    {
        "title": "Federated Innovation Network for Privacy-First Co-Development",
        "description": (
            "A federated learning framework that enables multiple organisations to collaboratively "
            "train specialised generative models without sharing raw data. "
            "Secure aggregation and differential privacy guarantees allow competing institutions "
            "to co-build IP-grade models while retaining full data sovereignty."
        ),
        "technical_approach": (
            "Uses FedAvg / FedProx for gradient aggregation with DP-SGD noise injection. "
            "Secure multi-party computation (SMPC) ensures aggregation server never sees individual "
            "gradients. Model personalisation via Federated Meta-Learning (Per-FedAvg) adapts the "
            "global model to each institution's data distribution."
        ),
        "use_cases": [
            "Multi-hospital rare-disease model training without patient data sharing",
            "Cross-bank fraud detection with shared threat intelligence, zero data exposure",
            "Collaborative drug-target interaction prediction across pharma consortia",
        ],
        "implementation_pathway": (
            "1. Define the federated data schema and privacy budget (ε, δ parameters). "
            "2. Implement local training loop with DP-SGD using PyTorch Opacus. "
            "3. Deploy secure aggregation server using PySyft or TensorFlow Federated. "
            "4. Add personalisation layer with Per-FedAvg fine-tuning on local data. "
            "5. Certify with ISO 27001 controls and GDPR Article 25 compliance audit."
        ),
        "strategic_positioning": (
            "Addresses the core contradiction in AI development: data-hungry models vs. "
            "privacy regulations. Uniquely applicable to consortium-style markets (banking, "
            "pharma, healthcare networks) where no single player owns sufficient data alone."
        ),
        "novelty_indicators": [
            "Combination of SMPC + DP-SGD + per-client personalisation in a single pipeline",
            "Application of federated meta-learning to generative model fine-tuning",
            "Automated privacy budget allocation across heterogeneous institutional data distributions",
        ],
    },
    {
        "title": "Self-Calibrating Explainable AI Decision Fabric",
        "description": (
            "An adaptive inference layer that wraps any black-box model and generates "
            "human-interpretable, confidence-calibrated explanations at decision time. "
            "The system learns task-specific explanation templates from domain expert feedback and "
            "continuously improves calibration via reinforcement learning from human ratings."
        ),
        "technical_approach": (
            "Integrates SHAP / integrated-gradients attribution with a learned explanation "
            "generator (fine-tuned T5 / GPT). A calibration module uses Platt Scaling + "
            "isotonic regression to ensure predicted confidence matches empirical accuracy. "
            "RLHF loop refines explanation quality using domain expert preference scores."
        ),
        "use_cases": [
            "Loan approval explanations meeting EU AI Act transparency requirements",
            "Radiology AI second-opinion tool with radiologist-grade explanation quality",
            "Software vulnerability prioritisation with security engineer–readable rationale",
        ],
        "implementation_pathway": (
            "1. Instrument target model with SHAP / IG attribution hooks. "
            "2. Fine-tune explanation generator on domain-specific (input, attribution, explanation) triples. "
            "3. Implement calibration module with held-out validation set. "
            "4. Build RLHF annotation interface for expert preference collection. "
            "5. Deploy as a model-agnostic middleware layer (REST / gRPC)."
        ),
        "strategic_positioning": (
            "Directly addresses EU AI Act Article 13 (transparency) and sector-specific "
            "explainability mandates (EBA guidelines, FDA SaMD guidance). "
            "Model-agnostic design enables rapid adoption on top of existing deployments, "
            "reducing platform lock-in and accelerating enterprise sales cycles."
        ),
        "novelty_indicators": [
            "RLHF-driven explanation quality optimisation (not static post-hoc explanations)",
            "Unified calibration + attribution + natural language generation in one inference call",
            "Domain-adaptive explanation templates learned from expert feedback without retraining the base model",
        ],
    },
]


# ──────────────────────────────────────────────────────────────────────────────
# Agent node function (called by LangGraph)
# ──────────────────────────────────────────────────────────────────────────────
async def run_ideation(state: Dict[str, Any]) -> Dict[str, Any]:
    """LangGraph node: generate innovation concepts."""
    from events import emit

    session_id      = state["session_id"]
    domain          = state["domain"]
    problem_space   = state["problem_space"]
    supervisor_plan = state.get("supervisor_plan", {})

    await emit(session_id, {
        "type":    "agent_start",
        "agent":   "ideation",
        "message": "Querying knowledge graph and generating innovation concepts…",
    })

    # Build graph context
    keywords = domain.split() + problem_space.split()[:6]
    kg = get_knowledge_graph()
    kg_context = kg.build_context_summary(keywords)

    await emit(session_id, {
        "type":    "agent_progress",
        "agent":   "ideation",
        "message": f"Knowledge graph context built. Generating concepts with LLM…",
        "data":    {"kg_context": kg_context},
    })

    concepts = await _generate_concepts(domain, problem_space, supervisor_plan, kg_context)

    await emit(session_id, {
        "type":    "agent_complete",
        "agent":   "ideation",
        "message": f"{len(concepts)} innovation concepts generated.",
        "data":    {"concepts": concepts},
    })

    return {
        "innovation_concepts": concepts,
        "messages": [{"role": "ideation", "content": f"{len(concepts)} concepts generated"}],
        "stage": "prior_art",
    }


# ──────────────────────────────────────────────────────────────────────────────
# LLM / mock logic
# ──────────────────────────────────────────────────────────────────────────────
async def _generate_concepts(
    domain: str,
    problem_space: str,
    plan: Dict[str, Any],
    kg_context: str,
) -> List[Dict[str, Any]]:
    if USE_MOCK:
        logger.info("Ideation: using mock concepts (no API key)")
        # Personalise titles to user's domain
        mocks = copy.deepcopy(_MOCK_CONCEPTS)
        mocks[0]["title"] = f"Knowledge-Graph Augmented Reasoning for {domain}"
        return mocks

    user_msg = (
        f"Domain: {domain}\n"
        f"Problem space: {problem_space}\n\n"
        f"Supervisor strategic plan:\n{json.dumps(plan, indent=2)}\n\n"
        f"Knowledge graph context:\n{kg_context}"
    )
    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import SystemMessage, HumanMessage

        llm = ChatOpenAI(
            model=OPENAI_MODEL,
            api_key=OPENAI_API_KEY,
            temperature=0.85,
            response_format={"type": "json_object"},
        )
        # Ask for a JSON object containing "concepts" array
        patched_prompt = SYSTEM_PROMPT + '\n\nReturn {"concepts": [<3 concept objects>]}'
        response = await llm.ainvoke(
            [SystemMessage(content=patched_prompt), HumanMessage(content=user_msg)]
        )
        parsed = json.loads(response.content)
        return parsed.get("concepts", parsed) if isinstance(parsed, dict) else parsed
    except Exception as exc:
        logger.warning("Ideation LLM error — falling back to mock: %s", exc)
        return copy.deepcopy(_MOCK_CONCEPTS)
