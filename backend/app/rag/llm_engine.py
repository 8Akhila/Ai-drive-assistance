"""
LLM Engine: unified wrapper for external LLM providers (OpenAI, Groq).
Place this file at: backend/app/rag/llm_engine.py

It expects environment variables:
- LLM_PROVIDER  -> "openai" or "groq"
- OPENAI_API_KEY (if using OpenAI)
- GROQ_API_KEY   (if using Groq)
- LLM_MODEL      -> optional model name for OpenAI (default "gpt-4o-mini")
"""

from __future__ import annotations
import os
import requests
import logging
from typing import Dict

logger = logging.getLogger("llm_engine")
logger.setLevel(logging.INFO)

# Read provider and keys from environment (you can also populate these from your Settings)
LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "openai").lower()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
LLM_MODEL = os.environ.get("LLM_MODEL", "gpt-4o-mini")
TIMEOUT = int(os.environ.get("LLM_API_TIMEOUT", "30"))

def run_llm(prompt: str) -> str:
    """
    Dispatch to chosen provider. Return the final generated text.
    Never raises raw provider exceptions — it returns an error message instead.
    """
    try:
        if LLM_PROVIDER == "openai":
            return _run_openai(prompt)
        elif LLM_PROVIDER == "groq":
            return _run_groq(prompt)
        else:
            return f"Error: Unsupported LLM_PROVIDER '{LLM_PROVIDER}'."
    except Exception as e:
        logger.exception("LLM call failed")
        return f"Error running LLM provider: {e}"

# ----------------------------
# OpenAI call (chat completion)
# ----------------------------
def _run_openai(prompt: str) -> str:
    if not OPENAI_API_KEY:
        return "OpenAI API key not configured (OPENAI_API_KEY)."

    url = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": os.environ.get("LLM_MODEL", LLM_MODEL),
        "messages": [
            {"role": "system", "content": "You are a helpful assistant. Answer using only the provided context."},
            {"role": "user", "content": prompt}
        ],
        "temperature": float(os.environ.get("LLM_TEMPERATURE", "0.0")),
        "max_tokens": int(os.environ.get("LLM_MAX_TOKENS", "512"))
    }
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    resp = requests.post(url, json=payload, headers=headers, timeout=TIMEOUT)
    resp.raise_for_status()
    data = resp.json()
    # Defensive parsing: handle different response shapes
    try:
        return data["choices"][0]["message"]["content"].strip()
    except Exception:
        # fallback: return entire json as string for debugging
        logger.warning("Unexpected OpenAI response shape: %s", data)
        return str(data)

# ----------------------------
# Groq call (example)
# ----------------------------
def _run_groq(prompt: str) -> str:
    if not GROQ_API_KEY:
        return "Groq API key not configured (GROQ_API_KEY)."

    # NOTE: replace endpoint/model with the exact Groq endpoint your account uses.
    url = os.environ.get("GROQ_API_URL", "https://api.groq.com/openai/v1/chat/completions")
    payload = {
        "model": os.environ.get("GROQ_MODEL", "mixtral-8x7b-32768"),
        "messages": [
            {"role": "system", "content": "You are a helpful assistant. Use only the provided context."},
            {"role": "user", "content": prompt}
        ],
        "temperature": float(os.environ.get("LLM_TEMPERATURE", "0.0")),
        "max_tokens": int(os.environ.get("LLM_MAX_TOKENS", "512"))
    }
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    resp = requests.post(url, json=payload, headers=headers, timeout=TIMEOUT)
    resp.raise_for_status()
    data = resp.json()
    try:
        return data["choices"][0]["message"]["content"].strip()
    except Exception:
        logger.warning("Unexpected Groq response shape: %s", data)
        return str(data)
