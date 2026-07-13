"""
Shared settings for the RAG pipeline.

M1: chunk size / overlap
M2: Chroma path, collection name, top_k
"""

from __future__ import annotations

import os
from pathlib import Path

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
