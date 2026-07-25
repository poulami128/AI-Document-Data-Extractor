import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def ask_question(document_text, question):

    prompt = f"""
You are an intelligent AI assistant.

Use the uploaded document as your primary source.

Rules:
1. Answer directly if the information is present.
2. If the answer requires reasoning based on the document (for example, suitable job roles, strengths, career suggestions, or likely skills), infer the answer from the document.
3. Clearly state when an answer is an inference.
4. If the document truly doesn't contain enough information to answer, reply:
   "The document does not contain enough information to answer this question."

Document:
{document_text}

Question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    return response.text