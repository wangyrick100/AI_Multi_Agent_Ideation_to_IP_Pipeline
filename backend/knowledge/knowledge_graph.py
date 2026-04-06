"""
NetworkX-based knowledge graph for domain-technology-problem reasoning.
Used by the Ideation Agent to discover non-obvious connections.
"""
from __future__ import annotations
import re

import networkx as nx
from typing import Any, Dict, List

from knowledge.domain_data import (
    DOMAIN_NODES,
    INNOVATION_PATTERNS,
    PATTERN_TECH_EDGES,
    PROBLEM_DOMAIN_EDGES,
    PROBLEM_NODES,
    TECH_DOMAIN_EDGES,
    TECHNOLOGY_NODES,
)

_STRENGTH_SCORE = {"low": 1, "medium": 2, "high": 3}


class InnovationKnowledgeGraph:
    """Directed property graph of technologies, domains, problems, and patterns."""

    def __init__(self) -> None:
        self.G: nx.DiGraph = nx.DiGraph()
        self._build()

    def _build(self) -> None:
        # Add nodes with type and tag attributes.
        for node in TECHNOLOGY_NODES:
            self.G.add_node(node["id"], kind="technology", **node)
        for node in DOMAIN_NODES:
            self.G.add_node(node["id"], kind="domain", **node)
        for node in PROBLEM_NODES:
            self.G.add_node(node["id"], kind="problem", **node)
        for node in INNOVATION_PATTERNS:
            self.G.add_node(node["id"], kind="pattern", **node)

        # Typed edges are defined in domain_data so the graph topology stays
        # inspectable and easy to evolve without editing this class.
        for edge in TECH_DOMAIN_EDGES:
            self.G.add_edge(edge["from"], edge["to"], relation=edge["relation"], strength=edge["strength"])
        for edge in PROBLEM_DOMAIN_EDGES:
            self.G.add_edge(edge["from"], edge["to"], relation=edge["relation"], strength=edge["strength"])
        for edge in PATTERN_TECH_EDGES:
            self.G.add_edge(edge["from"], edge["to"], relation=edge["relation"], strength=edge["strength"])

    # ------------------------------------------------------------------
    # Query helpers
    # ------------------------------------------------------------------

    def _normalize_keywords(self, keywords: List[str]) -> List[str]:
        normalized: List[str] = []
        for keyword in keywords:
            cleaned = re.sub(r"[^a-z0-9\+\-/ ]+", " ", str(keyword).lower()).strip()
            if cleaned and cleaned not in normalized:
                normalized.append(cleaned)
        return normalized

    def _matches_keywords(self, data: Dict[str, Any], keywords: List[str]) -> bool:
        normalized = self._normalize_keywords(keywords)
        if not normalized:
            return False

        label = data.get("label", "").lower()
        tags = [str(tag).lower() for tag in data.get("tags", [])]
        description = data.get("description", "").lower()

        for keyword in normalized:
            if keyword in label or keyword in description:
                return True
            if any(keyword in tag for tag in tags):
                return True
        return False

    def _matched_node_ids(self, kind: str, keywords: List[str]) -> List[str]:
        return [
            node_id
            for node_id, data in self.G.nodes(data=True)
            if data.get("kind") == kind and self._matches_keywords(data, keywords)
        ]

    def _candidate_domain_ids(self, keywords: List[str]) -> List[str]:
        direct_domain_ids = set(self._matched_node_ids("domain", keywords))
        if direct_domain_ids:
            return sorted(direct_domain_ids)

        domain_ids = set()
        for problem_id in self._matched_node_ids("problem", keywords):
            for domain_id in self.G.successors(problem_id):
                if self.G.nodes[domain_id].get("kind") == "domain":
                    domain_ids.add(domain_id)
        return sorted(domain_ids)

    def get_relevant_problems(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """Return problem nodes directly matched by the supplied keywords."""
        problems = [self.G.nodes[node_id] for node_id in self._matched_node_ids("problem", keywords)]
        return sorted(problems, key=lambda item: item["label"])

    def get_relevant_technologies(self, domain_keywords: List[str]) -> List[Dict[str, Any]]:
        """Return technologies relevant to direct or inferred domain matches."""
        technologies: Dict[str, Dict[str, Any]] = {}
        for domain_id in self._candidate_domain_ids(domain_keywords):
            domain_label = self.G.nodes[domain_id]["label"]
            for tech_id in self.G.predecessors(domain_id):
                tech_data = self.G.nodes[tech_id]
                if tech_data.get("kind") != "technology":
                    continue

                edge_data = self.G.edges[tech_id, domain_id]
                strength = edge_data.get("strength", "low")
                existing = technologies.get(tech_id)
                if existing is None:
                    technologies[tech_id] = {
                        **tech_data,
                        "strength": strength,
                        "matched_domains": [domain_label],
                    }
                    continue

                if domain_label not in existing["matched_domains"]:
                    existing["matched_domains"].append(domain_label)
                if _STRENGTH_SCORE[strength] > _STRENGTH_SCORE[existing["strength"]]:
                    existing["strength"] = strength

        return sorted(
            technologies.values(),
            key=lambda item: (-_STRENGTH_SCORE[item["strength"]], item["label"]),
        )

    def get_relevant_patterns(self, tech_ids: List[str]) -> List[Dict[str, Any]]:
        """Return innovation patterns that leverage the given technologies."""
        patterns: Dict[str, Dict[str, Any]] = {}
        for tech_id in tech_ids:
            for pattern_id in self.G.predecessors(tech_id):
                pattern_data = self.G.nodes[pattern_id]
                if pattern_data.get("kind") != "pattern":
                    continue

                edge_data = self.G.edges[pattern_id, tech_id]
                strength = edge_data.get("strength", "low")
                existing = patterns.get(pattern_id)
                if existing is None:
                    patterns[pattern_id] = {
                        **pattern_data,
                        "strength": strength,
                        "hit_count": 1,
                    }
                    continue

                existing["hit_count"] += 1
                if _STRENGTH_SCORE[strength] > _STRENGTH_SCORE[existing["strength"]]:
                    existing["strength"] = strength

        return sorted(
            patterns.values(),
            key=lambda item: (-item["hit_count"], -_STRENGTH_SCORE[item["strength"]], item["label"]),
        )

    def get_related_domains(self, domain_keywords: List[str]) -> List[str]:
        """Return related domains matched directly or inferred from matched problems."""
        return [self.G.nodes[node_id]["label"] for node_id in self._candidate_domain_ids(domain_keywords)]

    def build_context_summary(self, domain_keywords: List[str]) -> str:
        """Return a human-readable paragraph summarizing relevant graph context."""
        problems = self.get_relevant_problems(domain_keywords)
        techs = self.get_relevant_technologies(domain_keywords)
        patterns = self.get_relevant_patterns([tech["id"] for tech in techs])
        domains = self.get_related_domains(domain_keywords)

        summary_parts: List[str] = []
        if domains:
            summary_parts.append(f"Related domains: {', '.join(domains[:4])}.")
        if problems:
            summary_parts.append(
                f"Problem signals: {', '.join(problem['label'] for problem in problems[:4])}."
            )
        if techs:
            summary_parts.append(
                f"Applicable technologies: {', '.join(tech['label'] for tech in techs[:6])}."
            )
        if patterns:
            summary_parts.append(
                f"Promising innovation patterns: {', '.join(pattern['label'] for pattern in patterns[:4])}."
            )

        return " ".join(summary_parts) or (
            "No specific domain or problem context found; applying general innovation reasoning."
        )


# Module-level singleton
_kg: InnovationKnowledgeGraph | None = None


def get_knowledge_graph() -> InnovationKnowledgeGraph:
    global _kg
    if _kg is None:
        _kg = InnovationKnowledgeGraph()
    return _kg
