# RAG Document Q&A (`rag-doc-qa`)

[![Milestones](https://img.shields.io/badge/Milestones-M1–M2%20complete-2ea44f)](./MILESTONES.md)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![RAG](https://img.shields.io/badge/GenAI-RAG%20pipeline-7C3AED)](./MILESTONES.md)

Chat over **your PDFs** with retrieval + answers + citations (answer generation lands in M3).

**Author:** [Nilima Satapathy](https://github.com/nilima-satapathy) · Progress board: **[ai-career-journey](https://github.com/nilima-satapathy/ai-career-journey)**

| | |
|---|---|
| **Status** | In progress — **M1–M2 complete** |
| **Stack so far** | Python · pypdf · Chroma · local embeddings (MiniLM) |
| **Planned next** | LLM answers + citations · Streamlit · eval · deploy |
| **Releases** | [milestone tags](https://github.com/nilima-satapathy/rag-doc-qa/releases) |

---

## What’s done

| Milestone | Shipped |
|-----------|---------|
| **M1** | PDF load + configurable overlapping chunks |
| **M2** | Embed chunks → Chroma vector store → similarity search CLI |

---

## Setup (Windows / PowerShell)

```powershell
cd Desktop\Code\rag-doc-qa
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/generate_sample_pdfs.py   # if data/ is empty
```

---

## Milestone 1 — chunking

```powershell
python scripts/run_m1_chunk.py
python scripts/run_m1_chunk.py --chunk-size 400 --chunk-overlap 80
```

| Setting | Default | Meaning |
|---------|---------|---------|
| `chunk_size` | 800 | Max characters per chunk |
| `chunk_overlap` | 120 | Shared chars between neighbors |

---

## Milestone 2 — index + search

```powershell
# 1) Build / rebuild vector index (first run downloads a small embedding model)
python scripts/build_index.py

# 2) Search by meaning (not just keywords)
python scripts/run_m2_search.py "What is ApiClient timeout?"
python scripts/run_m2_search.py "What is Page Object Model?"
python scripts/run_m2_search.py "What is RAG?" --top-k 3

# Interactive mode
python scripts/run_m2_search.py
```

**How it works (simple):**

1. Chunks from M1 are turned into **embeddings** (number fingerprints of meaning).  
2. Stored in **Chroma** under `.chroma/` (local folder).  
3. Your question is embedded too; Chroma returns the **closest chunks**.

No API key required for M2 (local MiniLM via Chroma).

| Setting | Default | Env var |
|---------|---------|---------|
| Chroma folder | `.chroma/` | `RAG_CHROMA_DIR` |
| Collection | `rag_docs` | `RAG_COLLECTION_NAME` |
| Results | 3 | `RAG_TOP_K` |

---

## Sample documents (`data/`)

| File | About |
|------|--------|
| `project1-api-automation-notes.pdf` | ApiClient, 77 tests, negatives |
| `project2-playwright-pom-notes.pdf` | Playwright POM, SauceDemo |
| `rag-and-ai-quality-notes.pdf` | RAG pipeline + eval ideas |

---

## Project layout (M2)

```text
rag-doc-qa/
├── data/                     # sample PDFs
├── scripts/
│   ├── generate_sample_pdfs.py
│   ├── run_m1_chunk.py
│   ├── build_index.py        # M2: embed + store
│   └── run_m2_search.py      # M2: similarity search
└── src/
    ├── config.py
    ├── ingest.py             # M1: load + chunk
    └── retrieve.py           # M2: Chroma index + search
```

**Next (M3):** Take top chunks → ask an LLM to answer **only from that context** + show citations.

---

*Project 3 of [ai-career-journey](https://github.com/nilima-satapathy/ai-career-journey)*
