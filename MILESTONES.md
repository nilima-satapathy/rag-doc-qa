# Milestones — rag-doc-qa

| Milestone | Description | Status | Date |
|-----------|-------------|--------|------|
| M1 | PDF load + chunking (configurable size) | Done | 2026-07-13 |
| M2 | Embed + Chroma store + similarity search CLI | Done | 2026-07-13 |
| M3 | LLM answer with retrieved context + citations | Pending | — |
| M4 | Streamlit chat UI | Pending | — |
| M5 | Eval script on ≥10 questions | Pending | — |
| M6 | Deploy + README polish + architecture diagram | Pending | — |

## M1 notes

- `src/ingest.py`: load PDF + overlapping character chunks
- Sample PDFs in `data/` (3 files)
- Demo: `python scripts/run_m1_chunk.py`

## M2 notes

- `src/retrieve.py`: `build_index`, `search` (Chroma PersistentClient)
- Default embedding: Chroma `all-MiniLM-L6-v2` (ONNX, local — no API key)
- Store path: `.chroma/` (gitignored)
- Build: `python scripts/build_index.py`
- Search: `python scripts/run_m2_search.py "What is RAG?"`
- Verified: ApiClient → project1 PDF; POM → project2 PDF; RAG → rag notes PDF
