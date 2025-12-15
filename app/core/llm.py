import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-lite",
    system_instruction=(
        "You are a careful aerospace engineering assistant. "
        "Be conservative, factual, and clear. "
        "If information is uncertain, say so explicitly."
    )
)

def generate_response(prompt: str) -> str:
    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.2,
                "max_output_tokens": 500
            }
        )
        return response.text
    except ResourceExhausted:
        # In production, we should log this critical error and potentially alert.
        # We return a specific error message that agents can detect if needed.
        return "Error: AI Model quota exceeded. Please try again later."
    except Exception as e:
        return f"Error generating response: {str(e)}"
