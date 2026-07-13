"""
Shared settings for the RAG pipeline.

Milestone 1: chunk size / overlap (configurable).
Later milestones: paths for vector store, model names, etc.
"""

from __future__ import annotations

import os
from pathlib import Path

# Project root = parent of src/
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = Path(os.getenv("RAG_DATA_DIR", ROOT / "data"))

# --- Chunking (M1) ---
# Defaults are a reasonable starting point for short portfolio PDFs.
# Override with env vars without changing code:
#   $env:RAG_CHUNK_SIZE = "500"
#   $env:RAG_CHUNK_OVERLAP = "50"
CHUNK_SIZE = int(os.getenv("RAG_CHUNK_SIZE", "800"))
CHUNK_OVERLAP = int(os.getenv("RAG_CHUNK_OVERLAP", "120"))

if CHUNK_SIZE < 50:
    raise ValueError("RAG_CHUNK_SIZE must be at least 50")
if CHUNK_OVERLAP < 0 or CHUNK_OVERLAP >= CHUNK_SIZE:
    raise ValueError("RAG_CHUNK_OVERLAP must be >= 0 and < RAG_CHUNK_SIZE")
