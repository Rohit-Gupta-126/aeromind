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
