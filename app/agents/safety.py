from app.models.state import WorkflowState

def safety_agent(state: WorkflowState) -> WorkflowState:
    state["answer"] = "Safety agent is not yet implemented. Please check back later."
    state["confidence"] = "LOW"
    state["sources"] = []
    return state
