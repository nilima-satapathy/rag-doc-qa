# Milestones — rag-doc-qa

| Milestone | Description | Status | Date |
|-----------|-------------|--------|------|
| M1 | PDF load + chunking (configurable size) | Done | 2026-07-13 |
| M2 | Embed + Chroma store + similarity search CLI | Done | 2026-07-13 |
| M3 | LLM answer with retrieved context + citations | Done | 2026-07-13 |
| M4 | Streamlit chat UI | Done | 2026-07-14 |
| M5 | Eval script on ≥10 questions | Done | 2026-07-14 |
| M6 | Deploy + README polish + architecture diagram | Ready* | 2026-07-14 |

\*M6 code and docs are complete (auto-index cold start, secrets, diagram, deploy guide).  
**Final step:** publish on [Streamlit Community Cloud](./docs/DEPLOY.md) and paste the live URL into `README.md`.

## M1 notes

- PDF load + overlapping character chunks

## M2 notes

- Chroma + local MiniLM embeddings

## M3 notes

- Grok / Gemini / extractive answer + citations; weak retrieval fallback

## M4 notes

- `streamlit run app.py`

## M5 notes

- `eval/questions.json` — 14 cases (13 in-corpus + 1 out-of-scope)
- `eval/run_eval.py` — retrieval hit@k + keyword-in-context + latency
- Latest local run (top_k=3): **retrieval 13/13 (100%)**, keyword 13/13, avg **~292 ms**
- Results snapshot: `eval/last_results.json`

## M6 notes

- Auto-build index on cold start (`ensure_index` / `bootstrap_index`) for Cloud
- Streamlit secrets support in `src/config.py`
- `.streamlit/config.toml`, `runtime.txt`, `docs/DEPLOY.md`
- Architecture: `diagrams/architecture.svg` + mermaid notes
- README polish (demo placeholder, deploy table, layout)
