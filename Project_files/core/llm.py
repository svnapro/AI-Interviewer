import os
import requests

# Load your OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()

# Define your Streamlit App URL
APP_URL = os.getenv("APP_URL", "https://svnapro-ai-interviewer.streamlit.app")

# OpenRouter Chat Completions Endpoint
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def chat_with_ai(messages, model="gpt-3.5-turbo"):
    """
    Sends a chat message list to OpenRouter's ChatGPT-compatible API.
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Referer": APP_URL,  # ✅ Changed from HTTP-Referer to Referer
        "X-Title": "AI Interviewer",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7
    }

    try:
        res = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        if res.status_code != 200:
            return f"❌ API Error {res.status_code}: {res.text[:200]}"
        data = res.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"❌ Exception: {e}"
