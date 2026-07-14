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

try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
except ImportError:
    pass

ROOT = Path(__file__).resolve().parents[1]
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
LLM_PROVIDER = os.getenv("RAG_LLM_PROVIDER", "extractive").strip().lower()

# xAI / SpaceXAI (paid credits)
XAI_API_KEY = os.getenv("XAI_API_KEY", "")
XAI_BASE_URL = os.getenv("XAI_BASE_URL", "https://api.x.ai/v1")

# Ollama (free, local) — https://ollama.com
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

# Google Gemini free tier — https://aistudio.google.com/apikey
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "") or os.getenv("GOOGLE_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# Default model name depends on provider (override with RAG_LLM_MODEL)
_default_models = {
    "xai": "grok-4.5",
    "ollama": OLLAMA_MODEL,
    "gemini": GEMINI_MODEL,
    "extractive": "none",
}
LLM_MODEL = os.getenv("RAG_LLM_MODEL", _default_models.get(LLM_PROVIDER, "none"))

# Weak retrieval cutoff
MAX_DISTANCE = float(os.getenv("RAG_MAX_DISTANCE", "1.05"))
