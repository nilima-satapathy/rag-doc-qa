"""
Ingest: load PDFs and split into text chunks.

Milestone 1: load + chunk + print (no embeddings yet).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader

from src.config import CHUNK_OVERLAP, CHUNK_SIZE, DATA_DIR


@dataclass
class Chunk:
    """One piece of text from a PDF, ready for embedding later."""

    doc_id: str          # filename stem
    source_file: str     # filename only
    chunk_index: int     # 0-based index within this doc
    text: str
    char_start: int      # offset in full extracted text
    char_end: int


def load_pdf_text(path: Path) -> str:
    """
    Extract text from all pages of a PDF.

    Pages are joined with blank lines so page breaks stay visible in chunks.
    """
    if not path.is_file():
        raise FileNotFoundError(f"PDF not found: {path}")
    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Not a PDF: {path}")

    reader = PdfReader(str(path))
    parts: list[str] = []
    for i, page in enumerate(reader.pages):
        page_text = page.extract_text() or ""
        page_text = page_text.strip()
        if page_text:
            parts.append(f"[Page {i + 1}]\n{page_text}")
    return "\n\n".join(parts).strip()


def chunk_text(
    text: str,
    *,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> list[tuple[int, int, str]]:
    """
    Split text into overlapping character windows.

    Returns list of (start, end, chunk_text).
    Overlap keeps a little context so a sentence is less often cut in half
    with no surrounding words in the next chunk.
    """
    if chunk_size < 50:
        raise ValueError("chunk_size must be at least 50")
    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be >= 0 and < chunk_size")

    text = text.strip()
    if not text:
        return []

    step = chunk_size - chunk_overlap
    spans: list[tuple[int, int, str]] = []
    start = 0
    n = len(text)

    while start < n:
        end = min(start + chunk_size, n)
        # Prefer breaking on whitespace near the end (cleaner chunks)
        if end < n:
            window = text[start:end]
            last_space = window.rfind(" ")
            if last_space > chunk_size // 2:
                end = start + last_space
        piece = text[start:end].strip()
        if piece:
            spans.append((start, end, piece))
        if end >= n:
            break
        start += step

    return spans


def load_and_chunk_pdf(
    path: Path,
    *,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> list[Chunk]:
    """Load one PDF and return Chunk objects."""
    path = Path(path)
    full_text = load_pdf_text(path)
    spans = chunk_text(full_text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    doc_id = path.stem
    source = path.name
    return [
        Chunk(
            doc_id=doc_id,
            source_file=source,
            chunk_index=i,
            text=t,
            char_start=s,
            char_end=e,
        )
        for i, (s, e, t) in enumerate(spans)
    ]


def list_pdfs(data_dir: Path = DATA_DIR) -> list[Path]:
    """All PDFs in the data directory (sorted)."""
    data_dir = Path(data_dir)
    if not data_dir.is_dir():
        return []
    return sorted(data_dir.glob("*.pdf"))


def load_and_chunk_all(
    data_dir: Path = DATA_DIR,
    *,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> list[Chunk]:
    """Load every PDF under data_dir and chunk them."""
    pdfs = list_pdfs(data_dir)
    if not pdfs:
        raise FileNotFoundError(f"No PDFs found in {data_dir}")

    all_chunks: list[Chunk] = []
    for pdf in pdfs:
        all_chunks.extend(
            load_and_chunk_pdf(pdf, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        )
    return all_chunks


def format_chunk_preview(chunk: Chunk, max_chars: int = 200) -> str:
    """One-line-ish preview for terminal printing."""
    preview = chunk.text.replace("\n", " ")
    if len(preview) > max_chars:
        preview = preview[: max_chars - 3] + "..."
    return (
        f"[{chunk.source_file} | chunk {chunk.chunk_index} | "
        f"chars {chunk.char_start}-{chunk.char_end} | {len(chunk.text)} chars]\n"
        f"  {preview}"
    )
