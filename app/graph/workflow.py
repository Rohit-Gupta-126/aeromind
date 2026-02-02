from app.agents.router import route_query
from app.agents.verifier import verifier_agent
from app.models.state import WorkflowState
from app.services.formatter import format_response
from app.core.llm import generate_response, PRIMARY_MODEL
import time
import logging

logger = logging.getLogger(__name__)


def generate_followup_suggestions(question: str, answer: str, route: str) -> list:
    """
    Generate intelligent follow-up questions based on the query and response.
    This is a USP feature that helps users explore topics deeper.
    """
    prompt = f"""Based on this aerospace engineering conversation, suggest 3 brief follow-up questions.

Original Question: {question}
Topic Category: {route}
Answer Summary: {answer[:500] if answer else "No answer"}

Return ONLY a JSON array with 3 short follow-up questions. Example:
["What are the temperature limits?", "How does this affect fuel efficiency?", "Are there alternative materials?"]
"""
    try:
        response = generate_response(prompt, json_mode=True)
        import json
        suggestions = json.loads(response)
        return suggestions[:3] if isinstance(suggestions, list) else []
    except Exception as e:
        logger.warning(f"Failed to generate follow-up suggestions: {e}")
        return []


def assess_complexity(question: str) -> str:
    """
    Assess the complexity of the query for user transparency.
    """
    word_count = len(question.split())
    technical_keywords = ['thermal', 'aerodynamic', 'propulsion', 'structural', 'fatigue', 
                         'composite', 'turbine', 'combustion', 'avionics', 'hydraulic',
                         'supersonic', 'subsonic', 'reynolds', 'mach', 'thrust']
    
    technical_count = sum(1 for word in question.lower().split() if word in technical_keywords)
    
    if word_count > 30 or technical_count >= 3:
        return "COMPLEX"
    elif word_count > 15 or technical_count >= 1:
        return "MODERATE"
    return "SIMPLE"


def run_workflow(question: str, expert_mode: bool = False) -> dict:
    """
    Orchestrates the multi-agent workflow for processing a user query.
    
    Steps:
    1. Initialize workflow state.
    2. Route the query to the appropriate agent (Engineering, Safety, etc.).
    3. Execute the selected agent to generate an answer.
    4. Run the Verifier Agent to check for hallucinations (if applicable).
    5. Generate intelligent follow-up suggestions.
    6. Format the final response for the API.
    """
    start_time = time.time()
    
    state: WorkflowState = {
        "question": question,
        "route": None,
        "answer": None,
        "confidence": "LOW",
        "sources": [],
        "context": None,
        "verification_status": None,
        "verification_notes": None,
        "processing_time_ms": None,
        "suggested_followups": [],
        "complexity_score": assess_complexity(question),
        "expert_mode": expert_mode,
        "model_used": PRIMARY_MODEL
    }

    state = route_query(state)
    
    # Run verifier if we have an answer and it's an engineering or safety query
    if state["route"] in ["engineering", "safety"] and state["answer"]:
        state = verifier_agent(state)
        
        # Adjust confidence based on verification
        if state["verification_status"] == "PASS":
            state["confidence"] = "HIGH (verified)"
        elif state["verification_status"] == "PARTIAL":
            state["confidence"] = "MEDIUM (partial verification)"
        elif state["verification_status"] == "FAIL":
            state["confidence"] = "LOW (verification failed)"
    
    # Generate follow-up suggestions (USP Feature)
    if state["route"] in ["engineering", "safety"] and state["answer"]:
        state["suggested_followups"] = generate_followup_suggestions(
            question, state["answer"], state["route"]
        )
    
    # Calculate processing time
    processing_time_ms = (time.time() - start_time) * 1000

    return {
        "question": state["question"],
        "route_selected": state["route"] or "unknown",
        "answer": format_response(state["answer"]) if state["answer"] else "No answer generated.",
        "confidence": state["confidence"] or "LOW",
        "sources": state.get("sources", []),
        "verification_status": state.get("verification_status"),
        "verification_notes": state.get("verification_notes"),
        # USP Features
        "processing_time_ms": round(processing_time_ms, 2),
        "suggested_followups": state.get("suggested_followups", []),
        "complexity_score": state.get("complexity_score"),
        "model_used": state.get("model_used")
    }
