from app.core.llm import generate_response
from app.models.state import WorkflowState
import logging
import json

logger = logging.getLogger(__name__)

def verifier_agent(state: WorkflowState) -> WorkflowState:
    """
    Validates the generated answer against the retrieved context.
    
    This agent acts as a safety check to ensure the answer is grounded in the provided documents.
    It assigns a verification status (PASS, PARTIAL, FAIL) and provides notes on any discrepancies.
    """
    # If no answer or context, skip verification
    if not state.get("answer") or not state.get("context"):
        logger.info("Skipping verification: No answer or context.")
        state["verification_status"] = "SKIPPED"
        state["verification_notes"] = "No answer or context to verify."
        return state

    system_instruction = "You are a strict technical verifier for an aerospace engineering system."
    prompt = f"""
Your job is to check if the generated ANSWER is fully supported by the provided CONTEXT.

CONTEXT:
{state['context']}

ANSWER:
{state['answer']}

INSTRUCTIONS:
1. Check if every claim in the ANSWER is supported by the CONTEXT.
2. If the answer contains information NOT in the context, mark as FAIL.
3. If the answer is fully supported, mark as PASS.
4. If the answer is mostly supported but has minor hallucinations, mark as PARTIAL.

Output a JSON object with the following keys:
- "status": One of ["PASS", "PARTIAL", "FAIL"]
- "notes": Brief explanation of your decision.
"""

    try:
        response = generate_response(prompt, json_mode=True, system_instruction=system_instruction)
        
        # Clean up response if it contains markdown code blocks
        if "```json" in response:
            response = response.split("```json")[1].split("```")[0].strip()
        elif "```" in response:
            response = response.split("```")[1].split("```")[0].strip()
            
        data = json.loads(response)
        status = data.get("status", "FAIL")
        notes = data.get("notes", "No notes provided.")
                
        state["verification_status"] = status
        state["verification_notes"] = notes
        
        if status != "PASS":
            logger.warning(f"Verification failed or partial. Status: {status}. Notes: {notes}")
        else:
            logger.info("Verification passed.")
            
    except Exception as e:
        logger.error(f"Verifier LLM failed: {e}")
        state["verification_status"] = "ERROR"
        state["verification_notes"] = "Verification process failed."
    
    return state
