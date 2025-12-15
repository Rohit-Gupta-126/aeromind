from fastapi import APIRouter
from app.graph.workflow import run_workflow
from app.models.schemas import QuestionRequest, FinalResponse

router = APIRouter()

@router.post("/ask", response_model=FinalResponse)
def ask_question(payload: QuestionRequest):
    question = payload.question
    result = run_workflow(question)
    return result
