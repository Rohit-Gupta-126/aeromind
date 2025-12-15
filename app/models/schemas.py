from pydantic import BaseModel, Field
from typing import List, Optional

class QuestionRequest(BaseModel):
    question: str = Field(..., description="The engineering question to ask", min_length=3)

class AgentResponse(BaseModel):
    answer: str
    confidence: str
    sources: List[str]

class FinalResponse(BaseModel):
    question: str
    route_selected: str
    answer: str
    confidence: str
    sources: List[str] = Field(default_factory=list)
    verification_status: Optional[str] = None
    verification_notes: Optional[str] = None
