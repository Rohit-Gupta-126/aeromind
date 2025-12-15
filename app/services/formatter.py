import json
import logging

logger = logging.getLogger(__name__)

def format_response(answer: str) -> str:
    """
    Converts a JSON string answer into a formatted Markdown string.
    
    This function handles the transformation of structured agent output (JSON)
    into a human-readable format suitable for the API response.
    If the answer is not valid JSON, returns the original string.
    """
    try:
        data = json.loads(answer)
        
        markdown_output = ""
        
        if "summary" in data:
            markdown_output += f"### Summary\n{data['summary']}\n\n"
            
        if "key_findings" in data and isinstance(data["key_findings"], list):
            markdown_output += "### Key Findings\n"
            for item in data["key_findings"]:
                markdown_output += f"- {item}\n"
            markdown_output += "\n"
            
        if "risks" in data:
            markdown_output += f"### Risks & Considerations\n{data['risks']}\n\n"
            
        if "assumptions" in data:
            markdown_output += f"### Assumptions\n{data['assumptions']}\n\n"
            
        return markdown_output.strip()
        
    except json.JSONDecodeError:
        logger.warning("Failed to parse answer as JSON. Returning raw text.")
        return answer
    except Exception as e:
        logger.error(f"Error formatting response: {e}")
        return answer
