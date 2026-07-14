"""
Milestone 5 — evaluate retrieval quality on a golden question set.

Metrics (no LLM required by default):
  - retrieval_hit@k: expected PDF appears in top-k sources
  - context_keyword_hit: at least one must_include phrase appears in retrieved text
  - avg latency (ms) per question

Optional:
  --with-llm   also call answer_question (needs XAI_API_KEY + credits)

Usage (from project root):
  python eval/run_eval.py
  python eval/run_eval.py --top-k 3
  python eval/run_eval.py --with-llm
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import TOP_K
from src.retrieve import search

QUESTIONS_PATH = Path(__file__).resolve().parent / "questions.json"
RESULTS_PATH = Path(__file__).resolve().parent / "last_results.json"


def load_questions(path: Path = QUESTIONS_PATH) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list) or len(data) < 10:
        raise ValueError("questions.json must be a list of at least 10 items")
    return data


def context_has_keyword(text: str, keywords: list[str]) -> bool:
    lower = text.lower()
    return any(k.lower() in lower for k in keywords)


def evaluate_one(
    case: dict[str, Any],
    *,
    top_k: int,
    with_llm: bool,
) -> dict[str, Any]:
    q = case["question"]
    t0 = time.perf_counter()
    hits = search(q, top_k=top_k)
    retrieval_ms = (time.perf_counter() - t0) * 1000

    sources = [h.source_file for h in hits]
    joined = "\n".join(h.text for h in hits)
    relevant = case.get("relevant_doc")
    expect_weak = bool(case.get("expect_weak"))

    if expect_weak or relevant is None:
        # For out-of-corpus questions we only record retrieval; not scored as doc hit
        doc_hit = None
    else:
        doc_hit = relevant in sources

    keywords = case.get("must_include_in_context") or []
    kw_hit = context_has_keyword(joined, keywords) if keywords else None

    row: dict[str, Any] = {
        "id": case.get("id"),
        "question": q,
        "relevant_doc": relevant,
        "expect_weak": expect_weak,
        "top_sources": sources,
        "retrieval_hit": doc_hit,
        "keyword_hit": kw_hit,
        "retrieval_ms": round(retrieval_ms, 1),
        "best_distance": hits[0].distance if hits else None,
    }

    if with_llm:
        from src.generate import answer_question

        t1 = time.perf_counter()
        try:
            result = answer_question(q, top_k=top_k)
            row["answer_preview"] = result.answer[:240]
            row["used_llm"] = result.used_llm
            row["weak_retrieval"] = result.weak_retrieval
            row["llm_error"] = None
        except Exception as exc:  # noqa: BLE001
            row["answer_preview"] = None
            row["used_llm"] = False
            row["weak_retrieval"] = None
            row["llm_error"] = str(exc)[:300]
        row["total_ms"] = round((time.perf_counter() - t1) * 1000 + retrieval_ms, 1)

    return row


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    scored = [r for r in rows if r.get("retrieval_hit") is not None]
    hits = sum(1 for r in scored if r["retrieval_hit"])
    kw_rows = [r for r in rows if r.get("keyword_hit") is not None]
    kw_hits = sum(1 for r in kw_rows if r["keyword_hit"])
    latencies = [r["retrieval_ms"] for r in rows]

    return {
        "n_questions": len(rows),
        "n_scored_doc_hit": len(scored),
        "retrieval_hit_rate": f"{hits}/{len(scored)}" if scored else "n/a",
        "retrieval_hit_rate_pct": round(100 * hits / len(scored), 1) if scored else None,
        "keyword_hit_rate": f"{kw_hits}/{len(kw_rows)}" if kw_rows else "n/a",
        "keyword_hit_rate_pct": round(100 * kw_hits / len(kw_rows), 1) if kw_rows else None,
        "avg_retrieval_ms": round(sum(latencies) / len(latencies), 1) if latencies else None,
        "misses": [
            {"id": r["id"], "question": r["question"], "got": r["top_sources"]}
            for r in scored
            if not r["retrieval_hit"]
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="M5: RAG retrieval eval")
    parser.add_argument("--top-k", type=int, default=TOP_K)
    parser.add_argument("--questions", type=Path, default=QUESTIONS_PATH)
    parser.add_argument("--with-llm", action="store_true")
    parser.add_argument(
        "--rebuild-index",
        action="store_true",
        help="Rebuild Chroma index before eval",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("Project 3 — Milestone 5: evaluation")
    print("=" * 60)

    if args.rebuild_index:
        from src.retrieve import build_index

        print("Rebuilding index...")
        stats = build_index(reset=True)
        print(f"  indexed {stats['chunk_count']} chunks")

    cases = load_questions(args.questions)
    print(f"questions : {len(cases)} from {args.questions.name}")
    print(f"top_k     : {args.top_k}")
    print(f"with_llm  : {args.with_llm}")
    print()

    rows: list[dict[str, Any]] = []
    for case in cases:
        row = evaluate_one(case, top_k=args.top_k, with_llm=args.with_llm)
        rows.append(row)
        flag = row["retrieval_hit"]
        if flag is True:
            mark = "HIT "
        elif flag is False:
            mark = "MISS"
        else:
            mark = "skip"
        kw = row["keyword_hit"]
        kw_s = "kw+" if kw else ("kw-" if kw is False else "kw?")
        print(
            f"[{mark}|{kw_s}] {row['id']}: {row['question'][:56]}... "
            f"({row['retrieval_ms']} ms) → {row['top_sources'][:2]}"
        )

    summary = summarize(rows)
    print()
    print("-" * 60)
    print("SUMMARY")
    print(f"  Retrieval hit@k     : {summary['retrieval_hit_rate']} "
          f"({summary['retrieval_hit_rate_pct']}%)")
    print(f"  Keyword-in-context  : {summary['keyword_hit_rate']} "
          f"({summary['keyword_hit_rate_pct']}%)")
    print(f"  Avg retrieval       : {summary['avg_retrieval_ms']} ms")
    if summary["misses"]:
        print("  Misses:")
        for m in summary["misses"]:
            print(f"    - {m['id']}: got {m['got']}")
    print("-" * 60)

    payload = {
        "ran_at": datetime.now(timezone.utc).isoformat(),
        "top_k": args.top_k,
        "with_llm": args.with_llm,
        "summary": summary,
        "rows": rows,
    }
    RESULTS_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {RESULTS_PATH.relative_to(ROOT)}")
    print("M5 OK — next: M6 deploy + architecture diagram")
    return 0


if __name__ == "__main__":
    sys.exit(main())
