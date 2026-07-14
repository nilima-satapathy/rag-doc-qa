# RAG Document Q&A (`rag-doc-qa`)

[![Milestones](https://img.shields.io/badge/Milestones-M1–M4%20complete-2ea44f)](./MILESTONES.md)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B)](https://streamlit.io)
[![RAG](https://img.shields.io/badge/GenAI-RAG%20pipeline-7C3AED)](./MILESTONES.md)

Ask questions over **your PDFs** in a **browser chat**. The app retrieves relevant chunks, answers with an LLM **only from that context**, and shows **citations**.

**Author:** [Nilima Satapathy](https://github.com/nilima-satapathy) · Progress: **[ai-career-journey](https://github.com/nilima-satapathy/ai-career-journey)**

| | |
|---|---|
| **Status** | In progress — **M1–M4 complete** (local web UI ready) |
| **Stack** | Python · pypdf · Chroma · SpaceXAI/xAI · **Streamlit** |
| **Releases** | [tags](https://github.com/nilima-satapathy/rag-doc-qa/releases) |

---

## Pipeline

```text
PDF → chunks (M1) → Chroma search (M2) → Grok answer + citations (M3)
                                              ↓
                                    Streamlit chat UI (M4)  ← you use this
                                              ↓
                                    Eval (M5) → Deploy public URL (M6)
```

---

## Quick start — website (M4)

```powershell
cd Desktop\Code\rag-doc-qa
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# One-time: sample PDFs + vector index
python scripts/generate_sample_pdfs.py
python scripts/build_index.py

# API key for answers (copy .env.example → .env)
# XAI_API_KEY=xai-...
# Add credits at https://console.x.ai

streamlit run app.py
```

Browser opens at **http://localhost:8501**

### In the UI

| Feature | What it does |
|---------|----------------|
| Chat box | Ask questions about the PDFs |
| **Sources / citations** | File name, chunk id, distance, snippet |
| **Rebuild index** | Re-chunk + re-embed all `data/*.pdf` |
| Top-k / max distance | Tune retrieval strictness |
| Clear chat | Reset conversation |

**Example questions:**  
*What timeout does ApiClient use?* · *What is Page Object Model?* · *What is RAG?*

---

## CLI (still available)

```powershell
python scripts/run_m1_chunk.py
python scripts/build_index.py
python scripts/run_m2_search.py "What is RAG?"
python scripts/run_m3_ask.py "What timeout does ApiClient use?"
```

---

## API key (M3–M4 answers)

```env
# .env (never commit)
XAI_API_KEY=xai-your-key-here
```

- Create key + **credits**: [console.x.ai](https://console.x.ai)  
- Without credits, the API returns 403; retrieval still works.

---

## Project layout

```text
rag-doc-qa/
├── app.py                 # M4 Streamlit UI
├── data/                  # sample PDFs
├── scripts/
│   ├── run_m1_chunk.py
│   ├── build_index.py
│   ├── run_m2_search.py
│   └── run_m3_ask.py
└── src/
    ├── ingest.py
    ├── retrieve.py
    ├── llm_client.py
    └── generate.py
```

**Next (M5):** Eval script on ≥10 questions with hit-rate numbers in README.

---

*Project 3 of [ai-career-journey](https://github.com/nilima-satapathy/ai-career-journey)*
