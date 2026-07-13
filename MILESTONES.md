# Milestones — rag-doc-qa

| Milestone | Description | Status | Date |
|-----------|-------------|--------|------|
| M1 | PDF load + chunking (configurable size) | Done | 2026-07-13 |
| M2 | Embed + Chroma store + similarity search CLI | Pending | — |
| M3 | LLM answer with retrieved context + citations | Pending | — |
| M4 | Streamlit chat UI | Pending | — |
| M5 | Eval script on ≥10 questions | Pending | — |
| M6 | Deploy + README polish + architecture diagram | Pending | — |

## M1 notes

- `src/ingest.py`: `load_pdf_text`, `chunk_text`, `load_and_chunk_pdf`, `load_and_chunk_all`
- `src/config.py`: `RAG_CHUNK_SIZE` (default 800), `RAG_CHUNK_OVERLAP` (default 120)
- Sample PDFs in `data/` (3 files): Project 1 notes, Project 2 notes, RAG study notes
- Demo: `python scripts/run_m1_chunk.py`
- Generate PDFs: `python scripts/generate_sample_pdfs.py`
