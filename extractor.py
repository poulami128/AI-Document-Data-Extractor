import os
import json
from dotenv import load_dotenv
from google import genai
from prompts import SYSTEM_PROMPT

# Load API key
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def extract_document_data(document_text):
    prompt = f"""
{SYSTEM_PROMPT}

Document:

{document_text}
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        text = response.text.strip()

        # Remove markdown code fences if Gemini returns them
        if text.startswith("```json"):
            text = text.replace("```json", "", 1)

        if text.startswith("```"):
            text = text.replace("```", "", 1)

        if text.endswith("```"):
            text = text[:-3]

        text = text.strip()

        return json.loads(text)

    except json.JSONDecodeError:
        return {
            "error": "Invalid JSON returned by Gemini",
            "response": text
        }

    except Exception as e:
        return {
            "error": str(e)
        }