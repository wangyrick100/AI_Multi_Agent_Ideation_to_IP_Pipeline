"""
Pre-loaded domain knowledge used to seed the knowledge graph.
Covers common technology domains, problems, and innovation patterns.
"""
from typing import List, Dict, Any

TECHNOLOGY_NODES: List[Dict[str, Any]] = [
    {"id": "ai_ml",            "label": "AI / Machine Learning",          "tags": ["ml", "ai", "neural", "deep learning"]},
    {"id": "nlp",              "label": "Natural Language Processing",     "tags": ["nlp", "text", "language", "llm", "transformer"]},
    {"id": "computer_vision",  "label": "Computer Vision",                 "tags": ["image", "vision", "detection", "segmentation"]},
    {"id": "federated_learn",  "label": "Federated Learning",              "tags": ["federated", "privacy", "distributed training"]},
    {"id": "knowledge_graph",  "label": "Knowledge Graphs",                "tags": ["graph", "ontology", "relationship", "reasoning"]},
    {"id": "iot",              "label": "Internet of Things",              "tags": ["iot", "sensor", "edge", "device"]},
    {"id": "blockchain",       "label": "Blockchain / DLT",               "tags": ["blockchain", "decentralized", "ledger", "smart contract"]},
    {"id": "robotics",         "label": "Robotics & Automation",           "tags": ["robot", "automation", "actuator", "motion"]},
    {"id": "quantum",          "label": "Quantum Computing",               "tags": ["quantum", "qubit", "superposition", "entanglement"]},
    {"id": "ar_vr",            "label": "AR / VR / Mixed Reality",         "tags": ["ar", "vr", "xr", "immersive", "spatial"]},
    {"id": "edge_compute",     "label": "Edge Computing",                  "tags": ["edge", "on-device", "low latency", "fog computing"]},
    {"id": "reinforcement_rl", "label": "Reinforcement Learning",          "tags": ["rl", "reward", "policy", "agent", "environment"]},
    {"id": "generative_ai",    "label": "Generative AI",                   "tags": ["generative", "diffusion", "gan", "llm", "synthesis"]},
]

DOMAIN_NODES: List[Dict[str, Any]] = [
    {"id": "healthcare",     "label": "Healthcare & Life Sciences",     "tags": ["health", "medical", "clinical", "patient", "drug"]},
    {"id": "clean_energy",   "label": "Clean Energy & Climate Tech",    "tags": ["energy", "solar", "wind", "carbon", "climate", "battery"]},
    {"id": "fintech",        "label": "FinTech & Financial Services",   "tags": ["finance", "banking", "payments", "credit", "insurance"]},
    {"id": "manufacturing",  "label": "Smart Manufacturing / Industry 4.0", "tags": ["manufacturing", "factory", "supply chain", "quality", "predictive maintenance"]},
    {"id": "agritech",       "label": "AgriTech & Food Systems",        "tags": ["agriculture", "crop", "food", "farm", "soil"]},
    {"id": "edtech",         "label": "EdTech & Learning",              "tags": ["education", "learning", "training", "skill", "curriculum"]},
    {"id": "cybersecurity",  "label": "Cybersecurity",                  "tags": ["security", "threat", "intrusion", "vulnerability", "authentication"]},
    {"id": "logistics",      "label": "Logistics & Supply Chain",       "tags": ["logistics", "shipping", "warehouse", "route", "inventory"]},
    {"id": "smart_cities",   "label": "Smart Cities & Urban Tech",      "tags": ["city", "urban", "traffic", "infrastructure", "mobility"]},
    {"id": "retail",         "label": "Retail & E-commerce",            "tags": ["retail", "ecommerce", "recommendation", "inventory", "customer"]},
]

PROBLEM_NODES: List[Dict[str, Any]] = [
    {"id": "data_silos",       "label": "Data Silos & Fragmentation"},
    {"id": "real_time",        "label": "Real-time Decision Making"},
    {"id": "personalization",  "label": "Personalization at Scale"},
    {"id": "anomaly_detect",   "label": "Anomaly Detection"},
    {"id": "pred_maintenance", "label": "Predictive Maintenance"},
    {"id": "knowledge_mgmt",   "label": "Knowledge Management"},
    {"id": "compliance",       "label": "Regulatory Compliance"},
    {"id": "sustainability",   "label": "Sustainability & ESG"},
    {"id": "interoperability", "label": "System Interoperability"},
    {"id": "explainability",   "label": "AI Explainability & Trust"},
]

