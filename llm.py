import requests
import os

# Load secrets - Streamlit Cloud uses st.secrets
try:
    import streamlit as st
    API_URL = st.secrets.get("LLM_API_URL", "https://api.groq.com/openai/v1/chat/completions")
    API_KEY = st.secrets.get("LLM_API_KEY")
    MODEL_NAME = st.secrets.get("LLM_MODEL", "llama-3.1-8b-instant")
except Exception:
    # Fallback to environment variables for local development
    from dotenv import load_dotenv
    load_dotenv()
    API_URL = os.getenv("LLM_API_URL", "https://api.groq.com/openai/v1/chat/completions")
    API_KEY = os.getenv("LLM_API_KEY")
    MODEL_NAME = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")


def call_llm(prompt):
    if not API_KEY:
        raise ValueError("LLM_API_KEY not found. Please set it in .env file or Streamlit secrets.")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as e:
        error_detail = response.json() if response.text else "No error details"
        print(f"API Error: {error_detail}")
        raise Exception(f"Groq API Error: {error_detail}")
