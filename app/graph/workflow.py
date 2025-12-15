from app.agents.router import route_query
from app.agents.verifier import verifier_agent
from app.models.state import WorkflowState
from app.services.formatter import format_response


def run_workflow(question: str) -> dict:
    """
    Orchestrates the multi-agent workflow for processing a user query.
    
    Steps:
    1. Initialize workflow state.
    2. Route the query to the appropriate agent (Engineering, Safety, etc.).
    3. Execute the selected agent to generate an answer.
    4. Run the Verifier Agent to check for hallucinations (if applicable).
    5. Format the final response for the API.
    """
    state: WorkflowState = {
        "question": question,
        "route": None,
        "answer": None,
        "confidence": "LOW",
        "sources": [],
        "context": None,
        "verification_status": None,
        "verification_notes": None
    }

    state = route_query(state)
    
    # Run verifier if we have an answer and it's an engineering query
    if state["route"] == "engineering" and state["answer"]:
        state = verifier_agent(state)
        
        # Adjust confidence based on verification
        if state["verification_status"] == "PASS":
            state["confidence"] = "HIGH (verified)"
        elif state["verification_status"] == "PARTIAL":
            state["confidence"] = "MEDIUM (partial verification)"
        elif state["verification_status"] == "FAIL":
            state["confidence"] = "LOW (verification failed)"

    return {
        "question": state["question"],
        "route_selected": state["route"] or "unknown",
        "answer": format_response(state["answer"]) if state["answer"] else "No answer generated.",
        "confidence": state["confidence"] or "LOW",
        "sources": state.get("sources", []),
        "verification_status": state.get("verification_status"),
        "verification_notes": state.get("verification_notes")
    }
