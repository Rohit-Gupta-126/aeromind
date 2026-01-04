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
            markdown_output += "### Summary\n"
            if isinstance(data["summary"], list):
                for item in data["summary"]:
                    markdown_output += f"{item} "
                markdown_output += "\n\n"
            else:
                markdown_output += f"{data['summary']}\n\n"
            
        if "key_findings" in data and isinstance(data["key_findings"], list):
            markdown_output += "### Key Findings\n"
            for item in data["key_findings"]:
                markdown_output += f"- {item}\n"
            markdown_output += "\n"
            
        if "risks" in data:
            markdown_output += "### Risks & Considerations\n"
            if isinstance(data["risks"], list):
                for item in data["risks"]:
                    markdown_output += f"- {item}\n"
            else:
                markdown_output += f"{data['risks']}\n"
            markdown_output += "\n"
        if "assumptions" in data:
            markdown_output += "### Assumptions\n"
            if isinstance(data["assumptions"], list):
                for item in data["assumptions"]:
                    markdown_output += f"- {item}\n"
            else:
                markdown_output += f"{data['assumptions']}\n"
            markdown_output += "\n"

        if "regulations" in data:
            markdown_output += "### Regulations & Standards\n"
            if isinstance(data["regulations"], list):
                for item in data["regulations"]:
                    markdown_output += f"- {item}\n"
            else:
                markdown_output += f"{data['regulations']}\n"
            markdown_output += "\n"

        if "hazards" in data:
            markdown_output += "### Identified Hazards\n"
            if isinstance(data["hazards"], list):
                for item in data["hazards"]:
                    markdown_output += f"- {item}\n"
            else:
                markdown_output += f"{data['hazards']}\n"
            markdown_output += "\n"

        if "mitigations" in data:
            markdown_output += "### Recommended Mitigations\n"
            if isinstance(data["mitigations"], list):
                for item in data["mitigations"]:
                    markdown_output += f"- {item}\n"
            else:
                markdown_output += f"{data['mitigations']}\n"
            markdown_output += "\n"
            
        return markdown_output.strip()
        
    except json.JSONDecodeError:
        logger.warning("Failed to parse answer as JSON. Returning raw text.")
        return answer
    except Exception as e:
        logger.error(f"Error formatting response: {e}")
        return answer
