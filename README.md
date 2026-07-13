# RAG Document Q&A (`rag-doc-qa`)

[![Milestones](https://img.shields.io/badge/Milestones-M1–M3%20complete-2ea44f)](./MILESTONES.md)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![RAG](https://img.shields.io/badge/GenAI-RAG%20pipeline-7C3AED)](./MILESTONES.md)

Ask questions over **your PDFs**. The app **retrieves** relevant chunks, then an **LLM answers only from that context** and shows **citations**.

**Author:** [Nilima Satapathy](https://github.com/nilima-satapathy) · Progress: **[ai-career-journey](https://github.com/nilima-satapathy/ai-career-journey)**

| | |
|---|---|
| **Status** | In progress — **M1–M3 complete** |
| **Stack** | Python · pypdf · Chroma · SpaceXAI/xAI (Grok) · (next: Streamlit) |
| **Releases** | [tags](https://github.com/nilima-satapathy/rag-doc-qa/releases) |

---

## Pipeline so far

```text
PDF → chunks (M1) → embeddings + Chroma (M2) → top-k chunks
                                              → LLM answer + citations (M3)
                                              → Streamlit UI (M4)
```

---

## Setup

```powershell
cd Desktop\Code\rag-doc-qa
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/generate_sample_pdfs.py   # if needed
python scripts/build_index.py
```

### API key (M3)

1. Create a key at [console.x.ai](https://console.x.ai) and add **credits** to your team.  
2. Copy `.env.example` → `.env`  
3. Put only the key (one line):

```env
XAI_API_KEY=xai-your-key-here
```

Never commit `.env`.

---

## Commands

### M1 — chunk

```powershell
python scripts/run_m1_chunk.py
```

### M2 — search

```powershell
python scripts/build_index.py
python scripts/run_m2_search.py "What is RAG?"
```

### M3 — answer + citations

```powershell
python scripts/run_m3_ask.py "What timeout does ApiClient use?"
python scripts/run_m3_ask.py "What is Page Object Model?"
python scripts/run_m3_ask.py "What is the capital of Mars?"  # should not invent from docs
```

**How M3 decides:**

1. Search top-k chunks (default 3).  
2. If best **distance** is worse than `RAG_MAX_DISTANCE` (default `1.05`) → **no LLM**, reply “I don’t know…”.  
3. Else send context + question to **Grok** with a strict “answer only from context” prompt.  
4. Print answer + retrieved citations (file, chunk, snippet, distance).

| Env | Default | Meaning |
|-----|---------|---------|
| `XAI_API_KEY` | (required) | SpaceXAI / xAI key |
| `RAG_LLM_MODEL` | `grok-4.5` | Chat model |
| `RAG_TOP_K` | `3` | Chunks to retrieve |
| `RAG_MAX_DISTANCE` | `1.05` | Weak-retrieval cutoff |

---

## Project layout

```text
rag-doc-qa/
├── data/                 # sample PDFs
├── scripts/
│   ├── run_m1_chunk.py
│   ├── build_index.py
│   ├── run_m2_search.py
│   └── run_m3_ask.py
└── src/
    ├── ingest.py         # load + chunk
    ├── retrieve.py       # Chroma index + search
    ├── llm_client.py     # xAI OpenAI-compatible client
    └── generate.py       # RAG answer + citations
```

**Next (M4):** Streamlit chat website (local browser UI).

---

*Project 3 of [ai-career-journey](https://github.com/nilima-satapathy/ai-career-journey)*
