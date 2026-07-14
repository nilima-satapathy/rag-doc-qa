"""
Retrieve: embed chunks into Chroma and run similarity search.

Milestone 2: build index + query CLI (no LLM answer yet).
Chroma embeds documents automatically with its default embedding model.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import chromadb

from src.config import (
    CHROMA_DIR,
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    COLLECTION_NAME,
    DATA_DIR,
    TOP_K,
)
from src.ingest import Chunk, load_and_chunk_all


@dataclass
class SearchHit:
    """One retrieved chunk for a query."""

    rank: int
    source_file: str
    chunk_index: int
    text: str
    distance: float | None  # lower is closer for Chroma L2/cosine depending on space


def get_client(persist_dir: Path = CHROMA_DIR) -> chromadb.PersistentClient:
    """Persistent Chroma client (data survives process restarts)."""
    persist_dir = Path(persist_dir)
    persist_dir.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(persist_dir))


def index_chunk_count(
    *,
    persist_dir: Path = CHROMA_DIR,
    collection_name: str = COLLECTION_NAME,
) -> int:
    """Return number of vectors in the collection, or 0 if missing/empty."""
    try:
        client = get_client(persist_dir)
        col = client.get_collection(collection_name)
        return int(col.count())
    except Exception:  # noqa: BLE001
        return 0


def ensure_index(
    data_dir: Path = DATA_DIR,
    *,
    persist_dir: Path = CHROMA_DIR,
    collection_name: str = COLLECTION_NAME,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> dict[str, Any]:
    """
    Ensure a non-empty Chroma index exists (for deploy / cold start).

    If the collection is missing or empty, builds from data_dir PDFs.
    Safe to call on every app start; no-op when index already has vectors.
    """
    count = index_chunk_count(
        persist_dir=persist_dir, collection_name=collection_name
    )
    if count > 0:
        return {
            "chunk_count": count,
            "collection": collection_name,
            "persist_dir": str(Path(persist_dir).resolve()),
            "built": False,
        }
    stats = build_index(
        data_dir,
        persist_dir=persist_dir,
        collection_name=collection_name,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        reset=True,
    )
    stats["built"] = True
    return stats


def build_index(
    data_dir: Path = DATA_DIR,
    *,
    persist_dir: Path = CHROMA_DIR,
    collection_name: str = COLLECTION_NAME,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
    reset: bool = True,
) -> dict[str, Any]:
    """
    Load PDFs → chunk → embed + store in Chroma.

    If reset=True, drops the existing collection first so re-index is clean.
    """
    chunks: list[Chunk] = load_and_chunk_all(
        data_dir, chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    if not chunks:
        raise RuntimeError("No chunks produced — check your PDFs")

    client = get_client(persist_dir)

    if reset:
        try:
            client.delete_collection(collection_name)
        except Exception:  # noqa: BLE001 — collection may not exist yet
            pass

    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"},
    )

    ids = [f"{c.doc_id}__{c.chunk_index}" for c in chunks]
    documents = [c.text for c in chunks]
    metadatas = [
        {
            "source_file": c.source_file,
            "doc_id": c.doc_id,
            "chunk_index": c.chunk_index,
            "char_start": c.char_start,
            "char_end": c.char_end,
        }
        for c in chunks
    ]

    # Chroma embeds `documents` with its default embedding function
    collection.add(ids=ids, documents=documents, metadatas=metadatas)

    by_source: dict[str, int] = {}
    for c in chunks:
        by_source[c.source_file] = by_source.get(c.source_file, 0) + 1

    return {
        "chunk_count": len(chunks),
        "collection": collection_name,
        "persist_dir": str(Path(persist_dir).resolve()),
        "by_source": by_source,
    }


def search(
    query: str,
    *,
    top_k: int = TOP_K,
    persist_dir: Path = CHROMA_DIR,
    collection_name: str = COLLECTION_NAME,
) -> list[SearchHit]:
    """Return top_k most similar chunks for the query text."""
    query = (query or "").strip()
    if not query:
        raise ValueError("query must not be empty")
    if top_k < 1:
        raise ValueError("top_k must be >= 1")

    client = get_client(persist_dir)
    try:
        collection = client.get_collection(collection_name)
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            f"Collection '{collection_name}' not found. Run: python scripts/build_index.py"
        ) from exc

    count = collection.count()
    if count == 0:
        raise RuntimeError("Index is empty. Run: python scripts/build_index.py")

    n = min(top_k, count)
    raw = collection.query(
        query_texts=[query],
        n_results=n,
        include=["documents", "metadatas", "distances"],
    )

    documents = (raw.get("documents") or [[]])[0]
    metadatas = (raw.get("metadatas") or [[]])[0]
    distances = (raw.get("distances") or [[]])[0]

    hits: list[SearchHit] = []
    for i, (doc, meta, dist) in enumerate(zip(documents, metadatas, distances), start=1):
        meta = meta or {}
        hits.append(
            SearchHit(
                rank=i,
                source_file=str(meta.get("source_file", "unknown")),
                chunk_index=int(meta.get("chunk_index", -1)),
                text=doc or "",
                distance=float(dist) if dist is not None else None,
            )
        )
    return hits


def format_hit(hit: SearchHit, max_chars: int = 280) -> str:
    """Pretty print one search hit for the terminal."""
    preview = hit.text.replace("\n", " ")
    if len(preview) > max_chars:
        preview = preview[: max_chars - 3] + "..."
    dist = f"{hit.distance:.4f}" if hit.distance is not None else "n/a"
    return (
        f"#{hit.rank}  source={hit.source_file}  chunk={hit.chunk_index}  "
        f"distance={dist}\n"
        f"   {preview}"
    )
