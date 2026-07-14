# DocQ architecture

```mermaid
flowchart LR
  subgraph Ingest["Ingest (M1–M2)"]
    PDF["PDFs in data/"]
    CHUNK["Chunk + overlap"]
    EMB["Embed"]
    CHROMA[("Chroma vector store")]
    PDF --> CHUNK --> EMB --> CHROMA
  end

  subgraph Ask["Ask (M3–M4)"]
    UI["Streamlit DocQ UI"]
    Q["User question"]
    RET["Top‑k similarity search"]
    LLM["Answer engine\nextractive · Gemini · Ollama · xAI"]
    OUT["Answer + citations"]
    UI --> Q --> RET
    CHROMA --> RET
    RET --> LLM --> OUT
    OUT --> UI
  end

  subgraph Quality["Quality (M5)"]
    EVAL["eval/questions.json"]
    HIT["hit@k + latency"]
    EVAL --> HIT
    CHROMA --> HIT
  end
```

## Request path (happy path)

1. User opens DocQ (local or Streamlit Cloud).
2. App **auto-builds** the Chroma index from `data/*.pdf` if empty (deploy cold start).
3. Question → embed → top‑k chunks from Chroma.
4. Answer engine:
   - **extractive** (default free) — best matching PDF passages
   - **gemini / ollama / xai** — grounded generation with citations
5. UI shows answer + source file / chunk / distance.

## Components

| Layer | Module | Role |
|-------|--------|------|
| UI | `app.py`, `src/ui_theme.py` | Chat, settings, themes |
| Ingest | `src/ingest.py` | PDF load + chunk |
| Retrieve | `src/retrieve.py` | Chroma index + search |
| Generate | `src/generate.py`, `src/llm_client.py` | Grounded answer + citations |
| Config | `src/config.py` | Env + Streamlit secrets |
| Eval | `eval/run_eval.py` | Retrieval hit-rate@k |
