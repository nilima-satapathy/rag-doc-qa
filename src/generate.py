"""
Generate: retrieve context → LLM answer grounded in sources + citations.

Milestone 3.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.config import MAX_DISTANCE, TOP_K
from src.llm_client import chat_completion
from src.retrieve import SearchHit, search

SYSTEM_PROMPT = """You are a careful document Q&A assistant for a RAG portfolio app.

Rules:
1. Answer ONLY using the CONTEXT passages provided by the user message.
2. If the context is missing the answer, say exactly:
   I don't know based on the provided documents.
3. Do NOT invent facts, numbers, or file names that are not in the context.
4. Keep answers concise (a few sentences or short bullets).
5. After the answer, add a line starting with Sources: listing the source file names you used.
"""


@dataclass
class Citation:
    source_file: str
    chunk_index: int
    snippet: str
    distance: float | None


@dataclass
class AnswerResult:
    question: str
    answer: str
    citations: list[Citation] = field(default_factory=list)
    hits: list[SearchHit] = field(default_factory=list)
    used_llm: bool = False
    weak_retrieval: bool = False


def _snippet(text: str, max_len: int = 180) -> str:
    one = " ".join(text.split())
    if len(one) <= max_len:
        return one
    return one[: max_len - 3] + "..."


def _build_context_block(hits: list[SearchHit]) -> str:
    parts: list[str] = []
    for h in hits:
        parts.append(
            f"[source: {h.source_file} | chunk {h.chunk_index}]\n{h.text.strip()}"
        )
    return "\n\n---\n\n".join(parts)


def answer_question(
    question: str,
    *,
    top_k: int = TOP_K,
    max_distance: float = MAX_DISTANCE,
) -> AnswerResult:
    """
    Full M3 pipeline: search → (optional) LLM → answer + citations.
    """
    question = (question or "").strip()
    if not question:
        raise ValueError("question must not be empty")

    hits = search(question, top_k=top_k)
    citations = [
        Citation(
            source_file=h.source_file,
            chunk_index=h.chunk_index,
            snippet=_snippet(h.text),
            distance=h.distance,
        )
        for h in hits
    ]

    best = hits[0].distance if hits and hits[0].distance is not None else None
    weak = best is not None and best > max_distance

    if not hits or weak:
        return AnswerResult(
            question=question,
            answer=(
                "I don't know based on the provided documents. "
                "Retrieval did not find a close enough match in the indexed PDFs."
            ),
            citations=citations,
            hits=hits,
            used_llm=False,
            weak_retrieval=True,
        )

    context = _build_context_block(hits)
    user_msg = (
        f"QUESTION:\n{question}\n\n"
        f"CONTEXT (use only this):\n{context}\n\n"
        "Answer the question using only the context."
    )

    answer = chat_completion(system=SYSTEM_PROMPT, user=user_msg)
    return AnswerResult(
        question=question,
        answer=answer,
        citations=citations,
        hits=hits,
        used_llm=True,
        weak_retrieval=False,
    )


def format_answer(result: AnswerResult) -> str:
    """Pretty terminal output."""
    lines = [
        "=" * 60,
        f"Q: {result.question}",
        "-" * 60,
        result.answer,
        "-" * 60,
        "Retrieved context (citations):",
    ]
    if not result.citations:
        lines.append("  (none)")
    for i, c in enumerate(result.citations, start=1):
        dist = f"{c.distance:.4f}" if c.distance is not None else "n/a"
        lines.append(
            f"  [{i}] {c.source_file}  chunk={c.chunk_index}  distance={dist}"
        )
        lines.append(f"      {c.snippet}")
    lines.append("-" * 60)
    lines.append(
        f"used_llm={result.used_llm}  weak_retrieval={result.weak_retrieval}"
    )
    lines.append("=" * 60)
    return "\n".join(lines)
