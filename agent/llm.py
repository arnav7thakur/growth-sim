import requests
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Set API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/v1/chat/completions"

def get_goal_analysis(user_goal: str) -> str:
    """
    Uses GroqCloud (Mixtral) to analyze the user's goal and suggest an optimized strategy.
    """
    if not GROQ_API_KEY:
        return "Error: GROQ_API_KEY is missing. Please check your .env file."

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mixtral",  # Adjust if needed
        "messages": [
            {"role": "system", "content": "You are an expert in growth strategies."},
            {"role": "user", "content": f"Analyze the following goal and suggest strategies: {user_goal}"}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data)
        response.raise_for_status()  # Raise error if response is not 200
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"
