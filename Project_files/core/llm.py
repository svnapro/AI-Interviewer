import os
import requests

# ✅ Set your OpenRouter key here or as environment variable
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "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")

API_URL = "https://openrouter.ai/api/v1/chat/completions"

def chat_with_ai(messages, model="gpt-3.5-turbo"):
    """
    Query the OpenRouter (ChatGPT-compatible) API.
    messages = [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://svnapro-ai-interviewer.streamlit.app/",
        "X-Title": "AI Interviewer"
    }

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        if response.status_code != 200:
            return f"❌ API Error {response.status_code}: {response.text[:150]}"
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"❌ Exception: {e}"