INNOVATION_PATTERNS: List[Dict[str, Any]] = [
    {"id": "cross_domain",    "label": "Cross-Domain Transfer",        "description": "Apply techniques from one domain to solve problems in another"},
    {"id": "data_fusion",     "label": "Data Fusion",                  "description": "Combine heterogeneous data sources for richer insights"},
    {"id": "human_ai",        "label": "Human-AI Collaboration",       "description": "Augment human decision-making with AI assistance"},
    {"id": "edge_hybrid",     "label": "Edge-Cloud Hybrid Processing", "description": "Split processing between edge devices and cloud"},
    {"id": "adaptive_system", "label": "Adaptive / Self-learning Systems", "description": "Systems that improve through use"},
    {"id": "federated_priv",  "label": "Privacy-Preserving Analytics","description": "Gain insights without exposing raw data"},
    {"id": "explainable",     "label": "Explainable AI Outputs",       "description": "Make AI decisions interpretable to users"},
    {"id": "multimodal",      "label": "Multimodal Integration",       "description": "Combine text, image, sensor, and other modalities"},
]

# Edges: which technologies commonly apply to which domains
TECH_DOMAIN_EDGES: List[Dict[str, str]] = [
    {"from": "ai_ml",           "to": "healthcare",    "relation": "applied_in",   "strength": "high"},
    {"from": "nlp",             "to": "healthcare",    "relation": "applied_in",   "strength": "high"},
    {"from": "computer_vision", "to": "healthcare",    "relation": "applied_in",   "strength": "high"},
    {"from": "federated_learn", "to": "healthcare",    "relation": "applied_in",   "strength": "high"},
    {"from": "iot",             "to": "healthcare",    "relation": "applied_in",   "strength": "medium"},
    {"from": "ai_ml",           "to": "clean_energy",  "relation": "applied_in",   "strength": "high"},
    {"from": "iot",             "to": "clean_energy",  "relation": "applied_in",   "strength": "high"},
    {"from": "edge_compute",    "to": "clean_energy",  "relation": "applied_in",   "strength": "medium"},
    {"from": "ai_ml",           "to": "fintech",       "relation": "applied_in",   "strength": "high"},
    {"from": "blockchain",      "to": "fintech",       "relation": "applied_in",   "strength": "high"},
    {"from": "nlp",             "to": "fintech",       "relation": "applied_in",   "strength": "high"},
    {"from": "ai_ml",           "to": "manufacturing", "relation": "applied_in",   "strength": "high"},
    {"from": "iot",             "to": "manufacturing", "relation": "applied_in",   "strength": "high"},
    {"from": "robotics",        "to": "manufacturing", "relation": "applied_in",   "strength": "high"},
    {"from": "computer_vision", "to": "manufacturing", "relation": "applied_in",   "strength": "high"},
    {"from": "ai_ml",           "to": "agritech",      "relation": "applied_in",   "strength": "medium"},
    {"from": "iot",             "to": "agritech",      "relation": "applied_in",   "strength": "high"},
    {"from": "computer_vision", "to": "agritech",      "relation": "applied_in",   "strength": "medium"},
    {"from": "nlp",             "to": "edtech",        "relation": "applied_in",   "strength": "high"},
    {"from": "reinforcement_rl","to": "edtech",        "relation": "applied_in",   "strength": "medium"},
    {"from": "ai_ml",           "to": "cybersecurity", "relation": "applied_in",   "strength": "high"},
    {"from": "ai_ml",           "to": "logistics",     "relation": "applied_in",   "strength": "high"},
    {"from": "iot",             "to": "logistics",     "relation": "applied_in",   "strength": "high"},
    {"from": "generative_ai",   "to": "retail",        "relation": "applied_in",   "strength": "high"},
    {"from": "nlp",             "to": "retail",        "relation": "applied_in",   "strength": "high"},
]
