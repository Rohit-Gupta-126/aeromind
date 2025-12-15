from app.agents.engineering import engineering_agent
from app.models.state import WorkflowState
from app.core.llm import generate_response
import logging

logger = logging.getLogger(__name__)

def route_query(state: WorkflowState) -> WorkflowState:
    """
    Determines the appropriate domain agent for the user's query.
    
    Uses an LLM to classify the query into 'engineering', 'safety', or 'unsupported'.
    Routes the workflow to the selected agent or handles unsupported queries directly.
    """
    question = state["question"]
    
    prompt = f"""
You are a query router for an aerospace engineering system.
Classify the following question into one of these categories:
- engineering: Technical questions about engines, design, physics, or mechanics.
- safety: Questions about safety protocols, regulations, or risk assessment.
- unsupported: General knowledge, coding, or non-aerospace questions.

Question: {question}

Output ONLY the category name.
"""
    try:
        route = generate_response(prompt).strip().lower()
    except Exception as e:
        logger.error(f"Router LLM failed: {e}")
        route = "unsupported"
    
    # Fallback if LLM returns something unexpected
    valid_routes = ["engineering", "safety", "unsupported"]
    if route not in valid_routes:
        logger.warning(f"Invalid route '{route}' returned by LLM. Defaulting to 'unsupported'.")
        route = "unsupported"

    logger.info(f"Routing query '{question}' to '{route}'")
    state["route"] = route

    if route == "engineering":
        state = engineering_agent(state)
    elif route == "safety":
        # Import here to avoid circular imports if any
        from app.agents.safety import safety_agent
        state = safety_agent(state)
    else:
        state["answer"] = "I can only answer aerospace engineering and safety questions."
        state["confidence"] = "LOW"

    return state
