import json

from groq import Groq
from django.conf import settings


client = Groq(
    api_key=settings.GROQ_API_KEY
)


def assign_priority(subject, description):
    """
    Analyze ticket and return priority + department.
    """

    prompt = f"""
You are an AI Customer Support Classifier.

Analyze the ticket.

Subject:
{subject}

Description:
{description}

Choose:

Priority:
- Low
- Medium
- High

Department:
- Technical
- Billing
- Sales
- General

Return ONLY valid JSON.

Example:

{{
    "priority":"High",
    "department":"Technical"
}}
"""

    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            temperature=0,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        result = response.choices[0].message.content.strip()

        if result.startswith("```"):
            result = (
                result.replace("```json", "")
                      .replace("```", "")
                      .strip()
            )

        return json.loads(result)

    except Exception as e:

        print("Groq Error:", e)

        return {

            "priority": "Medium",

            "department": "General"

        }