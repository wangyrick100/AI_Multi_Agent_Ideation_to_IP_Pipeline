"""
Seed data for the innovation knowledge graph.

This module centralizes the domain taxonomy so the graph can be expanded
without scattering hidden relationships across the codebase.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Sequence

Node = Dict[str, Any]
Edge = Dict[str, str]
_VALID_STRENGTHS = {"low", "medium", "high"}


def _normalize_tags(tags: Sequence[str]) -> List[str]:
    return sorted({tag.strip().lower() for tag in tags if tag and tag.strip()})


def _node(node_id: str, label: str, tags: Sequence[str], description: str) -> Node:
    return {
        "id": node_id,
        "label": label,
        "tags": _normalize_tags(tags),
        "description": description,
    }


def _edge(from_id: str, to_id: str, relation: str, strength: str = "medium") -> Edge:
    if strength not in _VALID_STRENGTHS:
        raise ValueError(f"Unsupported edge strength: {strength}")
    return {"from": from_id, "to": to_id, "relation": relation, "strength": strength}


TECHNOLOGY_NODES: List[Node] = [
    _node("ai_ml", "AI / Machine Learning", ["ai", "ml", "machine learning", "predictive analytics", "deep learning", "neural network"], "General predictive and learning systems."),
    _node("nlp", "Natural Language Processing", ["nlp", "language", "text", "llm", "transformer", "document intelligence"], "Language understanding and generation."),
    _node("computer_vision", "Computer Vision", ["vision", "image", "video", "inspection", "detection", "ocr"], "Image and video perception workflows."),
    _node("federated_learn", "Federated Learning", ["federated", "privacy", "distributed training", "cross-silo"], "Distributed model training without centralizing data."),
    _node("knowledge_graph", "Knowledge Graphs", ["knowledge graph", "graph", "ontology", "semantic reasoning", "entity resolution"], "Structured entity and relationship grounding."),
    _node("iot", "Internet of Things", ["iot", "sensor", "telemetry", "connected device", "industrial sensor"], "Connected sensing and telemetry systems."),
    _node("blockchain", "Blockchain / DLT", ["blockchain", "distributed ledger", "smart contract", "traceability"], "Tamper-evident records and distributed trust."),
    _node("robotics", "Robotics & Automation", ["robotics", "robot", "automation", "cobot", "motion control"], "Physical automation and actuation."),
    _node("quantum", "Quantum Computing", ["quantum", "qubit", "annealing", "quantum simulation"], "Quantum-native optimization and simulation."),
    _node("ar_vr", "AR / VR / Mixed Reality", ["ar", "vr", "xr", "immersive", "spatial computing"], "Spatial and immersive interaction."),
    _node("edge_compute", "Edge Computing", ["edge", "on-device", "low latency", "fog computing", "local inference"], "Distributed compute near the data source."),
    _node("reinforcement_rl", "Reinforcement Learning", ["rl", "reinforcement learning", "reward", "policy optimization"], "Sequential decision optimization."),
    _node("generative_ai", "Generative AI", ["generative ai", "diffusion", "gan", "llm", "synthetic data"], "Content and representation synthesis."),
    _node("digital_twin", "Digital Twins", ["digital twin", "simulation", "virtual replica", "asset twin"], "Virtual operational replicas."),
    _node("time_series", "Time-Series Analytics", ["time series", "forecasting", "sequence modeling", "trend analysis"], "Temporal modeling for planning and anomalies."),
    _node("optimization", "Optimization & OR", ["optimization", "operations research", "routing", "scheduling", "resource allocation"], "Constraint-aware planning and allocation."),
]

DOMAIN_NODES: List[Node] = [
    _node("healthcare", "Healthcare & Life Sciences", ["healthcare", "health", "medical", "clinical", "hospital", "patient", "ehr", "pharma"], "Clinical care and life-science workflows."),
    _node("clean_energy", "Clean Energy & Climate Tech", ["energy", "utility", "solar", "wind", "grid", "battery", "carbon", "climate"], "Energy systems, carbon intelligence, and climate operations."),
    _node("fintech", "FinTech & Financial Services", ["fintech", "finance", "banking", "payments", "credit", "insurance", "fraud", "lending"], "Transactions, risk, and regulated finance workflows."),
    _node("manufacturing", "Smart Manufacturing / Industry 4.0", ["manufacturing", "factory", "industry 4.0", "industrial", "quality", "production", "plant"], "Industrial operations and asset-heavy environments."),
    _node("agritech", "AgriTech & Food Systems", ["agritech", "agriculture", "crop", "farm", "soil", "livestock", "precision agriculture"], "Agricultural productivity and food-system resilience."),
    _node("edtech", "EdTech & Learning", ["edtech", "education", "learning", "training", "curriculum", "assessment", "tutoring"], "Learning, training, and workforce development."),
    _node("cybersecurity", "Cybersecurity", ["cybersecurity", "security", "threat", "identity", "authentication", "vulnerability", "zero trust"], "Threat detection, identity, and cyber resilience."),
    _node("logistics", "Logistics & Supply Chain", ["logistics", "shipping", "warehouse", "route", "inventory", "fulfillment", "fleet", "transportation"], "Movement of goods, fleet operations, and fulfillment."),
    _node("smart_cities", "Smart Cities & Urban Tech", ["smart city", "urban", "traffic", "infrastructure", "mobility", "public transit", "utilities"], "Urban infrastructure and mobility systems."),
    _node("retail", "Retail & E-commerce", ["retail", "ecommerce", "merchandising", "pricing", "recommendation", "customer", "store operations"], "Customer experience and commerce operations."),
    _node("legaltech", "LegalTech", ["legaltech", "legal", "contract", "case law", "document review", "ediscovery"], "Legal analysis, contracts, and document-heavy workflows."),
    _node("public_sector", "Public Sector & GovTech", ["government", "public sector", "municipal", "civic", "social services", "public administration"], "Government operations and civic service delivery."),
    _node("telecom", "Telecommunications", ["telecom", "telecommunications", "network operations", "5g", "carrier", "connectivity"], "Carrier networks and service assurance."),
]

PROBLEM_NODES: List[Node] = [
    _node("data_silos", "Data Silos & Fragmentation", ["data silos", "fragmentation", "isolated systems", "data integration"], "Critical data is spread across disconnected systems."),
    _node("real_time", "Real-Time Decision Making", ["real-time", "latency", "streaming decisions", "online inference"], "Value depends on low-latency sensing and action."),
    _node("personalization", "Personalization at Scale", ["personalization", "recommendation", "adaptive experience", "customization"], "Systems must adapt to each user without losing efficiency."),
    _node("anomaly_detect", "Anomaly Detection", ["anomaly detection", "outlier", "fraud detection", "fault detection", "threat detection"], "Rare and high-risk events must be surfaced quickly."),
    _node("pred_maintenance", "Predictive Maintenance", ["predictive maintenance", "asset failure", "condition monitoring", "downtime"], "Failures must be anticipated before operational disruption."),
    _node("knowledge_mgmt", "Knowledge Management", ["knowledge management", "expert knowledge", "document retrieval", "institutional memory"], "Critical expertise must be captured and reused."),
    _node("compliance", "Regulatory Compliance", ["compliance", "auditability", "regulation", "governance", "policy enforcement"], "Systems must satisfy formal controls and audit expectations."),
    _node("sustainability", "Sustainability & ESG", ["sustainability", "esg", "carbon accounting", "emissions", "resource efficiency"], "Operations are constrained by emissions and ESG targets."),
    _node("interoperability", "System Interoperability", ["interoperability", "integration", "legacy systems", "data exchange"], "Platforms and datasets need to work across boundaries."),
    _node("explainability", "AI Explainability & Trust", ["explainability", "trust", "transparency", "model rationale", "responsible ai"], "AI outputs must be understandable and contestable."),
    _node("traceability", "Traceability & Provenance", ["traceability", "provenance", "lineage", "audit trail", "chain of custody"], "Stakeholders need to reconstruct what happened and why."),
    _node("forecasting", "Forecasting & Planning", ["forecasting", "demand planning", "load prediction", "capacity planning"], "Forward-looking estimates drive decisions and resource allocation."),
    _node("automation", "Workflow Automation", ["automation", "workflow orchestration", "decision automation", "autonomous operations"], "Manual work must be standardized or autonomously executed."),
    _node("risk_scoring", "Risk Scoring & Prioritization", ["risk scoring", "risk assessment", "triage", "underwriting", "prioritization"], "Cases and threats must be ranked under uncertainty."),
]

INNOVATION_PATTERNS: List[Node] = [
    _node("cross_domain", "Cross-Domain Transfer", ["cross domain", "adjacent market transfer", "analogy mining"], "Move a proven mechanism into a new domain."),
    _node("data_fusion", "Data Fusion", ["data fusion", "multisource intelligence", "heterogeneous data"], "Combine structured and unstructured signals."),
    _node("human_ai", "Human-AI Collaboration", ["human ai", "copilot", "decision support", "expert in the loop"], "Keep domain experts in the control loop."),
    _node("edge_hybrid", "Edge-Cloud Hybrid Processing", ["edge cloud", "hybrid inference", "local plus cloud"], "Split compute between local systems and centralized services."),
    _node("adaptive_system", "Adaptive / Self-Learning Systems", ["adaptive", "self learning", "online optimization", "feedback loop"], "Use feedback to tune the system over time."),
    _node("federated_priv", "Privacy-Preserving Analytics", ["privacy preserving", "secure collaboration", "confidential analytics"], "Generate shared insight without exposing raw data."),
    _node("explainable", "Explainable AI Outputs", ["explainable ai", "interpretable output", "transparent reasoning"], "Attach rationale, provenance, or confidence to outputs."),
    _node("multimodal", "Multimodal Integration", ["multimodal", "cross modal", "text image sensor fusion"], "Fuse text, image, video, audio, telemetry, or graph signals."),
    _node("retrieval_grounded", "Retrieval-Grounded Reasoning", ["retrieval grounded", "rag", "grounded generation", "evidence-backed output"], "Bind outputs to retrieved evidence or structured knowledge."),
    _node("digital_twin_loop", "Digital-Twin Control Loop", ["digital twin loop", "simulation in the loop", "virtual commissioning"], "Evaluate options in a live system model before acting."),
    _node("closed_loop_auto", "Closed-Loop Automation", ["closed loop", "sense decide act", "autonomous control"], "Connect sensing, reasoning, and execution in one cycle."),
]

TECH_DOMAIN_EDGES: List[Edge] = [
    _edge("ai_ml", "healthcare", "applied_in", "high"),
    _edge("nlp", "healthcare", "applied_in", "high"),
    _edge("computer_vision", "healthcare", "applied_in", "high"),
    _edge("federated_learn", "healthcare", "applied_in", "high"),
    _edge("knowledge_graph", "healthcare", "applied_in", "high"),
    _edge("time_series", "healthcare", "applied_in", "medium"),
    _edge("generative_ai", "healthcare", "applied_in", "medium"),
    _edge("ai_ml", "clean_energy", "applied_in", "high"),
    _edge("iot", "clean_energy", "applied_in", "high"),
    _edge("edge_compute", "clean_energy", "applied_in", "medium"),
    _edge("digital_twin", "clean_energy", "applied_in", "high"),
    _edge("time_series", "clean_energy", "applied_in", "high"),
    _edge("optimization", "clean_energy", "applied_in", "high"),
    _edge("ai_ml", "fintech", "applied_in", "high"),
    _edge("blockchain", "fintech", "applied_in", "high"),
    _edge("nlp", "fintech", "applied_in", "high"),
    _edge("knowledge_graph", "fintech", "applied_in", "medium"),
    _edge("generative_ai", "fintech", "applied_in", "medium"),
    _edge("ai_ml", "manufacturing", "applied_in", "high"),
    _edge("iot", "manufacturing", "applied_in", "high"),
    _edge("robotics", "manufacturing", "applied_in", "high"),
    _edge("computer_vision", "manufacturing", "applied_in", "high"),
    _edge("edge_compute", "manufacturing", "applied_in", "high"),
    _edge("digital_twin", "manufacturing", "applied_in", "high"),
    _edge("optimization", "manufacturing", "applied_in", "high"),
    _edge("time_series", "manufacturing", "applied_in", "high"),
    _edge("ai_ml", "agritech", "applied_in", "medium"),
    _edge("iot", "agritech", "applied_in", "high"),
    _edge("computer_vision", "agritech", "applied_in", "medium"),
    _edge("edge_compute", "agritech", "applied_in", "medium"),
    _edge("time_series", "agritech", "applied_in", "medium"),
    _edge("nlp", "edtech", "applied_in", "high"),
    _edge("reinforcement_rl", "edtech", "applied_in", "medium"),
    _edge("generative_ai", "edtech", "applied_in", "high"),
    _edge("knowledge_graph", "edtech", "applied_in", "medium"),
    _edge("ai_ml", "cybersecurity", "applied_in", "high"),
    _edge("nlp", "cybersecurity", "applied_in", "medium"),
    _edge("knowledge_graph", "cybersecurity", "applied_in", "medium"),
    _edge("ai_ml", "logistics", "applied_in", "high"),
    _edge("iot", "logistics", "applied_in", "high"),
    _edge("optimization", "logistics", "applied_in", "high"),
    _edge("digital_twin", "logistics", "applied_in", "medium"),
    _edge("time_series", "logistics", "applied_in", "medium"),
    _edge("computer_vision", "logistics", "applied_in", "medium"),
    _edge("iot", "smart_cities", "applied_in", "high"),
    _edge("edge_compute", "smart_cities", "applied_in", "high"),
    _edge("ai_ml", "smart_cities", "applied_in", "high"),
    _edge("digital_twin", "smart_cities", "applied_in", "high"),
    _edge("optimization", "smart_cities", "applied_in", "medium"),
    _edge("ai_ml", "retail", "applied_in", "high"),
    _edge("generative_ai", "retail", "applied_in", "high"),
    _edge("nlp", "retail", "applied_in", "high"),
    _edge("computer_vision", "retail", "applied_in", "medium"),
    _edge("knowledge_graph", "retail", "applied_in", "medium"),
    _edge("optimization", "retail", "applied_in", "medium"),
    _edge("nlp", "legaltech", "applied_in", "high"),
    _edge("generative_ai", "legaltech", "applied_in", "high"),
    _edge("knowledge_graph", "legaltech", "applied_in", "high"),
    _edge("ai_ml", "legaltech", "applied_in", "medium"),
    _edge("knowledge_graph", "public_sector", "applied_in", "high"),
    _edge("ai_ml", "public_sector", "applied_in", "medium"),
    _edge("nlp", "public_sector", "applied_in", "medium"),
    _edge("ai_ml", "telecom", "applied_in", "high"),
    _edge("edge_compute", "telecom", "applied_in", "high"),
    _edge("time_series", "telecom", "applied_in", "high"),
    _edge("optimization", "telecom", "applied_in", "medium"),
    _edge("iot", "telecom", "applied_in", "medium"),
]

PROBLEM_DOMAIN_EDGES: List[Edge] = [
    _edge("data_silos", "healthcare", "challenges", "high"),
    _edge("data_silos", "public_sector", "challenges", "high"),
    _edge("data_silos", "manufacturing", "challenges", "medium"),
    _edge("real_time", "manufacturing", "challenges", "high"),
    _edge("real_time", "logistics", "challenges", "high"),
    _edge("real_time", "smart_cities", "challenges", "high"),
    _edge("real_time", "telecom", "challenges", "high"),
    _edge("personalization", "retail", "challenges", "high"),
    _edge("personalization", "edtech", "challenges", "high"),
    _edge("personalization", "healthcare", "challenges", "medium"),
    _edge("personalization", "fintech", "challenges", "medium"),
    _edge("anomaly_detect", "cybersecurity", "challenges", "high"),
    _edge("anomaly_detect", "manufacturing", "challenges", "high"),
    _edge("anomaly_detect", "fintech", "challenges", "high"),
    _edge("anomaly_detect", "telecom", "challenges", "high"),
    _edge("pred_maintenance", "manufacturing", "challenges", "high"),
    _edge("pred_maintenance", "clean_energy", "challenges", "high"),
    _edge("pred_maintenance", "logistics", "challenges", "medium"),
    _edge("knowledge_mgmt", "legaltech", "challenges", "high"),
    _edge("knowledge_mgmt", "healthcare", "challenges", "medium"),
    _edge("knowledge_mgmt", "public_sector", "challenges", "medium"),
    _edge("knowledge_mgmt", "edtech", "challenges", "medium"),
    _edge("compliance", "fintech", "challenges", "high"),
    _edge("compliance", "healthcare", "challenges", "high"),
    _edge("compliance", "legaltech", "challenges", "high"),
    _edge("compliance", "public_sector", "challenges", "medium"),
    _edge("sustainability", "clean_energy", "challenges", "high"),
    _edge("sustainability", "manufacturing", "challenges", "medium"),
    _edge("sustainability", "agritech", "challenges", "medium"),
    _edge("sustainability", "logistics", "challenges", "medium"),
    _edge("interoperability", "healthcare", "challenges", "high"),
    _edge("interoperability", "smart_cities", "challenges", "high"),
    _edge("interoperability", "public_sector", "challenges", "high"),
    _edge("interoperability", "telecom", "challenges", "medium"),
    _edge("explainability", "healthcare", "challenges", "high"),
    _edge("explainability", "fintech", "challenges", "high"),
    _edge("explainability", "public_sector", "challenges", "medium"),
    _edge("traceability", "logistics", "challenges", "high"),
    _edge("traceability", "agritech", "challenges", "medium"),
    _edge("traceability", "fintech", "challenges", "medium"),
    _edge("traceability", "public_sector", "challenges", "medium"),
    _edge("forecasting", "clean_energy", "challenges", "high"),
    _edge("forecasting", "logistics", "challenges", "high"),
    _edge("forecasting", "agritech", "challenges", "high"),
    _edge("forecasting", "retail", "challenges", "medium"),
    _edge("automation", "manufacturing", "challenges", "high"),
    _edge("automation", "logistics", "challenges", "medium"),
    _edge("automation", "legaltech", "challenges", "medium"),
    _edge("automation", "public_sector", "challenges", "low"),
    _edge("risk_scoring", "fintech", "challenges", "high"),
    _edge("risk_scoring", "cybersecurity", "challenges", "medium"),
    _edge("risk_scoring", "healthcare", "challenges", "medium"),
]

PATTERN_TECH_EDGES: List[Edge] = [
    _edge("cross_domain", "ai_ml", "leverages", "high"),
    _edge("cross_domain", "knowledge_graph", "leverages", "medium"),
    _edge("cross_domain", "generative_ai", "leverages", "medium"),
    _edge("data_fusion", "ai_ml", "leverages", "high"),
    _edge("data_fusion", "knowledge_graph", "leverages", "high"),
    _edge("data_fusion", "iot", "leverages", "medium"),
    _edge("human_ai", "nlp", "leverages", "medium"),
    _edge("human_ai", "generative_ai", "leverages", "high"),
    _edge("human_ai", "ar_vr", "leverages", "medium"),
    _edge("edge_hybrid", "edge_compute", "leverages", "high"),
    _edge("edge_hybrid", "iot", "leverages", "high"),
    _edge("edge_hybrid", "ai_ml", "leverages", "medium"),
    _edge("adaptive_system", "reinforcement_rl", "leverages", "high"),
    _edge("adaptive_system", "ai_ml", "leverages", "high"),
    _edge("adaptive_system", "time_series", "leverages", "medium"),
    _edge("federated_priv", "federated_learn", "leverages", "high"),
    _edge("federated_priv", "ai_ml", "leverages", "medium"),
    _edge("explainable", "ai_ml", "leverages", "high"),
    _edge("explainable", "knowledge_graph", "leverages", "medium"),
    _edge("multimodal", "generative_ai", "leverages", "high"),
    _edge("multimodal", "computer_vision", "leverages", "high"),
    _edge("multimodal", "nlp", "leverages", "high"),
    _edge("multimodal", "iot", "leverages", "medium"),
    _edge("retrieval_grounded", "knowledge_graph", "leverages", "high"),
    _edge("retrieval_grounded", "nlp", "leverages", "high"),
    _edge("retrieval_grounded", "generative_ai", "leverages", "high"),
    _edge("digital_twin_loop", "digital_twin", "leverages", "high"),
    _edge("digital_twin_loop", "iot", "leverages", "high"),
    _edge("digital_twin_loop", "optimization", "leverages", "medium"),
    _edge("digital_twin_loop", "time_series", "leverages", "medium"),
    _edge("closed_loop_auto", "robotics", "leverages", "high"),
    _edge("closed_loop_auto", "ai_ml", "leverages", "high"),
    _edge("closed_loop_auto", "edge_compute", "leverages", "medium"),
]


def _validate_nodes(node_groups: Dict[str, Sequence[Node]]) -> None:
    seen_ids: Dict[str, str] = {}
    for group_name, nodes in node_groups.items():
        for node in nodes:
            node_id = node["id"]
            if node_id in seen_ids:
                raise ValueError(
                    f"Duplicate node id '{node_id}' found in {group_name} and {seen_ids[node_id]}."
                )
            seen_ids[node_id] = group_name


def _validate_edges(edge_groups: Dict[str, Sequence[Edge]], valid_ids: Iterable[str]) -> None:
    valid_id_set = set(valid_ids)
    for group_name, edges in edge_groups.items():
        for edge in edges:
            if edge["from"] not in valid_id_set:
                raise ValueError(f"{group_name} references unknown source node '{edge['from']}'.")
            if edge["to"] not in valid_id_set:
                raise ValueError(f"{group_name} references unknown target node '{edge['to']}'.")
            if edge["strength"] not in _VALID_STRENGTHS:
                raise ValueError(f"{group_name} uses invalid strength '{edge['strength']}'.")


def _validate_seed_data() -> None:
    node_groups = {
        "TECHNOLOGY_NODES": TECHNOLOGY_NODES,
        "DOMAIN_NODES": DOMAIN_NODES,
        "PROBLEM_NODES": PROBLEM_NODES,
        "INNOVATION_PATTERNS": INNOVATION_PATTERNS,
    }
    _validate_nodes(node_groups)

    valid_ids = [node["id"] for nodes in node_groups.values() for node in nodes]
    _validate_edges(
        {
            "TECH_DOMAIN_EDGES": TECH_DOMAIN_EDGES,
            "PROBLEM_DOMAIN_EDGES": PROBLEM_DOMAIN_EDGES,
            "PATTERN_TECH_EDGES": PATTERN_TECH_EDGES,
        },
        valid_ids,
    )


_validate_seed_data()

__all__ = [
    "TECHNOLOGY_NODES",
    "DOMAIN_NODES",
    "PROBLEM_NODES",
    "INNOVATION_PATTERNS",
    "TECH_DOMAIN_EDGES",
    "PROBLEM_DOMAIN_EDGES",
    "PATTERN_TECH_EDGES",
]
