from app.core.llm import generate_response
from app.services.rag import retrieve_context
from app.models.state import WorkflowState
import json


def engineering_agent(state: WorkflowState) -> WorkflowState:
    """
    Retrieves relevant engineering context and generates a structured response.
    
    This agent:
    1. Retrieves document chunks relevant to the user's question.
    2. Constructs a prompt enforcing a JSON output structure.
    3. Calls the LLM to generate a summary, key findings, risks, and assumptions.
    4. Updates the state with the raw JSON answer and source documents.
    """
    question = state["question"]

    context, sources = retrieve_context(question)
    
    state["context"] = context
    
    if not sources:
        state["answer"] = "Information not found in documents."
        state["confidence"] = "LOW (no documents)"
        state["sources"] = []
        return state

    prompt = f"""
You are an aerospace engineering assistant.

Use ONLY the information below to answer the question.
If the answer is not in the context, say "Information not found in documents."

Context:
{context}

Question:
{question}

Format your response as a JSON object with the following keys:
- "summary": A brief summary of the answer.
- "key_findings": A list of key technical points.
- "risks": Any risks or safety considerations mentioned.
- "assumptions": Any assumptions made based on the context.

Ensure the JSON is valid.
"""

    response = generate_response(prompt)
    
    # Clean up response if it contains markdown code blocks
    if "```json" in response:
        response = response.split("```json")[1].split("```")[0].strip()
    elif "```" in response:
        response = response.split("```")[1].split("```")[0].strip()

    state["answer"] = response
    state["sources"] = sources
    state["confidence"] = "MEDIUM (document grounded)"

    return state
