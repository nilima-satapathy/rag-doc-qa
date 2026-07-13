"""
Milestone 3: ask a question → retrieve → LLM answer + citations.

Requires:
  - Built index: python scripts/build_index.py
  - XAI_API_KEY in environment or .env

Usage:
  python scripts/run_m3_ask.py "What timeout does ApiClient use?"
  python scripts/run_m3_ask.py "What is the capital of France?"   # should refuse / not invent from docs
  python scripts/run_m3_ask.py   # interactive
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import MAX_DISTANCE, TOP_K
from src.generate import answer_question, format_answer


def main() -> int:
    parser = argparse.ArgumentParser(description="M3: RAG answer + citations")
    parser.add_argument("question", nargs="?", help="Question about the PDFs")
    parser.add_argument("--top-k", type=int, default=TOP_K)
    parser.add_argument(
        "--max-distance",
        type=float,
        default=MAX_DISTANCE,
        help="If best hit is worse than this, skip LLM and say I don't know",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("Project 3 — Milestone 3: answer + citations")
    print("=" * 60)
    print(f"top_k        : {args.top_k}")
    print(f"max_distance : {args.max_distance}")
    print()

    def ask(q: str) -> int:
        try:
            result = answer_question(
                q, top_k=args.top_k, max_distance=args.max_distance
            )
        except RuntimeError as exc:
            print(f"ERROR: {exc}")
            return 1
        print(format_answer(result))
        return 0

    if args.question:
        code = ask(args.question)
        if code == 0:
            print("M3 OK — next: M4 Streamlit chat UI")
        return code

    print("Interactive mode (empty line to quit).")
    while True:
        try:
            q = input("question> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not q:
            break
        ask(q)
    return 0


if __name__ == "__main__":
    sys.exit(main())
