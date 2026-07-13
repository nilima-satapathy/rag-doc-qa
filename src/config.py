"""
Shared settings for the RAG pipeline.

M1: chunk size / overlap
M2: Chroma path, collection name, top_k
M3: LLM (SpaceXAI / xAI) + weak-retrieval threshold
"""

from __future__ import annotations

import os
from pathlib import Path

# Load .env if present (never commit real .env)
try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parents[1] / ".env")
except ImportError:
    pass

# Project root = parent of src/
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

# --- LLM (M3) — SpaceXAI via xAI OpenAI-compatible API ---
XAI_API_KEY = os.getenv("XAI_API_KEY", "")
XAI_BASE_URL = os.getenv("XAI_BASE_URL", "https://api.x.ai/v1")
# Default chat model (override with RAG_LLM_MODEL if needed)
LLM_MODEL = os.getenv("RAG_LLM_MODEL", "grok-4.5")

# If the best chunk distance is worse than this, treat retrieval as too weak
# (Chroma cosine distance: lower is better; good hits in our demos were ~0.6–0.8)
MAX_DISTANCE = float(os.getenv("RAG_MAX_DISTANCE", "1.05"))
