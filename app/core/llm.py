import os
import logging
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted, ServiceUnavailable, InternalServerError

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# List of models to try in order of preference for fallback
MODEL_PRIORITY = [
    "gemini-2.0-flash-exp", # Updated to a likely valid preview or keep user's if they insist, but 2.5 is likely a typo/future. I'll keep user's 2.5 as primary if it works, but add real ones.
    "gemini-1.5-flash",
    "gemini-1.5-pro"
]

# Default system instruction
DEFAULT_SYSTEM_INSTRUCTION = (
    "You are a careful aerospace engineering assistant. "
    "Be conservative, factual, and clear. "
    "If information is uncertain, say so explicitly."
)

def generate_response(prompt: str, json_mode: bool = False, system_instruction: str = None) -> str:
    """
    Generates a response using Gemini models with fallback support.
    
    Args:
        prompt: The user prompt.
        json_mode: Whether to enforce JSON output.
        system_instruction: Optional system instruction to override the default.
    
    Returns:
        The generated text response.
    """
    if system_instruction is None:
        system_instruction = DEFAULT_SYSTEM_INSTRUCTION

    generation_config = {
        "temperature": 0.2,
        "max_output_tokens": 2000
    }
    
    if json_mode:
        generation_config["response_mime_type"] = "application/json"

    last_exception = None

    # Try the user's original model first, then fallbacks
    models_to_try = ["gemini-2.5-flash"] + MODEL_PRIORITY

    for model_name in models_to_try:
        try:
            logger.info(f"Attempting to generate response with model: {model_name}")
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=system_instruction
            )
            response = model.generate_content(
                prompt,
                generation_config=generation_config
            )
            return response.text
        except (ResourceExhausted, ServiceUnavailable, InternalServerError) as e:
            logger.warning(f"Model {model_name} failed with error: {e}. Trying next model...")
            last_exception = e
            continue
        except Exception as e:
            # If the model name is invalid (e.g. 404), we should also try the next one
            if "404" in str(e) or "not found" in str(e).lower():
                 logger.warning(f"Model {model_name} not found. Trying next model...")
                 continue
            
            logger.error(f"Non-retriable error with model {model_name}: {e}")
            return f"Error generating response: {str(e)}"

    return f"Error: All AI models failed. Last error: {str(last_exception)}"
