from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class InnovationRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    session_id: str = Field(..., min_length=1)
    domain: str = Field(..., description="Technology domain e.g. 'Healthcare AI'")
    problem_space: str = Field(..., description="Specific problem or opportunity area")
    user_intent: str = Field(..., description="What you want to achieve or explore")
    depth: Literal["quick", "standard", "deep"] = Field(
        default="standard",
        description="'quick' | 'standard' | 'deep'",
    )

    @field_validator("session_id", "domain", "problem_space", "user_intent")
    @classmethod
    def validate_not_empty(cls, value: str) -> str:
        if not value:
            raise ValueError("must not be empty")
        return value


class InnovationConcept(BaseModel):
    title: str
    description: str
    technical_approach: str
    use_cases: List[str]
    implementation_pathway: str
    strategic_positioning: str
    novelty_indicators: List[str]


class PriorArtItem(BaseModel):
    title: str
    authors: List[str]
    year: int
    source: str          # "arxiv" | "semantic_scholar"
    relevance_score: float
    summary: str
    url: Optional[str] = None
    key_differences: str


class PriorArtConceptResult(BaseModel):
    concept_index: int
    concept_title: str
    results: List[PriorArtItem]


class NoveltyAssessment(BaseModel):
    overall_score: float       # 0–100
    rating: str                # "High" | "Medium" | "Low"
    key_differentiators: List[str]
    risk_areas: List[str]
    recommendation: str


class FinalOutput(BaseModel):
    session_id: str
    domain: str
    problem_space: str
    innovation_concepts: List[InnovationConcept]
    prior_art_results: List[PriorArtConceptResult]
    novelty_assessment: NoveltyAssessment
    executive_summary: str
    ip_readiness_score: float   # 0–100
    next_steps: List[str]
    processing_time: float
    demo_mode: bool = False


class AgentEvent(BaseModel):
    type: str          # "agent_start" | "agent_progress" | "agent_complete" | "pipeline_complete" | "error"
    agent: str         # "supervisor" | "ideation" | "prior_art" | "synthesis"
    message: str
    data: Optional[Dict[str, Any]] = None
    timestamp: float = 0.0
