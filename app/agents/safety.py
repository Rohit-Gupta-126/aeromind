from app.core.llm import generate_response
from app.services.rag import retrieve_context
from app.models.state import WorkflowState

def safety_agent(state: WorkflowState) -> WorkflowState:
    """
    Retrieves relevant safety context and generates a structured response.
    """
    question = state["question"]

    # Retrieve context - assuming the same RAG system contains safety docs
    context, sources = retrieve_context(question)
    
    state["context"] = context
    
    if not sources:
        state["answer"] = "Safety information not found in documents."
        state["confidence"] = "LOW (no documents)"
        state["sources"] = []
        return state

    system_instruction = "You are an aerospace safety expert. Your goal is to identify hazards, regulations, and safety protocols."
    prompt = f"""
Use ONLY the information below to answer the safety-related question.
If the answer is not in the context, say "Information not found in documents."

Context:
{context}

Question:
{question}

Format your response as a JSON object with the following keys:
- "summary": A brief summary of the safety answer.
- "regulations": Relevant regulations or standards (e.g., FAA, EASA).
- "hazards": Potential hazards identified.
- "mitigations": Recommended safety mitigations.
"""

    response = generate_response(prompt, json_mode=True, system_instruction=system_instruction)
    
    # Clean up response if it contains markdown code blocks
    if "```json" in response:
        response = response.split("```json")[1].split("```")[0].strip()
    elif "```" in response:
        response = response.split("```")[1].split("```")[0].strip()

    state["answer"] = response
    state["sources"] = sources
    state["confidence"] = "MEDIUM (document grounded)"

    return state
