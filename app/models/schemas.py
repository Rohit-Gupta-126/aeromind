from pydantic import BaseModel, Field
from typing import List, Optional

class QuestionRequest(BaseModel):
    question: str = Field(..., description="The engineering question to ask", min_length=3)
    expert_mode: bool = Field(default=False, description="Enable expert mode for detailed technical responses")

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
    # USP Features
    processing_time_ms: Optional[float] = Field(None, description="Response generation time in milliseconds")
    suggested_followups: Optional[List[str]] = Field(default_factory=list, description="AI-suggested follow-up questions")
    complexity_score: Optional[str] = Field(None, description="Query complexity: SIMPLE, MODERATE, COMPLEX")
    model_used: Optional[str] = Field(None, description="The AI model used for this response")
