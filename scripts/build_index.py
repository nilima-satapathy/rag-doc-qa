"""
Milestone 2: build (or rebuild) the Chroma vector index from data/*.pdf

Usage:
  python scripts/build_index.py
  python scripts/build_index.py --chunk-size 500 --chunk-overlap 80
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import CHUNK_OVERLAP, CHUNK_SIZE, CHROMA_DIR, COLLECTION_NAME, DATA_DIR
from src.retrieve import build_index


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Chroma index from PDFs")
    parser.add_argument("--data-dir", type=Path, default=DATA_DIR)
    parser.add_argument("--chroma-dir", type=Path, default=CHROMA_DIR)
    parser.add_argument("--collection", default=COLLECTION_NAME)
    parser.add_argument("--chunk-size", type=int, default=CHUNK_SIZE)
    parser.add_argument("--chunk-overlap", type=int, default=CHUNK_OVERLAP)
    parser.add_argument(
        "--no-reset",
        action="store_true",
        help="Do not delete existing collection first (default: reset)",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("Project 3 — M2: build vector index")
    print("=" * 60)
    print(f"data_dir     : {args.data_dir}")
    print(f"chroma_dir   : {args.chroma_dir}")
    print(f"collection   : {args.collection}")
    print(f"chunk_size   : {args.chunk_size}")
    print(f"chunk_overlap: {args.chunk_overlap}")
    print()
    print("Indexing (first run may download a small embedding model)...")

    stats = build_index(
        args.data_dir,
        persist_dir=args.chroma_dir,
        collection_name=args.collection,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        reset=not args.no_reset,
    )

    print()
    print(f"Indexed {stats['chunk_count']} chunks into '{stats['collection']}'")
    print(f"Store   : {stats['persist_dir']}")
    for source, n in sorted(stats["by_source"].items()):
        print(f"  - {source}: {n} chunks")
    print()
    print("Next: python scripts/run_m2_search.py \"What is RAG?\"")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
