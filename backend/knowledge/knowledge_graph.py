"""
NetworkX-based knowledge graph for domain-technology-problem reasoning.
Used by the Ideation Agent to discover non-obvious connections.
"""
from __future__ import annotations
import networkx as nx
from typing import List, Dict, Any, Tuple

from knowledge.domain_data import (
    TECHNOLOGY_NODES,
    DOMAIN_NODES,
    PROBLEM_NODES,
    INNOVATION_PATTERNS,
    TECH_DOMAIN_EDGES,
)


class InnovationKnowledgeGraph:
    """Directed property graph of technologies, domains, problems, and patterns."""

    def __init__(self) -> None:
        self.G: nx.DiGraph = nx.DiGraph()
        self._build()

    def _build(self) -> None:
        # Add nodes with type and tag attributes
        for node in TECHNOLOGY_NODES:
            self.G.add_node(node["id"], kind="technology", **node)
        for node in DOMAIN_NODES:
            self.G.add_node(node["id"], kind="domain", **node)
        for node in PROBLEM_NODES:
            self.G.add_node(node["id"], kind="problem", **node)
        for node in INNOVATION_PATTERNS:
            self.G.add_node(node["id"], kind="pattern", **node)

        # Technology → Domain edges
        for edge in TECH_DOMAIN_EDGES:
            self.G.add_edge(edge["from"], edge["to"], relation=edge["relation"], strength=edge["strength"])

        # Problem → Domain edges (problems appear across domains)
        self.G.add_edge("data_silos",       "healthcare",    relation="challenges",  strength="high")
        self.G.add_edge("real_time",        "manufacturing", relation="challenges",  strength="high")
        self.G.add_edge("personalization",  "retail",        relation="challenges",  strength="high")
        self.G.add_edge("anomaly_detect",   "cybersecurity", relation="challenges",  strength="high")
        self.G.add_edge("pred_maintenance", "manufacturing", relation="challenges",  strength="high")
        self.G.add_edge("explainability",   "healthcare",    relation="challenges",  strength="high")
        self.G.add_edge("compliance",       "fintech",       relation="challenges",  strength="high")
        self.G.add_edge("sustainability",   "clean_energy",  relation="challenges",  strength="high")

        # Innovation pattern → Technology edges
        self.G.add_edge("cross_domain",    "ai_ml",          relation="leverages",   strength="high")
        self.G.add_edge("data_fusion",     "ai_ml",          relation="leverages",   strength="high")
        self.G.add_edge("federated_priv",  "federated_learn",relation="leverages",   strength="high")
        self.G.add_edge("edge_hybrid",     "edge_compute",   relation="leverages",   strength="high")
        self.G.add_edge("explainable",     "ai_ml",          relation="leverages",   strength="high")
        self.G.add_edge("multimodal",      "generative_ai",  relation="leverages",   strength="high")
        self.G.add_edge("human_ai",        "nlp",            relation="leverages",   strength="medium")

    # ------------------------------------------------------------------
    # Query helpers
    # ------------------------------------------------------------------

    def get_relevant_technologies(self, domain_keywords: List[str]) -> List[Dict[str, Any]]:
        """Return technologies relevant to the given domain keywords."""
        domain_matches: List[str] = []
        for nid, data in self.G.nodes(data=True):
            if data.get("kind") == "domain":
                label = data.get("label", "").lower()
                tags  = data.get("tags", [])
                if any(kw.lower() in label or any(kw.lower() in t for t in tags)
                       for kw in domain_keywords):
                    domain_matches.append(nid)

        techs: List[Dict[str, Any]] = []
        for domain_id in domain_matches:
            for pred_id in self.G.predecessors(domain_id):
                pred_data = self.G.nodes[pred_id]
                if pred_data.get("kind") == "technology":
                    edge_data = self.G.edges[pred_id, domain_id]
                    techs.append({**pred_data, "strength": edge_data.get("strength", "low")})

        # Deduplicate by id
        seen: set = set()
        unique: List[Dict] = []
        for t in techs:
            if t["id"] not in seen:
                seen.add(t["id"])
                unique.append(t)
        return unique

    def get_relevant_patterns(self, tech_ids: List[str]) -> List[Dict[str, Any]]:
        """Return innovation patterns that leverage the given technologies."""
        patterns: List[Dict[str, Any]] = []
        for nid, data in self.G.nodes(data=True):
            if data.get("kind") == "pattern":
                for tech_id in tech_ids:
                    if self.G.has_edge(nid, tech_id):
                        patterns.append(data)
                        break
        return patterns

    def get_related_domains(self, domain_keywords: List[str]) -> List[str]:
        """Return labels of all domain nodes that match keywords."""
        results: List[str] = []
        for nid, data in self.G.nodes(data=True):
            if data.get("kind") == "domain":
                label = data.get("label", "").lower()
                tags  = data.get("tags", [])
                if any(kw.lower() in label or any(kw.lower() in t for t in tags)
                       for kw in domain_keywords):
                    results.append(data["label"])
        return results

    def build_context_summary(self, domain_keywords: List[str]) -> str:
        """Return a human-readable paragraph summarising relevant knowledge."""
        techs    = self.get_relevant_technologies(domain_keywords)
        tech_ids = [t["id"] for t in techs]
        patterns = self.get_relevant_patterns(tech_ids)
        domains  = self.get_related_domains(domain_keywords)

        tech_labels    = [t["label"] for t in techs[:6]]
        pattern_labels = [p["label"] for p in patterns[:4]]

        summary_parts = []
        if domains:
            summary_parts.append(f"Related domains: {', '.join(domains[:4])}.")
        if tech_labels:
            summary_parts.append(f"Applicable technologies: {', '.join(tech_labels)}.")
        if pattern_labels:
            summary_parts.append(f"Promising innovation patterns: {', '.join(pattern_labels)}.")

        return " ".join(summary_parts) or "No specific domain context found; applying general innovation reasoning."


# Module-level singleton
_kg: InnovationKnowledgeGraph | None = None


def get_knowledge_graph() -> InnovationKnowledgeGraph:
    global _kg
    if _kg is None:
        _kg = InnovationKnowledgeGraph()
    return _kg
