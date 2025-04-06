import requests
import os
import ast  # safer than eval
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def get_goal_analysis(user_goal: str) -> list:
    """
    Uses Groq (Mixtral) to analyze the user's goal and return strategy suggestions as a Python list.
    Falls back to an empty list on any error.
    """
    if not GROQ_API_KEY:
        print("⚠️ No GROQ_API_KEY found.")
        return []

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a growth strategist for startups. Based on the user's goal, "
                    "recommend 2 to 4 relevant growth strategies. "
                    "Only respond with a Python list in lowercase snake_case. "
                    "Example: ['referral_program', 'localization']"
                )
            },
            {
                "role": "user",
                "content": f"My growth goal is: {user_goal}"
            }
        ],
        "temperature": 0.4
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        #print("Groq raw response:", response.text)
        response.raise_for_status()

        content = response.json()["choices"][0]["message"]["content"]
        strategies = ast.literal_eval(content.strip())  # safer than eval

        if isinstance(strategies, list):
            return [s.strip() for s in strategies if isinstance(s, str)]

        print("⚠️ LLM returned unexpected format:", content)
        return []

    except requests.exceptions.RequestException as e:
        print(f"LLM API Error: {e}")
        return []

    except (ValueError, SyntaxError) as e:
        print(f"LLM Response Parsing Error: {e} — Raw content: {content}")
        return []
