"""
Milestone 2 demo: similarity search over the Chroma index.

Usage:
  python scripts/run_m2_search.py "What is ApiClient?"
  python scripts/run_m2_search.py "What is POM?" --top-k 5
  python scripts/run_m2_search.py   # interactive prompts
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import CHROMA_DIR, COLLECTION_NAME, TOP_K
from src.retrieve import format_hit, search


def run_query(query: str, top_k: int) -> int:
    print("-" * 60)
    print(f"Query : {query}")
    print(f"top_k : {top_k}")
    print("-" * 60)
    try:
        hits = search(query, top_k=top_k)
    except RuntimeError as exc:
        print(f"ERROR: {exc}")
        return 1

    if not hits:
        print("No results.")
        return 0

    for hit in hits:
        print(format_hit(hit))
        print()
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="M2: similarity search CLI")
    parser.add_argument("query", nargs="?", help="Search question / phrase")
    parser.add_argument("--top-k", type=int, default=TOP_K)
    parser.add_argument("--chroma-dir", type=Path, default=CHROMA_DIR)
    parser.add_argument("--collection", default=COLLECTION_NAME)
    args = parser.parse_args()

    # Allow overrides via env-style paths already in config; scripts pass through config defaults.
    # If user passes custom chroma dir we temporarily rely on search() defaults unless we wire it:
    from src import retrieve as retrieve_mod

    # Monkey-patch free: pass kwargs into search
    def _search(q: str, top_k: int):
        return retrieve_mod.search(
            q,
            top_k=top_k,
            persist_dir=args.chroma_dir,
            collection_name=args.collection,
        )

    print("=" * 60)
    print("Project 3 — Milestone 2: similarity search")
    print("=" * 60)
    print(f"chroma_dir : {args.chroma_dir}")
    print(f"collection : {args.collection}")
    print()

    if args.query:
        try:
            hits = _search(args.query, args.top_k)
        except RuntimeError as exc:
            print(f"ERROR: {exc}")
            return 1
        print("-" * 60)
        print(f"Query : {args.query}")
        print(f"top_k : {args.top_k}")
        print("-" * 60)
        for hit in hits:
            print(format_hit(hit))
            print()
        print("M2 OK — next: M3 LLM answer + citations")
        return 0

    # Interactive mode
    print("Interactive mode (empty line to quit). Build index first if needed.")
    print('Example: What timeout does ApiClient use?')
    print()
    while True:
        try:
            q = input("query> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not q:
            break
        try:
            hits = _search(q, args.top_k)
        except RuntimeError as exc:
            print(f"ERROR: {exc}")
            continue
        for hit in hits:
            print(format_hit(hit))
            print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
