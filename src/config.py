"""
Shared settings for the RAG pipeline.

LLM providers (free options available):
  extractive — no LLM, show best matching PDF text (100% free, default)
  ollama     — free local models (install Ollama + pull a model)
  gemini     — Google AI Studio free API key
  xai        — SpaceXAI / Grok (needs paid credits)
"""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_ENV_PATH = ROOT / ".env"


def reload_env() -> None:
    """Re-read .env into process env (safe to call before each LLM request)."""
    try:
        from dotenv import load_dotenv

        load_dotenv(_ENV_PATH, override=True)
    except ImportError:
        pass


reload_env()

DATA_DIR = Path(os.getenv("RAG_DATA_DIR", ROOT / "data"))


# --- Chunking (M1) ---
CHUNK_SIZE = int(os.getenv("RAG_CHUNK_SIZE", "800"))
CHUNK_OVERLAP = int(os.getenv("RAG_CHUNK_OVERLAP", "120"))

if CHUNK_SIZE < 50:
    raise ValueError("RAG_CHUNK_SIZE must be at least 50")
if CHUNK_OVERLAP < 0 or CHUNK_OVERLAP >= CHUNK_SIZE:
    raise ValueError("RAG_CHUNK_OVERLAP must be >= 0 and < RAG_CHUNK_SIZE")

# --- Vector store (M2) ---
CHROMA_DIR = Path(os.getenv("RAG_CHROMA_DIR", ROOT / ".chroma"))
COLLECTION_NAME = os.getenv("RAG_COLLECTION_NAME", "rag_docs")
TOP_K = int(os.getenv("RAG_TOP_K", "3"))

if TOP_K < 1:
    raise ValueError("RAG_TOP_K must be >= 1")

# --- LLM provider (M3+) ---
# extractive | ollama | gemini | xai
def _env(name: str, default: str = "") -> str:
    return (os.getenv(name, default) or default).strip()


def get_llm_provider() -> str:
    reload_env()
    return _env("RAG_LLM_PROVIDER", "extractive").lower()


def get_gemini_api_key() -> str:
    reload_env()
    return _env("GEMINI_API_KEY") or _env("GOOGLE_API_KEY")


def get_xai_api_key() -> str:
    reload_env()
    return _env("XAI_API_KEY")


def get_ollama_settings() -> tuple[str, str]:
    reload_env()
    return (
        _env("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
        _env("OLLAMA_MODEL", "llama3.2"),
    )


# Snapshots at import (UI defaults); LLM calls should use get_* helpers above
LLM_PROVIDER = get_llm_provider()
XAI_API_KEY = get_xai_api_key()
XAI_BASE_URL = _env("XAI_BASE_URL", "https://api.x.ai/v1")
OLLAMA_BASE_URL, OLLAMA_MODEL = get_ollama_settings()
GEMINI_API_KEY = get_gemini_api_key()
# Prefer 1.5-flash: free-tier friendly. 2.0-flash often shows limit:0 in some regions.
GEMINI_MODEL = _env("GEMINI_MODEL", "gemini-1.5-flash")


_default_models = {
    "xai": "grok-4.5",
    "ollama": OLLAMA_MODEL,
    "gemini": GEMINI_MODEL,
    "extractive": "none",
}
LLM_MODEL = _env("RAG_LLM_MODEL", _default_models.get(LLM_PROVIDER, "none"))

# Weak retrieval cutoff
MAX_DISTANCE = float(_env("RAG_MAX_DISTANCE", "1.05"))
