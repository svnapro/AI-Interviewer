import os
import requests

# ✅ Load from Streamlit Cloud Secrets or local environment
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()

# ✅ Streamlit Cloud app URL
APP_URL = os.getenv("APP_URL", "https://svnapro-ai-interviewer.streamlit.app")

# ✅ OpenRouter endpoint (ChatGPT-compatible)
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def chat_with_ai(messages, model="gpt-3.5-turbo"):
    """
    Connects to OpenRouter API (ChatGPT-compatible)
    and returns the model's text response.
    """

    # --- Headers (IMPORTANT) ---
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": APP_URL,     # MUST match deployed Streamlit domain
        "X-Title": "AI Interviewer",
        "Content-Type": "application/json"
    }

    # --- Body payload ---
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



