import os
from groq import Groq
from dotenv import load_dotenv

from app.utils.prompts import SYSTEM_PROMPT

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL_NAME = os.getenv("LLM_MODEL")


def generate_response(
    user_message,
    session_memory,
    recommendations,
    clarification=None
):

    if clarification:
        return clarification

    history_text = ""

    for msg in session_memory["history"][-6:]:

        history_text += f"""
{msg['role'].upper()}:
{msg['content']}
"""

    recommendation_text = ""

    for idx, item in enumerate(recommendations, start=1):

        recommendation_text += f"""
{idx}. {item['name']}
Description: {item['description']}
Duration: {item['duration']}
"""

    user_prompt = f"""
Conversation History:
{history_text}

Session Context:
{session_memory}

Retrieved Recommendations:
{recommendation_text}

Latest User Message:
{user_message}

Generate a concise conversational recommendation response.

Rules:
- Mention only the most relevant assessments.
- Explain briefly why they fit.
- Keep response concise.
- Do not hallucinate assessments.
"""

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.2
    )

    return completion.choices[0].message.content