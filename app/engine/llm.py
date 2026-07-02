import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-2.5-flash")


def generate_llm_response(user_query, recommendations):
    if not recommendations:
        return "No matching assessments found."

    rec_text = "\n".join(
        [f"- {r['name']} ({r['test_type']})" for r in recommendations]
    )

    prompt = f"""
User query: {user_query}

Recommended assessments:
{rec_text}

Explain why these SHL assessments match the user's requirements.
Keep answer short, professional, and clear.
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("Gemini Error:", e)
        return (
            "These assessments match the requested role because they evaluate "
            "technical, analytical, and role-specific skills."
        )