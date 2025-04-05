import requests
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Set API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"


def get_goal_analysis(user_goal: str) -> list:
    """
    Uses Groq (Mixtral) to analyze the user's goal and return strategy suggestions as a Python list.
    """
    if not GROQ_API_KEY:
        return []

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mixtral-8x7b-32768",
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
            {"role": "user", "content": f"My growth goal is: {user_goal}"}
        ],
        "temperature": 0.4
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data)
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]

        # Try to safely parse the returned list
        strategies = eval(content.strip())
        if isinstance(strategies, list):
            return [s.strip() for s in strategies]
        return []
    except Exception as e:
        print(f"LLM Error: {e}")
        return []

