"""
Milestone 1 demo: load PDFs from data/ → chunk → print summary + previews.

Usage (from project root, venv active):
  python scripts/run_m1_chunk.py
  python scripts/run_m1_chunk.py --chunk-size 400 --chunk-overlap 80
  python scripts/run_m1_chunk.py --preview 3
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import CHUNK_OVERLAP, CHUNK_SIZE, DATA_DIR
from src.ingest import format_chunk_preview, list_pdfs, load_and_chunk_all


def main() -> int:
    parser = argparse.ArgumentParser(description="M1: PDF load + chunk preview")
    parser.add_argument("--chunk-size", type=int, default=CHUNK_SIZE)
    parser.add_argument("--chunk-overlap", type=int, default=CHUNK_OVERLAP)
    parser.add_argument(
        "--preview",
        type=int,
        default=2,
        help="How many chunk previews to print per PDF (default 2)",
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=DATA_DIR,
        help="Folder containing PDFs",
    )
    args = parser.parse_args()

    pdfs = list_pdfs(args.data_dir)
    print("=" * 60)
    print("Project 3 — Milestone 1: PDF load + chunking")
    print("=" * 60)
    print(f"data_dir     : {args.data_dir}")
    print(f"chunk_size   : {args.chunk_size}")
    print(f"chunk_overlap: {args.chunk_overlap}")
    print(f"PDFs found   : {len(pdfs)}")
    for p in pdfs:
        print(f"  - {p.name}")
    print()

    if not pdfs:
        print("No PDFs found. Run: python scripts/generate_sample_pdfs.py")
        return 1

    chunks = load_and_chunk_all(
        args.data_dir,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
    )

    by_source: dict[str, list] = defaultdict(list)
    for c in chunks:
        by_source[c.source_file].append(c)

    print(f"Total chunks : {len(chunks)}")
    print("-" * 60)
    for source, group in by_source.items():
        lengths = [len(c.text) for c in group]
        print(
            f"{source}: {len(group)} chunks "
            f"(min={min(lengths)}, max={max(lengths)}, avg={sum(lengths)//len(lengths)} chars)"
        )
        for c in group[: args.preview]:
            print(format_chunk_preview(c))
            print()
        if len(group) > args.preview:
            print(f"  ... ({len(group) - args.preview} more chunks not shown)")
            print()

    print("=" * 60)
    print("M1 OK — next: M2 embed + store + similarity search")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
