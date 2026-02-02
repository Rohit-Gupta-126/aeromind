from typing import TypedDict, List, Optional

class WorkflowState(TypedDict):
    question: str
    route: Optional[str]
    answer: Optional[str]
    confidence: Optional[str]
    sources: List[str]
    context: Optional[str]
    verification_status: Optional[str]
    verification_notes: Optional[str]
    # USP Features
    processing_time_ms: Optional[float]
    suggested_followups: Optional[List[str]]
    complexity_score: Optional[str]
    expert_mode: Optional[bool]
    model_used: Optional[str]
