# Milestones — rag-doc-qa

| Milestone | Description | Status | Date |
|-----------|-------------|--------|------|
| M1 | PDF load + chunking (configurable size) | Done | 2026-07-13 |
| M2 | Embed + Chroma store + similarity search CLI | Done | 2026-07-13 |
| M3 | LLM answer with retrieved context + citations | Done | 2026-07-13 |
| M4 | Streamlit chat UI | Done | 2026-07-14 |
| M5 | Eval script on ≥10 questions | Pending | — |
| M6 | Deploy + README polish + architecture diagram | Pending | — |

## M1 notes

- PDF load + overlapping character chunks
- Demo: `python scripts/run_m1_chunk.py`

## M2 notes

- Chroma + local MiniLM embeddings
- `python scripts/build_index.py` / `python scripts/run_m2_search.py "…"`

## M3 notes

- `src/generate.py` + `src/llm_client.py` (xAI / Grok)
- Weak retrieval → “I don’t know” without inventing
- Needs `XAI_API_KEY` + console credits for live LLM

## M4 notes

- `app.py` Streamlit chat UI
- Sidebar: rebuild index, top-k, max distance, doc list, clear chat
- Chat shows answer + expandable citations
- Run: `streamlit run app.py`
