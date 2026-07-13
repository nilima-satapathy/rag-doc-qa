# Milestones — rag-doc-qa

| Milestone | Description | Status | Date |
|-----------|-------------|--------|------|
| M1 | PDF load + chunking (configurable size) | Done | 2026-07-13 |
| M2 | Embed + Chroma store + similarity search CLI | Done | 2026-07-13 |
| M3 | LLM answer with retrieved context + citations | Done | 2026-07-13 |
| M4 | Streamlit chat UI | Pending | — |
| M5 | Eval script on ≥10 questions | Pending | — |
| M6 | Deploy + README polish + architecture diagram | Pending | — |

## M1 notes

- PDF load + overlapping character chunks
- Demo: `python scripts/run_m1_chunk.py`

## M2 notes

- Chroma PersistentClient + local MiniLM embeddings
- `python scripts/build_index.py` / `python scripts/run_m2_search.py "…"`

## M3 notes

- `src/generate.py`: retrieve → (optional) LLM → answer + citations
- `src/llm_client.py`: SpaceXAI / xAI (`XAI_API_KEY`, model `grok-4.5`)
- Weak retrieval: if best distance > `RAG_MAX_DISTANCE`, skip LLM and say “I don’t know”
- Demo: `python scripts/run_m3_ask.py "What timeout does ApiClient use?"`
- Requires xAI team **credits** at https://console.x.ai (key alone is not enough)
