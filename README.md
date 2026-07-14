# RAG Document Q&A (`rag-doc-qa`)

[![Milestones](https://img.shields.io/badge/Milestones-M1–M5%20complete-2ea44f)](./MILESTONES.md)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B)](https://streamlit.io)
[![Eval](https://img.shields.io/badge/Retrieval%20hit%403-13%2F13-success)](./eval/last_results.json)

Ask questions over **your PDFs** in a **browser chat**. The app retrieves relevant chunks, answers with an LLM **only from that context**, shows **citations**, and includes a **measured eval set**.

**Author:** [Nilima Satapathy](https://github.com/nilima-satapathy) · Progress: **[ai-career-journey](https://github.com/nilima-satapathy/ai-career-journey)**

| | |
|---|---|
| **Status** | In progress — **M1–M5 complete** |
| **Stack** | Python · pypdf · Chroma · SpaceXAI/xAI · Streamlit |
| **Releases** | [tags](https://github.com/nilima-satapathy/rag-doc-qa/releases) |

---

## Pipeline

```text
PDF → chunks (M1) → Chroma search (M2) → Grok answer + citations (M3)
                                              ↓
                                    Streamlit chat UI (M4)
                                              ↓
                                    Eval (M5) ✅ → Deploy public URL (M6)
```

---

## Evaluation (M5) — required portfolio signal

Golden set: **`eval/questions.json`** (14 cases: 13 in-corpus + 1 out-of-scope).

```powershell
python scripts/build_index.py
python eval/run_eval.py --top-k 3
# optional (needs API credits):
# python eval/run_eval.py --with-llm
```

### Latest local results

| Metric | Result |
|--------|--------|
| # docs indexed | 3 PDFs → 6 chunks |
| # eval questions (scored) | 13 in-corpus (+ 1 negative skipped for doc-hit) |
| **Retrieval hit-rate@3** | **13/13 (100%)** |
| Keyword-in-context | 13/13 (100%) |
| Avg retrieval latency | ~292 ms |
| Known limits | Small corpus; out-of-scope questions still return *some* nearest chunks (LLM “I don’t know” relies on M3 distance/prompt) |

Snapshot: [`eval/last_results.json`](./eval/last_results.json)

**What hit-rate@3 means:** for each question with an expected PDF, that file appears in the **top 3** retrieved sources.

---

## Quick start — website (M4)

```powershell
cd Desktop\Code\rag-doc-qa
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/generate_sample_pdfs.py
python scripts/build_index.py

# .env → XAI_API_KEY=...  (+ credits at https://console.x.ai)
streamlit run app.py
```

Browser: **http://localhost:8501**

---

## CLI

```powershell
python scripts/run_m1_chunk.py
python scripts/build_index.py
python scripts/run_m2_search.py "What is RAG?"
python scripts/run_m3_ask.py "What timeout does ApiClient use?"
python eval/run_eval.py
```

---

## Project layout

```text
rag-doc-qa/
├── app.py
├── data/                     # sample PDFs
├── eval/
│   ├── questions.json        # golden questions
│   ├── run_eval.py
│   └── last_results.json     # last measured run
├── scripts/
└── src/
```

**Next (M6):** public deploy + architecture diagram + final README polish.

---

*Project 3 of [ai-career-journey](https://github.com/nilima-satapathy/ai-career-journey)*
